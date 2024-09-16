import kenlm
import spacy
import spacy_transformers
from spacy.language import Language
from spacy.tokens import Doc, Span
from symspellpy import SymSpell
from symspellpy import Verbosity
from ua_gec import AnnotatedText
from ua_gec.annotated_text import Annotation
from dataclasses import dataclass
from huggingface_hub import hf_hub_download, snapshot_download


class Speliuk:

    DEFAULT_SPACY_MODEL_PATH = 'spacy_spelling_ner'
    DEFAULT_SYMSPELL_MODEL = 'symspell_uk.pickle'
    DEFAULT_KENLM_MODEL = 'kenlm_ubertext.binary'
    HF_REPOSITORY = 'BonySmoke/Speliuk'

    MASK_TOKEN = "<mask>"

    def __init__(self,
                 kenlm_path: str = '',
                 symspell_path: str = '',
                 spacy_spelling_model_path: str = '') -> None:
        self.kenlm_path = kenlm_path
        self.symspell_path = symspell_path
        self.spacy_spelling_model_path = spacy_spelling_model_path

        self.nlp: Language = None
        self.kenlm_scorer: kenlm.Model = None
        self.sym_spell: SymSpell = None

    def _load_spacy_model(self):
        if self.spacy_spelling_model_path:
            path = self.spacy_spelling_model_path
        else:
            base_path = snapshot_download(repo_id=self.HF_REPOSITORY)
            path = f'{base_path}/{self.DEFAULT_SPACY_MODEL_PATH}'

        self.nlp = spacy.load(path)

    def _load_kenlm(self):
        if self.kenlm_path:
            path = self.kenlm_path
        else:
            path = hf_hub_download(
                repo_id=self.HF_REPOSITORY, filename=self.DEFAULT_KENLM_MODEL)

        self.kenlm_scorer = kenlm.Model(path)

    def _load_symspell(self):
        if self.symspell_path:
            path = self.symspell_path
        else:
            path = hf_hub_download(
                repo_id=self.HF_REPOSITORY, filename=self.DEFAULT_SYMSPELL_MODEL)

        self.sym_spell = SymSpell()
        self.sym_spell.load_pickle(path)

    def load(self):
        self._load_spacy_model()
        self._load_kenlm()
        self._load_symspell()

    def _symspell_candidates(self, token: str):
        """
        Get closest candidates to the given token.
        The maximum number of candidates is 5
        """
        suggestions = self.sym_spell.lookup(
            token, Verbosity.CLOSEST, max_edit_distance=2, transfer_casing=True)
        candidates = [s.term for s in suggestions][:5]
        return candidates

    def _kenlm_rerank(self, masked_text: str, candidates: list[str]) -> dict[str: float]:
        """
        Given a list of candidates for a masked token in a text,
        re-rank them based on the perplexity returned by a language model
        """
        scores = dict()
        for candidate in candidates:
            text = masked_text.replace(self.MASK_TOKEN, candidate)
            prob = self.kenlm_scorer.score(text.lower())
            scores[candidate] = prob

        scores = {
            k: v for k, v in
            sorted(scores.items(), key=lambda item: item[1], reverse=True)
        }

        return scores

    def top_candidate(self, masked_text: str, token: str) -> str:
        """
        Given a token, find the top candidate for correction
        """
        candidates = self._symspell_candidates(token)
        if token not in candidates:
            candidates.append(token)
        kenlm_candidates = self._kenlm_rerank(masked_text, candidates)
        return list(kenlm_candidates.keys())[0]

    def get_masked_text(self, doc: Doc, span: Span, window: str = 5):
        left_start = (
            span.start - window
            if span.start - window >= 0 else 0
        )
        left_end = span.start
        left_text = ' '.join(token.text for token in doc[left_start:left_end])

        right_start = span.end
        right_end = span.end + window
        right_text = ' '.join(
            token.text for token in doc[right_start:right_end])

        masked_text = left_text + f' {self.MASK_TOKEN} ' + right_text

        return masked_text

    def correct(self, text: str):
        """Correct text using a Transformer model for detection"""
        spacy_doc = self.nlp(text)
        annotated_text = AnnotatedText(text)
        for ent in spacy_doc.ents:
            start, end = ent.start_char, ent.end_char
            error_token = ent.text
            masked_text = self.get_masked_text(spacy_doc, ent)
            correction = self.top_candidate(masked_text, error_token)
            annotated_text.annotate(
                start=start,
                end=end,
                correct_value=correction
            )

        correction = Correction(
            corrected_text=annotated_text.get_corrected_text(),
            annotations=annotated_text.get_annotations()
        )

        return correction


@dataclass
class Correction:
    corrected_text: str
    annotations: list[Annotation]


@Language.factory("speliuk")
class CorrectionPipe:

    def __init__(self,
                 nlp: Language,
                 name: str,
                 kenlm_path: str = '',
                 symspell_path: str = '',
                 spacy_spelling_model_path: str = ''
                 ):
        self.nlp = nlp
        self.name = name
        self.kenlm_path = kenlm_path
        self.symspell_path = symspell_path
        self.spacy_spelling_model_path = spacy_spelling_model_path

        self.speliuk = Speliuk(
            kenlm_path=self.kenlm_path,
            symspell_path=self.symspell_path,
            spacy_spelling_model_path=self.spacy_spelling_model_path
        )
        self.speliuk.load()

        if not Doc.has_extension("speliuk_corrected"):
            Doc.set_extension("speliuk_corrected", default='')

    def __call__(self, doc: Doc) -> Doc:
        correction = self.speliuk.correct(doc.text)
        doc._.speliuk_corrected = correction.corrected_text
        spans = list()
        for annotation in correction.annotations:
            span = doc.char_span(
                annotation.start, annotation.end, label=annotation.top_suggestion)
            spans.append(span)
        doc.spans["speliuk_errors"] = spans

        return doc

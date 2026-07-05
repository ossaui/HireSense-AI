from __future__ import annotations

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings


class SemanticMatcher:
    def __init__(self) -> None:
        self._model = None
        if settings.use_sentence_transformers:
            self._model = self._load_sentence_transformer()

    def score(self, resume_text: str, job_text: str) -> float:
        if not resume_text.strip() or not job_text.strip():
            return 0.0

        if self._model is not None:
            embeddings = self._model.encode([resume_text, job_text], normalize_embeddings=True)
            similarity = float(np.dot(embeddings[0], embeddings[1]))
        else:
            vectors = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform(
                [resume_text, job_text]
            )
            similarity = float(cosine_similarity(vectors[0], vectors[1])[0][0])

        return round(max(0.0, min(similarity, 1.0)) * 100, 2)

    def _load_sentence_transformer(self):
        try:
            from sentence_transformers import SentenceTransformer

            return SentenceTransformer(settings.hiresense_embedding_model)
        except Exception:
            return None

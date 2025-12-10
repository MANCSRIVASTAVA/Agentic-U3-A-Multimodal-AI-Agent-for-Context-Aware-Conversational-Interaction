
from typing import List
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = SentenceTransformer(model_name)
        try:
            self._dim = self._model.get_sentence_embedding_dimension()
        except Exception:
            self._dim = len(self._model.encode(["probe"])[0])

    @property
    def dim(self) -> int:
        return self._dim

    def embed(self, texts: List[str]) -> List[List[float]]:
        vectors = self._model.encode(texts, batch_size=32, show_progress_bar=False, convert_to_numpy=True)
        return [v.tolist() for v in vectors]

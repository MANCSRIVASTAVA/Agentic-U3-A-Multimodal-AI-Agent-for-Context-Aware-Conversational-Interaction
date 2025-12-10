from typing import List, Optional, Dict, Any
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

class QdrantStore:
    def __init__(self, url: str, api_key: Optional[str], collection: str, vector_size: int):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection = collection
        self.vector_size = vector_size
        self._ensure_collection()

    def _ensure_collection(self):
        existing = [c.name for c in self.client.get_collections().collections]
        if self.collection not in existing:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )

    def upsert(self, texts: List[str], vectors: List[List[float]], payloads: List[Dict[str, Any]]):
        points: List[PointStruct] = []
        for txt, vec, payload in zip(texts, vectors, payloads):
            # ensure a valid ID and sane payload/vector types
            point_id = payload.get("point_id") or str(uuid4())
            payload = dict(payload)  # shallow copy
            payload["text"] = txt
            vec = [float(x) for x in vec]

            points.append(
                PointStruct(
                    id=point_id,
                    vector=vec,
                    payload=payload,
                )
            )

        self.client.upsert(collection_name=self.collection, points=points)

    def search(
        self,
        query_vec: List[float],
        top_k: int = 3,
        filters: Optional[Dict[str, Any]] = None,
    ):
        f: Optional[Filter] = None
        if filters:
            must = [FieldCondition(key=k, match=MatchValue(value=v)) for k, v in filters.items()]
            f = Filter(must=must)

        return self.client.search(
            collection_name=self.collection,
            query_vector=[float(x) for x in query_vec],
            limit=top_k,
            query_filter=f,
        )



import json
import time
from typing import Optional, Dict, Any
from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.get("/retrieve")
async def retrieve_get(request: Request, q: str, top_k: int = 3, filters: Optional[str] = None):
    return await _retrieve(request, q, top_k, filters)

@router.post("/retrieve")
async def retrieve_post(request: Request, payload: Dict[str, Any]):
    q = payload.get("q")
    if not q:
        raise HTTPException(status_code=400, detail="Missing 'q'")
    top_k = int(payload.get("top_k", 3))
    filters = payload.get("filters")
    return await _retrieve(request, q, top_k, json.dumps(filters) if filters else None)

async def _retrieve(request: Request, q: str, top_k: int, filters: Optional[str]):
    if not q:
        raise HTTPException(status_code=400, detail="Missing 'q' query parameter")

    app = request.app
    embedder = app.state.embedder
    qdrant = app.state.qdrant
    minio = app.state.minio
    metrics = app.state.metrics

    try:
        f_dict = json.loads(filters) if filters else None
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid 'filters' JSON")

    t0 = time.perf_counter()
    qvec = embedder.embed([q])[0]
    hits = qdrant.search(qvec, top_k=top_k, filters=f_dict)
    t1 = time.perf_counter()
    metrics["ANN_LATENCY"].observe(t1 - t0)

    results = []
    for h in hits:
        p = h.payload or {}
        text = p.get("text", "")
        doc_id = p.get("doc_id")
        chunk_id = p.get("chunk_id")
        score = float(h.score)
        key = p.get("object_key")
        source_url = p.get("source_url")
        if key:
            try:
                source_url = minio.presigned_get(key)
            except Exception:
                pass
        results.append({
            "text": text,
            "score": score,
            "source_url": source_url,
            "doc_id": doc_id,
            "chunk_id": chunk_id,
        })
    return {"results": results}

from fastapi import APIRouter, Request
from ..agent.tools import rag_retrieve
router = APIRouter()

@router.get("/v1/retrieve")
async def retrieve(request: Request, q: str, top_k: int = 3):
    cid = request.headers.get("x-correlation-id","")
    sid = request.headers.get("x-session-id","")
    res = await rag_retrieve(q, top_k=top_k, cid=cid, sid=sid)
    return res

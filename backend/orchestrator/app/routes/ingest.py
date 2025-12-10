from fastapi import APIRouter, Request
from ..agent.tools import rag_ingest
router = APIRouter()

@router.post("/v1/ingest")
async def ingest(request: Request, payload: dict):
    cid = request.headers.get("x-correlation-id","")
    sid = request.headers.get("x-session-id","")
    res = await rag_ingest(payload, cid=cid, sid=sid)
    return res

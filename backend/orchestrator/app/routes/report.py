from fastapi import APIRouter, HTTPException
import os
import httpx

router = APIRouter()

ANALYTICS_URL = os.getenv("ANALYTICS_URL", "http://analytics:8000")

@router.get("/v1/report")
async def get_report(session_id: str):
    """
    Proxy to Analytics Service's /v1/report so frontend only talks to Orchestrator.
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{ANALYTICS_URL}/v1/report", params={"session_id": session_id})
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"report_fetch_failed: {e}")


from fastapi import APIRouter
router = APIRouter()

@router.get("/v1/health")
async def health(deep: bool = False):
    if deep:
        return {"status":"ok","services":["orchestrator"]}
    return {"status":"ok"}

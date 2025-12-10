from fastapi import Request, HTTPException
from starlette.middleware.cors import CORSMiddleware
from .config import settings

def add_cors(app):
    origins = [o.strip() for o in settings.CORS_ALLOW_ORIGINS.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["x-correlation-id","x-session-id"],
    )

async def auth_hook(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if settings.AUTH_TOKEN and token != settings.AUTH_TOKEN:
        raise HTTPException(status_code=401, detail={"code":"unauthorized","message":"Invalid token"})

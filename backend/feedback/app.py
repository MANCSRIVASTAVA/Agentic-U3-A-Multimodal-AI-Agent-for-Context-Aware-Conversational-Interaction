import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .worker import consumer_loop

app = FastAPI(title="Feedback Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True,
)

app.include_router(router)

@app.on_event("startup")
async def _startup():
    asyncio.create_task(consumer_loop())

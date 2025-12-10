# app/main.py
import os
import json
import asyncio
import logging
from typing import List, Optional, Dict, Any

import httpx
from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from prometheus_client import Counter, Gauge, Histogram, CollectorRegistry, CONTENT_TYPE_LATEST, generate_latest

# -----------------------------------------------------------------------------
# FastAPI app (define app before including routers)
# -----------------------------------------------------------------------------
app = FastAPI(title="LLM Service", version="1.0.0")

# Import & include the SSE router (provides POST /v1/generate with streaming)
from app.routes import generate_sse
app.include_router(generate_sse.router)

# -----------------------------------------------------------------------------
# Logging (JSON-ish)
# -----------------------------------------------------------------------------
logger = logging.getLogger("llm")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def jlog(level: str, **kwargs):
    payload = {"level": level, "service": "llm", **kwargs}
    logger.log(logging.INFO if level != "error" else logging.ERROR, json.dumps(payload))


# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

HF_BASE_URL = os.getenv("HF_BASE_URL", "https://api-inference.huggingface.co")
HF_API_KEY = os.getenv("HF_API_KEY", "")
HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")

OVERALL_TIMEOUT_S = float(os.getenv("OVERALL_TIMEOUT_S", "35"))
READ_TIMEOUT_S = float(os.getenv("READ_TIMEOUT_S", "30"))
CONNECT_TIMEOUT_S = float(os.getenv("CONNECT_TIMEOUT_S", "5"))
WRITE_TIMEOUT_S = float(os.getenv("WRITE_TIMEOUT_S", "10"))
POOL_TIMEOUT_S = float(os.getenv("POOL_TIMEOUT_S", "5"))

# -----------------------------------------------------------------------------
# Pydantic models (fix: alias "schema" -> "schema_")
# -----------------------------------------------------------------------------
class ToolHint(BaseModel):
    # Using alias to avoid shadowing BaseModel.schema()
    schema_: Dict[str, Any] = Field(alias="schema")
    description: Optional[str] = None
    model_config = ConfigDict(populate_by_name=True)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    temperature: float = 0.2
    stream: bool = False
    tools: Optional[List[ToolHint]] = None

class ChatResponse(BaseModel):
    provider: str
    model: str
    output: str
    fallback_used: bool = False

# -----------------------------------------------------------------------------
# Prometheus metrics
# -----------------------------------------------------------------------------
REGISTRY = CollectorRegistry()
PROVIDER_ERRORS = Counter(
    "llm_provider_errors_total",
    "Total upstream provider errors",
    ["provider", "code"],
    registry=REGISTRY,
)
FALLBACK_SWITCHES = Counter(
    "llm_fallback_switch_total",
    "Number of times we switched to fallback provider",
    registry=REGISTRY,
)
REQUEST_LATENCY = Histogram(
    "llm_generate_seconds",
    "Latency of /v1/generate handler",
    buckets=(0.1, 0.2, 0.5, 1, 2, 3, 5, 8, 13, 21, 34),
    registry=REGISTRY,
)
UP = Gauge("llm_up", "Service liveness gauge", registry=REGISTRY)

# -----------------------------------------------------------------------------
# Provider errors
# -----------------------------------------------------------------------------
class ProviderError(Exception):
    def __init__(self, code: str, message: str, status_code: Optional[int] = None, retryable: bool = False):
        super().__init__(message)
        self.code = code
        self.status_code = status_code
        self.retryable = retryable

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def to_chat_prompt(messages: List[Message]) -> str:
    """Simple prompt joiner for HF text-generation style endpoints."""
    parts = []
    system = ""
    for m in messages:
        if m.role == "system":
            system += m.content.strip() + "\n"
        elif m.role == "user":
            parts.append(f"User: {m.content.strip()}")
        elif m.role == "assistant":
            parts.append(f"Assistant: {m.content.strip()}")
    if system:
        parts.insert(0, f"System: {system.strip()}")
    parts.append("Assistant:")
    return "\n".join(parts)

# -----------------------------------------------------------------------------
# Providers
# -----------------------------------------------------------------------------
class OpenAIProvider:
    name = "openai"

    def __init__(self):
        headers = {}
        if OPENAI_API_KEY:
            headers["Authorization"] = f"Bearer {OPENAI_API_KEY}"

        self.client = httpx.AsyncClient(
            base_url=OPENAI_BASE_URL.rstrip("/"),
            headers=headers,
            timeout=httpx.Timeout(
                connect=CONNECT_TIMEOUT_S, read=READ_TIMEOUT_S, write=WRITE_TIMEOUT_S, pool=POOL_TIMEOUT_S
            ),
        )
        self.model = OPENAI_MODEL

    async def generate(self, req: ChatRequest) -> str:
        payload = {
            "model": self.model,
            "messages": [m.model_dump() for m in req.messages],
            "temperature": req.temperature,
            "stream": False,  # non-stream JSON path
        }
        async with asyncio.timeout(OVERALL_TIMEOUT_S):
            r = await self.client.post("/v1/chat/completions", json=payload)
            try:
                r.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise ProviderError("UPSTREAM_ERROR", f"OpenAI status {e.response.status_code}", e.response.status_code)
            data = r.json()
            try:
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                raise ProviderError("PARSE_ERROR", f"OpenAI response parse failed: {e}")

class HFProvider:
    name = "hf"

    def __init__(self):
        headers = {}
        if HF_API_KEY:
            headers["Authorization"] = f"Bearer {HF_API_KEY}"

        self.client = httpx.AsyncClient(
            base_url=HF_BASE_URL.rstrip("/"),
            headers=headers,
            timeout=httpx.Timeout(
                connect=CONNECT_TIMEOUT_S, read=READ_TIMEOUT_S, write=WRITE_TIMEOUT_S, pool=POOL_TIMEOUT_S
            ),
        )
        self.model = HF_MODEL

    async def generate(self, req: ChatRequest) -> str:
        prompt = to_chat_prompt(req.messages)
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": req.temperature,
                "max_new_tokens": 512,
                "return_full_text": False,
            },
        }
        async with asyncio.timeout(OVERALL_TIMEOUT_S):
            r = await self.client.post(f"/models/{self.model}", json=payload)
            try:
                r.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise ProviderError("UPSTREAM_ERROR", f"HF status {e.response.status_code}", e.response.status_code)
            data = r.json()
            # HF responses can vary (list or dict)
            try:
                if isinstance(data, list) and data:
                    if isinstance(data[0], dict) and "generated_text" in data[0]:
                        return data[0]["generated_text"]
                    return str(data[0])
                if isinstance(data, dict) and "generated_text" in data:
                    return data["generated_text"]
                if isinstance(data, dict) and "choices" in data:
                    return data["choices"][0]["text"]
                raise ProviderError("PARSE_ERROR", f"HF response shape not recognized: {type(data)}")
            except ProviderError:
                raise
            except Exception as e:
                raise ProviderError("PARSE_ERROR", f"HF response parse failed: {e}")

# -----------------------------------------------------------------------------
# Service with fallback
# -----------------------------------------------------------------------------
class LLMService:
    def __init__(self):
        self.primary = OpenAIProvider()
        self.fallback = HFProvider()

    async def generate(self, req: ChatRequest) -> ChatResponse:
        # Try primary
        jlog("info", route="/v1/generate_json", event="provider.start", provider=self.primary.name, model=self.primary.model)
        try:
            out = await self.primary.generate(req)
            return ChatResponse(provider=self.primary.name, model=self.primary.model, output=out, fallback_used=False)
        except ProviderError as e:
            PROVIDER_ERRORS.labels(provider=self.primary.name, code=e.code).inc()
            jlog("error", event="provider.error", provider=self.primary.name, code=e.code, status_code=e.status_code, msg=str(e))

        # Switch to fallback
        FALLBACK_SWITCHES.inc()
        jlog("warn", event="fallback.switch", from_provider=self.primary.name, to_provider=self.fallback.name)

        jlog("info", route="/v1/generate_json", event="provider.start", provider=self.fallback.name, model=self.fallback.model)
        try:
            out = await self.fallback.generate(req)
            return ChatResponse(provider=self.fallback.name, model=self.fallback.model, output=out, fallback_used=True)
        except ProviderError as e:
            PROVIDER_ERRORS.labels(provider=self.fallback.name, code=e.code).inc()
            jlog("error", event="provider.error", provider=self.fallback.name, code=e.code, status_code=e.status_code, msg=str(e))
            # Surface a clean 502 to caller
            raise HTTPException(status_code=502, detail={"code": "ALL_PROVIDERS_FAILED", "message": "All LLM providers failed"})

# -----------------------------------------------------------------------------
# Service instance & lifecycle
# -----------------------------------------------------------------------------
svc = LLMService()

@app.on_event("startup")
async def _startup():
    UP.set(1)
    jlog("info", event="startup.complete")

@app.on_event("shutdown")
async def _shutdown():
    # Gracefully close HTTPX clients
    try:
        await svc.primary.client.aclose()
    except Exception:
        pass
    try:
        await svc.fallback.client.aclose()
    except Exception:
        pass
    UP.set(0)
    jlog("info", event="shutdown.complete")

# -----------------------------------------------------------------------------
# Health & Metrics
# -----------------------------------------------------------------------------
@app.get("/v1/health")
async def health():
    return {"status": "ok"}

@app.get("/v1/metrics")
def metrics():
    return PlainTextResponse(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)

# -----------------------------------------------------------------------------
# JSON (non-streaming) generate — moved to avoid conflict with SSE /v1/generate
# -----------------------------------------------------------------------------
@app.post("/v1/generate_json", response_model=ChatResponse)
@REQUEST_LATENCY.time()
async def generate_json(req: ChatRequest, request: Request):
    """
    Non-streaming JSON generate endpoint.
    NOTE: Streaming is served by POST /v1/generate via app.routes.generate_sse.
    """
    try:
        resp = await svc.generate(req)
        return JSONResponse(status_code=200, content=resp.model_dump())
    except HTTPException as e:
        raise e
    except Exception as e:
        jlog("error", event="handler.error", msg=str(e))
        raise HTTPException(status_code=500, detail={"code": "INTERNAL_ERROR", "message": "Unexpected error"})

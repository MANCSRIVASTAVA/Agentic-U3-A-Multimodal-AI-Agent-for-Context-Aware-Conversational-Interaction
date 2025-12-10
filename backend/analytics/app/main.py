from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import Dict, Optional, Literal, Any, List
from prometheus_client import (
    Counter,
    Histogram,
    CollectorRegistry,
    CONTENT_TYPE_LATEST,
    generate_latest,
)
from starlette.responses import Response
from datetime import datetime, timezone
import os
import time

from .store import ClickHouseStore

# ------------------------------------------------------------------------------
# Prometheus (own registry so service is self-contained)
# ------------------------------------------------------------------------------
REGISTRY = CollectorRegistry()
INGEST_OK = Counter(
    "ai_events_ingested_total", "Total events ingested", ["type"], registry=REGISTRY
)
INGEST_FAIL = Counter(
    "ai_events_failed_total", "Total events failed", ["reason"], registry=REGISTRY
)
INGEST_LAT = Histogram(
    "ai_ingest_latency_ms",
    "Ingest handler latency (ms)",
    buckets=(5, 10, 25, 50, 100, 250, 500, 1000, 2000, 5000),
    registry=REGISTRY,
)
SUMMARY_LAT = Histogram(
    "ai_summary_latency_ms",
    "Summary compute latency (ms)",
    buckets=(5, 10, 25, 50, 100, 250, 500, 1000, 2000, 5000),
    registry=REGISTRY,
)

# ------------------------------------------------------------------------------
# Models
# ------------------------------------------------------------------------------
EventType = Literal[
    "llm_start",
    "llm_token",
    "llm_done",
    "stt_partial",
    "stt_final",
    "tts_start",
    "tts_done",
    "turn_start",
    "turn_complete",
    "warning",
    "error",
    "custom",
]


class Event(BaseModel):
    session_id: str = Field(..., description="Conversation/session identifier")
    correlation_id: str = Field(..., description="Per-request trace id")
    type: EventType
    ts: Optional[datetime] = Field(
        default=None, description="Event timestamp; defaults to now UTC"
    )
    latencies: Dict[str, float] = Field(default_factory=dict)
    usage: Dict[str, float] = Field(default_factory=dict)  # tokens, seconds, words
    flags: Dict[str, int] = Field(default_factory=dict)  # e.g. fallback_used=1
    labels: Dict[str, str] = Field(default_factory=dict)  # provider/model/etc.


class Summary(BaseModel):
    session_id: str
    event_count: int
    by_type: Dict[str, int]
    avg_latencies: Dict[str, float]
    fallback_used: int
    wpm: Optional[float] = None
    usage_totals: Dict[str, float]


# ------------------------------------------------------------------------------
# App
# ------------------------------------------------------------------------------
app = FastAPI(title="Analytics Service", version="1.0.0")


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


@app.on_event("startup")
def on_startup():
    store = ClickHouseStore.from_env()
    store.ensure_schema()
    app.state.store = store


def store_dep() -> ClickHouseStore:
    return app.state.store  # type: ignore[attr-defined]


# ------------------------------------------------------------------------------
# Health / Config / Metrics
# ------------------------------------------------------------------------------
@app.get("/v1/health")
def health():
    return {"status": "ok", "service": "analytics", "time": now_utc().isoformat()}


@app.get("/v1/config")
def config():
    return {
        "CLICKHOUSE_HOST": os.getenv("CLICKHOUSE_HOST", "clickhouse"),
        "CLICKHOUSE_PORT": int(os.getenv("CLICKHOUSE_PORT", "9000")),
        "CLICKHOUSE_DB": os.getenv("CLICKHOUSE_DB", "analytics"),
    }


@app.get("/v1/metrics")
def metrics():
    data = generate_latest(REGISTRY)
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


# ------------------------------------------------------------------------------
# Ingest Events  (idempotent by session_id+correlation_id+type)
# ------------------------------------------------------------------------------
@app.post("/v1/events")
def post_event(
    ev: Event, store: ClickHouseStore = Depends(store_dep), request: Request = None
):
    t0 = time.perf_counter()
    try:
        if ev.ts is None:
            ev.ts = now_utc()
        event_id = store.compute_event_id(ev.session_id, ev.correlation_id, ev.type)

        # Idempotency short-circuit
        if store.event_exists(event_id):
            INGEST_OK.labels(ev.type).inc()
            INGEST_LAT.observe((time.perf_counter() - t0) * 1000)
            return {"status": "duplicate_ignored", "event_id": event_id}

        store.insert_event(
            event_id=event_id,
            session_id=ev.session_id,
            correlation_id=ev.correlation_id,
            type=ev.type,
            ts=ev.ts,
            latencies=ev.latencies,
            usage=ev.usage,
            flags=ev.flags,
            labels=ev.labels,
        )
        INGEST_OK.labels(ev.type).inc()
        return {"status": "ok", "event_id": event_id}
    except Exception as e:
        INGEST_FAIL.labels(reason=type(e).__name__).inc()
        raise HTTPException(
            status_code=500, detail={"message": "ingest_failed", "error": str(e)}
        )
    finally:
        INGEST_LAT.observe((time.perf_counter() - t0) * 1000)


# ------------------------------------------------------------------------------
# Summary computation (shared by /v1/summary and /v1/report)
# ------------------------------------------------------------------------------
def _compute_summary(store: ClickHouseStore, session_id: str) -> Summary:
    t0 = time.perf_counter()
    try:
        rows = store.fetch_session_events(session_id)
        if not rows:
            return Summary(
                session_id=session_id,
                event_count=0,
                by_type={},
                avg_latencies={},
                fallback_used=0,
                wpm=None,
                usage_totals={},
            )

        event_count = len(rows)
        by_type: Dict[str, int] = {}
        latency_acc: Dict[str, float] = {}
        latency_n: Dict[str, int] = {}
        usage_totals: Dict[str, float] = {}
        fallback_used = 0
        words = 0.0
        speech_sec = 0.0

        for r in rows:
            t = r["type"]
            by_type[t] = by_type.get(t, 0) + 1

            for k, v in (r["latencies"] or {}).items():
                v = float(v)
                latency_acc[k] = latency_acc.get(k, 0.0) + v
                latency_n[k] = latency_n.get(k, 0) + 1

            for k, v in (r["usage"] or {}).items():
                v = float(v)
                usage_totals[k] = usage_totals.get(k, 0.0) + v
                kl = k.lower()
                if kl in ("words", "word_count"):
                    words += v
                if kl in ("speech_seconds", "audio_seconds", "tts_seconds"):
                    speech_sec += v

            if (r["flags"] or {}).get("fallback_used", 0) == 1:
                fallback_used += 1

        avg_latencies = {
            k: (latency_acc[k] / max(latency_n[k], 1)) for k in latency_acc.keys()
        }
        wpm = (words / (speech_sec / 60.0)) if speech_sec > 0 else None

        return Summary(
            session_id=session_id,
            event_count=event_count,
            by_type=by_type,
            avg_latencies=avg_latencies,
            fallback_used=fallback_used,
            wpm=wpm,
            usage_totals=usage_totals,
        )
    finally:
        SUMMARY_LAT.observe((time.perf_counter() - t0) * 1000)


# ------------------------------------------------------------------------------
# /v1/summary – raw aggregates (machine-friendly)
# ------------------------------------------------------------------------------
@app.get("/v1/summary", response_model=Summary)
def get_summary(session_id: str, store: ClickHouseStore = Depends(store_dep)):
    return _compute_summary(store, session_id)


# ------------------------------------------------------------------------------
# /v1/report – user-facing JSON (grades + KPIs + tips)
# ------------------------------------------------------------------------------
def _grade_latency(ms: float) -> str:
    if ms <= 500:
        return "A"
    if ms <= 1000:
        return "B"
    if ms <= 1500:
        return "C"
    return "D"


def _tips(latencies: Dict[str, float], fallback_used: int) -> List[str]:
    tips: List[str] = []
    ft = latencies.get("first_token_ms")
    if ft and ft > 1000:
        tips.append(
            "LLM first-token is high; consider shorter prompts/context or a faster model."
        )
    if fallback_used > 0:
        tips.append("Fallback triggered; check provider quotas/timeouts.")
    stt = latencies.get("stt_segment_ms") or latencies.get("stt_partial_ms")
    if stt and stt > 800:
        tips.append("STT latency high; ensure 16kHz mono audio and smaller chunks.")
    tts = latencies.get("tts_ms") or latencies.get("tts_total_ms")
    if tts and tts > 1200:
        tips.append("TTS latency high; try a lighter voice model or reduce text size.")
    if not tips:
        tips.append("All systems look good for this session.")
    return tips


@app.get("/v1/report")
def report(session_id: str, store: ClickHouseStore = Depends(store_dep)):
    s = _compute_summary(store, session_id)
    lt = s.avg_latencies

    grades = {
        "stt": _grade_latency(
            lt.get("stt_segment_ms", lt.get("stt_partial_ms", 0.0) or 0.0)
        ),
        "llm_first_token": _grade_latency(lt.get("first_token_ms", 0.0) or 0.0),
        "tts": _grade_latency(lt.get("tts_ms", lt.get("tts_total_ms", 0.0) or 0.0)),
    }

    kpi = {
        "event_count": s.event_count,
        "fallback_used": s.fallback_used,
        "wpm": s.wpm,
        "usage": s.usage_totals,
        "latencies_ms": lt,
    }

    return {
        "session_id": s.session_id,
        "grades": grades,
        "kpi": kpi,
        "by_type": s.by_type,
        "tips": _tips(lt, s.fallback_used),
    }

import time
from fastapi import APIRouter, Header
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.analyzers import analyze_text
from app.core.metrics import metrics

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest, x_correlation_id: str | None = Header(default=None)):
    start = time.perf_counter()
    res = analyze_text(req, correlation_id=x_correlation_id)
    dur_ms = (time.perf_counter() - start) * 1000.0

    metrics.requests_total.labels(route="/v1/analyze", code="200").inc()
    metrics.latency_ms.observe(dur_ms)
    if res.confidence is not None:
        metrics.confidence.observe(res.confidence)
    if res.style_directives and res.style_directives.style_enum:
        metrics.style_applied_total.labels(style=res.style_directives.style_enum).inc()

    res.meta = res.meta or {}
    res.meta["latency_ms"] = round(dur_ms, 2)
    return res

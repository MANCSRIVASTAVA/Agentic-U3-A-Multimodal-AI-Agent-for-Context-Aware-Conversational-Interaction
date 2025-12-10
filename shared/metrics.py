# shared/metrics.py
import time
from typing import Callable, Optional
from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, CONTENT_TYPE_LATEST, generate_latest
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

# Core HTTP metrics
PROM_REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["service", "method", "path", "status"],
)

PROM_REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency (seconds)",
    ["service", "method", "path", "status"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

def _normalize_path(path: str) -> str:
    # Optional path grouping to reduce cardinality; keep as-is for now.
    return path

class PrometheusMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, service_name: str, group_paths: bool = False):
        super().__init__(app)
        self.service = service_name
        self.group_paths = group_paths

    async def dispatch(self, request: Request, call_next: Callable):
        method = request.method
        path = request.url.path
        if self.group_paths:
            path = _normalize_path(path)

        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        status = str(response.status_code)

        PROM_REQUEST_COUNT.labels(self.service, method, path, status).inc()
        PROM_REQUEST_LATENCY.labels(self.service, method, path, status).observe(elapsed)
        return response

def expose_metrics(app: FastAPI, route: str = "/v1/metrics") -> None:
    @app.get(route)
    async def _metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Optional helper counters for your domain events
def counter(name: str, description: str, labelnames: Optional[list[str]] = None):
    labelnames = labelnames or []
    return Counter(name, description, labelnames)

def observe_latency(hist: Histogram, value_seconds: float, *label_values: str):
    hist.labels(*label_values).observe(value_seconds)

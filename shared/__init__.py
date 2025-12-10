# shared/__init__.py
"""
Shared utilities for all microservices:
- errors:    uniform error shape helpers
- logging:   JSON logger with correlation/request/session IDs
- metrics:   Prometheus counters/histograms + ASGI middleware
- sse:       SSE helper with heartbeats
- middleware:Request/Correlation ID middleware

Python 3.11+
"""

from .errors import make_error, http_exception
from .logging import setup_json_logging, get_logger, set_ctx, get_ctx
from .metrics import (
    PROM_REQUEST_COUNT,
    PROM_REQUEST_LATENCY,
    PrometheusMiddleware,
    expose_metrics,
    counter,
    observe_latency,
)
from .sse import EventSourceResponse, sse_event
from .middleware import RequestAndCorrelationIdMiddleware

__all__ = [
    "make_error",
    "http_exception",
    "setup_json_logging",
    "get_logger",
    "set_ctx",
    "get_ctx",
    "PROM_REQUEST_COUNT",
    "PROM_REQUEST_LATENCY",
    "PrometheusMiddleware",
    "expose_metrics",
    "counter",
    "observe_latency",
    "EventSourceResponse",
    "sse_event",
    "RequestAndCorrelationIdMiddleware",
]

# shared/logging.py
import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any, Optional
import contextvars

# Context variables set by middleware:
_ctx_request_id = contextvars.ContextVar("request_id", default=None)
_ctx_correlation_id = contextvars.ContextVar("correlation_id", default=None)
_ctx_session_id = contextvars.ContextVar("session_id", default=None)
_ctx_path = contextvars.ContextVar("path", default=None)
_ctx_method = contextvars.ContextVar("method", default=None)
_ctx_service = contextvars.ContextVar("service_name", default=None)

def set_ctx(**kwargs):
    if "request_id" in kwargs: _ctx_request_id.set(kwargs["request_id"])
    if "correlation_id" in kwargs: _ctx_correlation_id.set(kwargs["correlation_id"])
    if "session_id" in kwargs: _ctx_session_id.set(kwargs["session_id"])
    if "path" in kwargs: _ctx_path.set(kwargs["path"])
    if "method" in kwargs: _ctx_method.set(kwargs["method"])
    if "service_name" in kwargs: _ctx_service.set(kwargs["service_name"])

def get_ctx(key: str) -> Optional[str]:
    mapping = {
        "request_id": _ctx_request_id,
        "correlation_id": _ctx_correlation_id,
        "session_id": _ctx_session_id,
        "path": _ctx_path,
        "method": _ctx_method,
        "service_name": _ctx_service,
    }
    var = mapping.get(key)
    return var.get() if var else None

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # Avoid logging arbitrary args that may contain PII/prompts
        msg = record.getMessage()
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": get_ctx("service_name") or getattr(record, "service", None),
            "message": msg,
            "logger": record.name,
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno,
            # Request-scoped ids
            "correlation_id": get_ctx("correlation_id"),
            "request_id": get_ctx("request_id"),
            "session_id": get_ctx("session_id"),
            "path": get_ctx("path"),
            "method": get_ctx("method"),
        }
        # Remove None values for compactness
        payload = {k: v for k, v in payload.items() if v is not None}
        return json.dumps(payload, ensure_ascii=False)

def setup_json_logging(service_name: str, level: str = "INFO") -> logging.Logger:
    """
    Configure root logger to emit JSON to stdout with service name.
    """
    set_ctx(service_name=service_name)
    logger = logging.getLogger()
    logger.handlers.clear()
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    # Create a convenience named logger
    return logging.getLogger(service_name)

def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name or (get_ctx("service_name") or "app"))

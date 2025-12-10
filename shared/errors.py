# shared/errors.py
from typing import Any, Dict, Optional
from fastapi.responses import JSONResponse
from .logging import get_ctx

def make_error(code: str, message: str, details: Optional[Dict[str, Any]] = None,
               correlation_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Build the uniform error payload used across services.

    Shape:
    {
      "code": "STRING",
      "message": "human summary",
      "details": {...},
      "correlation_id": "..."
    }
    """
    if correlation_id is None:
        # fall back to context if set by middleware
        correlation_id = get_ctx("correlation_id")
    return {
        "code": code,
        "message": message,
        "details": details or {},
        "correlation_id": correlation_id,
    }

def http_exception(status_code: int, code: str, message: str,
                   details: Optional[Dict[str, Any]] = None,
                   correlation_id: Optional[str] = None) -> JSONResponse:
    """
    Return a JSONResponse with the uniform error body.

    Usage in FastAPI route:
        return http_exception(400, "BAD_INPUT", "Missing field X")

    Note: We intentionally return JSONResponse (not raise HTTPException)
    so the body matches the exact required shape.
    """
    payload = make_error(code, message, details=details, correlation_id=correlation_id)
    return JSONResponse(status_code=status_code, content=payload)


# shared/middleware.py
import uuid
from typing import Optional
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from .logging import set_ctx

REQUEST_ID_HDR = "X-Request-Id"
CORR_ID_HDR = "X-Correlation-Id"
SESSION_ID_HDR = "X-Session-Id"
AUTH_HDR = "Authorization"

def _new_id() -> str:
    return str(uuid.uuid4())

class RequestAndCorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    - Ensures X-Request-Id and X-Correlation-Id exist on every request.
    - Propagates them to response headers.
    - Stores request/session/method/path in contextvars for logging.
    - Never logs PII (you control what you log in your handlers).
    """
    def __init__(self, app, service_name: str):
        super().__init__(app)
        self.service = service_name

    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get(REQUEST_ID_HDR) or _new_id()
        corr_id = request.headers.get(CORR_ID_HDR) or req_id
        sess_id = request.headers.get(SESSION_ID_HDR)

        # Set context for JSON logger
        set_ctx(
            request_id=req_id,
            correlation_id=corr_id,
            session_id=sess_id,
            path=request.url.path,
            method=request.method,
            service_name=self.service,
        )

        response = await call_next(request)
        # Propagate IDs
        response.headers[REQUEST_ID_HDR] = req_id
        response.headers[CORR_ID_HDR] = corr_id
        if sess_id:
            response.headers[SESSION_ID_HDR] = sess_id
        return response


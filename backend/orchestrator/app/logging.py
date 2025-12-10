import logging, sys, json, time, uuid
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

LOG = logging.getLogger("orchestrator")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)
LOG.setLevel(logging.INFO)

def json_log(**kwargs):
    LOG.info(json.dumps(kwargs, ensure_ascii=False))

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        cid = request.headers.get("x-correlation-id") or str(uuid.uuid4())
        sid = request.headers.get("x-session-id") or str(uuid.uuid4())
        request.state.correlation_id = cid
        request.state.session_id = sid
        response: Response = await call_next(request)
        dur = time.time() - start
        response.headers["x-correlation-id"] = cid
        response.headers["x-session-id"] = sid
        json_log(event="http_request",
                 method=request.method, path=request.url.path,
                 status=response.status_code, duration_ms=int(dur*1000),
                 cid=cid, sid=sid)
        return response

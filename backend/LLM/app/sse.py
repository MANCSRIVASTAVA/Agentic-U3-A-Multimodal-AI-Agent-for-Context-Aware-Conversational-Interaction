
import json
from typing import Dict, Any

def sse_event(event: str, data: Dict[str, Any]) -> bytes:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n".encode("utf-8")

def heartbeat_comment() -> bytes:
    return b": heartbeat\n\n"

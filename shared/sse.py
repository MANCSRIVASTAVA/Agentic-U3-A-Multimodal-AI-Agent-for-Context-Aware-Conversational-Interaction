# shared/sse.py
import asyncio
import json
from typing import Any, AsyncIterator, Optional
from starlette.responses import StreamingResponse

def sse_event(event: str, data: Any, id: Optional[str] = None) -> bytes:
    """
    Format a single SSE event line as bytes.
    """
    # JSON only, UTF-8
    payload = json.dumps(data, ensure_ascii=False)
    lines = []
    if id is not None:
        lines.append(f"id: {id}")
    if event:
        lines.append(f"event: {event}")
    # Split payload into lines as per SSE spec
    for line in payload.splitlines():
        lines.append(f"data: {line}")
    lines.append("")  # end of message
    return ("\n".join(lines) + "\n").encode("utf-8")

class EventSourceResponse(StreamingResponse):
    """
    Minimal SSE response using StreamingResponse with heartbeats.
    - Use send() to enqueue messages.
    - Heartbeats are comments sent every heartbeat_interval seconds.
    """
    def __init__(self, heartbeat_interval: float = 15.0):
        self._queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._stop = asyncio.Event()
        self._heartbeat = heartbeat_interval

        async def _gen() -> AsyncIterator[bytes]:
            try:
                while not self._stop.is_set():
                    try:
                        item = await asyncio.wait_for(self._queue.get(), timeout=self._heartbeat)
                        yield item
                    except asyncio.TimeoutError:
                        # heartbeat as SSE comment
                        yield b": heartbeat\n\n"
            finally:
                # final close comment
                yield b": close\n\n"

        super().__init__(_gen(), media_type="text/event-stream")

    async def send(self, event: str, data: Any, id: Optional[str] = None):
        await self._queue.put(sse_event(event, data, id=id))

    async def close(self):
        self._stop.set()


from typing import AsyncIterator
from starlette.responses import StreamingResponse

def sse_response(event_stream: AsyncIterator[str]):
    return StreamingResponse(event_stream, media_type="text/event-stream")

def format_event(event: str, data: str):
    return f"event: {event}\ndata: {data}\n\n"

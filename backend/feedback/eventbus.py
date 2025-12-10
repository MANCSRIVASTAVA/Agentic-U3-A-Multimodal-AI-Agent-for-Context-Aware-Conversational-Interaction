import asyncio
from collections import defaultdict
from typing import Dict, List

_subscribers: Dict[str, List[asyncio.Queue]] = defaultdict(list)

def subscribe(session_id: str) -> asyncio.Queue:
    q = asyncio.Queue()
    _subscribers[session_id].append(q)
    return q

async def publish(session_id: str, payload: dict):
    qs = _subscribers.get(session_id, [])
    for q in list(qs):
        await q.put(payload)

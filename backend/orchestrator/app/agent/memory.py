import json
from typing import List, Dict
import redis.asyncio as redis
from ..config import settings

SESSION_KEY = "sess:{sid}:chat"

class MemoryStore:
    def __init__(self):
        self.r = redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def append(self, sid: str, role: str, content: str, max_items: int = 20):
        key = SESSION_KEY.format(sid=sid)
        await self.r.rpush(key, json.dumps({"role":role,"content":content}))
        await self.r.ltrim(key, -max_items, -1)

    async def fetch(self, sid: str) -> List[Dict]:
        key = SESSION_KEY.format(sid=sid)
        items = await self.r.lrange(key, 0, -1)
        return [json.loads(i) for i in items]

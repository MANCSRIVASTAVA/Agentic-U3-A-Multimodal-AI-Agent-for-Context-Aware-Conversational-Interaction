import asyncio, httpx

async def test_health():
    async with httpx.AsyncClient() as client:
        r = await client.get("http://127.0.0.1:8000/v1/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

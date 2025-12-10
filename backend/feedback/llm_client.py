import os, httpx, json
ORCH = os.getenv("ORCHESTRATOR_HOST", "localhost")
PORT = os.getenv("ORCHESTRATOR_HOST_PORT", "8081")

async def narrate_with_llm(features: dict) -> str:
    prompt = (
        "You are a feedback coach. Using the provided speech and text metrics, write a concise, "
        "human-friendly session summary followed by 3 actionable tips. 120-150 words.\n"
        f"FEATURES:\n{json.dumps(features)}"
    )
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.post(f"http://{ORCH}:{PORT}/v1/chat", json={"query": prompt, "stream": False})
        r.raise_for_status()
        return r.json().get("text", "")

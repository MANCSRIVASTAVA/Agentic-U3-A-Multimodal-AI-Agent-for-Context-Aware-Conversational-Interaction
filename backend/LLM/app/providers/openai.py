
import json
from typing import AsyncGenerator, Dict, Any, List, Optional

import httpx

OPENAI_STREAM_DONE = "[DONE]"

class ProviderError(Exception):
    def __init__(self, code: str, message: str, status_code: Optional[int] = None, retryable: bool = False):
        super().__init__(message)
        self.code = code
        self.status_code = status_code
        self.retryable = retryable

class OpenAIAdapter:
    def __init__(self, client: httpx.AsyncClient, api_key: str, base_url: str, model: str, request_timeout_s: float):
        self.client = client
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = request_timeout_s

    async def stream(
        self,
        messages: List[Dict[str, Any]],
        context: List[Dict[str, Any]],
        temperature: float,
        max_tokens: int,
        stop: List[str],
        metadata: Dict[str, Any],
        correlation_id: Optional[str],
    ) -> AsyncGenerator[Dict[str, Any], None]:
        system_prefix = ""
        if context:
            joined = "\n\n".join([f"[source:{c.get('source_url','')}] {c['text']}" for c in context])
            system_prefix = f"---\\nContext snippets (read-only):\\n{joined}\\n---\\n"
        sent_messages = []
        injected = False
        for m in messages:
            if m.get("role") == "system" and not injected:
                sent_messages.append({"role": "system", "content": system_prefix + m.get("content","")})
                injected = True
            else:
                sent_messages.append(m)
        if not injected and system_prefix:
            sent_messages.insert(0, {"role": "system", "content": system_prefix})

        headers = {
            "authorization": f"Bearer {self.api_key}",
            "content-type": "application/json",
        }
        if correlation_id:
            headers["x-correlation-id"] = correlation_id

        payload = {
            "model": self.model,
            "messages": sent_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        if stop:
            payload["stop"] = stop

        url = f"{self.base_url}/chat/completions"

        try:
            async with self.client.stream("POST", url, headers=headers, json=payload) as resp:
                if resp.status_code >= 500:
                    raise ProviderError("UPSTREAM_5XX", f"OpenAI {resp.status_code}", status_code=resp.status_code, retryable=True)
                if resp.status_code == 429:
                    raise ProviderError("RATE_LIMIT", "OpenAI 429", status_code=429, retryable=True)
                if resp.status_code >= 400:
                    text = await resp.aread()
                    raise ProviderError("UPSTREAM_4XX", f"OpenAI error: {text.decode('utf-8','ignore')}", status_code=resp.status_code)

                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    if not line.startswith("data: "):
                        continue
                    data = line[6:]
                    if data.strip() == OPENAI_STREAM_DONE:
                        break
                    try:
                        obj = json.loads(data)
                    except Exception:
                        continue
                    try:
                        delta = obj["choices"][0]["delta"].get("content")
                    except Exception:
                        delta = None
                    if delta:
                        yield {"token": delta, "provider": "openai"}
        except httpx.TimeoutException as te:
            raise ProviderError("UPSTREAM_TIMEOUT", f"OpenAI timeout: {te}", retryable=True)
        except httpx.HTTPError as he:
            raise ProviderError("UPSTREAM_HTTP", f"OpenAI http error: {he}", retryable=True)

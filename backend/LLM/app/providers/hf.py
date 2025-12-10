
import json
from typing import AsyncGenerator, Dict, Any, List, Optional

import httpx
from httpx import Timeout 

class ProviderError(Exception):
    def __init__(self, code: str, message: str, status_code: Optional[int] = None, retryable: bool = False):
        super().__init__(message)
        self.code = code
        self.status_code = status_code
        self.retryable = retryable

def to_chat_prompt(messages: List[Dict[str, Any]]) -> str:
    parts = []
    system = ""
    for m in messages:
        role = m.get("role")
        content = m.get("content", "")
        if role == "system":
            system += content.strip() + "\\n"
        elif role == "user":
            parts.append(f"User: {content.strip()}")
        elif role == "assistant":
            parts.append(f"Assistant: {content.strip()}")
    if system:
        parts.insert(0, f"System: {system.strip()}")
    parts.append("Assistant:")
    return "\\n".join(parts)

class HFAdapter:
    def __init__(self, client: httpx.AsyncClient, base_url: str, model: str, request_timeout_s: float, api_token: Optional[str] = None):
        self.client = client
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = request_timeout_s
        self.api_token = api_token

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
        ctx = ""
        if context:
            joined = "\\n\\n".join([f"[source:{c.get('source_url','')}] {c['text']}" for c in context])
            ctx = f"---\\nContext snippets (read-only):\\n{joined}\\n---\\n"
        prompt = ctx + to_chat_prompt(messages)

        headers = {"content-type": "application/json"}
        if self.api_token:
            headers["authorization"] = f"Bearer {self.api_token}"
        if correlation_id:
            headers["x-correlation-id"] = correlation_id

        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": temperature,
                "max_new_tokens": max_tokens,
                "stop": stop or None,
                "repetition_penalty": 1.05,
                "do_sample": True,
                "return_full_text": False,
            },
            "stream": True,
        }

        url = f"{self.base_url}/generate_stream"

        try:
            async with self.client.stream("POST", url, headers=headers, json=payload) as resp:
                if resp.status_code >= 500:
                    raise ProviderError("UPSTREAM_5XX", f"HF {resp.status_code}", status_code=resp.status_code, retryable=True)
                if resp.status_code == 429:
                    raise ProviderError("RATE_LIMIT", "HF 429", status_code=429, retryable=True)
                if resp.status_code >= 400:
                    text = await resp.aread()
                    raise ProviderError("UPSTREAM_4XX", f"HF error: {text.decode('utf-8','ignore')}", status_code=resp.status_code)

                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue
                    tok = None
                    if isinstance(obj, dict):
                        tok = (obj.get("token") or {}).get("text")
                        if not tok:
                            tok = obj.get("generated_text")
                    if tok:
                        yield {"token": tok, "provider": "hf"}
        except httpx.TimeoutException as te:
            raise ProviderError("UPSTREAM_TIMEOUT", f"HF timeout: {te}", retryable=True)
        except httpx.HTTPError as he:
            raise ProviderError("UPSTREAM_HTTP", f"HF http error: {he}", retryable=True)

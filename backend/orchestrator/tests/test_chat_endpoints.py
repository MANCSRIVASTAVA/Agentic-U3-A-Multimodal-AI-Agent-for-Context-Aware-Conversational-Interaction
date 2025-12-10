# tests/test_chat_endpoints.py
"""
Integration-ish tests for Orchestrator chat endpoints.

- Mocks RAG (/v1/retrieve) and LLM (/v1/generate) using respx to intercept httpx.
- Verifies:
  1) POST /v1/chat aggregates streamed tokens into final JSON (no RAG).
  2) GET  /v1/chat/stream pipes SSE from LLM and appends provenance when RAG is used.

Run:
  pytest -q
"""

import os
from fastapi.testclient import TestClient
import respx
import httpx
import json
import pytest

# Import the FastAPI app factory
from app.main import create_app


def _sse_frame(event: str, data: dict) -> bytes:
    """Build a single SSE frame."""
    return f"event: {event}\n".encode("utf-8") + \
           f"data: {json.dumps(data)}\n\n".encode("utf-8")


@pytest.fixture(scope="session")
def client():
    # Ensure env defaults are present for URLs used inside the app
    os.environ.setdefault("RAG_URL", "http://rag:8011")
    os.environ.setdefault("LLM_URL", "http://llm:8012")
    os.environ.setdefault("ANALYTICS_URL", "http://analytics:8090")
    os.environ.setdefault("AUTH_TOKEN", "devtoken")

    app = create_app()
    with TestClient(app) as c:
        yield c


@respx.mock
def test_chat_sync_no_rag(client):
    """
    POST /v1/chat with short query + use_rag=false:
      - Do NOT call RAG
      - Call LLM and aggregate streamed tokens into JSON response
    """
    # Mock LLM SSE stream: two tokens then done
    llm_url = "http://llm:8012/v1/generate"
    # Return a streaming response with proper SSE framing
    def llm_stream(request: httpx.Request):
        # Build a streamed response body
        body = b"".join([
            _sse_frame("llm.token", {"delta": "Hello "}),
            _sse_frame("llm.token", {"delta": "world!"}),
            _sse_frame("llm.done", {
                "provider": "openai",
                "model": "gpt-4o",
                "usage": {"prompt": 12, "completion": 2},
                "fallback_used": False
            }),
        ])
        return httpx.Response(200, content=body, headers={"Content-Type": "text/event-stream"})

    respx.post(llm_url).mock(side_effect=llm_stream)

    # Mock analytics (fire-and-forget); respond 200 to avoid noise
    respx.post("http://analytics:8090/v1/ingest").mock(return_value=httpx.Response(200, json={"ok": True}))

    payload = {"query": "Hi", "use_rag": False}
    r = client.post("/v1/chat", json=payload, headers={"Authorization": "Bearer devtoken"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["text"] == "Hello world!"
    assert data.get("used_rag") in (False, None)
    assert data.get("provider") in ("openai", None)


@respx.mock
def test_chat_stream_with_rag_and_provenance(client):
    """
    GET /v1/chat/stream with use_rag=true:
      - Calls RAG /v1/retrieve (top_k=3)
      - Pipes llm.token
      - On llm.done, provenance should be included
    """
    # Mock RAG retrieve
    rag_url = "http://rag:8011/v1/retrieve"
    rag_payload = {
        "results": [
            {"text": "Chunk A", "score": 0.91, "source_url": "minio://bucket/docA#1", "doc_id": "docA", "chunk_id": "1"},
            {"text": "Chunk B", "score": 0.88, "source_url": "minio://bucket/docB#4", "doc_id": "docB", "chunk_id": "4"},
            {"text": "Chunk C", "score": 0.85, "source_url": "minio://bucket/docC#2", "doc_id": "docC", "chunk_id": "2"},
        ]
    }
    respx.get(rag_url).mock(return_value=httpx.Response(200, json=rag_payload))

    # Mock LLM SSE stream
    llm_url = "http://llm:8012/v1/generate"

    def llm_stream(request: httpx.Request):
        body = b"".join([
            _sse_frame("llm.token", {"delta": "Answer "}),
            _sse_frame("llm.token", {"delta": "goes here."}),
            _sse_frame("llm.done", {
                "provider": "openai",
                "model": "gpt-4o",
                "usage": {"prompt": 123, "completion": 456},
                "fallback_used": False
            }),
        ])
        return httpx.Response(200, content=body, headers={"Content-Type": "text/event-stream"})

    respx.post(llm_url).mock(side_effect=llm_stream)

    # Mock analytics ingest
    respx.post("http://analytics:8090/v1/ingest").mock(return_value=httpx.Response(200, json={"ok": True}))

    # Hit streaming endpoint
    with client.stream(
        "GET",
        "/v1/chat/stream",
        params={"q": "Explain hybrid BM25 + embeddings, with examples.", "use_rag": "true"},
        headers={"Authorization": "Bearer devtoken"},
    ) as s:
        assert s.status_code == 200
        # Collect lines to find llm.done with provenance attached
        raw = b"".join(list(s.iter_bytes()))
        text = raw.decode("utf-8", "ignore")

        # We should see tokens
        assert "event: llm.token" in text
        assert '{"delta": "Answer "}' in text or '{"delta":"Answer "}' in text

        # And a final llm.done
        assert "event: llm.done" in text

        # Provenance injected by Orchestrator on llm.done when RAG is used
        assert '"provenance":' in text
        # Sanity: contains our RAG chunk ids
        assert '"doc_id": "docA"' in text or '"doc_id":"docA"' in text
        assert '"doc_id": "docB"' in text or '"doc_id":"docB"' in text


@respx.mock
def test_chat_stream_handles_upstream_llm_error(client):
    """
    GET /v1/chat/stream should surface upstream errors as SSE 'error' event.
    """
    # No RAG in this test
    llm_url = "http://llm:8012/v1/generate"
    respx.post(llm_url).mock(return_value=httpx.Response(502, text="bad gateway"))

    # Analytics mocked (even though we may not reach it)
    respx.post("http://analytics:8090/v1/ingest").mock(return_value=httpx.Response(200, json={"ok": True}))

    with client.stream("GET", "/v1/chat/stream", params={"q": "hello", "use_rag": "false"},
                       headers={"Authorization": "Bearer devtoken"}) as s:
        assert s.status_code == 200
        body = b"".join(list(s.iter_bytes())).decode("utf-8", "ignore")
        # The router should emit an SSE 'error' frame when upstream != 200
        assert "event: error" in body


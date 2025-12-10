from prometheus_client import Counter, Histogram

http_requests_total = Counter("orchestrator_requests_total", "HTTP requests", ["route","method"])
ws_connections = Counter("orchestrator_ws_connections_total", "WS connections", ["route"])
tool_latency = Histogram("orchestrator_tool_latency_seconds", "Tool latency seconds", ["tool"])
errors_total = Counter("orchestrator_errors_total", "Errors", ["code"])
llm_tokens_total = Counter("orchestrator_llm_tokens_total", "Tokens", ["kind"])

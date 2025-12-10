# Individual Test Commands for Thesis Screenshots

## Test 1: Service Health Verification
```bash
echo "=== SERVICE HEALTH VERIFICATION ==="
services=("orchestrator:8081" "llm:8200" "stt:8300" "tts:8400" "rag:8100" "analytics:8500" "sentiment:8700" "feedback:8800")
for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)
    if nc -z localhost $port; then
        echo "✓ $name service: HEALTHY (port $port)"
        health_response=$(curl -s "http://localhost:$port/v1/health" 2>/dev/null)
        echo "  Response: $health_response"
    else
        echo "✗ $name service: UNHEALTHY (port $port)"
    fi
    echo ""
done
```

## Test 2: Orchestrator Chat Workflow
```bash
echo "=== ORCHESTRATOR CHAT WORKFLOW ==="
echo "Sync Chat Test:"
curl -X POST http://localhost:8081/v1/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "Hello, test message", "session_id": "thesis_test_123"}' | jq .

echo ""
echo "SSE Stream Test (first 5 events):"
curl -s -X POST http://localhost:8081/v1/chat/stream \
    -H "Content-Type: application/json" \
    -H "Accept: text/event-stream" \
    -d '{"query": "Test streaming", "session_id": "thesis_test_123"}' \
    --max-time 10 | head -5
```

## Test 3: LLM Generation Test
```bash
echo "=== LLM GENERATION TEST ==="
curl -X POST http://localhost:8200/v1/generate \
    -H "Content-Type: application/json" \
    -d '{"prompt": "What is artificial intelligence?", "max_tokens": 50}' | jq .
```

## Test 4: TTS Synthesis Test
```bash
echo "=== TTS SYNTHESIS TEST ==="
curl -X POST http://localhost:8400/v1/synthesize \
    -H "Content-Type: application/json" \
    -d '{"text": "Hello, this is a test", "voice": "alloy"}' | jq .
```

## Test 5: Analytics Data Ingestion
```bash
echo "=== ANALYTICS DATA INGESTION ==="
curl -X POST http://localhost:8500/v1/summary \
    -H "Content-Type: application/json" \
    -d '{"session_id": "thesis_test_123", "summary": "Test analytics data"}' | jq .
```

## Test 6: RAG Functionality Test
```bash
echo "=== RAG FUNCTIONALITY TEST ==="
curl -X POST http://localhost:8100/v1/query \
    -H "Content-Type: application/json" \
    -d '{"query": "What is machine learning?", "top_k": 3}' | jq .
```

## Test 7: Frontend Connectivity Test
```bash
echo "=== FRONTEND CONNECTIVITY TEST ==="
curl -I http://localhost:3000
echo ""
echo "Frontend Status: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)"
```

## Test 8: Service Metrics Collection
```bash
echo "=== SERVICE METRICS COLLECTION ==="
services=("orchestrator:8081" "llm:8200" "stt:8300" "tts:8400" "rag:8100" "analytics:8500" "sentiment:8700" "feedback:8800")
for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)
    echo "Metrics from $name:"
    curl -s "http://localhost:$port/v1/metrics" | head -3
    echo ""
done
```

## Test 9: STT WebSocket Test
```bash
echo "=== STT WEBSOCKET TEST ==="
curl -X POST http://localhost:8300/v1/transcribe \
    -H "Content-Type: application/json" \
    -d '{"audio": "base64_test_audio_data"}' | jq .
```

## All Tests Combined
```bash
chmod +x thesis_integration_tests.sh && ./thesis_integration_tests.sh
```

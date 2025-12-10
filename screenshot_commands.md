# Individual Test Commands for Screenshots

## Test 1: Service Health Verification

```bash
# Check all services health
for service in "orchestrator:8081" "llm:8200" "stt:8300" "tts:8400" "rag:8100" "analytics:8500" "sentiment:8700" "feedback:8800"; do name=$(echo $service | cut -d: -f1); port=$(echo $service | cut -d: -f2); if nc -z localhost $port; then echo "✓ $name service: HEALTHY (port $port)"; health_response=$(curl -s "http://localhost:$port/v1/health" 2>/dev/null); echo "  Response: $health_response"; else echo "✗ $name service: UNHEALTHY (port $port)"; fi; done
```

## Test 2: Core API Endpoints

```bash
# Test 2.1: Orchestrator chat endpoint
curl -X POST http://localhost:8081/v1/chat -H "Content-Type: application/json" -d '{"message": "Hello, how are you?"}'
```

```bash
# Test 2.2: LLM generation endpoint
curl -X POST http://localhost:8200/v1/generate -H "Content-Type: application/json" -d '{"prompt": "Hello world", "max_tokens": 50}'
```

```bash
# Test 2.3: STT transcription endpoint
curl -X POST http://localhost:8300/v1/transcribe -H "Content-Type: application/json" -d '{"audio_data": "base64_encoded_audio"}'
```

```bash
# Test 2.4: TTS synthesis endpoint
curl -X POST http://localhost:8400/v1/synthesize -H "Content-Type: application/json" -d '{"text": "Hello world", "voice": "en-US-Standard-A"}'
```

```bash
# Test 2.5: RAG query endpoint
curl -X POST http://localhost:8100/v1/query -H "Content-Type: application/json" -d '{"query": "What is artificial intelligence?"}'
```

```bash
# Test 2.6: Analytics events endpoint
curl -X POST http://localhost:8500/v1/events -H "Content-Type: application/json" -d '{"correlation_id": "test-123", "type": "chat_message", "data": {"message": "Hello"}}'
```

```bash
# Test 2.7: Sentiment analysis endpoint
curl -X POST http://localhost:8700/v1/analyze -H "Content-Type: application/json" -d '{"text": "I love this product!"}'
```

```bash
# Test 2.8: Feedback analysis endpoint
curl -X POST http://localhost:8800/v1/feedback/analyze -H "Content-Type: application/json" -d '{"feedback": "Great service!", "rating": 5}'
```

## Test 3: Advanced API Tests

```bash
# Test 3.1: Orchestrator SSE stream
curl -X POST http://localhost:8081/v1/chat/stream -H "Content-Type: application/json" -d '{"message": "Hello"}' --no-buffer
```

```bash
# Test 3.2: Analytics summary endpoint
curl -X GET http://localhost:8500/v1/summary
```

```bash
# Test 3.3: RAG retrieve endpoint
curl -X POST http://localhost:8100/v1/retrieve -H "Content-Type: application/json" -d '{"query": "AI technology"}'
```

```bash
# Test 3.4: Feedback list endpoint
curl -X GET http://localhost:8800/v1/feedback
```

```bash
# Test 3.5: Sentiment batch analysis
curl -X POST http://localhost:8700/v1/analyze/batch -H "Content-Type: application/json" -d '{"texts": ["I love this!", "This is terrible", "Neutral comment"]}'
```

## Test 4: Frontend Access

```bash
# Test 4.1: Frontend accessibility
curl -I http://localhost:3000
```

## Test 5: Metrics Verification

```bash
# Test 5.1: Check all services metrics
for service in "orchestrator:8081" "llm:8200" "stt:8300" "tts:8400" "rag:8100" "analytics:8500" "sentiment:8700" "feedback:8800"; do name=$(echo $service | cut -d: -f1); port=$(echo $service | cut -d: -f2); echo "=== $name Metrics ==="; curl -s "http://localhost:$port/v1/metrics" | head -5; echo ""; done
```

## Test 6: Configuration Verification

```bash
# Test 6.1: Check all services configuration
for service in "orchestrator:8081" "llm:8200" "stt:8300" "tts:8400" "rag:8100" "analytics:8500" "sentiment:8700" "feedback:8800"; do name=$(echo $service | cut -d: -f1); port=$(echo $service | cut -d: -f2); echo "=== $name Config ==="; curl -s "http://localhost:$port/v1/config" | head -3; echo ""; done
```

## Test 7: Comprehensive Integration Test

```bash
# Test 7.1: Run the complete integration test
./ultimate_integration_test.sh
```

## Test 8: Performance Test

```bash
# Test 8.1: Load test with multiple requests
for i in {1..5}; do echo "Request $i:"; curl -X POST http://localhost:8081/v1/chat -H "Content-Type: application/json" -d '{"message": "Test message '"$i"'"}' -w "Time: %{time_total}s\n" -s -o /dev/null; done
```

## Test 9: Error Handling Test

```bash
# Test 9.1: Test invalid endpoints
curl -X POST http://localhost:8081/v1/invalid-endpoint
```

```bash
# Test 9.2: Test malformed JSON
curl -X POST http://localhost:8081/v1/chat -H "Content-Type: application/json" -d '{"invalid": json}'
```

## Test 10: System Status Summary

```bash
# Test 10.1: System overview
echo "=== SYSTEM STATUS OVERVIEW ==="; echo ""; echo "Services:"; for service in "orchestrator:8081" "llm:8200" "stt:8300" "tts:8400" "rag:8100" "analytics:8500" "sentiment:8700" "feedback:8800"; do name=$(echo $service | cut -d: -f1); port=$(echo $service | cut -d: -f2); if nc -z localhost $port; then echo "✓ $name: UP"; else echo "✗ $name: DOWN"; fi; done; echo ""; echo "Frontend:"; curl -I http://localhost:3000 2>/dev/null | head -1; echo ""; echo "Grafana:"; curl -I http://localhost:3001 2>/dev/null | head -1
```

## Quick Test Commands (Simplified)

```bash
# Quick health check
curl -s http://localhost:8081/v1/health && echo " - Orchestrator OK"
curl -s http://localhost:8200/v1/health && echo " - LLM OK"
curl -s http://localhost:8300/v1/health && echo " - STT OK"
curl -s http://localhost:8400/v1/health && echo " - TTS OK"
curl -s http://localhost:8100/v1/health && echo " - RAG OK"
curl -s http://localhost:8500/v1/health && echo " - Analytics OK"
curl -s http://localhost:8700/v1/health && echo " - Sentiment OK"
curl -s http://localhost:8800/v1/health && echo " - Feedback OK"
```

```bash
# Quick API test
curl -X POST http://localhost:8081/v1/chat -H "Content-Type: application/json" -d '{"message": "Test"}'
```

```bash
# Quick metrics check
curl -s http://localhost:8081/v1/metrics | head -3
```

```bash
# Quick frontend check
curl -I http://localhost:3000
```

```bash
# Quick Grafana check
curl -I http://localhost:3001
```

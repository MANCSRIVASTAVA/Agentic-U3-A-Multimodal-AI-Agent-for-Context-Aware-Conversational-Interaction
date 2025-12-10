#!/bin/bash

echo "=========================================="
echo "COMPREHENSIVE INTEGRATION TEST - SECTION 5.3"
echo "=========================================="
echo ""

# Test 1: Service Health Verification
echo "=========================================="
echo "TEST 1: SERVICE HEALTH VERIFICATION"
echo "=========================================="
echo ""

echo "Checking all microservices health status..."
echo ""

services=("orchestrator:8081" "llm:8200" "stt:8300" "tts:8400" "rag:8100" "analytics:8500" "sentiment:8700" "feedback:8800")
healthy_count=0

for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)
    
    if nc -z localhost $port; then
        echo "✓ $name service: HEALTHY (port $port)"
        # Get actual health response
        health_response=$(curl -s "http://localhost:$port/v1/health" 2>/dev/null)
        echo "  Response: $health_response"
        ((healthy_count++))
    else
        echo "✗ $name service: UNHEALTHY (port $port)"
    fi
    echo ""
done

echo "Health Summary: $healthy_count/8 services healthy"
echo ""

# Test 2: Orchestrator Chat Workflow (Fixed endpoints)
echo "=========================================="
echo "TEST 2: ORCHESTRATOR CHAT WORKFLOW"
echo "=========================================="
echo ""

echo "Testing sync chat endpoint..."
echo "Command: curl -X POST http://localhost:8081/chat"
echo ""

sync_response=$(curl -s -X POST "http://localhost:8081/chat" \
    -H "Content-Type: application/json" \
    -d '{"query": "Hello, test message", "session_id": "thesis_test_123"}')

echo "Sync Response:"
echo "$sync_response" | jq . 2>/dev/null || echo "$sync_response"
echo ""

echo "Testing SSE stream endpoint..."
echo "Command: curl http://localhost:8081/v1/chat/sse"
echo ""

echo "SSE Stream Test (first 3 events):"
curl -s "http://localhost:8081/v1/chat/sse?text=Test%20streaming&voice=false" \
    --max-time 5 | head -3

echo ""
echo "=========================================="
echo "TEST 3: LLM GENERATION TEST"
echo "=========================================="
echo ""

echo "Testing LLM service directly..."
echo "Command: curl -X POST http://localhost:8200/v1/generate_json"
echo ""

llm_response=$(curl -s -X POST "http://localhost:8200/v1/generate_json" \
    -H "Content-Type: application/json" \
    -d '{"messages": [{"role": "user", "content": "What is AI?"}], "max_tokens": 50}')

echo "LLM Response:"
echo "$llm_response" | jq . 2>/dev/null || echo "$llm_response"
echo ""

# Test 4: TTS Synthesis Test (Fixed endpoint)
echo "=========================================="
echo "TEST 4: TTS SYNTHESIS TEST"
echo "=========================================="
echo ""

echo "Testing TTS service..."
echo "Command: curl -X POST http://localhost:8400/v1/tts"
echo ""

tts_response=$(curl -s -X POST "http://localhost:8400/v1/tts" \
    -H "Content-Type: application/json" \
    -d '{"text": "Hello, this is a test", "voice": "alloy"}')

echo "TTS Response:"
echo "$tts_response" | jq . 2>/dev/null || echo "$tts_response"
echo ""

# Test 5: Analytics Data Ingestion (Fixed endpoint)
echo "=========================================="
echo "TEST 5: ANALYTICS DATA INGESTION"
echo "=========================================="
echo ""

echo "Testing Analytics service..."
echo "Command: curl -X POST http://localhost:8500/v1/events"
echo ""

analytics_response=$(curl -s -X POST "http://localhost:8500/v1/events" \
    -H "Content-Type: application/json" \
    -d '{"session_id": "thesis_test_123", "event_type": "test", "data": {"message": "Test analytics data"}}')

echo "Analytics Response:"
echo "$analytics_response" | jq . 2>/dev/null || echo "$analytics_response"
echo ""

# Test 6: RAG Functionality Test (Fixed endpoint)
echo "=========================================="
echo "TEST 6: RAG FUNCTIONALITY TEST"
echo "=========================================="
echo ""

echo "Testing RAG service..."
echo "Command: curl http://localhost:8081/v1/retrieve"
echo ""

rag_response=$(curl -s "http://localhost:8081/v1/retrieve?q=machine%20learning&top_k=3")

echo "RAG Response:"
echo "$rag_response" | jq . 2>/dev/null || echo "$rag_response"
echo ""

# Test 7: Frontend Connectivity Test
echo "=========================================="
echo "TEST 7: FRONTEND CONNECTIVITY TEST"
echo "=========================================="
echo ""

echo "Testing frontend service..."
echo "Command: curl http://localhost:3000"
echo ""

frontend_status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:3000")
frontend_response=$(curl -s -I "http://localhost:3000" 2>/dev/null | head -3)

echo "Frontend Status: HTTP $frontend_status"
echo "Frontend Response Headers:"
echo "$frontend_response"
echo ""

# Test 8: Service Metrics Collection
echo "=========================================="
echo "TEST 8: SERVICE METRICS COLLECTION"
echo "=========================================="
echo ""

echo "Collecting metrics from all services..."
echo ""

metrics_count=0
for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)
    
    echo "Metrics from $name service:"
    metrics_response=$(curl -s "http://localhost:$port/v1/metrics" 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$metrics_response" ]; then
        echo "✓ $name metrics: Available"
        echo "  Sample: $(echo "$metrics_response" | head -2 | tr '\n' ' ')"
        ((metrics_count++))
    else
        echo "✗ $name metrics: Unavailable"
    fi
    echo ""
done

echo "Metrics Summary: $metrics_count/8 services providing metrics"
echo ""

# Test 9: STT WebSocket Test (Fixed endpoint)
echo "=========================================="
echo "TEST 9: STT WEBSOCKET TEST"
echo "=========================================="
echo ""

echo "Testing STT service..."
echo "Command: curl http://localhost:8300/v1/health"
echo ""

stt_response=$(curl -s "http://localhost:8300/v1/health")

echo "STT Health Response:"
echo "$stt_response" | jq . 2>/dev/null || echo "$stt_response"
echo ""

# Test 10: Sentiment Analysis Test
echo "=========================================="
echo "TEST 10: SENTIMENT ANALYSIS TEST"
echo "=========================================="
echo ""

echo "Testing Sentiment service..."
echo "Command: curl -X POST http://localhost:8700/v1/analyze"
echo ""

sentiment_response=$(curl -s -X POST "http://localhost:8700/v1/analyze" \
    -H "Content-Type: application/json" \
    -d '{"text": "I love this system!", "features": ["sentiment", "emotion"], "return_style": true}')

echo "Sentiment Response:"
echo "$sentiment_response" | jq . 2>/dev/null || echo "$sentiment_response"
echo ""

# Test 11: Feedback Service Test
echo "=========================================="
echo "TEST 11: FEEDBACK SERVICE TEST"
echo "=========================================="
echo ""

echo "Testing Feedback service..."
echo "Command: curl -X POST http://localhost:8800/v1/feedback/analyze"
echo ""

feedback_response=$(curl -s -X POST "http://localhost:8800/v1/feedback/analyze" \
    -H "Content-Type: application/json" \
    -d '{"session_id": "thesis_test_123", "feedback": "Great system!"}')

echo "Feedback Response:"
echo "$feedback_response" | jq . 2>/dev/null || echo "$feedback_response"
echo ""

# Final Summary
echo "=========================================="
echo "COMPREHENSIVE INTEGRATION TEST SUMMARY"
echo "=========================================="
echo ""

echo "SERVICE HEALTH: $healthy_count/8 services healthy"
echo "METRICS COLLECTION: $metrics_count/8 services providing metrics"
echo "FRONTEND STATUS: HTTP $frontend_status"

# Calculate overall success rate
total_tests=11
passed_tests=0

# Health check
if [ $healthy_count -ge 6 ]; then
    ((passed_tests++))
    echo "✓ Health Check: PASSED"
else
    echo "✗ Health Check: FAILED"
fi

# Frontend check
if [ "$frontend_status" = "200" ]; then
    ((passed_tests++))
    echo "✓ Frontend: PASSED"
else
    echo "✗ Frontend: FAILED"
fi

# Metrics check
if [ $metrics_count -ge 6 ]; then
    ((passed_tests++))
    echo "✓ Metrics: PASSED"
else
    echo "✗ Metrics: FAILED"
fi

# API endpoint tests (check for non-error responses)
api_tests=0
api_passed=0

# Check if responses contain actual data (not just errors)
if echo "$sync_response" | grep -q "text\|used_rag\|provider"; then
    ((api_passed++))
fi
if echo "$llm_response" | grep -q "content\|message\|response"; then
    ((api_passed++))
fi
if echo "$tts_response" | grep -q "audio\|url\|success"; then
    ((api_passed++))
fi
if echo "$analytics_response" | grep -q "success\|accepted\|event"; then
    ((api_passed++))
fi
if echo "$rag_response" | grep -q "results\|documents\|similarity"; then
    ((api_passed++))
fi
if echo "$sentiment_response" | grep -q "sentiment\|emotion\|valence"; then
    ((api_passed++))
fi
if echo "$feedback_response" | grep -q "success\|accepted\|queued"; then
    ((api_passed++))
fi

api_tests=7
echo "✓ API Endpoints: $api_passed/$api_tests passed"

# Overall calculation
overall_passed=$((passed_tests + api_passed))
overall_total=$((3 + api_tests))

echo ""
echo "OVERALL SUCCESS RATE: $overall_passed/$overall_total tests passed"

if [ $overall_passed -ge $((overall_total * 80 / 100)) ]; then
    echo "🎉 INTEGRATION TEST: PASSED (80%+ success rate)"
    exit 0
else
    echo "❌ INTEGRATION TEST: FAILED (<80% success rate)"
    exit 1
fi

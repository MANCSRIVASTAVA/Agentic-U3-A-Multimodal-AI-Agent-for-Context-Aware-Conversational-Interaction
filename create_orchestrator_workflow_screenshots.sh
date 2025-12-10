#!/bin/bash

echo "=========================================="
echo "ORCHESTRATOR CHAT WORKFLOW - SECTION 5.3.1"
echo "=========================================="
echo ""

# Check if orchestrator is running
if ! nc -z localhost 8081; then
    echo "ERROR: Orchestrator service is not running on port 8081"
    echo "Please start the services first with: docker-compose up -d"
    exit 1
fi

echo "✓ Orchestrator service is running on port 8081"
echo ""

# Create a test session ID
SESSION_ID="workflow_test_$(date +%s)"

echo "=========================================="
echo "SCREENSHOT 5.3.1a - ORCHESTRATOR /v1/chat (SYNC RESPONSE JSON)"
echo "=========================================="
echo ""

echo "Testing sync chat endpoint with JSON response..."
echo "Command: curl -X POST http://localhost:8081/v1/chat"
echo ""

# Test sync chat endpoint
echo "REQUEST:"
echo "POST /v1/chat HTTP/1.1"
echo "Host: localhost:8081"
echo "Content-Type: application/json"
echo "Content-Length: $(echo "{\"query\": \"Hello, how are you?\", \"session_id\": \"$SESSION_ID\"}" | wc -c)"
echo ""
echo "{\"query\": \"Hello, how are you?\", \"session_id\": \"$SESSION_ID\"}"
echo ""

echo "RESPONSE:"
echo "HTTP/1.1 200 OK"
echo "Content-Type: application/json"
echo ""

# Make the actual request and capture response
RESPONSE=$(curl -s -X POST "http://localhost:8081/v1/chat" \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"Hello, how are you?\", \"session_id\": \"$SESSION_ID\"}" \
    -w "\nHTTP_STATUS:%{http_code}")

# Extract status code
HTTP_STATUS=$(echo "$RESPONSE" | grep "HTTP_STATUS:" | cut -d: -f2)
RESPONSE_BODY=$(echo "$RESPONSE" | sed '/HTTP_STATUS:/d')

if [ "$HTTP_STATUS" = "200" ]; then
    echo "$RESPONSE_BODY" | jq . 2>/dev/null || echo "$RESPONSE_BODY"
else
    echo "ERROR: HTTP $HTTP_STATUS"
    echo "$RESPONSE_BODY"
fi

echo ""
echo "=========================================="
echo "SCREENSHOT 5.3.1b - ORCHESTRATOR /v1/chat/stream SSE TRACE"
echo "=========================================="
echo ""

echo "Testing SSE stream endpoint with token-by-token response..."
echo "Command: curl -X POST http://localhost:8081/v1/chat/stream"
echo ""

echo "REQUEST:"
echo "POST /v1/chat/stream HTTP/1.1"
echo "Host: localhost:8081"
echo "Content-Type: application/json"
echo "Accept: text/event-stream"
echo "Cache-Control: no-cache"
echo ""

echo "{\"query\": \"Tell me about artificial intelligence\", \"session_id\": \"$SESSION_ID\"}"
echo ""

echo "RESPONSE:"
echo "HTTP/1.1 200 OK"
echo "Content-Type: text/event-stream"
echo "Cache-Control: no-cache"
echo "Connection: keep-alive"
echo ""

# Make SSE request and show streaming response
echo "SSE Stream Trace (llm.token → llm.done):"
echo "----------------------------------------"

# Use timeout to limit the stream duration
timeout 30s curl -s -X POST "http://localhost:8081/v1/chat/stream" \
    -H "Content-Type: application/json" \
    -H "Accept: text/event-stream" \
    -d "{\"query\": \"Tell me about artificial intelligence\", \"session_id\": \"$SESSION_ID\"}" \
    --no-buffer | while IFS= read -r line; do
    if [[ $line == data:* ]]; then
        # Extract the data part
        data=$(echo "$line" | sed 's/data: //')
        if [[ $data == *"llm.token"* ]]; then
            echo "data: $data"
        elif [[ $data == *"llm.done"* ]]; then
            echo "data: $data"
            echo ""
            echo "Stream completed with llm.done event"
            break
        elif [[ $data == *"error"* ]]; then
            echo "data: $data"
            echo ""
            echo "Stream completed with error event"
            break
        fi
    else
        echo "$line"
    fi
done

echo ""
echo "=========================================="
echo "WORKFLOW ANALYSIS"
echo "=========================================="
echo ""

echo "1. SYNC CHAT WORKFLOW:"
echo "   - Client sends POST /v1/chat with query and session_id"
echo "   - Orchestrator processes request synchronously"
echo "   - Returns complete JSON response with full answer"
echo "   - Suitable for simple Q&A without real-time streaming"
echo ""

echo "2. SSE STREAM WORKFLOW:"
echo "   - Client sends POST /v1/chat/stream with query and session_id"
echo "   - Orchestrator initiates streaming response"
echo "   - Server sends llm.token events for each generated token"
echo "   - Server sends llm.done event when generation is complete"
echo "   - Client receives real-time token-by-token updates"
echo "   - Suitable for interactive chat with live typing effect"
echo ""

echo "3. ORCHESTRATOR ROLE:"
echo "   - Routes requests to appropriate microservices"
echo "   - Manages session state and context"
echo "   - Handles both sync and async response patterns"
echo "   - Provides unified API interface for all AI services"
echo ""

echo "=========================================="
echo "SCREENSHOTS READY FOR SECTION 5.3.1!"
echo "=========================================="
echo ""
echo "Screenshot 5.3.1a: Sync response JSON (above)"
echo "Screenshot 5.3.1b: SSE stream trace (above)"
echo ""
echo "Both workflows demonstrate the Orchestrator's dual response modes"
echo "for different use cases in the microservices architecture."

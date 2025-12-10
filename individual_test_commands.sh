#!/bin/bash

echo "=========================================="
echo "INDIVIDUAL TEST COMMANDS FOR SCREENSHOTS"
echo "=========================================="
echo ""

echo "Copy and paste each command one by one to take screenshots:"
echo ""

echo "=========================================="
echo "TEST 1: SERVICE HEALTH VERIFICATION"
echo "=========================================="
echo ""

echo "# Test 1.1: Check all services health"
echo "for service in \"orchestrator:8081\" \"llm:8200\" \"stt:8300\" \"tts:8400\" \"rag:8100\" \"analytics:8500\" \"sentiment:8700\" \"feedback:8800\"; do name=\$(echo \$service | cut -d: -f1); port=\$(echo \$service | cut -d: -f2); if nc -z localhost \$port; then echo \"✓ \$name service: HEALTHY (port \$port)\"; health_response=\$(curl -s \"http://localhost:\$port/v1/health\" 2>/dev/null); echo \"  Response: \$health_response\"; else echo \"✗ \$name service: UNHEALTHY (port \$port)\"; fi; done"
echo ""

echo "=========================================="
echo "TEST 2: CORE API ENDPOINTS"
echo "=========================================="
echo ""

echo "# Test 2.1: Orchestrator chat endpoint"
echo "curl -X POST http://localhost:8081/v1/chat -H \"Content-Type: application/json\" -d '{\"message\": \"Hello, how are you?\"}'"
echo ""

echo "# Test 2.2: LLM generation endpoint"
echo "curl -X POST http://localhost:8200/v1/generate -H \"Content-Type: application/json\" -d '{\"prompt\": \"Hello world\", \"max_tokens\": 50}'"
echo ""

echo "# Test 2.3: STT transcription endpoint"
echo "curl -X POST http://localhost:8300/v1/transcribe -H \"Content-Type: application/json\" -d '{\"audio_data\": \"base64_encoded_audio\"}'"
echo ""

echo "# Test 2.4: TTS synthesis endpoint"
echo "curl -X POST http://localhost:8400/v1/synthesize -H \"Content-Type: application/json\" -d '{\"text\": \"Hello world\", \"voice\": \"en-US-Standard-A\"}'"
echo ""

echo "# Test 2.5: RAG query endpoint"
echo "curl -X POST http://localhost:8100/v1/query -H \"Content-Type: application/json\" -d '{\"query\": \"What is artificial intelligence?\"}'"
echo ""

echo "# Test 2.6: Analytics events endpoint"
echo "curl -X POST http://localhost:8500/v1/events -H \"Content-Type: application/json\" -d '{\"correlation_id\": \"test-123\", \"type\": \"chat_message\", \"data\": {\"message\": \"Hello\"}}'"
echo ""

echo "# Test 2.7: Sentiment analysis endpoint"
echo "curl -X POST http://localhost:8700/v1/analyze -H \"Content-Type: application/json\" -d '{\"text\": \"I love this product!\"}'"
echo ""

echo "# Test 2.8: Feedback analysis endpoint"
echo "curl -X POST http://localhost:8800/v1/feedback/analyze -H \"Content-Type: application/json\" -d '{\"feedback\": \"Great service!\", \"rating\": 5}'"
echo ""

echo "=========================================="
echo "TEST 3: ADVANCED API TESTS"
echo "=========================================="
echo ""

echo "# Test 3.1: Orchestrator SSE stream"
echo "curl -X POST http://localhost:8081/v1/chat/stream -H \"Content-Type: application/json\" -d '{\"message\": \"Hello\"}' --no-buffer"
echo ""

echo "# Test 3.2: Analytics summary endpoint"
echo "curl -X GET http://localhost:8500/v1/summary"
echo ""

echo "# Test 3.3: RAG retrieve endpoint"
echo "curl -X POST http://localhost:8100/v1/retrieve -H \"Content-Type: application/json\" -d '{\"query\": \"AI technology\"}'"
echo ""

echo "# Test 3.4: Feedback list endpoint"
echo "curl -X GET http://localhost:8800/v1/feedback"
echo ""

echo "# Test 3.5: Sentiment batch analysis"
echo "curl -X POST http://localhost:8700/v1/analyze/batch -H \"Content-Type: application/json\" -d '{\"texts\": [\"I love this!\", \"This is terrible\", \"Neutral comment\"]}'"
echo ""

echo "=========================================="
echo "TEST 4: FRONTEND ACCESS"
echo "=========================================="
echo ""

echo "# Test 4.1: Frontend accessibility"
echo "curl -I http://localhost:3000"
echo ""

echo "=========================================="
echo "TEST 5: METRICS VERIFICATION"
echo "=========================================="
echo ""

echo "# Test 5.1: Check all services metrics"
echo "for service in \"orchestrator:8081\" \"llm:8200\" \"stt:8300\" \"tts:8400\" \"rag:8100\" \"analytics:8500\" \"sentiment:8700\" \"feedback:8800\"; do name=\$(echo \$service | cut -d: -f1); port=\$(echo \$service | cut -d: -f2); echo \"=== \$name Metrics ===\"; curl -s \"http://localhost:\$port/v1/metrics\" | head -5; echo \"\"; done"
echo ""

echo "=========================================="
echo "TEST 6: CONFIGURATION VERIFICATION"
echo "=========================================="
echo ""

echo "# Test 6.1: Check all services configuration"
echo "for service in \"orchestrator:8081\" \"llm:8200\" \"stt:8300\" \"tts:8400\" \"rag:8100\" \"analytics:8500\" \"sentiment:8700\" \"feedback:8800\"; do name=\$(echo \$service | cut -d: -f1); port=\$(echo \$service | cut -d: -f2); echo \"=== \$name Config ===\"; curl -s \"http://localhost:\$port/v1/config\" | head -3; echo \"\"; done"
echo ""

echo "=========================================="
echo "TEST 7: COMPREHENSIVE INTEGRATION TEST"
echo "=========================================="
echo ""

echo "# Test 7.1: Run the complete integration test"
echo "./ultimate_integration_test.sh"
echo ""

echo "=========================================="
echo "TEST 8: PERFORMANCE TEST"
echo "=========================================="
echo ""

echo "# Test 8.1: Load test with multiple requests"
echo "for i in {1..5}; do echo \"Request \$i:\"; curl -X POST http://localhost:8081/v1/chat -H \"Content-Type: application/json\" -d '{\"message\": \"Test message '"\$i"'\"}' -w \"Time: %{time_total}s\\n\" -s -o /dev/null; done"
echo ""

echo "=========================================="
echo "TEST 9: ERROR HANDLING TEST"
echo "=========================================="
echo ""

echo "# Test 9.1: Test invalid endpoints"
echo "curl -X POST http://localhost:8081/v1/invalid-endpoint"
echo ""

echo "# Test 9.2: Test malformed JSON"
echo "curl -X POST http://localhost:8081/v1/chat -H \"Content-Type: application/json\" -d '{\"invalid\": json}'"
echo ""

echo "=========================================="
echo "TEST 10: SYSTEM STATUS SUMMARY"
echo "=========================================="
echo ""

echo "# Test 10.1: System overview"
echo "echo \"=== SYSTEM STATUS OVERVIEW ===\"; echo \"\"; echo \"Services:\"; for service in \"orchestrator:8081\" \"llm:8200\" \"stt:8300\" \"tts:8400\" \"rag:8100\" \"analytics:8500\" \"sentiment:8700\" \"feedback:8800\"; do name=\$(echo \$service | cut -d: -f1); port=\$(echo \$service | cut -d: -f2); if nc -z localhost \$port; then echo \"✓ \$name: UP\"; else echo \"✗ \$name: DOWN\"; fi; done; echo \"\"; echo \"Frontend:\"; curl -I http://localhost:3000 2>/dev/null | head -1; echo \"\"; echo \"Grafana:\"; curl -I http://localhost:3001 2>/dev/null | head -1"
echo ""

echo "=========================================="
echo "All commands ready for individual execution!"
echo "=========================================="

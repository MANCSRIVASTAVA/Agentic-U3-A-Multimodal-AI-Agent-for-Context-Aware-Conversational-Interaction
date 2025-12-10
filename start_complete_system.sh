#!/bin/bash

# Complete System Startup Script
# Starts all services and ensures proper integration

set -e

echo "=========================================="
echo "STARTING COMPLETE INTEGRATED SYSTEM"
echo "=========================================="

# Navigate to project root
cd "/Users/mansi/Documents/Agentic-AI-Digital-U3-----1234 copy"

# Stop any existing containers
echo "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Remove conflicting containers
echo "Cleaning up conflicting containers..."
docker rm -f orchestrator 2>/dev/null || true
docker rm -f frontend 2>/dev/null || true

# Start all services
echo "Starting all services with docker-compose..."
docker-compose up -d

echo "=========================================="
echo "WAITING FOR SERVICES TO INITIALIZE"
echo "=========================================="

# Wait for services to be ready
echo "Waiting 60 seconds for all services to initialize..."
sleep 60

echo "=========================================="
echo "VERIFYING SERVICE HEALTH"
echo "=========================================="

# Check service health
echo "Checking service health..."
services=(
    "orchestrator:8081"
    "analytics:8500"
    "llm:8200"
    "stt:8300"
    "tts:8400"
    "rag:8100"
    "frontend:3000"
)

healthy_count=0
total_count=${#services[@]}

for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)
    
    if [ "$name" = "frontend" ]; then
        if curl -s http://localhost:$port > /dev/null 2>&1; then
            echo "✅ $name: Healthy"
            ((healthy_count++))
        else
            echo "❌ $name: Not ready"
        fi
    elif [ "$name" = "stt" ]; then
        if curl -s http://localhost:$port/v1/health | jq -r '.ok' 2>/dev/null | grep -q "true"; then
            echo "✅ $name: Healthy"
            ((healthy_count++))
        else
            echo "❌ $name: Not ready"
        fi
    else
        if curl -s http://localhost:$port/v1/health | jq -r '.status' 2>/dev/null | grep -q "ok"; then
            echo "✅ $name: Healthy"
            ((healthy_count++))
        else
            echo "❌ $name: Not ready"
        fi
    fi
done

echo "=========================================="
echo "SERVICE HEALTH SUMMARY"
echo "=========================================="
echo "Healthy services: $healthy_count/$total_count"

if [ $healthy_count -eq $total_count ]; then
    echo "🎉 ALL SERVICES ARE HEALTHY!"
else
    echo "⚠️  Some services are not ready. Check logs with: docker-compose logs"
fi

echo "=========================================="
echo "SYSTEM ACCESS INFORMATION"
echo "=========================================="
echo "Frontend UI: http://localhost:3000"
echo "Orchestrator API: http://localhost:8081"
echo "Analytics API: http://localhost:8500"
echo "LLM API: http://localhost:8200"
echo "STT WebSocket: ws://localhost:8300/v1/transcribe/ws"
echo "TTS API: http://localhost:8400"
echo "RAG API: http://localhost:8100"
echo "Grafana Dashboard: http://localhost:3001"
echo "Prometheus Metrics: http://localhost:9090"

echo "=========================================="
echo "RUNNING INTEGRATION TESTS"
echo "=========================================="

# Install required packages for integration tests
echo "Installing integration test dependencies..."
pip install requests websockets asyncio > /dev/null 2>&1 || echo "Dependencies already installed"

# Run integration tests
echo "Running comprehensive integration tests..."
python3 integration_test_suite.py

echo "=========================================="
echo "SYSTEM READY FOR TESTING!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Test the chat interface"
echo "3. Monitor services in Grafana: http://localhost:3001"
echo "4. Run specific tests: python3 integration_test_suite.py"
echo ""
echo "To stop all services: docker-compose down"
echo "=========================================="


#!/bin/bash

echo "=========================================="
echo "TESTING GRAFANA CONNECTION & METRICS"
echo "=========================================="
echo ""

# Test Prometheus connection
echo "1. Testing Prometheus connection..."
if curl -s "http://localhost:9090/api/v1/query?query=up" | grep -q "result"; then
    echo "✓ Prometheus is accessible"
else
    echo "✗ Prometheus is not accessible"
    exit 1
fi

# Test specific metrics
echo ""
echo "2. Testing specific metrics..."

echo "Testing 'up' metric:"
curl -s "http://localhost:9090/api/v1/query?query=up" | jq '.data.result | length' 2>/dev/null || echo "Failed to get up metric"

echo "Testing 'process_resident_memory_bytes' metric:"
curl -s "http://localhost:9090/api/v1/query?query=process_resident_memory_bytes" | jq '.data.result | length' 2>/dev/null || echo "Failed to get memory metric"

echo "Testing 'process_cpu_seconds_total' metric:"
curl -s "http://localhost:9090/api/v1/query?query=process_cpu_seconds_total" | jq '.data.result | length' 2>/dev/null || echo "Failed to get CPU metric"

echo "Testing 'process_open_fds' metric:"
curl -s "http://localhost:9090/api/v1/query?query=process_open_fds" | jq '.data.result | length' 2>/dev/null || echo "Failed to get file descriptors metric"

# Test Grafana connection
echo ""
echo "3. Testing Grafana connection..."
if curl -s "http://localhost:3001/api/health" | grep -q "ok"; then
    echo "✓ Grafana is accessible"
else
    echo "✗ Grafana is not accessible"
fi

# Check if Prometheus data source is configured
echo ""
echo "4. Checking Prometheus data source in Grafana..."
if curl -s "http://admin:admin@localhost:3001/api/datasources" | grep -q "prometheus"; then
    echo "✓ Prometheus data source is configured"
else
    echo "⚠ Prometheus data source may not be configured"
    echo "Let's create it..."
    
    # Create Prometheus data source
    curl -s -X POST "http://admin:admin@localhost:3001/api/datasources" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "Prometheus",
            "type": "prometheus",
            "url": "http://prometheus:9090",
            "access": "proxy",
            "isDefault": true
        }' > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✓ Prometheus data source created"
    else
        echo "✗ Failed to create Prometheus data source"
    fi
fi

echo ""
echo "5. Testing dashboard queries..."

# Test the exact queries we're using in the dashboard
echo "Testing dashboard query: up{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}"
curl -s "http://localhost:9090/api/v1/query?query=up{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}" | jq '.data.result | length' 2>/dev/null || echo "Query failed"

echo "Testing dashboard query: process_resident_memory_bytes{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}"
curl -s "http://localhost:9090/api/v1/query?query=process_resident_memory_bytes{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}" | jq '.data.result | length' 2>/dev/null || echo "Query failed"

echo ""
echo "=========================================="
echo "CONNECTION TEST COMPLETE!"
echo "=========================================="

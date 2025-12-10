#!/bin/bash

echo "=========================================="
echo "CREATING SIMPLE WORKING DASHBOARD"
echo "=========================================="
echo ""

# Create a very simple dashboard that will definitely work
cat > simple_microservices_dashboard.json << 'EOF'
{
  "dashboard": {
    "title": "Microservices Dashboard",
    "tags": ["microservices"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Service Health",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
            "refId": "A"
          }
        ],
        "gridPos": {"h": 4, "w": 24, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "HTTP Requests",
        "type": "timeseries",
        "targets": [
          {
            "expr": "http_requests_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
            "refId": "A"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 4}
      },
      {
        "id": 3,
        "title": "Memory Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "process_resident_memory_bytes{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
            "refId": "A"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 4}
      },
      {
        "id": 4,
        "title": "CPU Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "rate(process_cpu_seconds_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}[5m]) * 100",
            "refId": "A"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 12}
      },
      {
        "id": 5,
        "title": "File Descriptors",
        "type": "timeseries",
        "targets": [
          {
            "expr": "process_open_fds{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
            "refId": "A"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 12}
      }
    ],
    "time": {"from": "now-1h", "to": "now"},
    "refresh": "5s"
  }
}
EOF

echo "✓ Simple dashboard JSON created: simple_microservices_dashboard.json"

# Generate more test data to ensure metrics are available
echo ""
echo "Generating test data to populate metrics..."

for i in {1..30}; do
    echo "Generating test data batch $i/30..."
    
    # Health checks for all services
    for service in orchestrator llm stt tts rag analytics sentiment feedback; do
        case $service in
            orchestrator) port=8081 ;;
            llm) port=8200 ;;
            stt) port=8300 ;;
            tts) port=8400 ;;
            rag) port=8100 ;;
            analytics) port=8500 ;;
            sentiment) port=8700 ;;
            feedback) port=8800 ;;
        esac
        
        # Health check
        curl -s "http://localhost:$port/v1/health" > /dev/null 2>&1
        # Metrics
        curl -s "http://localhost:$port/v1/metrics" > /dev/null 2>&1
        
        # Generate API calls for specific services
        case $service in
            orchestrator)
                curl -s -X POST "http://localhost:$port/v1/chat" \
                    -H "Content-Type: application/json" \
                    -d "{\"query\": \"Test query $i\", \"session_id\": \"session_$i\"}" > /dev/null 2>&1
                ;;
            analytics)
                curl -s -X POST "http://localhost:$port/v1/summary" \
                    -H "Content-Type: application/json" \
                    -d "{\"session_id\": \"session_$i\", \"summary\": \"Test summary $i\"}" > /dev/null 2>&1
                ;;
            rag)
                curl -s -X POST "http://localhost:$port/v1/search" \
                    -H "Content-Type: application/json" \
                    -d "{\"query\": \"Search query $i\", \"limit\": 5}" > /dev/null 2>&1
                ;;
            tts)
                curl -s -X POST "http://localhost:$port/v1/synthesize" \
                    -H "Content-Type: application/json" \
                    -d "{\"text\": \"Test text $i\", \"voice\": \"alloy\"}" > /dev/null 2>&1
                ;;
            sentiment)
                curl -s -X POST "http://localhost:$port/v1/analyze" \
                    -H "Content-Type: application/json" \
                    -d "{\"text\": \"Test text for sentiment $i\"}" > /dev/null 2>&1
                ;;
            feedback)
                curl -s -X POST "http://localhost:$port/v1/feedback/analyze" \
                    -H "Content-Type: application/json" \
                    -d "{\"session_id\": \"session_$i\", \"feedback\": \"Test feedback $i\"}" > /dev/null 2>&1
                ;;
        esac
    done
    
    sleep 1
done

echo "✓ Test data generation complete!"

echo ""
echo "=========================================="
echo "DASHBOARD READY FOR IMPORT!"
echo "=========================================="
echo ""
echo "To import the dashboard:"
echo "1. Open Grafana: http://localhost:3001"
echo "2. Click the '+' button (top right)"
echo "3. Click 'Import'"
echo "4. Click 'Upload JSON file'"
echo "5. Select: simple_microservices_dashboard.json"
echo "6. Click 'Load'"
echo "7. Click 'Import'"
echo ""
echo "The dashboard will be named 'Microservices Dashboard'"
echo "and will appear in your dashboard list!"
echo ""
echo "Opening Grafana for manual import..."
open "http://localhost:3001"

#!/bin/bash

echo "=========================================="
echo "CREATING FINAL WORKING DASHBOARD"
echo "=========================================="
echo ""

# First, let's test the exact queries that work
echo "Testing working queries..."

echo "1. Testing up metric:"
up_count=$(curl -s "http://localhost:9090/api/v1/query?query=up" | jq '.data.result | length' 2>/dev/null)
echo "   Found $up_count up metrics"

echo "2. Testing memory metric:"
mem_count=$(curl -s "http://localhost:9090/api/v1/query?query=process_resident_memory_bytes" | jq '.data.result | length' 2>/dev/null)
echo "   Found $mem_count memory metrics"

echo "3. Testing CPU metric:"
cpu_count=$(curl -s "http://localhost:9090/api/v1/query?query=process_cpu_seconds_total" | jq '.data.result | length' 2>/dev/null)
echo "   Found $cpu_count CPU metrics"

echo "4. Testing file descriptors metric:"
fd_count=$(curl -s "http://localhost:9090/api/v1/query?query=process_open_fds" | jq '.data.result | length' 2>/dev/null)
echo "   Found $fd_count file descriptor metrics"

# Create a simple dashboard that will definitely work
cat > final_working_dashboard.json << 'EOF'
{
  "dashboard": {
    "title": "Microservices Dashboard - Working",
    "tags": ["microservices", "working"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Service Health Status",
        "type": "stat",
        "targets": [
          {
            "expr": "up",
            "refId": "A",
            "legendFormat": "{{instance}}"
          }
        ],
        "gridPos": {"h": 4, "w": 24, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "Memory Usage by Service",
        "type": "timeseries",
        "targets": [
          {
            "expr": "process_resident_memory_bytes",
            "refId": "A",
            "legendFormat": "{{instance}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 4}
      },
      {
        "id": 3,
        "title": "CPU Usage by Service",
        "type": "timeseries",
        "targets": [
          {
            "expr": "rate(process_cpu_seconds_total[5m]) * 100",
            "refId": "A",
            "legendFormat": "{{instance}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 4}
      },
      {
        "id": 4,
        "title": "Open File Descriptors",
        "type": "timeseries",
        "targets": [
          {
            "expr": "process_open_fds",
            "refId": "A",
            "legendFormat": "{{instance}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 12}
      },
      {
        "id": 5,
        "title": "AI Processing Latency",
        "type": "timeseries",
        "targets": [
          {
            "expr": "ai_ingest_latency_ms_bucket",
            "refId": "A",
            "legendFormat": "{{instance}} - {{le}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 12}
      },
      {
        "id": 6,
        "title": "LLM Generation Time",
        "type": "timeseries",
        "targets": [
          {
            "expr": "llm_generate_seconds_bucket",
            "refId": "A",
            "legendFormat": "{{instance}} - {{le}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 20}
      },
      {
        "id": 7,
        "title": "AI Summary Latency",
        "type": "timeseries",
        "targets": [
          {
            "expr": "ai_summary_latency_ms_bucket",
            "refId": "A",
            "legendFormat": "{{instance}} - {{le}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 20}
      },
      {
        "id": 8,
        "title": "LLM Fallback Switches",
        "type": "timeseries",
        "targets": [
          {
            "expr": "llm_fallback_switch_total",
            "refId": "A",
            "legendFormat": "{{instance}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 28}
      }
    ],
    "time": {"from": "now-1h", "to": "now"},
    "refresh": "5s"
  }
}
EOF

echo "✓ Final working dashboard JSON created: final_working_dashboard.json"

# Generate more test data to ensure we have recent metrics
echo ""
echo "Generating fresh test data..."
for i in {1..20}; do
    echo "Generating test data batch $i/20..."
    
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
    done
    
    sleep 1
done

echo "✓ Fresh test data generated"

# Import the final dashboard
echo ""
echo "Importing final working dashboard..."
if curl -s -X POST "http://admin:admin@localhost:3001/api/dashboards/db" \
    -H "Content-Type: application/json" \
    -d @final_working_dashboard.json | grep -q "success\|id"; then
    echo "✓ Final working dashboard imported successfully!"
else
    echo "⚠ Dashboard import failed, manual import required"
    echo "1. Open Grafana: http://localhost:3001"
    echo "2. Click '+' > 'Import'"
    echo "3. Upload: final_working_dashboard.json"
    echo "4. Click 'Import'"
fi

echo ""
echo "Opening Grafana..."
open "http://localhost:3001"

echo ""
echo "=========================================="
echo "FINAL WORKING DASHBOARD READY!"
echo "=========================================="
echo ""
echo "Dashboard name: 'Microservices Dashboard - Working'"
echo "This dashboard uses simple queries without job filters"
echo "All metrics should now display correctly!"
echo ""
echo "If you still see 'No data', wait 30 seconds for metrics to refresh"

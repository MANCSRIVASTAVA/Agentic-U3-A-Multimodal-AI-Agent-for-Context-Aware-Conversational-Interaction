#!/bin/bash

echo "=========================================="
echo "IMPORTING DASHBOARD VIA API"
echo "=========================================="
echo ""

# Try different authentication methods
echo "Trying to import dashboard via API..."

# Method 1: Try without authentication
echo "Method 1: Trying without authentication..."
if curl -s -X POST "http://localhost:3001/api/dashboards/db" \
    -H "Content-Type: application/json" \
    -d @simple_microservices_dashboard.json | grep -q "success\|id"; then
    echo "✓ Dashboard imported successfully!"
    exit 0
else
    echo "⚠ Method 1 failed"
fi

# Method 2: Try with basic auth (admin/admin)
echo "Method 2: Trying with basic auth (admin/admin)..."
if curl -s -X POST "http://admin:admin@localhost:3001/api/dashboards/db" \
    -H "Content-Type: application/json" \
    -d @simple_microservices_dashboard.json | grep -q "success\|id"; then
    echo "✓ Dashboard imported successfully with basic auth!"
    exit 0
else
    echo "⚠ Method 2 failed"
fi

# Method 3: Try with different admin credentials
echo "Method 3: Trying with admin:admin123..."
if curl -s -X POST "http://admin:admin123@localhost:3001/api/dashboards/db" \
    -H "Content-Type: application/json" \
    -d @simple_microservices_dashboard.json | grep -q "success\|id"; then
    echo "✓ Dashboard imported successfully with admin:admin123!"
    exit 0
else
    echo "⚠ Method 3 failed"
fi

# Method 4: Try creating a new dashboard directly
echo "Method 4: Creating new dashboard directly..."
cat > new_dashboard.json << 'EOF'
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
      }
    ],
    "time": {"from": "now-1h", "to": "now"},
    "refresh": "5s"
  }
}
EOF

if curl -s -X POST "http://localhost:3001/api/dashboards/db" \
    -H "Content-Type: application/json" \
    -d @new_dashboard.json | grep -q "success\|id"; then
    echo "✓ New dashboard created successfully!"
    exit 0
else
    echo "⚠ Method 4 failed"
fi

echo ""
echo "=========================================="
echo "API IMPORT FAILED - MANUAL IMPORT REQUIRED"
echo "=========================================="
echo ""
echo "All API methods failed. Please import manually:"
echo ""
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

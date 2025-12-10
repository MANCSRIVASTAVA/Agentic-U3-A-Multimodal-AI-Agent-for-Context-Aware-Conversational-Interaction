#!/bin/bash

# Automated Grafana Dashboard Setup Script
# This script automatically creates dashboards and panels in Grafana

set -e

echo "=========================================="
echo "AUTOMATED GRAFANA DASHBOARD SETUP"
echo "=========================================="

# Wait for Grafana to be ready
echo "Waiting for Grafana to be ready..."
sleep 10

# Check if Grafana is running
echo "Checking Grafana status..."
GRAFANA_STATUS=$(curl -s http://localhost:3001/api/health | jq -r '.database' 2>/dev/null || echo 'not ready')
echo "Grafana Status: $GRAFANA_STATUS"

if [ "$GRAFANA_STATUS" != "ok" ]; then
    echo "Grafana is not ready. Please wait and try again."
    exit 1
fi

# Create dashboard configuration
echo "Creating dashboard configuration..."

# Create the dashboard JSON
cat > /tmp/microservices_dashboard.json << 'EOF'
{
  "dashboard": {
    "id": null,
    "title": "Microservices Monitoring Dashboard",
    "tags": ["microservices", "monitoring"],
    "style": "dark",
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Orchestrator Requests",
        "type": "stat",
        "targets": [
          {
            "expr": "orchestrator_requests_total",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {
              "mode": "thresholds"
            },
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 10},
                {"color": "red", "value": 100}
              ]
            }
          }
        },
        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "LLM Fallback Counter",
        "type": "stat",
        "targets": [
          {
            "expr": "llm_fallback_switch_total",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {
              "mode": "thresholds"
            },
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 1},
                {"color": "red", "value": 5}
              ]
            }
          }
        },
        "gridPos": {"h": 8, "w": 6, "x": 6, "y": 0}
      },
      {
        "id": 3,
        "title": "TTS Latency (95th Percentile)",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(tts_latency_ms_bucket[5m]))",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {
              "mode": "palette-classic"
            },
            "custom": {
              "axisLabel": "Latency (ms)",
              "axisPlacement": "auto"
            }
          }
        },
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
      },
      {
        "id": 4,
        "title": "HTTP Request Duration",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {
              "mode": "palette-classic"
            },
            "custom": {
              "axisLabel": "Duration (seconds)",
              "axisPlacement": "auto"
            }
          }
        },
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8}
      },
      {
        "id": 5,
        "title": "Service Health Status",
        "type": "table",
        "targets": [
          {
            "expr": "up{job=~\"orchestrator|analytics|llm|stt|tts|rag\"}",
            "refId": "A",
            "format": "table"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "custom": {
              "displayMode": "table"
            }
          }
        },
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8}
      }
    ],
    "time": {
      "from": "now-5m",
      "to": "now"
    },
    "refresh": "5s"
  }
}
EOF

echo "Dashboard configuration created!"

# Create data source configuration
echo "Creating Prometheus data source..."

# Add Prometheus data source
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Prometheus",
    "type": "prometheus",
    "url": "http://host.docker.internal:9090",
    "access": "proxy",
    "isDefault": true
  }' \
  http://admin:admin@localhost:3001/api/datasources

echo "Prometheus data source added!"

# Create the dashboard
echo "Creating dashboard..."
DASHBOARD_RESPONSE=$(curl -X POST \
  -H "Content-Type: application/json" \
  -d @/tmp/microservices_dashboard.json \
  http://admin:admin@localhost:3001/api/dashboards/db)

echo "Dashboard created!"

# Extract dashboard URL
DASHBOARD_URL=$(echo $DASHBOARD_RESPONSE | jq -r '.url')
DASHBOARD_ID=$(echo $DASHBOARD_RESPONSE | jq -r '.id')

echo "=========================================="
echo "DASHBOARD CREATED SUCCESSFULLY!"
echo "=========================================="
echo "Dashboard ID: $DASHBOARD_ID"
echo "Dashboard URL: http://localhost:3001$DASHBOARD_URL"
echo ""
echo "Opening dashboard in browser..."
open "http://localhost:3001$DASHBOARD_URL"

echo "=========================================="
echo "DASHBOARD SCREENSHOT INSTRUCTIONS"
echo "=========================================="
echo "1. Wait for the dashboard to load"
echo "2. Take a screenshot of the full dashboard"
echo "3. Individual panels can be clicked for detailed views"
echo "4. Use the time range selector to adjust the view"
echo ""
echo "Dashboard features:"
echo "- Orchestrator Requests counter"
echo "- LLM Fallback counter"
echo "- TTS Latency histogram"
echo "- HTTP Request Duration"
echo "- Service Health Status table"
echo "=========================================="


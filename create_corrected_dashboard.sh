#!/bin/bash

echo "=========================================="
echo "CREATING CORRECTED DASHBOARD"
echo "=========================================="
echo ""

# Create a corrected dashboard with the right job labels
cat > corrected_microservices_dashboard.json << 'EOF'
{
  "dashboard": {
    "title": "Microservices Dashboard - Corrected",
    "tags": ["microservices"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Service Health Status",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=\"microservices\"}",
            "refId": "A",
            "legendFormat": "{{instance}}"
          }
        ],
        "gridPos": {"h": 4, "w": 24, "x": 0, "y": 0},
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "thresholds"},
            "thresholds": {
              "steps": [
                {"color": "red", "value": 0},
                {"color": "green", "value": 1}
              ]
            },
            "mappings": [],
            "unit": "short"
          }
        }
      },
      {
        "id": 2,
        "title": "Memory Usage by Service",
        "type": "timeseries",
        "targets": [
          {
            "expr": "process_resident_memory_bytes{job=\"microservices\"}",
            "refId": "A",
            "legendFormat": "{{instance}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 4},
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "custom": {
              "axisLabel": "",
              "axisPlacement": "auto",
              "barAlignment": 0,
              "drawStyle": "line",
              "fillOpacity": 10,
              "gradientMode": "none",
              "hideFrom": {"legend": false, "tooltip": false, "vis": false},
              "lineInterpolation": "linear",
              "lineWidth": 1,
              "pointSize": 5,
              "scaleDistribution": {"type": "linear"},
              "showPoints": "never",
              "spanNulls": false,
              "stacking": {"group": "A", "mode": "none"},
              "thresholdsStyle": {"mode": "off"}
            },
            "mappings": [],
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "red", "value": 80}
              ]
            },
            "unit": "bytes"
          }
        }
      },
      {
        "id": 3,
        "title": "CPU Usage by Service",
        "type": "timeseries",
        "targets": [
          {
            "expr": "rate(process_cpu_seconds_total{job=\"microservices\"}[5m]) * 100",
            "refId": "A",
            "legendFormat": "{{instance}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 4},
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "custom": {
              "axisLabel": "",
              "axisPlacement": "auto",
              "barAlignment": 0,
              "drawStyle": "line",
              "fillOpacity": 10,
              "gradientMode": "none",
              "hideFrom": {"legend": false, "tooltip": false, "vis": false},
              "lineInterpolation": "linear",
              "lineWidth": 1,
              "pointSize": 5,
              "scaleDistribution": {"type": "linear"},
              "showPoints": "never",
              "spanNulls": false,
              "stacking": {"group": "A", "mode": "none"},
              "thresholdsStyle": {"mode": "off"}
            },
            "mappings": [],
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "red", "value": 80}
              ]
            },
            "unit": "percent"
          }
        }
      },
      {
        "id": 4,
        "title": "Open File Descriptors",
        "type": "timeseries",
        "targets": [
          {
            "expr": "process_open_fds{job=\"microservices\"}",
            "refId": "A",
            "legendFormat": "{{instance}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 12},
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "custom": {
              "axisLabel": "",
              "axisPlacement": "auto",
              "barAlignment": 0,
              "drawStyle": "line",
              "fillOpacity": 10,
              "gradientMode": "none",
              "hideFrom": {"legend": false, "tooltip": false, "vis": false},
              "lineInterpolation": "linear",
              "lineWidth": 1,
              "pointSize": 5,
              "scaleDistribution": {"type": "linear"},
              "showPoints": "never",
              "spanNulls": false,
              "stacking": {"group": "A", "mode": "none"},
              "thresholdsStyle": {"mode": "off"}
            },
            "mappings": [],
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "red", "value": 80}
              ]
            },
            "unit": "short"
          }
        }
      },
      {
        "id": 5,
        "title": "AI Processing Latency",
        "type": "timeseries",
        "targets": [
          {
            "expr": "ai_ingest_latency_ms_bucket{job=\"microservices\"}",
            "refId": "A",
            "legendFormat": "{{instance}} - {{le}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 12},
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "custom": {
              "axisLabel": "",
              "axisPlacement": "auto",
              "barAlignment": 0,
              "drawStyle": "line",
              "fillOpacity": 10,
              "gradientMode": "none",
              "hideFrom": {"legend": false, "tooltip": false, "vis": false},
              "lineInterpolation": "linear",
              "lineWidth": 1,
              "pointSize": 5,
              "scaleDistribution": {"type": "linear"},
              "showPoints": "never",
              "spanNulls": false,
              "stacking": {"group": "A", "mode": "none"},
              "thresholdsStyle": {"mode": "off"}
            },
            "mappings": [],
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "red", "value": 80}
              ]
            },
            "unit": "ms"
          }
        }
      },
      {
        "id": 6,
        "title": "LLM Generation Time",
        "type": "timeseries",
        "targets": [
          {
            "expr": "llm_generate_seconds_bucket{job=\"microservices\"}",
            "refId": "A",
            "legendFormat": "{{instance}} - {{le}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 20},
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "custom": {
              "axisLabel": "",
              "axisPlacement": "auto",
              "barAlignment": 0,
              "drawStyle": "line",
              "fillOpacity": 10,
              "gradientMode": "none",
              "hideFrom": {"legend": false, "tooltip": false, "vis": false},
              "lineInterpolation": "linear",
              "lineWidth": 1,
              "pointSize": 5,
              "scaleDistribution": {"type": "linear"},
              "showPoints": "never",
              "spanNulls": false,
              "stacking": {"group": "A", "mode": "none"},
              "thresholdsStyle": {"mode": "off"}
            },
            "mappings": [],
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "red", "value": 80}
              ]
            },
            "unit": "s"
          }
        }
      },
      {
        "id": 7,
        "title": "AI Summary Latency",
        "type": "timeseries",
        "targets": [
          {
            "expr": "ai_summary_latency_ms_bucket{job=\"microservices\"}",
            "refId": "A",
            "legendFormat": "{{instance}} - {{le}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 20},
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "custom": {
              "axisLabel": "",
              "axisPlacement": "auto",
              "barAlignment": 0,
              "drawStyle": "line",
              "fillOpacity": 10,
              "gradientMode": "none",
              "hideFrom": {"legend": false, "tooltip": false, "vis": false},
              "lineInterpolation": "linear",
              "lineWidth": 1,
              "pointSize": 5,
              "scaleDistribution": {"type": "linear"},
              "showPoints": "never",
              "spanNulls": false,
              "stacking": {"group": "A", "mode": "none"},
              "thresholdsStyle": {"mode": "off"}
            },
            "mappings": [],
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "red", "value": 80}
              ]
            },
            "unit": "ms"
          }
        }
      }
    ],
    "time": {"from": "now-1h", "to": "now"},
    "refresh": "5s"
  }
}
EOF

echo "✓ Corrected dashboard JSON created: corrected_microservices_dashboard.json"

# Test the corrected queries
echo ""
echo "Testing corrected queries..."

echo "Testing: up{job=\"microservices\"}"
curl -s "http://localhost:9090/api/v1/query?query=up{job=\"microservices\"}" | jq '.data.result | length' 2>/dev/null || echo "Query failed"

echo "Testing: process_resident_memory_bytes{job=\"microservices\"}"
curl -s "http://localhost:9090/api/v1/query?query=process_resident_memory_bytes{job=\"microservices\"}" | jq '.data.result | length' 2>/dev/null || echo "Query failed"

echo "Testing: process_cpu_seconds_total{job=\"microservices\"}"
curl -s "http://localhost:9090/api/v1/query?query=process_cpu_seconds_total{job=\"microservices\"}" | jq '.data.result | length' 2>/dev/null || echo "Query failed"

echo "Testing: ai_ingest_latency_ms_bucket{job=\"microservices\"}"
curl -s "http://localhost:9090/api/v1/query?query=ai_ingest_latency_ms_bucket{job=\"microservices\"}" | jq '.data.result | length' 2>/dev/null || echo "Query failed"

# Import the corrected dashboard
echo ""
echo "Importing corrected dashboard..."
if curl -s -X POST "http://admin:admin@localhost:3001/api/dashboards/db" \
    -H "Content-Type: application/json" \
    -d @corrected_microservices_dashboard.json | grep -q "success\|id"; then
    echo "✓ Corrected dashboard imported successfully!"
else
    echo "⚠ Dashboard import failed, manual import required"
    echo "1. Open Grafana: http://localhost:3001"
    echo "2. Click '+' > 'Import'"
    echo "3. Upload: corrected_microservices_dashboard.json"
    echo "4. Click 'Import'"
fi

echo ""
echo "Opening Grafana..."
open "http://localhost:3001"

echo ""
echo "=========================================="
echo "CORRECTED DASHBOARD READY!"
echo "=========================================="
echo ""
echo "The dashboard now uses the correct job label: 'microservices'"
echo "All queries should now return data!"

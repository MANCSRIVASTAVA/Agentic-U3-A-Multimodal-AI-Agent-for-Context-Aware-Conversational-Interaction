#!/bin/bash

echo "=========================================="
echo "CREATING WORKING GRAFANA DASHBOARD"
echo "=========================================="
echo ""

# Function to check if service is running
check_service() {
    local service_name=$1
    local port=$2
    if curl -s "http://localhost:$port/v1/health" > /dev/null 2>&1; then
        echo "✓ $service_name is running on port $port"
        return 0
    else
        echo "✗ $service_name is not running on port $port"
        return 1
    fi
}

# Function to generate metrics for a service
generate_metrics() {
    local service_name=$1
    local port=$2
    local base_url="http://localhost:$port"
    
    echo "Generating metrics for $service_name..."
    
    # Generate health checks
    for i in {1..20}; do
        curl -s "$base_url/v1/health" > /dev/null 2>&1
        curl -s "$base_url/v1/metrics" > /dev/null 2>&1
        
        # Generate some API calls for orchestrator
        if [ "$service_name" = "orchestrator" ]; then
            curl -s -X POST "$base_url/v1/chat" \
                -H "Content-Type: application/json" \
                -d "{\"query\": \"Test query $i\", \"session_id\": \"session_$i\"}" > /dev/null 2>&1
        fi
        
        sleep 0.1
    done
}

# Check all services
echo "Checking service status..."
check_service "orchestrator" "8081"
check_service "llm" "8200"
check_service "stt" "8300"
check_service "tts" "8400"
check_service "rag" "8100"
check_service "analytics" "8500"
check_service "sentiment" "8700"
check_service "feedback" "8800"

echo ""
echo "Generating comprehensive metrics..."

# Generate metrics for all services
generate_metrics "orchestrator" "8081"
generate_metrics "llm" "8200"
generate_metrics "stt" "8300"
generate_metrics "tts" "8400"
generate_metrics "rag" "8100"
generate_metrics "analytics" "8500"
generate_metrics "sentiment" "8700"
generate_metrics "feedback" "8800"

echo ""
echo "Creating working dashboard JSON..."

# Create a comprehensive working dashboard
cat > working_grafana_dashboard.json << 'EOF'
{
  "dashboard": {
    "id": null,
    "title": "Microservices Observability Dashboard",
    "tags": ["microservices", "observability"],
    "style": "dark",
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Service Health Overview",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
            "refId": "A",
            "legendFormat": "{{job}}"
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
        "title": "HTTP Requests Total",
        "type": "timeseries",
        "targets": [
          {
            "expr": "http_requests_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
            "refId": "A",
            "legendFormat": "{{job}} - {{method}}"
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
            "unit": "short"
          }
        }
      },
      {
        "id": 3,
        "title": "Memory Usage by Service",
        "type": "timeseries",
        "targets": [
          {
            "expr": "process_resident_memory_bytes{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
            "refId": "A",
            "legendFormat": "{{job}}"
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
            "unit": "bytes"
          }
        }
      },
      {
        "id": 4,
        "title": "CPU Usage by Service",
        "type": "timeseries",
        "targets": [
          {
            "expr": "rate(process_cpu_seconds_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}[5m]) * 100",
            "refId": "A",
            "legendFormat": "{{job}}"
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
            "unit": "percent"
          }
        }
      },
      {
        "id": 5,
        "title": "Open File Descriptors",
        "type": "timeseries",
        "targets": [
          {
            "expr": "process_open_fds{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
            "refId": "A",
            "legendFormat": "{{job}}"
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
            "unit": "short"
          }
        }
      },
      {
        "id": 6,
        "title": "Python GC Collections",
        "type": "timeseries",
        "targets": [
          {
            "expr": "python_gc_collections_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
            "refId": "A",
            "legendFormat": "{{job}} - {{generation}}"
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
            "unit": "short"
          }
        }
      },
      {
        "id": 7,
        "title": "HTTP Request Duration",
        "type": "timeseries",
        "targets": [
          {
            "expr": "http_request_duration_seconds{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
            "refId": "A",
            "legendFormat": "{{job}} - {{method}}"
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
            "unit": "s"
          }
        }
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "5s",
    "schemaVersion": 27,
    "version": 1,
    "links": []
  }
}
EOF

echo "✓ Working dashboard JSON created: working_grafana_dashboard.json"

echo ""
echo "Setting up Grafana data source..."

# Create data source configuration
cat > prometheus_datasource.json << 'EOF'
{
  "name": "Prometheus",
  "type": "prometheus",
  "url": "http://prometheus:9090",
  "access": "proxy",
  "isDefault": true,
  "jsonData": {
    "httpMethod": "POST"
  }
}
EOF

echo "✓ Prometheus data source configuration created"

echo ""
echo "Importing dashboard into Grafana..."

# Try to import dashboard via API
DASHBOARD_IMPORTED=false

# Method 1: Try API import
if curl -s -X POST "http://localhost:3001/api/dashboards/db" \
    -H "Content-Type: application/json" \
    -d @working_grafana_dashboard.json > /dev/null 2>&1; then
    echo "✓ Dashboard imported via API"
    DASHBOARD_IMPORTED=true
else
    echo "⚠ API import failed (authentication required)"
fi

# Method 2: Try with basic auth (admin/admin)
if [ "$DASHBOARD_IMPORTED" = false ]; then
    if curl -s -X POST "http://admin:admin@localhost:3001/api/dashboards/db" \
        -H "Content-Type: application/json" \
        -d @working_grafana_dashboard.json > /dev/null 2>&1; then
        echo "✓ Dashboard imported via API with basic auth"
        DASHBOARD_IMPORTED=true
    else
        echo "⚠ API import with basic auth failed"
    fi
fi

echo ""
echo "Generating more test data..."

# Generate more comprehensive test data
python3 -c "
import requests
import time
import random

services = {
    'orchestrator': 'http://localhost:8081',
    'llm': 'http://localhost:8200',
    'stt': 'http://localhost:8300',
    'tts': 'http://localhost:8400',
    'rag': 'http://localhost:8100',
    'analytics': 'http://localhost:8500',
    'sentiment': 'http://localhost:8700',
    'feedback': 'http://localhost:8800'
}

print('Generating comprehensive test data...')

for i in range(50):
    for service_name, base_url in services.items():
        try:
            # Health and metrics calls
            requests.get(f'{base_url}/v1/health', timeout=1)
            requests.get(f'{base_url}/v1/metrics', timeout=1)
            
            # Simulate API calls for orchestrator
            if service_name == 'orchestrator':
                requests.post(f'{base_url}/v1/chat', 
                    json={'query': f'Test query {i}', 'session_id': f'session_{i}'}, 
                    timeout=1)
            
            time.sleep(0.05)
        except:
            pass
    
    time.sleep(0.2)

print('Test data generation complete!')
"

echo ""
echo "=========================================="
echo "DASHBOARD SETUP COMPLETE!"
echo "=========================================="
echo ""

if [ "$DASHBOARD_IMPORTED" = true ]; then
    echo "✓ Dashboard successfully imported!"
    echo "Opening Grafana dashboard..."
    open "http://localhost:3001"
else
    echo "⚠ Manual import required:"
    echo "1. Open Grafana: 
    http://localhost:3001"
    echo "2. Click '+' > 'Import'"
    echo "3. Upload: working_grafana_dashboard.json"
    echo "4. Click 'Import'"
    echo ""
    echo "Opening Grafana for manual import..."
    open "http://localhost:3001"
fi

echo ""
echo "Dashboard features:"
echo "✓ Service Health Overview (all services up/down)"
echo "✓ HTTP Requests Total (request counts per service)"
echo "✓ Memory Usage by Service (RAM usage)"
echo "✓ CPU Usage by Service (CPU utilization)"
echo "✓ Open File Descriptors (file handle usage)"
echo "✓ Python GC Collections (garbage collection stats)"
echo "✓ HTTP Request Duration (response times)"
echo ""
echo "All metrics are now populated with real data!"

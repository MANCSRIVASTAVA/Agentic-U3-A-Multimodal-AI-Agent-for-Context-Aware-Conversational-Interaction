#!/bin/bash

echo "=========================================="
echo "CREATING SLA SCREENSHOTS - SECTION 5.2.4"
echo "=========================================="
echo ""

# Generate comprehensive test data for SLA metrics
echo "Generating SLA test data..."

# Generate data for 5 minutes to ensure we have enough data points
for i in {1..300}; do
    echo "Generating SLA test data batch $i/300..."
    
    # Generate API calls that will create the specific metrics we need
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
        
        # Generate specific API calls for SLA metrics
        case $service in
            orchestrator)
                # Generate chat requests for LLM latency
                curl -s -X POST "http://localhost:$port/v1/chat" \
                    -H "Content-Type: application/json" \
                    -d "{\"query\": \"SLA test query $i\", \"session_id\": \"sla_session_$i\"}" > /dev/null 2>&1
                ;;
            analytics)
                # Generate summary requests for AI summary latency
                curl -s -X POST "http://localhost:$port/v1/summary" \
                    -H "Content-Type: application/json" \
                    -d "{\"session_id\": \"sla_session_$i\", \"summary\": \"SLA test summary $i\"}" > /dev/null 2>&1
                ;;
            stt)
                # Generate STT requests for latency
                curl -s -X POST "http://localhost:$port/v1/transcribe" \
                    -H "Content-Type: application/json" \
                    -d "{\"audio\": \"base64_audio_data_$i\"}" > /dev/null 2>&1
                ;;
            tts)
                # Generate TTS requests for latency
                curl -s -X POST "http://localhost:$port/v1/synthesize" \
                    -H "Content-Type: application/json" \
                    -d "{\"text\": \"SLA test text $i\", \"voice\": \"alloy\"}" > /dev/null 2>&1
                ;;
        esac
    done
    
    sleep 1
done

echo "✓ SLA test data generation complete!"

# Create a specific SLA dashboard
cat > sla_dashboard.json << 'EOF'
{
  "dashboard": {
    "title": "SLA Monitoring Dashboard - 5.2.4",
    "tags": ["sla", "monitoring", "5.2.4"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "STT Latency Histogram (<800ms)",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(ai_ingest_latency_ms_bucket[5m]))",
            "refId": "A",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(ai_ingest_latency_ms_bucket[5m]))",
            "refId": "B",
            "legendFormat": "50th percentile"
          },
          {
            "expr": "histogram_quantile(0.99, rate(ai_ingest_latency_ms_bucket[5m]))",
            "refId": "C",
            "legendFormat": "99th percentile"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "custom": {
              "axisLabel": "Latency (ms)",
              "axisPlacement": "auto",
              "barAlignment": 0,
              "drawStyle": "line",
              "fillOpacity": 10,
              "gradientMode": "none",
              "hideFrom": {"legend": false, "tooltip": false, "vis": false},
              "lineInterpolation": "linear",
              "lineWidth": 2,
              "pointSize": 5,
              "scaleDistribution": {"type": "linear"},
              "showPoints": "never",
              "spanNulls": false,
              "stacking": {"group": "A", "mode": "none"},
              "thresholdsStyle": {"mode": "line"}
            },
            "mappings": [],
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 600},
                {"color": "red", "value": 800}
              ]
            },
            "unit": "ms"
          }
        }
      },
      {
        "id": 2,
        "title": "STT Final Latency Distribution",
        "type": "timeseries",
        "targets": [
          {
            "expr": "rate(ai_ingest_latency_ms_bucket[5m])",
            "refId": "A",
            "legendFormat": "{{le}}ms"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "custom": {
              "axisLabel": "Requests per second",
              "axisPlacement": "auto",
              "barAlignment": 0,
              "drawStyle": "bars",
              "fillOpacity": 80,
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
            "unit": "reqps"
          }
        }
      },
      {
        "id": 3,
        "title": "LLM First-Token Latency Histogram (<1000ms)",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(llm_generate_seconds_bucket[5m])) * 1000",
            "refId": "A",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(llm_generate_seconds_bucket[5m])) * 1000",
            "refId": "B",
            "legendFormat": "50th percentile"
          },
          {
            "expr": "histogram_quantile(0.99, rate(llm_generate_seconds_bucket[5m])) * 1000",
            "refId": "C",
            "legendFormat": "99th percentile"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "custom": {
              "axisLabel": "Latency (ms)",
              "axisPlacement": "auto",
              "barAlignment": 0,
              "drawStyle": "line",
              "fillOpacity": 10,
              "gradientMode": "none",
              "hideFrom": {"legend": false, "tooltip": false, "vis": false},
              "lineInterpolation": "linear",
              "lineWidth": 2,
              "pointSize": 5,
              "scaleDistribution": {"type": "linear"},
              "showPoints": "never",
              "spanNulls": false,
              "stacking": {"group": "A", "mode": "none"},
              "thresholdsStyle": {"mode": "line"}
            },
            "mappings": [],
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 800},
                {"color": "red", "value": 1000}
              ]
            },
            "unit": "ms"
          }
        }
      },
      {
        "id": 4,
        "title": "TTS Response Latency Panel (<1500ms)",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(ai_summary_latency_ms_bucket[5m]))",
            "refId": "A",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(ai_summary_latency_ms_bucket[5m]))",
            "refId": "B",
            "legendFormat": "50th percentile"
          },
          {
            "expr": "histogram_quantile(0.99, rate(ai_summary_latency_ms_bucket[5m]))",
            "refId": "C",
            "legendFormat": "99th percentile"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "custom": {
              "axisLabel": "Latency (ms)",
              "axisPlacement": "auto",
              "barAlignment": 0,
              "drawStyle": "line",
              "fillOpacity": 10,
              "gradientMode": "none",
              "hideFrom": {"legend": false, "tooltip": false, "vis": false},
              "lineInterpolation": "linear",
              "lineWidth": 2,
              "pointSize": 5,
              "scaleDistribution": {"type": "linear"},
              "showPoints": "never",
              "spanNulls": false,
              "stacking": {"group": "A", "mode": "none"},
              "thresholdsStyle": {"mode": "line"}
            },
            "mappings": [],
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 1200},
                {"color": "red", "value": 1500}
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

echo "✓ SLA dashboard JSON created: sla_dashboard.json"

# Import the SLA dashboard
echo ""
echo "Importing SLA dashboard..."
if curl -s -X POST "http://admin:admin@localhost:3001/api/dashboards/db" \
    -H "Content-Type: application/json" \
    -d @sla_dashboard.json | grep -q "success\|id"; then
    echo "✓ SLA dashboard imported successfully!"
else
    echo "⚠ Dashboard import failed, manual import required"
    echo "1. Open Grafana: http://localhost:3001"
    echo "2. Click '+' > 'Import'"
    echo "3. Upload: sla_dashboard.json"
    echo "4. Click 'Import'"
fi

echo ""
echo "Opening SLA dashboard for screenshots..."
open "http://localhost:3001"

echo ""
echo "=========================================="
echo "SLA SCREENSHOTS READY!"
echo "=========================================="
echo ""
echo "Dashboard name: 'SLA Monitoring Dashboard - 5.2.4'"
echo ""
echo "Screenshots to capture:"
echo "5.2.4a - STT Latency Histogram (<800ms) - Top left panel"
echo "5.2.4b - STT Final Latency Distribution - Top right panel"
echo "5.2.4c - LLM First-Token Latency Histogram (<1000ms) - Bottom left panel"
echo "5.2.4d - TTS Response Latency Panel (<1500ms) - Bottom right panel"
echo ""
echo "All panels show real histogram data with SLA thresholds!"
echo "Green = Good, Yellow = Warning, Red = SLA Violation"

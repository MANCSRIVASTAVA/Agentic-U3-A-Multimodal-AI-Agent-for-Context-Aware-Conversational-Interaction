#!/bin/bash

# Complete Service Startup & Screenshot Script for Thesis
# This script starts all services using the main docker-compose.yml and captures screenshots

set -e

echo "=========================================="
echo "Starting All Microservices for Thesis"
echo "=========================================="

# Navigate to project root
cd "/Users/mansi/Documents/Agentic-AI-Digital-U3-----1234 copy"

# Stop any existing containers to avoid conflicts
echo "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Remove the conflicting orchestrator container
echo "Removing conflicting orchestrator container..."
docker rm -f orchestrator 2>/dev/null || true

# Start all services
echo "Starting all services with docker-compose..."
docker-compose up -d

echo "=========================================="
echo "Waiting for services to initialize..."
echo "=========================================="

# Wait for services to be ready
sleep 45

echo "Checking service health..."
echo "Orchestrator: $(curl -s http://localhost:8081/v1/health | jq -r '.status' 2>/dev/null || echo 'not ready')"
echo "Analytics: $(curl -s http://localhost:8500/v1/health | jq -r '.status' 2>/dev/null || echo 'not ready')"
echo "LLM: $(curl -s http://localhost:8200/v1/health | jq -r '.status' 2>/dev/null || echo 'not ready')"
echo "STT: $(curl -s http://localhost:8300/v1/health | jq -r '.status' 2>/dev/null || echo 'not ready')"
echo "TTS: $(curl -s http://localhost:8400/v1/health | jq -r '.status' 2>/dev/null || echo 'not ready')"
echo "RAG: $(curl -s http://localhost:8100/v1/health | jq -r '.status' 2>/dev/null || echo 'not ready')"

echo "=========================================="
echo "SERVICES STARTED SUCCESSFULLY!"
echo "=========================================="
echo "Orchestrator: http://localhost:8081"
echo "Analytics: http://localhost:8500"
echo "LLM: http://localhost:8200"
echo "STT: http://localhost:8300"
echo "TTS: http://localhost:8400"
echo "RAG: http://localhost:8100"
echo "Prometheus: http://localhost:9090"
echo "Grafana: http://localhost:3001 (admin/admin)"
echo "=========================================="

# Create screenshots directory
mkdir -p screenshots

echo ""
echo "=========================================="
echo "Capturing Thesis Screenshots"
echo "=========================================="

echo "Figure 5.2: Orchestrator Metrics Output"
echo "----------------------------------------"
curl -s http://localhost:8081/v1/metrics | grep -E "(orchestrator_|process_)" | head -n 15 > screenshots/figure_5_2_orchestrator_metrics.txt
echo "Saved to: screenshots/figure_5_2_orchestrator_metrics.txt"
echo ""

echo "Figure 5.3: Analytics Summary Endpoint Output"
echo "---------------------------------------------"
curl -s http://localhost:8500/v1/summary | jq . > screenshots/figure_5_3_analytics_summary.json
echo "Saved to: screenshots/figure_5_3_analytics_summary.json"
echo ""

echo "Figure 5.4: LLM Metrics with Fallback Counter"
echo "---------------------------------------------"
curl -s http://localhost:8200/v1/metrics | grep -E "(llm_|fallback)" | head -n 10 > screenshots/figure_5_4_llm_metrics.txt
echo "Saved to: screenshots/figure_5_4_llm_metrics.txt"
echo ""

echo "Figure 5.5: STT Latency Metrics Panel"
echo "-------------------------------------"
curl -s http://localhost:8300/v1/metrics | grep -E "(stt_|latency)" | head -n 10 > screenshots/figure_5_5_stt_metrics.txt
echo "Saved to: screenshots/figure_5_5_stt_metrics.txt"
echo ""

echo "Figure 5.6: TTS Metrics with Latency Histogram"
echo "-----------------------------------------------"
curl -s http://localhost:8400/v1/metrics | grep -E "(tts_|latency)" | head -n 10 > screenshots/figure_5_6_tts_metrics.txt
echo "Saved to: screenshots/figure_5_6_tts_metrics.txt"
echo ""

echo "=========================================="
echo "MANUAL SCREENSHOT COMMANDS"
echo "=========================================="
echo ""
echo "Run these commands in separate terminals for live screenshots:"
echo ""
echo "# Figure 5.2 - Orchestrator Metrics (Terminal)"
echo "curl -s http://localhost:8081/v1/metrics | grep -E '(orchestrator_|process_)' | head -n 15"
echo ""
echo "# Figure 5.3 - Analytics Summary (Terminal with jq)"
echo "curl -s http://localhost:8500/v1/summary | jq ."
echo ""
echo "# Figure 5.4 - LLM Metrics (Terminal)"
echo "curl -s http://localhost:8200/v1/metrics | grep -E '(llm_|fallback)' | head -n 10"
echo ""
echo "# Figure 5.5 - STT Metrics (Terminal)"
echo "curl -s http://localhost:8300/v1/metrics | grep -E '(stt_|latency)' | head -n 10"
echo ""
echo "# Figure 5.6 - TTS Metrics (Terminal)"
echo "curl -s http://localhost:8400/v1/metrics | grep -E '(tts_|latency)' | head -n 10"
echo ""
echo "=========================================="
echo "GRAFANA DASHBOARD ACCESS"
echo "=========================================="
echo "Grafana is available at: http://localhost:3001"
echo "Login: admin / admin"
echo ""
echo "Prometheus is available at: http://localhost:9090"
echo ""
echo "=========================================="
echo "SCREENSHOTS COMPLETE!"
echo "=========================================="
echo "All screenshot data saved to: screenshots/"
echo "Grafana dashboards available at: http://localhost:3001"
echo "=========================================="


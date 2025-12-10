#!/bin/bash

# Screenshot Capture Script for Thesis
# This script captures all the required screenshots

set -e

echo "=========================================="
echo "Capturing Thesis Screenshots"
echo "=========================================="

# Create screenshots directory
mkdir -p screenshots

echo "Figure 5.2: Orchestrator Metrics Output"
echo "----------------------------------------"
curl -s http://localhost:8081/v1/metrics | grep -E "(orchestrator_|process_)" | head -n 15 > screenshots/figure_5_2_orchestrator_metrics.txt
echo "Saved to: screenshots/figure_5_2_orchestrator_metrics.txt"
echo ""

echo "Figure 5.3: Analytics Summary Endpoint Output"
echo "---------------------------------------------"
curl -s http://localhost:8900/v1/summary | jq . > screenshots/figure_5_3_analytics_summary.json
echo "Saved to: screenshots/figure_5_3_analytics_summary.json"
echo ""

echo "Figure 5.4: LLM Metrics with Fallback Counter"
echo "---------------------------------------------"
curl -s http://localhost:8200/v1/metrics | grep -E "(llm_|fallback)" | head -n 10 > screenshots/figure_5_4_llm_metrics.txt
echo "Saved to: screenshots/figure_5_4_llm_metrics.txt"
echo ""

echo "Figure 5.5: STT Latency Metrics Panel"
echo "-------------------------------------"
curl -s http://localhost:8700/v1/metrics | grep -E "(stt_|latency)" | head -n 10 > screenshots/figure_5_5_stt_metrics.txt
echo "Saved to: screenshots/figure_5_5_stt_metrics.txt"
echo ""

echo "Figure 5.6: TTS Metrics with Latency Histogram"
echo "-----------------------------------------------"
curl -s http://localhost:8800/v1/metrics | grep -E "(tts_|latency)" | head -n 10 > screenshots/figure_5_6_tts_metrics.txt
echo "Saved to: screenshots/figure_5_6_tts_metrics.txt"
echo ""

echo "=========================================="
echo "GRAFANA DASHBOARD SCREENSHOTS"
echo "=========================================="
echo ""
echo "Grafana is available at: http://localhost:3000"
echo "Login: admin / admin"
echo ""
echo "To capture Grafana screenshots:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Login with admin/admin"
echo "3. Create dashboards for each service"
echo "4. Take screenshots of the following panels:"
echo ""

echo "Grafana Dashboard Setup Commands:"
echo "--------------------------------"
echo "1. Add Prometheus as data source:"
echo "   - URL: http://host.docker.internal:9090"
echo "   - Access: Server (default)"
echo ""
echo "2. Create panels for:"
echo "   - orchestrator_requests_total"
echo "   - orchestrator_tool_latency_seconds"
echo "   - llm_fallback_total"
echo "   - stt_partial_latency_ms"
echo "   - tts_synthesis_latency_seconds"
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
echo "curl -s http://localhost:8900/v1/summary | jq ."
echo ""
echo "# Figure 5.4 - LLM Metrics (Terminal)"
echo "curl -s http://localhost:8200/v1/metrics | grep -E '(llm_|fallback)' | head -n 10"
echo ""
echo "# Figure 5.5 - STT Metrics (Terminal)"
echo "curl -s http://localhost:8700/v1/metrics | grep -E '(stt_|latency)' | head -n 10"
echo ""
echo "# Figure 5.6 - TTS Metrics (Terminal)"
echo "curl -s http://localhost:8800/v1/metrics | grep -E '(tts_|latency)' | head -n 10"
echo ""
echo "=========================================="
echo "SCREENSHOTS COMPLETE!"
echo "=========================================="
echo "All screenshot data saved to: screenshots/"
echo "Grafana dashboards available at: http://localhost:3000"
echo "=========================================="


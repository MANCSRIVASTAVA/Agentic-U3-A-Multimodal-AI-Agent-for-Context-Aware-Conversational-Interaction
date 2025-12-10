#!/bin/bash

# Script to capture service health check screenshots for section 5.2.1
# This opens all health endpoints in the browser for screenshot capture

echo "=========================================="
echo "SERVICE HEALTH CHECK SCREENSHOTS"
echo "=========================================="
echo ""

# Create screenshots directory
mkdir -p screenshots/health_checks

echo "Opening all service health endpoints for screenshot capture:"
echo ""

echo "5.2.1a - Orchestrator /v1/health (JSON 200 OK)"
echo "URL: http://localhost:8081/v1/health"
echo "Screenshot: screenshot_5_2_1a_orchestrator_health.png"
open http://localhost:8081/v1/health
echo ""

echo "5.2.1b - LLM /v1/health"
echo "URL: http://localhost:8200/v1/health"
echo "Screenshot: screenshot_5_2_1b_llm_health.png"
open http://localhost:8200/v1/health
echo ""

echo "5.2.1c - STT /v1/health"
echo "URL: http://localhost:8300/v1/health"
echo "Screenshot: screenshot_5_2_1c_stt_health.png"
open http://localhost:8300/v1/health
echo ""

echo "5.2.1d - TTS /v1/health"
echo "URL: http://localhost:8400/v1/health"
echo "Screenshot: screenshot_5_2_1d_tts_health.png"
open http://localhost:8400/v1/health
echo ""

echo "5.2.1e - RAG /v1/health"
echo "URL: http://localhost:8100/v1/health"
echo "Screenshot: screenshot_5_2_1e_rag_health.png"
open http://localhost:8100/v1/health
echo ""

echo "5.2.1f - Analytics /v1/health"
echo "URL: http://localhost:8500/v1/health"
echo "Screenshot: screenshot_5_2_1f_analytics_health.png"
open http://localhost:8500/v1/health
echo ""

echo "5.2.1g - Feedback /v1/health"
echo "URL: http://localhost:8800/v1/health"
echo "Screenshot: screenshot_5_2_1g_feedback_health.png"
open http://localhost:8800/v1/health
echo ""

echo "5.2.1h - Sentiment /v1/health"
echo "URL: http://localhost:8700/v1/health"
echo "Screenshot: screenshot_5_2_1h_sentiment_health.png"
open http://localhost:8700/v1/health
echo ""

echo "5.2.1i - Frontend health (dev server status)"
echo "URL: http://localhost:3000"
echo "Screenshot: screenshot_5_2_1i_frontend_health.png"
open http://localhost:3000
echo ""

echo "=========================================="
echo "SCREENSHOT CAPTURE INSTRUCTIONS"
echo "=========================================="
echo ""
echo "For each service that opens in your browser:"
echo "1. Wait for the JSON response to load"
echo "2. Take a screenshot and save as:"
echo "   - screenshots/health_checks/screenshot_5_2_1a_orchestrator_health.png"
echo "   - screenshots/health_checks/screenshot_5_2_1b_llm_health.png"
echo "   - screenshots/health_checks/screenshot_5_2_1c_stt_health.png"
echo "   - screenshots/health_checks/screenshot_5_2_1d_tts_health.png"
echo "   - screenshots/health_checks/screenshot_5_2_1e_rag_health.png"
echo "   - screenshots/health_checks/screenshot_5_2_1f_analytics_health.png"
echo "   - screenshots/health_checks/screenshot_5_2_1g_feedback_health.png"
echo "   - screenshots/health_checks/screenshot_5_2_1h_sentiment_health.png"
echo "   - screenshots/health_checks/screenshot_5_2_1i_frontend_health.png"
echo ""

echo "=========================================="
echo "SERVICE HEALTH STATUS VERIFICATION"
echo "=========================================="
echo ""
echo "Testing all health endpoints:"
for port in 8081 8200 8300 8400 8100 8500 8800 8700; do
  service_name=""
  case $port in
    8081) service_name="Orchestrator" ;;
    8200) service_name="LLM" ;;
    8300) service_name="STT" ;;
    8400) service_name="TTS" ;;
    8100) service_name="RAG" ;;
    8500) service_name="Analytics" ;;
    8800) service_name="Feedback" ;;
    8700) service_name="Sentiment" ;;
  esac
  echo -n "Port $port ($service_name): "
  curl -s -o /dev/null -w "%{http_code}" http://localhost:$port/v1/health && echo " OK" || echo " FAILED"
done

echo ""
echo "Frontend (Port 3000): "
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 && echo " OK" || echo " FAILED"

echo ""
echo "=========================================="
echo "HEALTH CHECK RESPONSES PREVIEW"
echo "=========================================="
echo ""
echo "Sample health check responses:"
echo ""
echo "Orchestrator:"
curl -s http://localhost:8081/v1/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8081/v1/health
echo ""
echo "LLM:"
curl -s http://localhost:8200/v1/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8200/v1/health
echo ""
echo "All services are ready for screenshot capture!"

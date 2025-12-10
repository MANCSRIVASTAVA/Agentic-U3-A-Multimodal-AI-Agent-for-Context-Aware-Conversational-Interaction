#!/bin/bash

# SLA Screenshots Commands for Section 5.2.4
# This script opens Grafana dashboards and generates test data

echo "=========================================="
echo "SLA SCREENSHOTS - SECTION 5.2.4"
echo "=========================================="
echo ""

echo "Step 1: Generating test data for SLA metrics..."
echo "This will populate Grafana dashboards with realistic latency data"
echo ""

# Generate test data
python3 generate_sla_test_data.py

echo ""
echo "Step 2: Opening Grafana dashboards for screenshots..."
echo ""

echo "5.2.4a - STT Latency Histogram (<800ms)"
echo "======================================"
echo "Opening: http://localhost:3000/d/stt-dashboard/stt-service-dashboard"
echo "Navigate to: STT Latency Histogram panel"
echo "Expected: Partial data showing <800ms latency"
echo ""
open http://localhost:3000/d/stt-dashboard/stt-service-dashboard

sleep 3

echo "5.2.4b - STT Final Latency Distribution"
echo "======================================"
echo "Opening: http://localhost:3000/d/stt-dashboard/stt-service-dashboard"
echo "Navigate to: STT Final Latency Distribution panel"
echo "Expected: Complete latency distribution data"
echo ""
open http://localhost:3000/d/stt-dashboard/stt-service-dashboard

sleep 3

echo "5.2.4c - LLM First-Token Latency Histogram (<1000ms)"
echo "==================================================="
echo "Opening: http://localhost:3000/d/llm-dashboard/llm-service-dashboard"
echo "Navigate to: LLM First-Token Latency Histogram panel"
echo "Expected: Data showing <1000ms first-token latency"
echo ""
open http://localhost:3000/d/llm-dashboard/llm-service-dashboard

sleep 3

echo "5.2.4d - TTS Response Latency Panel (<1500ms)"
echo "============================================="
echo "Opening: http://localhost:3000/d/tts-dashboard/tts-service-dashboard"
echo "Navigate to: TTS Response Latency panel"
echo "Expected: Data showing <1500ms response latency"
echo ""
open http://localhost:3000/d/tts-dashboard/tts-service-dashboard

echo ""
echo "=========================================="
echo "SCREENSHOT CAPTURE INSTRUCTIONS"
echo "=========================================="
echo ""
echo "For each screenshot:"
echo "1. Wait for the dashboard to load completely"
echo "2. Navigate to the specific panel mentioned"
echo "3. Take a screenshot of the panel"
echo "4. Save with the filename: 5.2.4a, 5.2.4b, 5.2.4c, 5.2.4d"
echo ""
echo "Expected SLA Metrics:"
echo "- STT Latency: <800ms (most requests)"
echo "- LLM First-Token: <1000ms (most requests)"
echo "- TTS Response: <1500ms (most requests)"
echo ""
echo "If dashboards show no data, run the test data generator again:"
echo "python3 generate_sla_test_data.py"
echo ""
echo "All Grafana dashboards are now open for screenshot capture!"

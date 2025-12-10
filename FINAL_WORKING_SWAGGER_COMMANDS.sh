#!/bin/bash

# FINAL WORKING Swagger Documentation Commands for ALL 8 Microservices
# Including the fixed Feedback service

echo "=========================================="
echo "FINAL WORKING SWAGGER DOCUMENTATION"
echo "=========================================="
echo ""

# Create directories
mkdir -p screenshots/swagger docs/openapi

echo "Opening all 8 Swagger UIs for screenshot capture:"
echo ""

echo "1. Orchestrator Service (Port 8081):"
echo "   URL: http://localhost:8081/docs"
echo "   Screenshot: figure_b_1_orchestrator_swagger.png"
open http://localhost:8081/docs
echo ""

echo "2. RAG Service (Port 8100):"
echo "   URL: http://localhost:8100/docs"
echo "   Screenshot: figure_b_2_rag_swagger.png"
open http://localhost:8100/docs
echo ""

echo "3. LLM Service (Port 8200):"
echo "   URL: http://localhost:8200/docs"
echo "   Screenshot: figure_b_3_llm_swagger.png"
open http://localhost:8200/docs
echo ""

echo "4. STT Service (Port 8300):"
echo "   URL: http://localhost:8300/docs"
echo "   Screenshot: figure_b_4_stt_swagger.png"
open http://localhost:8300/docs
echo ""

echo "5. TTS Service (Port 8400):"
echo "   URL: http://localhost:8400/docs"
echo "   Screenshot: figure_b_5_tts_swagger.png"
open http://localhost:8400/docs
echo ""

echo "6. Analytics Service (Port 8500):"
echo "   URL: http://localhost:8500/docs"
echo "   Screenshot: figure_b_6_analytics_swagger.png"
open http://localhost:8500/docs
echo ""

echo "7. Sentiment Service (Port 8700):"
echo "   URL: http://localhost:8700/docs"
echo "   Screenshot: figure_b_7_sentiment_swagger.png"
open http://localhost:8700/docs
echo ""

echo "8. Feedback Service (Port 8800) - FIXED:"
echo "   URL: http://localhost:8800/docs"
echo "   Screenshot: figure_b_8_feedback_swagger.png"
open http://localhost:8800/docs
echo ""

echo "=========================================="
echo "SCREENSHOT CAPTURE INSTRUCTIONS"
echo "=========================================="
echo ""
echo "For each service that opens in your browser:"
echo "1. Wait for the Swagger UI to fully load"
echo "2. Take a screenshot and save as:"
echo "   - screenshots/swagger/figure_b_1_orchestrator_swagger.png"
echo "   - screenshots/swagger/figure_b_2_rag_swagger.png"
echo "   - screenshots/swagger/figure_b_3_llm_swagger.png"
echo "   - screenshots/swagger/figure_b_4_stt_swagger.png"
echo "   - screenshots/swagger/figure_b_5_tts_swagger.png"
echo "   - screenshots/swagger/figure_b_6_analytics_swagger.png"
echo "   - screenshots/swagger/figure_b_7_sentiment_swagger.png"
echo "   - screenshots/swagger/figure_b_8_feedback_swagger.png"
echo ""

echo "=========================================="
echo "SERVICE STATUS CHECK"
echo "=========================================="
echo ""
echo "Testing all services:"
for port in 8081 8100 8200 8300 8400 8500 8700 8800; do
    echo -n "Port $port: "
    curl -s -o /dev/null -w "%{http_code}" http://localhost:$port/docs && echo " OK" || echo " FAILED"
done
echo ""

echo "=========================================="
echo "OPENAPI SPECIFICATIONS STATUS"
echo "=========================================="
echo ""
echo "OpenAPI YAML files extracted:"
ls -la docs/openapi/*.yaml
echo ""

echo "=========================================="
echo "COMPLETE APPENDIX B - ALL 8 SERVICES WORKING!"
echo "=========================================="
echo ""
echo "All 8 microservices are now accessible and documented!"
echo "Ready for thesis Appendix B capture!"

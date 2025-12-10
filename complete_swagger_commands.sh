#!/bin/bash

# Complete Swagger Documentation Commands for ALL 8 Microservices
# Including Sentiment and Feedback services

echo "=========================================="
echo "COMPLETE SWAGGER DOCUMENTATION CAPTURE"
echo "=========================================="
echo ""

# Create directories
mkdir -p screenshots/swagger docs/openapi

echo "Opening all Swagger UIs for manual screenshot capture:"
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

echo "8. Feedback Service (Port 8800):"
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
echo "OPENAPI SPECIFICATIONS STATUS"
echo "=========================================="
echo ""
echo "OpenAPI YAML files extracted:"
ls -la docs/openapi/*.yaml
echo ""

echo "=========================================="
echo "UPDATED APPENDIX B STRUCTURE"
echo "=========================================="
echo ""
echo "B.1 Orchestrator Service"
echo "B.2 RAG Service"
echo "B.3 LLM Service"
echo "B.4 STT Service"
echo "B.5 TTS Service"
echo "B.6 Analytics Service"
echo "B.7 Sentiment Service"
echo "B.8 Feedback Service"
echo ""
echo "All 8 microservices are now documented!"

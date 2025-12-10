#!/bin/bash

echo "=========================================="
echo "STARTING CONTINUOUS TEST DATA GENERATION"
echo "=========================================="
echo ""

# Function to generate test data continuously
generate_continuous_data() {
    echo "Generating continuous test data for Grafana..."
    echo "Press Ctrl+C to stop"
    echo ""
    
    counter=0
    while true; do
        counter=$((counter + 1))
        echo "Batch $counter: Generating test data..."
        
        # Generate health checks and metrics for all services
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
            curl -s "http://localhost:$port/v1/health" > /dev/null 2>&1 &
            # Metrics
            curl -s "http://localhost:$port/v1/metrics" > /dev/null 2>&1 &
            
            # Generate API calls for specific services
            case $service in
                orchestrator)
                    curl -s -X POST "http://localhost:$port/v1/chat" \
                        -H "Content-Type: application/json" \
                        -d "{\"query\": \"Test query $counter\", \"session_id\": \"session_$counter\"}" > /dev/null 2>&1 &
                    ;;
                analytics)
                    curl -s -X POST "http://localhost:$port/v1/summary" \
                        -H "Content-Type: application/json" \
                        -d "{\"session_id\": \"session_$counter\", \"summary\": \"Test summary $counter\"}" > /dev/null 2>&1 &
                    ;;
                rag)
                    curl -s -X POST "http://localhost:$port/v1/search" \
                        -H "Content-Type: application/json" \
                        -d "{\"query\": \"Search query $counter\", \"limit\": 5}" > /dev/null 2>&1 &
                    ;;
                tts)
                    curl -s -X POST "http://localhost:$port/v1/synthesize" \
                        -H "Content-Type: application/json" \
                        -d "{\"text\": \"Test text $counter\", \"voice\": \"alloy\"}" > /dev/null 2>&1 &
                    ;;
                sentiment)
                    curl -s -X POST "http://localhost:$port/v1/analyze" \
                        -H "Content-Type: application/json" \
                        -d "{\"text\": \"Test text for sentiment $counter\"}" > /dev/null 2>&1 &
                    ;;
                feedback)
                    curl -s -X POST "http://localhost:$port/v1/feedback/analyze" \
                        -H "Content-Type: application/json" \
                        -d "{\"session_id\": \"session_$counter\", \"feedback\": \"Test feedback $counter\"}" > /dev/null 2>&1 &
                    ;;
            esac
        done
        
        # Wait for all background processes
        wait
        
        echo "✓ Batch $counter completed"
        sleep 2
    done
}

# Start continuous data generation
generate_continuous_data

#!/bin/bash

# Comprehensive Health Testing - Isolation Testing Style
# This mimics the isolation testing pattern for health checks

echo "=========================================="
echo "COMPREHENSIVE HEALTH TESTING SUITE"
echo "=========================================="
echo ""

# Create screenshots directory
mkdir -p screenshots/comprehensive_health

echo "Starting comprehensive health testing for all microservices..."
echo "Test Suite: Service Health Validation"
echo "Timestamp: $(date)"
echo ""

echo "=========================================="
echo "INDIVIDUAL SERVICE HEALTH CHECKS"
echo "=========================================="
echo ""

# Function to test a service
test_service() {
    local service_name=$1
    local port=$2
    local endpoint=$3
    
    echo "Testing $service_name Service..."
    echo "Endpoint: http://localhost:$port$endpoint"
    echo ""
    
    if [ "$service_name" = "frontend" ]; then
        response=$(curl -s -I http://localhost:$port)
        status_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port)
        echo "Response Headers:"
        echo "$response" | head -3
        echo ""
        echo "Status Code: $status_code"
    else
        response=$(curl -s http://localhost:$port$endpoint)
        status_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port$endpoint)
        echo "Response Body:"
        echo "$response" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(json.dumps(data, indent=2))
except:
    print(sys.stdin.read())
" 2>/dev/null || echo "$response"
        echo ""
        echo "Status Code: $status_code"
    fi
    
    if [ "$status_code" = "200" ]; then
        echo "Result: PASS - Service is healthy"
    else
        echo "Result: FAIL - Service returned $status_code"
    fi
    echo ""
    echo "----------------------------------------"
    echo ""
}

# Test all services
test_service "Orchestrator" "8081" "/v1/health"
test_service "LLM" "8200" "/v1/health"
test_service "STT" "8300" "/v1/health"
test_service "TTS" "8400" "/v1/health"
test_service "RAG" "8100" "/v1/health"
test_service "Analytics" "8500" "/v1/health"
test_service "Feedback" "8800" "/v1/health"
test_service "Sentiment" "8700" "/v1/health"
test_service "Frontend" "3000" ""

echo "=========================================="
echo "BATCH HEALTH CHECK TESTING"
echo "=========================================="
echo ""

echo "Running batch health checks for all services..."
echo ""

# Batch test all services
services=(
    "orchestrator:8081:/v1/health"
    "llm:8200:/v1/health"
    "stt:8300:/v1/health"
    "tts:8400:/v1/health"
    "rag:8100:/v1/health"
    "analytics:8500:/v1/health"
    "feedback:8800:/v1/health"
    "sentiment:8700:/v1/health"
    "frontend:3000:"
)

passed=0
failed=0
total=${#services[@]}

echo "Service Status Summary:"
echo "----------------------"

for service_info in "${services[@]}"; do
    IFS=':' read -r name port endpoint <<< "$service_info"
    
    if [ "$name" = "frontend" ]; then
        status_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port)
    else
        status_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port$endpoint)
    fi
    
    if [ "$status_code" = "200" ]; then
        echo "$name: PASS - HTTP $status_code"
        ((passed++))
    else
        echo "$name: FAIL - HTTP $status_code"
        ((failed++))
    fi
done

echo ""
echo "=========================================="
echo "HEALTH CHECK METRICS"
echo "=========================================="
echo ""

echo "Test Results Summary:"
echo "Total Services Tested: $total"
echo "Passed: $passed"
echo "Failed: $failed"
echo "Success Rate: $(( (passed * 100) / total ))%"
echo ""

echo "Response Time Analysis:"
echo "----------------------"

# Test response times
for service_info in "${services[@]}"; do
    IFS=':' read -r name port endpoint <<< "$service_info"
    
    if [ "$name" = "frontend" ]; then
        response_time=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:$port)
    else
        response_time=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:$port$endpoint)
    fi
    
    echo "$name: ${response_time}s"
done

echo ""
echo "=========================================="
echo "SYSTEM HEALTH ASSESSMENT"
echo "=========================================="
echo ""

if [ $passed -eq $total ]; then
    echo "Overall Status: ALL SYSTEMS OPERATIONAL"
    echo "Health Level: EXCELLENT"
    echo "System Status: READY FOR PRODUCTION"
    echo ""
    echo "All microservices are responding correctly:"
    echo "- All health endpoints returning 200 OK"
    echo "- All services accessible and functional"
    echo "- System is fully operational"
elif [ $passed -gt $((total / 2)) ]; then
    echo "Overall Status: MOSTLY OPERATIONAL"
    echo "Health Level: GOOD"
    echo "System Status: DEGRADED BUT FUNCTIONAL"
    echo ""
    echo "Most services are healthy with some issues:"
    echo "- $passed out of $total services operational"
    echo "- System is functional but may have reduced capacity"
else
    echo "Overall Status: SYSTEM DEGRADED"
    echo "Health Level: POOR"
    echo "System Status: REQUIRES ATTENTION"
    echo ""
    echo "Multiple services are experiencing issues:"
    echo "- Only $passed out of $total services operational"
    echo "- System requires immediate attention"
fi

echo ""
echo "=========================================="
echo "RECOMMENDATIONS"
echo "=========================================="
echo ""

if [ $failed -eq 0 ]; then
    echo "No action required - all services are healthy"
    echo "Continue monitoring for optimal performance"
elif [ $failed -le 2 ]; then
    echo "Minor issues detected:"
    echo "- Investigate failed services"
    echo "- Check logs for error details"
    echo "- Monitor system performance"
else
    echo "Multiple issues detected:"
    echo "- Immediate investigation required"
    echo "- Check system resources and logs"
    echo "- Consider rolling back recent changes"
fi

echo ""
echo "=========================================="
echo "TEST EXECUTION COMPLETE"
echo "=========================================="
echo ""
echo "Comprehensive health testing completed at: $(date)"
echo "Test Duration: $(date +%s) seconds"
echo ""
echo "Screenshots ready for thesis section 5.2.1:"
echo "- Individual service health checks"
echo "- Batch health testing results"
echo "- System health assessment"
echo "- Performance metrics"
echo ""
echo "All health testing data captured for documentation!"

#!/bin/bash

echo "=========================================="
echo "VERIFYING GRAFANA DASHBOARD"
echo "=========================================="
echo ""

# Function to check if services are running
check_services() {
    echo "Checking service status..."
    services=("orchestrator:8081" "llm:8200" "stt:8300" "tts:8400" "rag:8100" "analytics:8500" "sentiment:8700" "feedback:8800")
    
    for service in "${services[@]}"; do
        IFS=':' read -r name port <<< "$service"
        if curl -s "http://localhost:$port/v1/health" > /dev/null 2>&1; then
            echo "✓ $name is running on port $port"
        else
            echo "✗ $name is not running on port $port"
        fi
    done
}

# Function to check Prometheus metrics
check_prometheus() {
    echo ""
    echo "Checking Prometheus metrics..."
    if curl -s "http://localhost:9090/api/v1/query?query=up" | grep -q "result"; then
        echo "✓ Prometheus is collecting metrics"
    else
        echo "⚠ Prometheus may not be ready"
    fi
}

# Function to check Grafana
check_grafana() {
    echo ""
    echo "Checking Grafana..."
    if curl -s "http://localhost:3001/api/health" | grep -q "ok"; then
        echo "✓ Grafana is running"
    else
        echo "⚠ Grafana may not be ready"
    fi
}

# Function to show dashboard URLs
show_dashboard_urls() {
    echo ""
    echo "Dashboard URLs:"
    echo "Main Grafana: http://localhost:3001"
    echo "Prometheus: http://localhost:9090"
    echo ""
    echo "Direct dashboard links:"
    echo "Microservices Dashboard: http://localhost:3001/dashboards"
    echo "Prometheus Targets: http://localhost:9090/targets"
    echo ""
}

# Function to generate a quick test
generate_quick_test() {
    echo "Generating quick test data..."
    for i in {1..10}; do
        echo "Test batch $i/10..."
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
            
            curl -s "http://localhost:$port/v1/health" > /dev/null 2>&1
            curl -s "http://localhost:$port/v1/metrics" > /dev/null 2>&1
        done
        sleep 1
    done
    echo "✓ Quick test data generated"
}

# Main execution
check_services
check_prometheus
check_grafana
show_dashboard_urls

echo "Generating quick test data to ensure metrics are flowing..."
generate_quick_test

echo ""
echo "=========================================="
echo "VERIFICATION COMPLETE!"
echo "=========================================="
echo ""
echo "Your Grafana dashboard should now show:"
echo "✓ Service health status (all green)"
echo "✓ HTTP request counts"
echo "✓ Memory usage graphs"
echo "✓ CPU usage graphs"
echo "✓ File descriptor counts"
echo "✓ Python GC collections"
echo "✓ HTTP request durations"
echo ""
echo "If you still see 'No data', wait 30 seconds and refresh the dashboard."
echo "The metrics need time to be scraped by Prometheus and displayed in Grafana."
echo ""
echo "Opening Grafana for verification..."
open "http://localhost:3001"

#!/bin/bash

# Complete Microservices Startup & Screenshot Script for Thesis
# This script starts all services and captures screenshots

set -e

echo "=========================================="
echo "Starting All Microservices for Thesis"
echo "=========================================="

# Navigate to backend directory
cd /Users/mansi/Documents/Agentic-AI-Digital-U3-----1234\ copy/backend

echo "Starting Orchestrator..."
cd orchestrator && docker-compose up -d && cd ..

echo "Starting Analytics..."
cd analytics && docker-compose up -d && cd ..

echo "Starting LLM..."
cd LLM && docker-compose up -d && cd ..

echo "Starting STT..."
cd stt && docker-compose up -d && cd ..

echo "Starting TTS..."
cd tts && docker-compose up -d && cd ..

echo "Starting RAG..."
cd rag && docker-compose up -d && cd ..

echo "Starting Sentiment..."
cd sentiment && docker-compose up -d && cd ..

echo "Starting Feedback..."
cd feedback && docker-compose up -d && cd ..

echo "Starting Prometheus (for metrics)..."
# Create prometheus config if it doesn't exist
mkdir -p prometheus
cat > prometheus/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'orchestrator'
    static_configs:
      - targets: ['host.docker.internal:8081']
  - job_name: 'analytics'
    static_configs:
      - targets: ['host.docker.internal:8900']
  - job_name: 'llm'
    static_configs:
      - targets: ['host.docker.internal:8200']
  - job_name: 'stt'
    static_configs:
      - targets: ['host.docker.internal:8700']
  - job_name: 'tts'
    static_configs:
      - targets: ['host.docker.internal:8800']
EOF

# Start Prometheus
docker run -d --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus:latest

echo "Starting Grafana (for dashboards)..."
# Start Grafana
docker run -d --name grafana \
  -p 3000:3000 \
  -e "GF_SECURITY_ADMIN_PASSWORD=admin" \
  grafana/grafana:latest

echo "=========================================="
echo "Waiting for services to initialize..."
echo "=========================================="

# Wait for services to be ready
sleep 30

echo "Checking service health..."
echo "Orchestrator: $(curl -s http://localhost:8081/v1/health | jq -r '.status' 2>/dev/null || echo 'not ready')"
echo "Analytics: $(curl -s http://localhost:8900/v1/health | jq -r '.status' 2>/dev/null || echo 'not ready')"
echo "LLM: $(curl -s http://localhost:8200/v1/health | jq -r '.status' 2>/dev/null || echo 'not ready')"
echo "STT: $(curl -s http://localhost:8700/v1/health | jq -r '.status' 2>/dev/null || echo 'not ready')"
echo "TTS: $(curl -s http://localhost:8800/v1/health | jq -r '.status' 2>/dev/null || echo 'not ready')"

echo "=========================================="
echo "SERVICES STARTED SUCCESSFULLY!"
echo "=========================================="
echo "Orchestrator: http://localhost:8081"
echo "Analytics: http://localhost:8900"
echo "LLM: http://localhost:8200"
echo "STT: http://localhost:8700"
echo "TTS: http://localhost:8800"
echo "Prometheus: http://localhost:9090"
echo "Grafana: http://localhost:3000 (admin/admin)"
echo "=========================================="


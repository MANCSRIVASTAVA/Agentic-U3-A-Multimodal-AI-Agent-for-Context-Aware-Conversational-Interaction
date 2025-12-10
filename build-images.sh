#!/bin/bash

# Docker Image Build Script for Agentic AI System
# Builds all microservices including sentiment and feedback

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}DOCKER IMAGE BUILD SCRIPT${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# Function to build a service
build_service() {
    local service=$1
    local context=$2
    local dockerfile=$3
    
    echo -e "${YELLOW}Building ${service}...${NC}"
    
    if [ -f "${dockerfile}" ]; then
        docker build -t ${service}:latest -f ${dockerfile} ${context}
        echo -e "${GREEN}✓ ${service} built successfully${NC}"
    else
        echo -e "${RED}✗ Dockerfile not found: ${dockerfile}${NC}"
        return 1
    fi
}

# Build all services
echo -e "${YELLOW}Building all microservices...${NC}"
echo ""

# Backend services
build_service "orchestrator" "./backend/orchestrator" "./backend/orchestrator/Dockerfile"
build_service "rag" "./backend/rag" "./backend/rag/Dockerfile"
build_service "llm" "./backend/LLM" "./backend/LLM/Dockerfile"
build_service "stt" "./backend/stt" "./backend/stt/Dockerfile"
build_service "tts" "./backend/tts" "./backend/tts/Dockerfile"
build_service "analytics" "./backend/analytics" "./backend/analytics/Dockerfile"
build_service "sentiment" "./backend/sentiment" "./backend/sentiment/Dockerfile"
build_service "feedback" "./backend/feedback" "./backend/feedback/Dockerfile"

# Frontend
build_service "frontend" "./frontend" "./frontend/Dockerfile"

echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}ALL IMAGES BUILT SUCCESSFULLY!${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""

# Show built images
echo -e "${YELLOW}Built images:${NC}"
docker images | grep -E "(orchestrator|rag|llm|stt|tts|analytics|sentiment|feedback|frontend)" | head -10

echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Deploy to Kubernetes: ./k8s/deploy.sh"
echo "2. Or use Docker Compose: docker-compose up -d"
echo "3. Check service status: kubectl get pods -n agentic-ai"

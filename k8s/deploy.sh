#!/bin/bash

# Kubernetes Deployment Script for Agentic AI System
# This script deploys all microservices to Kubernetes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="agentic-ai"
TIMEOUT="300s"

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}KUBERNETES DEPLOYMENT SCRIPT${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# Function to check if kubectl is available
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        echo -e "${RED}Error: kubectl is not installed or not in PATH${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ kubectl is available${NC}"
}

# Function to check if cluster is accessible
check_cluster() {
    if ! kubectl cluster-info &> /dev/null; then
        echo -e "${RED}Error: Cannot connect to Kubernetes cluster${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Kubernetes cluster is accessible${NC}"
}

# Function to create namespace
create_namespace() {
    echo -e "${YELLOW}Creating namespace: ${NAMESPACE}${NC}"
    kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
    echo -e "${GREEN}✓ Namespace created/updated${NC}"
}

# Function to deploy ConfigMap
deploy_configmap() {
    echo -e "${YELLOW}Deploying ConfigMap...${NC}"
    kubectl apply -f configmap.yaml
    echo -e "${GREEN}✓ ConfigMap deployed${NC}"
}

# Function to deploy data services
deploy_data_services() {
    echo -e "${YELLOW}Deploying data services...${NC}"
    kubectl apply -f data/
    echo -e "${GREEN}✓ Data services deployed${NC}"
}

# Function to wait for data services
wait_for_data_services() {
    echo -e "${YELLOW}Waiting for data services to be ready...${NC}"
    
    echo "Waiting for Redis..."
    kubectl wait --for=condition=ready pod -l app=redis -n ${NAMESPACE} --timeout=${TIMEOUT}
    
    echo "Waiting for PostgreSQL..."
    kubectl wait --for=condition=ready pod -l app=postgres -n ${NAMESPACE} --timeout=${TIMEOUT}
    
    echo "Waiting for ClickHouse..."
    kubectl wait --for=condition=ready pod -l app=clickhouse -n ${NAMESPACE} --timeout=${TIMEOUT}
    
    echo "Waiting for Qdrant..."
    kubectl wait --for=condition=ready pod -l app=qdrant -n ${NAMESPACE} --timeout=${TIMEOUT}
    
    echo "Waiting for MinIO..."
    kubectl wait --for=condition=ready pod -l app=minio -n ${NAMESPACE} --timeout=${TIMEOUT}
    
    echo -e "${GREEN}✓ All data services are ready${NC}"
}

# Function to deploy backend services
deploy_backend_services() {
    echo -e "${YELLOW}Deploying backend services...${NC}"
    kubectl apply -f backend/
    echo -e "${GREEN}✓ Backend services deployed${NC}"
}

# Function to deploy frontend
deploy_frontend() {
    echo -e "${YELLOW}Deploying frontend...${NC}"
    kubectl apply -f frontend/
    echo -e "${GREEN}✓ Frontend deployed${NC}"
}

# Function to deploy observability
deploy_observability() {
    echo -e "${YELLOW}Deploying observability services...${NC}"
    kubectl apply -f observability/
    echo -e "${GREEN}✓ Observability services deployed${NC}"
}

# Function to wait for all deployments
wait_for_deployments() {
    echo -e "${YELLOW}Waiting for all deployments to be ready...${NC}"
    kubectl wait --for=condition=available deployment --all -n ${NAMESPACE} --timeout=600s
    echo -e "${GREEN}✓ All deployments are ready${NC}"
}

# Function to show status
show_status() {
    echo -e "${BLUE}==========================================${NC}"
    echo -e "${BLUE}DEPLOYMENT STATUS${NC}"
    echo -e "${BLUE}==========================================${NC}"
    echo ""
    
    echo -e "${YELLOW}Pods:${NC}"
    kubectl get pods -n ${NAMESPACE}
    echo ""
    
    echo -e "${YELLOW}Services:${NC}"
    kubectl get services -n ${NAMESPACE}
    echo ""
    
    echo -e "${YELLOW}Deployments:${NC}"
    kubectl get deployments -n ${NAMESPACE}
    echo ""
}

# Function to show service URLs
show_service_urls() {
    echo -e "${BLUE}==========================================${NC}"
    echo -e "${BLUE}SERVICE ACCESS URLs${NC}"
    echo -e "${BLUE}==========================================${NC}"
    echo ""
    
    # Get the cluster IP or use port-forward
    echo -e "${YELLOW}To access services, use port-forward:${NC}"
    echo "kubectl port-forward -n ${NAMESPACE} service/orchestrator 8081:8000"
    echo "kubectl port-forward -n ${NAMESPACE} service/rag 8100:8000"
    echo "kubectl port-forward -n ${NAMESPACE} service/llm 8200:8000"
    echo "kubectl port-forward -n ${NAMESPACE} service/stt 8300:8000"
    echo "kubectl port-forward -n ${NAMESPACE} service/tts 8400:8000"
    echo "kubectl port-forward -n ${NAMESPACE} service/analytics 8500:8000"
    echo "kubectl port-forward -n ${NAMESPACE} service/sentiment 8700:8000"
    echo "kubectl port-forward -n ${NAMESPACE} service/feedback 8800:8000"
    echo "kubectl port-forward -n ${NAMESPACE} service/frontend 3000:3000"
    echo ""
}

# Main deployment function
main() {
    echo -e "${BLUE}Starting Kubernetes deployment...${NC}"
    echo ""
    
    check_kubectl
    check_cluster
    create_namespace
    deploy_configmap
    deploy_data_services
    wait_for_data_services
    deploy_backend_services
    deploy_frontend
    deploy_observability
    wait_for_deployments
    show_status
    show_service_urls
    
    echo -e "${GREEN}==========================================${NC}"
    echo -e "${GREEN}DEPLOYMENT COMPLETED SUCCESSFULLY!${NC}"
    echo -e "${GREEN}==========================================${NC}"
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "status")
        show_status
        ;;
    "urls")
        show_service_urls
        ;;
    "clean")
        echo -e "${YELLOW}Cleaning up deployment...${NC}"
        kubectl delete namespace ${NAMESPACE}
        echo -e "${GREEN}✓ Cleanup completed${NC}"
        ;;
    *)
        echo "Usage: $0 {deploy|status|urls|clean}"
        echo "  deploy - Deploy all services (default)"
        echo "  status - Show deployment status"
        echo "  urls   - Show service access URLs"
        echo "  clean  - Clean up deployment"
        exit 1
        ;;
esac
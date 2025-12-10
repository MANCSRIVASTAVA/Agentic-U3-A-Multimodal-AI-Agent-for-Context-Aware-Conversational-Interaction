# Kubernetes Deployment for Agentic AI System

This directory contains Kubernetes manifests for deploying the complete Agentic AI microservices system.

## 🏗️ Architecture

The system consists of:

### Backend Services
- **Orchestrator** - Central coordination service
- **RAG** - Retrieval-Augmented Generation service
- **LLM** - Large Language Model service
- **STT** - Speech-to-Text service
- **TTS** - Text-to-Speech service
- **Analytics** - Analytics and reporting service
- **Sentiment** - Sentiment analysis service ✨ **NEW**
- **Feedback** - User feedback analysis service ✨ **NEW**

### Data Services
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage
- **ClickHouse** - Analytics database
- **Qdrant** - Vector database
- **MinIO** - Object storage

### Frontend
- **Frontend** - React-based user interface

### Observability
- **Prometheus** - Metrics collection
- **Grafana** - Monitoring dashboards

## 📁 Directory Structure

```
k8s/
├── backend/           # Backend service deployments
│   ├── orchestrator.yaml
│   ├── rag.yaml
│   ├── llm.yaml
│   ├── stt.yaml
│   ├── tts.yaml
│   ├── analytics.yaml
│   ├── sentiment.yaml  # ✨ NEW
│   └── feedback.yaml   # ✨ NEW
├── data/              # Data service deployments
│   ├── postgres.yaml
│   ├── redis.yaml
│   ├── clickhouse.yaml
│   ├── qdrant.yaml
│   └── minio.yaml
├── frontend/          # Frontend deployment
│   └── frontend.yaml
├── observability/     # Monitoring deployments
│   ├── prometheus.yaml
│   └── grafana.yaml
├── configmap.yaml     # Application configuration
├── namespace.yaml     # Namespace definition
├── deploy.sh          # Deployment script
└── README.md          # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Kubernetes cluster** (local or cloud)
2. **kubectl** configured to access your cluster
3. **Docker images** built and available in your registry

### Deploy All Services

```bash
# Make the deployment script executable
chmod +x deploy.sh

# Deploy all services
./deploy.sh

# Or deploy step by step
./deploy.sh deploy
```

### Check Deployment Status

```bash
# Show deployment status
./deploy.sh status

# Show service access URLs
./deploy.sh urls
```

### Clean Up

```bash
# Remove all deployments
./deploy.sh clean
```

## 🔧 Manual Deployment

If you prefer to deploy manually:

```bash
# Create namespace
kubectl create namespace agentic-ai

# Deploy ConfigMap
kubectl apply -f configmap.yaml

# Deploy data services
kubectl apply -f data/

# Wait for data services
kubectl wait --for=condition=ready pod -l app=redis -n agentic-ai --timeout=300s
kubectl wait --for=condition=ready pod -l app=postgres -n agentic-ai --timeout=300s
kubectl wait --for=condition=ready pod -l app=clickhouse -n agentic-ai --timeout=300s

# Deploy backend services
kubectl apply -f backend/

# Deploy frontend
kubectl apply -f frontend/

# Deploy observability
kubectl apply -f observability/
```

## 🌐 Service Access

After deployment, access services using port-forward:

```bash
# Orchestrator (Main API)
kubectl port-forward -n agentic-ai service/orchestrator 8081:8000

# Individual Services
kubectl port-forward -n agentic-ai service/rag 8100:8000
kubectl port-forward -n agentic-ai service/llm 8200:8000
kubectl port-forward -n agentic-ai service/stt 8300:8000
kubectl port-forward -n agentic-ai service/tts 8400:8000
kubectl port-forward -n agentic-ai service/analytics 8500:8000
kubectl port-forward -n agentic-ai service/sentiment 8700:8000
kubectl port-forward -n agentic-ai service/feedback 8800:8000

# Frontend
kubectl port-forward -n agentic-ai service/frontend 3000:3000

# Observability
kubectl port-forward -n agentic-ai service/prometheus 9090:9090
kubectl port-forward -n agentic-ai service/grafana 3001:3000
```

## 📊 Monitoring

Access monitoring dashboards:

- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

## 🔐 Configuration

All configuration is managed through the `configmap.yaml` file. Key configuration includes:

- Database connections
- Service URLs
- API keys
- Environment variables

## 🏷️ Resource Requirements

Each service has defined resource requests and limits:

- **CPU**: 250m request, 500m limit
- **Memory**: 256Mi request, 512Mi limit

## 🔄 CI/CD Integration

The deployment is integrated with GitHub Actions CI/CD pipeline:

1. **Test** - Run tests and linting
2. **Build** - Build Docker images
3. **Deploy** - Deploy to Kubernetes
4. **Security** - Run security scans
5. **Performance** - Run performance tests

## 🐛 Troubleshooting

### Common Issues

1. **Pods not starting**: Check resource limits and node capacity
2. **Services not accessible**: Verify service selectors and ports
3. **Database connection issues**: Check ConfigMap values and service names

### Debug Commands

```bash
# Check pod status
kubectl get pods -n agentic-ai

# Check pod logs
kubectl logs -n agentic-ai <pod-name>

# Check service endpoints
kubectl get endpoints -n agentic-ai

# Check ConfigMap
kubectl describe configmap app-config -n agentic-ai
```

## 📈 Scaling

To scale services:

```bash
# Scale orchestrator to 3 replicas
kubectl scale deployment orchestrator --replicas=3 -n agentic-ai

# Scale all backend services
kubectl scale deployment --replicas=3 -l tier=backend -n agentic-ai
```

## 🔒 Security

- All services run in the `agentic-ai` namespace
- Services use ClusterIP for internal communication
- External access via port-forward or Ingress
- Secrets should be managed via Kubernetes Secrets

## 📝 Notes

- Images use `imagePullPolicy: Never` for local development
- For production, update image references and pull policies
- Consider using Helm charts for more complex deployments
- Monitor resource usage and adjust limits as needed

## 🆕 Recent Updates

- ✅ Added **Sentiment** service deployment
- ✅ Added **Feedback** service deployment
- ✅ Updated ConfigMap with new service URLs
- ✅ Enhanced deployment script with better error handling
- ✅ Added comprehensive CI/CD pipeline
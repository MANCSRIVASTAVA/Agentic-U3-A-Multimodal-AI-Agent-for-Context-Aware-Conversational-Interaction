# Orchestrator Service - Complete Swagger Documentation

## ✅ **ORCHESTRATOR SERVICE - FULL DOCUMENTATION**

The Orchestrator service is the central hub of your microservices architecture, coordinating all other services.

### 🔗 **Service Access**
- **URL**: http://localhost:8081/docs
- **Status**: ✅ **WORKING** (200 OK)
- **OpenAPI Spec**: http://localhost:8081/openapi.json
- **Port**: 8081

### 📋 **Complete API Endpoints (9 total)**

| Method | Endpoint | Description | Purpose |
|--------|----------|-------------|---------|
| `GET` | `/v1/health` | Health check | Service health monitoring |
| `GET` | `/v1/config` | Get Config | Service configuration |
| `GET` | `/v1/metrics` | Prometheus Metrics | Metrics collection |
| `POST` | `/v1/chat` | Chat Sync | Synchronous chat processing |
| `GET` | `/v1/chat/stream` | Chat Stream | Streaming chat responses |
| `GET` | `/v1/chat/sse` | Chat SSE | Server-Sent Events chat |
| `POST` | `/v1/ingest` | Ingest | Document ingestion |
| `GET` | `/v1/retrieve` | Retrieve | Document retrieval |
| `POST` | `/v1/tts` | TTS | Text-to-speech synthesis |

### 🧪 **Test the Endpoints**

```bash
# Health check
curl http://localhost:8081/v1/health

# Get configuration
curl http://localhost:8081/v1/config

# Get metrics
curl http://localhost:8081/v1/metrics

# Chat sync (POST)
curl -X POST http://localhost:8081/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello", "session_id": "test123"}'

# Document ingestion
curl -X POST http://localhost:8081/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{"content": "Sample document", "metadata": {}}'

# Document retrieval
curl "http://localhost:8081/v1/retrieve?query=sample&limit=10"

# TTS synthesis
curl -X POST http://localhost:8081/v1/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "voice": "default"}'
```

### 📊 **API Response Examples**

#### Health Check Response:
```json
{
  "status": "ok",
  "service": "orchestrator",
  "timestamp": "2024-09-10T00:00:00Z"
}
```

#### Config Response:
```json
{
  "service": "orchestrator",
  "version": "1.0.0",
  "downstreams": {
    "rag": "http://rag:8000",
    "llm": "http://llm:8000",
    "stt": "ws://stt:8000/v1/transcribe/ws",
    "tts": "http://tts:8000",
    "analytics": "http://analytics:8000"
  }
}
```

#### Chat Response:
```json
{
  "response": "Hello! How can I help you today?",
  "session_id": "test123",
  "timestamp": "2024-09-10T00:00:00Z",
  "metadata": {
    "processing_time": 1.23,
    "model_used": "gpt-4o"
  }
}
```

### 📁 **OpenAPI Specification Details**

- **File**: `docs/openapi/orchestrator_openapi.yaml`
- **Size**: 7.9 KB
- **Version**: OpenAPI 3.1.0
- **Schemas**: ConfigResponse, Downstreams, HTTPValidationError, ValidationError

### 🏗️ **Service Architecture**

The Orchestrator service acts as the central coordinator for:

1. **Chat Processing**: Handles both sync and async chat requests
2. **Service Discovery**: Manages connections to downstream services
3. **Document Management**: Coordinates RAG ingestion and retrieval
4. **Audio Processing**: Manages TTS synthesis requests
5. **Health Monitoring**: Provides service health and metrics

### 🔧 **Technical Details**

- **Framework**: FastAPI with Uvicorn
- **Port**: 8081 (host) → 8000 (container)
- **Authentication**: Middleware-based (bypassed for docs)
- **CORS**: Enabled for frontend integration
- **Dependencies**: Redis, PostgreSQL, MinIO, Qdrant, ClickHouse

### 📈 **Service Dependencies**

The Orchestrator coordinates with:
- **RAG Service** (Port 8100): Document retrieval and search
- **LLM Service** (Port 8200): Text generation and chat
- **STT Service** (Port 8300): Speech-to-text processing
- **TTS Service** (Port 8400): Text-to-speech synthesis
- **Analytics Service** (Port 8500): Data analytics and reporting

### 🎯 **Ready for Screenshot**

The Orchestrator service Swagger UI is fully functional and ready for screenshot capture:
- **Screenshot file**: `screenshots/swagger/figure_b_1_orchestrator_swagger.png`
- **URL**: http://localhost:8081/docs
- **Status**: All 9 endpoints working and documented

### 📝 **Key Features**

1. **Centralized API**: Single entry point for all microservices
2. **Streaming Support**: Real-time chat with SSE and WebSocket
3. **Document Management**: Complete RAG pipeline integration
4. **Audio Processing**: TTS synthesis capabilities
5. **Health Monitoring**: Comprehensive service status and metrics
6. **Error Handling**: Robust error responses and validation

The Orchestrator service is the backbone of your microservices architecture and is fully documented and ready for your thesis! 🎯

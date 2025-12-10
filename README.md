# Agentic AI-Powered Multimodal Assistant (Project U3)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


A modular, microservice-based AI system designed to handle real-time speech transcription, natural language processing, dialogue orchestration, and multimodal interaction. Built to scale and deploy with Docker & CI/CD.

---

## Architecture

```
/Agentic-AI-Digital-U3
├── MicroServices
│   ├── STT               # Speech-to-Text service using Whisper/Faster-Whisper
│   ├── TTS               # Text-to-Speech using ElevenLabs & gTTS
│   ├── LLM Agent         # Handles LLM queries using OpenAI / HF
│   ├── Orchestrator      # Directs data flow between services
│   ├── Analytics         # Logs, metrics, WPM, latency
│   └── Dialogue_Steering # (Planned) for conversation state mgmt
├── Memory                # Vector DB & Redis for caching/memory
├── Frontend              # (Optional) Webapp built with React
├── Scripts               # Dev/test tools
├── docker-compose.yml    # Service orchestration
└── .github/workflows     # CI/CD GitHub Actions
```

---

## Goals

- Modular and independently deployable microservices
- Real-time WebSocket streaming support for audio
- Language detection and fallback STT/LLM logic
- Dockerized infrastructure
- GitHub Actions CI/CD setup
- Ready for Kubernetes (optional future)

---

## Tech Stack

- **Backend:** FastAPI • Uvicorn • Python
- **Models:** OpenAI Whisper • Faster-Whisper
- **Speech:** ElevenLabs • gTTS
- **Memory:** Redis • FAISS
- **Audio:** PyDub • ffmpeg
- **DevOps:** Docker • GitHub Actions
- **Frontend (Optional):** React + Tailwind

---

## CI/CD Pipeline

> Uses **GitHub Actions** to automate:

- Code formatting, linting
- Build & test pipeline
- Docker image creation
- Health check endpoints
- Optional: Deploy to cloud or VPS

📁 Config located at: `.github/workflows/ci.yml`

---

## How to Run (Locally with Docker)

```bash
# Build all services
docker compose build

# Run a specific service
docker compose up stt

# Or run everything
docker compose up
```

---


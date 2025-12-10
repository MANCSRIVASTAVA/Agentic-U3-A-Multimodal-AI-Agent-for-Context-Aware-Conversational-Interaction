
# Backend Docker Pack (services only)

This pack adds per-service Dockerfiles, requirements, .dockerignore and docker-compose.yml files.
Use alongside your existing `data/` and `obs/` stacks.

## Start everything (data + obs + services)
docker compose \
  -f data/docker-compose.data.yml \
  -f obs/docker-compose.obs.yml \
  -f Services/analytics/docker-compose.yml \
  -f Services/LLM/docker-compose.yml \
  -f Services/stt/docker-compose.yml \
  -f Services/tts/docker-compose.yml \
  -f Services/rag/docker-compose.yml \
  -f Services/orchestrator/docker-compose.yml \
  up -d --build

## Notes
- Each service mounts `../../shared` into the container at `/app/shared` (read-only).
- Each service mounts its local `app/` folder at `/app/app` (read-only) for dev.
- All services listen on container port 8000; host ports:
  - orchestrator: 8080
  - rag: 8100
  - llm: 8200
  - stt: 8300
  - tts: 8400
  - analytics: 8500

# Observability Stack (Local, Free)

Includes **Prometheus (9090)**, **Grafana (3000)**, **Loki (3100)**, **Promtail**, **Tempo (3200)**, and **OpenTelemetry Collector (4318 HTTP)**.

## Prereq

Create a shared Docker network once:
```bash
docker network create agentic-net || true
```

Ensure your microservices join this network and expose **/v1/metrics** on port **8000**
with service names: `orchestrator, rag, llm, stt, tts, analytics`.

## Bring up

```bash
cd obs
docker compose -f docker-compose.obs.yml up -d
```

- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
- Loki: http://localhost:3100
- Tempo: http://localhost:3200
- OTLP HTTP ingest: http://localhost:4318

## Wire services

- **Metrics:** expose `/v1/metrics` on `:8000`.
- **Traces:** set in each service: `OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318`
- **Logs:** Docker logs are tailed by Promtail and shipped to Loki. Labels include `service` (Compose service name).

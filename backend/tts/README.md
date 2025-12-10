# TTS Service (Phase 8)

## Quickstart
```bash
cd services/tts
cp .env.example .env
docker build -t tts-service .
docker run --rm -p 8400:8000 --env-file .env tts-service
# or
docker compose up --build
```

## Test
```bash
curl -N -X POST http://localhost:8400/v1/tts \
  -H 'Content-Type: application/json' \
  -d '{"text":"Hello world","voice":"female_en","format":"mp3"}'
```

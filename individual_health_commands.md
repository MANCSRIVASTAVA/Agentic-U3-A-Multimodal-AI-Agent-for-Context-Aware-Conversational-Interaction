# Section 5.2.1 - Service Health Checks Screenshots

## Individual Commands for Each Screenshot

### 5.2.1a - Orchestrator /v1/health (JSON 200 OK)
```bash
# Open in browser
open http://localhost:8081/v1/health

# Test response
curl -s http://localhost:8081/v1/health | python3 -m json.tool

# Screenshot: screenshot_5_2_1a_orchestrator_health.png
```

### 5.2.1b - LLM /v1/health
```bash
# Open in browser
open http://localhost:8200/v1/health

# Test response
curl -s http://localhost:8200/v1/health | python3 -m json.tool

# Screenshot: screenshot_5_2_1b_llm_health.png
```

### 5.2.1c - STT /v1/health
```bash
# Open in browser
open http://localhost:8300/v1/health

# Test response
curl -s http://localhost:8300/v1/health | python3 -m json.tool

# Screenshot: screenshot_5_2_1c_stt_health.png
```

### 5.2.1d - TTS /v1/health
```bash
# Open in browser
open http://localhost:8400/v1/health

# Test response
curl -s http://localhost:8400/v1/health | python3 -m json.tool

# Screenshot: screenshot_5_2_1d_tts_health.png
```

### 5.2.1e - RAG /v1/health
```bash
# Open in browser
open http://localhost:8100/v1/health

# Test response
curl -s http://localhost:8100/v1/health | python3 -m json.tool

# Screenshot: screenshot_5_2_1e_rag_health.png
```

### 5.2.1f - Analytics /v1/health
```bash
# Open in browser
open http://localhost:8500/v1/health

# Test response
curl -s http://localhost:8500/v1/health | python3 -m json.tool

# Screenshot: screenshot_5_2_1f_analytics_health.png
```

### 5.2.1g - Feedback /v1/health
```bash
# Open in browser
open http://localhost:8800/v1/health

# Test response
curl -s http://localhost:8800/v1/health | python3 -m json.tool

# Screenshot: screenshot_5_2_1g_feedback_health.png
```

### 5.2.1h - Sentiment /v1/health
```bash
# Open in browser
open http://localhost:8700/v1/health

# Test response
curl -s http://localhost:8700/v1/health | python3 -m json.tool

# Screenshot: screenshot_5_2_1h_sentiment_health.png
```

### 5.2.1i - Frontend health (dev server status)
```bash
# Open in browser
open http://localhost:3000

# Test response
curl -s -I http://localhost:3000

# Screenshot: screenshot_5_2_1i_frontend_health.png
```

## Quick Test All Services
```bash
# Test all health endpoints at once
for port in 8081 8200 8300 8400 8100 8500 8800 8700; do
  echo "Port $port: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port/v1/health)"
done

# Test frontend
echo "Frontend: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)"
```

## Screenshot Directory Structure
```
screenshots/health_checks/
├── screenshot_5_2_1a_orchestrator_health.png
├── screenshot_5_2_1b_llm_health.png
├── screenshot_5_2_1c_stt_health.png
├── screenshot_5_2_1d_tts_health.png
├── screenshot_5_2_1e_rag_health.png
├── screenshot_5_2_1f_analytics_health.png
├── screenshot_5_2_1g_feedback_health.png
├── screenshot_5_2_1h_sentiment_health.png
└── screenshot_5_2_1i_frontend_health.png
```

## Expected Health Check Responses

### Backend Services (JSON)
```json
{
  "status": "ok"
}
```

### Frontend (HTML)
```html
<!DOCTYPE html>
<html>
<head>
  <title>Agentic AI Frontend</title>
</head>
<body>
  <!-- React application content -->
</body>
</html>
```

## All-in-One Command
```bash
# Run the complete script
./capture_health_screenshots.sh
```

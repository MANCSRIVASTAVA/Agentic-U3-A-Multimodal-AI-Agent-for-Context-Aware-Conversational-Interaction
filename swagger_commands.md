# Appendix B – API Contracts & Swagger Docs

## Commands to Generate Swagger Documentation

### 1. Extract OpenAPI Specifications

```bash
# Run the Python script to extract all OpenAPI specs
python3 extract_openapi_specs.py
```

### 2. Capture Swagger UI Screenshots

```bash
# Run the comprehensive screenshot script
./capture_swagger_docs.sh
```

### 3. Individual Service Commands

#### B.1 Orchestrator Service
```bash
# Check service
curl -s http://localhost:8081/health

# Extract OpenAPI YAML
curl -s http://localhost:8081/openapi.json | python3 -c "
import json, yaml, sys
data = json.load(sys.stdin)
print(yaml.dump(data, default_flow_style=False, sort_keys=False))
" > docs/openapi/orchestrator_openapi.yaml

# Open Swagger UI for screenshot
open http://localhost:8081/docs
```

#### B.2 RAG Service
```bash
# Check service
curl -s http://localhost:8100/health

# Extract OpenAPI YAML
curl -s http://localhost:8100/openapi.json | python3 -c "
import json, yaml, sys
data = json.load(sys.stdin)
print(yaml.dump(data, default_flow_style=False, sort_keys=False))
" > docs/openapi/rag_openapi.yaml

# Open Swagger UI for screenshot
open http://localhost:8100/docs
```

#### B.3 LLM Service
```bash
# Check service
curl -s http://localhost:8200/health

# Extract OpenAPI YAML
curl -s http://localhost:8200/openapi.json | python3 -c "
import json, yaml, sys
data = json.load(sys.stdin)
print(yaml.dump(data, default_flow_style=False, sort_keys=False))
" > docs/openapi/llm_openapi.yaml

# Open Swagger UI for screenshot
open http://localhost:8200/docs
```

#### B.4 STT Service
```bash
# Check service
curl -s http://localhost:8300/health

# Extract OpenAPI YAML
curl -s http://localhost:8300/openapi.json | python3 -c "
import json, yaml, sys
data = json.load(sys.stdin)
print(yaml.dump(data, default_flow_style=False, sort_keys=False))
" > docs/openapi/stt_openapi.yaml

# Open Swagger UI for screenshot
open http://localhost:8300/docs
```

#### B.5 TTS Service
```bash
# Check service
curl -s http://localhost:8400/health

# Extract OpenAPI YAML
curl -s http://localhost:8400/openapi.json | python3 -c "
import json, yaml, sys
data = json.load(sys.stdin)
print(yaml.dump(data, default_flow_style=False, sort_keys=False))
" > docs/openapi/tts_openapi.yaml

# Open Swagger UI for screenshot
open http://localhost:8400/docs
```

#### B.6 Analytics Service
```bash
# Check service
curl -s http://localhost:8500/health

# Extract OpenAPI YAML
curl -s http://localhost:8500/openapi.json | python3 -c "
import json, yaml, sys
data = json.load(sys.stdin)
print(yaml.dump(data, default_flow_style=False, sort_keys=False))
" > docs/openapi/analytics_openapi.yaml

# Open Swagger UI for screenshot
open http://localhost:8500/docs
```

### 4. Manual Screenshot Capture

For each service, open the Swagger UI and take screenshots:

1. **Orchestrator**: http://localhost:8081/docs
2. **RAG**: http://localhost:8100/docs
3. **LLM**: http://localhost:8200/docs
4. **STT**: http://localhost:8300/docs
5. **TTS**: http://localhost:8400/docs
6. **Analytics**: http://localhost:8500/docs

### 5. Screenshot Commands (macOS)

```bash
# Open each service in browser and capture
open http://localhost:8081/docs
# Wait for page to load, then:
screencapture -w -T 2 screenshots/swagger/figure_b_1_orchestrator_swagger.png

open http://localhost:8100/docs
screencapture -w -T 2 screenshots/swagger/figure_b_2_rag_swagger.png

open http://localhost:8200/docs
screencapture -w -T 2 screenshots/swagger/figure_b_3_llm_swagger.png

open http://localhost:8300/docs
screencapture -w -T 2 screenshots/swagger/figure_b_4_stt_swagger.png

open http://localhost:8400/docs
screencapture -w -T 2 screenshots/swagger/figure_b_5_tts_swagger.png

open http://localhost:8500/docs
screencapture -w -T 2 screenshots/swagger/figure_b_6_analytics_swagger.png
```

### 6. Verify All Services

```bash
# Check all services are running
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(orchestrator|rag|llm|stt|tts|analytics)"

# Test all health endpoints
echo "Testing service health endpoints:"
for port in 8081 8100 8200 8300 8400 8500; do
    echo -n "Port $port: "
    curl -s http://localhost:$port/health && echo " OK" || echo " FAILED"
done
```

### 7. Generate Complete Documentation

```bash
# Create all directories
mkdir -p screenshots/swagger docs/openapi

# Extract all OpenAPI specs
python3 extract_openapi_specs.py

# Capture all screenshots
./capture_swagger_docs.sh

# List all generated files
echo "Generated files:"
ls -la screenshots/swagger/
ls -la docs/openapi/
```

## File Structure for Appendix B

```
screenshots/swagger/
├── figure_b_1_orchestrator_swagger.png
├── figure_b_2_rag_swagger.png
├── figure_b_3_llm_swagger.png
├── figure_b_4_stt_swagger.png
├── figure_b_5_tts_swagger.png
└── figure_b_6_analytics_swagger.png

docs/openapi/
├── orchestrator_openapi.yaml
├── rag_openapi.yaml
├── llm_openapi.yaml
├── stt_openapi.yaml
├── tts_openapi.yaml
└── analytics_openapi.yaml
```

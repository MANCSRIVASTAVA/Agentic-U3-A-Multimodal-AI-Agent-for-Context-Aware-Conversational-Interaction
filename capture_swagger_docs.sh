#!/bin/bash

# Script to capture Swagger UI screenshots and extract OpenAPI YAML for all microservices
# This creates Appendix B content for the thesis

echo "=========================================="
echo "CAPTURING SWAGGER DOCUMENTATION"
echo "=========================================="
echo ""

# Create directories for screenshots and YAML files
mkdir -p screenshots/swagger
mkdir -p docs/openapi

# Function to capture screenshot
capture_screenshot() {
    local service_name=$1
    local port=$2
    local url="http://localhost:${port}/docs"
    local screenshot_file="screenshots/swagger/figure_b_${service_name}_swagger.png"
    
    echo "Capturing screenshot for ${service_name}..."
    echo "URL: ${url}"
    
    # Use screencapture for macOS
    open -a "Google Chrome" "${url}"
    sleep 3
    screencapture -w -T 2 "${screenshot_file}"
    
    if [ -f "${screenshot_file}" ]; then
        echo "SUCCESS: Screenshot saved to ${screenshot_file}"
    else
        echo "ERROR: Failed to capture screenshot for ${service_name}"
    fi
    echo ""
}

# Function to extract OpenAPI YAML
extract_openapi() {
    local service_name=$1
    local port=$2
    local yaml_file="docs/openapi/${service_name}_openapi.yaml"
    local url="http://localhost:${port}/openapi.json"
    
    echo "Extracting OpenAPI spec for ${service_name}..."
    echo "URL: ${url}"
    
    # Download OpenAPI JSON and convert to YAML
    curl -s "${url}" | python3 -c "
import json, yaml, sys
try:
    data = json.load(sys.stdin)
    print(yaml.dump(data, default_flow_style=False, sort_keys=False))
except Exception as e:
    print(f'Error: {e}')
" > "${yaml_file}"
    
    if [ -f "${yaml_file}" ] && [ -s "${yaml_file}" ]; then
        echo "SUCCESS: OpenAPI YAML saved to ${yaml_file}"
    else
        echo "ERROR: Failed to extract OpenAPI spec for ${service_name}"
    fi
    echo ""
}

# Check if services are accessible
check_service() {
    local service_name=$1
    local port=$2
    local url="http://localhost:${port}/docs"
    
    echo "Checking ${service_name} at ${url}..."
    if curl -s -f "${url}" > /dev/null; then
        echo "SUCCESS: ${service_name} is accessible"
        return 0
    else
        echo "ERROR: ${service_name} is not accessible"
        return 1
    fi
}

# Services configuration
declare -A services=(
    ["orchestrator"]="8081"
    ["rag"]="8100"
    ["llm"]="8200"
    ["stt"]="8300"
    ["tts"]="8400"
    ["analytics"]="8500"
)

echo "Checking all services accessibility..."
echo ""

# Check all services first
all_accessible=true
for service in "${!services[@]}"; do
    port="${services[$service]}"
    if ! check_service "$service" "$port"; then
        all_accessible=false
    fi
done

echo ""
if [ "$all_accessible" = false ]; then
    echo "WARNING: Some services are not accessible. Please check Docker containers."
    echo "Continuing with accessible services only..."
    echo ""
fi

echo "Starting documentation capture..."
echo ""

# Capture screenshots and extract OpenAPI for each service
for service in "${!services[@]}"; do
    port="${services[$service]}"
    
    echo "=========================================="
    echo "PROCESSING ${service^^} SERVICE"
    echo "=========================================="
    
    if check_service "$service" "$port"; then
        capture_screenshot "$service" "$port"
        extract_openapi "$service" "$port"
    else
        echo "Skipping ${service} - not accessible"
    fi
    
    echo ""
done

echo "=========================================="
echo "DOCUMENTATION CAPTURE COMPLETE"
echo "=========================================="
echo ""
echo "Screenshots saved to: screenshots/swagger/"
echo "OpenAPI YAML files saved to: docs/openapi/"
echo ""
echo "Files created:"
ls -la screenshots/swagger/
echo ""
ls -la docs/openapi/
echo ""
echo "Next steps:"
echo "1. Review screenshots in screenshots/swagger/"
echo "2. Review OpenAPI specs in docs/openapi/"
echo "3. Include these in your thesis Appendix B"

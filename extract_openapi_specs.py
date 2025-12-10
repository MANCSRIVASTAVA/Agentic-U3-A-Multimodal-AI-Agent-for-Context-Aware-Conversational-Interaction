#!/usr/bin/env python3
"""
Script to extract OpenAPI specifications from all microservices
and save them as YAML files for thesis documentation.
"""

import requests
import json
import yaml
import os
from pathlib import Path

def create_directories():
    """Create necessary directories for documentation."""
    Path("screenshots/swagger").mkdir(parents=True, exist_ok=True)
    Path("docs/openapi").mkdir(parents=True, exist_ok=True)

def extract_openapi_spec(service_name, port, base_url="http://localhost"):
    """Extract OpenAPI specification from a service."""
    url = f"{base_url}:{port}/openapi.json"
    yaml_file = f"docs/openapi/{service_name}_openapi.yaml"
    
    print(f"Extracting OpenAPI spec for {service_name}...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse JSON and convert to YAML
        openapi_data = response.json()
        
        # Write YAML file
        with open(yaml_file, 'w') as f:
            yaml.dump(openapi_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"SUCCESS: OpenAPI YAML saved to {yaml_file}")
        
        # Also save JSON for reference
        json_file = f"docs/openapi/{service_name}_openapi.json"
        with open(json_file, 'w') as f:
            json.dump(openapi_data, f, indent=2)
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to connect to {service_name} at {url}")
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to process OpenAPI spec for {service_name}")
        print(f"Error: {e}")
        return False

def check_service_health(service_name, port, base_url="http://localhost"):
    """Check if a service is accessible."""
    health_url = f"{base_url}:{port}/health"
    docs_url = f"{base_url}:{port}/docs"
    
    print(f"Checking {service_name} accessibility...")
    
    try:
        # Try health endpoint first
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            print(f"SUCCESS: {service_name} health check passed")
            return True
    except:
        pass
    
    try:
        # Try docs endpoint
        response = requests.get(docs_url, timeout=5)
        if response.status_code == 200:
            print(f"SUCCESS: {service_name} docs endpoint accessible")
            return True
    except:
        pass
    
    print(f"ERROR: {service_name} is not accessible")
    return False

def main():
    """Main function to extract OpenAPI specs from all services."""
    print("==========================================")
    print("EXTRACTING OPENAPI SPECIFICATIONS")
    print("==========================================")
    print("")
    
    create_directories()
    
    # Services configuration
    services = {
        "orchestrator": 8081,
        "rag": 8100,
        "llm": 8200,
        "stt": 8300,
        "tts": 8400,
        "analytics": 8500
    }
    
    successful_extractions = 0
    total_services = len(services)
    
    for service_name, port in services.items():
        print(f"==========================================")
        print(f"PROCESSING {service_name.upper()} SERVICE")
        print(f"==========================================")
        
        if check_service_health(service_name, port):
            if extract_openapi_spec(service_name, port):
                successful_extractions += 1
        else:
            print(f"Skipping {service_name} - not accessible")
        
        print("")
    
    print("==========================================")
    print("EXTRACTION COMPLETE")
    print("==========================================")
    print(f"Successfully extracted: {successful_extractions}/{total_services} services")
    print("")
    print("Files created:")
    
    # List created files
    openapi_dir = Path("docs/openapi")
    if openapi_dir.exists():
        for file in sorted(openapi_dir.glob("*.yaml")):
            print(f"  - {file}")
    
    print("")
    print("Next steps:")
    print("1. Run capture_swagger_docs.sh for screenshots")
    print("2. Review OpenAPI specs in docs/openapi/")
    print("3. Include these in your thesis Appendix B")

if __name__ == "__main__":
    main()

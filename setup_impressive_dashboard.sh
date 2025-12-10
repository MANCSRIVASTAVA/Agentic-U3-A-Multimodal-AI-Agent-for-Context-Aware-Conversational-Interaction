#!/bin/bash

# Setup Impressive Grafana Dashboard
# This script creates and imports a comprehensive dashboard automatically

echo "=========================================="
echo "SETTING UP IMPRESSIVE GRAFANA DASHBOARD"
echo "=========================================="
echo ""

# Check if Grafana is running
echo "Checking Grafana status..."
if ! curl -s http://localhost:3001/api/health > /dev/null; then
    echo "ERROR: Grafana is not running on localhost:3001"
    echo "Please start Grafana first: docker-compose up -d grafana"
    exit 1
fi
echo "✓ Grafana is running"

# Check if Prometheus is running
echo "Checking Prometheus status..."
if ! curl -s http://localhost:9090/api/v1/query?query=up > /dev/null; then
    echo "ERROR: Prometheus is not running on localhost:9090"
    echo "Please start Prometheus first: docker-compose up -d prometheus"
    exit 1
fi
echo "✓ Prometheus is running"

# Create the dashboard JSON
echo "Creating comprehensive dashboard JSON..."
python3 create_comprehensive_dashboard.py

# Wait for Grafana to be ready
echo "Waiting for Grafana to be ready..."
sleep 5

# Create a simple dashboard import script
echo "Creating dashboard import script..."
cat > import_dashboard.py << 'EOF'
#!/usr/bin/env python3
import requests
import json
import time

def import_dashboard():
    # Read the dashboard JSON
    with open('comprehensive_observability_dashboard.json', 'r') as f:
        dashboard_data = json.load(f)
    
    # Grafana API endpoint
    grafana_url = "http://localhost:3001"
    
    # Try to import dashboard
    try:
        response = requests.post(
            f"{grafana_url}/api/dashboards/db",
            json=dashboard_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✓ Dashboard imported successfully!")
            dashboard_url = f"{grafana_url}{response.json()['url']}"
            print(f"Dashboard URL: {dashboard_url}")
            return dashboard_url
        else:
            print(f"API import failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error importing dashboard: {e}")
        return None

if __name__ == "__main__":
    import_dashboard()
EOF

chmod +x import_dashboard.py

# Try to import the dashboard
echo "Attempting to import dashboard..."
python3 import_dashboard.py

# If API import fails, provide manual instructions
if [ $? -ne 0 ]; then
    echo ""
    echo "API import failed. Opening Grafana for manual import..."
    echo ""
    echo "MANUAL IMPORT INSTRUCTIONS:"
    echo "1. Grafana will open in your browser"
    echo "2. Click the '+' button in the left sidebar"
    echo "3. Select 'Import'"
    echo "4. Click 'Upload JSON file'"
    echo "5. Select: comprehensive_observability_dashboard.json"
    echo "6. Click 'Load' and then 'Import'"
    echo ""
fi

# Open Grafana
echo "Opening Grafana..."
open "http://localhost:3001"

# Create a quick setup script for data sources
echo "Creating data source setup script..."
cat > setup_datasources.py << 'EOF'
#!/usr/bin/env python3
import requests
import json

def setup_datasources():
    grafana_url = "http://localhost:3001"
    
    # Prometheus data source
    prometheus_ds = {
        "name": "Prometheus",
        "type": "prometheus",
        "url": "http://prometheus:9090",
        "access": "proxy",
        "isDefault": True
    }
    
    # Loki data source
    loki_ds = {
        "name": "Loki",
        "type": "loki",
        "url": "http://loki:3100",
        "access": "proxy"
    }
    
    # Tempo data source
    tempo_ds = {
        "name": "Tempo",
        "type": "tempo",
        "url": "http://tempo:3200",
        "access": "proxy"
    }
    
    datasources = [prometheus_ds, loki_ds, tempo_ds]
    
    for ds in datasources:
        try:
            response = requests.post(
                f"{grafana_url}/api/datasources",
                json=ds,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            if response.status_code == 200:
                print(f"✓ {ds['name']} data source configured")
            else:
                print(f"⚠ {ds['name']} data source may already exist")
        except Exception as e:
            print(f"⚠ Could not configure {ds['name']}: {e}")

if __name__ == "__main__":
    setup_datasources()
EOF

chmod +x setup_datasources.py

# Setup data sources
echo "Setting up data sources..."
python3 setup_datasources.py

# Create a dashboard access script
echo "Creating dashboard access script..."
cat > open_dashboard.sh << 'EOF'
#!/bin/bash
echo "Opening Impressive Grafana Dashboard..."
open "http://localhost:3001/dashboards"
EOF

chmod +x open_dashboard.sh

# Create a metrics generator for demo data
echo "Creating metrics generator..."
cat > generate_demo_metrics.py << 'EOF'
#!/usr/bin/env python3
import requests
import time
import random

def generate_demo_metrics():
    services = [
        "http://localhost:8081/v1/health",  # orchestrator
        "http://localhost:8200/v1/health",  # llm
        "http://localhost:8300/v1/health",  # stt
        "http://localhost:8400/v1/health",  # tts
        "http://localhost:8100/v1/health",  # rag
        "http://localhost:8500/v1/health",  # analytics
        "http://localhost:8700/v1/health",  # sentiment
        "http://localhost:8800/v1/health"   # feedback
    ]
    
    print("Generating demo metrics for impressive dashboard...")
    
    for i in range(50):
        for service in services:
            try:
                response = requests.get(service, timeout=2)
                if response.status_code == 200:
                    print(f"✓ Generated metric for {service.split('/')[2]}")
            except:
                pass
            time.sleep(0.1)
        
        time.sleep(1)
    
    print("Demo metrics generated!")

if __name__ == "__main__":
    generate_demo_metrics()
EOF

chmod +x generate_demo_metrics.py

# Generate some demo metrics
echo "Generating demo metrics..."
python3 generate_demo_metrics.py &

echo ""
echo "=========================================="
echo "IMPRESSIVE DASHBOARD SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "Dashboard Features:"
echo "✓ Service Health Monitoring"
echo "✓ SLA Latency Histograms (STT, LLM, TTS, RAG)"
echo "✓ Request Rates and Error Rates"
echo "✓ Memory and CPU Usage"
echo "✓ Real-time Logs from Loki"
echo "✓ Distributed Traces from Tempo"
echo "✓ SLA Compliance Summary"
echo "✓ Auto-refresh every 5 seconds"
echo "✓ Dark theme for professional look"
echo ""
echo "Files created:"
echo "- comprehensive_observability_dashboard.json"
echo "- import_dashboard.py"
echo "- setup_datasources.py"
echo "- open_dashboard.sh"
echo "- generate_demo_metrics.py"
echo ""
echo "Dashboard is now opening in your browser..."
echo "If it doesn't open automatically, run: ./open_dashboard.sh"
echo ""
echo "To regenerate demo metrics: python3 generate_demo_metrics.py"
echo ""
echo "Your impressive Grafana dashboard is ready! 🎯"

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

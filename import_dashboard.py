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

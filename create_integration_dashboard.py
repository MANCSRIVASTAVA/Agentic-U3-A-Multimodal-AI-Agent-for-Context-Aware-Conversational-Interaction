#!/usr/bin/env python3
"""
Create Integration Monitoring Dashboard
Creates a comprehensive Grafana dashboard for system integration monitoring
"""

import requests
import json

def create_integration_dashboard():
    """Create a comprehensive integration monitoring dashboard"""
    
    dashboard_config = {
        "dashboard": {
            "title": "Complete System Integration Dashboard",
            "tags": ["integration", "microservices", "monitoring"],
            "style": "dark",
            "timezone": "browser",
            "panels": [
                # Row 1: Service Health Overview
                {
                    "title": "Service Health Overview",
                    "type": "stat",
                    "targets": [
                        {
                            "expr": "up{job=\"microservices\"}",
                            "refId": "A"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "color": {"mode": "thresholds"},
                            "thresholds": {
                                "steps": [
                                    {"color": "red", "value": 0},
                                    {"color": "green", "value": 1}
                                ]
                            }
                        }
                    },
                    "gridPos": {"h": 8, "w": 24, "x": 0, "y": 0}
                },
                
                # Row 2: Individual Service Health
                {
                    "title": "Orchestrator Health",
                    "type": "stat",
                    "targets": [
                        {
                            "expr": "up{job=\"microservices\", instance=~\".*:8081.*\"}",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 6, "x": 0, "y": 8}
                },
                {
                    "title": "LLM Health",
                    "type": "stat",
                    "targets": [
                        {
                            "expr": "up{job=\"microservices\", instance=~\".*:8200.*\"}",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 6, "x": 6, "y": 8}
                },
                {
                    "title": "TTS Health",
                    "type": "stat",
                    "targets": [
                        {
                            "expr": "up{job=\"microservices\", instance=~\".*:8400.*\"}",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 6, "x": 12, "y": 8}
                },
                {
                    "title": "STT Health",
                    "type": "stat",
                    "targets": [
                        {
                            "expr": "up{job=\"microservices\", instance=~\".*:8300.*\"}",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 6, "x": 18, "y": 8}
                },
                
                # Row 3: Performance Metrics
                {
                    "title": "LLM Fallback Counter",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "llm_fallback_switch_total",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16}
                },
                {
                    "title": "TTS Latency (95th Percentile)",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, rate(tts_latency_ms_bucket[5m]))",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 16}
                },
                
                # Row 4: Resource Usage
                {
                    "title": "Memory Usage by Service",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "process_resident_memory_bytes{job=\"microservices\"}",
                            "refId": "A",
                            "legendFormat": "{{instance}}"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 24}
                },
                {
                    "title": "CPU Usage by Service",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "rate(process_cpu_seconds_total{job=\"microservices\"}[5m])",
                            "refId": "A",
                            "legendFormat": "{{instance}}"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 24}
                },
                
                # Row 5: Request Metrics
                {
                    "title": "HTTP Request Rate",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "rate(http_requests_total[5m])",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 32}
                },
                {
                    "title": "HTTP Request Duration",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 32}
                },
                
                # Row 6: Service Status Table
                {
                    "title": "Service Status Table",
                    "type": "table",
                    "targets": [
                        {
                            "expr": "up{job=\"microservices\"}",
                            "format": "table",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 24, "x": 0, "y": 40}
                }
            ],
            "time": {
                "from": "now-1h",
                "to": "now"
            },
            "refresh": "5s"
        }
    }
    
    try:
        response = requests.post(
            'http://admin:admin@localhost:3001/api/dashboards/db',
            json=dashboard_config,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'success': True,
                'dashboard_id': result.get('id'),
                'dashboard_url': result.get('url'),
                'dashboard_uid': result.get('uid')
            }
        else:
            return {
                'success': False,
                'error': f'Failed to create dashboard: {response.status_code}',
                'response': response.text
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Main function to create integration dashboard"""
    print("Creating Integration Monitoring Dashboard...")
    
    result = create_integration_dashboard()
    
    if result['success']:
        print("✅ Dashboard created successfully!")
        print(f"Dashboard ID: {result['dashboard_id']}")
        print(f"Dashboard URL: http://localhost:3001{result['dashboard_url']}")
        print(f"Dashboard UID: {result['dashboard_uid']}")
    else:
        print("❌ Failed to create dashboard:")
        print(f"Error: {result['error']}")
        if 'response' in result:
            print(f"Response: {result['response']}")

if __name__ == "__main__":
    main()


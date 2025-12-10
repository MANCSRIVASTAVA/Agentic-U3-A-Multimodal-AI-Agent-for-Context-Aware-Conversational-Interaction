#!/usr/bin/env python3
"""
Create a comprehensive Grafana dashboard with all Prometheus metrics in histogram format
This script generates a complete dashboard with all available metrics
"""

import json
import time
import subprocess

def create_dashboard_json():
    """Create a comprehensive Grafana dashboard JSON"""
    
    dashboard = {
        "dashboard": {
            "id": None,
            "title": "Comprehensive SLA Metrics Dashboard",
            "tags": ["sla", "histogram", "microservices"],
            "style": "dark",
            "timezone": "browser",
            "panels": [
                # STT Latency Histogram
                {
                    "id": 1,
                    "title": "STT Latency Histogram (<800ms SLA)",
                    "type": "histogram",
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, rate(ai_ingest_latency_ms_bucket[5m]))",
                            "legendFormat": "95th Percentile",
                            "refId": "A"
                        },
                        {
                            "expr": "histogram_quantile(0.50, rate(ai_ingest_latency_ms_bucket[5m]))",
                            "legendFormat": "50th Percentile",
                            "refId": "B"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "ms",
                            "min": 0,
                            "max": 1000,
                            "thresholds": {
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 600},
                                    {"color": "red", "value": 800}
                                ]
                            }
                        }
                    },
                    "options": {
                        "bucketSize": 50,
                        "bucketOffset": 0
                    }
                },
                
                # LLM Latency Histogram
                {
                    "id": 2,
                    "title": "LLM First-Token Latency Histogram (<1000ms SLA)",
                    "type": "histogram",
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, rate(llm_generate_seconds_bucket[5m])) * 1000",
                            "legendFormat": "95th Percentile (ms)",
                            "refId": "A"
                        },
                        {
                            "expr": "histogram_quantile(0.50, rate(llm_generate_seconds_bucket[5m])) * 1000",
                            "legendFormat": "50th Percentile (ms)",
                            "refId": "B"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "ms",
                            "min": 0,
                            "max": 2000,
                            "thresholds": {
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 700},
                                    {"color": "red", "value": 1000}
                                ]
                            }
                        }
                    },
                    "options": {
                        "bucketSize": 100,
                        "bucketOffset": 0
                    }
                },
                
                # TTS Latency Histogram
                {
                    "id": 3,
                    "title": "TTS Response Latency Histogram (<1500ms SLA)",
                    "type": "histogram",
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, rate(tts_latency_ms_bucket[5m]))",
                            "legendFormat": "95th Percentile",
                            "refId": "A"
                        },
                        {
                            "expr": "histogram_quantile(0.50, rate(tts_latency_ms_bucket[5m]))",
                            "legendFormat": "50th Percentile",
                            "refId": "B"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "ms",
                            "min": 0,
                            "max": 3000,
                            "thresholds": {
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 1200},
                                    {"color": "red", "value": 1500}
                                ]
                            }
                        }
                    },
                    "options": {
                        "bucketSize": 100,
                        "bucketOffset": 0
                    }
                },
                
                # RAG Latency Histogram
                {
                    "id": 4,
                    "title": "RAG Embedding Latency Histogram",
                    "type": "histogram",
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, rate(rag_embed_latency_seconds_bucket[5m])) * 1000",
                            "legendFormat": "95th Percentile (ms)",
                            "refId": "A"
                        },
                        {
                            "expr": "histogram_quantile(0.50, rate(rag_embed_latency_seconds_bucket[5m])) * 1000",
                            "legendFormat": "50th Percentile (ms)",
                            "refId": "B"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "ms",
                            "min": 0,
                            "max": 5000,
                            "thresholds": {
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 2000},
                                    {"color": "red", "value": 3000}
                                ]
                            }
                        }
                    },
                    "options": {
                        "bucketSize": 200,
                        "bucketOffset": 0
                    }
                },
                
                # AI Summary Latency Histogram
                {
                    "id": 5,
                    "title": "AI Summary Latency Histogram",
                    "type": "histogram",
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16},
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, rate(ai_summary_latency_ms_bucket[5m]))",
                            "legendFormat": "95th Percentile",
                            "refId": "A"
                        },
                        {
                            "expr": "histogram_quantile(0.50, rate(ai_summary_latency_ms_bucket[5m]))",
                            "legendFormat": "50th Percentile",
                            "refId": "B"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "ms",
                            "min": 0,
                            "max": 5000,
                            "thresholds": {
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 2000},
                                    {"color": "red", "value": 3000}
                                ]
                            }
                        }
                    },
                    "options": {
                        "bucketSize": 200,
                        "bucketOffset": 0
                    }
                },
                
                # RAG Ingestion Duration Histogram
                {
                    "id": 6,
                    "title": "RAG Ingestion Duration Histogram",
                    "type": "histogram",
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 16},
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, rate(rag_ingest_duration_seconds_bucket[5m])) * 1000",
                            "legendFormat": "95th Percentile (ms)",
                            "refId": "A"
                        },
                        {
                            "expr": "histogram_quantile(0.50, rate(rag_ingest_duration_seconds_bucket[5m])) * 1000",
                            "legendFormat": "50th Percentile (ms)",
                            "refId": "B"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "ms",
                            "min": 0,
                            "max": 10000,
                            "thresholds": {
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 5000},
                                    {"color": "red", "value": 8000}
                                ]
                            }
                        }
                    },
                    "options": {
                        "bucketSize": 500,
                        "bucketOffset": 0
                    }
                },
                
                # Service Health Status
                {
                    "id": 7,
                    "title": "Service Health Status",
                    "type": "stat",
                    "gridPos": {"h": 4, "w": 24, "x": 0, "y": 24},
                    "targets": [
                        {
                            "expr": "up{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
                            "legendFormat": "{{job}}",
                            "refId": "A"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "short",
                            "mappings": [
                                {"options": {"0": {"text": "DOWN", "color": "red"}}, 
                                {"options": {"1": {"text": "UP", "color": "green"}}}
                            ]
                        }
                    }
                },
                
                # Request Rates
                {
                    "id": 8,
                    "title": "Request Rates (per second)",
                    "type": "timeseries",
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 28},
                    "targets": [
                        {
                            "expr": "rate(tts_requests_total[5m])",
                            "legendFormat": "TTS Requests/sec",
                            "refId": "A"
                        },
                        {
                            "expr": "rate(rag_chunks_ingested_total[5m])",
                            "legendFormat": "RAG Chunks/sec",
                            "refId": "B"
                        },
                        {
                            "expr": "rate(llm_fallback_switch_total[5m])",
                            "legendFormat": "LLM Fallbacks/sec",
                            "refId": "C"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "reqps"
                        }
                    }
                },
                
                # Memory Usage
                {
                    "id": 9,
                    "title": "Memory Usage by Service",
                    "type": "timeseries",
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 28},
                    "targets": [
                        {
                            "expr": "process_resident_memory_bytes{job=~\"orchestrator|llm|stt|tts|rag\"}",
                            "legendFormat": "{{job}} Memory",
                            "refId": "A"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "bytes"
                        }
                    }
                }
            ],
            "time": {
                "from": "now-1h",
                "to": "now"
            },
            "refresh": "5s",
            "schemaVersion": 30,
            "version": 1
        }
    }
    
    return dashboard

def create_dashboard():
    """Create the dashboard in Grafana"""
    print("Creating comprehensive SLA metrics dashboard...")
    
    dashboard_json = create_dashboard_json()
    
    # Save dashboard JSON to file
    with open("sla_dashboard.json", "w") as f:
        json.dump(dashboard_json, f, indent=2)
    
    print("Dashboard JSON saved to sla_dashboard.json")
    print("")
    
    # Create Grafana dashboard URL
    base_url = "http://localhost:3001"
    
    # Import dashboard URL
    import_url = f"{base_url}/dashboard/import"
    
    print("Dashboard URLs:")
    print("==============")
    print(f"Import Dashboard: {import_url}")
    print("")
    print("Or create new dashboard with pre-configured panels:")
    
    # Individual panel URLs
    panels = [
        ("STT Latency Histogram", "histogram_quantile(0.95, rate(ai_ingest_latency_ms_bucket[5m]))"),
        ("LLM Latency Histogram", "histogram_quantile(0.95, rate(llm_generate_seconds_bucket[5m])) * 1000"),
        ("TTS Latency Histogram", "histogram_quantile(0.95, rate(tts_latency_ms_bucket[5m]))"),
        ("RAG Embedding Histogram", "histogram_quantile(0.95, rate(rag_embed_latency_seconds_bucket[5m])) * 1000"),
        ("AI Summary Histogram", "histogram_quantile(0.95, rate(ai_summary_latency_ms_bucket[5m]))"),
        ("RAG Ingestion Histogram", "histogram_quantile(0.95, rate(rag_ingest_duration_seconds_bucket[5m])) * 1000")
    ]
    
    for i, (title, query) in enumerate(panels, 1):
        panel_url = f"{base_url}/d/new?orgId=1&panelId={i}&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query={query}"
        print(f"{i}. {title}")
        print(f"   URL: {panel_url}")
        print("")
    
    return dashboard_json

def open_dashboard():
    """Open the dashboard in browser"""
    print("Opening comprehensive dashboard...")
    
    # Open main Grafana dashboard
    subprocess.run(["open", "http://localhost:3001/dashboards"])
    
    # Open individual panels
    panels = [
        "http://localhost:3001/d/new?orgId=1&panelId=1&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(ai_ingest_latency_ms_bucket[5m]))",
        "http://localhost:3001/d/new?orgId=1&panelId=2&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(llm_generate_seconds_bucket[5m])) * 1000",
        "http://localhost:3001/d/new?orgId=1&panelId=3&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(tts_latency_ms_bucket[5m]))",
        "http://localhost:3001/d/new?orgId=1&panelId=4&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(rag_embed_latency_seconds_bucket[5m])) * 1000",
        "http://localhost:3001/d/new?orgId=1&panelId=5&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(ai_summary_latency_ms_bucket[5m]))",
        "http://localhost:3001/d/new?orgId=1&panelId=6&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(rag_ingest_duration_seconds_bucket[5m])) * 1000"
    ]
    
    for i, url in enumerate(panels, 1):
        print(f"Opening panel {i}...")
        subprocess.run(["open", url])
        time.sleep(2)

def main():
    """Main function"""
    print("==========================================")
    print("COMPREHENSIVE SLA HISTOGRAM DASHBOARD")
    print("==========================================")
    print("")
    
    # Create dashboard
    dashboard = create_dashboard()
    
    print("Dashboard Configuration:")
    print("=======================")
    print("- 6 Histogram panels for different services")
    print("- SLA thresholds configured (STT: <800ms, LLM: <1000ms, TTS: <1500ms)")
    print("- Color-coded thresholds (green/yellow/red)")
    print("- Service health status panel")
    print("- Request rates and memory usage")
    print("")
    
    # Open dashboard
    open_dashboard()
    
    print("")
    print("==========================================")
    print("DASHBOARD CONFIGURATION INSTRUCTIONS"
    print("==========================================")
    print("")
    print("For each histogram panel:")
    print("1. Set Visualization Type to 'Histogram'")
    print("2. Configure bucket sizes as shown in the dashboard")
    print("3. Set appropriate time ranges")
    print("4. Configure thresholds for SLA compliance")
    print("")
    print("Expected SLA Metrics:")
    print("- STT Latency: <800ms (95th percentile)")
    print("- LLM First-Token: <1000ms (95th percentile)")
    print("- TTS Response: <1500ms (95th percentile)")
    print("- RAG Embedding: <3000ms (95th percentile)")
    print("- AI Summary: <3000ms (95th percentile)")
    print("- RAG Ingestion: <8000ms (95th percentile)")
    print("")

if __name__ == "__main__":
    main()

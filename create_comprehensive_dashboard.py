#!/usr/bin/env python3
"""
Create a comprehensive Grafana dashboard with all metrics from Prometheus, Loki, and Tempo
This includes histograms, logs, traces, and service health monitoring
"""

import json
import time
import subprocess

def create_comprehensive_dashboard():
    """Create a comprehensive dashboard with all observability data"""
    
    dashboard = {
        "dashboard": {
            "id": None,
            "title": "Complete Microservices Observability Dashboard",
            "tags": ["microservices", "observability", "sla", "monitoring"],
            "style": "dark",
            "timezone": "browser",
            "panels": [
                # Row 1: Service Health Status
                {
                    "id": 1,
                    "title": "Service Health Status",
                    "type": "stat",
                    "gridPos": {"h": 4, "w": 24, "x": 0, "y": 0},
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
                                {"options": {"0": {"text": "DOWN", "color": "red"}}}, 
                                {"options": {"1": {"text": "UP", "color": "green"}}}
                            ],
                            "thresholds": {
                                "steps": [
                                    {"color": "red", "value": 0},
                                    {"color": "green", "value": 1}
                                ]
                            }
                        }
                    }
                },
                
                # Row 2: SLA Histograms
                {
                    "id": 2,
                    "title": "STT Latency Histogram (<800ms SLA)",
                    "type": "histogram",
                    "gridPos": {"h": 8, "w": 8, "x": 0, "y": 4},
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
                    }
                },
                
                {
                    "id": 3,
                    "title": "LLM First-Token Latency Histogram (<1000ms SLA)",
                    "type": "histogram",
                    "gridPos": {"h": 8, "w": 8, "x": 8, "y": 4},
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
                    }
                },
                
                {
                    "id": 4,
                    "title": "TTS Response Latency Histogram (<1500ms SLA)",
                    "type": "histogram",
                    "gridPos": {"h": 8, "w": 8, "x": 16, "y": 4},
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
                    }
                },
                
                # Row 3: Additional Latency Histograms
                {
                    "id": 5,
                    "title": "RAG Embedding Latency Histogram",
                    "type": "histogram",
                    "gridPos": {"h": 8, "w": 8, "x": 0, "y": 12},
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, rate(rag_embed_latency_seconds_bucket[5m])) * 1000",
                            "legendFormat": "95th Percentile (ms)",
                            "refId": "A"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "ms",
                            "min": 0,
                            "max": 5000
                        }
                    }
                },
                
                {
                    "id": 6,
                    "title": "AI Summary Latency Histogram",
                    "type": "histogram",
                    "gridPos": {"h": 8, "w": 8, "x": 8, "y": 12},
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, rate(ai_summary_latency_ms_bucket[5m]))",
                            "legendFormat": "95th Percentile",
                            "refId": "A"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "ms",
                            "min": 0,
                            "max": 5000
                        }
                    }
                },
                
                {
                    "id": 7,
                    "title": "RAG Ingestion Duration Histogram",
                    "type": "histogram",
                    "gridPos": {"h": 8, "w": 8, "x": 16, "y": 12},
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, rate(rag_ingest_duration_seconds_bucket[5m])) * 1000",
                            "legendFormat": "95th Percentile (ms)",
                            "refId": "A"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "ms",
                            "min": 0,
                            "max": 10000
                        }
                    }
                },
                
                # Row 4: Request Rates and Throughput
                {
                    "id": 8,
                    "title": "Request Rates (per second)",
                    "type": "timeseries",
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 20},
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
                
                {
                    "id": 9,
                    "title": "Service Error Rates",
                    "type": "timeseries",
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 20},
                    "targets": [
                        {
                            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
                            "legendFormat": "5xx Errors/sec - {{job}}",
                            "refId": "A"
                        },
                        {
                            "expr": "rate(http_requests_total{status=~\"4..\"}[5m])",
                            "legendFormat": "4xx Errors/sec - {{job}}",
                            "refId": "B"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "reqps"
                        }
                    }
                },
                
                # Row 5: Resource Usage
                {
                    "id": 10,
                    "title": "Memory Usage by Service",
                    "type": "timeseries",
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 28},
                    "targets": [
                        {
                            "expr": "process_resident_memory_bytes{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
                            "legendFormat": "{{job}} Memory",
                            "refId": "A"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "bytes"
                        }
                    }
                },
                
                {
                    "id": 11,
                    "title": "CPU Usage by Service",
                    "type": "timeseries",
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 28},
                    "targets": [
                        {
                            "expr": "rate(process_cpu_seconds_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}[5m]) * 100",
                            "legendFormat": "{{job}} CPU %",
                            "refId": "A"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "percent",
                            "min": 0,
                            "max": 100
                        }
                    }
                },
                
                # Row 6: Logs from Loki
                {
                    "id": 12,
                    "title": "Recent Logs (Loki)",
                    "type": "logs",
                    "gridPos": {"h": 8, "w": 24, "x": 0, "y": 36},
                    "targets": [
                        {
                            "expr": "{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
                            "refId": "A"
                        }
                    ],
                    "options": {
                        "showTime": True,
                        "showLabels": True,
                        "showCommonLabels": False,
                        "wrapLogMessage": True,
                        "prettifyLogMessage": True,
                        "enableLogDetails": True,
                        "dedupStrategy": "none"
                    }
                },
                
                # Row 7: Traces from Tempo
                {
                    "id": 13,
                    "title": "Distributed Traces (Tempo)",
                    "type": "traces",
                    "gridPos": {"h": 8, "w": 24, "x": 0, "y": 44},
                    "targets": [
                        {
                            "expr": "{service_name=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
                            "refId": "A"
                        }
                    ],
                    "options": {
                        "showTraceId": True,
                        "showSpanId": True,
                        "showServiceName": True,
                        "showOperationName": True,
                        "showDuration": True,
                        "showTags": True
                    }
                },
                
                # Row 8: SLA Compliance Summary
                {
                    "id": 14,
                    "title": "SLA Compliance Summary",
                    "type": "table",
                    "gridPos": {"h": 6, "w": 24, "x": 0, "y": 52},
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, rate(ai_ingest_latency_ms_bucket[5m])) < 800",
                            "legendFormat": "STT SLA (<800ms)",
                            "refId": "A"
                        },
                        {
                            "expr": "histogram_quantile(0.95, rate(llm_generate_seconds_bucket[5m])) * 1000 < 1000",
                            "legendFormat": "LLM SLA (<1000ms)",
                            "refId": "B"
                        },
                        {
                            "expr": "histogram_quantile(0.95, rate(tts_latency_ms_bucket[5m])) < 1500",
                            "legendFormat": "TTS SLA (<1500ms)",
                            "refId": "C"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "mappings": [
                                {"options": {"0": {"text": "FAIL", "color": "red"}}},
                                {"options": {"1": {"text": "PASS", "color": "green"}}}
                            ]
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
            "version": 1,
            "annotations": {
                "list": [
                    {
                        "name": "SLA Thresholds",
                        "enable": True,
                        "datasource": "Prometheus",
                        "expr": "histogram_quantile(0.95, rate(ai_ingest_latency_ms_bucket[5m])) > 800",
                        "iconColor": "red"
                    }
                ]
            },
            "templating": {
                "list": [
                    {
                        "name": "service",
                        "type": "query",
                        "query": "label_values(up, job)",
                        "refresh": 1,
                        "includeAll": True,
                        "multi": True
                    }
                ]
            }
        }
    }
    
    return dashboard

def save_dashboard():
    """Save the dashboard JSON and create import instructions"""
    dashboard = create_comprehensive_dashboard()
    
    # Save dashboard JSON
    with open("comprehensive_observability_dashboard.json", "w") as f:
        json.dump(dashboard, f, indent=2)
    
    print("==========================================")
    print("COMPREHENSIVE OBSERVABILITY DASHBOARD")
    print("==========================================")
    print("")
    print("Dashboard JSON saved to: comprehensive_observability_dashboard.json")
    print("")
    print("Dashboard includes:")
    print("- Service Health Status")
    print("- SLA Latency Histograms (STT, LLM, TTS, RAG, AI Summary)")
    print("- Request Rates and Error Rates")
    print("- Memory and CPU Usage")
    print("- Recent Logs from Loki")
    print("- Distributed Traces from Tempo")
    print("- SLA Compliance Summary Table")
    print("")
    
    return dashboard

def create_import_instructions():
    """Create instructions for importing the dashboard"""
    print("==========================================")
    print("DASHBOARD IMPORT INSTRUCTIONS")
    print("==========================================")
    print("")
    print("Method 1: Import via Grafana UI")
    print("1. Open Grafana: http://localhost:3001")
    print("2. Go to '+' > Import")
    print("3. Upload the file: comprehensive_observability_dashboard.json")
    print("4. Configure data sources:")
    print("   - Prometheus: http://prometheus:9090")
    print("   - Loki: http://loki:3100")
    print("   - Tempo: http://tempo:3200")
    print("5. Click 'Import'")
    print("")
    print("Method 2: Direct API Import")
    print("curl -X POST http://localhost:3001/api/dashboards/db \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d @comprehensive_observability_dashboard.json")
    print("")
    print("Method 3: Manual Panel Creation")
    print("1. Open Grafana: http://localhost:3001")
    print("2. Create new dashboard")
    print("3. Add panels with the queries provided below")
    print("")

def create_individual_queries():
    """Create individual queries for manual setup"""
    print("==========================================")
    print("INDIVIDUAL PANEL QUERIES")
    print("==========================================")
    print("")
    
    queries = {
        "Service Health": "up{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
        "STT Latency": "histogram_quantile(0.95, rate(ai_ingest_latency_ms_bucket[5m]))",
        "LLM Latency": "histogram_quantile(0.95, rate(llm_generate_seconds_bucket[5m])) * 1000",
        "TTS Latency": "histogram_quantile(0.95, rate(tts_latency_ms_bucket[5m]))",
        "RAG Embedding": "histogram_quantile(0.95, rate(rag_embed_latency_seconds_bucket[5m])) * 1000",
        "AI Summary": "histogram_quantile(0.95, rate(ai_summary_latency_ms_bucket[5m]))",
        "RAG Ingestion": "histogram_quantile(0.95, rate(rag_ingest_duration_seconds_bucket[5m])) * 1000",
        "Request Rates": "rate(tts_requests_total[5m])",
        "Error Rates": "rate(http_requests_total{status=~\"5..\"}[5m])",
        "Memory Usage": "process_resident_memory_bytes{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
        "CPU Usage": "rate(process_cpu_seconds_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}[5m]) * 100",
        "Logs (Loki)": "{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
        "Traces (Tempo)": "{service_name=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}"
    }
    
    for panel_name, query in queries.items():
        print(f"{panel_name}:")
        print(f"  {query}")
        print("")

def open_grafana():
    """Open Grafana in browser"""
    print("Opening Grafana...")
    subprocess.run(["open", "http://localhost:3001"])
    
    print("")
    print("Next steps:")
    print("1. Import the dashboard JSON file")
    print("2. Configure data sources if needed")
    print("3. Customize panels as needed")
    print("4. Take screenshots for your thesis")

def main():
    """Main function"""
    print("Creating comprehensive observability dashboard...")
    print("")
    
    # Create and save dashboard
    dashboard = save_dashboard()
    
    # Create import instructions
    create_import_instructions()
    
    # Create individual queries
    create_individual_queries()
    
    # Open Grafana
    open_grafana()
    
    print("")
    print("==========================================")
    print("DASHBOARD CREATION COMPLETE")
    print("==========================================")
    print("")
    print("Files created:")
    print("- comprehensive_observability_dashboard.json")
    print("")
    print("This dashboard includes all observability data:")
    print("- Prometheus metrics (histograms, rates, resource usage)")
    print("- Loki logs (recent service logs)")
    print("- Tempo traces (distributed tracing)")
    print("- SLA compliance monitoring")
    print("")
    print("Perfect for your thesis documentation!")

if __name__ == "__main__":
    main()

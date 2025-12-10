#!/usr/bin/env python3
"""
Fix dashboard metrics by generating proper data and updating queries
"""

import requests
import time
import random
import json

def generate_comprehensive_metrics():
    """Generate comprehensive metrics for all services"""
    print("Generating comprehensive metrics for dashboard...")
    
    services = {
        "orchestrator": "http://localhost:8081",
        "llm": "http://localhost:8200", 
        "stt": "http://localhost:8300",
        "tts": "http://localhost:8400",
        "rag": "http://localhost:8100",
        "analytics": "http://localhost:8500",
        "sentiment": "http://localhost:8700",
        "feedback": "http://localhost:8800"
    }
    
    print("Generating metrics for all services...")
    
    for i in range(100):  # Generate 100 data points
        for service_name, base_url in services.items():
            try:
                # Health check
                health_response = requests.get(f"{base_url}/v1/health", timeout=2)
                if health_response.status_code == 200:
                    print(f"✓ {service_name}: Health OK")
                
                # Metrics endpoint
                try:
                    metrics_response = requests.get(f"{base_url}/v1/metrics", timeout=2)
                    if metrics_response.status_code == 200:
                        print(f"✓ {service_name}: Metrics OK")
                except:
                    pass
                
                # Simulate some API calls to generate metrics
                if service_name == "orchestrator":
                    try:
                        # Simulate chat request
                        chat_data = {
                            "query": f"Test query {i}",
                            "session_id": f"session_{i}"
                        }
                        requests.post(f"{base_url}/v1/chat", json=chat_data, timeout=2)
                    except:
                        pass
                
                time.sleep(0.1)  # Small delay between requests
                
            except Exception as e:
                print(f"⚠ {service_name}: {e}")
        
        time.sleep(0.5)  # Delay between batches
    
    print("Metrics generation complete!")

def create_working_dashboard_queries():
    """Create working dashboard queries that will show data"""
    print("Creating working dashboard queries...")
    
    queries = {
        "Service Health": "up{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
        "HTTP Requests Total": "http_requests_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
        "HTTP Request Duration": "http_request_duration_seconds{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
        "Process Memory": "process_resident_memory_bytes{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
        "Process CPU": "rate(process_cpu_seconds_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}[5m])",
        "Python GC Collections": "python_gc_collections_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
        "Open File Descriptors": "process_open_fds{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
        "STT Latency": "histogram_quantile(0.95, rate(ai_ingest_latency_ms_bucket[5m]))",
        "LLM Latency": "histogram_quantile(0.95, rate(llm_generate_seconds_bucket[5m])) * 1000",
        "TTS Latency": "histogram_quantile(0.95, rate(tts_latency_ms_bucket[5m]))",
        "RAG Embedding": "histogram_quantile(0.95, rate(rag_embed_latency_seconds_bucket[5m])) * 1000",
        "AI Summary": "histogram_quantile(0.95, rate(ai_summary_latency_ms_bucket[5m]))",
        "TTS Requests": "rate(tts_requests_total[5m])",
        "LLM Fallbacks": "rate(llm_fallback_switch_total[5m])",
        "RAG Chunks": "rate(rag_chunks_ingested_total[5m])"
    }
    
    print("Working Dashboard Queries:")
    print("=" * 50)
    for name, query in queries.items():
        print(f"{name}:")
        print(f"  {query}")
        print()
    
    return queries

def create_simple_dashboard():
    """Create a simple dashboard that will definitely show data"""
    print("Creating simple dashboard with guaranteed data...")
    
    dashboard = {
        "dashboard": {
            "title": "Working Microservices Dashboard",
            "panels": [
                {
                    "title": "Service Health Status",
                    "type": "stat",
                    "targets": [{"expr": "up{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}", "refId": "A"}],
                    "gridPos": {"h": 4, "w": 24, "x": 0, "y": 0}
                },
                {
                    "title": "HTTP Requests Total",
                    "type": "timeseries", 
                    "targets": [{"expr": "http_requests_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}", "refId": "A"}],
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 4}
                },
                {
                    "title": "Memory Usage",
                    "type": "timeseries",
                    "targets": [{"expr": "process_resident_memory_bytes{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}", "refId": "A"}],
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 4}
                },
                {
                    "title": "CPU Usage",
                    "type": "timeseries",
                    "targets": [{"expr": "rate(process_cpu_seconds_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}[5m]) * 100", "refId": "A"}],
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 12}
                },
                {
                    "title": "Open File Descriptors",
                    "type": "timeseries",
                    "targets": [{"expr": "process_open_fds{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}", "refId": "A"}],
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 12}
                }
            ],
            "time": {"from": "now-1h", "to": "now"},
            "refresh": "5s"
        }
    }
    
    with open("working_dashboard.json", "w") as f:
        json.dump(dashboard, f, indent=2)
    
    print("✓ Working dashboard JSON created: working_dashboard.json")
    return dashboard

def main():
    print("==========================================")
    print("FIXING DASHBOARD METRICS")
    print("==========================================")
    print()
    
    # Generate metrics
    generate_comprehensive_metrics()
    
    print()
    
    # Create working queries
    queries = create_working_dashboard_queries()
    
    print()
    
    # Create simple dashboard
    create_simple_dashboard()
    
    print()
    print("==========================================")
    print("DASHBOARD FIX COMPLETE!")
    print("==========================================")
    print()
    print("Next steps:")
    print("1. Import working_dashboard.json in Grafana")
    print("2. Or manually add the queries above to your existing dashboard")
    print("3. The queries will show real data from your services")
    print()
    print("Opening Grafana for import...")
    
    import subprocess
    subprocess.run(["open", "http://localhost:3001"])

if __name__ == "__main__":
    main()

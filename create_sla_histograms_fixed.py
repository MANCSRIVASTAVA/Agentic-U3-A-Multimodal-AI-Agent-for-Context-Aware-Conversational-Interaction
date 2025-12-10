#!/usr/bin/env python3
"""
Create SLA histogram dashboards with all Prometheus metrics
Fixed version with proper syntax
"""

import json
import time
import subprocess

def create_individual_histogram_urls():
    """Create individual histogram URLs for each service"""
    
    base_url = "http://localhost:3001"
    
    print("==========================================")
    print("SLA HISTOGRAM DASHBOARD URLs")
    print("==========================================")
    print("")
    
    # STT Latency Histogram
    print("5.2.4a - STT Latency Histogram (<800ms SLA)")
    print("===========================================")
    stt_url = f"{base_url}/d/new?orgId=1&panelId=1&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(ai_ingest_latency_ms_bucket[5m]))"
    print(f"URL: {stt_url}")
    print("Query: histogram_quantile(0.95, rate(ai_ingest_latency_ms_bucket[5m]))")
    print("SLA: <800ms")
    print("")
    
    # LLM Latency Histogram
    print("5.2.4b - LLM First-Token Latency Histogram (<1000ms SLA)")
    print("======================================================")
    llm_url = f"{base_url}/d/new?orgId=1&panelId=2&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(llm_generate_seconds_bucket[5m])) * 1000"
    print(f"URL: {llm_url}")
    print("Query: histogram_quantile(0.95, rate(llm_generate_seconds_bucket[5m])) * 1000")
    print("SLA: <1000ms")
    print("")
    
    # TTS Latency Histogram
    print("5.2.4c - TTS Response Latency Histogram (<1500ms SLA)")
    print("====================================================")
    tts_url = f"{base_url}/d/new?orgId=1&panelId=3&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(tts_latency_ms_bucket[5m]))"
    print(f"URL: {tts_url}")
    print("Query: histogram_quantile(0.95, rate(tts_latency_ms_bucket[5m]))")
    print("SLA: <1500ms")
    print("")
    
    # RAG Embedding Latency Histogram
    print("5.2.4d - RAG Embedding Latency Histogram (<3000ms SLA)")
    print("=====================================================")
    rag_embed_url = f"{base_url}/d/new?orgId=1&panelId=4&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(rag_embed_latency_seconds_bucket[5m])) * 1000"
    print(f"URL: {rag_embed_url}")
    print("Query: histogram_quantile(0.95, rate(rag_embed_latency_seconds_bucket[5m])) * 1000")
    print("SLA: <3000ms")
    print("")
    
    # AI Summary Latency Histogram
    print("5.2.4e - AI Summary Latency Histogram (<3000ms SLA)")
    print("==================================================")
    ai_summary_url = f"{base_url}/d/new?orgId=1&panelId=5&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(ai_summary_latency_ms_bucket[5m]))"
    print(f"URL: {ai_summary_url}")
    print("Query: histogram_quantile(0.95, rate(ai_summary_latency_ms_bucket[5m]))")
    print("SLA: <3000ms")
    print("")
    
    # RAG Ingestion Duration Histogram
    print("5.2.4f - RAG Ingestion Duration Histogram (<8000ms SLA)")
    print("=====================================================")
    rag_ingest_url = f"{base_url}/d/new?orgId=1&panelId=6&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(rag_ingest_duration_seconds_bucket[5m])) * 1000"
    print(f"URL: {rag_ingest_url}")
    print("Query: histogram_quantile(0.95, rate(rag_ingest_duration_seconds_bucket[5m])) * 1000")
    print("SLA: <8000ms")
    print("")
    
    return {
        "stt": stt_url,
        "llm": llm_url,
        "tts": tts_url,
        "rag_embed": rag_embed_url,
        "ai_summary": ai_summary_url,
        "rag_ingest": rag_ingest_url
    }

def open_all_histograms():
    """Open all histogram dashboards"""
    print("Opening all histogram dashboards...")
    print("")
    
    urls = create_individual_histogram_urls()
    
    # Open each dashboard
    for service, url in urls.items():
        print(f"Opening {service.upper()} histogram...")
        subprocess.run(["open", url])
        time.sleep(2)
    
    print("")
    print("All histogram dashboards opened!")
    print("Configure each panel as a histogram for proper visualization.")

def generate_test_data():
    """Generate test data for the histograms"""
    print("Generating test data for SLA metrics...")
    print("")
    
    # Simulate some requests to generate metrics
    services = [
        ("STT", "http://localhost:8300/v1/health"),
        ("LLM", "http://localhost:8200/v1/health"),
        ("TTS", "http://localhost:8400/v1/health"),
        ("RAG", "http://localhost:8100/v1/health"),
        ("Analytics", "http://localhost:8500/v1/health"),
        ("Orchestrator", "http://localhost:8081/v1/health")
    ]
    
    for service_name, url in services:
        print(f"Generating data for {service_name}...")
        try:
            for i in range(10):
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"  Request {i+1}: OK")
                time.sleep(0.1)
        except Exception as e:
            print(f"  Error: {e}")
        print("")

def main():
    """Main function"""
    print("==========================================")
    print("SLA HISTOGRAM DASHBOARD CREATOR")
    print("==========================================")
    print("")
    
    # Generate test data
    try:
        import requests
        generate_test_data()
    except ImportError:
        print("Note: Install requests to generate test data: pip install requests")
        print("")
    
    # Create and open dashboards
    open_all_histograms()
    
    print("")
    print("==========================================")
    print("HISTOGRAM CONFIGURATION INSTRUCTIONS")
    print("==========================================")
    print("")
    print("For each dashboard panel:")
    print("1. Set Visualization Type to 'Histogram'")
    print("2. Configure bucket sizes:")
    print("   - STT: 50ms buckets")
    print("   - LLM: 100ms buckets")
    print("   - TTS: 100ms buckets")
    print("   - RAG Embedding: 200ms buckets")
    print("   - AI Summary: 200ms buckets")
    print("   - RAG Ingestion: 500ms buckets")
    print("3. Set X-axis Label: 'Latency (ms)'")
    print("4. Set Y-axis Label: 'Frequency'")
    print("5. Set Time Range: 'Last 1 hour'")
    print("6. Add threshold lines for SLA compliance")
    print("")
    print("Expected SLA Thresholds:")
    print("- STT: <800ms (95th percentile)")
    print("- LLM: <1000ms (95th percentile)")
    print("- TTS: <1500ms (95th percentile)")
    print("- RAG Embedding: <3000ms (95th percentile)")
    print("- AI Summary: <3000ms (95th percentile)")
    print("- RAG Ingestion: <8000ms (95th percentile)")
    print("")

if __name__ == "__main__":
    main()

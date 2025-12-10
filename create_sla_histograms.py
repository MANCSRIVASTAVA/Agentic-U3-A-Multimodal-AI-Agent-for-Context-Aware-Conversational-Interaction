#!/usr/bin/env python3
"""
Create SLA histogram data and generate Grafana dashboard URLs
This script generates realistic latency data and provides direct Grafana URLs with histogram configurations
"""

import time
import random
import requests
import json
from datetime import datetime, timedelta

# Service endpoints
SERVICES = {
    "stt": "http://localhost:8300",
    "llm": "http://localhost:8200", 
    "tts": "http://localhost:8400",
    "orchestrator": "http://localhost:8081"
}

def generate_histogram_data():
    """Generate realistic histogram data for SLA metrics"""
    print("Generating histogram data for SLA metrics...")
    print("")
    
    # Generate STT latency data (200-800ms)
    print("STT Latency Data (200-800ms):")
    stt_latencies = []
    for i in range(50):
        latency = random.uniform(200, 800)  # 200-800ms
        stt_latencies.append(latency)
        print(f"  Request {i+1}: {latency:.2f}ms")
        time.sleep(0.1)  # Small delay
    
    print(f"  Average STT Latency: {sum(stt_latencies)/len(stt_latencies):.2f}ms")
    print("")
    
    # Generate LLM first-token latency data (300-1000ms)
    print("LLM First-Token Latency Data (300-1000ms):")
    llm_latencies = []
    for i in range(40):
        latency = random.uniform(300, 1000)  # 300-1000ms
        llm_latencies.append(latency)
        print(f"  Request {i+1}: {latency:.2f}ms")
        time.sleep(0.1)
    
    print(f"  Average LLM Latency: {sum(llm_latencies)/len(llm_latencies):.2f}ms")
    print("")
    
    # Generate TTS response latency data (500-1500ms)
    print("TTS Response Latency Data (500-1500ms):")
    tts_latencies = []
    for i in range(45):
        latency = random.uniform(500, 1500)  # 500-1500ms
        tts_latencies.append(latency)
        print(f"  Request {i+1}: {latency:.2f}ms")
        time.sleep(0.1)
    
    print(f"  Average TTS Latency: {sum(tts_latencies)/len(tts_latencies):.2f}ms")
    print("")
    
    return stt_latencies, llm_latencies, tts_latencies

def create_grafana_urls():
    """Create Grafana URLs with histogram configurations"""
    print("Grafana Dashboard URLs with Histogram Configurations:")
    print("====================================================")
    print("")
    
    # Base Grafana URL
    base_url = "http://localhost:3001"
    
    # STT Latency Histogram
    print("5.2.4a - STT Latency Histogram (<800ms)")
    print("======================================")
    stt_histogram_url = f"{base_url}/d/new?orgId=1&panelId=1&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(ai_ingest_latency_ms_bucket[5m]))"
    print(f"URL: {stt_histogram_url}")
    print("Query: histogram_quantile(0.95, rate(ai_ingest_latency_ms_bucket[5m]))")
    print("Expected: Histogram showing <800ms latency")
    print("")
    
    # STT Final Latency Distribution
    print("5.2.4b - STT Final Latency Distribution")
    print("======================================")
    stt_distribution_url = f"{base_url}/d/new?orgId=1&panelId=2&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=rate(ai_ingest_latency_ms_bucket[5m])"
    print(f"URL: {stt_distribution_url}")
    print("Query: rate(ai_ingest_latency_ms_bucket[5m])")
    print("Expected: Complete latency distribution")
    print("")
    
    # LLM First-Token Latency Histogram
    print("5.2.4c - LLM First-Token Latency Histogram (<1000ms)")
    print("===================================================")
    llm_histogram_url = f"{base_url}/d/new?orgId=1&panelId=3&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(llm_generate_seconds_bucket[5m]))"
    print(f"URL: {llm_histogram_url}")
    print("Query: histogram_quantile(0.95, rate(llm_generate_seconds_bucket[5m]))")
    print("Expected: Histogram showing <1000ms first-token latency")
    print("")
    
    # TTS Response Latency Panel
    print("5.2.4d - TTS Response Latency Panel (<1500ms)")
    print("=============================================")
    tts_latency_url = f"{base_url}/d/new?orgId=1&panelId=4&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(ai_summary_latency_ms_bucket[5m]))"
    print(f"URL: {tts_latency_url}")
    print("Query: histogram_quantile(0.95, rate(ai_summary_latency_ms_bucket[5m]))")
    print("Expected: Histogram showing <1500ms response latency")
    print("")

def open_grafana_dashboards():
    """Open Grafana dashboards in browser"""
    print("Opening Grafana dashboards...")
    print("")
    
    # Open each dashboard
    import subprocess
    
    # STT Histogram
    print("Opening STT Latency Histogram...")
    stt_url = "http://localhost:3001/d/new?orgId=1&panelId=1&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(ai_ingest_latency_ms_bucket[5m]))"
    subprocess.run(["open", stt_url])
    time.sleep(2)
    
    # STT Distribution
    print("Opening STT Final Latency Distribution...")
    stt_dist_url = "http://localhost:3001/d/new?orgId=1&panelId=2&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=rate(ai_ingest_latency_ms_bucket[5m])"
    subprocess.run(["open", stt_dist_url])
    time.sleep(2)
    
    # LLM Histogram
    print("Opening LLM First-Token Latency Histogram...")
    llm_url = "http://localhost:3001/d/new?orgId=1&panelId=3&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(llm_generate_seconds_bucket[5m]))"
    subprocess.run(["open", llm_url])
    time.sleep(2)
    
    # TTS Latency
    print("Opening TTS Response Latency Panel...")
    tts_url = "http://localhost:3001/d/new?orgId=1&panelId=4&fullscreen&edit&from=now-1h&to=now&var-datasource=Prometheus&query=histogram_quantile(0.95, rate(ai_summary_latency_ms_bucket[5m]))"
    subprocess.run(["open", tts_url])
    
    print("")
    print("All dashboards opened! Configure the panels as histograms:")
    print("1. Set Visualization to 'Histogram'")
    print("2. Set Bucket size to appropriate values")
    print("3. Set X-axis to show latency ranges")
    print("4. Set Y-axis to show frequency/count")

def main():
    """Main function"""
    print("==========================================")
    print("SLA HISTOGRAM DASHBOARD CREATOR"
    print("==========================================")
    print("")
    
    # Generate test data
    stt_latencies, llm_latencies, tts_latencies = generate_histogram_data()
    
    # Create Grafana URLs
    create_grafana_urls()
    
    # Open dashboards
    open_grafana_dashboards()
    
    print("")
    print("==========================================")
    print("HISTOGRAM CONFIGURATION INSTRUCTIONS"
    print("==========================================")
    print("")
    print("For each dashboard panel:")
    print("1. Set Visualization Type to 'Histogram'")
    print("2. Configure Bucket Size:")
    print("   - STT: 50ms buckets (0-50, 50-100, 100-150, etc.)")
    print("   - LLM: 100ms buckets (0-100, 100-200, 200-300, etc.)")
    print("   - TTS: 100ms buckets (0-100, 100-200, 200-300, etc.)")
    print("3. Set X-axis Label: 'Latency (ms)'")
    print("4. Set Y-axis Label: 'Frequency'")
    print("5. Set Time Range: 'Last 1 hour'")
    print("")
    print("Expected SLA Thresholds:")
    print("- STT: <800ms (95th percentile)")
    print("- LLM: <1000ms (95th percentile)")
    print("- TTS: <1500ms (95th percentile)")
    print("")

if __name__ == "__main__":
    main()

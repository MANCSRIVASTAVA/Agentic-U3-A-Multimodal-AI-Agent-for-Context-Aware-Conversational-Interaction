#!/usr/bin/env python3
"""
Generate test data for SLA metrics to populate Grafana dashboards
This script generates realistic latency data for STT, LLM, and TTS services
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

def generate_stt_test_data():
    """Generate STT test data with realistic latency patterns"""
    print("Generating STT test data...")
    
    # Simulate multiple STT requests with varying latency
    for i in range(20):
        try:
            # Simulate audio transcription request
            start_time = time.time()
            
            # Make a test request to STT service
            response = requests.get(f"{SERVICES['stt']}/v1/health", timeout=5)
            
            # Simulate processing time (200-800ms for STT)
            processing_time = random.uniform(0.2, 0.8)
            time.sleep(processing_time)
            
            end_time = time.time()
            total_latency = (end_time - start_time) * 1000  # Convert to ms
            
            print(f"STT Request {i+1}: {total_latency:.2f}ms")
            
        except Exception as e:
            print(f"STT Request {i+1}: Error - {e}")
        
        # Small delay between requests
        time.sleep(0.5)

def generate_llm_test_data():
    """Generate LLM test data with first-token latency patterns"""
    print("Generating LLM test data...")
    
    for i in range(15):
        try:
            # Simulate LLM generation request
            start_time = time.time()
            
            # Make a test request to LLM service
            response = requests.get(f"{SERVICES['llm']}/v1/health", timeout=5)
            
            # Simulate first-token latency (300-1000ms for LLM)
            first_token_latency = random.uniform(0.3, 1.0)
            time.sleep(first_token_latency)
            
            end_time = time.time()
            total_latency = (end_time - start_time) * 1000  # Convert to ms
            
            print(f"LLM Request {i+1}: {total_latency:.2f}ms (first-token: {first_token_latency*1000:.2f}ms)")
            
        except Exception as e:
            print(f"LLM Request {i+1}: Error - {e}")
        
        # Small delay between requests
        time.sleep(0.8)

def generate_tts_test_data():
    """Generate TTS test data with response latency patterns"""
    print("Generating TTS test data...")
    
    for i in range(18):
        try:
            # Simulate TTS synthesis request
            start_time = time.time()
            
            # Make a test request to TTS service
            response = requests.get(f"{SERVICES['tts']}/v1/health", timeout=5)
            
            # Simulate TTS response latency (500-1500ms for TTS)
            response_latency = random.uniform(0.5, 1.5)
            time.sleep(response_latency)
            
            end_time = time.time()
            total_latency = (end_time - start_time) * 1000  # Convert to ms
            
            print(f"TTS Request {i+1}: {total_latency:.2f}ms")
            
        except Exception as e:
            print(f"TTS Request {i+1}: Error - {e}")
        
        # Small delay between requests
        time.sleep(0.6)

def generate_orchestrator_test_data():
    """Generate orchestrator test data to trigger all services"""
    print("Generating Orchestrator test data...")
    
    for i in range(10):
        try:
            # Simulate full chat request through orchestrator
            start_time = time.time()
            
            # Make a test request to orchestrator
            response = requests.get(f"{SERVICES['orchestrator']}/v1/health", timeout=5)
            
            # Simulate full pipeline latency
            pipeline_latency = random.uniform(1.0, 3.0)
            time.sleep(pipeline_latency)
            
            end_time = time.time()
            total_latency = (end_time - start_time) * 1000  # Convert to ms
            
            print(f"Orchestrator Request {i+1}: {total_latency:.2f}ms")
            
        except Exception as e:
            print(f"Orchestrator Request {i+1}: Error - {e}")
        
        # Delay between requests
        time.sleep(1.0)

def main():
    """Main function to generate all test data"""
    print("==========================================")
    print("GENERATING SLA TEST DATA FOR GRAFANA"
    print("==========================================")
    print("")
    print("This will generate realistic latency data for:")
    print("- STT Service (200-800ms latency)")
    print("- LLM Service (300-1000ms first-token latency)")
    print("- TTS Service (500-1500ms response latency)")
    print("- Orchestrator (full pipeline latency)")
    print("")
    print("Data will be visible in Grafana dashboards...")
    print("")
    
    # Generate test data for each service
    generate_stt_test_data()
    print("")
    generate_llm_test_data()
    print("")
    generate_tts_test_data()
    print("")
    generate_orchestrator_test_data()
    
    print("")
    print("==========================================")
    print("TEST DATA GENERATION COMPLETE"
    print("==========================================")
    print("")
    print("Now open Grafana dashboards to see the data:")
    print("- STT Dashboard: http://localhost:3000/d/stt-dashboard/stt-service-dashboard")
    print("- LLM Dashboard: http://localhost:3000/d/llm-dashboard/llm-service-dashboard")
    print("- TTS Dashboard: http://localhost:3000/d/tts-dashboard/tts-service-dashboard")
    print("")
    print("Look for latency histograms and distribution panels!")
    print("")

if __name__ == "__main__":
    main()

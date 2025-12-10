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

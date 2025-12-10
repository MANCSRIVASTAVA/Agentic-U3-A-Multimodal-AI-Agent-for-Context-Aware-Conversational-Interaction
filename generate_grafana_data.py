#!/usr/bin/env python3
"""
Generate realistic test data for Grafana dashboard
"""

import requests
import time
import random
import json
import threading
from datetime import datetime

class MetricsGenerator:
    def __init__(self):
        self.services = {
            "orchestrator": "http://localhost:8081",
            "llm": "http://localhost:8200",
            "stt": "http://localhost:8300",
            "tts": "http://localhost:8400",
            "rag": "http://localhost:8100",
            "analytics": "http://localhost:8500",
            "sentiment": "http://localhost:8700",
            "feedback": "http://localhost:8800"
        }
        self.running = True
        
    def generate_health_checks(self):
        """Generate continuous health checks"""
        while self.running:
            for service_name, base_url in self.services.items():
                try:
                    # Health check
                    response = requests.get(f"{base_url}/v1/health", timeout=2)
                    if response.status_code == 200:
                        print(f"✓ {service_name}: Health OK")
                    
                    # Metrics endpoint
                    metrics_response = requests.get(f"{base_url}/v1/metrics", timeout=2)
                    if metrics_response.status_code == 200:
                        print(f"✓ {service_name}: Metrics OK")
                    
                except Exception as e:
                    print(f"⚠ {service_name}: {e}")
            
            time.sleep(2)  # Check every 2 seconds
    
    def generate_api_calls(self):
        """Generate realistic API calls to create metrics"""
        while self.running:
            try:
                # Orchestrator chat calls
                orchestrator_url = self.services["orchestrator"]
                chat_data = {
                    "query": f"Test query at {datetime.now().strftime('%H:%M:%S')}",
                    "session_id": f"session_{random.randint(1000, 9999)}"
                }
                
                response = requests.post(
                    f"{orchestrator_url}/v1/chat",
                    json=chat_data,
                    timeout=5
                )
                if response.status_code in [200, 400, 401, 422]:  # Accept various responses
                    print(f"✓ Orchestrator: Chat API call (status: {response.status_code})")
                
                # Analytics summary calls
                analytics_url = self.services["analytics"]
                summary_data = {
                    "session_id": f"session_{random.randint(1000, 9999)}",
                    "summary": f"Test summary {random.randint(1, 100)}"
                }
                
                response = requests.post(
                    f"{analytics_url}/v1/summary",
                    json=summary_data,
                    timeout=5
                )
                if response.status_code in [200, 400, 401, 422]:
                    print(f"✓ Analytics: Summary API call (status: {response.status_code})")
                
                # RAG search calls
                rag_url = self.services["rag"]
                search_data = {
                    "query": f"Search query {random.randint(1, 100)}",
                    "limit": 5
                }
                
                response = requests.post(
                    f"{rag_url}/v1/search",
                    json=search_data,
                    timeout=5
                )
                if response.status_code in [200, 400, 401, 422]:
                    print(f"✓ RAG: Search API call (status: {response.status_code})")
                
                # TTS synthesis calls
                tts_url = self.services["tts"]
                tts_data = {
                    "text": f"Test text for TTS {random.randint(1, 100)}",
                    "voice": "alloy"
                }
                
                response = requests.post(
                    f"{tts_url}/v1/synthesize",
                    json=tts_data,
                    timeout=5
                )
                if response.status_code in [200, 400, 401, 422]:
                    print(f"✓ TTS: Synthesis API call (status: {response.status_code})")
                
                # Sentiment analysis calls
                sentiment_url = self.services["sentiment"]
                sentiment_data = {
                    "text": f"Test text for sentiment analysis {random.randint(1, 100)}"
                }
                
                response = requests.post(
                    f"{sentiment_url}/v1/analyze",
                    json=sentiment_data,
                    timeout=5
                )
                if response.status_code in [200, 400, 401, 422]:
                    print(f"✓ Sentiment: Analysis API call (status: {response.status_code})")
                
                # Feedback analysis calls
                feedback_url = self.services["feedback"]
                feedback_data = {
                    "session_id": f"session_{random.randint(1000, 9999)}",
                    "feedback": f"Test feedback {random.randint(1, 100)}"
                }
                
                response = requests.post(
                    f"{feedback_url}/v1/feedback/analyze",
                    json=feedback_data,
                    timeout=5
                )
                if response.status_code in [200, 400, 401, 422]:
                    print(f"✓ Feedback: Analysis API call (status: {response.status_code})")
                
            except Exception as e:
                print(f"⚠ API calls error: {e}")
            
            time.sleep(3)  # Generate calls every 3 seconds
    
    def generate_load_test(self):
        """Generate load test data"""
        while self.running:
            try:
                # Generate burst of requests
                for _ in range(10):
                    for service_name, base_url in self.services.items():
                        try:
                            # Health check
                            requests.get(f"{base_url}/v1/health", timeout=1)
                            # Metrics
                            requests.get(f"{base_url}/v1/metrics", timeout=1)
                        except:
                            pass
                    
                    time.sleep(0.1)  # Small delay between requests
                
                print(f"✓ Load test burst completed at {datetime.now().strftime('%H:%M:%S')}")
                
            except Exception as e:
                print(f"⚠ Load test error: {e}")
            
            time.sleep(10)  # Burst every 10 seconds
    
    def start(self):
        """Start all metric generation threads"""
        print("Starting metrics generation...")
        
        # Start health check thread
        health_thread = threading.Thread(target=self.generate_health_checks, daemon=True)
        health_thread.start()
        
        # Start API calls thread
        api_thread = threading.Thread(target=self.generate_api_calls, daemon=True)
        api_thread.start()
        
        # Start load test thread
        load_thread = threading.Thread(target=self.generate_load_test, daemon=True)
        load_thread.start()
        
        print("All metric generation threads started!")
        print("Press Ctrl+C to stop...")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping metric generation...")
            self.running = False

def create_simple_dashboard():
    """Create a simple dashboard that will definitely show data"""
    print("Creating simple dashboard with guaranteed metrics...")
    
    dashboard = {
        "dashboard": {
            "title": "Simple Microservices Dashboard",
            "tags": ["microservices", "simple"],
            "timezone": "browser",
            "panels": [
                {
                    "id": 1,
                    "title": "Service Health",
                    "type": "stat",
                    "targets": [
                        {
                            "expr": "up{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 4, "w": 24, "x": 0, "y": 0}
                },
                {
                    "id": 2,
                    "title": "HTTP Requests",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "http_requests_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 4}
                },
                {
                    "id": 3,
                    "title": "Memory Usage",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "process_resident_memory_bytes{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 4}
                },
                {
                    "id": 4,
                    "title": "CPU Usage",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "rate(process_cpu_seconds_total{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}[5m]) * 100",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 12}
                },
                {
                    "id": 5,
                    "title": "File Descriptors",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "process_open_fds{job=~\"orchestrator|llm|stt|tts|rag|analytics|sentiment|feedback\"}",
                            "refId": "A"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 12}
                }
            ],
            "time": {"from": "now-1h", "to": "now"},
            "refresh": "5s"
        }
    }
    
    with open("simple_dashboard.json", "w") as f:
        json.dump(dashboard, f, indent=2)
    
    print("✓ Simple dashboard created: simple_dashboard.json")
    return dashboard

def main():
    print("==========================================")
    print("GENERATING GRAFANA TEST DATA")
    print("==========================================")
    print("")
    
    # Create simple dashboard
    create_simple_dashboard()
    
    # Start metrics generation
    generator = MetricsGenerator()
    generator.start()

if __name__ == "__main__":
    main()

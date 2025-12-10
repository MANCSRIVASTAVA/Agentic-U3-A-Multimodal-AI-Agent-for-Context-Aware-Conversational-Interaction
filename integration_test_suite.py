#!/usr/bin/env python3
"""
Complete System Integration Test Suite
Tests end-to-end workflows and service interactions
"""

import asyncio
import json
import time
import requests
import websockets
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemIntegrationTester:
    def __init__(self):
        self.base_urls = {
            'orchestrator': 'http://localhost:8081',
            'analytics': 'http://localhost:8500',
            'llm': 'http://localhost:8200',
            'stt': 'http://localhost:8300',
            'tts': 'http://localhost:8400',
            'rag': 'http://localhost:8100',
            'frontend': 'http://localhost:3000'
        }
        self.test_results = {}
        
    def test_service_health(self) -> Dict[str, bool]:
        """Test all services are healthy"""
        logger.info("Testing service health...")
        health_status = {}
        
        for service, url in self.base_urls.items():
            try:
                if service == 'stt':
                    response = requests.get(f"{url}/v1/health", timeout=5)
                    health_status[service] = response.json().get('ok', False)
                elif service == 'frontend':
                    response = requests.get(url, timeout=5)
                    health_status[service] = response.status_code == 200
                else:
                    response = requests.get(f"{url}/v1/health", timeout=5)
                    health_status[service] = response.json().get('status') == 'ok'
            except Exception as e:
                logger.error(f"Health check failed for {service}: {e}")
                health_status[service] = False
                
        self.test_results['health'] = health_status
        return health_status
    
    def test_orchestrator_chat_workflow(self) -> Dict[str, Any]:
        """Test complete chat workflow through orchestrator"""
        logger.info("Testing orchestrator chat workflow...")
        
        try:
            # Test chat endpoint
            chat_payload = {
                "query": "Hello, can you help me with a test message?",
                "session_id": "integration_test_session"
            }
            
            response = requests.post(
                f"{self.base_urls['orchestrator']}/v1/chat",
                json=chat_payload,
                timeout=30
            )
            
            result = {
                'status_code': response.status_code,
                'response': response.json() if response.status_code == 200 else response.text,
                'success': response.status_code == 200
            }
            
            self.test_results['orchestrator_chat'] = result
            return result
            
        except Exception as e:
            error_result = {'success': False, 'error': str(e)}
            self.test_results['orchestrator_chat'] = error_result
            return error_result
    
    def test_llm_generation(self) -> Dict[str, Any]:
        """Test LLM service directly"""
        logger.info("Testing LLM generation...")
        
        try:
            payload = {
                "prompt": "Generate a short test response for integration testing",
                "max_tokens": 50
            }
            
            response = requests.post(
                f"{self.base_urls['llm']}/v1/generate",
                json=payload,
                timeout=60
            )
            
            result = {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'response_length': len(response.text) if response.status_code == 200 else 0
            }
            
            self.test_results['llm_generation'] = result
            return result
            
        except Exception as e:
            error_result = {'success': False, 'error': str(e)}
            self.test_results['llm_generation'] = error_result
            return error_result
    
    def test_tts_synthesis(self) -> Dict[str, Any]:
        """Test TTS service"""
        logger.info("Testing TTS synthesis...")
        
        try:
            payload = {
                "text": "This is a test message for TTS integration testing",
                "voice": "female_en"
            }
            
            response = requests.post(
                f"{self.base_urls['tts']}/v1/tts",
                json=payload,
                timeout=30
            )
            
            result = {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'content_type': response.headers.get('content-type', ''),
                'response_length': len(response.content) if response.status_code == 200 else 0
            }
            
            self.test_results['tts_synthesis'] = result
            return result
            
        except Exception as e:
            error_result = {'success': False, 'error': str(e)}
            self.test_results['tts_synthesis'] = error_result
            return error_result
    
    def test_analytics_data_ingestion(self) -> Dict[str, Any]:
        """Test analytics service data ingestion"""
        logger.info("Testing analytics data ingestion...")
        
        try:
            # Test analytics summary
            response = requests.get(
                f"{self.base_urls['analytics']}/v1/summary?session_id=integration_test",
                timeout=10
            )
            
            result = {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'data': response.json() if response.status_code == 200 else None
            }
            
            self.test_results['analytics'] = result
            return result
            
        except Exception as e:
            error_result = {'success': False, 'error': str(e)}
            self.test_results['analytics'] = error_result
            return error_result
    
    def test_rag_functionality(self) -> Dict[str, Any]:
        """Test RAG service"""
        logger.info("Testing RAG functionality...")
        
        try:
            # Test RAG health and basic functionality
            response = requests.get(f"{self.base_urls['rag']}/v1/health", timeout=10)
            
            result = {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'health_status': response.json() if response.status_code == 200 else None
            }
            
            self.test_results['rag'] = result
            return result
            
        except Exception as e:
            error_result = {'success': False, 'error': str(e)}
            self.test_results['rag'] = error_result
            return error_result
    
    async def test_stt_websocket(self) -> Dict[str, Any]:
        """Test STT WebSocket connection"""
        logger.info("Testing STT WebSocket...")
        
        try:
            uri = f"ws://localhost:8300/v1/transcribe/ws"
            
            async with websockets.connect(uri) as websocket:
                # Send a ping message
                ping_message = json.dumps({"event": "ping"})
                await websocket.send(ping_message)
                
                # Wait for pong response
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                response_data = json.loads(response)
                
                result = {
                    'success': response_data.get('event') == 'pong',
                    'response': response_data
                }
                
                self.test_results['stt_websocket'] = result
                return result
                
        except Exception as e:
            error_result = {'success': False, 'error': str(e)}
            self.test_results['stt_websocket'] = error_result
            return error_result
    
    def test_frontend_connectivity(self) -> Dict[str, Any]:
        """Test frontend connectivity and API integration"""
        logger.info("Testing frontend connectivity...")
        
        try:
            # Test frontend is accessible
            response = requests.get(self.base_urls['frontend'], timeout=10)
            
            result = {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'content_type': response.headers.get('content-type', ''),
                'response_length': len(response.text)
            }
            
            self.test_results['frontend'] = result
            return result
            
        except Exception as e:
            error_result = {'success': False, 'error': str(e)}
            self.test_results['frontend'] = error_result
            return error_result
    
    def test_service_metrics(self) -> Dict[str, Any]:
        """Test that all services are exposing metrics"""
        logger.info("Testing service metrics...")
        
        metrics_status = {}
        
        for service, url in self.base_urls.items():
            if service == 'frontend':
                continue
                
            try:
                response = requests.get(f"{url}/v1/metrics", timeout=5)
                metrics_status[service] = {
                    'success': response.status_code == 200,
                    'content_length': len(response.text),
                    'has_prometheus_format': '# HELP' in response.text
                }
            except Exception as e:
                metrics_status[service] = {'success': False, 'error': str(e)}
        
        self.test_results['metrics'] = metrics_status
        return metrics_status
    
    def run_complete_integration_test(self) -> Dict[str, Any]:
        """Run all integration tests"""
        logger.info("Starting complete system integration test...")
        start_time = time.time()
        
        # Run synchronous tests
        health_results = self.test_service_health()
        orchestrator_results = self.test_orchestrator_chat_workflow()
        llm_results = self.test_llm_generation()
        tts_results = self.test_tts_synthesis()
        analytics_results = self.test_analytics_data_ingestion()
        rag_results = self.test_rag_functionality()
        frontend_results = self.test_frontend_connectivity()
        metrics_results = self.test_service_metrics()
        
        # Run asynchronous tests
        stt_results = asyncio.run(self.test_stt_websocket())
        
        end_time = time.time()
        
        # Calculate overall success
        all_tests = [
            health_results, orchestrator_results, llm_results, 
            tts_results, analytics_results, rag_results, 
            frontend_results, stt_results
        ]
        
        # Check each test individually
        health_success = all(health_results.values())
        orchestrator_success = orchestrator_results.get('success', False)
        llm_success = llm_results.get('success', False)
        tts_success = tts_results.get('success', False)
        analytics_success = analytics_results.get('success', False)
        rag_success = rag_results.get('success', False)
        frontend_success = frontend_results.get('success', False)
        stt_success = stt_results.get('success', False)
        
        # Metrics test is special - check if all services have metrics
        metrics_success = all(
            service.get('success', False) 
            for service in metrics_results.values()
        )
        
        overall_success = all([
            health_success, orchestrator_success, llm_success, 
            tts_success, analytics_success, rag_success, 
            frontend_success, stt_success, metrics_success
        ])
        
        summary = {
            'overall_success': overall_success,
            'total_duration': end_time - start_time,
            'test_results': self.test_results,
            'summary': {
                'services_healthy': sum(health_results.values()),
                'total_services': len(health_results),
                'successful_tests': sum([
                    health_success, orchestrator_success, llm_success, 
                    tts_success, analytics_success, rag_success, 
                    frontend_success, stt_success, metrics_success
                ]),
                'total_tests': len(all_tests)
            }
        }
        
        return summary
    
    def print_test_report(self, results: Dict[str, Any]):
        """Print a formatted test report"""
        print("\n" + "="*60)
        print("SYSTEM INTEGRATION TEST REPORT")
        print("="*60)
        
        print(f"Overall Success: {'PASS' if results['overall_success'] else 'FAIL'}")
        print(f"Total Duration: {results['total_duration']:.2f} seconds")
        print(f"Services Healthy: {results['summary']['services_healthy']}/{results['summary']['total_services']}")
        print(f"Successful Tests: {results['summary']['successful_tests']}/{results['summary']['total_tests']}")
        
        print("\n" + "-"*40)
        print("DETAILED RESULTS")
        print("-"*40)
        
        for test_name, result in results['test_results'].items():
            if isinstance(result, dict):
                if 'success' in result:
                    status = "PASS" if result['success'] else "FAIL"
                    print(f"{test_name}: {status}")
                else:
                    # Health check results
                    if all(isinstance(v, bool) for v in result.values()):
                        healthy_count = sum(result.values())
                        total_count = len(result)
                        print(f"{test_name}: {healthy_count}/{total_count} services healthy")
                    else:
                        print(f"{test_name}: {result}")
            else:
                print(f"{test_name}: {result}")
        
        print("\n" + "="*60)

def main():
    """Main function to run integration tests"""
    tester = SystemIntegrationTester()
    results = tester.run_complete_integration_test()
    tester.print_test_report(results)
    
    # Save results to file
    with open('integration_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: integration_test_results.json")
    
    return results['overall_success']

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

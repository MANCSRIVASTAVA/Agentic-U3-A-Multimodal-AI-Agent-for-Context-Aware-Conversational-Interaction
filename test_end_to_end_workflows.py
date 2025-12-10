#!/usr/bin/env python3
"""
End-to-End Workflow Tests
Tests complete user workflows from frontend to all backend services
"""

import asyncio
import json
import time
import requests
import websockets
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EndToEndWorkflowTester:
    def __init__(self):
        self.base_urls = {
            'frontend': 'http://localhost:3000',
            'orchestrator': 'http://localhost:8081',
            'analytics': 'http://localhost:8500',
            'llm': 'http://localhost:8200',
            'stt': 'ws://localhost:8300',
            'tts': 'http://localhost:8400',
            'rag': 'http://localhost:8100'
        }
        self.test_session_id = f"e2e_test_{int(time.time())}"
        
    def workflow_1_chat_conversation(self) -> Dict[str, Any]:
        """Workflow 1: Complete chat conversation through orchestrator"""
        logger.info("Testing Workflow 1: Chat Conversation")
        
        try:
            # Step 1: Start conversation
            chat_payload = {
                "query": "Hello, I need help with a technical question about microservices architecture.",
                "session_id": self.test_session_id
            }
            
            response = requests.post(
                f"{self.base_urls['orchestrator']}/v1/chat",
                json=chat_payload,
                timeout=30
            )
            
            if response.status_code != 200:
                return {'success': False, 'error': f'Chat failed: {response.status_code}'}
            
            chat_response = response.json()
            
            # Step 2: Follow-up question
            followup_payload = {
                "query": "Can you explain how the orchestrator coordinates different services?",
                "session_id": self.test_session_id
            }
            
            response2 = requests.post(
                f"{self.base_urls['orchestrator']}/v1/chat",
                json=followup_payload,
                timeout=30
            )
            
            if response2.status_code != 200:
                return {'success': False, 'error': f'Follow-up chat failed: {response2.status_code}'}
            
            followup_response = response2.json()
            
            return {
                'success': True,
                'initial_response': chat_response,
                'followup_response': followup_response,
                'session_id': self.test_session_id
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def workflow_2_llm_direct_generation(self) -> Dict[str, Any]:
        """Workflow 2: Direct LLM generation"""
        logger.info("Testing Workflow 2: Direct LLM Generation")
        
        try:
            payload = {
                "prompt": "Write a short technical explanation of microservices isolation testing.",
                "max_tokens": 20
            }
            
            response = requests.post(
                f"{self.base_urls['llm']}/v1/generate",
                json=payload,
                timeout=120
            )
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response_length': len(response.text) if response.status_code == 200 else 0,
                'content': response.text[:200] if response.status_code == 200 else response.text
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def workflow_3_tts_synthesis(self) -> Dict[str, Any]:
        """Workflow 3: Text-to-Speech synthesis"""
        logger.info("Testing Workflow 3: TTS Synthesis")
        
        try:
            payload = {
                "text": "This is a test of the text-to-speech synthesis system for end-to-end workflow testing.",
                "voice": "female_en"
            }
            
            response = requests.post(
                f"{self.base_urls['tts']}/v1/tts",
                json=payload,
                timeout=30
            )
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'response_size': len(response.content) if response.status_code == 200 else 0
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def workflow_4_stt_websocket(self) -> Dict[str, Any]:
        """Workflow 4: Speech-to-Text WebSocket"""
        logger.info("Testing Workflow 4: STT WebSocket")
        
        try:
            uri = f"{self.base_urls['stt']}/v1/transcribe/ws"
            
            async with websockets.connect(uri) as websocket:
                # Send ping
                ping_message = json.dumps({"event": "ping"})
                await websocket.send(ping_message)
                
                # Wait for pong
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                response_data = json.loads(response)
                
                # Send close
                close_message = json.dumps({"event": "close"})
                await websocket.send(close_message)
                
                return {
                    'success': response_data.get('event') == 'pong',
                    'response': response_data
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def workflow_5_analytics_data_flow(self) -> Dict[str, Any]:
        """Workflow 5: Analytics data collection and retrieval"""
        logger.info("Testing Workflow 5: Analytics Data Flow")
        
        try:
            # Generate some activity first
            chat_payload = {
                "query": "Generate analytics data for testing",
                "session_id": self.test_session_id
            }
            
            requests.post(
                f"{self.base_urls['orchestrator']}/v1/chat",
                json=chat_payload,
                timeout=10
            )
            
            # Wait a moment for data to be processed
            time.sleep(2)
            
            # Retrieve analytics summary
            response = requests.get(
                f"{self.base_urls['analytics']}/v1/summary?session_id={self.test_session_id}",
                timeout=10
            )
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'analytics_data': response.json() if response.status_code == 200 else None
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def workflow_6_rag_integration(self) -> Dict[str, Any]:
        """Workflow 6: RAG service integration"""
        logger.info("Testing Workflow 6: RAG Integration")
        
        try:
            # Test RAG health
            response = requests.get(f"{self.base_urls['rag']}/v1/health", timeout=10)
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'rag_status': response.json() if response.status_code == 200 else None
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def workflow_7_frontend_backend_integration(self) -> Dict[str, Any]:
        """Workflow 7: Frontend-Backend Integration"""
        logger.info("Testing Workflow 7: Frontend-Backend Integration")
        
        try:
            # Test frontend accessibility
            frontend_response = requests.get(self.base_urls['frontend'], timeout=10)
            
            # Test API proxy (if configured)
            api_response = requests.get(f"{self.base_urls['frontend']}/api/v1/health", timeout=10)
            
            return {
                'success': frontend_response.status_code == 200,
                'frontend_status': frontend_response.status_code,
                'api_proxy_status': api_response.status_code,
                'frontend_size': len(frontend_response.text)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def workflow_8_metrics_collection(self) -> Dict[str, Any]:
        """Workflow 8: Metrics collection across all services"""
        logger.info("Testing Workflow 8: Metrics Collection")
        
        metrics_status = {}
        
        for service, url in self.base_urls.items():
            if service == 'frontend' or service == 'stt':
                continue
                
            try:
                response = requests.get(f"{url}/v1/metrics", timeout=5)
                metrics_status[service] = {
                    'success': response.status_code == 200,
                    'has_prometheus_format': '# HELP' in response.text,
                    'content_length': len(response.text)
                }
            except Exception as e:
                metrics_status[service] = {'success': False, 'error': str(e)}
        
        return {
            'success': all(service.get('success', False) for service in metrics_status.values()),
            'metrics_status': metrics_status
        }
    
    async def run_all_workflows(self) -> Dict[str, Any]:
        """Run all end-to-end workflows"""
        logger.info("Starting all end-to-end workflows...")
        start_time = time.time()
        
        # Run synchronous workflows
        workflows = {
            'chat_conversation': self.workflow_1_chat_conversation(),
            'llm_generation': self.workflow_2_llm_direct_generation(),
            'tts_synthesis': self.workflow_3_tts_synthesis(),
            'analytics_data_flow': self.workflow_5_analytics_data_flow(),
            'rag_integration': self.workflow_6_rag_integration(),
            'frontend_backend_integration': self.workflow_7_frontend_backend_integration(),
            'metrics_collection': self.workflow_8_metrics_collection()
        }
        
        # Run asynchronous workflows
        workflows['stt_websocket'] = await self.workflow_4_stt_websocket()
        
        end_time = time.time()
        
        # Calculate overall success
        overall_success = all(workflow.get('success', False) for workflow in workflows.values())
        
        summary = {
            'overall_success': overall_success,
            'total_duration': end_time - start_time,
            'workflows': workflows,
            'summary': {
                'successful_workflows': sum(1 for workflow in workflows.values() if workflow.get('success', False)),
                'total_workflows': len(workflows)
            }
        }
        
        return summary
    
    def print_workflow_report(self, results: Dict[str, Any]):
        """Print formatted workflow report"""
        print("\n" + "="*70)
        print("END-TO-END WORKFLOW TEST REPORT")
        print("="*70)
        
        print(f"Overall Success: {'PASS' if results['overall_success'] else 'FAIL'}")
        print(f"Total Duration: {results['total_duration']:.2f} seconds")
        print(f"Successful Workflows: {results['summary']['successful_workflows']}/{results['summary']['total_workflows']}")
        
        print("\n" + "-"*50)
        print("WORKFLOW DETAILS")
        print("-"*50)
        
        for workflow_name, result in results['workflows'].items():
            status = "PASS" if result.get('success', False) else "FAIL"
            print(f"{workflow_name.replace('_', ' ').title()}: {status}")
            
            if not result.get('success', False) and 'error' in result:
                print(f"  Error: {result['error']}")
        
        print("\n" + "="*70)

def main():
    """Main function to run end-to-end workflow tests"""
    tester = EndToEndWorkflowTester()
    results = asyncio.run(tester.run_all_workflows())
    tester.print_workflow_report(results)
    
    # Save results to file
    with open('e2e_workflow_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: e2e_workflow_results.json")
    
    return results['overall_success']

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

#!/usr/bin/env python3
"""
Frontend Integration Test
Tests the frontend UI connectivity and API integration
"""

import requests
import json
import time
from typing import Dict, Any

class FrontendIntegrationTester:
    def __init__(self):
        self.frontend_url = "http://localhost:3000"
        self.orchestrator_url = "http://localhost:8081"
        
    def test_frontend_accessibility(self) -> Dict[str, Any]:
        """Test if frontend is accessible"""
        print("Testing frontend accessibility...")
        
        try:
            response = requests.get(self.frontend_url, timeout=10)
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'response_size': len(response.text)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_api_proxy_connectivity(self) -> Dict[str, Any]:
        """Test if frontend can reach backend APIs through proxy"""
        print("Testing API proxy connectivity...")
        
        # Test if frontend can reach orchestrator through API proxy
        try:
            # This tests the /api proxy route that should forward to orchestrator
            response = requests.get(f"{self.frontend_url}/api/v1/health", timeout=10)
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response': response.json() if response.status_code == 200 else response.text
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_chat_workflow(self) -> Dict[str, Any]:
        """Test complete chat workflow through frontend"""
        print("Testing chat workflow...")
        
        try:
            # Test chat endpoint through frontend proxy
            chat_payload = {
                "query": "Hello, this is a frontend integration test",
                "session_id": "frontend_test_session"
            }
            
            response = requests.post(
                f"{self.frontend_url}/api/v1/chat",
                json=chat_payload,
                timeout=30
            )
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response': response.json() if response.status_code == 200 else response.text
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_direct_orchestrator_connection(self) -> Dict[str, Any]:
        """Test direct connection to orchestrator (bypassing frontend)"""
        print("Testing direct orchestrator connection...")
        
        try:
            response = requests.get(f"{self.orchestrator_url}/v1/health", timeout=10)
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response': response.json() if response.status_code == 200 else response.text
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_cors_headers(self) -> Dict[str, Any]:
        """Test CORS headers for frontend-backend communication"""
        print("Testing CORS headers...")
        
        try:
            # Test OPTIONS request with proper CORS preflight headers
            headers = {
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            response = requests.options(f"{self.orchestrator_url}/v1/chat", headers=headers, timeout=10)
            
            cors_headers = {
                'access_control_allow_origin': response.headers.get('Access-Control-Allow-Origin'),
                'access_control_allow_methods': response.headers.get('Access-Control-Allow-Methods'),
                'access_control_allow_headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'cors_headers': cors_headers,
                'cors_working': 'Access-Control-Allow-Origin' in response.headers
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def run_complete_frontend_test(self) -> Dict[str, Any]:
        """Run all frontend integration tests"""
        print("Starting frontend integration tests...")
        start_time = time.time()
        
        results = {
            'frontend_accessibility': self.test_frontend_accessibility(),
            'api_proxy_connectivity': self.test_api_proxy_connectivity(),
            'chat_workflow': self.test_chat_workflow(),
            'direct_orchestrator': self.test_direct_orchestrator_connection(),
            'cors_headers': self.test_cors_headers()
        }
        
        end_time = time.time()
        
        # Calculate overall success
        overall_success = all(result.get('success', False) for result in results.values())
        
        summary = {
            'overall_success': overall_success,
            'total_duration': end_time - start_time,
            'test_results': results,
            'summary': {
                'successful_tests': sum(1 for result in results.values() if result.get('success', False)),
                'total_tests': len(results)
            }
        }
        
        return summary
    
    def print_test_report(self, results: Dict[str, Any]):
        """Print formatted test report"""
        print("\n" + "="*60)
        print("FRONTEND INTEGRATION TEST REPORT")
        print("="*60)
        
        print(f"Overall Success: {'PASS' if results['overall_success'] else 'FAIL'}")
        print(f"Total Duration: {results['total_duration']:.2f} seconds")
        print(f"Successful Tests: {results['summary']['successful_tests']}/{results['summary']['total_tests']}")
        
        print("\n" + "-"*40)
        print("DETAILED RESULTS")
        print("-"*40)
        
        for test_name, result in results['test_results'].items():
            status = "PASS" if result.get('success', False) else "FAIL"
            print(f"{test_name}: {status}")
            
            if not result.get('success', False) and 'error' in result:
                print(f"  Error: {result['error']}")
        
        print("\n" + "="*60)

def main():
    """Main function to run frontend integration tests"""
    tester = FrontendIntegrationTester()
    results = tester.run_complete_frontend_test()
    tester.print_test_report(results)
    
    # Save results to file
    with open('frontend_integration_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: frontend_integration_results.json")
    
    return results['overall_success']

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

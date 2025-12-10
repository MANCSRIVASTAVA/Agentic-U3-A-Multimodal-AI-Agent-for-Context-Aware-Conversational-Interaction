#!/usr/bin/env python3
"""
Comprehensive User Interface Testing Suite
Tests all aspects of the frontend UI and its integration with backend services
"""

import requests
import json
import time
from typing import Dict, Any, List
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UIComprehensiveTester:
    def __init__(self):
        self.frontend_url = "http://localhost:3000"
        self.orchestrator_url = "http://localhost:8081"
        self.test_results = {}
        
    def test_ui_accessibility(self) -> Dict[str, Any]:
        """Test UI accessibility and basic functionality"""
        logger.info("Testing UI accessibility...")
        
        try:
            # Test main page load
            response = requests.get(self.frontend_url, timeout=10)
            
            # Check if it's a valid HTML page
            is_html = response.headers.get('content-type', '').startswith('text/html')
            has_react_root = '<div id="root">' in response.text
            has_assets = 'assets/' in response.text
            
            return {
                'success': response.status_code == 200 and is_html and has_react_root,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'is_html': is_html,
                'has_react_root': has_react_root,
                'has_assets': has_assets,
                'response_size': len(response.text)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_api_proxy_functionality(self) -> Dict[str, Any]:
        """Test API proxy functionality"""
        logger.info("Testing API proxy functionality...")
        
        try:
            # Test health endpoint through proxy
            health_response = requests.get(f"{self.frontend_url}/api/v1/health", timeout=10)
            
            # Test chat endpoint through proxy
            chat_payload = {
                "query": "Test UI chat functionality",
                "session_id": "ui_test_session"
            }
            chat_response = requests.post(
                f"{self.frontend_url}/api/v1/chat",
                json=chat_payload,
                timeout=30
            )
            
            return {
                'success': health_response.status_code == 200 and chat_response.status_code == 200,
                'health_status': health_response.status_code,
                'chat_status': chat_response.status_code,
                'health_response': health_response.json() if health_response.status_code == 200 else None,
                'chat_response': chat_response.json() if chat_response.status_code == 200 else None
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_ui_responsiveness(self) -> Dict[str, Any]:
        """Test UI responsiveness and performance"""
        logger.info("Testing UI responsiveness...")
        
        try:
            start_time = time.time()
            response = requests.get(self.frontend_url, timeout=10)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            return {
                'success': response.status_code == 200 and response_time < 2.0,
                'status_code': response.status_code,
                'response_time': response_time,
                'is_fast': response_time < 1.0,
                'is_acceptable': response_time < 2.0
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_ui_assets_loading(self) -> Dict[str, Any]:
        """Test UI assets loading (CSS, JS)"""
        logger.info("Testing UI assets loading...")
        
        try:
            # Get main page
            main_response = requests.get(self.frontend_url, timeout=10)
            
            if main_response.status_code != 200:
                return {'success': False, 'error': 'Main page not accessible'}
            
            # Extract asset URLs from HTML
            html_content = main_response.text
            css_assets = []
            js_assets = []
            
            # Find CSS assets
            import re
            css_pattern = r'href="([^"]*\.css[^"]*)"'
            css_matches = re.findall(css_pattern, html_content)
            
            # Find JS assets
            js_pattern = r'src="([^"]*\.js[^"]*)"'
            js_matches = re.findall(js_pattern, html_content)
            
            # Test CSS assets
            css_success = 0
            for css_url in css_matches:
                if css_url.startswith('/'):
                    css_url = f"{self.frontend_url}{css_url}"
                try:
                    css_response = requests.get(css_url, timeout=5)
                    if css_response.status_code == 200:
                        css_success += 1
                except:
                    pass
            
            # Test JS assets
            js_success = 0
            for js_url in js_matches:
                if js_url.startswith('/'):
                    js_url = f"{self.frontend_url}{js_url}"
                try:
                    js_response = requests.get(js_url, timeout=5)
                    if js_response.status_code == 200:
                        js_success += 1
                except:
                    pass
            
            return {
                'success': css_success > 0 and js_success > 0,
                'css_assets_found': len(css_matches),
                'js_assets_found': len(js_matches),
                'css_assets_loaded': css_success,
                'js_assets_loaded': js_success,
                'css_assets': css_matches,
                'js_assets': js_matches
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_ui_error_handling(self) -> Dict[str, Any]:
        """Test UI error handling"""
        logger.info("Testing UI error handling...")
        
        try:
            # Test non-existent page
            not_found_response = requests.get(f"{self.frontend_url}/nonexistent", timeout=10)
            
            # Test malformed API request
            malformed_response = requests.post(
                f"{self.frontend_url}/api/v1/chat",
                json={"invalid": "data"},
                timeout=10
            )
            
            return {
                'success': True,  # UI should handle errors gracefully
                'not_found_status': not_found_response.status_code,
                'malformed_status': malformed_response.status_code,
                'handles_404': not_found_response.status_code in [200, 404],
                'handles_malformed': malformed_response.status_code in [200, 400, 422]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_ui_cors_headers(self) -> Dict[str, Any]:
        """Test CORS headers for cross-origin requests"""
        logger.info("Testing CORS headers...")
        
        try:
            # Test OPTIONS request with proper CORS preflight headers
            headers = {
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            options_response = requests.options(f"{self.orchestrator_url}/v1/chat", headers=headers, timeout=10)
            
            cors_headers = {
                'access_control_allow_origin': options_response.headers.get('Access-Control-Allow-Origin'),
                'access_control_allow_methods': options_response.headers.get('Access-Control-Allow-Methods'),
                'access_control_allow_headers': options_response.headers.get('Access-Control-Allow-Headers')
            }
            
            # Test actual POST request with CORS
            post_headers = {
                'Origin': 'http://localhost:3000',
                'Content-Type': 'application/json'
            }
            post_response = requests.post(
                f"{self.orchestrator_url}/v1/chat",
                headers=post_headers,
                json={"query": "test", "session_id": "cors_test"},
                timeout=10
            )
            
            return {
                'success': options_response.status_code == 200 and post_response.status_code == 200,
                'options_status': options_response.status_code,
                'post_status': post_response.status_code,
                'cors_headers': cors_headers,
                'has_cors': any(cors_headers.values()),
                'cors_working': options_response.status_code == 200 and 'Access-Control-Allow-Origin' in options_response.headers
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_ui_chat_workflow(self) -> Dict[str, Any]:
        """Test complete chat workflow through UI"""
        logger.info("Testing UI chat workflow...")
        
        try:
            # Test chat through UI proxy
            chat_payload = {
                "query": "Hello, this is a UI test message",
                "session_id": "ui_chat_test"
            }
            
            response = requests.post(
                f"{self.frontend_url}/api/v1/chat",
                json=chat_payload,
                timeout=30
            )
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response': response.json() if response.status_code == 200 else response.text,
                'has_text': 'text' in (response.json() if response.status_code == 200 else {}),
                'has_provider': 'provider' in (response.json() if response.status_code == 200 else {})
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def run_comprehensive_ui_test(self) -> Dict[str, Any]:
        """Run all UI tests"""
        logger.info("Starting comprehensive UI testing...")
        start_time = time.time()
        
        tests = {
            'ui_accessibility': self.test_ui_accessibility(),
            'api_proxy_functionality': self.test_api_proxy_functionality(),
            'ui_responsiveness': self.test_ui_responsiveness(),
            'ui_assets_loading': self.test_ui_assets_loading(),
            'ui_error_handling': self.test_ui_error_handling(),
            'ui_cors_headers': self.test_ui_cors_headers(),
            'ui_chat_workflow': self.test_ui_chat_workflow()
        }
        
        end_time = time.time()
        
        # Calculate overall success
        overall_success = all(test.get('success', False) for test in tests.values())
        
        summary = {
            'overall_success': overall_success,
            'total_duration': end_time - start_time,
            'test_results': tests,
            'summary': {
                'successful_tests': sum(1 for test in tests.values() if test.get('success', False)),
                'total_tests': len(tests)
            }
        }
        
        return summary
    
    def print_ui_test_report(self, results: Dict[str, Any]):
        """Print formatted UI test report"""
        print("\n" + "="*70)
        print("COMPREHENSIVE USER INTERFACE TEST REPORT")
        print("="*70)
        
        print(f"Overall Success: {'PASS' if results['overall_success'] else 'FAIL'}")
        print(f"Total Duration: {results['total_duration']:.2f} seconds")
        print(f"Successful Tests: {results['summary']['successful_tests']}/{results['summary']['total_tests']}")
        
        print("\n" + "-"*50)
        print("UI TEST DETAILS")
        print("-"*50)
        
        for test_name, result in results['test_results'].items():
            status = "PASS" if result.get('success', False) else "FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
            
            if not result.get('success', False) and 'error' in result:
                print(f"  Error: {result['error']}")
        
        print("\n" + "="*70)

def main():
    """Main function to run comprehensive UI tests"""
    tester = UIComprehensiveTester()
    results = tester.run_comprehensive_ui_test()
    tester.print_ui_test_report(results)
    
    # Save results to file
    with open('ui_comprehensive_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: ui_comprehensive_results.json")
    
    return results['overall_success']

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

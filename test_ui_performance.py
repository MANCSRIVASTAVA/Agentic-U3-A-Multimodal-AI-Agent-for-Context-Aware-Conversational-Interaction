#!/usr/bin/env python3
"""
User Interface Performance Testing Suite
Tests UI performance, load times, and responsiveness
"""

import requests
import time
import statistics
from typing import Dict, Any, List
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UIPerformanceTester:
    def __init__(self):
        self.frontend_url = "http://localhost:3000"
        self.orchestrator_url = "http://localhost:8081"
        
    def test_page_load_performance(self, num_requests: int = 10) -> Dict[str, Any]:
        """Test page load performance with multiple requests"""
        logger.info(f"Testing page load performance with {num_requests} requests...")
        
        response_times = []
        success_count = 0
        
        for i in range(num_requests):
            try:
                start_time = time.time()
                response = requests.get(self.frontend_url, timeout=10)
                end_time = time.time()
                
                if response.status_code == 200:
                    success_count += 1
                    response_times.append(end_time - start_time)
            except Exception as e:
                logger.warning(f"Request {i+1} failed: {e}")
        
        if response_times:
            return {
                'success': success_count == num_requests,
                'total_requests': num_requests,
                'successful_requests': success_count,
                'success_rate': success_count / num_requests,
                'avg_response_time': statistics.mean(response_times),
                'min_response_time': min(response_times),
                'max_response_time': max(response_times),
                'median_response_time': statistics.median(response_times),
                'response_times': response_times
            }
        else:
            return {
                'success': False,
                'error': 'No successful requests',
                'total_requests': num_requests,
                'successful_requests': 0
            }
    
    def test_api_performance(self, num_requests: int = 5) -> Dict[str, Any]:
        """Test API performance through UI proxy"""
        logger.info(f"Testing API performance with {num_requests} requests...")
        
        response_times = []
        success_count = 0
        
        for i in range(num_requests):
            try:
                start_time = time.time()
                response = requests.get(f"{self.frontend_url}/api/v1/health", timeout=10)
                end_time = time.time()
                
                if response.status_code == 200:
                    success_count += 1
                    response_times.append(end_time - start_time)
            except Exception as e:
                logger.warning(f"API request {i+1} failed: {e}")
        
        if response_times:
            return {
                'success': success_count == num_requests,
                'total_requests': num_requests,
                'successful_requests': success_count,
                'success_rate': success_count / num_requests,
                'avg_response_time': statistics.mean(response_times),
                'min_response_time': min(response_times),
                'max_response_time': max(response_times),
                'median_response_time': statistics.median(response_times),
                'response_times': response_times
            }
        else:
            return {
                'success': False,
                'error': 'No successful API requests',
                'total_requests': num_requests,
                'successful_requests': 0
            }
    
    def test_chat_performance(self, num_requests: int = 3) -> Dict[str, Any]:
        """Test chat workflow performance"""
        logger.info(f"Testing chat performance with {num_requests} requests...")
        
        response_times = []
        success_count = 0
        
        for i in range(num_requests):
            try:
                start_time = time.time()
                chat_payload = {
                    "query": f"Test message {i+1}",
                    "session_id": f"perf_test_{i+1}"
                }
                response = requests.post(
                    f"{self.frontend_url}/api/v1/chat",
                    json=chat_payload,
                    timeout=30
                )
                end_time = time.time()
                
                if response.status_code == 200:
                    success_count += 1
                    response_times.append(end_time - start_time)
            except Exception as e:
                logger.warning(f"Chat request {i+1} failed: {e}")
        
        if response_times:
            return {
                'success': success_count == num_requests,
                'total_requests': num_requests,
                'successful_requests': success_count,
                'success_rate': success_count / num_requests,
                'avg_response_time': statistics.mean(response_times),
                'min_response_time': min(response_times),
                'max_response_time': max(response_times),
                'median_response_time': statistics.median(response_times),
                'response_times': response_times
            }
        else:
            return {
                'success': False,
                'error': 'No successful chat requests',
                'total_requests': num_requests,
                'successful_requests': 0
            }
    
    def test_concurrent_requests(self, num_concurrent: int = 5) -> Dict[str, Any]:
        """Test concurrent request handling"""
        logger.info(f"Testing concurrent requests with {num_concurrent} simultaneous requests...")
        
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request(request_id):
            try:
                start_time = time.time()
                response = requests.get(self.frontend_url, timeout=10)
                end_time = time.time()
                
                results.put({
                    'request_id': request_id,
                    'success': response.status_code == 200,
                    'response_time': end_time - start_time,
                    'status_code': response.status_code
                })
            except Exception as e:
                results.put({
                    'request_id': request_id,
                    'success': False,
                    'error': str(e),
                    'response_time': None
                })
        
        # Start concurrent requests
        threads = []
        start_time = time.time()
        
        for i in range(num_concurrent):
            thread = threading.Thread(target=make_request, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Collect results
        request_results = []
        while not results.empty():
            request_results.append(results.get())
        
        successful_requests = sum(1 for r in request_results if r['success'])
        response_times = [r['response_time'] for r in request_results if r['response_time'] is not None]
        
        return {
            'success': successful_requests == num_concurrent,
            'total_concurrent': num_concurrent,
            'successful_requests': successful_requests,
            'success_rate': successful_requests / num_concurrent,
            'total_time': total_time,
            'avg_response_time': statistics.mean(response_times) if response_times else 0,
            'request_results': request_results
        }
    
    def run_performance_tests(self) -> Dict[str, Any]:
        """Run all performance tests"""
        logger.info("Starting UI performance testing...")
        start_time = time.time()
        
        tests = {
            'page_load_performance': self.test_page_load_performance(10),
            'api_performance': self.test_api_performance(5),
            'chat_performance': self.test_chat_performance(3),
            'concurrent_requests': self.test_concurrent_requests(5)
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
    
    def print_performance_report(self, results: Dict[str, Any]):
        """Print formatted performance report"""
        print("\n" + "="*70)
        print("USER INTERFACE PERFORMANCE TEST REPORT")
        print("="*70)
        
        print(f"Overall Success: {'PASS' if results['overall_success'] else 'FAIL'}")
        print(f"Total Duration: {results['total_duration']:.2f} seconds")
        print(f"Successful Tests: {results['summary']['successful_tests']}/{results['summary']['total_tests']}")
        
        print("\n" + "-"*50)
        print("PERFORMANCE DETAILS")
        print("-"*50)
        
        for test_name, result in results['test_results'].items():
            status = "PASS" if result.get('success', False) else "FAIL"
            print(f"\n{test_name.replace('_', ' ').title()}: {status}")
            
            if 'avg_response_time' in result:
                print(f"  Average Response Time: {result['avg_response_time']:.3f}s")
                print(f"  Min Response Time: {result['min_response_time']:.3f}s")
                print(f"  Max Response Time: {result['max_response_time']:.3f}s")
                print(f"  Success Rate: {result.get('success_rate', 0)*100:.1f}%")
            
            if 'total_time' in result:
                print(f"  Total Time: {result['total_time']:.3f}s")
            
            if not result.get('success', False) and 'error' in result:
                print(f"  Error: {result['error']}")
        
        print("\n" + "="*70)

def main():
    """Main function to run UI performance tests"""
    tester = UIPerformanceTester()
    results = tester.run_performance_tests()
    tester.print_performance_report(results)
    
    # Save results to file
    import json
    with open('ui_performance_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: ui_performance_results.json")
    
    return results['overall_success']

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)


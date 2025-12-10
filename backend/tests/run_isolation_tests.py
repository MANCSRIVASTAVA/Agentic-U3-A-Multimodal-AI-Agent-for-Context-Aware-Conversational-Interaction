#!/usr/bin/env python3
"""
Isolation test runner for microservices.

This script runs isolation tests for all microservices and provides
detailed reporting on test results.
"""
import os
import sys
import subprocess
import argparse
import json
from pathlib import Path
from typing import Dict, List, Any
import time

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

class TestRunner:
    """Manages isolation test execution for microservices."""
    
    def __init__(self, verbose: bool = False, coverage: bool = False):
        self.verbose = verbose
        self.coverage = coverage
        self.results = {}
        self.start_time = None
        
    def run_tests(self, services: List[str] = None) -> Dict[str, Any]:
        """Run isolation tests for specified services."""
        if services is None:
            services = self._get_all_services()
        
        self.start_time = time.time()
        
        print(f"Starting isolation tests for {len(services)} services...")
        print(f"Services: {', '.join(services)}")
        print("-" * 60)
        
        for service in services:
            self._run_service_tests(service)
        
        self._print_summary()
        return self.results
    
    def _get_all_services(self) -> List[str]:
        """Get list of all available services."""
        # Return individual microservices for detailed testing
        return ["orchestrator", "analytics", "llm", "sentiment", "stt", "tts", "rag", "feedback"]
    
    def _run_service_tests(self, service: str):
        """Run tests for a specific service."""
        print(f"\nTesting {service.upper()} service...")
        
        if service == "thesis_ready":
            test_file = "test_thesis_ready.py"
        elif service == "working_isolation":
            test_file = "test_working_isolation.py"
        elif service == "comprehensive":
            test_file = "test_comprehensive_isolation.py"
        elif service == "performance":
            test_file = "test_performance_isolation.py"
        else:
            test_file = f"test_{service}_isolation.py"
        
        test_path = Path(__file__).parent / test_file
        
        if not test_path.exists():
            print(f"WARNING: No isolation tests found for {service}")
            self.results[service] = {
                "status": "skipped",
                "reason": "No test file found",
                "tests_run": 0,
                "tests_passed": 0,
                "tests_failed": 0,
                "duration": 0
            }
            return
        
        # Build pytest command
        cmd = self._build_pytest_command(test_path, service)
        
        # Run tests
        start_time = time.time()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            duration = time.time() - start_time
            
            # Parse results
            self.results[service] = self._parse_pytest_output(result, duration)
            
        except Exception as e:
            duration = time.time() - start_time
            self.results[service] = {
                "status": "error",
                "reason": str(e),
                "tests_run": 0,
                "tests_passed": 0,
                "tests_failed": 0,
                "duration": duration
            }
    
    def _build_pytest_command(self, test_path: Path, service: str) -> List[str]:
        """Build pytest command for running tests."""
        cmd = [
            sys.executable, "-m", "pytest",
            str(test_path),
            "-v" if self.verbose else "-q",
            "--tb=short",
            "--disable-warnings"
        ]
        
        if self.coverage:
            cmd.extend([
                "--cov", f"../{service}",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov/{service}"
            ])
        
        # Add JSON reporting
        report_filename = f"{test_path.stem}_report.json"
        cmd.extend([
            "--json-report",
            f"--json-report-file=reports/{report_filename}"
        ])
        
        return cmd
    
    def _parse_pytest_output(self, result: subprocess.CompletedProcess, duration: float) -> Dict[str, Any]:
        """Parse pytest output to extract test results."""
        status = "passed" if result.returncode == 0 else "failed"
        
        # Try to parse JSON report if available
        # Extract the test file name from the command arguments
        test_file_name = None
        for arg in result.args:
            if arg.endswith('.py') and 'test_' in arg:
                test_file_name = arg.split('/')[-1].replace('.py', '')
                break
        
        if test_file_name:
            report_file = Path(__file__).parent / "reports" / f"{test_file_name}_report.json"
            if report_file.exists():
                try:
                    with open(report_file) as f:
                        report_data = json.load(f)
                        summary = report_data.get("summary", {})
                        return {
                            "status": status,
                            "tests_run": summary.get("total", 0),
                            "tests_passed": summary.get("passed", 0),
                            "tests_failed": summary.get("failed", 0),
                            "tests_skipped": summary.get("skipped", 0),
                            "duration": duration,
                            "output": result.stdout,
                            "errors": result.stderr
                        }
                except Exception as e:
                    print(f"Warning: Could not parse JSON report: {e}")
                    pass
        
        # Fallback to parsing stdout
        lines = result.stdout.split('\n')
        tests_run = 0
        tests_passed = 0
        tests_failed = 0
        
        for line in lines:
            if "PASSED" in line:
                tests_passed += 1
                tests_run += 1
            elif "FAILED" in line:
                tests_failed += 1
                tests_run += 1
        
        return {
            "status": status,
            "tests_run": tests_run,
            "tests_passed": tests_passed,
            "tests_failed": tests_failed,
            "duration": duration,
            "output": result.stdout,
            "errors": result.stderr
        }
    
    def _print_summary(self):
        """Print test execution summary."""
        total_time = time.time() - self.start_time
        
        print("\n" + "=" * 60)
        print("ISOLATION TEST SUMMARY")
        print("=" * 60)
        
        total_tests = 0
        total_passed = 0
        total_failed = 0
        services_passed = 0
        services_failed = 0
        
        for service, result in self.results.items():
            status_icon = "PASS" if result["status"] == "passed" else "FAIL" if result["status"] == "failed" else "SKIP"
            skipped = result.get('tests_skipped', 0)
            print(f"{status_icon} {service.upper():<15} | "
                  f"Tests: {result['tests_run']:3d} | "
                  f"Passed: {result['tests_passed']:3d} | "
                  f"Failed: {result['tests_failed']:3d} | "
                  f"Skipped: {skipped:3d} | "
                  f"Time: {result['duration']:.2f}s")
            
            total_tests += result["tests_run"]
            total_passed += result["tests_passed"]
            total_failed += result["tests_failed"]
            
            if result["status"] == "passed":
                services_passed += 1
            elif result["status"] == "failed":
                services_failed += 1
        
        print("-" * 60)
        print(f"TOTALS: {total_tests} tests | {total_passed} passed | {total_failed} failed")
        print(f"SERVICES: {services_passed} passed | {services_failed} failed | {len(self.results) - services_passed - services_failed} skipped")
        print(f"TOTAL TIME: {total_time:.2f}s")
        
        if total_failed > 0:
            print("\nERROR: Some tests failed. Check the output above for details.")
            sys.exit(1)
        else:
            print("\nSUCCESS: All tests passed!")

def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="Run isolation tests for microservices")
    parser.add_argument(
        "--services", 
        nargs="+", 
        help="Specific services to test (default: all)"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Verbose output"
    )
    parser.add_argument(
        "--coverage", "-c", 
        action="store_true", 
        help="Generate coverage report"
    )
    parser.add_argument(
        "--output", "-o", 
        help="Output file for test results (JSON)"
    )
    
    args = parser.parse_args()
    
    # Create reports directory
    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Run tests
    runner = TestRunner(verbose=args.verbose, coverage=args.coverage)
    results = runner.run_tests(args.services)
    
    # Save results to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {args.output}")

if __name__ == "__main__":
    main()

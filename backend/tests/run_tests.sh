#!/bin/bash

# Microservices Isolation Test Runner
# This script provides an easy way to run isolation tests for all microservices

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
VERBOSE=false
COVERAGE=false
SERVICES=""
OUTPUT=""
DOCKER=false
CLEAN=false

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help              Show this help message"
    echo "  -v, --verbose           Enable verbose output"
    echo "  -c, --coverage          Generate coverage report"
    echo "  -s, --services LIST     Comma-separated list of services to test"
    echo "  -o, --output FILE       Output file for test results (JSON)"
    echo "  -d, --docker            Run tests in Docker"
    echo "  --clean                 Clean up test artifacts before running"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Run all tests"
    echo "  $0 -v -c                             # Run with verbose output and coverage"
    echo "  $0 -s orchestrator,analytics         # Test specific services"
    echo "  $0 -d                                # Run in Docker"
    echo "  $0 --clean -v -c                    # Clean and run with verbose output and coverage"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is required but not installed"
        exit 1
    fi
    
    # Check if we're in the right directory
    if [ ! -f "run_isolation_tests.py" ]; then
        print_error "Please run this script from the backend/tests directory"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing test dependencies..."
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found"
        exit 1
    fi
    
    pip3 install -r requirements.txt --quiet
    print_success "Dependencies installed"
}

# Function to clean test artifacts
clean_artifacts() {
    print_status "Cleaning test artifacts..."
    
    # Remove old reports
    rm -rf reports/
    rm -rf htmlcov/
    rm -rf .pytest_cache/
    rm -rf __pycache__/
    rm -rf .coverage
    
    # Remove old test files
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    print_success "Test artifacts cleaned"
}

# Function to run tests locally
run_tests_local() {
    print_status "Running tests locally..."
    
    # Build command
    cmd="python3 run_isolation_tests.py"
    
    if [ "$VERBOSE" = true ]; then
        cmd="$cmd --verbose"
    fi
    
    if [ "$COVERAGE" = true ]; then
        cmd="$cmd --coverage"
    fi
    
    if [ -n "$SERVICES" ]; then
        cmd="$cmd --services $SERVICES"
    fi
    
    if [ -n "$OUTPUT" ]; then
        cmd="$cmd --output $OUTPUT"
    fi
    
    # Run the command
    print_status "Executing: $cmd"
    eval $cmd
    
    if [ $? -eq 0 ]; then
        print_success "All tests passed!"
    else
        print_error "Some tests failed"
        exit 1
    fi
}

# Function to run tests in Docker
run_tests_docker() {
    print_status "Running tests in Docker..."
    
    # Check if Docker is available
    if ! command -v docker &> /dev/null; then
        print_error "Docker is required but not installed"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is required but not installed"
        exit 1
    fi
    
    # Build and run tests
    print_status "Building Docker image and running tests..."
    
    # Create reports directory
    mkdir -p reports htmlcov
    
    # Run with docker-compose
    if [ -n "$SERVICES" ]; then
        # Convert comma-separated list to space-separated
        services_list=$(echo $SERVICES | tr ',' ' ')
        docker-compose -f docker-compose.test.yml run --rm test-runner python3 run_isolation_tests.py --services $services_list
    else
        docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
    fi
    
    if [ $? -eq 0 ]; then
        print_success "All tests passed in Docker!"
    else
        print_error "Some tests failed in Docker"
        exit 1
    fi
}

# Function to show test results
show_results() {
    if [ -d "reports" ] && [ "$(ls -A reports)" ]; then
        print_status "Test results available in reports/ directory"
        
        if [ -f "reports/full_report.json" ]; then
            print_status "Full report: reports/full_report.json"
        fi
        
        # List individual service reports
        for report in reports/*_report.json; do
            if [ -f "$report" ]; then
                service_name=$(basename "$report" _report.json)
                print_status "Service report: $report"
            fi
        done
    fi
    
    if [ -d "htmlcov" ] && [ "$(ls -A htmlcov)" ]; then
        print_status "Coverage report available in htmlcov/ directory"
        print_status "Open htmlcov/index.html in your browser to view coverage"
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -s|--services)
            SERVICES="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT="$2"
            shift 2
            ;;
        -d|--docker)
            DOCKER=true
            shift
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Main execution
main() {
    echo "Microservices Isolation Test Runner"
    echo "===================================="
    
    # Check prerequisites
    check_prerequisites
    
    # Clean artifacts if requested
    if [ "$CLEAN" = true ]; then
        clean_artifacts
    fi
    
    # Install dependencies if not using Docker
    if [ "$DOCKER" = false ]; then
        install_dependencies
    fi
    
    # Run tests
    if [ "$DOCKER" = true ]; then
        run_tests_docker
    else
        run_tests_local
    fi
    
    # Show results
    show_results
    
    print_success "Test execution completed!"
}

# Run main function
main

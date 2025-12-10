# Microservices Isolation Testing Framework

This directory contains comprehensive isolation tests for all microservices in the backend. The tests verify that each service works correctly in isolation by mocking external dependencies.

## 🏗️ Architecture

The testing framework includes:

- **Isolation Tests**: Each service is tested independently with mocked dependencies
- **Mock Services**: Simulated external services (databases, APIs, etc.)
- **Test Fixtures**: Reusable test data and configurations
- **Coverage Reporting**: Code coverage analysis for each service
- **Performance Testing**: Basic performance benchmarks

## 📁 Structure

```
tests/
├── conftest.py                    # Shared test configuration and fixtures
├── test_orchestrator_isolation.py # Orchestrator service tests
├── test_analytics_isolation.py    # Analytics service tests
├── test_llm_isolation.py          # LLM service tests
├── test_rag_isolation.py          # RAG service tests
├── test_sentiment_isolation.py    # Sentiment service tests
├── test_stt_isolation.py          # STT service tests
├── test_tts_isolation.py          # TTS service tests
├── run_isolation_tests.py         # Test runner script
├── requirements.txt               # Testing dependencies
├── pytest.ini                    # Pytest configuration
├── Dockerfile.test               # Docker image for testing
├── docker-compose.test.yml       # Test environment setup
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional)
- pip

### Local Testing

1. **Install dependencies**:
   ```bash
   cd backend/tests
   pip install -r requirements.txt
   ```

2. **Run all isolation tests**:
   ```bash
   python run_isolation_tests.py
   ```

3. **Run tests for specific services**:
   ```bash
   python run_isolation_tests.py --services orchestrator analytics
   ```

4. **Run with coverage**:
   ```bash
   python run_isolation_tests.py --coverage
   ```

5. **Run with verbose output**:
   ```bash
   python run_isolation_tests.py --verbose
   ```

### Docker Testing

1. **Run tests in Docker**:
   ```bash
   cd backend/tests
   docker-compose -f docker-compose.test.yml up --build
   ```

2. **Run specific service tests**:
   ```bash
   docker-compose -f docker-compose.test.yml run test-runner python run_isolation_tests.py --services orchestrator
   ```

## 🧪 Test Categories

### 1. Orchestrator Service Tests
- Health endpoint functionality
- Chat endpoints (sync and streaming)
- RAG integration (mocked)
- LLM integration (mocked)
- Analytics integration (mocked)
- Authentication and authorization
- Error handling and fallbacks

### 2. Analytics Service Tests
- Event ingestion and storage
- Summary computation
- Report generation with performance grades
- ClickHouse integration (mocked)
- Data validation and error handling
- Performance metrics calculation

### 3. LLM Service Tests
- Text generation with primary provider
- Fallback provider functionality
- Error handling and retries
- Provider switching logic
- Response validation
- Performance metrics

### 4. RAG Service Tests
- Document retrieval
- Document ingestion
- Qdrant integration (mocked)
- MinIO integration (mocked)
- Embedding generation (mocked)
- Search result ranking

### 5. Sentiment Service Tests
- Text sentiment analysis
- Emotion classification
- Audio tone analysis (if supported)
- Multilingual text handling
- Confidence score validation
- Model loading and initialization

### 6. STT Service Tests
- Audio transcription
- Multiple audio formats
- Language detection
- Confidence scoring
- Word-level timestamps
- Error handling for corrupted audio

### 7. TTS Service Tests
- Text-to-speech synthesis
- Multiple voice options
- Speed and pitch control
- Audio format selection
- SSML support (if available)
- Performance optimization

## 🔧 Configuration

### Environment Variables

The tests use the following environment variables (automatically set in test fixtures):

```bash
# Service URLs
RAG_URL=http://localhost:8011
LLM_URL=http://localhost:8012
ANALYTICS_URL=http://localhost:8090
SENTIMENT_URL=http://localhost:8013
STT_URL=http://localhost:8014
TTS_URL=http://localhost:8015
FEEDBACK_URL=http://localhost:8016

# Database connections
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=9000
CLICKHOUSE_DB=test_analytics
REDIS_URL=redis://localhost:6379
POSTGRES_URL=postgresql://test:test@localhost:5432/test
QDRANT_URL=http://localhost:6333
MINIO_URL=http://localhost:9000

# Authentication
AUTH_TOKEN=test-token
```

### Test Data

The framework includes sample data for testing:

- **Sample Events**: Analytics events for testing ingestion
- **Sample RAG Responses**: Document retrieval results
- **Sample LLM Responses**: Text generation outputs
- **Sample Audio Data**: Mock audio files for STT/TTS testing

## 📊 Coverage and Reporting

### Coverage Reports

Coverage reports are generated in HTML format:

```bash
# Generate coverage report
python run_isolation_tests.py --coverage

# View coverage report
open htmlcov/index.html
```

### Test Reports

JSON test reports are saved to the `reports/` directory:

```bash
# Generate detailed report
python run_isolation_tests.py --output reports/detailed_report.json
```

### Performance Metrics

Basic performance metrics are collected:

- Test execution time
- Service response times
- Memory usage (if available)
- Concurrent request handling

## 🐛 Debugging

### Verbose Output

Enable verbose output to see detailed test execution:

```bash
python run_isolation_tests.py --verbose
```

### Individual Test Execution

Run specific test methods:

```bash
# Run specific test
pytest test_orchestrator_isolation.py::TestOrchestratorIsolation::test_health_endpoint -v

# Run with debugging
pytest test_orchestrator_isolation.py -v -s --pdb
```

### Mock Debugging

Check mock interactions:

```python
# In test files, add debug prints
print(f"Mock calls: {mock_function.call_args_list}")
```

## 🔄 CI/CD Integration

### GitHub Actions

Add to your `.github/workflows/test.yml`:

```yaml
name: Isolation Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend/tests
          pip install -r requirements.txt
      - name: Run isolation tests
        run: |
          cd backend/tests
          python run_isolation_tests.py --coverage --output reports/ci_report.json
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: backend/tests/htmlcov/coverage.xml
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'cd backend/tests && python run_isolation_tests.py --coverage'
            }
        }
    }
    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'backend/tests/htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
        }
    }
}
```

## 📈 Best Practices

### Writing Tests

1. **Isolation**: Each test should be independent
2. **Mocking**: Mock all external dependencies
3. **Data**: Use realistic test data
4. **Assertions**: Test both success and failure cases
5. **Performance**: Include basic performance checks

### Test Organization

1. **Group by service**: One test file per service
2. **Group by functionality**: Group related tests in classes
3. **Descriptive names**: Use clear, descriptive test names
4. **Documentation**: Add docstrings to test methods

### Maintenance

1. **Regular updates**: Update tests when services change
2. **Coverage monitoring**: Maintain high test coverage
3. **Performance tracking**: Monitor test execution times
4. **Dependency updates**: Keep testing dependencies current

## 🆘 Troubleshooting

### Common Issues

1. **Import errors**: Check Python path and module structure
2. **Mock failures**: Verify mock configurations
3. **Timeout errors**: Increase timeout values in pytest.ini
4. **Memory issues**: Reduce test data size or use smaller datasets

### Getting Help

1. Check test output for specific error messages
2. Run individual tests to isolate issues
3. Use verbose mode for detailed output
4. Check mock configurations and return values

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Mocking in Python](https://docs.python.org/3/library/unittest.mock.html)
- [Test Coverage](https://coverage.readthedocs.io/)

## 🤝 Contributing

When adding new tests:

1. Follow the existing naming conventions
2. Add appropriate docstrings
3. Include both positive and negative test cases
4. Update this README if adding new features
5. Ensure tests pass before submitting

## 📄 License

This testing framework is part of the microservices project and follows the same license terms.

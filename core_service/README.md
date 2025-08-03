# Orchestrator Agent

A central coordination service that automates the testing and evaluation of AI agents through a three-stage pipeline: prompt optimization, agent testing, and response scoring. It provides a standardized framework for assessing agent performance across multiple criteria.

## Features

- **Agent Registration**: Register and validate AI agents for testing
- **Prompt Optimization**: Automatically optimize prompts using the prompt optimizer service
- **Agent Testing**: Execute tests against AI agents with optimized prompts
- **Response Scoring**: Score agent responses using the scoring service
- **Batch Testing**: Execute multiple tests in parallel
- **Health Monitoring**: Monitor the health of all services and agents

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Orchestrator  │────│ Prompt Optimizer │────│   Score Agent   │
│     Agent       │    │   (Port 8001)    │    │  (Port 8000)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │
         │
┌─────────────────┐
│  Agent Under    │
│     Test        │
└─────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.9+
- Prompt Optimizer Service running on port 8001
- Scoring Service running on port 8000

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd core_service
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the services:
```bash
# Edit config.yaml or set environment variables
export OPTIMIZER_URL="http://localhost:8001"
export SCORER_URL="http://localhost:8000"
```

4. Run the service:
```bash
python main.py
```

The service will be available at `http://localhost:8003`

## API Endpoints

### Health Check
```http
GET /health
```

### Register Agent
```http
POST /register-agent
Content-Type: application/json

{
  "agent_endpoint": "http://localhost:3000",
  "agent_description": "A helpful AI assistant",
  "system_prompt": "You are a helpful assistant",
  "skills_and_tools": ["web_search", "calculator"],
  "test_criteria": ["accuracy", "relevance", "clarity", "completeness"],
  "scoring_threshold": 6.0
}
```

### Test Agent
```http
POST /test-agent
Content-Type: application/json

{
  "agent_endpoint": "http://localhost:3000",
  "test_prompt": "What is the capital of France?",
  "test_criteria": ["accuracy", "relevance", "clarity"],
  "scoring_threshold": 6.0,
  "optimization_context": {
    "language": "English",
    "complexity": "basic"
  }
}
```

### Batch Testing
```http
POST /test-batch
Content-Type: application/json

{
  "tests": [
    {
      "agent_endpoint": "http://localhost:3000",
      "test_prompt": "What is the capital of France?",
      "test_criteria": ["accuracy", "relevance"]
    },
    {
      "agent_endpoint": "http://localhost:3000",
      "test_prompt": "Explain quantum computing",
      "test_criteria": ["accuracy", "clarity", "completeness"]
    }
  ],
  "parallel_execution": true
}
```

### Health Check Agent
```http
POST /health-check-agent
Content-Type: application/json

{
  "agent_endpoint": "http://localhost:3000"
}
```

## Configuration

The service can be configured via `config.yaml` or environment variables:

### Environment Variables

- `ORCHESTRATOR_HOST`: Host to bind to (default: 0.0.0.0)
- `ORCHESTRATOR_PORT`: Port to bind to (default: 8002)
- `ORCHESTRATOR_TIMEOUT`: Default timeout in seconds (default: 30)
- `MAX_CONCURRENT_TESTS`: Maximum concurrent tests (default: 100)
- `OPTIMIZER_URL`: Prompt optimizer service URL (default: http://localhost:8001)
- `OPTIMIZER_TIMEOUT`: Optimizer service timeout (default: 15)
- `SCORER_URL`: Scoring service URL (default: http://localhost:8000)
- `SCORER_TIMEOUT`: Scoring service timeout (default: 20)
- `DEFAULT_SCORING_THRESHOLD`: Default scoring threshold (default: 6.0)
- `DEFAULT_SCORING_CRITERIA`: Default scoring criteria (default: accuracy,relevance,clarity,completeness)
- `LOG_LEVEL`: Logging level (default: INFO)

### Configuration File

```yaml
orchestrator:
  host: "0.0.0.0"
  port: 8002
  timeout: 30
  max_concurrent_tests: 100

services:
  optimizer:
    url: "http://localhost:8001"
    timeout: 15
  scorer:
    url: "http://localhost:8000"
    timeout: 20

scoring:
  default_threshold: 6.0
  criteria: ["accuracy", "relevance", "clarity", "completeness"]

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## Testing Workflow

1. **Agent Registration**: Register an agent with its endpoint and capabilities
2. **Prompt Optimization**: The orchestrator sends the test prompt to the prompt optimizer service
3. **Agent Testing**: The optimized prompt is sent to the target agent
4. **Response Scoring**: The agent's response is sent to the scoring service
5. **Result Processing**: The orchestrator processes the scores and determines pass/fail status

## Response Format

### Test Execution Response
```json
{
  "test_id": "uuid",
  "agent_endpoint": "http://localhost:3000",
  "test_status": "passed",
  "overall_score": 7.5,
  "criteria_scores": {
    "accuracy": 8.0,
    "relevance": 7.0,
    "clarity": 7.5,
    "completeness": 7.0
  },
  "test_result": {
    "status": "passed",
    "description": "Test passed with score 7.50",
    "reasoning": "The response accurately answered the question..."
  },
  "original_prompt": "What is the capital of France?",
  "optimized_prompt": "Please provide a clear and accurate answer: What is the capital of France?",
  "agent_response": "The capital of France is Paris.",
  "timestamp": "2024-01-01T12:00:00Z",
  "processing_time_ms": 2500
}
```

## Development

### Project Structure
```
core_service/
├── app/
│   ├── core/
│   │   └── orchestrator.py
│   ├── models/
│   │   ├── request_models.py
│   │   └── response_models.py
│   ├── services/
│   │   ├── agent_testing_service.py
│   │   ├── prompt_optimizer_service.py
│   │   └── scoring_service.py
│   └── utils/
│       ├── error_handlers.py
│       └── logging_config.py
├── config.yaml
├── main.py
├── requirements.txt
└── README.md
```

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## Monitoring

The service provides several monitoring endpoints:

- `/health`: Overall system health
- `/config`: Current configuration
- `/api-info`: API information and documentation links

## Error Handling

The service includes comprehensive error handling:

- Retry logic for external service calls
- Circuit breaker patterns for service failures
- Detailed error responses with timestamps
- Graceful degradation when services are unavailable

## Performance

- Supports up to 100 concurrent tests (configurable)
- Average processing time: < 25 seconds
- Response time: < 30 seconds for complete testing cycle
- Availability target: 99.5% uptime

## Security

- API key authentication (to be implemented)
- Request validation and sanitization
- CORS configuration
- Comprehensive audit logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For support and questions:
- Email: support@example.com
- Documentation: `/docs` endpoint when service is running
- Issues: GitHub Issues 
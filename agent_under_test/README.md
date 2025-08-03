# BDD Scenario Generator AI Agent

An AI-powered agent that automatically generates Behavior-Driven Development (BDD) scenarios from natural language requirements. This tool transforms business requirements into structured Given-When-Then scenarios, enabling faster test automation and improved collaboration between business stakeholders and development teams.

## Features

- **Natural Language Processing**: Analyzes requirements using NLP to extract key entities, actions, and conditions
- **BDD Scenario Generation**: Converts requirements into proper Given-When-Then format
- **Multiple Output Formats**: Supports Gherkin syntax, JSON, and plain text outputs
- **Quality Validation**: Ensures generated scenarios meet BDD best practices
- **Negative Scenario Generation**: Automatically creates error path scenarios
- **Examples Tables**: Generates scenario outlines with example data
- **RESTful API**: Easy integration with existing tools and workflows

## Quick Start

### Prerequisites

- Python 3.9+
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agent_under_test
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Run the application**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8003
   ```

### Using Docker

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually**
   ```bash
   docker build -t bdd-ai-agent .
   docker run -p 8003:8003 bdd-ai-agent
   ```

## API Usage

### Generate BDD Scenarios

**Endpoint:** `POST /bdd-from-text`

**Request Body:**
```json
{
  "requirements": "As a user, I should be able to log into the system. When I enter valid credentials, the system should authenticate me and redirect me to the dashboard.",
  "options": {
    "include_negative_scenarios": true,
    "output_format": "both",
    "max_scenarios_per_requirement": 5,
    "include_examples": true
  },
  "metadata": {
    "feature_name": "User Authentication",
    "project_id": "PROJ-001",
    "author": "John Doe"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "scenarios": [
    {
      "feature": "User Login Feature",
      "scenario": "User Login Successfully",
      "given": [
        "the user is logged into the system",
        "the user has appropriate permissions"
      ],
      "when": [
        "the user enters valid credentials"
      ],
      "then": [
        "the system should authenticate the user",
        "the user should be redirected to the dashboard"
      ],
      "examples": [
        {
          "user_type": "admin",
          "action_parameter": "item1",
          "expected_result": "success"
        }
      ],
      "gherkin": "Feature: User Login Feature\n\n  Scenario: User Login Successfully\n    Given the user is logged into the system\n    Given the user has appropriate permissions\n    When the user enters valid credentials\n    Then the system should authenticate the user\n    Then the user should be redirected to the dashboard"
    }
  ],
  "metadata": {
    "processing_time_ms": 1250.5,
    "scenarios_generated": 3,
    "quality_score": 0.85,
    "timestamp": "2025-01-27T10:30:00.000Z"
  },
  "warnings": [],
  "errors": []
}
```

### Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-27T10:30:00.000Z",
  "version": "1.0.0",
  "model_loaded": true
}
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `include_negative_scenarios` | boolean | true | Generate negative (error path) scenarios |
| `output_format` | string | "both" | Output format: "gherkin", "json", or "both" |
| `max_scenarios_per_requirement` | integer | 5 | Maximum scenarios to generate per requirement |
| `include_examples` | boolean | true | Include examples tables in scenarios |

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run specific test categories:

```bash
# Unit tests
pytest tests/test_bdd_generator.py::TestBDDGenerator -v

# Validation tests
pytest tests/test_bdd_generator.py::TestValidators -v

# Formatter tests
pytest tests/test_bdd_generator.py::TestFormatters -v
```

## Architecture

The application follows a modular architecture:

```
app/
├── main.py              # FastAPI application and endpoints
├── models/
│   └── bdd_generator.py # Core BDD generation logic
└── utils/
    ├── validators.py    # Input validation utilities
    └── formatters.py    # Output formatting utilities
```

### Key Components

1. **BDDGenerator**: Core AI model that analyzes requirements and generates scenarios
2. **Validators**: Input validation and sanitization
3. **Formatters**: Convert scenarios to Gherkin, JSON, and other formats
4. **API Layer**: FastAPI-based RESTful interface

## Performance

- **Response Time**: < 5 seconds for typical requirements (< 1000 words)
- **Throughput**: Handles 100+ concurrent requests
- **Memory Usage**: ~2GB RAM recommended
- **CPU**: 4+ cores recommended

## Security

- Input validation and sanitization
- Rate limiting support
- No persistent storage of user data
- HTTPS encryption recommended for production

## Monitoring

The application provides health checks and metrics:

- `/health` - Detailed health status
- `/` - Basic service information
- Built-in logging for request/response tracking

## Development

### Local Development

1. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-asyncio
   ```

3. **Run in development mode**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8003
   ```

### Code Style

The project follows PEP 8 guidelines. Use a linter:

```bash
pip install flake8 black
flake8 app/ tests/
black app/ tests/
```

## Deployment

### Production Deployment

1. **Environment Variables**
   ```bash
   export LOG_LEVEL=INFO
   export PYTHONPATH=/app
   ```

2. **Using Docker Compose**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

3. **Using Kubernetes**
   ```bash
   kubectl apply -f k8s/
   ```

### Monitoring and Logging

- Application logs are available via Docker logs
- Health checks are configured for container orchestration
- Metrics can be exposed via Prometheus endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information
4. Include logs and error messages

## Roadmap

- [ ] Enhanced NLP models for better entity extraction
- [ ] Support for multiple languages
- [ ] Integration with popular test frameworks
- [ ] Web-based UI for non-technical users
- [ ] Batch processing for multiple requirements
- [ ] Custom scenario templates
- [ ] Integration with CI/CD pipelines 
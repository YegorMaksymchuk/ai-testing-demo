# AI Scoring Agent

A FastAPI-based service for scoring AI responses using OpenAI. This service provides both single and batch scoring capabilities with configurable criteria and comprehensive error handling.

## 🚀 Features

- **Single Response Scoring**: Score individual AI responses with detailed reasoning
- **Batch Processing**: Score multiple responses concurrently with progress tracking
- **Configurable Criteria**: Support for multiple scoring criteria (accuracy, relevance, clarity, completeness, coherence)
- **Rate Limiting**: Built-in rate limiting to respect OpenAI API limits
- **Error Handling**: Comprehensive error handling with retry logic
- **Health Monitoring**: Health check endpoints for monitoring
- **Docker Support**: Full containerization with Docker and docker-compose
- **Testing**: Comprehensive test suite with unit and integration tests

## 📋 Prerequisites

- Python 3.11+
- OpenAI API key
- Docker (optional, for containerized deployment)

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-scoring-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t ai-scoring-agent:latest .
   ```

2. **Run with Docker**
   ```bash
   docker run -d \
     --name scoring-agent \
     -p 8000:8000 \
     -e OPENAI_API_KEY=your_api_key_here \
     ai-scoring-agent:latest
   ```

3. **Run with docker-compose**
   ```bash
   # Set environment variables in .env file first
   docker-compose up -d
   ```

## 🔧 Configuration

The application can be configured using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4` | OpenAI model to use |
| `OPENAI_MAX_TOKENS` | `2000` | Maximum tokens for OpenAI response |
| `OPENAI_TEMPERATURE` | `0.0` | Temperature for OpenAI response |
| `LOG_LEVEL` | `INFO` | Logging level |
| `HOST` | `0.0.0.0` | Host to bind to |
| `PORT` | `8000` | Port to bind to |
| `DEFAULT_SCORING_CRITERIA` | `accuracy,relevance,clarity` | Default scoring criteria |
| `SCORING_SCALE` | `1-10` | Scoring scale |
| `MAX_BATCH_SIZE` | `100` | Maximum batch size |
| `RATE_LIMIT_PER_MINUTE` | `60` | Rate limit per minute |

## 📚 API Documentation

The API provides comprehensive documentation through multiple interfaces:

### Interactive Documentation
- **Swagger UI**: Visit `/docs` for interactive API documentation with testing interface
- **ReDoc**: Visit `/redoc` for alternative API documentation with better readability
- **Landing Page**: Visit `/landing` for a beautiful landing page with links to all documentation

### OpenAPI Specification
- **JSON Format**: `/openapi.json` - Raw OpenAPI specification in JSON format
- **YAML Format**: `/openapi.yaml` - Raw OpenAPI specification in YAML format
- **API Info**: `/api-info` - API information and links

### Endpoints

#### `GET /`
Root endpoint returning basic service information.

#### `GET /health`
Health check endpoint for monitoring.

#### `GET /config`
Get current configuration settings.

#### `GET /api-info`
Get API information and documentation links.

#### `GET /openapi.yaml`
Get OpenAPI specification in YAML format.

#### `POST /score`
Score a single AI response.

**Request Body:**
```json
{
  "response": "The AI response to evaluate",
  "criteria": ["accuracy", "relevance", "clarity"],
  "context": "Additional context for scoring"
}
```

**Response:**
```json
{
  "score": 8.5,
  "reasoning": "Detailed explanation of the score",
  "criteria_scores": {
    "accuracy": 9.0,
    "relevance": 8.0,
    "clarity": 8.5
  },
  "confidence": 0.9,
  "model_used": "gpt-4",
  "timestamp": "2024-01-01T12:00:00Z",
  "processing_time_ms": 1500.0
}
```

#### `POST /score/batch`
Score multiple AI responses in batch.

**Request Body:**
```json
{
  "responses": [
    "First AI response",
    "Second AI response",
    "Third AI response"
  ],
  "criteria": ["accuracy", "relevance"],
  "context": "Additional context for scoring"
}
```

**Response:**
```json
{
  "results": [
    {
      "response": "First AI response",
      "score": 8.0,
      "reasoning": "Good response",
      "criteria_scores": {"accuracy": 8.5},
      "confidence": 0.8
    }
  ],
  "total_processed": 3,
  "successful": 3,
  "failed": 0,
  "model_used": "gpt-4",
  "timestamp": "2024-01-01T12:00:00Z",
  "total_processing_time_ms": 4500.0,
  "average_processing_time_ms": 1500.0
}
```

## 🧪 Testing

### Run all tests
```bash
pytest
```

### Run specific test files
```bash
pytest tests/test_scoring_service.py
pytest tests/test_api_endpoints.py
```

### Run with coverage
```bash
pytest --cov=. --cov-report=html
```

## 📊 Usage Examples

### Python Client Example

```python
import requests
import json

# Single scoring
response = requests.post(
    "http://localhost:8000/score",
    json={
        "response": "The capital of France is Paris.",
        "criteria": ["accuracy", "relevance"],
        "context": "Question: What is the capital of France?"
    }
)

result = response.json()
print(f"Score: {result['score']}")
print(f"Reasoning: {result['reasoning']}")

# Batch scoring
batch_response = requests.post(
    "http://localhost:8000/score/batch",
    json={
        "responses": [
            "The capital of France is Paris.",
            "The capital of France is London.",
            "Paris is the capital of France."
        ],
        "criteria": ["accuracy", "relevance"]
    }
)

batch_result = batch_response.json()
for i, result in enumerate(batch_result['results']):
    print(f"Response {i+1}: Score {result['score']}")
```

### cURL Examples

```bash
# Single scoring
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "The capital of France is Paris.",
    "criteria": ["accuracy", "relevance"],
    "context": "Question: What is the capital of France?"
  }'

# Batch scoring
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      "The capital of France is Paris.",
      "The capital of France is London.",
      "Paris is the capital of France."
    ],
    "criteria": ["accuracy", "relevance", "clarity"],
    "context": "Question: What is the capital of France?"
  }'
```

For more comprehensive cURL examples, see `examples/curl_examples.md`.

### Test Scripts
- `examples/test_single_scoring.sh` - Bash script to test single scoring
- `examples/test_single_scoring.py` - Python script to test single scoring
- `examples/test_batch_scoring.sh` - Bash script to test batch scoring
- `examples/test_batch_scoring.py` - Python script to test batch scoring

## 🔍 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Configuration
```bash
curl http://localhost:8000/config
```

### API Information
```bash
curl http://localhost:8000/api-info
```

### OpenAPI Specification
```bash
# JSON format
curl http://localhost:8000/openapi.json

# YAML format
curl http://localhost:8000/openapi.yaml
```

## 🐳 Docker Commands

### Build and run
```bash
# Build image
docker build -t ai-scoring-agent:latest .

# Run container
docker run -d \
  --name scoring-agent \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key_here \
  ai-scoring-agent:latest

# View logs
docker logs scoring-agent

# Stop container
docker stop scoring-agent
```

### Access Documentation
Once the container is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Landing Page**: http://localhost:8000/landing
- **OpenAPI JSON**: http://localhost:8000/openapi.json
- **OpenAPI YAML**: http://localhost:8000/openapi.yaml

### Development with volume mounting
```bash
docker run -d \
  --name scoring-agent-dev \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key_here \
  -v $(pwd):/app \
  ai-scoring-agent:latest
```

## 📝 Logging

Logs are written to both console and file:
- Console: Standard output
- File: `logs/app_YYYYMMDD.log`

Log levels can be configured via the `LOG_LEVEL` environment variable.

## 🔒 Security

- Non-root user in Docker container
- Environment variable configuration
- Input validation and sanitization
- Rate limiting to prevent abuse
- CORS configuration for web access

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## 🚀 Performance Tips

- Use batch scoring for multiple responses
- Configure appropriate rate limits
- Monitor processing times
- Use appropriate OpenAI models for your use case
- Consider caching for repeated evaluations 
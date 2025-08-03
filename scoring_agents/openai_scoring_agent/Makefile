.PHONY: help install test run clean docker-build docker-run docker-stop lint format

# Default target
help:
	@echo "🤖 AI Scoring Agent - Available Commands"
	@echo "========================================"
	@echo "install     - Install dependencies"
	@echo "test        - Run tests"
	@echo "run         - Run the application"
	@echo "clean       - Clean up generated files"
	@echo "docker-build- Build Docker image"
	@echo "docker-run  - Run with Docker"
	@echo "docker-stop - Stop Docker container"
	@echo "lint        - Run linting"
	@echo "format      - Format code"
	@echo "help        - Show this help"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest

# Run tests with coverage
test-cov:
	@echo "🧪 Running tests with coverage..."
	pytest --cov=. --cov-report=html --cov-report=term-missing

# Run the application
run:
	@echo "🚀 Starting AI Scoring Agent..."
	python run.py

# Clean up generated files
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf logs/*.log

# Build Docker image
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t ai-scoring-agent:latest .

# Run with Docker
docker-run:
	@echo "🐳 Running with Docker..."
	docker run -d \
		--name scoring-agent \
		-p 8000:8000 \
		-e OPENAI_API_KEY=$${OPENAI_API_KEY} \
		ai-scoring-agent:latest

# Stop Docker container
docker-stop:
	@echo "🐳 Stopping Docker container..."
	docker stop scoring-agent || true
	docker rm scoring-agent || true

# Run with docker-compose
docker-compose-up:
	@echo "🐳 Starting with docker-compose..."
	docker-compose up -d

# Stop docker-compose
docker-compose-down:
	@echo "🐳 Stopping docker-compose..."
	docker-compose down

# Run linting
lint:
	@echo "🔍 Running linting..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Format code
format:
	@echo "🎨 Formatting code..."
	black .
	isort .

# Check code quality
check:
	@echo "🔍 Checking code quality..."
	black --check .
	isort --check-only .
	flake8 .

# Setup development environment
setup-dev: install
	@echo "🔧 Setting up development environment..."
	pre-commit install

# Run example
example:
	@echo "📊 Running example..."
	python examples/example_usage.py

# Health check
health:
	@echo "🏥 Checking service health..."
	curl -f http://localhost:8000/health || echo "Service not running"

# Show logs
logs:
	@echo "📝 Showing logs..."
	tail -f logs/app_$(shell date +%Y%m%d).log

# Performance test
perf-test:
	@echo "⚡ Running performance test..."
	python -c "
import requests
import time
import json

responses = ['Response ' + str(i) for i in range(10)]
start_time = time.time()

result = requests.post('http://localhost:8000/score/batch', json={
    'responses': responses,
    'criteria': ['accuracy', 'relevance']
})

end_time = time.time()
print(f'Batch processing time: {(end_time - start_time) * 1000:.0f}ms')
print(f'Results: {result.json()}')
" 
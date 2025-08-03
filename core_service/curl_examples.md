# Orchestrator Agent - Curl Examples

## Health Check
```bash
curl -X GET http://localhost:8003/health
```

## Get Configuration
```bash
curl -X GET http://localhost:8003/config
```

## Register Agent
```bash
curl -X POST http://localhost:8003/register-agent \
  -H "Content-Type: application/json" \
  -d '{
    "agent_endpoint": "http://localhost:3000",
    "agent_description": "BDD Agent that creates BDD scenarios from text",
    "system_prompt": "You are a BDD agent that converts text descriptions into BDD (Behavior Driven Development) scenarios using Gherkin syntax.",
    "skills_and_tools": ["text_analysis", "gherkin_generation", "scenario_creation"],
    "test_criteria": ["accuracy", "relevance", "clarity", "completeness"],
    "scoring_threshold": 6.0
  }'
```

## Test Agent (Single Test)
```bash
curl -X POST http://localhost:8003/test-agent \
  -H "Content-Type: application/json" \
  -d '{
    "agent_endpoint": "http://localhost:3000",
    "test_prompt": "Create a BDD scenario for user login functionality",
    "test_criteria": ["accuracy", "relevance", "clarity", "completeness"],
    "scoring_threshold": 6.0,
    "optimization_context": {
      "language": "English",
      "complexity": "intermediate",
      "target_audience": "developers"
    }
  }'
```

## Batch Test
```bash
curl -X POST http://localhost:8003/test-batch \
  -H "Content-Type: application/json" \
  -d '{
    "tests": [
      {
        "agent_endpoint": "http://localhost:3000",
        "test_prompt": "Create a BDD scenario for user registration",
        "test_criteria": ["accuracy", "relevance", "clarity"],
        "scoring_threshold": 6.0
      },
      {
        "agent_endpoint": "http://localhost:3000",
        "test_prompt": "Create a BDD scenario for password reset",
        "test_criteria": ["accuracy", "relevance", "clarity"],
        "scoring_threshold": 6.0
      },
      {
        "agent_endpoint": "http://localhost:3000",
        "test_prompt": "Create a BDD scenario for shopping cart checkout",
        "test_criteria": ["accuracy", "relevance", "clarity"],
        "scoring_threshold": 6.0
      }
    ],
    "parallel_execution": true
  }'
```

## Health Check Agent
```bash
curl -X POST http://localhost:8003/health-check-agent \
  -H "Content-Type: application/json" \
  -d '{
    "agent_endpoint": "http://localhost:3000"
  }'
```

## Get API Info
```bash
curl -X GET http://localhost:8003/api-info
```

## BDD Agent Test Examples

### Test 1: User Login
```bash
curl -X POST http://localhost:8003/test-agent \
  -H "Content-Type: application/json" \
  -d '{
    "agent_endpoint": "http://localhost:3000",
    "test_prompt": "Create a BDD scenario for a user logging into an e-commerce website",
    "test_criteria": ["accuracy", "relevance", "clarity", "completeness"],
    "scoring_threshold": 6.0
  }'
```

### Test 2: Shopping Cart
```bash
curl -X POST http://localhost:8003/test-agent \
  -H "Content-Type: application/json" \
  -d '{
    "agent_endpoint": "http://localhost:3000",
    "test_prompt": "Create a BDD scenario for adding items to shopping cart",
    "test_criteria": ["accuracy", "relevance", "clarity", "completeness"],
    "scoring_threshold": 6.0
  }'
```

### Test 3: Payment Processing
```bash
curl -X POST http://localhost:8003/test-agent \
  -H "Content-Type: application/json" \
  -d '{
    "agent_endpoint": "http://localhost:3000",
    "test_prompt": "Create a BDD scenario for credit card payment processing",
    "test_criteria": ["accuracy", "relevance", "clarity", "completeness"],
    "scoring_threshold": 6.0
  }'
```

### Test 4: User Registration
```bash
curl -X POST http://localhost:8003/test-agent \
  -H "Content-Type: application/json" \
  -d '{
    "agent_endpoint": "http://localhost:3000",
    "test_prompt": "Create a BDD scenario for new user registration with email verification",
    "test_criteria": ["accuracy", "relevance", "clarity", "completeness"],
    "scoring_threshold": 6.0
  }'
```

### Test 5: Password Reset
```bash
curl -X POST http://localhost:8003/test-agent \
  -H "Content-Type: application/json" \
  -d '{
    "agent_endpoint": "http://localhost:3000",
    "test_prompt": "Create a BDD scenario for password reset functionality",
    "test_criteria": ["accuracy", "relevance", "clarity", "completeness"],
    "scoring_threshold": 6.0
  }'
``` 
# cURL Examples for AI Scoring Agent API

This document provides comprehensive cURL examples for the AI Scoring Agent API endpoints.

## Single Scoring Endpoint (`/score`)

### Basic Single Scoring

```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "The capital of France is Paris.",
    "criteria": ["accuracy", "relevance"],
    "context": "Question: What is the capital of France?"
  }'
```

### Comprehensive Single Scoring

```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "The capital of France is Paris, which is located in the northern part of the country and is known for landmarks like the Eiffel Tower.",
    "criteria": ["accuracy", "relevance", "clarity", "completeness", "coherence"],
    "context": "Question: What is the capital of France? Please provide a clear and detailed answer."
  }'
```

### Minimal Single Scoring (Default Criteria)

```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "Paris is the capital of France."
  }'
```

### Single Scoring with Custom Criteria Only

```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "The capital of France is Paris.",
    "criteria": ["accuracy", "relevance"]
  }'
```

### Single Scoring with Context Only

```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "The capital of France is Paris.",
    "context": "Question: What is the capital of France?"
  }'
```

### Error Handling Examples

#### Invalid Criteria
```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "The capital of France is Paris.",
    "criteria": ["invalid_criterion"]
  }'
```

#### Empty Response
```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "",
    "criteria": ["accuracy"]
  }'
```

#### Missing Response
```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "criteria": ["accuracy"]
  }'
```

### Testing Different Scenarios

#### Academic Question
```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen.",
    "criteria": ["accuracy", "relevance", "clarity"],
    "context": "Question: What is photosynthesis? Provide a scientific explanation."
  }'
```

#### Creative Writing
```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "The sunset painted the sky in brilliant hues of orange and pink, casting long shadows across the landscape.",
    "criteria": ["clarity", "coherence", "completeness"],
    "context": "Write a descriptive sentence about a sunset."
  }'
```

#### Technical Explanation
```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "REST APIs use HTTP methods like GET, POST, PUT, DELETE to perform CRUD operations on resources.",
    "criteria": ["accuracy", "relevance", "clarity", "completeness"],
    "context": "Explain what REST APIs are and how they work."
  }'
```

#### Mathematical Problem
```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "To solve 2x + 5 = 13, subtract 5 from both sides: 2x = 8, then divide by 2: x = 4.",
    "criteria": ["accuracy", "clarity"],
    "context": "Solve the equation: 2x + 5 = 13"
  }'
```

### Expected Response Format

#### Successful Response
```json
{
  "score": 8.5,
  "reasoning": "This is an accurate and relevant response that clearly answers the question about France's capital.",
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

#### Error Response
```json
{
  "error": "Validation Error",
  "detail": [
    {
      "loc": ["body", "criteria", 0],
      "msg": "value is not a valid enumeration member; permitted: 'accuracy', 'relevance', 'clarity', 'completeness', 'coherence'",
      "type": "enum"
    }
  ],
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Batch Scoring Endpoint (`/score/batch`)

### Basic Batch Scoring

```bash
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      "The capital of France is Paris.",
      "The capital of France is London.",
      "Paris is the capital of France."
    ],
    "criteria": ["accuracy", "relevance"],
    "context": "Question: What is the capital of France?"
  }'
```

### Comprehensive Batch Scoring

```bash
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      "The capital of France is Paris, which is located in the northern part of the country.",
      "The capital of France is London, which is a beautiful city.",
      "I don't know the capital of France.",
      "France's capital city is Paris, which is known for the Eiffel Tower and is located in the Île-de-France region.",
      "The capital of France is Berlin."
    ],
    "criteria": ["accuracy", "relevance", "clarity", "completeness", "coherence"],
    "context": "Question: What is the capital of France? Please provide a clear and accurate answer."
  }'
```

### Minimal Batch Scoring (Default Criteria)

```bash
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      "Paris is the capital of France.",
      "The capital is Paris.",
      "France's capital is Paris."
    ]
  }'
```

### Batch Scoring with Custom Criteria Only

```bash
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      "The capital of France is Paris.",
      "The capital of France is London.",
      "Paris is the capital of France."
    ],
    "criteria": ["accuracy", "relevance"]
  }'
```

### Large Batch Example

```bash
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      "The capital of France is Paris.",
      "The capital of France is London.",
      "Paris is the capital of France.",
      "France's capital city is Paris, located in the northern part of the country.",
      "I don't know the capital of France.",
      "The capital of France is Paris, which is known for the Eiffel Tower.",
      "France's capital is Paris, a beautiful city with rich history.",
      "The capital of France is Berlin.",
      "Paris is the capital and largest city of France.",
      "France's capital is Paris, situated in the Île-de-France region."
    ],
    "criteria": ["accuracy", "relevance", "clarity"],
    "context": "Question: What is the capital of France? Provide a clear and accurate answer."
  }'
```

### Error Handling Examples

#### Invalid Criteria
```bash
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": ["The capital of France is Paris."],
    "criteria": ["invalid_criterion"]
  }'
```

#### Empty Responses Array
```bash
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [],
    "criteria": ["accuracy"]
  }'
```

#### Batch Size Exceeded
```bash
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      "Response 1",
      "Response 2",
      "Response 3",
      "Response 4",
      "Response 5"
    ],
    "criteria": ["accuracy"]
  }'
```

## Expected Response Format

### Successful Response
```json
{
  "results": [
    {
      "response": "The capital of France is Paris.",
      "score": 9.0,
      "reasoning": "This is an accurate and relevant response that clearly answers the question about France's capital.",
      "criteria_scores": {
        "accuracy": 9.5,
        "relevance": 8.5,
        "clarity": 9.0
      },
      "confidence": 0.9
    },
    {
      "response": "The capital of France is London.",
      "score": 2.0,
      "reasoning": "This is an incorrect response - London is the capital of England, not France.",
      "criteria_scores": {
        "accuracy": 1.0,
        "relevance": 3.0,
        "clarity": 8.0
      },
      "confidence": 0.8
    }
  ],
  "total_processed": 2,
  "successful": 2,
  "failed": 0,
  "model_used": "gpt-4",
  "timestamp": "2024-01-01T12:00:00Z",
  "total_processing_time_ms": 3000.0,
  "average_processing_time_ms": 1500.0
}
```

### Error Response
```json
{
  "error": "Validation Error",
  "detail": [
    {
      "loc": ["body", "criteria", 0],
      "msg": "value is not a valid enumeration member; permitted: 'accuracy', 'relevance', 'clarity', 'completeness', 'coherence'",
      "type": "enum"
    }
  ],
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Available Scoring Criteria

- **accuracy**: How correct and factual is the response
- **relevance**: How well does it address the question/context
- **clarity**: How clear and well-structured is the response
- **completeness**: How comprehensive is the response
- **coherence**: How logical and coherent is the response

## Rate Limiting

The API implements rate limiting to respect OpenAI API limits. Default is 60 requests per minute. If you exceed this limit, you'll receive a rate limit error.

## Performance Tips

1. **Use batch scoring for multiple responses**: It's more efficient than individual requests
2. **Keep batch sizes reasonable**: Default max is 100 responses per batch
3. **Provide context**: Adding context helps improve scoring accuracy
4. **Specify criteria**: Be explicit about which criteria to evaluate

## Testing with Different Scenarios

### Academic Questions
```bash
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      "Photosynthesis is the process by which plants convert sunlight into energy.",
      "Photosynthesis is when plants make food from light.",
      "I think photosynthesis is about plants and sunlight."
    ],
    "criteria": ["accuracy", "relevance", "clarity"],
    "context": "Question: What is photosynthesis? Provide a scientific explanation."
  }'
```

### Creative Writing
```bash
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      "The sunset painted the sky in brilliant hues of orange and pink.",
      "The sun went down and it was pretty.",
      "The evening sky was illuminated by the setting sun."
    ],
    "criteria": ["clarity", "coherence", "completeness"],
    "context": "Write a descriptive sentence about a sunset."
  }'
```

### Technical Explanations
```bash
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      "REST APIs use HTTP methods like GET, POST, PUT, DELETE to perform CRUD operations.",
      "REST is a way to build web services.",
      "REST APIs are stateless and use standard HTTP methods for data manipulation."
    ],
    "criteria": ["accuracy", "relevance", "clarity", "completeness"],
    "context": "Explain what REST APIs are and how they work."
  }'
``` 
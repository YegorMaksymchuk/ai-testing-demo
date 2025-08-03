#!/bin/bash

# Test script for the AI Scoring Agent single scoring endpoint
# Make sure the service is running on localhost:8000

echo "🤖 Testing AI Scoring Agent Single Scoring Endpoint"
echo "=================================================="

# Test 1: Basic single scoring
echo -e "\n📝 Test 1: Basic single scoring"
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "The capital of France is Paris.",
    "criteria": ["accuracy", "relevance"],
    "context": "Question: What is the capital of France?"
  }' | jq '.'

# Test 2: Comprehensive scoring with all criteria
echo -e "\n📝 Test 2: Comprehensive scoring with all criteria"
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "The capital of France is Paris, which is located in the northern part of the country and is known for landmarks like the Eiffel Tower.",
    "criteria": ["accuracy", "relevance", "clarity", "completeness", "coherence"],
    "context": "Question: What is the capital of France? Please provide a clear and detailed answer."
  }' | jq '.'

# Test 3: Minimal request (default criteria)
echo -e "\n📝 Test 3: Minimal request (default criteria)"
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "Paris is the capital of France."
  }' | jq '.'

# Test 4: Academic question
echo -e "\n📝 Test 4: Academic question"
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen.",
    "criteria": ["accuracy", "relevance", "clarity"],
    "context": "Question: What is photosynthesis? Provide a scientific explanation."
  }' | jq '.'

# Test 5: Creative writing
echo -e "\n📝 Test 5: Creative writing"
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "The sunset painted the sky in brilliant hues of orange and pink, casting long shadows across the landscape.",
    "criteria": ["clarity", "coherence", "completeness"],
    "context": "Write a descriptive sentence about a sunset."
  }' | jq '.'

# Test 6: Technical explanation
echo -e "\n📝 Test 6: Technical explanation"
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "REST APIs use HTTP methods like GET, POST, PUT, DELETE to perform CRUD operations on resources.",
    "criteria": ["accuracy", "relevance", "clarity", "completeness"],
    "context": "Explain what REST APIs are and how they work."
  }' | jq '.'

# Test 7: Error handling - invalid criteria
echo -e "\n📝 Test 7: Error handling - invalid criteria"
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "The capital of France is Paris.",
    "criteria": ["invalid_criterion"]
  }' | jq '.'

# Test 8: Error handling - empty response
echo -e "\n📝 Test 8: Error handling - empty response"
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "",
    "criteria": ["accuracy"]
  }' | jq '.'

# Test 9: Error handling - missing response
echo -e "\n📝 Test 9: Error handling - missing response"
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "criteria": ["accuracy"]
  }' | jq '.'

# Test 10: Mathematical problem
echo -e "\n📝 Test 10: Mathematical problem"
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "To solve 2x + 5 = 13, subtract 5 from both sides: 2x = 8, then divide by 2: x = 4.",
    "criteria": ["accuracy", "clarity"],
    "context": "Solve the equation: 2x + 5 = 13"
  }' | jq '.'

echo -e "\n✅ Single scoring tests completed!"
echo "Check the responses above for results and error handling." 
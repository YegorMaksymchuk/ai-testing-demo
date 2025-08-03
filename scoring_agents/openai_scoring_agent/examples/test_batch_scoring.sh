#!/bin/bash

# Test script for the AI Scoring Agent batch endpoint
# Make sure the service is running on localhost:8000

echo "🤖 Testing AI Scoring Agent Batch Endpoint"
echo "=========================================="

# Test 1: Basic batch scoring
echo -e "\n📝 Test 1: Basic batch scoring"
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
  }' | jq '.'

# Test 2: Comprehensive scoring with all criteria
echo -e "\n📝 Test 2: Comprehensive scoring with all criteria"
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      "The capital of France is Paris, which is located in the northern part of the country.",
      "The capital of France is London, which is a beautiful city.",
      "I don't know the capital of France.",
      "France's capital city is Paris, which is known for the Eiffel Tower and is located in the Île-de-France region."
    ],
    "criteria": ["accuracy", "relevance", "clarity", "completeness", "coherence"],
    "context": "Question: What is the capital of France? Please provide a clear and accurate answer."
  }' | jq '.'

# Test 3: Minimal request (default criteria)
echo -e "\n📝 Test 3: Minimal request (default criteria)"
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      "Paris is the capital of France.",
      "The capital is Paris.",
      "France's capital is Paris."
    ]
  }' | jq '.'

# Test 4: Error handling - invalid criteria
echo -e "\n📝 Test 4: Error handling - invalid criteria"
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": ["The capital of France is Paris."],
    "criteria": ["invalid_criterion"]
  }' | jq '.'

# Test 5: Error handling - empty responses
echo -e "\n📝 Test 5: Error handling - empty responses"
curl -X POST "http://localhost:8000/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [],
    "criteria": ["accuracy"]
  }' | jq '.'

echo -e "\n✅ Batch scoring tests completed!"
echo "Check the responses above for results and error handling." 
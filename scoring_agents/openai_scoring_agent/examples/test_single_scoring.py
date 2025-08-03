#!/usr/bin/env python3
"""
Test script for the AI Scoring Agent single scoring endpoint.
Make sure the service is running on localhost:8000
"""

import requests
import json
import time
from typing import Dict, Any


def test_single_scoring():
    """Test the single scoring endpoint with various scenarios."""
    
    base_url = "http://localhost:8000"
    
    print("🤖 Testing AI Scoring Agent Single Scoring Endpoint")
    print("=" * 50)
    
    # Test 1: Basic single scoring
    print("\n📝 Test 1: Basic single scoring")
    test_data = {
        "response": "The capital of France is Paris.",
        "criteria": ["accuracy", "relevance"],
        "context": "Question: What is the capital of France?"
    }
    
    response = requests.post(f"{base_url}/score", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Score: {result['score']}/10")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Processing time: {result.get('processing_time_ms', 0):.0f}ms")
        if result.get('criteria_scores'):
            print("Criteria scores:")
            for criterion, score in result['criteria_scores'].items():
                print(f"  {criterion}: {score}/10")
    else:
        print(f"Error: {response.text}")
    
    # Test 2: Comprehensive scoring with all criteria
    print("\n📝 Test 2: Comprehensive scoring with all criteria")
    test_data = {
        "response": "The capital of France is Paris, which is located in the northern part of the country and is known for landmarks like the Eiffel Tower.",
        "criteria": ["accuracy", "relevance", "clarity", "completeness", "coherence"],
        "context": "Question: What is the capital of France? Please provide a clear and detailed answer."
    }
    
    response = requests.post(f"{base_url}/score", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Score: {result['score']}/10")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Processing time: {result.get('processing_time_ms', 0):.0f}ms")
        if result.get('criteria_scores'):
            print("Criteria scores:")
            for criterion, score in result['criteria_scores'].items():
                print(f"  {criterion}: {score}/10")
    else:
        print(f"Error: {response.text}")
    
    # Test 3: Minimal request (default criteria)
    print("\n📝 Test 3: Minimal request (default criteria)")
    test_data = {
        "response": "Paris is the capital of France."
    }
    
    response = requests.post(f"{base_url}/score", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Score: {result['score']}/10")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Processing time: {result.get('processing_time_ms', 0):.0f}ms")
    else:
        print(f"Error: {response.text}")
    
    # Test 4: Academic question
    print("\n📝 Test 4: Academic question")
    test_data = {
        "response": "Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen.",
        "criteria": ["accuracy", "relevance", "clarity"],
        "context": "Question: What is photosynthesis? Provide a scientific explanation."
    }
    
    response = requests.post(f"{base_url}/score", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Score: {result['score']}/10")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Processing time: {result.get('processing_time_ms', 0):.0f}ms")
    else:
        print(f"Error: {response.text}")
    
    # Test 5: Creative writing
    print("\n📝 Test 5: Creative writing")
    test_data = {
        "response": "The sunset painted the sky in brilliant hues of orange and pink, casting long shadows across the landscape.",
        "criteria": ["clarity", "coherence", "completeness"],
        "context": "Write a descriptive sentence about a sunset."
    }
    
    response = requests.post(f"{base_url}/score", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Score: {result['score']}/10")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Processing time: {result.get('processing_time_ms', 0):.0f}ms")
    else:
        print(f"Error: {response.text}")
    
    # Test 6: Technical explanation
    print("\n📝 Test 6: Technical explanation")
    test_data = {
        "response": "REST APIs use HTTP methods like GET, POST, PUT, DELETE to perform CRUD operations on resources.",
        "criteria": ["accuracy", "relevance", "clarity", "completeness"],
        "context": "Explain what REST APIs are and how they work."
    }
    
    response = requests.post(f"{base_url}/score", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Score: {result['score']}/10")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Processing time: {result.get('processing_time_ms', 0):.0f}ms")
    else:
        print(f"Error: {response.text}")
    
    # Test 7: Error handling - invalid criteria
    print("\n📝 Test 7: Error handling - invalid criteria")
    test_data = {
        "response": "The capital of France is Paris.",
        "criteria": ["invalid_criterion"]
    }
    
    response = requests.post(f"{base_url}/score", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Expected error: {response.text}")
    else:
        print("Unexpected success")
    
    # Test 8: Error handling - empty response
    print("\n📝 Test 8: Error handling - empty response")
    test_data = {
        "response": "",
        "criteria": ["accuracy"]
    }
    
    response = requests.post(f"{base_url}/score", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Expected error: {response.text}")
    else:
        print("Unexpected success")
    
    # Test 9: Error handling - missing response
    print("\n📝 Test 9: Error handling - missing response")
    test_data = {
        "criteria": ["accuracy"]
    }
    
    response = requests.post(f"{base_url}/score", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Expected error: {response.text}")
    else:
        print("Unexpected success")
    
    # Test 10: Mathematical problem
    print("\n📝 Test 10: Mathematical problem")
    test_data = {
        "response": "To solve 2x + 5 = 13, subtract 5 from both sides: 2x = 8, then divide by 2: x = 4.",
        "criteria": ["accuracy", "clarity"],
        "context": "Solve the equation: 2x + 5 = 13"
    }
    
    response = requests.post(f"{base_url}/score", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Score: {result['score']}/10")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Processing time: {result.get('processing_time_ms', 0):.0f}ms")
    else:
        print(f"Error: {response.text}")
    
    # Test 11: Performance test
    print("\n📝 Test 11: Performance test")
    test_data = {
        "response": "The capital of France is Paris, which is a beautiful city known for its culture, history, and landmarks like the Eiffel Tower.",
        "criteria": ["accuracy", "relevance", "clarity"],
        "context": "Question: What is the capital of France?"
    }
    
    start_time = time.time()
    response = requests.post(f"{base_url}/score", json=test_data)
    end_time = time.time()
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        api_time = (end_time - start_time) * 1000
        processing_time = result.get('processing_time_ms', 0)
        print(f"API time: {api_time:.0f}ms")
        print(f"Processing time: {processing_time:.0f}ms")
        print(f"Score: {result['score']}/10")
    else:
        print(f"Error: {response.text}")
    
    print("\n✅ Single scoring tests completed!")
    print("Check the responses above for results and error handling.")


if __name__ == "__main__":
    try:
        test_single_scoring()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the scoring agent.")
        print("   Make sure the service is running on http://localhost:8000")
        print("   Start the service with: python run.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}") 
#!/usr/bin/env python3
"""
Test script for the AI Scoring Agent batch endpoint.
Make sure the service is running on localhost:8000
"""

import requests
import json
import time
from typing import List, Dict, Any


def test_batch_scoring():
    """Test the batch scoring endpoint with various scenarios."""
    
    base_url = "http://localhost:8000"
    
    print("🤖 Testing AI Scoring Agent Batch Endpoint")
    print("=" * 50)
    
    # Test 1: Basic batch scoring
    print("\n📝 Test 1: Basic batch scoring")
    test_data = {
        "responses": [
            "The capital of France is Paris.",
            "The capital of France is London.",
            "Paris is the capital of France."
        ],
        "criteria": ["accuracy", "relevance"],
        "context": "Question: What is the capital of France?"
    }
    
    response = requests.post(f"{base_url}/score/batch", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Total processed: {result['total_processed']}")
        print(f"Successful: {result['successful']}")
        print(f"Failed: {result['failed']}")
        for i, item in enumerate(result['results']):
            print(f"  Response {i+1}: Score {item['score']}/10")
    else:
        print(f"Error: {response.text}")
    
    # Test 2: Comprehensive scoring with all criteria
    print("\n📝 Test 2: Comprehensive scoring with all criteria")
    test_data = {
        "responses": [
            "The capital of France is Paris, which is located in the northern part of the country.",
            "The capital of France is London, which is a beautiful city.",
            "I don't know the capital of France.",
            "France's capital city is Paris, which is known for the Eiffel Tower and is located in the Île-de-France region."
        ],
        "criteria": ["accuracy", "relevance", "clarity", "completeness", "coherence"],
        "context": "Question: What is the capital of France? Please provide a clear and accurate answer."
    }
    
    response = requests.post(f"{base_url}/score/batch", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Total processed: {result['total_processed']}")
        print(f"Successful: {result['successful']}")
        print(f"Failed: {result['failed']}")
        print(f"Processing time: {result.get('total_processing_time_ms', 0):.0f}ms")
        for i, item in enumerate(result['results']):
            print(f"  Response {i+1}: Score {item['score']}/10")
            if item.get('criteria_scores'):
                for criterion, score in item['criteria_scores'].items():
                    print(f"    {criterion}: {score}/10")
    else:
        print(f"Error: {response.text}")
    
    # Test 3: Minimal request (default criteria)
    print("\n📝 Test 3: Minimal request (default criteria)")
    test_data = {
        "responses": [
            "Paris is the capital of France.",
            "The capital is Paris.",
            "France's capital is Paris."
        ]
    }
    
    response = requests.post(f"{base_url}/score/batch", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Total processed: {result['total_processed']}")
        print(f"Successful: {result['successful']}")
        print(f"Failed: {result['failed']}")
        for i, item in enumerate(result['results']):
            print(f"  Response {i+1}: Score {item['score']}/10")
    else:
        print(f"Error: {response.text}")
    
    # Test 4: Error handling - invalid criteria
    print("\n📝 Test 4: Error handling - invalid criteria")
    test_data = {
        "responses": ["The capital of France is Paris."],
        "criteria": ["invalid_criterion"]
    }
    
    response = requests.post(f"{base_url}/score/batch", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Expected error: {response.text}")
    else:
        print("Unexpected success")
    
    # Test 5: Error handling - empty responses
    print("\n📝 Test 5: Error handling - empty responses")
    test_data = {
        "responses": [],
        "criteria": ["accuracy"]
    }
    
    response = requests.post(f"{base_url}/score/batch", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Expected error: {response.text}")
    else:
        print("Unexpected success")
    
    # Test 6: Performance test with larger batch
    print("\n📝 Test 6: Performance test with larger batch")
    test_data = {
        "responses": [
            f"Response {i}: The capital of France is Paris." for i in range(5)
        ],
        "criteria": ["accuracy", "relevance"],
        "context": "Question: What is the capital of France?"
    }
    
    start_time = time.time()
    response = requests.post(f"{base_url}/score/batch", json=test_data)
    end_time = time.time()
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        api_time = (end_time - start_time) * 1000
        processing_time = result.get('total_processing_time_ms', 0)
        print(f"API time: {api_time:.0f}ms")
        print(f"Processing time: {processing_time:.0f}ms")
        print(f"Total processed: {result['total_processed']}")
        print(f"Successful: {result['successful']}")
        print(f"Failed: {result['failed']}")
    else:
        print(f"Error: {response.text}")
    
    print("\n✅ Batch scoring tests completed!")
    print("Check the responses above for results and error handling.")


if __name__ == "__main__":
    try:
        test_batch_scoring()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the scoring agent.")
        print("   Make sure the service is running on http://localhost:8000")
        print("   Start the service with: python run.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}") 
#!/usr/bin/env python3
"""
Example usage of the AI Scoring Agent.
This script demonstrates how to use the scoring agent API.
"""

import requests
import json
import time
from typing import List, Dict, Any


class ScoringAgentClient:
    """Client for interacting with the AI Scoring Agent API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check the health of the scoring agent."""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def get_config(self) -> Dict[str, Any]:
        """Get the current configuration."""
        response = self.session.get(f"{self.base_url}/config")
        response.raise_for_status()
        return response.json()
    
    def score_response(
        self, 
        response: str, 
        criteria: List[str] = None, 
        context: str = None
    ) -> Dict[str, Any]:
        """Score a single AI response."""
        payload = {
            "response": response,
            "criteria": criteria or ["accuracy", "relevance", "clarity"],
            "context": context
        }
        
        response_obj = self.session.post(f"{self.base_url}/score", json=payload)
        response_obj.raise_for_status()
        return response_obj.json()
    
    def score_batch(
        self, 
        responses: List[str], 
        criteria: List[str] = None, 
        context: str = None
    ) -> Dict[str, Any]:
        """Score multiple AI responses in batch."""
        payload = {
            "responses": responses,
            "criteria": criteria or ["accuracy", "relevance", "clarity"],
            "context": context
        }
        
        response_obj = self.session.post(f"{self.base_url}/score/batch", json=payload)
        response_obj.raise_for_status()
        return response_obj.json()


def main():
    """Main example function."""
    print("🤖 AI Scoring Agent - Example Usage")
    print("=" * 50)
    
    # Initialize client
    client = ScoringAgentClient()
    
    try:
        # Check health
        print("\n1. Health Check")
        health = client.health_check()
        print(f"✅ Service Status: {health['status']}")
        print(f"📊 Service: {health['service']}")
        print(f"🔢 Version: {health['version']}")
        
        # Get configuration
        print("\n2. Configuration")
        config = client.get_config()
        print(f"🤖 OpenAI Model: {config['openai_model']}")
        print(f"⚙️ Max Tokens: {config['max_tokens']}")
        print(f"🌡️ Temperature: {config['temperature']}")
        print(f"📋 Default Criteria: {config['default_criteria']}")
        
        # Example responses to score
        example_responses = [
            "The capital of France is Paris.",
            "The capital of France is London.",
            "Paris is the capital of France.",
            "France's capital city is Paris, which is located in the northern part of the country.",
            "I don't know the capital of France."
        ]
        
        questions = [
            "What is the capital of France?",
            "What is the capital of France?",
            "What is the capital of France?",
            "What is the capital of France?",
            "What is the capital of France?"
        ]
        
        print("\n3. Single Response Scoring")
        print("-" * 30)
        
        for i, (response, question) in enumerate(zip(example_responses, questions)):
            print(f"\n📝 Response {i+1}: {response}")
            print(f"❓ Question: {question}")
            
            start_time = time.time()
            result = client.score_response(
                response=response,
                criteria=["accuracy", "relevance", "clarity"],
                context=question
            )
            end_time = time.time()
            
            print(f"⭐ Score: {result['score']}/10")
            print(f"💭 Reasoning: {result['reasoning']}")
            print(f"⏱️ Processing Time: {result.get('processing_time_ms', 0):.0f}ms")
            print(f"🔄 API Time: {(end_time - start_time) * 1000:.0f}ms")
            
            if result.get('criteria_scores'):
                print("📊 Criteria Scores:")
                for criterion, score in result['criteria_scores'].items():
                    print(f"   - {criterion}: {score}/10")
        
        print("\n4. Batch Response Scoring")
        print("-" * 30)
        
        start_time = time.time()
        batch_result = client.score_batch(
            responses=example_responses,
            criteria=["accuracy", "relevance", "clarity"],
            context="What is the capital of France?"
        )
        end_time = time.time()
        
        print(f"📦 Total Processed: {batch_result['total_processed']}")
        print(f"✅ Successful: {batch_result['successful']}")
        print(f"❌ Failed: {batch_result['failed']}")
        print(f"⏱️ Total Processing Time: {batch_result.get('total_processing_time_ms', 0):.0f}ms")
        print(f"📊 Average Processing Time: {batch_result.get('average_processing_time_ms', 0):.0f}ms")
        print(f"🔄 API Time: {(end_time - start_time) * 1000:.0f}ms")
        
        print("\n📋 Individual Results:")
        for i, result in enumerate(batch_result['results']):
            print(f"\n   Response {i+1}: {result['response'][:50]}...")
            print(f"   Score: {result['score']}/10")
            print(f"   Reasoning: {result['reasoning'][:100]}...")
            
            if result.get('error'):
                print(f"   ❌ Error: {result['error']}")
        
        # Performance comparison
        print("\n5. Performance Analysis")
        print("-" * 30)
        
        single_total_time = sum(
            result.get('processing_time_ms', 0) 
            for result in batch_result['results']
        )
        batch_total_time = batch_result.get('total_processing_time_ms', 0)
        
        if single_total_time > 0:
            speedup = single_total_time / batch_total_time if batch_total_time > 0 else 1
            print(f"🚀 Batch processing is {speedup:.1f}x faster than individual requests")
        
        print("\n✅ Example completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the scoring agent.")
        print("   Make sure the service is running on http://localhost:8000")
        print("   Start the service with: python main.py")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if e.response is not None:
            print(f"   Response: {e.response.text}")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main() 
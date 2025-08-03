#!/usr/bin/env python3
"""
Test script to demonstrate the BDD AI Agent functionality
"""

import requests
import json
import time

def test_bdd_agent():
    """Test the BDD AI Agent with sample requirements"""
    
    # Sample requirements for testing
    sample_requirements = """
    As a user, I should be able to log into the system using my email and password.
    When I enter valid credentials, the system should authenticate me and redirect me to the dashboard.
    If I enter invalid credentials, the system should show an error message and not log me in.
    The system should also support password reset functionality where users can request a reset link via email.
    """
    
    # Test data
    test_data = {
        "requirements": sample_requirements,
        "options": {
            "include_negative_scenarios": True,
            "output_format": "both",
            "max_scenarios_per_requirement": 5,
            "include_examples": True
        },
        "metadata": {
            "feature_name": "User Authentication System",
            "project_id": "AUTH-001",
            "author": "Test User"
        }
    }
    
    print("🚀 Testing BDD AI Agent")
    print("=" * 50)
    print(f"Requirements: {len(sample_requirements)} characters")
    print(f"Options: {test_data['options']}")
    print()
    
    try:
        # Test health endpoint first
        print("📋 Checking service health...")
        health_response = requests.get("http://localhost:8003/health", timeout=10)
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Service is healthy")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Model loaded: {health_data.get('model_loaded')}")
            print(f"   Version: {health_data.get('version')}")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
            return
        
        print()
        print("🔄 Generating BDD scenarios...")
        start_time = time.time()
        
        # Make request to generate BDD scenarios
        response = requests.post(
            "http://localhost:8003/bdd-from-text",
            json=test_data,
            timeout=30
        )
        
        end_time = time.time()
        processing_time = (end_time - start_time) * 1000
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Successfully generated scenarios in {processing_time:.2f}ms")
            print()
            
            # Display results
            print("📊 Results Summary:")
            print(f"   Status: {result.get('status')}")
            print(f"   Scenarios generated: {result.get('metadata', {}).get('scenarios_generated', 0)}")
            print(f"   Quality score: {result.get('metadata', {}).get('quality_score', 0):.2f}")
            print(f"   Processing time: {result.get('metadata', {}).get('processing_time_ms', 0):.2f}ms")
            
            # Display scenarios
            scenarios = result.get('scenarios', [])
            print()
            print(f"📝 Generated Scenarios ({len(scenarios)}):")
            print("=" * 50)
            
            for i, scenario in enumerate(scenarios, 1):
                print(f"\n{i}. {scenario.get('scenario', 'Unknown Scenario')}")
                print(f"   Feature: {scenario.get('feature', 'Unknown Feature')}")
                print(f"   Type: {scenario.get('type', 'positive')}")
                
                print("   Given:")
                for step in scenario.get('given', []):
                    print(f"     - {step}")
                
                print("   When:")
                for step in scenario.get('when', []):
                    print(f"     - {step}")
                
                print("   Then:")
                for step in scenario.get('then', []):
                    print(f"     - {step}")
                
                # Show examples if present
                examples = scenario.get('examples', [])
                if examples:
                    print("   Examples:")
                    for example in examples[:3]:  # Show first 3 examples
                        print(f"     - {example}")
                    if len(examples) > 3:
                        print(f"     ... and {len(examples) - 3} more")
            
            # Display warnings and errors
            warnings = result.get('warnings', [])
            errors = result.get('errors', [])
            
            if warnings:
                print()
                print("⚠️  Warnings:")
                for warning in warnings:
                    print(f"   - {warning}")
            
            if errors:
                print()
                print("❌ Errors:")
                for error in errors:
                    print(f"   - {error}")
            
            # Show sample Gherkin output
            if scenarios:
                print()
                print("🌱 Sample Gherkin Output:")
                print("=" * 50)
                print(scenarios[0].get('gherkin', 'No Gherkin output available'))
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the service. Make sure it's running on http://localhost:8003")
        print("   Start the service with: python run.py")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The service might be overloaded or not responding.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

def test_simple_requirements():
    """Test with simpler requirements"""
    
    simple_requirements = "As a customer, I should be able to add items to my shopping cart and checkout."
    
    test_data = {
        "requirements": simple_requirements,
        "options": {
            "include_negative_scenarios": False,
            "max_scenarios_per_requirement": 2,
            "include_examples": False
        }
    }
    
    print("\n🧪 Testing with simple requirements...")
    
    try:
        response = requests.post(
            "http://localhost:8003/bdd-from-text",
            json=test_data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            scenarios = result.get('scenarios', [])
            print(f"✅ Generated {len(scenarios)} scenarios for simple requirements")
            
            for i, scenario in enumerate(scenarios, 1):
                print(f"   {i}. {scenario.get('scenario', 'Unknown')}")
        else:
            print(f"❌ Simple test failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Simple test error: {str(e)}")

if __name__ == "__main__":
    print("BDD AI Agent Test Script")
    print("=" * 50)
    print("This script tests the BDD Scenario Generator AI Agent")
    print("Make sure the service is running on http://localhost:8003")
    print()
    
    # Run main test
    test_bdd_agent()
    
    # Run simple test
    test_simple_requirements()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("Check the API documentation at: http://localhost:8003/docs") 
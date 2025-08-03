#!/usr/bin/env python3
"""
Demo script to test the Orchestrator Agent functionality.
This script demonstrates how to use the Orchestrator Agent API.
"""

import asyncio
import httpx
import json
from typing import Dict, Any


class OrchestratorDemo:
    """Demo class for testing the Orchestrator Agent."""
    
    def __init__(self, base_url: str = "http://localhost:8003"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def health_check(self) -> Dict[str, Any]:
        """Check the health of the orchestrator service."""
        print("🔍 Checking orchestrator health...")
        try:
            response = await self.client.get(f"{self.base_url}/health")
            response.raise_for_status()
            result = response.json()
            print(f"✅ Health check passed: {result['status']}")
            return result
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}
    
    async def get_config(self) -> Dict[str, Any]:
        """Get the current configuration."""
        print("⚙️ Getting configuration...")
        try:
            response = await self.client.get(f"{self.base_url}/config")
            response.raise_for_status()
            result = response.json()
            print("✅ Configuration retrieved successfully")
            return result
        except Exception as e:
            print(f"❌ Failed to get configuration: {e}")
            return {}
    
    async def register_agent(self, agent_endpoint: str) -> Dict[str, Any]:
        """Register an agent for testing."""
        print(f"📝 Registering agent at {agent_endpoint}...")
        
        payload = {
            "agent_endpoint": agent_endpoint,
            "agent_description": "A helpful AI assistant for testing",
            "system_prompt": "You are a helpful AI assistant. Provide accurate and relevant responses.",
            "skills_and_tools": ["web_search", "calculator", "knowledge_base"],
            "test_criteria": ["accuracy", "relevance", "clarity", "completeness"],
            "scoring_threshold": 6.0,
            "optimization_context": {
                "language": "English",
                "complexity": "intermediate",
                "target_audience": "general"
            }
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/register-agent",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            print(f"✅ Agent registered successfully: {result['registration_status']}")
            return result
        except Exception as e:
            print(f"❌ Agent registration failed: {e}")
            return {"error": str(e)}
    
    async def test_agent(self, agent_endpoint: str, test_prompt: str) -> Dict[str, Any]:
        """Test an agent with a specific prompt."""
        print(f"🧪 Testing agent with prompt: '{test_prompt}'...")
        
        payload = {
            "agent_endpoint": agent_endpoint,
            "test_prompt": test_prompt,
            "test_criteria": ["accuracy", "relevance", "clarity", "completeness"],
            "scoring_threshold": 6.0,
            "optimization_context": {
                "language": "English",
                "complexity": "basic",
                "target_audience": "general"
            }
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/test-agent",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Test completed:")
            print(f"   Status: {result['test_status']}")
            print(f"   Overall Score: {result['overall_score']:.2f}")
            print(f"   Processing Time: {result['processing_time_ms']}ms")
            print(f"   Agent Response: {result['agent_response'][:100]}...")
            
            return result
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return {"error": str(e)}
    
    async def batch_test(self, agent_endpoint: str) -> Dict[str, Any]:
        """Run a batch of tests on an agent."""
        print(f"📊 Running batch tests on {agent_endpoint}...")
        
        test_prompts = [
            "What is the capital of France?",
            "Explain quantum computing in simple terms",
            "What are the benefits of renewable energy?",
            "How does machine learning work?",
            "What is the difference between AI and AGI?"
        ]
        
        tests = []
        for prompt in test_prompts:
            tests.append({
                "agent_endpoint": agent_endpoint,
                "test_prompt": prompt,
                "test_criteria": ["accuracy", "relevance", "clarity"],
                "scoring_threshold": 6.0
            })
        
        payload = {
            "tests": tests,
            "parallel_execution": True
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/test-batch",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Batch test completed:")
            print(f"   Total Tests: {result['total_tests']}")
            print(f"   Passed: {result['passed_tests']}")
            print(f"   Failed: {result['failed_tests']}")
            print(f"   Total Processing Time: {result['batch_processing_time_ms']}ms")
            
            return result
        except Exception as e:
            print(f"❌ Batch test failed: {e}")
            return {"error": str(e)}
    
    async def health_check_agent(self, agent_endpoint: str) -> Dict[str, Any]:
        """Check the health of a specific agent."""
        print(f"🏥 Checking health of agent at {agent_endpoint}...")
        
        payload = {
            "agent_endpoint": agent_endpoint
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/health-check-agent",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Agent health check:")
            print(f"   Status: {result['status']}")
            if result.get('response_time_ms'):
                print(f"   Response Time: {result['response_time_ms']:.2f}ms")
            if result.get('error_message'):
                print(f"   Error: {result['error_message']}")
            
            return result
        except Exception as e:
            print(f"❌ Agent health check failed: {e}")
            return {"error": str(e)}
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


async def main():
    """Main demo function."""
    print("🚀 Orchestrator Agent Demo")
    print("=" * 50)
    
    demo = OrchestratorDemo()
    
    try:
        # Test agent endpoint (you can replace this with a real agent)
        test_agent_endpoint = "http://localhost:3000"
        
        # 1. Health check
        await demo.health_check()
        print()
        
        # 2. Get configuration
        config = await demo.get_config()
        print(f"Configuration: {json.dumps(config, indent=2)}")
        print()
        
        # 3. Register agent
        await demo.register_agent(test_agent_endpoint)
        print()
        
        # 4. Health check agent
        await demo.health_check_agent(test_agent_endpoint)
        print()
        
        # 5. Single test
        await demo.test_agent(
            test_agent_endpoint,
            "What is the capital of France?"
        )
        print()
        
        # 6. Batch test
        await demo.batch_test(test_agent_endpoint)
        print()
        
        print("✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    
    finally:
        await demo.close()


if __name__ == "__main__":
    asyncio.run(main()) 
import logging
import httpx
import asyncio
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import get_settings

logger = logging.getLogger(__name__)


class AgentTestingService:
    """Service for testing AI agents."""
    
    def __init__(self):
        self.settings = get_settings()
        self.timeout = self.settings.orchestrator.timeout
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def test_agent(
        self, 
        agent_endpoint: str, 
        prompt: str,
        system_prompt: Optional[str] = None,
        skills_and_tools: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Test an AI agent by sending a prompt and receiving a response.
        
        Args:
            agent_endpoint: The agent's endpoint URL
            prompt: The prompt to send to the agent
            system_prompt: Optional system prompt
            skills_and_tools: Optional list of skills and tools
            
        Returns:
            Dict containing the agent's response and metadata
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Prepare the request payload
                payload = {
                    "prompt": prompt,
                    "system_prompt": system_prompt,
                    "skills_and_tools": skills_and_tools or []
                }
                
                logger.info(f"Testing agent at {agent_endpoint} with prompt: {prompt[:100]}...")
                
                # Try different common endpoints for AI agents
                endpoints_to_try = [
                    f"{agent_endpoint}/bdd-from-text",
                    f"{agent_endpoint}/generate",
                    f"{agent_endpoint}/completion",
                    f"{agent_endpoint}/",
                    agent_endpoint
                ]
                
                response = None
                used_endpoint = None
                
                for endpoint in endpoints_to_try:
                    try:
                        response = await client.post(
                            endpoint,
                            json=payload,
                            timeout=self.timeout
                        )
                        response.raise_for_status()
                        used_endpoint = endpoint
                        break
                    except httpx.HTTPStatusError as e:
                        if e.response.status_code == 404:
                            continue  # Try next endpoint
                        else:
                            raise
                    except httpx.RequestError:
                        continue  # Try next endpoint
                
                if response is None:
                    raise Exception("No valid endpoint found for the agent")
                
                result = response.json()
                logger.info(f"Agent test completed successfully using endpoint: {used_endpoint}")
                
                # Extract response text from common response formats
                response_text = self._extract_response_text(result)
                
                return {
                    "response": response_text,
                    "raw_response": result,
                    "endpoint_used": used_endpoint,
                    "status_code": response.status_code,
                    "response_time_ms": response.elapsed.total_seconds() * 1000
                }
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during agent testing: {e}")
            raise Exception(f"Agent testing error: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Request error during agent testing: {e}")
            raise Exception(f"Agent testing failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during agent testing: {e}")
            raise Exception(f"Agent testing failed: {str(e)}")
    
    def _extract_response_text(self, response_data: Dict[str, Any]) -> str:
        """
        Extract response text from various response formats.
        
        Args:
            response_data: The raw response data from the agent
            
        Returns:
            The extracted response text
        """
        # Common response field names
        possible_fields = [
            "response", "content", "text", "message", "output", 
            "result", "answer", "generated_text", "completion"
        ]
        
        # Check for direct string response
        if isinstance(response_data, str):
            return response_data
        
        # Check for common field names
        for field in possible_fields:
            if field in response_data:
                value = response_data[field]
                if isinstance(value, str):
                    return value
                elif isinstance(value, dict) and "content" in value:
                    return value["content"]
                elif isinstance(value, list) and len(value) > 0:
                    # Handle list of messages format
                    first_item = value[0]
                    if isinstance(first_item, dict) and "content" in first_item:
                        return first_item["content"]
        
        # If no standard field found, try to convert to string
        return str(response_data)
    
    async def health_check(self, agent_endpoint: str) -> Dict[str, Any]:
        """
        Check if an agent is healthy and responsive.
        
        Args:
            agent_endpoint: The agent's endpoint URL
            
        Returns:
            Dict containing health status and response time
        """
        try:
            start_time = asyncio.get_event_loop().time()
            
            async with httpx.AsyncClient(timeout=10) as client:
                # Try health check endpoints
                health_endpoints = [
                    f"{agent_endpoint}/health",
                    f"{agent_endpoint}/status",
                    f"{agent_endpoint}/",
                    agent_endpoint
                ]
                
                for endpoint in health_endpoints:
                    try:
                        response = await client.get(endpoint, timeout=10)
                        if response.status_code in [200, 404]:  # 404 might mean endpoint exists but method not allowed
                            end_time = asyncio.get_event_loop().time()
                            response_time_ms = (end_time - start_time) * 1000
                            
                            return {
                                "status": "healthy",
                                "response_time_ms": response_time_ms,
                                "endpoint_used": endpoint,
                                "status_code": response.status_code
                            }
                    except httpx.RequestError:
                        continue
                
                # If no health endpoint responds, try a simple GET request
                try:
                    response = await client.get(agent_endpoint, timeout=10)
                    end_time = asyncio.get_event_loop().time()
                    response_time_ms = (end_time - start_time) * 1000
                    
                    return {
                        "status": "healthy",
                        "response_time_ms": response_time_ms,
                        "endpoint_used": agent_endpoint,
                        "status_code": response.status_code
                    }
                except httpx.RequestError:
                    return {
                        "status": "unhealthy",
                        "error_message": "Agent endpoint not reachable",
                        "response_time_ms": None
                    }
                    
        except Exception as e:
            logger.error(f"Health check failed for agent {agent_endpoint}: {e}")
            return {
                "status": "unhealthy",
                "error_message": str(e),
                "response_time_ms": None
            } 
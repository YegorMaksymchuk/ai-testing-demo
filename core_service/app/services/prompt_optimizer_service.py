import logging
import httpx
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import get_settings

logger = logging.getLogger(__name__)


class PromptOptimizerService:
    """Service for integrating with the prompt optimizer API."""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.services.optimizer.url
        self.timeout = self.settings.services.optimizer.timeout
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def optimize_prompt(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Optimize a prompt using the prompt optimizer service.
        
        Args:
            prompt: The original prompt to optimize
            context: Additional context for optimization
            
        Returns:
            Dict containing optimized prompt and analysis
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "prompt": prompt,
                    "context": context or {}
                }
                
                logger.info(f"Requesting prompt optimization for prompt: {prompt[:100]}...")
                
                response = await client.post(
                    f"{self.base_url}/optimize",
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                logger.info("Prompt optimization completed successfully")
                
                return {
                    "enhanced_prompt": result.get("enhanced_prompt", prompt),
                    "analysis": result.get("analysis", {}),
                    "applied_practices": result.get("applied_practices", []),
                    "agent_memory": result.get("agent_memory", [])
                }
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during prompt optimization: {e}")
            raise Exception(f"Prompt optimizer service error: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Request error during prompt optimization: {e}")
            raise Exception(f"Prompt optimizer service unavailable: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during prompt optimization: {e}")
            raise Exception(f"Prompt optimization failed: {str(e)}")
    
    async def health_check(self) -> bool:
        """
        Check if the prompt optimizer service is healthy.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed for prompt optimizer: {e}")
            return False 
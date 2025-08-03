import logging
import httpx
from typing import Dict, Any, List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import get_settings

logger = logging.getLogger(__name__)


class ScoringService:
    """Service for integrating with the scoring API."""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.services.scorer.url
        self.timeout = self.settings.services.scorer.timeout
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def score_response(
        self, 
        response: str, 
        criteria: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Score an AI response using the scoring service.
        
        Args:
            response: The AI response to score
            criteria: List of scoring criteria
            context: Additional context for scoring
            
        Returns:
            Dict containing scores and reasoning
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "response": response,
                    "criteria": criteria,
                    "context": context or {}
                }
                
                logger.info(f"Requesting response scoring for response: {response[:100]}...")
                
                response_obj = await client.post(
                    f"{self.base_url}/score",
                    json=payload
                )
                response_obj.raise_for_status()
                
                result = response_obj.json()
                logger.info("Response scoring completed successfully")
                
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during response scoring: {e}")
            raise Exception(f"Scoring service error: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Request error during response scoring: {e}")
            raise Exception(f"Scoring service unavailable: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during response scoring: {e}")
            raise Exception(f"Response scoring failed: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def score_batch(
        self, 
        responses: List[str], 
        criteria: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Score multiple AI responses in batch.
        
        Args:
            responses: List of AI responses to score
            criteria: List of scoring criteria
            context: Additional context for scoring
            
        Returns:
            Dict containing batch scores and results
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "responses": responses,
                    "criteria": criteria,
                    "context": context or {}
                }
                
                logger.info(f"Requesting batch scoring for {len(responses)} responses")
                
                response = await client.post(
                    f"{self.base_url}/score/batch",
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                logger.info("Batch scoring completed successfully")
                
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during batch scoring: {e}")
            raise Exception(f"Scoring service error: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Request error during batch scoring: {e}")
            raise Exception(f"Scoring service unavailable: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during batch scoring: {e}")
            raise Exception(f"Batch scoring failed: {str(e)}")
    
    async def health_check(self) -> bool:
        """
        Check if the scoring service is healthy.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed for scoring service: {e}")
            return False 
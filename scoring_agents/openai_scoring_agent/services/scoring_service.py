"""
Scoring Service for AI Scoring Agent.
Handles OpenAI integration and scoring logic.
"""

import asyncio
import json
import logging
import os
import time
from typing import List, Optional, Dict, Any
from datetime import datetime

import openai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from models.response_models import (
    ScoringResponse, 
    BatchScoringResponse, 
    BatchScoringItem,
    ScoringResult
)

logger = logging.getLogger(__name__)


class ScoringService:
    """Service for scoring AI responses using OpenAI."""
    
    def __init__(self):
        """Initialize the scoring service."""
        self.client = None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", 2000))
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", 0.0))
        self.default_criteria = os.getenv("DEFAULT_SCORING_CRITERIA", "accuracy,relevance,clarity").split(",")
        self.scoring_scale = os.getenv("SCORING_SCALE", "1-10")
        
        # Rate limiting
        self.rate_limit_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", 60))
        self.request_times = []
    
    async def initialize(self):
        """Initialize the OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = openai.AsyncOpenAI(api_key=api_key)
        
        # Test the connection
        try:
            await self._test_connection()
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup resources."""
        if self.client:
            await self.client.close()
            logger.info("OpenAI client closed")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((openai.RateLimitError, openai.APITimeoutError))
    )
    async def _test_connection(self):
        """Test OpenAI connection with a simple request."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10,
                temperature=0
            )
            logger.info("OpenAI connection test successful")
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {e}")
            raise
    
    def _check_rate_limit(self):
        """Check if we're within rate limits."""
        current_time = time.time()
        # Remove requests older than 1 minute
        self.request_times = [t for t in self.request_times if current_time - t < 60]
        
        if len(self.request_times) >= self.rate_limit_per_minute:
            raise Exception(f"Rate limit exceeded: {self.rate_limit_per_minute} requests per minute")
        
        self.request_times.append(current_time)
    
    def _build_scoring_prompt(self, response: str, criteria: Optional[List[str]] = None, context: Optional[str] = None) -> str:
        """Build the scoring prompt for OpenAI."""
        criteria = criteria or self.default_criteria
        criteria_text = ", ".join(criteria)
        
        prompt = f"""You are an expert evaluator of AI responses. Please score the following AI response on a scale of 1-10, where 10 is excellent and 1 is very poor.

Scoring Criteria: {criteria_text}

AI Response to Evaluate:
{response}

"""
        
        if context:
            prompt += f"Context/Question: {context}\n\n"
        
        prompt += f"""Please provide your evaluation in the following JSON format:
{{
    "score": <numeric_score_1-10>,
    "reasoning": "<detailed_explanation_of_score>",
    "criteria_scores": {{
        {", ".join([f'"{criterion}": <score_1-10>' for criterion in criteria])}
    }},
    "confidence": <confidence_level_0-1>
}}

Focus on:
- Accuracy: How correct and factual is the response?
- Relevance: How well does it address the question/context?
- Clarity: How clear and well-structured is the response?
- Completeness: How comprehensive is the response?
- Coherence: How logical and coherent is the response?

Provide only the JSON response, no additional text."""

        return prompt
    
    def _parse_scoring_response(self, response_text: str) -> ScoringResult:
        """Parse the scoring response from OpenAI."""
        try:
            # Extract JSON from response
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_data = json.loads(response_text.strip())
            
            # Validate required fields
            if "score" not in response_data or "reasoning" not in response_data:
                raise ValueError("Missing required fields in scoring response")
            
            score = float(response_data["score"])
            reasoning = response_data["reasoning"]
            criteria_scores = response_data.get("criteria_scores")
            confidence = response_data.get("confidence")
            
            # Validate score range
            if not (0 <= score <= 10):
                raise ValueError(f"Score {score} is outside valid range 0-10")
            
            # Validate confidence if provided
            if confidence is not None and not (0 <= confidence <= 1):
                raise ValueError(f"Confidence {confidence} is outside valid range 0-1")
            
            return ScoringResult(
                score=score,
                reasoning=reasoning,
                criteria_scores=criteria_scores,
                confidence=confidence
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Invalid JSON response from OpenAI: {response_text}")
        except Exception as e:
            logger.error(f"Failed to parse scoring response: {e}")
            raise ValueError(f"Failed to parse scoring response: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((openai.RateLimitError, openai.APITimeoutError))
    )
    async def _call_openai(self, prompt: str) -> str:
        """Make a call to OpenAI API with retry logic."""
        self._check_rate_limit()
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content
            
        except openai.RateLimitError as e:
            logger.warning(f"Rate limit hit: {e}")
            raise
        except openai.APITimeoutError as e:
            logger.warning(f"OpenAI API timeout: {e}")
            raise
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def score_response(
        self, 
        response: str, 
        criteria: Optional[List[str]] = None, 
        context: Optional[str] = None
    ) -> ScoringResponse:
        """
        Score a single AI response.
        
        Args:
            response: The AI response to score
            criteria: List of scoring criteria
            context: Additional context for scoring
            
        Returns:
            ScoringResponse: The scoring result
        """
        start_time = time.time()
        
        try:
            # Build the scoring prompt
            prompt = self._build_scoring_prompt(response, criteria, context)
            
            # Call OpenAI
            openai_response = await self._call_openai(prompt)
            
            # Parse the response
            scoring_result = self._parse_scoring_response(openai_response)
            
            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000
            
            return ScoringResponse(
                score=scoring_result.score,
                reasoning=scoring_result.reasoning,
                criteria_scores=scoring_result.criteria_scores,
                confidence=scoring_result.confidence,
                model_used=self.model,
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error scoring response: {e}")
            raise
    
    async def score_batch(
        self, 
        responses: List[str], 
        criteria: Optional[List[str]] = None, 
        context: Optional[str] = None
    ) -> BatchScoringResponse:
        """
        Score multiple AI responses in batch.
        
        Args:
            responses: List of AI responses to score
            criteria: List of scoring criteria
            context: Additional context for scoring
            
        Returns:
            BatchScoringResponse: The batch scoring results
        """
        start_time = time.time()
        results = []
        successful = 0
        failed = 0
        
        # Process responses concurrently with semaphore for rate limiting
        semaphore = asyncio.Semaphore(5)  # Limit concurrent requests
        
        async def score_single_response(response: str, index: int) -> BatchScoringItem:
            nonlocal successful, failed
            
            try:
                async with semaphore:
                    scoring_response = await self.score_response(response, criteria, context)
                    
                    successful += 1
                    return BatchScoringItem(
                        response=response,
                        score=scoring_response.score,
                        reasoning=scoring_response.reasoning,
                        criteria_scores=scoring_response.criteria_scores,
                        confidence=scoring_response.confidence
                    )
                    
            except Exception as e:
                failed += 1
                logger.error(f"Failed to score response {index}: {e}")
                return BatchScoringItem(
                    response=response,
                    score=0.0,
                    reasoning=f"Scoring failed: {str(e)}",
                    error=str(e)
                )
        
        # Create tasks for all responses
        tasks = [
            score_single_response(response, i) 
            for i, response in enumerate(responses)
        ]
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Calculate processing times
        total_processing_time = (time.time() - start_time) * 1000
        average_processing_time = total_processing_time / len(responses) if responses else 0
        
        return BatchScoringResponse(
            results=results,
            total_processed=len(responses),
            successful=successful,
            failed=failed,
            model_used=self.model,
            total_processing_time_ms=total_processing_time,
            average_processing_time_ms=average_processing_time
        ) 
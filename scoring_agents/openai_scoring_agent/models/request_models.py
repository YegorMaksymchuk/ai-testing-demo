"""
Request models for the AI Scoring Agent API.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class ScoringRequest(BaseModel):
    """Request model for single response scoring."""
    
    response: str = Field(..., description="The AI response to be scored", min_length=1)
    criteria: Optional[List[str]] = Field(
        default=None,
        description="List of scoring criteria to evaluate"
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context for scoring (e.g., original question, expected format)"
    )
    
    @validator('response')
    def validate_response(cls, v):
        if not v.strip():
            raise ValueError('Response cannot be empty')
        return v.strip()
    
    @validator('criteria')
    def validate_criteria(cls, v):
        if v is not None:
            valid_criteria = ['accuracy', 'relevance', 'clarity', 'completeness', 'coherence']
            for criterion in v:
                if criterion not in valid_criteria:
                    raise ValueError(f'Invalid criterion: {criterion}. Valid criteria: {valid_criteria}')
        return v


class BatchScoringRequest(BaseModel):
    """Request model for batch response scoring."""
    
    responses: List[str] = Field(..., description="List of AI responses to be scored", min_items=1)
    criteria: Optional[List[str]] = Field(
        default=None,
        description="List of scoring criteria to evaluate"
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context for scoring (e.g., original question, expected format)"
    )
    
    @validator('responses')
    def validate_responses(cls, v):
        if not v:
            raise ValueError('At least one response is required')
        for i, response in enumerate(v):
            if not response.strip():
                raise ValueError(f'Response at index {i} cannot be empty')
        return [r.strip() for r in v]
    
    @validator('criteria')
    def validate_criteria(cls, v):
        if v is not None:
            valid_criteria = ['accuracy', 'relevance', 'clarity', 'completeness', 'coherence']
            for criterion in v:
                if criterion not in valid_criteria:
                    raise ValueError(f'Invalid criterion: {criterion}. Valid criteria: {valid_criteria}')
        return v


class ConfigRequest(BaseModel):
    """Request model for updating configuration."""
    
    openai_model: Optional[str] = Field(None, description="OpenAI model to use")
    max_tokens: Optional[int] = Field(None, ge=1, le=4000, description="Maximum tokens for OpenAI response")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Temperature for OpenAI response")
    default_criteria: Optional[List[str]] = Field(None, description="Default scoring criteria")
    scoring_scale: Optional[str] = Field(None, description="Scoring scale (e.g., '1-10', '1-5')")
    max_batch_size: Optional[int] = Field(None, ge=1, le=1000, description="Maximum batch size")
    rate_limit_per_minute: Optional[int] = Field(None, ge=1, le=1000, description="Rate limit per minute") 
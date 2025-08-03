"""
Response models for the AI Scoring Agent API.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ScoringResult(BaseModel):
    """Individual scoring result."""
    
    score: float = Field(..., ge=0.0, le=10.0, description="Numeric score from 0-10")
    reasoning: str = Field(..., description="Detailed reasoning for the score")
    criteria_scores: Optional[Dict[str, float]] = Field(
        None,
        description="Individual scores for each criterion"
    )
    confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confidence level in the scoring (0-1)"
    )


class ScoringResponse(BaseModel):
    """Response model for single response scoring."""
    
    score: float = Field(..., ge=0.0, le=10.0, description="Overall score from 0-10")
    reasoning: str = Field(..., description="Detailed reasoning for the score")
    criteria_scores: Optional[Dict[str, float]] = Field(
        None,
        description="Individual scores for each criterion"
    )
    confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confidence level in the scoring (0-1)"
    )
    model_used: str = Field(..., description="OpenAI model used for scoring")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of scoring")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")


class BatchScoringItem(BaseModel):
    """Individual item in batch scoring response."""
    
    response: str = Field(..., description="The original response that was scored")
    score: float = Field(..., ge=0.0, le=10.0, description="Overall score from 0-10")
    reasoning: str = Field(..., description="Detailed reasoning for the score")
    criteria_scores: Optional[Dict[str, float]] = Field(
        None,
        description="Individual scores for each criterion"
    )
    confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confidence level in the scoring (0-1)"
    )
    error: Optional[str] = Field(None, description="Error message if scoring failed")


class BatchScoringResponse(BaseModel):
    """Response model for batch response scoring."""
    
    results: List[BatchScoringItem] = Field(..., description="List of scoring results")
    total_processed: int = Field(..., description="Total number of responses processed")
    successful: int = Field(..., description="Number of successful scorings")
    failed: int = Field(..., description="Number of failed scorings")
    model_used: str = Field(..., description="OpenAI model used for scoring")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of batch scoring")
    total_processing_time_ms: Optional[float] = Field(None, description="Total processing time in milliseconds")
    average_processing_time_ms: Optional[float] = Field(None, description="Average processing time per response")


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(..., description="Health status (healthy, unhealthy, degraded)")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")
    uptime_seconds: Optional[float] = Field(None, description="Service uptime in seconds")
    openai_status: Optional[str] = Field(None, description="OpenAI API connection status")


class ErrorResponse(BaseModel):
    """Response model for error responses."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")


class ConfigResponse(BaseModel):
    """Response model for configuration."""
    
    openai_model: str = Field(..., description="OpenAI model being used")
    max_tokens: int = Field(..., description="Maximum tokens for OpenAI response")
    temperature: float = Field(..., description="Temperature for OpenAI response")
    default_criteria: List[str] = Field(..., description="Default scoring criteria")
    scoring_scale: str = Field(..., description="Scoring scale")
    max_batch_size: int = Field(..., description="Maximum batch size")
    rate_limit_per_minute: int = Field(..., description="Rate limit per minute")
    environment: str = Field(..., description="Environment (development, production)") 
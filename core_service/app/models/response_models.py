from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TestResult(BaseModel):
    """Model for individual test result."""
    status: str = Field(..., description="Test status: passed|failed")
    description: str = Field(..., description="Test result description")
    reasoning: str = Field(..., description="Reasoning for the result")


class CriteriaScores(BaseModel):
    """Model for criteria scores."""
    accuracy: Optional[float] = Field(None, description="Accuracy score")
    relevance: Optional[float] = Field(None, description="Relevance score")
    clarity: Optional[float] = Field(None, description="Clarity score")
    completeness: Optional[float] = Field(None, description="Completeness score")
    coherence: Optional[float] = Field(None, description="Coherence score")


class TestExecutionResponse(BaseModel):
    """Response model for test execution."""
    test_id: str = Field(..., description="Unique test identifier")
    agent_endpoint: str = Field(..., description="Agent endpoint URL")
    test_status: str = Field(..., description="Overall test status: passed|failed")
    overall_score: float = Field(..., description="Overall score")
    criteria_scores: CriteriaScores = Field(..., description="Individual criteria scores")
    test_result: TestResult = Field(..., description="Detailed test result")
    original_prompt: str = Field(..., description="Original test prompt")
    optimized_prompt: str = Field(..., description="Optimized prompt")
    agent_response: str = Field(..., description="Agent response")
    timestamp: datetime = Field(..., description="Test timestamp")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")
    error_message: Optional[str] = Field(None, description="Error message if test failed")


class BatchTestResponse(BaseModel):
    """Response model for batch testing."""
    batch_id: str = Field(..., description="Unique batch identifier")
    total_tests: int = Field(..., description="Total number of tests")
    passed_tests: int = Field(..., description="Number of passed tests")
    failed_tests: int = Field(..., description="Number of failed tests")
    results: List[TestExecutionResponse] = Field(..., description="Individual test results")
    batch_processing_time_ms: int = Field(..., description="Total batch processing time")
    timestamp: datetime = Field(..., description="Batch timestamp")


class AgentRegistrationResponse(BaseModel):
    """Response model for agent registration."""
    agent_id: str = Field(..., description="Unique agent identifier")
    agent_endpoint: str = Field(..., description="Agent endpoint URL")
    registration_status: str = Field(..., description="Registration status")
    health_check_status: str = Field(..., description="Health check status")
    timestamp: datetime = Field(..., description="Registration timestamp")


class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    agent_endpoint: str = Field(..., description="Agent endpoint URL")
    status: str = Field(..., description="Health status: healthy|unhealthy")
    response_time_ms: Optional[int] = Field(None, description="Response time in milliseconds")
    error_message: Optional[str] = Field(None, description="Error message if unhealthy")
    timestamp: datetime = Field(..., description="Health check timestamp")


class SystemHealthResponse(BaseModel):
    """Response model for system health check."""
    status: str = Field(..., description="System status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(..., description="Health check timestamp")
    dependencies: Dict[str, str] = Field(..., description="Dependency health status")


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    timestamp: datetime = Field(..., description="Error timestamp") 
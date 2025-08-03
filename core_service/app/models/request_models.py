from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, HttpUrl


class AgentRegistrationRequest(BaseModel):
    """Request model for agent registration."""
    agent_endpoint: HttpUrl = Field(..., description="Agent endpoint URL")
    agent_description: str = Field(..., description="Description of the agent")
    system_prompt: Optional[str] = Field(None, description="System prompt for the agent")
    skills_and_tools: Optional[List[str]] = Field(default=[], description="List of skills and tools")
    test_criteria: Optional[List[str]] = Field(
        default=["accuracy", "relevance", "clarity", "completeness"],
        description="List of test criteria"
    )
    scoring_threshold: Optional[float] = Field(default=6.0, description="Scoring threshold")
    optimization_context: Optional[Dict[str, Any]] = Field(
        default={},
        description="Context for prompt optimization"
    )


class TestExecutionRequest(BaseModel):
    """Request model for test execution."""
    agent_endpoint: HttpUrl = Field(..., description="Agent endpoint URL")
    test_prompt: str = Field(..., description="Test prompt to send to agent")
    test_criteria: Optional[List[str]] = Field(
        default=["accuracy", "relevance", "clarity", "completeness"],
        description="List of test criteria"
    )
    scoring_threshold: Optional[float] = Field(default=6.0, description="Scoring threshold")
    optimization_context: Optional[Dict[str, Any]] = Field(
        default={},
        description="Context for prompt optimization"
    )


class BatchTestRequest(BaseModel):
    """Request model for batch testing."""
    tests: List[TestExecutionRequest] = Field(..., description="List of tests to execute")
    parallel_execution: Optional[bool] = Field(default=True, description="Execute tests in parallel")


class HealthCheckRequest(BaseModel):
    """Request model for health check."""
    agent_endpoint: HttpUrl = Field(..., description="Agent endpoint URL to check") 
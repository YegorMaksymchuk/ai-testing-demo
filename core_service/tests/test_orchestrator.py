import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from app.core.orchestrator import Orchestrator
from app.models.request_models import TestExecutionRequest
from app.models.response_models import TestExecutionResponse


class TestOrchestrator:
    """Test cases for the Orchestrator class."""
    
    @pytest.fixture
    def orchestrator(self):
        """Create an orchestrator instance with mocked services."""
        orchestrator = Orchestrator()
        
        # Mock the services
        orchestrator.optimizer_service = Mock()
        orchestrator.scoring_service = Mock()
        orchestrator.agent_testing_service = Mock()
        
        return orchestrator
    
    @pytest.fixture
    def test_request(self):
        """Create a test execution request."""
        return TestExecutionRequest(
            agent_endpoint="http://localhost:3000",
            test_prompt="What is the capital of France?",
            test_criteria=["accuracy", "relevance", "clarity"],
            scoring_threshold=6.0
        )
    
    @pytest.mark.asyncio
    async def test_execute_test_success(self, orchestrator, test_request):
        """Test successful test execution."""
        # Mock service responses
        orchestrator.optimizer_service.optimize_prompt = AsyncMock(return_value={
            "enhanced_prompt": "Please provide a clear answer: What is the capital of France?"
        })
        
        orchestrator.agent_testing_service.test_agent = AsyncMock(return_value={
            "response": "The capital of France is Paris."
        })
        
        orchestrator.scoring_service.score_response = AsyncMock(return_value={
            "criteria_scores": {
                "accuracy": 8.0,
                "relevance": 7.0,
                "clarity": 7.5
            },
            "reasoning": "The response is accurate and relevant."
        })
        
        # Execute test
        result = await orchestrator.execute_test(test_request)
        
        # Verify result
        assert isinstance(result, TestExecutionResponse)
        assert result.test_status == "passed"
        assert result.overall_score > 0
        assert result.original_prompt == test_request.test_prompt
        assert result.optimized_prompt == "Please provide a clear answer: What is the capital of France?"
        assert result.agent_response == "The capital of France is Paris."
    
    @pytest.mark.asyncio
    async def test_execute_test_failure(self, orchestrator, test_request):
        """Test test execution with failure."""
        # Mock service failure
        orchestrator.optimizer_service.optimize_prompt = AsyncMock(
            side_effect=Exception("Optimizer service unavailable")
        )
        
        # Execute test
        result = await orchestrator.execute_test(test_request)
        
        # Verify result
        assert isinstance(result, TestExecutionResponse)
        assert result.test_status == "failed"
        assert result.overall_score == 0.0
        assert result.error_message is not None
    
    @pytest.mark.asyncio
    async def test_calculate_overall_score(self, orchestrator):
        """Test overall score calculation."""
        from app.models.response_models import CriteriaScores
        
        # Test with all scores
        criteria_scores = CriteriaScores(
            accuracy=8.0,
            relevance=7.0,
            clarity=7.5,
            completeness=6.5
        )
        overall_score = orchestrator._calculate_overall_score(criteria_scores)
        assert overall_score == 7.25
        
        # Test with missing scores
        criteria_scores = CriteriaScores(
            accuracy=8.0,
            relevance=7.0,
            clarity=None,
            completeness=None
        )
        overall_score = orchestrator._calculate_overall_score(criteria_scores)
        assert overall_score == 7.5
        
        # Test with no scores
        criteria_scores = CriteriaScores()
        overall_score = orchestrator._calculate_overall_score(criteria_scores)
        assert overall_score == 0.0
    
    @pytest.mark.asyncio
    async def test_extract_criteria_scores(self, orchestrator):
        """Test criteria scores extraction."""
        scoring_result = {
            "criteria_scores": {
                "accuracy": 8.0,
                "relevance": 7.0,
                "clarity": 7.5,
                "completeness": 6.5,
                "coherence": 8.5
            }
        }
        
        criteria_scores = orchestrator._extract_criteria_scores(scoring_result)
        
        assert criteria_scores.accuracy == 8.0
        assert criteria_scores.relevance == 7.0
        assert criteria_scores.clarity == 7.5
        assert criteria_scores.completeness == 6.5
        assert criteria_scores.coherence == 8.5
    
    @pytest.mark.asyncio
    async def test_health_check(self, orchestrator):
        """Test health check functionality."""
        # Mock service health checks
        orchestrator.optimizer_service.health_check = AsyncMock(return_value=True)
        orchestrator.scoring_service.health_check = AsyncMock(return_value=True)
        
        health_status = await orchestrator.health_check()
        
        assert health_status["status"] == "healthy"
        assert "optimizer" in health_status["services"]
        assert "scorer" in health_status["services"]
        assert health_status["services"]["optimizer"] == "healthy"
        assert health_status["services"]["scorer"] == "healthy" 
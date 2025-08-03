"""
Unit tests for the scoring service.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from services.scoring_service import ScoringService
from models.response_models import ScoringResponse, BatchScoringResponse


class TestScoringService:
    """Test cases for ScoringService."""
    
    @pytest.fixture
    async def scoring_service(self):
        """Create a scoring service instance for testing."""
        service = ScoringService()
        # Mock the OpenAI client
        service.client = AsyncMock()
        return service
    
    @pytest.mark.asyncio
    async def test_initialize_success(self, scoring_service):
        """Test successful initialization."""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
            await scoring_service.initialize()
            assert scoring_service.client is not None
    
    @pytest.mark.asyncio
    async def test_initialize_missing_api_key(self, scoring_service):
        """Test initialization with missing API key."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable is required"):
                await scoring_service.initialize()
    
    @pytest.mark.asyncio
    async def test_build_scoring_prompt(self, scoring_service):
        """Test prompt building."""
        response = "This is a test response"
        criteria = ["accuracy", "relevance"]
        context = "Test context"
        
        prompt = scoring_service._build_scoring_prompt(response, criteria, context)
        
        assert "accuracy, relevance" in prompt
        assert response in prompt
        assert context in prompt
        assert "JSON format" in prompt
    
    @pytest.mark.asyncio
    async def test_parse_scoring_response_valid(self, scoring_service):
        """Test parsing valid scoring response."""
        response_text = '''
        {
            "score": 8.5,
            "reasoning": "This is a good response",
            "criteria_scores": {
                "accuracy": 9.0,
                "relevance": 8.0
            },
            "confidence": 0.9
        }
        '''
        
        result = scoring_service._parse_scoring_response(response_text)
        
        assert result.score == 8.5
        assert result.reasoning == "This is a good response"
        assert result.criteria_scores["accuracy"] == 9.0
        assert result.criteria_scores["relevance"] == 8.0
        assert result.confidence == 0.9
    
    @pytest.mark.asyncio
    async def test_parse_scoring_response_invalid_json(self, scoring_service):
        """Test parsing invalid JSON response."""
        response_text = "Invalid JSON"
        
        with pytest.raises(ValueError, match="Invalid JSON response"):
            scoring_service._parse_scoring_response(response_text)
    
    @pytest.mark.asyncio
    async def test_parse_scoring_response_missing_fields(self, scoring_service):
        """Test parsing response with missing required fields."""
        response_text = '{"reasoning": "Test"}'
        
        with pytest.raises(ValueError, match="Missing required fields"):
            scoring_service._parse_scoring_response(response_text)
    
    @pytest.mark.asyncio
    async def test_parse_scoring_response_invalid_score(self, scoring_service):
        """Test parsing response with invalid score."""
        response_text = '{"score": 15, "reasoning": "Test"}'
        
        with pytest.raises(ValueError, match="Score 15 is outside valid range"):
            scoring_service._parse_scoring_response(response_text)
    
    @pytest.mark.asyncio
    async def test_score_response_success(self, scoring_service):
        """Test successful single response scoring."""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '''
        {
            "score": 7.5,
            "reasoning": "Good response",
            "criteria_scores": {"accuracy": 8.0},
            "confidence": 0.8
        }
        '''
        scoring_service.client.chat.completions.create.return_value = mock_response
        
        result = await scoring_service.score_response("Test response")
        
        assert isinstance(result, ScoringResponse)
        assert result.score == 7.5
        assert result.reasoning == "Good response"
        assert result.model_used == scoring_service.model
    
    @pytest.mark.asyncio
    async def test_score_batch_success(self, scoring_service):
        """Test successful batch scoring."""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '''
        {
            "score": 7.5,
            "reasoning": "Good response",
            "criteria_scores": {"accuracy": 8.0},
            "confidence": 0.8
        }
        '''
        scoring_service.client.chat.completions.create.return_value = mock_response
        
        responses = ["Response 1", "Response 2"]
        result = await scoring_service.score_batch(responses)
        
        assert isinstance(result, BatchScoringResponse)
        assert result.total_processed == 2
        assert result.successful == 2
        assert result.failed == 0
        assert len(result.results) == 2
    
    @pytest.mark.asyncio
    async def test_rate_limit_check(self, scoring_service):
        """Test rate limiting."""
        # Fill up the rate limit
        for _ in range(scoring_service.rate_limit_per_minute):
            scoring_service._check_rate_limit()
        
        # Next request should fail
        with pytest.raises(Exception, match="Rate limit exceeded"):
            scoring_service._check_rate_limit()
    
    @pytest.mark.asyncio
    async def test_cleanup(self, scoring_service):
        """Test cleanup method."""
        scoring_service.client = AsyncMock()
        
        await scoring_service.cleanup()
        
        scoring_service.client.close.assert_called_once()


@pytest.mark.asyncio
async def test_scoring_service_integration():
    """Integration test for scoring service."""
    # This test would require a real OpenAI API key
    # and should be run separately in integration tests
    pass 
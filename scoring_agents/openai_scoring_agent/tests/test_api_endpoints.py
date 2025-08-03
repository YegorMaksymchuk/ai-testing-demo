"""
API endpoint tests for the AI Scoring Agent.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock

from main import app
from models.request_models import ScoringRequest, BatchScoringRequest
from models.response_models import ScoringResponse, BatchScoringResponse


class TestAPIEndpoints:
    """Test cases for API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "AI Scoring Agent API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"
    
    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "ai-scoring-agent"
        assert data["version"] == "1.0.0"
    
    def test_config_endpoint(self, client):
        """Test the config endpoint."""
        response = client.get("/config")
        assert response.status_code == 200
        data = response.json()
        assert "openai_model" in data
        assert "max_tokens" in data
        assert "temperature" in data
        assert "default_criteria" in data
    
    def test_api_info_endpoint(self, client):
        """Test the api-info endpoint."""
        response = client.get("/api-info")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "AI Scoring Agent API"
        assert data["version"] == "1.0.0"
        assert "documentation" in data
        assert "endpoints" in data
    
    def test_openapi_yaml_endpoint(self, client):
        """Test the openapi.yaml endpoint."""
        response = client.get("/openapi.yaml")
        assert response.status_code == 200
        content = response.text
        assert "openapi:" in content
        assert "AI Scoring Agent API" in content
    
    @patch('main.scoring_service')
    def test_score_endpoint_success(self, mock_scoring_service, client):
        """Test successful scoring endpoint."""
        # Mock the scoring service
        mock_service = AsyncMock()
        mock_response = ScoringResponse(
            score=8.5,
            reasoning="Good response",
            criteria_scores={"accuracy": 9.0, "relevance": 8.0},
            confidence=0.9,
            model_used="gpt-4",
            processing_time_ms=1500.0
        )
        mock_service.score_response.return_value = mock_response
        mock_scoring_service.return_value = mock_service
        
        # Test request
        request_data = {
            "response": "This is a test response",
            "criteria": ["accuracy", "relevance"],
            "context": "Test context"
        }
        
        response = client.post("/score", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["score"] == 8.5
        assert data["reasoning"] == "Good response"
        assert data["model_used"] == "gpt-4"
    
    @patch('main.scoring_service')
    def test_score_endpoint_validation_error(self, mock_scoring_service, client):
        """Test scoring endpoint with validation error."""
        # Test with empty response
        request_data = {
            "response": "",
            "criteria": ["accuracy"]
        }
        
        response = client.post("/score", json=request_data)
        assert response.status_code == 422
    
    @patch('main.scoring_service')
    def test_score_batch_endpoint_success(self, mock_scoring_service, client):
        """Test successful batch scoring endpoint."""
        # Mock the scoring service
        mock_service = AsyncMock()
        mock_response = BatchScoringResponse(
            results=[
                {
                    "response": "Response 1",
                    "score": 8.0,
                    "reasoning": "Good response",
                    "criteria_scores": {"accuracy": 8.5},
                    "confidence": 0.8
                },
                {
                    "response": "Response 2",
                    "score": 7.5,
                    "reasoning": "Decent response",
                    "criteria_scores": {"accuracy": 7.0},
                    "confidence": 0.7
                }
            ],
            total_processed=2,
            successful=2,
            failed=0,
            model_used="gpt-4",
            total_processing_time_ms=3000.0,
            average_processing_time_ms=1500.0
        )
        mock_service.score_batch.return_value = mock_response
        mock_scoring_service.return_value = mock_service
        
        # Test request
        request_data = {
            "responses": ["Response 1", "Response 2"],
            "criteria": ["accuracy", "relevance"],
            "context": "Test context"
        }
        
        response = client.post("/score/batch", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["total_processed"] == 2
        assert data["successful"] == 2
        assert data["failed"] == 0
        assert len(data["results"]) == 2
    
    @patch('main.scoring_service')
    def test_score_batch_endpoint_validation_error(self, mock_scoring_service, client):
        """Test batch scoring endpoint with validation error."""
        # Test with empty responses list
        request_data = {
            "responses": [],
            "criteria": ["accuracy"]
        }
        
        response = client.post("/score/batch", json=request_data)
        assert response.status_code == 422
    
    @patch('main.scoring_service')
    def test_score_endpoint_service_unavailable(self, mock_scoring_service, client):
        """Test scoring endpoint when service is unavailable."""
        # Set scoring service to None
        mock_scoring_service.return_value = None
        
        request_data = {
            "response": "Test response",
            "criteria": ["accuracy"]
        }
        
        response = client.post("/score", json=request_data)
        assert response.status_code == 503
        assert "Scoring service not available" in response.json()["detail"]
    
    def test_score_endpoint_invalid_criteria(self, client):
        """Test scoring endpoint with invalid criteria."""
        request_data = {
            "response": "Test response",
            "criteria": ["invalid_criterion"]
        }
        
        response = client.post("/score", json=request_data)
        assert response.status_code == 422


class TestRequestModels:
    """Test cases for request models."""
    
    def test_scoring_request_valid(self):
        """Test valid scoring request."""
        request = ScoringRequest(
            response="Test response",
            criteria=["accuracy", "relevance"],
            context="Test context"
        )
        assert request.response == "Test response"
        assert request.criteria == ["accuracy", "relevance"]
        assert request.context == "Test context"
    
    def test_scoring_request_empty_response(self):
        """Test scoring request with empty response."""
        with pytest.raises(ValueError, match="Response cannot be empty"):
            ScoringRequest(response="")
    
    def test_scoring_request_invalid_criteria(self):
        """Test scoring request with invalid criteria."""
        with pytest.raises(ValueError, match="Invalid criterion"):
            ScoringRequest(
                response="Test response",
                criteria=["invalid_criterion"]
            )
    
    def test_batch_scoring_request_valid(self):
        """Test valid batch scoring request."""
        request = BatchScoringRequest(
            responses=["Response 1", "Response 2"],
            criteria=["accuracy", "relevance"],
            context="Test context"
        )
        assert len(request.responses) == 2
        assert request.criteria == ["accuracy", "relevance"]
        assert request.context == "Test context"
    
    def test_batch_scoring_request_empty_responses(self):
        """Test batch scoring request with empty responses."""
        with pytest.raises(ValueError, match="At least one response is required"):
            BatchScoringRequest(responses=[])
    
    def test_batch_scoring_request_empty_response_item(self):
        """Test batch scoring request with empty response item."""
        with pytest.raises(ValueError, match="Response at index 0 cannot be empty"):
            BatchScoringRequest(responses=["", "Response 2"])


if __name__ == "__main__":
    pytest.main([__file__]) 
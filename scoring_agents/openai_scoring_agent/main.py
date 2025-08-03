"""
AI Scoring Agent - Main Application
A FastAPI-based service for scoring AI responses using OpenAI.
"""

import asyncio
import logging
import os
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

from services.scoring_service import ScoringService
from models.request_models import ScoringRequest, BatchScoringRequest
from models.response_models import ScoringResponse, BatchScoringResponse, HealthResponse
from utils.logging_config import setup_logging
from utils.error_handlers import setup_error_handlers

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global scoring service
scoring_service: Optional[ScoringService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global scoring_service
    
    # Startup
    logger.info("Starting AI Scoring Agent...")
    
    # Initialize scoring service
    try:
        scoring_service = ScoringService()
        await scoring_service.initialize()
        logger.info("Scoring service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize scoring service: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Scoring Agent...")
    if scoring_service:
        await scoring_service.cleanup()


# Create FastAPI app
app = FastAPI(
    title="AI Scoring Agent",
    description="""
    A FastAPI-based service for scoring AI responses using OpenAI. 
    This service provides both single and batch scoring capabilities with configurable criteria and comprehensive error handling.
    
    ## Features
    - **Single Response Scoring**: Score individual AI responses with detailed reasoning
    - **Batch Processing**: Score multiple responses concurrently with progress tracking
    - **Configurable Criteria**: Support for multiple scoring criteria (accuracy, relevance, clarity, completeness, coherence)
    - **Rate Limiting**: Built-in rate limiting to respect OpenAI API limits
    - **Error Handling**: Comprehensive error handling with retry logic
    - **Health Monitoring**: Health check endpoints for monitoring
    
    ## Authentication
    This API requires an OpenAI API key to be configured in the environment.
    
    ## Rate Limiting
    The API implements rate limiting to respect OpenAI API limits. Default is 60 requests per minute.
    
    ## Scoring Criteria
    Available scoring criteria:
    - **accuracy**: How correct and factual is the response
    - **relevance**: How well does it address the question/context
    - **clarity**: How clear and well-structured is the response
    - **completeness**: How comprehensive is the response
    - **coherence**: How logical and coherent is the response
    """,
    version="1.0.0",
    contact={
        "name": "AI Scoring Agent Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {"url": "http://localhost:8000", "description": "Local development server"},
        {"url": "https://api.example.com", "description": "Production server"},
    ],
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup error handlers
setup_error_handlers(app)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "message": "AI Scoring Agent API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/landing")
async def landing_page():
    """Serve the landing page."""
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="ai-scoring-agent",
        version="1.0.0"
    )


@app.post("/score", response_model=ScoringResponse)
async def score_response(request: ScoringRequest):
    """
    Score a single AI response.
    
    Args:
        request: The scoring request containing the response to evaluate
        
    Returns:
        ScoringResponse: The scoring result with score and reasoning
    """
    if not scoring_service:
        raise HTTPException(status_code=503, detail="Scoring service not available")
    
    try:
        result = await scoring_service.score_response(
            response=request.response,
            criteria=request.criteria,
            context=request.context
        )
        return result
    except Exception as e:
        logger.error(f"Error scoring response: {e}")
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")


@app.post("/score/batch", response_model=BatchScoringResponse)
async def score_batch(request: BatchScoringRequest, background_tasks: BackgroundTasks):
    """
    Score multiple AI responses in batch.
    
    Args:
        request: The batch scoring request
        background_tasks: FastAPI background tasks
        
    Returns:
        BatchScoringResponse: The batch scoring results
    """
    if not scoring_service:
        raise HTTPException(status_code=503, detail="Scoring service not available")
    
    try:
        # Validate batch size
        if len(request.responses) > int(os.getenv("MAX_BATCH_SIZE", 100)):
            raise HTTPException(
                status_code=400, 
                detail=f"Batch size exceeds maximum of {os.getenv('MAX_BATCH_SIZE', 100)}"
            )
        
        results = await scoring_service.score_batch(
            responses=request.responses,
            criteria=request.criteria,
            context=request.context
        )
        return results
    except Exception as e:
        logger.error(f"Error scoring batch: {e}")
        raise HTTPException(status_code=500, detail=f"Batch scoring failed: {str(e)}")


@app.get("/config")
async def get_config():
    """Get current configuration."""
    return {
        "openai_model": os.getenv("OPENAI_MODEL", "gpt-4"),
        "max_tokens": int(os.getenv("OPENAI_MAX_TOKENS", 2000)),
        "temperature": float(os.getenv("OPENAI_TEMPERATURE", 0.0)),
        "default_criteria": os.getenv("DEFAULT_SCORING_CRITERIA", "accuracy,relevance,clarity").split(","),
        "scoring_scale": os.getenv("SCORING_SCALE", "1-10"),
        "max_batch_size": int(os.getenv("MAX_BATCH_SIZE", 100)),
        "rate_limit_per_minute": int(os.getenv("RATE_LIMIT_PER_MINUTE", 60)),
        "environment": os.getenv("ENVIRONMENT", "development")
    }


@app.get("/openapi.yaml")
async def get_openapi_yaml():
    """Get OpenAPI specification in YAML format."""
    from fastapi.openapi.utils import get_openapi
    
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    import yaml
    return yaml.dump(openapi_schema, default_flow_style=False)


@app.get("/api-info")
async def get_api_info():
    """Get API information and links."""
    return {
        "name": "AI Scoring Agent API",
        "version": "1.0.0",
        "description": "A service for scoring AI responses using OpenAI",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json",
            "openapi_yaml": "/openapi.yaml"
        },
        "endpoints": {
            "health": "/health",
            "config": "/config",
            "single_scoring": "/score",
            "batch_scoring": "/score/batch"
        },
        "contact": {
            "name": "AI Scoring Agent Support",
            "email": "support@example.com"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        workers=int(os.getenv("WORKERS", 1)),
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    ) 
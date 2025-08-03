import asyncio
import logging
import os
from typing import Dict, Any, List
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.core.orchestrator import Orchestrator
from app.models.request_models import (
    AgentRegistrationRequest, 
    TestExecutionRequest, 
    BatchTestRequest,
    HealthCheckRequest
)
from app.models.response_models import (
    TestExecutionResponse, 
    BatchTestResponse, 
    AgentRegistrationResponse,
    HealthCheckResponse,
    SystemHealthResponse
)
from app.utils.logging_config import setup_logging
from app.utils.error_handlers import setup_error_handlers
from app.config import get_settings

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global orchestrator
orchestrator: Orchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global orchestrator
    
    # Startup
    logger.info("Starting Orchestrator Agent...")
    
    # Initialize orchestrator
    try:
        orchestrator = Orchestrator()
        logger.info("Orchestrator initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize orchestrator: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Orchestrator Agent...")


# Create FastAPI app
app = FastAPI(
    title="Orchestrator Agent",
    description="""
    A central coordination service that automates the testing and evaluation of AI agents through a three-stage pipeline: 
    prompt optimization, agent testing, and response scoring. It provides a standardized framework for assessing agent 
    performance across multiple criteria.
    
    ## Features
    - **Agent Registration**: Register and validate AI agents for testing
    - **Prompt Optimization**: Automatically optimize prompts using the prompt optimizer service
    - **Agent Testing**: Execute tests against AI agents with optimized prompts
    - **Response Scoring**: Score agent responses using the scoring service
    - **Batch Testing**: Execute multiple tests in parallel
    - **Health Monitoring**: Monitor the health of all services and agents
    
    ## Workflow
    1. Register an agent with its endpoint and capabilities
    2. Execute tests with prompts that get optimized automatically
    3. Receive comprehensive scoring and evaluation results
    4. Monitor test results and agent performance
    
    ## Dependencies
    - Prompt Optimizer Service (Port 8001)
    - Scoring Service (Port 8000)
    """,
    version="1.0.0",
    contact={
        "name": "Orchestrator Agent Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {"url": "http://localhost:8003", "description": "Local development server"},
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
        "message": "Orchestrator Agent API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", response_model=SystemHealthResponse)
async def health_check():
    """Health check endpoint."""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    
    try:
        health_status = await orchestrator.health_check()
        return SystemHealthResponse(
            status=health_status["status"],
            service="orchestrator-agent",
            version="1.0.0",
            timestamp=health_status["timestamp"],
            dependencies=health_status["services"]
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


@app.post("/register-agent", response_model=AgentRegistrationResponse)
async def register_agent(request: AgentRegistrationRequest):
    """
    Register an AI agent for testing.
    
    Args:
        request: The agent registration request
        
    Returns:
        AgentRegistrationResponse: The registration result
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    
    try:
        # Perform health check on the agent
        health_result = await orchestrator.agent_testing_service.health_check(
            str(request.agent_endpoint)
        )
        
        # Create registration response
        from datetime import datetime
        return AgentRegistrationResponse(
            agent_id=str(hash(str(request.agent_endpoint))),  # Simple ID generation
            agent_endpoint=str(request.agent_endpoint),
            registration_status="registered",
            health_check_status=health_result["status"],
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Agent registration failed: {e}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@app.post("/test-agent", response_model=TestExecutionResponse)
async def test_agent(request: TestExecutionRequest):
    """
    Execute a single test on an AI agent.
    
    Args:
        request: The test execution request
        
    Returns:
        TestExecutionResponse: The test execution result
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    
    try:
        result = await orchestrator.execute_test(request)
        return result
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Test execution failed: {str(e)}")


@app.post("/test-batch", response_model=BatchTestResponse)
async def test_batch(request: BatchTestRequest, background_tasks: BackgroundTasks):
    """
    Execute multiple tests in batch.
    
    Args:
        request: The batch test request
        background_tasks: FastAPI background tasks
        
    Returns:
        BatchTestResponse: The batch test results
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    
    try:
        # Validate batch size
        max_batch_size = get_settings().orchestrator.max_concurrent_tests
        if len(request.tests) > max_batch_size:
            raise HTTPException(
                status_code=400, 
                detail=f"Batch size exceeds maximum of {max_batch_size}"
            )
        
        # Execute batch tests
        results = await orchestrator.execute_batch_tests(request.tests)
        
        # Calculate batch statistics
        from datetime import datetime
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.test_status == "passed")
        failed_tests = total_tests - passed_tests
        total_processing_time = sum(r.processing_time_ms for r in results)
        
        return BatchTestResponse(
            batch_id=str(hash(str(results))),  # Simple ID generation
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            results=results,
            batch_processing_time_ms=total_processing_time,
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Batch test execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Batch test execution failed: {str(e)}")


@app.post("/health-check-agent", response_model=HealthCheckResponse)
async def health_check_agent(request: HealthCheckRequest):
    """
    Check the health of a specific agent.
    
    Args:
        request: The health check request
        
    Returns:
        HealthCheckResponse: The health check result
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    
    try:
        health_result = await orchestrator.agent_testing_service.health_check(
            str(request.agent_endpoint)
        )
        
        from datetime import datetime
        return HealthCheckResponse(
            agent_endpoint=str(request.agent_endpoint),
            status=health_result["status"],
            response_time_ms=health_result.get("response_time_ms"),
            error_message=health_result.get("error_message"),
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Agent health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.get("/config")
async def get_config():
    """Get current configuration."""
    settings = get_settings()
    return {
        "orchestrator": {
            "host": settings.orchestrator.host,
            "port": settings.orchestrator.port,
            "timeout": settings.orchestrator.timeout,
            "max_concurrent_tests": settings.orchestrator.max_concurrent_tests
        },
        "services": {
            "optimizer": {
                "url": settings.services.optimizer.url,
                "timeout": settings.services.optimizer.timeout
            },
            "scorer": {
                "url": settings.services.scorer.url,
                "timeout": settings.services.scorer.timeout
            }
        },
        "scoring": {
            "default_threshold": settings.scoring.default_threshold,
            "criteria": settings.scoring.criteria
        }
    }


@app.get("/api-info")
async def get_api_info():
    """Get API information and links."""
    return {
        "name": "Orchestrator Agent API",
        "version": "1.0.0",
        "description": "A central coordination service for AI agent testing and evaluation",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        },
        "endpoints": {
            "health": "/health",
            "config": "/config",
            "register_agent": "/register-agent",
            "test_agent": "/test-agent",
            "test_batch": "/test-batch",
            "health_check_agent": "/health-check-agent"
        },
        "contact": {
            "name": "Orchestrator Agent Support",
            "email": "support@example.com"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    }


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.orchestrator.host,
        port=settings.orchestrator.port,
        workers=1,
        log_level=settings.logging.level.lower()
    ) 
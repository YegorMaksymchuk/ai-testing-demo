import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.models.response_models import ErrorResponse
from datetime import datetime

logger = logging.getLogger(__name__)


def setup_error_handlers(app: FastAPI):
    """Setup error handlers for the FastAPI application."""
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="Internal server error",
                detail=str(exc),
                timestamp=datetime.now()
            ).dict()
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Handle ValueError exceptions."""
        logger.error(f"ValueError: {exc}")
        
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                error="Invalid input",
                detail=str(exc),
                timestamp=datetime.now()
            ).dict()
        )
    
    @app.exception_handler(TimeoutError)
    async def timeout_error_handler(request: Request, exc: TimeoutError):
        """Handle TimeoutError exceptions."""
        logger.error(f"TimeoutError: {exc}")
        
        return JSONResponse(
            status_code=408,
            content=ErrorResponse(
                error="Request timeout",
                detail=str(exc),
                timestamp=datetime.now()
            ).dict()
        ) 
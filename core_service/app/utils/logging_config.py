import logging
import sys
from app.config import get_settings


def setup_logging():
    """Setup logging configuration."""
    settings = get_settings()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.logging.level.upper()),
        format=settings.logging.format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("orchestrator.log")
        ]
    )
    
    # Set specific logger levels
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    # Create logger for the application
    logger = logging.getLogger("orchestrator")
    logger.setLevel(getattr(logging, settings.logging.level.upper()))
    
    return logger 
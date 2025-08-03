import os
import yaml
from typing import List
from pydantic import BaseModel, Field
from functools import lru_cache


class OrchestratorConfig(BaseModel):
    """Configuration for the orchestrator service."""
    host: str = Field(default="0.0.0.0", description="Host to bind to")
    port: int = Field(default=8002, description="Port to bind to")
    timeout: int = Field(default=30, description="Default timeout in seconds")
    max_concurrent_tests: int = Field(default=100, description="Maximum concurrent tests")


class ServiceConfig(BaseModel):
    """Configuration for external services."""
    url: str = Field(..., description="Service URL")
    timeout: int = Field(default=15, description="Service timeout in seconds")


class ServicesConfig(BaseModel):
    """Configuration for all external services."""
    optimizer: ServiceConfig
    scorer: ServiceConfig


class ScoringConfig(BaseModel):
    """Configuration for scoring."""
    default_threshold: float = Field(default=6.0, description="Default scoring threshold")
    criteria: List[str] = Field(
        default=["accuracy", "relevance", "clarity", "completeness"],
        description="Default scoring criteria"
    )


class DatabaseConfig(BaseModel):
    """Configuration for database."""
    url: str = Field(default="postgresql://user:password@localhost/orchestrator_db")
    echo: bool = Field(default=False, description="Enable SQLAlchemy echo")


class RedisConfig(BaseModel):
    """Configuration for Redis."""
    url: str = Field(default="redis://localhost:6379")


class LoggingConfig(BaseModel):
    """Configuration for logging."""
    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Logging format"
    )


class Settings(BaseModel):
    """Main application settings."""
    orchestrator: OrchestratorConfig
    services: ServicesConfig
    scoring: ScoringConfig
    database: DatabaseConfig
    redis: RedisConfig
    logging: LoggingConfig


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings from config file and environment variables.
    
    Returns:
        Settings object with all configuration
    """
    # Load config from file
    config_file = os.getenv("CONFIG_FILE", "config.yaml")
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)
    else:
        config_data = {}
    
    # Override with environment variables
    env_config = {
        "orchestrator": {
            "host": os.getenv("ORCHESTRATOR_HOST", "0.0.0.0"),
            "port": int(os.getenv("ORCHESTRATOR_PORT", "8002")),
            "timeout": int(os.getenv("ORCHESTRATOR_TIMEOUT", "30")),
            "max_concurrent_tests": int(os.getenv("MAX_CONCURRENT_TESTS", "100"))
        },
        "services": {
            "optimizer": {
                "url": os.getenv("OPTIMIZER_URL", "http://localhost:8001"),
                "timeout": int(os.getenv("OPTIMIZER_TIMEOUT", "15"))
            },
            "scorer": {
                "url": os.getenv("SCORER_URL", "http://localhost:8000"),
                "timeout": int(os.getenv("SCORER_TIMEOUT", "20"))
            }
        },
        "scoring": {
            "default_threshold": float(os.getenv("DEFAULT_SCORING_THRESHOLD", "6.0")),
            "criteria": os.getenv("DEFAULT_SCORING_CRITERIA", "accuracy,relevance,clarity,completeness").split(",")
        },
        "database": {
            "url": os.getenv("DATABASE_URL", "postgresql://user:password@localhost/orchestrator_db"),
            "echo": os.getenv("DATABASE_ECHO", "false").lower() == "true"
        },
        "redis": {
            "url": os.getenv("REDIS_URL", "redis://localhost:6379")
        },
        "logging": {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "format": os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        }
    }
    
    # Merge config file with environment variables
    def merge_configs(file_config, env_config):
        result = env_config.copy()
        for key, value in file_config.items():
            if key in result and isinstance(value, dict) and isinstance(result[key], dict):
                result[key] = merge_configs(value, result[key])
            else:
                result[key] = value
        return result
    
    final_config = merge_configs(config_data, env_config)
    
    return Settings(**final_config) 
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import time
import logging
from datetime import datetime

from .models.bdd_generator import BDDGenerator
from .utils.validators import validate_requirements
from .utils.formatters import format_gherkin, format_json_output

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BDD Scenario Generator AI Agent",
    description="AI agent that generates BDD scenarios from natural language requirements",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize BDD generator
bdd_generator = BDDGenerator()

class RequirementsRequest(BaseModel):
    requirements: str = Field(..., min_length=10, max_length=10000, description="Natural language requirements text")
    options: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Generation options")
    metadata: Optional[Dict[str, str]] = Field(default_factory=dict, description="Request metadata")

class BDDScenario(BaseModel):
    feature: str
    scenario: str
    given: List[str]
    when: List[str]
    then: List[str]
    examples: Optional[List[Dict[str, str]]] = None
    gherkin: str

class BDDResponse(BaseModel):
    status: str
    scenarios: List[BDDScenario]
    metadata: Dict[str, Any]
    warnings: List[str] = []
    errors: List[str] = []

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "BDD Scenario Generator AI Agent",
        "version": "1.0.0",
        "status": "healthy",
        "endpoint": "/bdd-from-text"
    }

@app.post("/bdd-from-text", response_model=BDDResponse)
async def generate_bdd_scenarios(
    request: RequirementsRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate BDD scenarios from natural language requirements
    
    Args:
        request: RequirementsRequest containing the requirements text and options
        
    Returns:
        BDDResponse with generated scenarios and metadata
    """
    start_time = time.time()
    
    try:
        # Validate input requirements
        validation_result = validate_requirements(request.requirements)
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["errors"])
        
        # Extract options with defaults
        options = {
            "include_negative_scenarios": True,
            "output_format": "both",
            "max_scenarios_per_requirement": 5,
            "include_examples": True,
            **request.options
        }
        
        # Generate BDD scenarios
        logger.info(f"Generating BDD scenarios for requirements: {len(request.requirements)} characters")
        
        scenarios_data = await bdd_generator.generate_scenarios(
            requirements=request.requirements,
            options=options
        )
        
        # Format scenarios
        formatted_scenarios = []
        for scenario_data in scenarios_data:
            gherkin_text = format_gherkin(scenario_data)
            
            scenario = BDDScenario(
                feature=scenario_data.get("feature", "Generated Feature"),
                scenario=scenario_data.get("scenario", "Generated Scenario"),
                given=scenario_data.get("given", []),
                when=scenario_data.get("when", []),
                then=scenario_data.get("then", []),
                examples=scenario_data.get("examples"),
                gherkin=gherkin_text
            )
            formatted_scenarios.append(scenario)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Prepare metadata
        metadata = {
            "processing_time_ms": round(processing_time, 2),
            "scenarios_generated": len(formatted_scenarios),
            "quality_score": bdd_generator.calculate_quality_score(formatted_scenarios),
            "timestamp": datetime.utcnow().isoformat(),
            "input_length": len(request.requirements),
            "options_used": options
        }
        
        # Add request metadata if provided
        if request.metadata:
            metadata.update(request.metadata)
        
        logger.info(f"Successfully generated {len(formatted_scenarios)} scenarios in {processing_time:.2f}ms")
        
        return BDDResponse(
            status="success",
            scenarios=formatted_scenarios,
            metadata=metadata,
            warnings=bdd_generator.get_warnings(),
            errors=[]
        )
        
    except Exception as e:
        logger.error(f"Error generating BDD scenarios: {str(e)}")
        processing_time = (time.time() - start_time) * 1000
        
        return BDDResponse(
            status="error",
            scenarios=[],
            metadata={
                "processing_time_ms": round(processing_time, 2),
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            },
            warnings=[],
            errors=[str(e)]
        )

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "model_loaded": bdd_generator.is_model_loaded()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003) 
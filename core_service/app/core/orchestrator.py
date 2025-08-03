import logging
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from app.services.prompt_optimizer_service import PromptOptimizerService
from app.services.scoring_service import ScoringService
from app.services.agent_testing_service import AgentTestingService
from app.models.request_models import TestExecutionRequest
from app.models.response_models import TestExecutionResponse, TestResult, CriteriaScores
from app.config import get_settings

logger = logging.getLogger(__name__)


class Orchestrator:
    """Main orchestrator that coordinates testing workflows."""
    
    def __init__(self):
        self.settings = get_settings()
        self.optimizer_service = PromptOptimizerService()
        self.scoring_service = ScoringService()
        self.agent_testing_service = AgentTestingService()
        
    async def execute_test(self, request: TestExecutionRequest) -> TestExecutionResponse:
        """
        Execute a complete test workflow.
        
        Args:
            request: The test execution request
            
        Returns:
            TestExecutionResponse with complete test results
        """
        start_time = datetime.now()
        test_id = str(uuid.uuid4())
        
        try:
            logger.info(f"Starting test execution {test_id} for agent {request.agent_endpoint}")
            
            # Step 1: Optimize the prompt
            logger.info("Step 1: Optimizing prompt")
            optimization_result = await self.optimizer_service.optimize_prompt(
                prompt=request.test_prompt,
                context=request.optimization_context
            )
            optimized_prompt = optimization_result["enhanced_prompt"]
            
            # Step 2: Test the agent
            logger.info("Step 2: Testing agent")
            agent_result = await self.agent_testing_service.test_agent(
                agent_endpoint=str(request.agent_endpoint),
                prompt=optimized_prompt
            )
            agent_response = agent_result["response"]
            
            # Step 3: Score the response
            logger.info("Step 3: Scoring response")
            scoring_result = await self.scoring_service.score_response(
                response=agent_response,
                criteria=request.test_criteria,
                context={"original_prompt": request.test_prompt, "optimized_prompt": optimized_prompt}
            )
            
            # Step 4: Process results
            logger.info("Step 4: Processing results")
            end_time = datetime.now()
            processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            # Extract scores
            criteria_scores = self._extract_criteria_scores(scoring_result)
            overall_score = self._calculate_overall_score(criteria_scores)
            
            # Determine test status
            test_status = "passed" if overall_score >= request.scoring_threshold else "failed"
            
            # Create test result
            test_result = TestResult(
                status=test_status,
                description=f"Test {'passed' if test_status == 'passed' else 'failed'} with score {overall_score:.2f}",
                reasoning=scoring_result.get("reasoning", "No reasoning provided")
            )
            
            logger.info(f"Test {test_id} completed with status: {test_status}, score: {overall_score}")
            
            return TestExecutionResponse(
                test_id=test_id,
                agent_endpoint=str(request.agent_endpoint),
                test_status=test_status,
                overall_score=overall_score,
                criteria_scores=criteria_scores,
                test_result=test_result,
                original_prompt=request.test_prompt,
                optimized_prompt=optimized_prompt,
                agent_response=agent_response,
                timestamp=end_time,
                processing_time_ms=processing_time_ms
            )
            
        except Exception as e:
            logger.error(f"Test {test_id} failed: {e}")
            end_time = datetime.now()
            processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            return TestExecutionResponse(
                test_id=test_id,
                agent_endpoint=str(request.agent_endpoint),
                test_status="failed",
                overall_score=0.0,
                criteria_scores=CriteriaScores(),
                test_result=TestResult(
                    status="failed",
                    description="Test failed due to error",
                    reasoning=str(e)
                ),
                original_prompt=request.test_prompt,
                optimized_prompt=request.test_prompt,  # Fallback to original
                agent_response="",
                timestamp=end_time,
                processing_time_ms=processing_time_ms,
                error_message=str(e)
            )
    
    async def execute_batch_tests(self, requests: List[TestExecutionRequest]) -> List[TestExecutionResponse]:
        """
        Execute multiple tests in parallel.
        
        Args:
            requests: List of test execution requests
            
        Returns:
            List of test execution responses
        """
        logger.info(f"Starting batch execution of {len(requests)} tests")
        
        # Execute tests in parallel
        tasks = [self.execute_test(request) for request in requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Test {i} failed with exception: {result}")
                # Create error response
                error_response = TestExecutionResponse(
                    test_id=str(uuid.uuid4()),
                    agent_endpoint=str(requests[i].agent_endpoint),
                    test_status="failed",
                    overall_score=0.0,
                    criteria_scores=CriteriaScores(),
                    test_result=TestResult(
                        status="failed",
                        description="Test failed due to exception",
                        reasoning=str(result)
                    ),
                    original_prompt=requests[i].test_prompt,
                    optimized_prompt=requests[i].test_prompt,
                    agent_response="",
                    timestamp=datetime.now(),
                    processing_time_ms=0,
                    error_message=str(result)
                )
                processed_results.append(error_response)
            else:
                processed_results.append(result)
        
        logger.info(f"Batch execution completed with {len(processed_results)} results")
        return processed_results
    
    def _extract_criteria_scores(self, scoring_result: Dict[str, Any]) -> CriteriaScores:
        """Extract criteria scores from scoring result."""
        scores = scoring_result.get("criteria_scores", {})
        
        return CriteriaScores(
            accuracy=scores.get("accuracy"),
            relevance=scores.get("relevance"),
            clarity=scores.get("clarity"),
            completeness=scores.get("completeness"),
            coherence=scores.get("coherence")
        )
    
    def _calculate_overall_score(self, criteria_scores: CriteriaScores) -> float:
        """Calculate overall score from criteria scores."""
        scores = []
        
        if criteria_scores.accuracy is not None:
            scores.append(criteria_scores.accuracy)
        if criteria_scores.relevance is not None:
            scores.append(criteria_scores.relevance)
        if criteria_scores.clarity is not None:
            scores.append(criteria_scores.clarity)
        if criteria_scores.completeness is not None:
            scores.append(criteria_scores.completeness)
        if criteria_scores.coherence is not None:
            scores.append(criteria_scores.coherence)
        
        if not scores:
            return 0.0
        
        return sum(scores) / len(scores)
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check of all services.
        
        Returns:
            Dict with health status of all services
        """
        logger.info("Performing health check of all services")
        
        health_results = {}
        
        # Check optimizer service
        try:
            optimizer_healthy = await self.optimizer_service.health_check()
            health_results["optimizer"] = "healthy" if optimizer_healthy else "unhealthy"
        except Exception as e:
            logger.error(f"Optimizer health check failed: {e}")
            health_results["optimizer"] = "unhealthy"
        
        # Check scoring service
        try:
            scorer_healthy = await self.scoring_service.health_check()
            health_results["scorer"] = "healthy" if scorer_healthy else "unhealthy"
        except Exception as e:
            logger.error(f"Scorer health check failed: {e}")
            health_results["scorer"] = "unhealthy"
        
        # Overall status
        overall_status = "healthy" if all(
            status == "healthy" for status in health_results.values()
        ) else "unhealthy"
        
        return {
            "status": overall_status,
            "services": health_results,
            "timestamp": datetime.now()
        } 
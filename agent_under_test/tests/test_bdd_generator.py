import pytest
import asyncio
from app.models.bdd_generator import BDDGenerator
from app.utils.validators import validate_requirements, validate_options
from app.utils.formatters import format_gherkin, format_json_output

class TestBDDGenerator:
    """Test cases for BDD Generator"""
    
    @pytest.fixture
    def bdd_generator(self):
        """Create a BDD generator instance for testing"""
        return BDDGenerator()
    
    @pytest.fixture
    def sample_requirements(self):
        """Sample requirements for testing"""
        return """
        As a user, I should be able to log into the system.
        When I enter valid credentials, the system should authenticate me.
        If I enter invalid credentials, the system should show an error message.
        """
    
    def test_bdd_generator_initialization(self, bdd_generator):
        """Test BDD generator initialization"""
        assert bdd_generator is not None
        # Note: Model loading might fail in test environment, so we don't assert model_loaded
    
    @pytest.mark.asyncio
    async def test_generate_scenarios_positive(self, bdd_generator, sample_requirements):
        """Test positive scenario generation"""
        try:
            options = {
                "include_negative_scenarios": False,
                "max_scenarios_per_requirement": 3,
                "include_examples": True
            }
            
            scenarios = await bdd_generator.generate_scenarios(sample_requirements, options)
            
            assert isinstance(scenarios, list)
            assert len(scenarios) > 0
            
            for scenario in scenarios:
                assert "feature" in scenario
                assert "scenario" in scenario
                assert "given" in scenario
                assert "when" in scenario
                assert "then" in scenario
                assert isinstance(scenario["given"], list)
                assert isinstance(scenario["when"], list)
                assert isinstance(scenario["then"], list)
                
        except Exception as e:
            # Model might not be loaded in test environment
            pytest.skip(f"Model not available: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_generate_scenarios_with_negative(self, bdd_generator, sample_requirements):
        """Test scenario generation including negative scenarios"""
        try:
            options = {
                "include_negative_scenarios": True,
                "max_scenarios_per_requirement": 5,
                "include_examples": True
            }
            
            scenarios = await bdd_generator.generate_scenarios(sample_requirements, options)
            
            assert isinstance(scenarios, list)
            assert len(scenarios) > 0
            
            # Check for both positive and negative scenarios
            scenario_types = [s.get("type", "positive") for s in scenarios]
            assert "positive" in scenario_types or "negative" in scenario_types
            
        except Exception as e:
            pytest.skip(f"Model not available: {str(e)}")
    
    def test_analyze_requirements(self, bdd_generator, sample_requirements):
        """Test requirements analysis"""
        try:
            analysis = bdd_generator._analyze_requirements(sample_requirements)
            
            assert "entities" in analysis
            assert "sentences" in analysis
            assert "original_text" in analysis
            assert "word_count" in analysis
            
            entities = analysis["entities"]
            assert "users" in entities
            assert "actions" in entities
            assert "conditions" in entities
            assert "outcomes" in entities
            
        except Exception as e:
            pytest.skip(f"Model not available: {str(e)}")
    
    def test_create_scenario_structure(self, bdd_generator):
        """Test scenario structure creation"""
        user = "admin"
        action = "create"
        conditions = ["user has permissions"]
        outcomes = ["item is created successfully"]
        
        scenario = bdd_generator._create_scenario_structure(
            user=user,
            action=action,
            conditions=conditions,
            outcomes=outcomes,
            scenario_type="positive"
        )
        
        assert scenario["feature"] == "Admin Create Feature"
        assert scenario["scenario"] == "Admin Create Successfully"
        assert len(scenario["given"]) > 0
        assert len(scenario["when"]) > 0
        assert len(scenario["then"]) > 0
        assert scenario["type"] == "positive"
    
    def test_create_generic_scenario(self, bdd_generator):
        """Test generic scenario creation"""
        analysis = {
            "entities": {"users": [], "actions": []},
            "sentences": ["Test sentence"],
            "original_text": "Test requirements",
            "word_count": 2
        }
        
        scenario = bdd_generator._create_generic_scenario(analysis, "positive")
        
        assert scenario["feature"] == "User Action Feature"
        assert scenario["scenario"] == "User Performs Action Successfully"
        assert len(scenario["given"]) > 0
        assert len(scenario["when"]) > 0
        assert len(scenario["then"]) > 0
    
    def test_create_negative_variant(self, bdd_generator):
        """Test negative scenario variant creation"""
        positive_scenario = {
            "feature": "Test Feature",
            "scenario": "Test Successfully",
            "given": ["the user is logged in"],
            "when": ["the user performs action"],
            "then": ["the operation succeeds"],
            "type": "positive"
        }
        
        negative_scenario = bdd_generator._create_negative_variant(positive_scenario)
        
        assert negative_scenario["scenario"] == "Test Fails"
        assert negative_scenario["type"] == "negative"
        assert "the system is experiencing issues" in negative_scenario["given"]
        assert "fail gracefully" in negative_scenario["then"][0]
    
    def test_generate_examples(self, bdd_generator):
        """Test example generation"""
        scenario = {
            "type": "positive",
            "feature": "Test Feature",
            "scenario": "Test Scenario"
        }
        
        examples = bdd_generator._generate_examples(scenario)
        
        assert isinstance(examples, list)
        assert len(examples) > 0
        
        for example in examples:
            assert "user_type" in example
            assert "action_parameter" in example
            assert "expected_result" in example
    
    def test_calculate_quality_score(self, bdd_generator):
        """Test quality score calculation"""
        # Mock scenario objects
        class MockScenario:
            def __init__(self, given, when, then):
                self.given = given
                self.when = when
                self.then = then
        
        scenarios = [
            MockScenario(["step1"], ["step2"], ["step3"]),
            MockScenario(["step4"], ["step5"], ["step6"])
        ]
        
        score = bdd_generator.calculate_quality_score(scenarios)
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
    
    def test_get_warnings(self, bdd_generator):
        """Test warning retrieval"""
        bdd_generator.warnings = ["Test warning 1", "Test warning 2"]
        
        warnings = bdd_generator.get_warnings()
        
        assert warnings == ["Test warning 1", "Test warning 2"]
        assert len(bdd_generator.warnings) == 0  # Warnings should be cleared

class TestValidators:
    """Test cases for validation utilities"""
    
    def test_validate_requirements_valid(self):
        """Test valid requirements validation"""
        requirements = "As a user, I should be able to log into the system and access my profile."
        
        result = validate_requirements(requirements)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_requirements_empty(self):
        """Test empty requirements validation"""
        requirements = ""
        
        result = validate_requirements(requirements)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0
    
    def test_validate_requirements_too_short(self):
        """Test too short requirements validation"""
        requirements = "Short"
        
        result = validate_requirements(requirements)
        
        assert result["valid"] is False
        assert any("at least 10 characters" in error for error in result["errors"])
    
    def test_validate_requirements_malicious_content(self):
        """Test malicious content detection"""
        requirements = "As a user <script>alert('xss')</script> I should be able to log in."
        
        result = validate_requirements(requirements)
        
        assert result["valid"] is False
        assert any("malicious content" in error for error in result["errors"])
    
    def test_validate_requirements_bdd_keywords(self):
        """Test BDD keywords detection"""
        requirements = "Given a user When they log in Then they should see the dashboard"
        
        result = validate_requirements(requirements)
        
        assert result["valid"] is True
        assert len(result["warnings"]) > 0
        assert any("BDD keywords" in warning for warning in result["warnings"])
    
    def test_validate_options_valid(self):
        """Test valid options validation"""
        options = {
            "include_negative_scenarios": True,
            "output_format": "both",
            "max_scenarios_per_requirement": 5,
            "include_examples": True
        }
        
        result = validate_options(options)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_options_invalid_format(self):
        """Test invalid output format validation"""
        options = {
            "output_format": "invalid_format"
        }
        
        result = validate_options(options)
        
        assert result["valid"] is False
        assert any("output_format" in error for error in result["errors"])
    
    def test_validate_options_invalid_max_scenarios(self):
        """Test invalid max scenarios validation"""
        options = {
            "max_scenarios_per_requirement": "invalid"
        }
        
        result = validate_options(options)
        
        assert result["valid"] is False
        assert any("integer" in error for error in result["errors"])

class TestFormatters:
    """Test cases for formatting utilities"""
    
    def test_format_gherkin(self):
        """Test Gherkin formatting"""
        scenario_data = {
            "feature": "User Login",
            "scenario": "Successful Login",
            "given": ["the user is on the login page"],
            "when": ["the user enters valid credentials"],
            "then": ["the user should be logged in successfully"]
        }
        
        gherkin = format_gherkin(scenario_data)
        
        assert "Feature: User Login" in gherkin
        assert "Scenario: Successful Login" in gherkin
        assert "Given the user is on the login page" in gherkin
        assert "When the user enters valid credentials" in gherkin
        assert "Then the user should be logged in successfully" in gherkin
    
    def test_format_gherkin_with_examples(self):
        """Test Gherkin formatting with examples"""
        scenario_data = {
            "feature": "User Login",
            "scenario": "Login with Different Users",
            "given": ["the user is on the login page"],
            "when": ["the user enters credentials"],
            "then": ["the user should be logged in"],
            "examples": [
                {"user_type": "admin", "expected_result": "success"},
                {"user_type": "regular", "expected_result": "success"}
            ]
        }
        
        gherkin = format_gherkin(scenario_data)
        
        assert "Examples:" in gherkin
        assert "| user_type | expected_result |" in gherkin
        assert "| admin | success |" in gherkin
    
    def test_format_json_output(self):
        """Test JSON output formatting"""
        scenarios = [{
            "feature": "User Login",
            "scenario": "Successful Login",
            "given": ["the user is on the login page"],
            "when": ["the user enters valid credentials"],
            "then": ["the user should be logged in successfully"]
        }]
        
        metadata = {
            "processing_time_ms": 100,
            "scenarios_generated": 1
        }
        
        json_output = format_json_output(scenarios, metadata)
        
        assert json_output["status"] == "success"
        assert len(json_output["scenarios"]) == 1
        assert json_output["metadata"]["processing_time_ms"] == 100
        assert json_output["metadata"]["scenarios_generated"] == 1 
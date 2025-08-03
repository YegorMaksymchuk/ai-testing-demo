from typing import Dict, List, Any, Optional
import re

def format_gherkin(scenario_data: Dict[str, Any]) -> str:
    """
    Format scenario data into Gherkin syntax
    
    Args:
        scenario_data: Dictionary containing scenario information
        
    Returns:
        Formatted Gherkin string
    """
    gherkin_lines = []
    
    # Add feature line
    feature = scenario_data.get("feature", "Generated Feature")
    gherkin_lines.append(f"Feature: {feature}")
    gherkin_lines.append("")
    
    # Add scenario line
    scenario = scenario_data.get("scenario", "Generated Scenario")
    gherkin_lines.append(f"  Scenario: {scenario}")
    
    # Add Given steps
    given_steps = scenario_data.get("given", [])
    for step in given_steps:
        gherkin_lines.append(f"    Given {step}")
    
    # Add When steps
    when_steps = scenario_data.get("when", [])
    for step in when_steps:
        gherkin_lines.append(f"    When {step}")
    
    # Add Then steps
    then_steps = scenario_data.get("then", [])
    for step in then_steps:
        gherkin_lines.append(f"    Then {step}")
    
    # Add examples if present
    examples = scenario_data.get("examples")
    if examples and len(examples) > 0:
        gherkin_lines.append("")
        gherkin_lines.append("    Examples:")
        
        # Get all unique keys from examples
        if examples:
            keys = list(examples[0].keys())
            gherkin_lines.append(f"      | {' | '.join(keys)} |")
            gherkin_lines.append(f"      | {' | '.join(['---'] * len(keys))} |")
            
            for example in examples:
                values = [str(example.get(key, '')) for key in keys]
                gherkin_lines.append(f"      | {' | '.join(values)} |")
    
    return "\n".join(gherkin_lines)

def format_json_output(scenarios: List[Dict[str, Any]], metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format scenarios and metadata into JSON output
    
    Args:
        scenarios: List of scenario dictionaries
        metadata: Metadata dictionary
        
    Returns:
        Formatted JSON dictionary
    """
    formatted_scenarios = []
    
    for scenario in scenarios:
        formatted_scenario = {
            "feature": scenario.get("feature", "Generated Feature"),
            "scenario": scenario.get("scenario", "Generated Scenario"),
            "given": scenario.get("given", []),
            "when": scenario.get("when", []),
            "then": scenario.get("then", []),
            "examples": scenario.get("examples", []),
            "gherkin": format_gherkin(scenario),
            "type": scenario.get("type", "positive")
        }
        formatted_scenarios.append(formatted_scenario)
    
    return {
        "status": "success",
        "scenarios": formatted_scenarios,
        "metadata": metadata,
        "warnings": [],
        "errors": []
    }

def format_scenario_outline(scenario_data: Dict[str, Any]) -> str:
    """
    Format scenario as a scenario outline with examples
    
    Args:
        scenario_data: Dictionary containing scenario information
        
    Returns:
        Formatted scenario outline string
    """
    gherkin_lines = []
    
    # Add feature line
    feature = scenario_data.get("feature", "Generated Feature")
    gherkin_lines.append(f"Feature: {feature}")
    gherkin_lines.append("")
    
    # Add scenario outline line
    scenario = scenario_data.get("scenario", "Generated Scenario")
    gherkin_lines.append(f"  Scenario Outline: {scenario}")
    
    # Add Given steps with placeholders
    given_steps = scenario_data.get("given", [])
    for step in given_steps:
        # Replace common patterns with placeholders
        step_with_placeholders = _add_placeholders_to_step(step)
        gherkin_lines.append(f"    Given {step_with_placeholders}")
    
    # Add When steps with placeholders
    when_steps = scenario_data.get("when", [])
    for step in when_steps:
        step_with_placeholders = _add_placeholders_to_step(step)
        gherkin_lines.append(f"    When {step_with_placeholders}")
    
    # Add Then steps with placeholders
    then_steps = scenario_data.get("then", [])
    for step in then_steps:
        step_with_placeholders = _add_placeholders_to_step(step)
        gherkin_lines.append(f"    Then {step_with_placeholders}")
    
    # Add examples
    examples = scenario_data.get("examples")
    if examples and len(examples) > 0:
        gherkin_lines.append("")
        gherkin_lines.append("    Examples:")
        
        # Get all unique keys from examples
        keys = list(examples[0].keys())
        gherkin_lines.append(f"      | {' | '.join(keys)} |")
        gherkin_lines.append(f"      | {' | '.join(['---'] * len(keys))} |")
        
        for example in examples:
            values = [str(example.get(key, '')) for key in keys]
            gherkin_lines.append(f"      | {' | '.join(values)} |")
    
    return "\n".join(gherkin_lines)

def _add_placeholders_to_step(step: str) -> str:
    """
    Add placeholders to a step for scenario outlines
    
    Args:
        step: Original step text
        
    Returns:
        Step text with placeholders
    """
    # Common patterns to replace with placeholders
    replacements = [
        (r"the (\w+) is logged into the system", r"the <user_type> is logged into the system"),
        (r"the (\w+) has appropriate permissions", r"the <user_type> has appropriate permissions"),
        (r"the (\w+) (\w+)s the requested item", r"the <user_type> <action>s the <item>"),
        (r"the system should (.+)", r"the system should <expected_result>"),
        (r"the operation should (.+)", r"the operation should <expected_result>"),
        (r"the user should (.+)", r"the user should <expected_result>")
    ]
    
    modified_step = step
    for pattern, replacement in replacements:
        modified_step = re.sub(pattern, replacement, modified_step, flags=re.IGNORECASE)
    
    return modified_step

def format_background(scenario_data: Dict[str, Any]) -> str:
    """
    Format common Given steps as a Background section
    
    Args:
        scenario_data: Dictionary containing scenario information
        
    Returns:
        Formatted background string
    """
    gherkin_lines = []
    
    # Add feature line
    feature = scenario_data.get("feature", "Generated Feature")
    gherkin_lines.append(f"Feature: {feature}")
    gherkin_lines.append("")
    
    # Add background
    gherkin_lines.append("  Background:")
    
    # Add common Given steps
    given_steps = scenario_data.get("given", [])
    for step in given_steps:
        gherkin_lines.append(f"    Given {step}")
    
    gherkin_lines.append("")
    
    # Add scenario without Given steps (since they're in background)
    scenario = scenario_data.get("scenario", "Generated Scenario")
    gherkin_lines.append(f"  Scenario: {scenario}")
    
    # Add When steps
    when_steps = scenario_data.get("when", [])
    for step in when_steps:
        gherkin_lines.append(f"    When {step}")
    
    # Add Then steps
    then_steps = scenario_data.get("then", [])
    for step in then_steps:
        gherkin_lines.append(f"    Then {step}")
    
    return "\n".join(gherkin_lines)

def format_multiple_scenarios(scenarios: List[Dict[str, Any]]) -> str:
    """
    Format multiple scenarios into a single Gherkin feature file
    
    Args:
        scenarios: List of scenario dictionaries
        
    Returns:
        Formatted Gherkin string with multiple scenarios
    """
    if not scenarios:
        return ""
    
    gherkin_lines = []
    
    # Use the feature from the first scenario
    feature = scenarios[0].get("feature", "Generated Feature")
    gherkin_lines.append(f"Feature: {feature}")
    gherkin_lines.append("")
    
    # Add each scenario
    for i, scenario in enumerate(scenarios):
        if i > 0:
            gherkin_lines.append("")
        
        scenario_name = scenario.get("scenario", f"Generated Scenario {i+1}")
        gherkin_lines.append(f"  Scenario: {scenario_name}")
        
        # Add Given steps
        given_steps = scenario.get("given", [])
        for step in given_steps:
            gherkin_lines.append(f"    Given {step}")
        
        # Add When steps
        when_steps = scenario.get("when", [])
        for step in when_steps:
            gherkin_lines.append(f"    When {step}")
        
        # Add Then steps
        then_steps = scenario.get("then", [])
        for step in then_steps:
            gherkin_lines.append(f"    Then {step}")
    
    return "\n".join(gherkin_lines) 
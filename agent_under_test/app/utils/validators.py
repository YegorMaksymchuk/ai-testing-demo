import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

def validate_requirements(requirements: str) -> Dict[str, Any]:
    """
    Validate requirements input for BDD scenario generation
    
    Args:
        requirements: Requirements text to validate
        
    Returns:
        Dictionary with validation result and any errors
    """
    errors = []
    warnings = []
    
    # Check if requirements is empty or too short
    if not requirements or not requirements.strip():
        errors.append("Requirements text cannot be empty")
        return {"valid": False, "errors": errors, "warnings": warnings}
    
    # Check minimum length
    if len(requirements.strip()) < 10:
        errors.append("Requirements text must be at least 10 characters long")
    
    # Check maximum length
    if len(requirements) > 10000:
        errors.append("Requirements text cannot exceed 10,000 characters")
    
    # Check for potentially malicious content
    malicious_patterns = [
        r"<script.*?>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe.*?>.*?</iframe>",
        r"<object.*?>.*?</object>",
        r"<embed.*?>",
        r"<form.*?>.*?</form>"
    ]
    
    for pattern in malicious_patterns:
        if re.search(pattern, requirements, re.IGNORECASE):
            errors.append("Requirements text contains potentially malicious content")
            break
    
    # Check for common BDD keywords to ensure it's actually requirements
    bdd_keywords = ["given", "when", "then", "and", "but", "feature", "scenario"]
    requirements_lower = requirements.lower()
    
    # If the text already contains BDD keywords, it might be a scenario rather than requirements
    if any(keyword in requirements_lower for keyword in bdd_keywords):
        warnings.append("Input appears to already contain BDD keywords - ensure this is requirements text, not a scenario")
    
    # Check for basic sentence structure
    sentences = re.split(r'[.!?]+', requirements)
    valid_sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(valid_sentences) < 1:
        errors.append("Requirements text must contain at least one complete sentence")
    
    # Check for action words (verbs) that indicate requirements
    action_words = ["should", "must", "will", "can", "able to", "able", "enable", "allow", "provide", "support"]
    has_action_words = any(word in requirements_lower for word in action_words)
    
    if not has_action_words:
        warnings.append("Requirements text may benefit from action words like 'should', 'must', 'will', etc.")
    
    # Check for user roles or actors
    user_patterns = [
        r"\b(user|admin|manager|customer|client|staff|employee)\b",
        r"\b(he|she|they)\s+(should|must|will|can)",
        r"\b(system|application)\s+(should|must|will)"
    ]
    
    has_user_roles = any(re.search(pattern, requirements, re.IGNORECASE) for pattern in user_patterns)
    
    if not has_user_roles:
        warnings.append("Consider including user roles or actors in your requirements for better BDD scenarios")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def validate_options(options: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate generation options
    
    Args:
        options: Options dictionary to validate
        
    Returns:
        Dictionary with validation result and any errors
    """
    errors = []
    warnings = []
    
    # Validate include_negative_scenarios
    if "include_negative_scenarios" in options:
        if not isinstance(options["include_negative_scenarios"], bool):
            errors.append("include_negative_scenarios must be a boolean value")
    
    # Validate output_format
    if "output_format" in options:
        valid_formats = ["gherkin", "json", "both"]
        if options["output_format"] not in valid_formats:
            errors.append(f"output_format must be one of: {', '.join(valid_formats)}")
    
    # Validate max_scenarios_per_requirement
    if "max_scenarios_per_requirement" in options:
        try:
            max_scenarios = int(options["max_scenarios_per_requirement"])
            if max_scenarios < 1 or max_scenarios > 20:
                errors.append("max_scenarios_per_requirement must be between 1 and 20")
        except (ValueError, TypeError):
            errors.append("max_scenarios_per_requirement must be an integer")
    
    # Validate include_examples
    if "include_examples" in options:
        if not isinstance(options["include_examples"], bool):
            errors.append("include_examples must be a boolean value")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def sanitize_text(text: str) -> str:
    """
    Sanitize input text to prevent injection attacks
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove script tags and content
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove potentially dangerous attributes
    text = re.sub(r'on\w+\s*=\s*["\'][^"\']*["\']', '', text, flags=re.IGNORECASE)
    
    # Remove javascript: URLs
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    
    # Remove iframe tags
    text = re.sub(r'<iframe.*?>.*?</iframe>', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove object tags
    text = re.sub(r'<object.*?>.*?</object>', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove embed tags
    text = re.sub(r'<embed.*?>', '', text, flags=re.IGNORECASE)
    
    # Remove form tags
    text = re.sub(r'<form.*?>.*?</form>', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def validate_metadata(metadata: Dict[str, str]) -> Dict[str, Any]:
    """
    Validate metadata fields
    
    Args:
        metadata: Metadata dictionary to validate
        
    Returns:
        Dictionary with validation result and any errors
    """
    errors = []
    warnings = []
    
    # Check for required fields if present
    if "feature_name" in metadata:
        if not metadata["feature_name"].strip():
            errors.append("feature_name cannot be empty if provided")
        elif len(metadata["feature_name"]) > 100:
            errors.append("feature_name cannot exceed 100 characters")
    
    if "project_id" in metadata:
        if not metadata["project_id"].strip():
            errors.append("project_id cannot be empty if provided")
        elif len(metadata["project_id"]) > 50:
            errors.append("project_id cannot exceed 50 characters")
    
    if "author" in metadata:
        if not metadata["author"].strip():
            errors.append("author cannot be empty if provided")
        elif len(metadata["author"]) > 100:
            errors.append("author cannot exceed 100 characters")
    
    # Check for potentially malicious content in metadata
    for key, value in metadata.items():
        if re.search(r'[<>"\']', value):
            errors.append(f"Metadata field '{key}' contains potentially dangerous characters")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    } 
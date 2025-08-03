#!/usr/bin/env python3
"""
Simple BDD Agent Example
This is a mock BDD agent that creates BDD scenarios from text descriptions.
You can run this as a separate service to test the Orchestrator Agent.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

app = FastAPI(
    title="BDD Agent",
    description="A simple BDD agent that creates Gherkin scenarios from text descriptions",
    version="1.0.0"
)

class BDDRequest(BaseModel):
    prompt: str
    system_prompt: str = "You are a BDD agent that converts text descriptions into BDD scenarios using Gherkin syntax."
    skills_and_tools: list = []

class BDDResponse(BaseModel):
    response: str
    scenario: str
    gherkin_syntax: str

@app.post("/", response_model=BDDResponse)
async def create_bdd_scenario(request: BDDRequest):
    """Create a BDD scenario from text description."""
    
    # Simple BDD scenario generation based on keywords
    prompt_lower = request.prompt.lower()
    
    if "login" in prompt_lower or "sign in" in prompt_lower:
        scenario = """
Feature: User Login

Scenario: Successful user login
  Given the user is on the login page
  When the user enters valid email "user@example.com"
  And the user enters valid password "password123"
  And the user clicks the login button
  Then the user should be redirected to the dashboard
  And the user should see a welcome message
  And the user session should be created

Scenario: Failed login with invalid credentials
  Given the user is on the login page
  When the user enters invalid email "invalid@example.com"
  And the user enters invalid password "wrongpassword"
  And the user clicks the login button
  Then an error message should be displayed
  And the user should remain on the login page
        """
    elif "registration" in prompt_lower or "sign up" in prompt_lower:
        scenario = """
Feature: User Registration

Scenario: Successful user registration
  Given the user is on the registration page
  When the user enters valid email "newuser@example.com"
  And the user enters valid password "securepassword123"
  And the user confirms password "securepassword123"
  And the user accepts terms and conditions
  And the user clicks the register button
  Then a verification email should be sent
  And the user should see a registration success message
  And the user account should be created in pending state

Scenario: Registration with existing email
  Given the user is on the registration page
  When the user enters existing email "existing@example.com"
  And the user enters valid password "password123"
  And the user clicks the register button
  Then an error message should be displayed
  And the user should remain on the registration page
        """
    elif "shopping cart" in prompt_lower or "cart" in prompt_lower:
        scenario = """
Feature: Shopping Cart

Scenario: Add item to shopping cart
  Given the user is browsing products
  When the user clicks "Add to Cart" for "Product A"
  Then the item should be added to the shopping cart
  And the cart count should increase by 1
  And a success message should be displayed

Scenario: Remove item from shopping cart
  Given the user has items in the shopping cart
  When the user clicks "Remove" for "Product A"
  Then the item should be removed from the cart
  And the cart count should decrease by 1
  And the cart total should be updated
        """
    elif "payment" in prompt_lower or "checkout" in prompt_lower:
        scenario = """
Feature: Payment Processing

Scenario: Successful credit card payment
  Given the user is on the checkout page
  And the user has items in the shopping cart
  When the user enters valid credit card number "4111111111111111"
  And the user enters valid expiry date "12/25"
  And the user enters valid CVV "123"
  And the user enters billing address
  And the user clicks "Pay Now"
  Then the payment should be processed successfully
  And an order confirmation should be displayed
  And an order confirmation email should be sent

Scenario: Failed payment with invalid card
  Given the user is on the checkout page
  When the user enters invalid credit card number "4000000000000002"
  And the user clicks "Pay Now"
  Then a payment error should be displayed
  And the user should remain on the checkout page
        """
    elif "password reset" in prompt_lower or "forgot password" in prompt_lower:
        scenario = """
Feature: Password Reset

Scenario: Request password reset
  Given the user is on the login page
  When the user clicks "Forgot Password"
  And the user enters valid email "user@example.com"
  And the user clicks "Send Reset Link"
  Then a password reset email should be sent
  And a success message should be displayed

Scenario: Reset password with token
  Given the user has received a password reset email
  When the user clicks the reset link
  And the user enters new password "newpassword123"
  And the user confirms new password "newpassword123"
  And the user clicks "Reset Password"
  Then the password should be updated
  And the user should be redirected to login page
  And a success message should be displayed
        """
    else:
        # Generic BDD scenario
        scenario = """
Feature: Generic Functionality

Scenario: Basic user interaction
  Given the user is on the application
  When the user performs the requested action
  Then the expected result should occur
  And the system should respond appropriately
        """
    
    return BDDResponse(
        response=f"Created BDD scenario for: {request.prompt}",
        scenario=scenario.strip(),
        gherkin_syntax=scenario.strip()
    )

@app.post("/chat", response_model=BDDResponse)
async def chat_endpoint(request: BDDRequest):
    """Chat endpoint for compatibility."""
    return await create_bdd_scenario(request)

@app.post("/generate", response_model=BDDResponse)
async def generate_endpoint(request: BDDRequest):
    """Generate endpoint for compatibility."""
    return await create_bdd_scenario(request)

@app.post("/completion", response_model=BDDResponse)
async def completion_endpoint(request: BDDRequest):
    """Completion endpoint for compatibility."""
    return await create_bdd_scenario(request)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "bdd-agent"}

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "BDD Agent",
        "version": "1.0.0",
        "status": "running",
        "description": "Creates BDD scenarios from text descriptions"
    }

if __name__ == "__main__":
    print("🚀 Starting BDD Agent on http://localhost:3000")
    print("📚 API Documentation: http://localhost:3000/docs")
    print("🏥 Health Check: http://localhost:3000/health")
    print("")
    print("This agent creates BDD scenarios from text descriptions.")
    print("It supports keywords like: login, registration, shopping cart, payment, password reset")
    print("")
    
    uvicorn.run(
        "bdd_agent_example:app",
        host="0.0.0.0",
        port=3000,
        reload=True
    ) 
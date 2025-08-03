#!/usr/bin/env python3
"""
Simple run script for the BDD AI Agent
"""

import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting BDD Scenario Generator AI Agent...")
    print("Server will be available at: http://localhost:8003")
    print("API Documentation: http://localhost:8003/docs")
    print("Health Check: http://localhost:8003/health")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8003,
        reload=True,
        log_level="info"
    ) 
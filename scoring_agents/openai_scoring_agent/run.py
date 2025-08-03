#!/usr/bin/env python3
"""
Simple script to run the AI Scoring Agent.
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Run the AI Scoring Agent."""
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable is required")
        print("   Please set it in your .env file or environment")
        print("   Example: export OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    workers = int(os.getenv("WORKERS", 1))
    
    print("🤖 Starting AI Scoring Agent...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"📝 Log Level: {log_level}")
    print(f"👥 Workers: {workers}")
    print(f"🤖 OpenAI Model: {os.getenv('OPENAI_MODEL', 'gpt-4')}")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            log_level=log_level,
            workers=workers,
            reload=False
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down AI Scoring Agent...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
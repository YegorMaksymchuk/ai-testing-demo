#!/usr/bin/env python3
"""
Setup script for BDD AI Agent
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies"""
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Install spaCy model
    if not run_command("python -m spacy download en_core_web_sm", "Installing spaCy English model"):
        return False
    
    return True

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    if not run_command("python -m pytest tests/ -v", "Running test suite"):
        print("⚠️  Some tests failed, but the application may still work")
        return True  # Don't fail setup if tests fail
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["logs", "temp"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("🚀 BDD AI Agent Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Run tests
    run_tests()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Start the service: python run.py")
    print("   2. Test the service: python test_agent.py")
    print("   3. View API docs: http://localhost:8003/docs")
    print("   4. Health check: http://localhost:8003/health")
    print("\n🐳 Or use Docker:")
    print("   docker-compose up --build")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main() 
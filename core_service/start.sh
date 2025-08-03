#!/bin/bash

# Orchestrator Agent Startup Script

echo "🚀 Starting Orchestrator Agent..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if config file exists
if [ ! -f "config.yaml" ]; then
    echo "⚠️  config.yaml not found. Using default configuration."
fi

# Set default environment variables if not set
export ORCHESTRATOR_HOST=${ORCHESTRATOR_HOST:-"0.0.0.0"}
export ORCHESTRATOR_PORT=${ORCHESTRATOR_PORT:-"8003"}
export OPTIMIZER_URL=${OPTIMIZER_URL:-"http://localhost:8001"}
export SCORER_URL=${SCORER_URL:-"http://localhost:8000"}
export LOG_LEVEL=${LOG_LEVEL:-"INFO"}

echo "⚙️  Configuration:"
echo "   Host: $ORCHESTRATOR_HOST"
echo "   Port: $ORCHESTRATOR_PORT"
echo "   Optimizer URL: $OPTIMIZER_URL"
echo "   Scorer URL: $SCORER_URL"
echo "   Log Level: $LOG_LEVEL"

# Start the service
echo "🚀 Starting Orchestrator Agent on http://$ORCHESTRATOR_HOST:$ORCHESTRATOR_PORT"
echo "📚 API Documentation: http://$ORCHESTRATOR_HOST:$ORCHESTRATOR_PORT/docs"
echo "🏥 Health Check: http://$ORCHESTRATOR_HOST:$ORCHESTRATOR_PORT/health"
echo ""
echo "Press Ctrl+C to stop the service"
echo ""

python main.py 
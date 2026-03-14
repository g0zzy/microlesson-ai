#!/bin/bash

echo "🚀 Starting MicroLesson AI..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env and add your ANTHROPIC_API_KEY"
    echo "   Get your key from: https://console.anthropic.com/"
    exit 1
fi

# Check if API key is set
if grep -q "your_api_key_here" .env; then
    echo "❌ Please set your ANTHROPIC_API_KEY in .env file"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Start backend
echo "🎯 Starting backend server on http://localhost:8000"
echo "📖 API docs available at http://localhost:8000/docs"
echo ""
echo "👉 Open frontend/index.html in your browser to use the app"
echo "   Or run: open frontend/index.html (macOS)"
echo ""

cd backend
python main.py

#!/bin/bash

echo "🚀 Setting up Blue Djedi Temple Website..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node dependencies
echo "📦 Installing Node dependencies..."
npm install

# Build Tailwind CSS
echo "🎨 Building CSS..."
npm run build-css

echo "✅ Setup complete!"
echo ""
echo "To run in development mode:"
echo "  npm run dev"
echo ""
echo "To run in production mode:"
echo "  gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'"

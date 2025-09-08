#!/bin/bash

# Uganda Tech Connect - TypeScript Build Script
# This script compiles TypeScript files and sets up the development environment

echo "🚀 Building Uganda Tech Connect TypeScript modules..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Download from: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm are available"

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing TypeScript dependencies..."
    npm install
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
    
    echo "✅ Dependencies installed successfully"
else
    echo "✅ Dependencies already installed"
fi

# Clean previous build
if [ -d "dist" ]; then
    echo "🧹 Cleaning previous build..."
    rm -rf dist
fi

# Compile TypeScript
echo "🔨 Compiling TypeScript files..."
npx tsc

if [ $? -eq 0 ]; then
    echo "✅ TypeScript compilation successful!"
    
    # List compiled files
    echo "📁 Generated files:"
    find dist -name "*.js" -type f | while read file; do
        echo "   - $file"
    done
    
    echo ""
    echo "🎉 Build completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Start your Django development server"
    echo "   2. Open the test file: test_tailwind.html"
    echo "   3. Check browser console for TypeScript integration status"
    echo ""
    echo "💡 For development with auto-compilation, run:"
    echo "   npm run dev"
    
else
    echo "❌ TypeScript compilation failed"
    echo "   Please check the errors above and fix them"
    exit 1
fi

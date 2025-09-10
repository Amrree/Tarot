#!/bin/bash

# Build script for Tarot Studio macOS app

set -e

echo "Building Tarot Studio macOS app..."

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script must be run on macOS"
    exit 1
fi

# Check if Python 3.10+ is available
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.10+ is required, found $python_version"
    exit 1
fi

# Set up virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install py2app

# Create app icon (placeholder)
echo "Creating app icon..."
mkdir -p tarot_studio/packaging
if [ ! -f "tarot_studio/packaging/icon.icns" ]; then
    echo "Creating placeholder icon..."
    # Create a simple icon using sips (macOS built-in tool)
    # This is a placeholder - you should replace with a proper icon
    echo "⚠️  Warning: Using placeholder icon. Please create a proper icon.icns file."
fi

# Build the app
echo "Building app bundle..."
cd tarot_studio/packaging
python3 setup_app.py py2app

# Check if build was successful
if [ -d "dist/Tarot Studio.app" ]; then
    echo "✅ App built successfully!"
    echo "Location: $(pwd)/dist/Tarot Studio.app"
    
    # Get app size
    app_size=$(du -sh "dist/Tarot Studio.app" | cut -f1)
    echo "App size: $app_size"
    
    # Optional: Code sign the app (requires Apple Developer account)
    if command -v codesign &> /dev/null; then
        echo "Code signing app..."
        codesign --force --deep --sign - "dist/Tarot Studio.app"
        echo "✅ App signed successfully!"
    else
        echo "⚠️  codesign not found. App is not signed."
    fi
    
    # Optional: Create DMG
    if command -v create-dmg &> /dev/null; then
        echo "Creating DMG..."
        create-dmg --volname "Tarot Studio" --window-pos 200 120 --window-size 600 300 --icon-size 100 --icon "Tarot Studio.app" 175 120 --hide-extension "Tarot Studio.app" --app-drop-link 425 120 "dist/Tarot Studio.dmg" "dist/"
        echo "✅ DMG created successfully!"
    else
        echo "⚠️  create-dmg not found. Install with: brew install create-dmg"
    fi
    
else
    echo "❌ App build failed!"
    exit 1
fi

echo "Build complete! 🎉"
echo ""
echo "To run the app:"
echo "  open 'dist/Tarot Studio.app'"
echo ""
echo "To install the app:"
echo "  cp -r 'dist/Tarot Studio.app' /Applications/"
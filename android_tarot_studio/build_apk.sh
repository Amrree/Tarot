#!/bin/bash

# Android Tarot Studio APK Build Script
# This script attempts to build the APK for the Tarot Studio Android app

echo "🚀 Building Android Tarot Studio APK..."
echo "=================================="

# Check if we're in the right directory
if [ ! -f "buildozer.spec" ]; then
    echo "❌ Error: buildozer.spec not found. Please run this script from the android_tarot_studio directory."
    exit 1
fi

# Check if buildozer is available
if ! command -v buildozer &> /dev/null; then
    echo "⚠️  Buildozer not found. Attempting to install..."
    
    # Try to install buildozer
    if command -v pip3 &> /dev/null; then
        echo "📦 Installing buildozer via pip3..."
        pip3 install --user buildozer cython==0.29.19
    elif command -v pip &> /dev/null; then
        echo "📦 Installing buildozer via pip..."
        pip install --user buildozer cython==0.29.19
    else
        echo "❌ Error: pip not found. Please install Python pip first."
        echo "   Try: sudo apt install python3-pip"
        exit 1
    fi
fi

# Check if buildozer is now available
if ! command -v buildozer &> /dev/null; then
    echo "❌ Error: Could not install buildozer. Please install manually:"
    echo "   pip install buildozer cython==0.29.19"
    exit 1
fi

echo "✅ Buildozer found. Starting build process..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
buildozer android clean

# Build debug APK
echo "🔨 Building debug APK..."
buildozer android debug

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! APK built successfully!"
    echo "=================================="
    echo "📱 APK Location: bin/tarotstudio-1.0.0-debug.apk"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Test the APK on an Android device"
    echo "2. For release, run: buildozer android release"
    echo "3. Sign the APK with your release keystore"
    echo "4. Submit to Google Play Store"
    echo ""
    echo "🔗 APK File: $(pwd)/bin/tarotstudio-1.0.0-debug.apk"
    
    # List the APK file
    if [ -f "bin/tarotstudio-1.0.0-debug.apk" ]; then
        echo "📊 APK Details:"
        ls -lh bin/tarotstudio-1.0.0-debug.apk
    fi
else
    echo ""
    echo "❌ Build failed. Please check the error messages above."
    echo ""
    echo "🔧 Common solutions:"
    echo "1. Install required dependencies:"
    echo "   sudo apt install python3-pip python3-venv python3-dev"
    echo "   sudo apt install build-essential libssl-dev libffi-dev"
    echo "   sudo apt install autoconf libtool pkg-config zlib1g-dev"
    echo "   sudo apt install libncurses5-dev libncursesw5-dev libtinfo5"
    echo "   sudo apt install cmake libffi-dev libssl-dev"
    echo "   sudo apt install python3-setuptools git zip unzip openjdk-8-jdk"
    echo ""
    echo "2. Try building in a virtual environment:"
    echo "   python3 -m venv buildozer_env"
    echo "   source buildozer_env/bin/activate"
    echo "   pip install buildozer cython==0.29.19"
    echo "   buildozer android debug"
    echo ""
    echo "3. Use Docker (if available):"
    echo "   docker pull kivy/buildozer"
    echo "   docker run --rm -v \$(pwd):/src kivy/buildozer android debug"
fi

echo ""
echo "📚 For detailed build instructions, see: BUILD_APK_GUIDE.md"
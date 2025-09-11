#!/bin/bash
# Tarot Studio Android APK Build Script

echo "🚀 Building Tarot Studio Android APK..."

# Extract project
tar -xzf android_tarot_studio.tar.gz
cd android_tarot_studio

# Install prerequisites
sudo apt update
sudo apt install python3-pip python3-venv python3-dev python3-full
sudo apt install build-essential libssl-dev libffi-dev
sudo apt install autoconf libtool pkg-config zlib1g-dev
sudo apt install libncurses5-dev libncursesw5-dev libtinfo5
sudo apt install cmake libffi-dev libssl-dev python3-setuptools
sudo apt install git zip unzip openjdk-8-jdk python3-kivy
sudo apt install keytool jarsigner

# Setup buildozer
python3 -m venv buildozer_env
source buildozer_env/bin/activate
pip install buildozer cython==0.29.19

# Build APK
buildozer android debug

echo "✅ APK build complete!"
echo "📱 APK Location: bin/tarotstudio-1.0.0-debug.apk"

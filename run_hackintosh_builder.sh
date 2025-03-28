#!/bin/bash

echo "Hackintosh EFI Builder Launcher"
echo "=============================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH."
    echo "Please install Python 3.8 or higher."
    echo ""
    exit 1
fi

# Check if resources exist, if not generate them
if [ ! -f "resources/app_icon.png" ]; then
    echo "Generating resources..."
    python3 generate_resources.py
fi

# Check if dependencies are installed
echo "Checking dependencies..."
if ! python3 -c "import customtkinter" &> /dev/null; then
    echo "Installing required dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies."
        echo "Please run 'pip3 install -r requirements.txt' manually."
        exit 1
    fi
fi

# Run the application
echo "Starting Hackintosh EFI Builder..."
python3 main.py

exit 0
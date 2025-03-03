#!/bin/bash

# Exit on error
set -e

echo "Starting resume dashboard..."

# Only create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating new virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "Installing required packages..."
    python3 -m pip install -r requirements.txt
else
    echo "Using existing virtual environment..."
    source venv/bin/activate
fi

# Create images directory if it doesn't exist
if [ ! -d "assets/images" ]; then
    echo "Creating images directory..."
    mkdir -p assets/images
fi

# Create default nologo.jpeg if it doesn't exist
if [ ! -f "assets/images/nologo.jpeg" ]; then
    echo "Creating default logo placeholder..."
    touch assets/images/nologo.jpeg
fi

# Run the application
echo "Starting the dashboard..."
python3 app.py

# Deactivate virtual environment on exit
trap "echo 'Deactivating virtual environment...'; deactivate" EXIT 
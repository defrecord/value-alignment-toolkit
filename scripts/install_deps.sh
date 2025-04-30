#!/bin/bash
# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Please activate the virtual environment first"
    echo "  source venv/bin/activate  # On Unix/macOS"
    echo "  venv\\Scripts\\activate   # On Windows"
    exit 1
fi

# Install Python dependencies
pip install -r requirements.txt

# Install additional system dependencies if needed
if command -v apt-get &> /dev/null; then
    echo "Detected Debian/Ubuntu - installing system dependencies"
    sudo apt-get update
    sudo apt-get install -y guile-3.0 guile-3.0-dev
elif command -v brew &> /dev/null; then
    echo "Detected macOS with Homebrew - installing system dependencies"
    brew install guile
elif command -v pacman &> /dev/null; then
    echo "Detected Arch Linux - installing system dependencies"
    sudo pacman -S guile
else
    echo "Please install Guile 3.0 manually for your system"
fi

# Setup spaCy models
python -m spacy download en_core_web_md

echo "Dependencies installed successfully"

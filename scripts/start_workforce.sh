#!/bin/bash
# Start the Content Generator Workforce using honcho
# Usage: ./scripts/start_workforce.sh

cd "$(dirname "$0")/.."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please edit .env and add your API keys"
fi

# Check if honcho is installed
if ! command -v honcho &> /dev/null; then
    echo "Installing honcho..."
    pip install honcho
fi

echo "Starting Content Generator Workforce..."
echo "========================================="
honcho start -f honcho.yml

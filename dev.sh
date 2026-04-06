#!/bin/bash

# Function to kill background processes on exit
cleanup() {
    echo -e "\nStopping dev servers..."
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup EXIT

# Start FastAPI server in the background
echo "Starting FastAPI server on http://127.0.0.1:8000..."
uv run uvicorn main:app --reload --port 8000 &

# Wait a moment for uvicorn to initialize
sleep 2

# Start Browser-Sync proxy
# It will watch your templates and static files and proxy localhost:8000
echo "Starting Browser-Sync proxy on http://localhost:3000..."
npx browser-sync start --proxy "localhost:8000" --files "templates/*.html, static/**/*.*" --no-notify

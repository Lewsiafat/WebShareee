#!/bin/bash

# Define paths relative to the script's location
SCRIPT_DIR=$(dirname "$0")
PROJECT_ROOT=$(cd "$SCRIPT_DIR/..". && pwd)
FRONTEND_DIR="$PROJECT_ROOT/frontend"

echo "Building frontend application..."

# --- Build Frontend ---
cd "$FRONTEND_DIR" || { echo "Error: Frontend directory not found."; exit 1; }
npm run build
BUILD_STATUS=$? # Capture exit status
cd "$PROJECT_ROOT" # Go back to project root

if [ $BUILD_STATUS -eq 0 ]; then
    echo "Frontend build completed successfully."
    echo "Output is in: $FRONTEND_DIR/dist"
else
    echo "Error: Frontend build failed."
    exit 1
fi

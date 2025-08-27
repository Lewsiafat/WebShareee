#!/bin/bash

# Define paths relative to the script's location
SCRIPT_DIR=$(dirname "$0")
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
FRONTEND_DIR="$PROJECT_ROOT/frontend"
BACKEND_DIR="$PROJECT_ROOT/backend"
PIDS_FILE="$SCRIPT_DIR/pids.txt"

echo "Starting frontend and backend services..."

# Clear previous PIDs file
> "$PIDS_FILE" # Create/truncate the file before writing

# --- Start Frontend ---
# Launch frontend in a subshell, print its PID to stdout
FRONTEND_PID_OUTPUT=$( # Capture stdout of this subshell
    cd "$FRONTEND_DIR" || { echo "Error: Frontend directory not found."; exit 1; }
    npm run dev > /dev/null 2>&1 &
    echo $! # Print PID to stdout of this subshell
)

# --- Start Backend ---
# Launch backend in a subshell, print its PID to stdout
BACKEND_PID_OUTPUT=$( # Capture stdout of this subshell
    cd "$BACKEND_DIR" || { echo "Error: Backend directory not found."; exit 1; }
    "$BACKEND_DIR/.venv/bin/uvicorn" app.main:app --reload --port 8700 &
    echo $! # Print PID to stdout of this subshell
)

# Capture the PIDs from the subshells' stdout
FRONTEND_PID=$(echo "$FRONTEND_PID_OUTPUT")
BACKEND_PID=$(echo "$BACKEND_PID_OUTPUT")

# Write PIDs to the main PIDS_FILE
if [ -n "$FRONTEND_PID" ]; then
    echo "$FRONTEND_PID" >> "$PIDS_FILE"
fi
if [ -n "$BACKEND_PID" ]; then
    echo "$BACKEND_PID" >> "$PIDS_FILE"
fi

echo "Services started. PIDs saved to $PIDS_FILE"
echo "Frontend: http://localhost:8080"
echo "Backend API Docs: http://localhost:8700/docs"
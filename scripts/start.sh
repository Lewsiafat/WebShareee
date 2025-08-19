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
echo "Starting frontend (Vite dev server) on port 8080..."
(
    cd "$FRONTEND_DIR" || { echo "Error: Frontend directory not found."; exit 1; }
    npm run dev > /dev/null 2>&1 &
    echo $! > "$PIDS_FILE.tmp_frontend" # Write PID to a temporary file
) &
FRONTEND_LAUNCHER_PID=$! # PID of the subshell that launches frontend

# --- Start Backend ---
echo "Starting backend (FastAPI/Uvicorn) on port 8700..."
(
    cd "$BACKEND_DIR" || { echo "Error: Backend directory not found."; exit 1; }
    "$BACKEND_DIR/.venv/bin/uvicorn" app.main:app --reload --port 8700 > /dev/null 2>&1 &
    echo $! > "$PIDS_FILE.tmp_backend" # Write PID to a temporary file
) &
BACKEND_LAUNCHER_PID=$! # PID of the subshell that launches backend

# Wait for the launcher subshells to finish and write their PIDs
wait $FRONTEND_LAUNCHER_PID
wait $BACKEND_LAUNCHER_PID

# Read PIDs from temporary files and consolidate into PIDS_FILE
FRONTEND_PID=$(cat "$PIDS_FILE.tmp_frontend")
BACKEND_PID=$(cat "$PIDS_FILE.tmp_backend")

echo "$FRONTEND_PID" >> "$PIDS_FILE"
echo "$BACKEND_PID" >> "$PIDS_FILE"

rm "$PIDS_FILE.tmp_frontend" "$PIDS_FILE.tmp_backend" # Clean up temporary files

echo "Frontend started with PID: $FRONTEND_PID"
echo "Backend started with PID: $BACKEND_PID"

echo "Services started. PIDs saved to $PIDS_FILE"
echo "Frontend: http://localhost:8080"
echo "Backend API Docs: http://localhost:8700/docs"

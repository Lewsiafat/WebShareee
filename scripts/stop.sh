#!/bin/bash

# Define paths relative to the script's location
SCRIPT_DIR=$(dirname "$0")
PIDS_FILE="$SCRIPT_DIR/pids.txt"

echo "Stopping services..."

if [ -f "$PIDS_FILE" ]; then
    PIDS=$(cat "$PIDS_FILE")
    for PID in $PIDS; do
        if ps -p $PID > /dev/null; then
            kill $PID
        fi
    done
    rm "$PIDS_FILE"
    echo "Services stopped and PIDs file removed."
else
    echo "PIDS file ($PIDS_FILE) not found. No services to stop or they were not started by this script."
fi
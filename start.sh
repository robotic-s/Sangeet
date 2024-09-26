#!/bin/bash

# Find the process ID (PID) using port 80
PIDS=$(lsof -t -i:80)

# Check if any process is found
if [ -z "$PIDS" ]; then
  echo "No process found running on port 80."
else
  # Kill the processes
  echo "Killing processes running on port 80..."
  kill -9 $PIDS
  echo "Processes killed."
fi

#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export DANGEROUSLY_OMIT_AUTH=true

# Run the inspector
echo "Starting MCP Inspector..."
echo "This will run until you press Ctrl+C"
echo "Once started, open http://127.0.0.1:6274 in your browser"
echo ""

npx @modelcontextprotocol/inspector python server.py --stdio
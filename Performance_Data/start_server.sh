#!/bin/bash
# Start CORS-enabled local server for Performance Dashboard
# This serves the xlsx/csv files for auto-loading

PORT=8080
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║    Starting CORS-enabled server for Performance Dashboard ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if cors_server.py exists
if [ -f "$DIR/cors_server.py" ]; then
    cd "$DIR" && python3 cors_server.py
else
    echo "⚠️  cors_server.py not found, using basic server (may have CORS issues)"
    echo ""
    cd "$DIR" && python3 -m http.server $PORT
fi

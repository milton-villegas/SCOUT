#!/bin/bash
# Start SCOUT Web Application (Backend + Frontend)
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "======================================"
echo "  SCOUT Web Application"
echo "======================================"
echo ""

# Check and install Python dependencies
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Installing Python dependencies..."
    cd "$SCRIPT_DIR"
    pip3 install -r requirements.txt -r backend/requirements.txt -q
fi

# Check and install Node dependencies
if [ ! -d "$SCRIPT_DIR/frontend/node_modules" ]; then
    echo "Installing Node dependencies..."
    cd "$SCRIPT_DIR/frontend"
    npm install -q
fi

# Start FastAPI backend
echo "Starting backend on http://localhost:8000..."
cd "$SCRIPT_DIR"
PYTHONPATH="$SCRIPT_DIR" python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend
sleep 3

# Start SvelteKit frontend
echo "Starting frontend on http://localhost:5173..."
cd "$SCRIPT_DIR/frontend"
VITE_API_URL="http://localhost:8000" npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!

# Wait for frontend to be ready
sleep 3

# Open browser
if command -v open &> /dev/null; then
    open http://localhost:5173
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5173
fi

echo ""
echo "======================================"
echo "  SCOUT is running!"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo "======================================"
echo ""
echo "Press Ctrl+C to stop both servers."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait

@echo off
echo ======================================
echo   SCOUT Web Application
echo ======================================
echo.

REM Set project root (parent of scripts/)
set PROJECT_ROOT=%~dp0..

REM Check and install Python dependencies
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Installing Python dependencies...
    pip install -r %PROJECT_ROOT%\requirements.txt -r %PROJECT_ROOT%\backend\requirements.txt -q
)

REM Check and install Node dependencies
if not exist "%PROJECT_ROOT%\frontend\node_modules" (
    echo Installing Node dependencies...
    cd %PROJECT_ROOT%\frontend
    npm install -q
    cd %PROJECT_ROOT%
)

echo Starting backend on http://localhost:8000...
set PYTHONPATH=%PROJECT_ROOT%
start /B cmd /c "cd %PROJECT_ROOT% && python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak > nul

echo Starting frontend on http://localhost:5173...
start /B cmd /c "cd %PROJECT_ROOT%\frontend && set VITE_API_URL=http://localhost:8000 && npm run dev -- --host 0.0.0.0 --port 5173"

timeout /t 3 /nobreak > nul

REM Open browser
start http://localhost:5173

echo.
echo ======================================
echo   SCOUT is running!
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo ======================================
echo.
echo Press any key to stop...
pause > nul
taskkill /f /im uvicorn.exe 2>nul
taskkill /f /im node.exe 2>nul

@echo off
REM Quick Start Script for HydroSentinel Backend
REM Run this to install dependencies and start the server

echo ====================================
echo   HydroSentinel Backend Setup
echo ====================================
echo.

echo [1/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo Try: pip install pipwin ^&^& pipwin install rasterio
    pause
    exit /b 1
)
echo.

echo [2/4] Generating demo data...
python generate_demo_data.py
if %errorlevel% neq 0 (
    echo WARNING: Failed to generate demo data
    echo Continuing anyway - modules have fallback data
)
echo.

echo [3/4] Testing processing modules...
echo Testing surface.py...
python processing/surface.py > nul 2>&1
echo Testing oil.py...
python processing/oil.py > nul 2>&1
echo Testing risk.py...
python processing/risk.py > nul 2>&1
echo All modules tested!
echo.

echo [4/4] Starting API server...
echo Server will start at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
uvicorn main:app --reload

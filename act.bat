@echo off
echo ===================================
echo NexusLMD Django Project Launcher
echo ===================================
echo.

REM Activate the virtual environment if it exists
if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
    echo Virtual environment activated
) else (
    echo No virtual environment found at .venv
)
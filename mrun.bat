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

echo.
echo Step 1: Running code linting with Ruff...
call ruff check .
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Linting issues found. Please consider fixing them.
    echo Run 'lint.bat --fix' to automatically fix some issues.
    echo.
    timeout /t 2 > nul
)

echo.
echo Step 2: Making migrations...
python manage.py makemigrations
echo.

echo Step 3: Applying migrations...
python manage.py migrate
echo.

echo Step 4: Opening browser to 127.0.0.1:8000...
start http://127.0.0.1:8000
echo.

echo Step 5: Starting Django development server...
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver

REM This line will only be reached if the server is stopped
echo.
echo Server stopped. Goodbye!
pause
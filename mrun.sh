#!/bin/bash
echo "==================================="
echo "NexusLMD Django Project Launcher"
echo "==================================="
echo

# Activate the virtual environment if it exists
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
    echo "Virtual environment activated"
else
    echo "No virtual environment found at .venv"
fi

echo
echo "Step 0: Installing missing dependencies..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
    echo "Dependencies installed."
else
    echo "No requirements.txt file found. Skipping dependency installation."
fi

echo
echo "Step 1: Running code linting with Ruff..."
ruff check .
if [ $? -ne 0 ]; then
    echo "[WARNING] Linting issues found. Please consider fixing them."
    echo "Run './lint.sh --fix' to automatically fix some issues."
    echo
    sleep 2
fi

echo
echo "Step 2: Making migrations..."
python manage.py makemigrations
echo

echo "Step 3: Applying migrations..."
python manage.py migrate
echo

echo "Step 4: Opening browser to 127.0.0.1:8000..."
open http://127.0.0.1:8000
echo

echo "Step 5: Starting Django development server..."
echo "Press Ctrl+C to stop the server"
echo
python manage.py runserver

# This line will only be reached if the server is stopped
echo
echo "Server stopped. Goodbye!"
read -p "Press [Enter] to exit..."

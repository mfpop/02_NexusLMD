#!/bin/bash
echo ===================================
echo NexusLMD Django Project Launcher
echo ===================================
echo

# Activate the virtual environment if it exists
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
    echo "Virtual environment activated"
else
    echo "No virtual environment found at .venv"
fi

python manage.py tailwind start
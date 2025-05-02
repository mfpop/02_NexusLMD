@echo off
echo Running Ruff linter on your project...
ruff check .
if %ERRORLEVEL% EQU 0 (
    echo Linting completed successfully!
) else (
    echo Linting found issues. Please fix them.
)

echo.
echo To automatically fix some issues, run: lint.bat --fix
if "%1"=="--fix" (
    echo Attempting to fix issues automatically...
    ruff check --fix .
)
@echo off
echo Starting MySQL synchronization utilities...

REM Check for admin privileges
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo This script requires administrator privileges
    echo Please run Command Prompt as administrator and try again
    pause
    exit /b 1
)

echo Checking MySQL service...
sc query MySQL80 | findstr "RUNNING" >nul
IF %ERRORLEVEL% NEQ 0 (
    echo Starting MySQL80 service...
    net start MySQL80
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to start MySQL80. Please start it manually.
        exit /b 1
    )
) ELSE (
    echo MySQL80 service is already running.
)

echo.
echo Running database verification script...
python verify_mysql_sync.py
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo Applying migrations to ensure database synchronization...
    python manage.py migrate
    
    echo.
    echo Verifying again...
    python verify_mysql_sync.py
)

echo.
echo MySQL synchronization completed!
echo Your admin dashboard should now reflect the MySQL database content.
pause
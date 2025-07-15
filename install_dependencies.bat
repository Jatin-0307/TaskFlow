@echo off
echo ================================
echo    TaskFlow Installation
echo ================================
echo.
echo Installing Python dependencies...
echo.

pip install Flask==3.0.0
if %errorlevel% neq 0 (
    echo Error installing Flask
    pause
    exit /b 1
)

pip install Flask-SQLAlchemy==3.1.1
if %errorlevel% neq 0 (
    echo Error installing Flask-SQLAlchemy
    pause
    exit /b 1
)

pip install SQLAlchemy==2.0.23
if %errorlevel% neq 0 (
    echo Error installing SQLAlchemy
    pause
    exit /b 1
)

pip install Flask-Login==0.6.3
if %errorlevel% neq 0 (
    echo Error installing Flask-Login
    pause
    exit /b 1
)

pip install Flask-WTF==1.2.1
if %errorlevel% neq 0 (
    echo Error installing Flask-WTF
    pause
    exit /b 1
)

pip install WTForms==3.1.1
if %errorlevel% neq 0 (
    echo Error installing WTForms
    pause
    exit /b 1
)

pip install Werkzeug==3.0.1
if %errorlevel% neq 0 (
    echo Error installing Werkzeug
    pause
    exit /b 1
)

pip install email-validator==2.1.0
if %errorlevel% neq 0 (
    echo Error installing email-validator
    pause
    exit /b 1
)

pip install python-dotenv==1.0.0
if %errorlevel% neq 0 (
    echo Error installing python-dotenv
    pause
    exit /b 1
)

echo.
echo ================================
echo   Installation Complete!
echo ================================
echo.
echo You can now run TaskFlow by:
echo 1. Double-clicking start_taskflow.bat
echo 2. Or running: python app.py
echo.
echo Default admin login:
echo Username: admin
echo Password: admin123
echo.
pause

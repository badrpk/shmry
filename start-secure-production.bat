@echo off
title SHMRY Secure Production Server
color 0A

echo.
echo ========================================
echo 🔐 SHMRY Secure Production Server
echo ========================================
echo.
echo Starting SHMRY with production security...
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ❌ ERROR: .env file not found!
    echo.
    echo Please create .env file from env.template:
    echo   1. Copy env.template to .env
    echo   2. Fill in your secure credentials
    echo   3. Never commit .env to source control
    echo.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

echo ✅ Environment file found
echo.

REM Validate security configuration
echo 🔒 Validating security configuration...
node security-config.js
if %errorlevel% neq 0 (
    echo ❌ Security validation failed!
    echo Please check your .env configuration
    echo.
    pause
    exit /b 1
)

echo ✅ Security configuration validated
echo.

REM Start secure production server
echo 🚀 Starting secure production server...
echo.
echo 🔒 Admin services bound to localhost only
echo 🌐 Public website accessible on port 80
echo 📊 Health check: http://localhost/health
echo 📈 Status page: http://localhost/status
echo.

start "SHMRY Secure Production" cmd /k "node deployment/production-server.js"

echo.
echo ========================================
echo ✅ SHMRY Secure Production Started!
echo ========================================
echo.
echo 🌐 Public Website: http://localhost:80
echo 🔒 Admin Panel: http://127.0.0.1:3001 (localhost only)
echo 🎯 Master Dashboard: http://127.0.0.1:3002 (localhost only)
echo 🌍 Network Discovery: http://127.0.0.1:3003 (localhost only)
echo.
echo 🔐 Security Features Active:
echo   • Rate limiting enabled
echo   • CORS protection
echo   • Security headers
echo   • Admin services isolated
echo   • Environment validation
echo.
echo Press any key to close...
pause > nul

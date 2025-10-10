@echo off
title Docker Flask App Manager
color 0A

:menu
cls
echo ========================================
echo    Docker Flask App Manager
echo ========================================
echo.

REM Check Docker status
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Docker is not installed or not in PATH
    echo Please install Docker Desktop for Windows
    echo Download from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✓ Docker is available
echo.

REM Check container status
docker-compose ps 2>nul | find "flask-app" >nul
if %errorlevel% equ 0 (
    echo ✓ Application is RUNNING
) else (
    echo ✗ Application is STOPPED
)
echo.

echo ========================================
echo    Available Commands:
echo ========================================
echo.
echo [1] Start Application
echo [2] Stop Application  
echo [3] Restart Application
echo [4] View Status
echo [5] View Logs
echo [6] Open Application in Browser
echo [7] Build New Image
echo [8] Clean Up
echo [9] Exit
echo.
echo ========================================

set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" (
    echo.
    echo Starting application...
    docker-compose up -d
    echo Application started!
    timeout /t 3 /nobreak >nul
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo Stopping application...
    docker-compose down
    echo Application stopped!
    timeout /t 2 /nobreak >nul
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo Restarting application...
    docker-compose restart
    echo Application restarted!
    timeout /t 3 /nobreak >nul
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo Container status:
    docker-compose ps
    echo.
    echo Application URLs:
    echo   - Direct: http://localhost:5000/
    echo   - Via Nginx: http://localhost:80/
    echo.
    pause
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo Application logs (press Ctrl+C to exit):
    echo ========================================
    docker-compose logs -f flask-app
    goto menu
)

if "%choice%"=="6" (
    echo.
    echo Opening application in browser...
    start http://localhost:5000/
    echo Browser opened!
    timeout /t 2 /nobreak >nul
    goto menu
)

if "%choice%"=="7" (
    echo.
    echo Building new image...
    docker-compose build --no-cache
    echo Image built successfully!
    timeout /t 2 /nobreak >nul
    goto menu
)

if "%choice%"=="8" (
    echo.
    echo Cleaning up Docker resources...
    docker-compose down
    docker system prune -f
    echo Cleanup completed!
    timeout /t 2 /nobreak >nul
    goto menu
)

if "%choice%"=="9" (
    echo.
    echo Goodbye!
    exit /b 0
)

echo.
echo Invalid choice! Please enter 1-9.
timeout /t 2 /nobreak >nul
goto menu

@echo off
echo Docker Deployment Script
echo ========================
echo.

cd /d "%~dp0"

echo Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not installed or not in PATH.
    echo Please install Docker Desktop for Windows.
    echo Download from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo Docker found!
echo.

echo Stopping existing containers...
docker-compose down 2>nul

echo Building new image...
docker-compose build --no-cache

echo Starting application...
docker-compose up -d

echo.
echo Application deployed successfully!
echo.
echo URLs:
echo   - Direct: http://localhost:5000/
echo   - Via Nginx: http://localhost:80/
echo.
echo Container status:
docker-compose ps

echo.
echo To view logs:
echo   docker-compose logs -f flask-app
echo.
echo To stop:
echo   docker-compose down
echo.
pause

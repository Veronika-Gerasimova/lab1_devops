# Flask Application Deployment with Docker

## 📋 Overview
This document describes the Docker-based deployment and management of the Flask student management application.

## 🌐 Application URLs
- **Direct Access**: http://localhost:5000/
- **Via Nginx**: http://localhost:80/
- **Network Access**: http://10.255.0.1:5000/

## 🐳 Docker Management

### Main Management Menu
```batch
docker-manage.bat
```
- Interactive menu for all Docker operations
- Shows container status
- Provides easy access to all Docker commands

### Docker Commands
```bash
# Start application
docker-compose up -d

# Stop application
docker-compose down

# Restart application
docker-compose restart

# View logs
docker-compose logs -f flask-app

# View status
docker-compose ps

# Build new image
docker-compose build --no-cache
```

## 🔄 Auto-startup Configuration

Docker containers automatically restart on system reboot with the `restart: unless-stopped` policy in docker-compose.yml.

### Docker Restart Policies
- **unless-stopped**: Container restarts automatically unless manually stopped
- **always**: Container always restarts
- **on-failure**: Container restarts only on failure

### Enable Docker Desktop Auto-start
1. Open Docker Desktop settings
2. Go to "General" tab
3. Enable "Start Docker Desktop when you log in"

## 📁 Project Structure
```
devops/
├── app.py                 # Main Flask application
├── test_app.py           # Test suite
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose configuration
├── docker-manage.bat     # Docker management script
├── DEPLOYMENT_README.md   # This file
└── venv/                 # Virtual environment (for local development)
```

## 🧪 Testing the Application

### Manual Testing
1. Open browser and navigate to http://localhost:5000/
2. Test the student management features:
   - View student list: http://localhost:5000/students
   - Add new student: http://localhost:5000/add-student
   - API endpoint: http://localhost:5000/api/students

### Automated Testing
```cmd
.\venv\Scripts\pytest.exe -v
```

## 🔧 Troubleshooting

### Docker Issues

#### Application Won't Start
1. Check Docker Desktop is running:
   ```cmd
   docker --version
   ```
2. Check if ports are available:
   ```cmd
   netstat -an | findstr :5000
   netstat -an | findstr :80
   ```
3. View container logs:
   ```cmd
   docker-compose logs flask-app
   ```

#### Container Won't Stop
1. Force stop containers:
   ```cmd
   docker-compose down --remove-orphans
   ```
2. Kill all containers:
   ```cmd
   docker kill $(docker ps -q)
   ```

#### Image Build Issues
1. Clean Docker cache:
   ```cmd
   docker system prune -a
   ```
2. Rebuild without cache:
   ```cmd
   docker-compose build --no-cache
   ```

#### Port Conflicts
1. Check what's using port 5000:
   ```cmd
   netstat -ano | findstr :5000
   ```
2. Change port in docker-compose.yml:
   ```yaml
   ports:
     - "5001:5000"  # Use port 5001 instead
   ```

## 📝 Deployment Process

The application is automatically deployed via Jenkins CI/CD pipeline when code is pushed to the `main` branch:

1. **Checkout** - Gets latest code from repository
2. **Setup Environment** - Creates virtual environment and installs dependencies
3. **Run Tests** - Executes automated test suite
4. **Docker Deploy** - Stops old containers, builds new image, starts new containers
5. **Health Check** - Verifies application is running and responding

### Manual Deployment
```cmd
# Quick deployment
docker-compose up -d --build

# Full deployment with cleanup
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🎯 Features

- **Student Management**: Add, view, and manage student records
- **Web Interface**: User-friendly HTML interface
- **REST API**: JSON API for programmatic access
- **Health Check**: Built-in health monitoring endpoint
- **Docker Deployment**: Containerized application with auto-restart
- **Nginx Reverse Proxy**: Load balancing and SSL termination
- **CI/CD**: Automated deployment via Jenkins
- **Isolation**: Secure containerized environment

## 📞 Support

For issues or questions:
1. Check the Jenkins build logs
2. Review this documentation
3. Use the Docker management script: `docker-manage.bat`
4. Check Docker Desktop logs
5. View container logs: `docker-compose logs flask-app`

### Quick Commands
```cmd
# Check status
docker-compose ps

# View logs
docker-compose logs -f flask-app

# Restart
docker-compose restart

# Full reset
docker-compose down && docker-compose up -d --build
```

---
*Last updated: Docker deployment setup*

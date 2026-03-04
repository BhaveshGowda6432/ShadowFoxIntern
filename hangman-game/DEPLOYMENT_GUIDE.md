# 🚀 Deployment Guide - Hangman Game

Complete guide for deploying the Hangman Game in various environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Virtual Environment Setup](#virtual-environment-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites

- Python 3.8+ (3.10+ recommended)
- pip (usually comes with Python)
- Git (optional)

### Quick Start

```bash
# Clone or download the project
cd hangman-game

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Play the game
python run_game.py
```

### Deactivate Virtual Environment

```bash
deactivate
```

---

## Virtual Environment Setup

### Why Use Virtual Environment?

Virtual environments isolate project dependencies from system Python, preventing conflicts with other projects.

### Setup Steps

#### Option 1: Using venv (Built-in)

```bash
# Create environment
python -m venv hangman_env

# Activate
# Windows:
hangman_env\Scripts\activate
# macOS/Linux:
source hangman_env/bin/activate

# Install packages
pip install -r requirements.txt

# Verify installation
pip list
```

#### Option 2: Using Conda

```bash
# Create environment
conda create -n hangman python=3.10

# Activate
conda activate hangman

# Install packages
pip install -r requirements.txt
```

#### Option 3: Using Poetry

```bash
# Install poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Create environment and install
poetry install

# Run with poetry
poetry run python run_game.py
```

---

## Docker Deployment

### Why Docker?

- 🐳 Consistent environment across machines
- 🔒 Isolated dependencies
- 📦 Easy distribution
- 🚀 Simple deployment

### Build Docker Image

```bash
# Navigate to project directory
cd hangman-game

# Build image
docker build -t hangman-game:latest .

# Verify image was built
docker images
```

### Run Docker Container

#### Interactive Mode (Play the Game)

```bash
docker run -it hangman-game:latest
```

#### With Volume Mount (Development)

```bash
docker run -it -v $(pwd):/app hangman-game:latest
```

**On Windows (PowerShell):**

```powershell
docker run -it -v ${pwd}:/app hangman-game:latest
```

#### Run Tests in Container

```bash
docker run hangman-game:latest pytest tests/ -v
```

### Using Docker Compose

#### Build and Run

```bash
# Build and start container
docker-compose up --build

# Run in background
docker-compose up -d

# Stop container
docker-compose down

# View logs
docker-compose logs -f
```

#### Development Workflow

```bash
# Start container with volume mount
docker-compose up

# In another terminal, execute commands
docker-compose exec hangman-game bash
docker-compose exec hangman-game python run_game.py
docker-compose exec hangman-game pytest tests/ -v
```

---

## Production Deployment

### Cloud Deployment Options

#### 1. AWS Deployment

**Using Docker and ECR:**

```bash
# Create ECR repository
aws ecr create-repository --repository-name hangman-game

# Build and push image
docker build -t <account-id>.dkr.ecr.<region>.amazonaws.com/hangman-game .
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/hangman-game

# Run on EC2 or ECS
```

#### 2. Google Cloud Deployment

**Using Cloud Run:**

```bash
# Enable required APIs
gcloud services enable run.googleapis.com

# Build image
gcloud builds submit --tag gcr.io/<project-id>/hangman-game

# Deploy
gcloud run deploy hangman-game \
  --image gcr.io/<project-id>/hangman-game \
  --platform managed \
  --region us-central1
```

#### 3. Azure Deployment

**Using Container Instances:**

```bash
# Build and push to ACR
az acr build --registry <registry-name> --image hangman-game:latest .

# Deploy
az container create \
  --resource-group <group> \
  --name hangman-game \
  --image <registry>.azurecr.io/hangman-game:latest
```

#### 4. Heroku Deployment

**Using Git:**

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create hangman-game

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

**Using Docker:**

```bash
# Build image
docker build -t hangman-game .

# Tag for Heroku
docker tag hangman-game registry.heroku.com/<app-name>/web

# Push to Heroku
heroku container:push web --app <app-name>

# Release
heroku container:release web --app <app-name>
```

### Kubernetes Deployment

**Create deployment.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hangman-game
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hangman-game
  template:
    metadata:
      labels:
        app: hangman-game
    spec:
      containers:
        - name: hangman-game
          image: hangman-game:latest
          ports:
            - containerPort: 8000
```

**Deploy:**

```bash
kubectl apply -f deployment.yaml
kubectl expose deployment hangman-game --type=LoadBalancer
```

---

## Troubleshooting

### Common Issues

#### 1. Module Not Found Error

**Problem:** `ModuleNotFoundError: No module named 'pytest'`

**Solution:**

```bash
# Ensure virtual environment is activated
pip install -r requirements.txt

# Or on Windows
python -m pip install -r requirements.txt
```

#### 2. Permission Denied (Linux/Mac)

**Problem:** `Permission denied: './run_game.py'`

**Solution:**

```bash
# Make file executable
chmod +x run_game.py

# Run with python
python run_game.py
```

#### 3. Port Already in Use (Docker)

**Problem:** `bind: address already in use`

**Solution:**

```bash
# Check running containers
docker ps

# Stop container
docker stop <container-id>

# Or use different port
docker run -p 8001:8000 hangman-game
```

#### 4. Virtual Environment Not Activating

**Problem:** Virtual environment doesn't activate

**Solution:**

```bash
# Delete and recreate
rm -rf venv  # rm -r venv on Windows
python -m venv venv

# Activate properly
# Windows:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Verify
python --version
pip list
```

#### 5. Docker Build Fails

**Problem:** `ERROR: failed to solve with frontend dockerfile.v0`

**Solution:**

```bash
# Check Docker daemon is running
docker version

# Clean up Docker
docker system prune -a

# Rebuild
docker build -t hangman-game .
```

#### 6. Tests Failing

**Problem:** Tests fail in container

**Solution:**

```bash
# Run with verbose output
docker run hangman-game pytest tests/ -v -s

# Check file permissions
docker run hangman-game ls -la tests/

# Use bash to investigate
docker run -it hangman-game bash
```

### Debug Mode

#### Python Debug

```bash
# Add to code
import pdb; pdb.set_trace()

# Or use debugpy
python -m debugpy --listen 5678 run_game.py
```

#### Docker Debug

```bash
# Run bash instead of game
docker run -it hangman-game bash

# Then run commands manually
python run_game.py
pytest tests/ -v
```

---

## Performance Optimization

### Speed Up Development

```bash
# Use --cache for faster test runs
pytest --cache-clear tests/

# Profile code
python -m cProfile -s cumulative run_game.py

# Run specific slow test
pytest tests/test_game_engine.py::TestGameEngine::test_win_condition -v
```

### Docker Optimization

```bash
# Multi-stage build (update Dockerfile)
# Layer caching for faster rebuilds
# Only copy what's needed

# Build without cache
docker build --no-cache -t hangman-game .
```

---

## Monitoring & Logging

### Application Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### Container Logging

```bash
# View logs
docker logs <container-id>

# Follow logs
docker logs -f <container-id>

# Last 100 lines
docker logs --tail 100 <container-id>

# Kubernetes logs
kubectl logs <pod-name>
```

---

## Update & Maintenance

### Update Dependencies

```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade pytest

# Update all
pip install --upgrade -r requirements.txt
```

### Version Management

```bash
# Tag releases
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Docker image versioning
docker build -t hangman-game:1.0.0 .
docker build -t hangman-game:latest .
```

---

## Support

For deployment issues:

1. Check logs: `docker logs <container-id>`
2. Review README.md
3. Check test output: `pytest tests/ -v`
4. Refer to framework documentation

---

**Last Updated:** 2026

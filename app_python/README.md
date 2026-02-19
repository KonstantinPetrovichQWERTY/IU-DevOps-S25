# DevOps Info Service

A production-ready web service that provides comprehensive system and runtime information. Built as the foundation for a DevOps monitoring tool that will evolve throughout the course.

[![Workflow Status](https://github.com/KonstantinPetrovichQWERTY/IU-DevOps-S25/actions/workflows/ci.yml/badge.svg)](https://github.com/KonstantinPetrovichQWERTY/IU-DevOps-S25/actions/workflows/ci.yml)

## Table of contents

- [Overview](#-overview)
  - [Quick Start](#-quick-start)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Docker](#docker)
  - [Configuration](#-configuration)
  - [Running the Unit Tests](#running-the-unit-tests)
    - [Test structure](#test-structure)
  - [API Endpoints](#-api-endpoints)
    - [GET `/`](#get-)
    - [GET `/health`](#get-health)
  - [Development](#️-development)
    - [Project Structure](#project-structure)
  - [Contributing](#-contributing)

## 📋 Overview

The DevOps Info Service is a lightweight web application that exposes detailed information about:

- Service metadata and configuration
- System hardware and platform details
- Runtime statistics and uptime
- HTTP request information

This service serves as the starting point for a comprehensive monitoring solution that will later include containerization, CI/CD pipelines, metrics export, and Kubernetes deployment.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- virtualenv (recommended)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/KonstantinPetrovichQWERTY/IU-DevOps-S25.git
   cd app_python
   ```

2. **Create and activate virtual environment**

   ```bash
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

To start the FastAPI application, run the following command:

```bash
uvicorn app_python.src.main:app --reload
```

- The `--reload` flag enables auto-reloading, so the server restarts whenever you make changes to the code.
- Open your browser and navigate to `http://127.0.0.1:8000/`. You should see the system information displayed in JSON format.
- To see the SwaggerUI documentation navigate to `http://127.0.0.1:8000/docs`.

---

## Docker

Or you can simply use docker to run and build the application:

1. **How to build?**
To build the Docker image locally, navigate to the project directory (app_python) and run the following command. This will create a Docker image tagged as `devops-info-app`.

   ```bash
   docker build -t devops-info-app .
   ```

2. **How to run?**
To run the Docker container, use the following command. The `-d` flag runs the container in detached mode, and `-p 8000:8000` maps port 8000 on your local machine to port 8000 in the container.

   ```bash
   docker run -d -p 8000:8000 devops-info-app:1.0
   ```

3. **How to pull?**
You can pull docker image from DockerHub [repo](https://hub.docker.com/repository/docker/konstantinqwertin/devops-info-app/general).

   ```bash
   docker pull konstantinqwertin/devops-info-app:1.0
   docker run -d -p 8000:8000 konstantinqwertin/devops-info-app:1.0
   ```

---

## 🔧 Configuration

The application can be configured using environment variables:

| Variable | Description | Default | Example |
| ---------- | ------------- | --------- | --------- |
| `HOST` | Bind address | `0.0.0.0` | `127.0.0.1` |
| `PORT` | Listening port | `5000` | `8080` |
| `DEBUG` | Debug mode | `False` | `True` |

**Examples:**

```bash
# Custom port
PORT=8080 uvicorn app_python.src.main:app --reload

# Local only with debug mode
HOST=127.0.0.1 DEBUG=True uvicorn app_python.src.main:app --reload

# Production configuration
HOST=0.0.0.0 PORT=3000 uvicorn app_python.src.main:app --reload
```

---

## Running the Unit Tests

First of all, install required dependencies to your virtual environment (venv):

```bash
pip install pytest
```

To start the tests, run the following command in `app_python` directory:

```bash
pytest tests/test_main.py -v 
```

If everything is correct, the test should pass:

```bash
======================================= test session starts =======================================
collected 5 items

tests/test_main.py::TestRootEndpoint::test_root_endpoint_structure PASSED                    [ 20%]
tests/test_main.py::TestRootEndpoint::test_root_endpoint_returns_valid_datetime PASSED       [ 40%] 
tests/test_main.py::TestHealthEndpoint::test_health_check_success PASSED                     [ 60%] 
tests/test_main.py::TestHealthEndpoint::test_health_check_timestamp_format PASSED            [ 80%] 
tests/test_main.py::TestConfiguration::test_port_configuration PASSED                        [100%]

======================================== 5 passed in 0.61s ========================================
```

### Test structure

Class Organization

- `TestRootEndpoint` - Tests for the main API endpoint
- `TestHealthEndpoint` - Tests for health check functionality
- `TestConfiguration` - Tests for configuration handling

---

## 📡 API Endpoints

### GET `/`

Returns comprehensive service and system information.

**Response Example:**

```json
{
  "service": {
    "name": "devops-info-service",
    "version": "1.0.0",
    "description": "DevOps course info service",
    "framework": "FastApi"
  },
  "system": {
    "hostname": "LAPTOP-2BCVD7LH",
    "platform": "Windows",
    "platform_version": "10.0.19045",
    "architecture": "AMD64",
    "cpu_count": 8,
    "python_version": "3.11.9"
  },
  "runtime": {
    "uptime_seconds": 6,
    "uptime_human": "0 hours, 0 minutes",
    "current_time": "2026-02-16T22:13:31.723824+00:00",
    "timezone": "UTC"
  },
  "request": {
    "client_ip": "127.0.0.1",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "method": "GET",
    "path": "/"
  },
  "endpoints": [
    {
      "path": "/",
      "method": "GET",
      "description": "Service information"
    },
    {
      "path": "/health",
      "method": "GET",
      "description": "Health check"
    }
  ]
}
```

### GET `/health`

Simple health check endpoint for monitoring probes.

**Response Example:**

```json
{
  "status": "healthy",
  "timestamp": "2026-02-16T22:13:53.189929+00:00",
  "uptime_seconds": 27
}
```

**Status Codes:**

- `200 OK` - Service is healthy
- `500 Internal Server Error` - Service is unhealthy

## 🛠️ Development

### Project Structure

```project structure
app_python/
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── tests/                   # Unit tests (Lab 3)
│   └── __init__.py
└── docs/                    # Documentation
    ├── LAB01.md             # Lab 1 submission
    └── screenshots/         # Proof of work
        ├── 01-main-endpoint.png
        ├── 02-health-check.png
        └── 03-formatted-output.png
```

## 👥 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

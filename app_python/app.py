import os
from fastapi import FastAPI, Request
from datetime import datetime
import pytz
import logging

import platform
import socket

# Env variables config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


app = FastAPI()
start_time = datetime.now()


# Service function
def get_uptime():
    """Returns uptaime in seconds"""
    delta = datetime.now() - start_time
    seconds = int(delta.total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return {"seconds": seconds, "human": f"{hours} hours, {minutes} minutes"}


# Logging middleware. Logs all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(
        msg=(
            f"Incoming request: {request.method} {request.url.path} "
            f"from {request.client.host}"
        )
    )

    response = await call_next(request)

    logger.info(f"Outgoing response: Status {response.status_code}")
    return response


@app.get(
    "/",
    description="Service information",
)
def get_service_information(request: Request):
    """Service and system information"""

    utc_now = datetime.now(pytz.utc)

    hostname = socket.gethostname()
    platform_name = platform.system()
    platform_version = platform.version()
    architecture = platform.machine()
    python_version = platform.python_version()
    cpu_count = os.cpu_count()

    uptime = get_uptime()

    return {
        "service": {
            "name": "devops-info-service",
            "version": "1.0.0",
            "description": "DevOps course info service",
            "framework": "FastApi",
        },
        "system": {
            "hostname": hostname,
            "platform": platform_name,
            "platform_version": platform_version,
            "architecture": architecture,
            "cpu_count": cpu_count,
            "python_version": python_version,
        },
        "runtime": {
            "uptime_seconds": uptime.get("seconds", None),
            "uptime_human": uptime.get("human", None),
            "current_time": utc_now,
            "timezone": "UTC",
        },
        "request": {
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent"),
            "method": request.method,
            "path": request.url.path,
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
            },
        ],
    }


@app.get(
    "/health",
    description="Health check",
    status_code=200,
)
def health_check():
    """Health check endpoint"""
    uptime = get_uptime()

    return {
        "status": "healthy",
        "timestamp": datetime.now(pytz.utc),
        "uptime_seconds": uptime.get("seconds", None),
    }

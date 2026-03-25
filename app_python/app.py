import os
from fastapi import FastAPI, Request
from datetime import datetime
from datetime import timezone
import pytz
import logging
import json

import platform
import socket

# Env variables config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"


# Logging config
class JSONFormatter(logging.Formatter):
    """Formats application logs as JSON for log aggregation systems."""

    STANDARD_FIELDS = {
        "name",
        "msg",
        "args",
        "levelname",
        "levelno",
        "pathname",
        "filename",
        "module",
        "exc_info",
        "exc_text",
        "stack_info",
        "lineno",
        "funcName",
        "created",
        "msecs",
        "relativeCreated",
        "thread",
        "threadName",
        "processName",
        "process",
        "message",
        "asctime",
    }

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        for key, value in record.__dict__.items():
            if key in self.STANDARD_FIELDS or key.startswith("_"):
                continue
            if isinstance(value, (str, int, float, bool)) or value is None:
                payload[key] = value

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=True)


logger = logging.getLogger("devops-info-service")
logger.setLevel(logging.INFO)
logger.handlers.clear()
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(JSONFormatter())
logger.addHandler(stream_handler)
logger.propagate = False


app = FastAPI()
start_time = datetime.now()


@app.on_event("startup")
async def startup_event():
    """Logs application startup for deployment visibility."""
    logger.info(
        "Application startup complete",
        extra={"event": "startup", "host": HOST, "port": PORT},
    )


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
    client_ip = request.client.host if request.client else "unknown"
    logger.info(
        "Incoming request",
        extra={
            "event": "request_in",
            "method": request.method,
            "path": request.url.path,
            "client_ip": client_ip,
        },
    )

    try:
        response = await call_next(request)
    except Exception:
        logger.exception(
            "Request processing failed",
            extra={
                "event": "request_error",
                "method": request.method,
                "path": request.url.path,
                "client_ip": client_ip,
                "status_code": 500,
            },
        )
        raise

    logger.info(
        "Outgoing response",
        extra={
            "event": "request_out",
            "method": request.method,
            "path": request.url.path,
            "client_ip": client_ip,
            "status_code": response.status_code,
        },
    )
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

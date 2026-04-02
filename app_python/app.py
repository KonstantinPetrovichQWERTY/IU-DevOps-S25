import os
import time
import tempfile
import threading
from fastapi import FastAPI, Request, Response
from datetime import datetime
from datetime import timezone
import pytz
import logging
import json
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

import platform
import socket
from pathlib import Path

# Env variables config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
VISITS_FILE = os.getenv("VISITS_FILE", "data/visits")


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
visits_lock = threading.Lock()


# Prometheus metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint", "status_code"],
)

http_requests_in_progress = Gauge(
    "http_requests_in_progress",
    "HTTP requests currently being processed",
    ["method", "endpoint", "status_code"],
)

endpoint_calls_total = Counter(
    "devops_info_endpoint_calls_total",
    "Total calls to application endpoints",
    ["endpoint"],
)

system_info_collection_seconds = Histogram(
    "devops_info_system_collection_seconds",
    "Time spent collecting system information",
)


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


def get_endpoint_label(request: Request) -> str:
    """Returns low-cardinality endpoint labels for metrics."""
    route = request.scope.get("route")
    if route and hasattr(route, "path"):
        return route.path

    path = request.url.path
    if path in {"/", "/health", "/metrics", "/visits"}:
        return path
    return "other"


def read_visits_count() -> int:
    """Reads visit counter from file"""
    visits_path = Path(VISITS_FILE)
    if not visits_path.exists():
        return 0

    try:
        content = visits_path.read_text(encoding="utf-8").strip()
        return int(content) if content else 0
    except (ValueError, OSError):
        return 0


def write_visits_count(count: int) -> None:
    """Writes visit counter atomically to avoid partial writes."""
    visits_path = Path(VISITS_FILE)
    visits_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=visits_path.parent,
        delete=False,
    ) as tmp_file:
        tmp_file.write(str(count))
        temp_name = tmp_file.name
    os.replace(temp_name, visits_path)


def increment_visits_count() -> int:
    """Increments visit counter"""
    with visits_lock:
        current = read_visits_count()
        updated = current + 1
        write_visits_count(updated)
        return updated


# Logging middleware. Logs all requests and records Prometheus metrics.
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_timer = time.perf_counter()
    status_code = 500
    method = request.method
    endpoint = get_endpoint_label(request)
    in_progress_metric = http_requests_in_progress.labels(
        method=method,
        endpoint=endpoint,
        status_code="in_progress",
    )
    in_progress_metric.inc()

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
        status_code = response.status_code
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
    finally:
        duration = time.perf_counter() - start_timer
        http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status_code=str(status_code),
        ).inc()
        http_request_duration_seconds.labels(
            method=method,
            endpoint=endpoint,
            status_code=str(status_code),
        ).observe(duration)
        in_progress_metric.dec()

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
    "/metrics",
    description="Prometheus metrics",
    include_in_schema=False,
)
def get_metrics():
    """Exposes Prometheus metrics."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get(
    "/",
    description="Service information",
)
def get_service_information(request: Request):
    """Service and system information"""

    visits = increment_visits_count()
    endpoint_calls_total.labels(endpoint="/").inc()

    with system_info_collection_seconds.time():
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
            "visits_count": visits,
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
            {
                "path": "/metrics",
                "method": "GET",
                "description": "Prometheus metrics"
            },
            {
                "path": "/visits",
                "method": "GET",
                "description": "Get current visits counter"
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
    endpoint_calls_total.labels(endpoint="/health").inc()
    uptime = get_uptime()

    return {
        "status": "healthy",
        "timestamp": datetime.now(pytz.utc),
        "uptime_seconds": uptime.get("seconds", None),
    }


@app.get(
    "/visits",
    description="Current visits counter",
    status_code=200,
)
def get_visits_count():
    """Returns current persisted visits counter."""
    endpoint_calls_total.labels(endpoint="/visits").inc()
    with visits_lock:
        visits = read_visits_count()
    return {
        "visits": visits,
    }

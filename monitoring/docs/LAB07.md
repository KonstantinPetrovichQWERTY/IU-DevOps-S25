# LAB07 - Centralized Logging with Grafana Loki

## 1. Architecture

Centralized logging stack is deployed with Docker Compose and contains:

- Loki 3.0.0: log storage and querying backend (TSDB + filesystem)
- Promtail 3.0.0: log collection agent from Docker containers
- Grafana 12.3.1: visualization and log exploration UI
- app-python: FastAPI service from previous labs with JSON logging

Data flow:

1. Application writes structured JSON logs to stdout.
2. Promtail discovers Docker containers, filters by label logging=promtail, and ships logs to Loki.
3. Loki stores logs using TSDB schema v13 with 7-day retention.
4. Grafana queries Loki with LogQL for Explore and dashboard panels.

## 2. Setup Guide

### 2.1 Deploy

1. Create runtime env file for Grafana admin credentials.

   ```bash
   copy .env.example .env
   ```

2. Start the stack.

   ```bash
   docker compose -f monitoring/docker-compose.yml --env-file monitoring/.env up -d --build
   ```

3. Verify services.

   ```bash
   docker compose -f monitoring/docker-compose.yml ps
   ```

4. Open web interfaces:

- Grafana: `http://localhost:3000`
- Loki readiness endpoint: `http://localhost:3100/ready`
- App endpoint: `http://localhost:8000`

## 3. Configuration

### 3.1 Loki Configuration

Configured in `monitoring/loki/config.yml`:

- auth_enabled: false for lab environment
- server.http_listen_port: 3100
- schema_config: v13 with tsdb store
- storage backend: filesystem
- retention: 168h (7 days)
- compactor enabled for retention cleanup

Why this setup:

- TSDB is the recommended storage mode for Loki 3.x.
- Filesystem backend is simple and sufficient for single-node lab setup.
- Retention and compactor simulate production log lifecycle behavior.

### 3.2 Promtail Configuration

Configured in `monitoring/promtail/config.yml`:

- Docker service discovery via unix socket
- Client push endpoint: `http://loki:3100/loki/api/v1/push`
- Container filter by Docker label logging=promtail
- Relabeling:
  - container name from __meta_docker_container_name
  - app label from __meta_docker_container_label_app
  - service label from compose service name

Why this setup:

- Label filtering avoids collecting noise from unrelated containers.
- App and container labels simplify LogQL queries and dashboards.

### 3.3 Grafana Configuration

Configured in `monitoring/docker-compose.yml` and provisioning:

- Anonymous access disabled
- Admin credentials from env file
- Loki datasource auto-provisioned

## 4. Application Logging

Structured logging implemented in `app_python/app.py`.

What was added:

- Custom `JSONFormatter` using Python `logging` module
- Startup event logging
- HTTP middleware logs:
  - incoming request (method, path, client_ip)
  - outgoing response (status_code + request context)
  - unhandled exceptions with stack trace

## 5. Dashboard

### Panel 1: Logs Table

- Visualization: Logs
- Query: `{app=~"devops-.*"}`
- Purpose: Recent raw logs from all integrated applications.

### Panel 2: Request Rate

- Visualization: Time series
- Query: `sum by (app) (rate({app=~"devops-.*"}[1m]))`
- Purpose: Logs/second grouped by application.

### Panel 3: Error Logs

- Visualization: Logs
- Query: `{app=~"devops-.*"} | json | level="ERROR"`
- Purpose: Focused stream of application errors only.

### Panel 4: Log Level Distribution

- Visualization: Pie chart
- Query: `sum by (level) (count_over_time({app=~"devops-.*"} | json [5m]))`
- Purpose: Distribution of log levels (INFO/ERROR/etc.).

## 6. Production Config

Implemented production-oriented controls:

- Resource limits and reservations for all services
- Health checks:
  - Loki: /ready
  - Grafana: /api/health
- Anonymous Grafana login disabled
- Admin password externalized via env file
- Loki retention policy: 7 days

## 7. Testing

### 7.1 Verify in Grafana Explore

LogQL queries used:

- {app="devops-python"}
- {app="devops-python"} |= "ERROR"
- {app="devops-python"} | json | method="GET"

### 7.2 Service Health Validation

   ```bash
   docker compose -f monitoring/docker-compose.yml ps
   ```

## Evidence Checklist

Add screenshots into `monitoring/docs/screenshots` and reference them below:

0. JSON logs in terminal from app-python
1. Grafana login page with anonymous access disabled
2. Grafana dashboard with 4 panels
3. Grafana Explore showing INFO logs from app(s)
4. Grafana Explore showing Outgoing logs from app(s)
5. docker compose ps with healthy status

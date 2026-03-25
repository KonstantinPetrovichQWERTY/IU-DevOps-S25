# LAB08 - Metrics and Monitoring with Prometheus

## 1. Architecture

Monitoring pipeline for Lab 08:

1. FastAPI app exposes application metrics at `/metrics`.
2. Prometheus scrapes metrics from app, Loki, Grafana, and itself every 15 seconds.
3. Grafana uses Prometheus as metrics datasource and Loki as logs datasource.
4. Dashboards visualize request rate, latency, active requests, status distribution, and service uptime.

Metric flow: `app-python -> Prometheus -> Grafana`.

## 2. Application Instrumentation

### Added HTTP metrics

- `http_requests_total{method,endpoint,status_code}` (Counter): total request count.
- `http_request_duration_seconds{method,endpoint,status_code}` (Histogram): request latency.
- `http_requests_in_progress{method,endpoint,status_code}` (Gauge): currently active requests.

### Added business metrics

- `devops_info_endpoint_calls_total{endpoint}` (Counter): endpoint usage.
- `devops_info_system_collection_seconds` (Histogram): system info collection duration.

### Middleware behavior

- Records request start time with `time.perf_counter()`.
- Increments in-progress gauge at request start.
- Logs incoming/outgoing request in JSON format.
- In `finally` block records counter + histogram and decrements gauge.
- `/metrics` endpoint exports Prometheus text format.

## 3. Prometheus Configuration

Configuration file: `monitoring/prometheus/prometheus.yml`.

### Global settings

- `scrape_interval: 15s`
- `evaluation_interval: 15s`

### Scrape targets

- `prometheus`: `localhost:9090`
- `app`: `app-python:8000` (`/metrics`)
- `loki`: `loki:3100` (`/metrics`)
- `grafana`: `grafana:3000` (`/metrics`)

### Retention policy

Configured in `monitoring/docker-compose.yml` command args:

- `--storage.tsdb.retention.time=15d`
- `--storage.tsdb.retention.size=10GB`

Why: limits disk growth and preserves enough history for lab analysis.

## 4. Dashboard Walkthrough

Exported dashboard file:

- `monitoring/grafana/dashboards/lab08-app-metrics-dashboard.json`

Panels and queries:

1. Request Rate by Endpoint (Time series)
   - Query: `sum by (endpoint) (rate(http_requests_total[5m]))`
2. Error Rate (5xx) (Time series)
   - Query: `sum(rate(http_requests_total{status_code=~"5.."}[5m]))`
3. Request Duration p95 (Time series)
   - Query: `histogram_quantile(0.95, sum by (le, endpoint) (rate(http_request_duration_seconds_bucket[5m])))`
4. Request Duration Heatmap (Heatmap)
   - Query: `sum by (le) (rate(http_request_duration_seconds_bucket[5m]))`
5. Active Requests (Gauge)
   - Query: `sum(http_requests_in_progress)`
6. Status Code Distribution (Pie chart)
   - Query: `sum by (status_code) (rate(http_requests_total[5m]))`
7. Uptime (Stat)
   - Query: `up{job="app"}`

### Community Dashboard (Imported)

In addition to the custom Lab08 dashboard, a community dashboard was imported:

- Grafana dashboard ID: `3662` (Prometheus 2.0 Overview)
- Local JSON file: `monitoring/grafana/dashboards/lab08-import-3662.json`
- Purpose: monitor Prometheus server internals (scrape health, TSDB, ingestion, rule evaluation) alongside app-level RED metrics.

This gives two complementary views:

- application observability via the custom `Lab08 - App Metrics` dashboard;
- Prometheus platform observability via the community `Prometheus 2.0 Overview` dashboard.

## 5. PromQL Examples

1. Requests per second by HTTP method:
   - `sum by (method) (rate(http_requests_total[5m]))`
2. Error percentage (5xx / all requests):
   - `(sum(rate(http_requests_total{status_code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100`
3. p99 request latency by endpoint:
   - `histogram_quantile(0.99, sum by (le, endpoint) (rate(http_request_duration_seconds_bucket[5m])))`
4. Status-class traffic split (2xx/4xx/5xx):
   - `sum by (status_code) (rate(http_requests_total{status_code=~"2..|4..|5.."}[5m]))`
5. In-progress requests by endpoint:
   - `sum by (endpoint) (http_requests_in_progress)`
6. Top endpoints by call volume (last 5 minutes):
   - `topk(5, sum by (endpoint) (increase(http_requests_total[5m])))`
7. System info collection p95 duration:
   - `histogram_quantile(0.95, rate(devops_info_system_collection_seconds_bucket[5m]))`

## 6. Production Setup

- Health checks:
  - Prometheus: `/-/healthy`
  - Loki: `/ready`
  - Grafana: `/api/health`
  - App: `/health`
- Resource limits:
  - Prometheus: `1 CPU`, `1G RAM`
  - Loki: `1 CPU`, `1G RAM`
  - Grafana: `0.5 CPU`, `512M RAM`
  - App: `0.5 CPU`, `256M RAM`
- Persistent volumes:
  - `prometheus-data`
  - `loki-data`
  - `grafana-data`
  - `promtail-positions`
- Shared Docker network:
  - `logging`

## 7. Testing Results

### Evidence files

Place screenshots in `monitoring/docs/screenshots`

# Lab 09 - Kubernetes Deployment

## 1. Architecture Overview

**Minikube** (my choice)

- **Multi-node support** - Can run multi-node clusters for realistic testing
- **Built-in addons** - Dashboard, ingress, metrics-server, etc. ready out-of-box
- **Multiple drivers** - Supports Docker, Hyper-V, VirtualBox, HyperKit
- **Persistent storage** - Better volume mount support
- **Mature & stable** - Older, more battle-tested in production-like environments

1. Client sends requests to `devops-info-service` on Service port `80`.
2. Service forwards traffic to Pod container port `8000`.
3. Deployment manages replicated Pods (`app=devops-info-app`) and performs rolling updates.

Resources used:

- Deployment: `devops-info-app`
- Service: `devops-info-service` (type: NodePort, nodePort: `30080`)
- Replica count baseline: `3` in manifest
- Scaling demonstration: `5` replicas via `kubectl scale`

Resource allocation strategy:

- Requests: `cpu=100m`, `memory=128Mi`
- Limits: `cpu=250m`, `memory=256Mi`

## 2. Manifest Files

### `k8s/deployment.yml`

Key configuration:

- `replicas: 3`
- `RollingUpdate` strategy with `maxSurge: 1`, `maxUnavailable: 0`
- Container image: `konstantinqwertin/devops-info-app:latest`
- Health checks:
  - Liveness probe: `GET /health`
  - Readiness probe: `GET /health`
- Resource requests/limits configured
- Security hardening: `allowPrivilegeEscalation: false`

Why these values:

- `3` replicas provide baseline fault tolerance.
- `maxUnavailable: 0` enforces availability during updates.
- `/health` endpoint exists in the app and is suitable for probe checks.

### `k8s/service.yml`

Key configuration:

- Service type: `NodePort`
- Service port: `80`
- Target port: `8000`
- NodePort: `30080`
- Selector: `app=devops-info-app`

Why NodePort:

- Required for local cluster access without cloud LoadBalancer.

## 3. Deployment Evidence

Evidence is stored in `k8s/docs/terminal_outputs.md`.

Main verification commands used:

```bash
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/service.yml
kubectl rollout status deployment/devops-info-app
kubectl get all -l app=devops-info-app
kubectl get pods,svc -l app=devops-info-app
kubectl describe deployment devops-info-app
```

Observed results:

- Deployment reached ready state (`3/3` available for baseline).
- Service created successfully as `NodePort`.
- Endpoints populated with Pod IPs.
- Probes active and healthy.

Service access evidence you can check in `k8s/docs/terminal_output.md`

Both `/` and `/health` returned successful JSON responses.

## 4. Operations Performed

### Deploy

```bash
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/service.yml
```

### Scale to 5 replicas

```bash
kubectl scale deployment/devops-info-app --replicas=5
```

Result: `5/5` ready.

### Rolling update

Rolling update was completed successfully:

```bash
kubectl set image deployment/devops-info-app devops-info-app=konstantinqwertin/devops-info-app:a6eb67992f8c0f5127dc9e09862621f662597c9e
kubectl rollout status deployment/devops-info-app
kubectl get deployment devops-info-app
```

Result: rollout finished successfully with `5/5` available Pods on the new image tag.

### Rollback

```bash
kubectl rollout undo deployment/devops-info-app
kubectl rollout history deployment/devops-info-app
```

Rollback completed successfully and deployment returned to healthy state.

## 5. Production Considerations

Health checks:

- Liveness probe detects hung containers and triggers restart.
- Readiness probe ensures only healthy Pods receive traffic.

Resource limits rationale:

- Requests protect scheduling guarantees.
- Limits prevent noisy-neighbor impact.

Improvements for production:

- Add `startupProbe` for slower startup environments.
- Add HPA (CPU/RPS based autoscaling).
- Move config to ConfigMap and secrets to Secret.

Monitoring/observability strategy:

- Scrape `/metrics` endpoint with Prometheus.
- Build Grafana dashboards and alerting rules for latency, error rate, and restarts.

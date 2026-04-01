# Lab 10 - Helm Package Manager

## 1. Chart Overview

Chart location:

- `k8s/devops-info-chart`

Structure:

- `Chart.yaml`: chart metadata and versions
- `values.yaml`: default configuration
- `values-dev.yaml`: development overrides
- `values-prod.yaml`: production overrides
- `templates/deployment.yaml`: templated Deployment
- `templates/service.yaml`: templated Service
- `templates/_helpers.tpl`: reusable names and labels
- `templates/hooks/pre-install-job.yaml`: pre-install validation Job
- `templates/hooks/post-install-job.yaml`: post-install smoke test Job

Values organization strategy:

- Grouped values by concern (`image`, `service`, `resources`, probes, hooks).
- Environment-specific overrides are isolated in dedicated files.
- Health checks are fully configurable and enabled by default.

## 2. Configuration Guide

Important values:

- `replicaCount`: number of Pod replicas
- `image.repository`, `image.tag`, `image.pullPolicy`: image configuration
- `service.type`, `service.port`, `service.targetPort`, `service.nodePort`: network exposure
- `resources.requests` and `resources.limits`: scheduling and protection
- `livenessProbe` and `readinessProbe`: health checks
- `hookJobs.*`: lifecycle hook behavior and weights

Example installs:

```bash
helm install devops-info-dev k8s/devops-info-chart -f k8s/devops-info-chart/values-dev.yaml
helm upgrade devops-info-dev k8s/devops-info-chart -f k8s/devops-info-chart/values-prod.yaml
```

## 3. Hook Implementation

Implemented hooks:

- Pre-install hook (`pre-install-job.yaml`): validates release setup before resource creation.
- Post-install hook (`post-install-job.yaml`): executes smoke test against `/health` endpoint.

Hook order and policies:

- Pre-install weight: `-5`
- Post-install weight: `5`
- Deletion policy: `before-hook-creation,hook-succeeded`

Why this setup:

- Pre-install catches obvious issues before deployment.
- Post-install confirms service is reachable from inside cluster.
- Succeeded hooks are cleaned automatically to reduce clutter.

## 4. Installation Evidence

Evidence command set:

```bash
helm version
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm show chart prometheus-community/prometheus
helm lint k8s/devops-info-chart
helm template devops-info-dev k8s/devops-info-chart -f k8s/devops-info-chart/values-dev.yaml
helm install devops-info-dev k8s/devops-info-chart -f k8s/devops-info-chart/values-dev.yaml
helm list
kubectl get all -l app.kubernetes.io/instance=devops-info-dev
helm upgrade devops-info-dev k8s/devops-info-chart -f k8s/devops-info-chart/values-prod.yaml
kubectl get deploy,svc -l app.kubernetes.io/instance=devops-info-dev
```

Outputs are saved in `k8s/docs/helm_terminal_outputs.md`.

## 5. Operations

Install:

```bash
helm install devops-info-dev k8s/devops-info-chart -f k8s/devops-info-chart/values-dev.yaml
```

Upgrade (dev -> prod profile):

```bash
helm upgrade devops-info-dev k8s/devops-info-chart -f k8s/devops-info-chart/values-prod.yaml
```

Inspect:

```bash
helm list
helm get values devops-info-dev
helm get manifest devops-info-dev
```

Uninstall:

```bash
helm uninstall devops-info-dev
```

## 6. Testing and Validation

Validation workflow:

- `helm lint` validates chart quality.
- `helm template` verifies rendered manifests locally.
- Pre and post hooks are verified using `kubectl get jobs` and `kubectl logs job/<name>`.
- Service accessibility is verified via either:
  - `kubectl port-forward service/<service-name> 8080:80` and curl, or
  - `minikube service <service-name> --url`.

Accessibility checks:

```bash
kubectl port-forward service/devops-info-dev-devops-info-chart 8080:80
curl http://127.0.0.1:8080/
curl http://127.0.0.1:8080/health
```

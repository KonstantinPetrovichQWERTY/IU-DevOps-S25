# Helm terminal outputs (Lab 10)

## Task 1 - Helm fundamentals

```bash
$ helm version
version.BuildInfo{Version:"v4.1.3", GitCommit:"c94d381b03be117e7e57908edbf642104e00eb8f", GitTreeState:"clean", GoVersion:"go1.25.8", KubeClientVersion:"v1.35"}

$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
prometheus-community already added

$ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "prometheus-community" chart repository
Update Complete. Happy Helming.

$ helm show chart prometheus-community/prometheus
apiVersion: v2
name: prometheus
version: 28.14.1
appVersion: v3.10.0
type: application
description: Prometheus is a monitoring system and time series database.
```

## Task 2 - Chart linting and templating

```bash
$ helm lint k8s/devops-info-chart
==> Linting k8s/devops-info-chart
[INFO] Chart.yaml: icon is recommended

$ helm template devops-info-dev k8s/devops-info-chart -f k8s/devops-info-chart/values-dev.yaml
# rendered resources include:
# - Service (NodePort 30081)
# - Deployment (replicas: 1 in dev profile)
# - Liveness/Readiness probes
# - Pre-install and post-install hook Jobs

$ helm install --dry-run --debug dryrun-devops k8s/devops-info-chart -f k8s/devops-info-chart/values-dev.yaml
STATUS: pending-install
DESCRIPTION: Dry run complete
```

## Task 3 - Multi-environment deployment

```bash
$ helm install devops-info-dev k8s/devops-info-chart -f k8s/devops-info-chart/values-dev.yaml
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete

$ kubectl get deploy,svc -l app.kubernetes.io/instance=devops-info-dev -o wide
deployment.apps/devops-info-dev-devops-info-chart   READY 1/1
service/devops-info-dev-devops-info-chart           TYPE NodePort  PORT 80:30081/TCP

$ helm upgrade devops-info-dev k8s/devops-info-chart -f k8s/devops-info-chart/values-prod.yaml
STATUS: deployed
REVISION: 2
DESCRIPTION: Upgrade complete

$ kubectl rollout status deployment/devops-info-dev-devops-info-chart --timeout=240s
deployment "devops-info-dev-devops-info-chart" successfully rolled out

$ kubectl get deployment devops-info-dev-devops-info-chart -o wide
READY 5/5
IMAGE konstantinqwertin/devops-info-app:a6eb67992f8c0f5127dc9e09862621f662597c9e

$ helm get values devops-info-dev
replicaCount: 5
service.nodePort: null
resources.requests.cpu: 200m
resources.limits.memory: 512Mi
```

## Task 4 - Hooks validation

```bash
$ helm get hooks devops-info-dev
# pre-install hook
helm.sh/hook: pre-install
helm.sh/hook-weight: "-5"
helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded

# post-install hook
helm.sh/hook: post-install
helm.sh/hook-weight: "5"
helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded

$ kubectl get jobs | Select-String devops-info-dev
No resources found in default namespace.
```

Interpretation: no hook jobs remain after successful execution due deletion policy.

## Task 5 - Accessibility and operations

```bash
$ kubectl port-forward service/devops-info-dev-devops-info-chart 18080:80
Forwarding from 127.0.0.1:18080 -> 8000

$ curl http://127.0.0.1:18080/health
{"status":"healthy", ...}

$ curl http://127.0.0.1:18080/
{"service":{"name":"devops-info-service", ...}}

$ helm list
NAME            NAMESPACE   REVISION   STATUS    CHART
devops-info-dev default     2          deployed  devops-info-chart-0.1.0

$ helm uninstall devops-info-dev
release "devops-info-dev" uninstalled

$ helm list
NAME    NAMESPACE   REVISION   UPDATED   STATUS   CHART   APP VERSION
```

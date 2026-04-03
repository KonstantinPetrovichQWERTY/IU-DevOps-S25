# Lab 13 - GitOps with ArgoCD

## 1. ArgoCD Setup

### 1.1 Installation (Helm)

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

kubectl create namespace argocd
helm install argocd argo/argo-cd --namespace argocd

kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=180s
kubectl get pods -n argocd
```

### 1.2 UI Access

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

Login:

- URL: `https://localhost:8080`
- Username: `admin`
- Password: from the secret above

### 1.3 CLI Access

```bash
# Install CLI (Windows with winget)
winget install -e --id argoproj.argocd

# Login and verify
argocd login localhost:8080 --insecure
argocd account get-user-info
argocd app list
```

## 2. Application Configuration

ArgoCD manifests are stored in `k8s/argocd/`.

### 2.1 Source and Destination

All applications use:

- `repoURL`: `https://github.com/KonstantinPetrovichQWERTY/IU-DevOps-S25.git`
- `targetRevision`: `master`
- `path`: `k8s/devops-info-chart`
- `destination.server`: `https://kubernetes.default.svc`

### 2.2 Apply Manifests

```bash
kubectl apply -f k8s/argocd/namespaces.yaml
kubectl apply -f k8s/argocd/application.yaml
kubectl apply -f k8s/argocd/application-dev.yaml
kubectl apply -f k8s/argocd/application-prod.yaml

argocd app list
```

### 2.3 Initial Sync

```bash
# Base app (manual sync)
argocd app sync python-app
argocd app get python-app

# Prod app (manual sync)
argocd app sync python-app-prod
argocd app get python-app-prod
```

Dev app (`python-app-dev`) should auto-sync when OutOfSync is detected.

## 3. Multi-Environment Deployment

### 3.1 Namespaces

- Development namespace: `dev`
- Production namespace: `prod`

### 3.2 Configuration Differences

- `python-app-dev` uses `values-dev.yaml`
- `python-app-prod` uses `values-prod.yaml`

Expected behavior from values files:

- Dev: fewer replicas, lower resources, debug-friendly settings
- Prod: more replicas, tighter production resource profile, production environment settings

### 3.3 Sync Policy Differences

Dev policy (`application-dev.yaml`):

- `automated.prune: true`
- `automated.selfHeal: true`
- automatically converges cluster state to Git

Prod policy (`application-prod.yaml`):

- no `automated` block
- manual sync required

Why manual sync for production:

- change review gate before rollout
- controlled deployment windows
- safer rollback planning

### 3.4 Verification

Check /docs/argocd_terminal_output.md

## 4. Self-Healing and Drift Tests

Run these tests in `python-app-dev` (auto-sync enabled).

### 4.1 Manual Scale Drift

```bash
kubectl scale deployment devops-info-dev-devops-info-chart -n dev --replicas=5
argocd app get python-app-dev
kubectl get deploy -n dev
```

Actual result in this cluster run:

- manual scale to 5 replicas succeeded (`kubectl scale ... --replicas=5`)
- ArgoCD detected `OutOfSync` within a few seconds
- ArgoCD auto-synced and restored replicas to Git value (`replicaCount=1`)
- final state: `Synced`, `Healthy`
Check /docs/argocd_terminal_output.md

### 4.2 Pod Deletion Test (Kubernetes Self-Healing)

```bash
kubectl delete pod -n dev -l app.kubernetes.io/instance=devops-info-dev
kubectl get pods -n dev -w
```

Actual result:

- deleted pod was recreated by Deployment/ReplicaSet controller
- new pod reached `Running/Ready` quickly (seconds in this run)
- confirms this behavior is Kubernetes self-healing, not ArgoCD reconciliation

### 4.3 When ArgoCD Syncs vs Kubernetes Heals

- Kubernetes heals runtime state (restarts/recreates pods to satisfy Deployment/ReplicaSet specs).
- ArgoCD heals declarative drift (cluster manifests changed outside Git).
- ArgoCD checks Git periodically (default ~3 minutes) and can also reconcile on manual sync or webhook events.

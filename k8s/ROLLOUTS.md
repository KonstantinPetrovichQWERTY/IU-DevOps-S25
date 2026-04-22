# Lab 14 - Progressive Delivery with Argo Rollouts

## Task 1 - Argo Rollouts Fundamentals

### Installation and verification

- Argo Rollouts controller and dashboard are installed in namespace `argo-rollouts`.
- kubectl plugin is installed and verified with `kubectl argo rollouts version`.
- Dashboard access command: `kubectl port-forward svc/argo-rollouts-dashboard -n argo-rollouts 3100:3100`.

Terminal evidence: [k8s/docs/argocd_rollout_terminal_outputs.md](k8s/docs/argocd_rollout_terminal_outputs.md)

## Task 2 - Canary Deployment

### Strategy configuration

Configured canary steps:

- 20% -> pause (manual)
- 40% -> pause 30s
- 60% -> pause 30s
- 80% -> pause 30s
- 100%

### Test results

- Rollout paused at canary step and required manual promotion.
- Abort operation moved rollout to `Degraded` and kept stable replica set.
- Retry + promote completed rollout to `Healthy`.

Terminal evidence: [k8s/docs/argocd_rollout_terminal_outputs.md](k8s/docs/argocd_rollout_terminal_outputs.md)

## Task 3 - Blue-Green Deployment

### Strategy configuration

Key settings:

- `activeService`: `devops-info-prod-devops-info-chart`
- `previewService`: `devops-info-prod-devops-info-chart-preview`
- `autoPromotionEnabled: false`

### Test results

- New revision created preview ReplicaSet and preview selector hash.
- Promotion and rollback (`undo`) both completed successfully.
- During first run with `replicaCount=5`, cluster capacity caused `active service cutover pending`; run was completed with `replicaCount=1` test profile.

Terminal evidence: [k8s/docs/argocd_rollout_terminal_outputs.md](k8s/docs/argocd_rollout_terminal_outputs.md)

## Task 4

### Strategy comparison

Canary:

- Pros: gradual risk reduction, checkpointed rollout.
- Cons: slower completion, more operator actions.

Blue-Green:

- Pros: clear preview/active separation, fast rollback by service switch.
- Cons: higher temporary resource demand.

When to use:

- Use Canary for incremental confidence under live traffic.
- Use Blue-Green when rollback speed and preview validation are priorities.

### CLI Commands Reference

Setup:

- `kubectl create namespace argo-rollouts`
- `kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml`
- `kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/dashboard-install.yaml`
- `kubectl argo rollouts version`

Canary:

- `kubectl argo rollouts get rollout devops-info-dev-devops-info-chart -n dev`
- `kubectl argo rollouts promote devops-info-dev-devops-info-chart -n dev`
- `kubectl argo rollouts abort devops-info-dev-devops-info-chart -n dev`
- `kubectl argo rollouts retry rollout devops-info-dev-devops-info-chart -n dev`

Blue-Green:

- `kubectl argo rollouts get rollout devops-info-prod-devops-info-chart -n prod`
- `kubectl argo rollouts promote devops-info-prod-devops-info-chart -n prod`
- `kubectl argo rollouts undo devops-info-prod-devops-info-chart -n prod`
- `kubectl get svc devops-info-prod-devops-info-chart -n prod -o jsonpath="{.spec.selector.rollouts-pod-template-hash}"`
- `kubectl get svc devops-info-prod-devops-info-chart-preview -n prod -o jsonpath="{.spec.selector.rollouts-pod-template-hash}"`

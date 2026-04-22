
# Lab 14 - Progressive Delivery with Argo Rollouts Terminal Outputs

## 1. Argo Rollouts Installation and Verification

```bash
$ kubectl create namespace argo-rollouts

Error from server (AlreadyExists): namespaces "argo-rollouts" already exists


$ kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

customresourcedefinition.apiextensions.k8s.io/rollouts.argoproj.io unchanged
serviceaccount/argo-rollouts unchanged
clusterrole.rbac.authorization.k8s.io/argo-rollouts unchanged
clusterrolebinding.rbac.authorization.k8s.io/argo-rollouts unchanged
service/argo-rollouts-metrics unchanged
deployment.apps/argo-rollouts configured
serviceaccount/argo-rollouts-dashboard unchanged
clusterrole.rbac.authorization.k8s.io/argo-rollouts-dashboard unchanged
clusterrolebinding.rbac.authorization.k8s.io/argo-rollouts-dashboard unchanged
service/argo-rollouts-dashboard unchanged
deployment.apps/argo-rollouts-dashboard unchanged


$ kubectl get pods -n argo-rollouts

NAME                                        READY   STATUS    RESTARTS   AGE
argo-rollouts-6cbc794dd5-q9jzt             1/1     Running   0          54m
argo-rollouts-dashboard-767988f986-r72bg   1/1     Running   0          54m


$ kubectl argo rollouts version

kubectl-argo-rollouts: v1.9.0+838d4e7
	BuildDate: 2026-03-20T21:15:27Z
	GitCommit: 838d4e792be666ec11bd0c80331e0c5511b5010e
	GitTreeState: clean
	GoVersion: go1.24.13
	Compiler: gc
	Platform: windows/amd64
```

Dashboard access:

```bash
kubectl port-forward svc/argo-rollouts-dashboard -n argo-rollouts 3100:3100
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

```PowerShell
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($(kubectl -n argocd get secret 
argocd-initial-admin-secret -o jsonpath="{.data.password}")))
```

---

## 2. Canary Rollout Test (dev namespace)

Apply baseline manifest for canary:

```bash
$ kubectl argo rollouts status devops-info-dev-devops-info-chart -n dev --timeout 240s

Healthy


$ kubectl argo rollouts get rollout devops-info-dev-devops-info-chart -n dev

Name:            devops-info-dev-devops-info-chart
Namespace:       dev
Status:          Paused
Message:         CanaryPauseStep
Strategy:        Canary
	Step:          1/9
	SetWeight:     20
	ActualWeight:  50
Images:          konstantinqwertin/devops-info-app:a6eb67992f8c0f5127dc9e09862621f662597c9e (stable)
								 konstantinqwertin/devops-info-app:latest (canary)
```

Trigger a revision and verify healthy state:

```bash
$ helm template devops-info-dev k8s/devops-info-chart -f k8s/devops-info-chart/values-dev.yaml --set vault.enabled=false --set image.tag=a6eb67992f8c0f5127dc9e09862621f662597c9e | kubectl apply -n dev -f -
$ kubectl argo rollouts get rollout devops-info-dev-devops-info-chart -n dev

Name:            devops-info-dev-devops-info-chart
Namespace:       dev
Status:          Healthy
Strategy:        Canary
	Step:          9/9
	SetWeight:     100
	ActualWeight:  100
Images:          konstantinqwertin/devops-info-app:a6eb67992f8c0f5127dc9e09862621f662597c9e (stable)
```

Manual promotion command used:

```bash
$ kubectl argo rollouts promote devops-info-dev-devops-info-chart -n dev

rollout 'devops-info-dev-devops-info-chart' promoted
```

Abort test during canary rollout:

```bash
$ kubectl argo rollouts abort devops-info-dev-devops-info-chart -n dev
rollout 'devops-info-dev-devops-info-chart' aborted


$ kubectl argo rollouts get rollout devops-info-dev-devops-info-chart -n dev
Name:            devops-info-dev-devops-info-chart
Namespace:       dev
Status:          Degraded
Message:         RolloutAborted: Rollout aborted update to revision 5
Strategy:        Canary
	Step:          0/9
	SetWeight:     0
	ActualWeight:  0
Images:          konstantinqwertin/devops-info-app:a6eb67992f8c0f5127dc9e09862621f662597c9e (stable)
```

Retry after abort:

```bash
$ kubectl argo rollouts retry rollout devops-info-dev-devops-info-chart -n dev

rollout 'devops-info-dev-devops-info-chart' retried
Progressing - more replicas need to be updated
Progressing - old replicas are pending termination
Paused - CanaryPauseStep

rollout 'devops-info-dev-devops-info-chart' promoted
Healthy


$ kubectl argo rollouts get rollout devops-info-dev-devops-info-chart -n dev

Name:            devops-info-dev-devops-info-chart
Namespace:       dev
Status:          Healthy
Strategy:        Canary
	Step:          9/9
	SetWeight:     100
	ActualWeight:  100
Images:          konstantinqwertin/devops-info-app:latest (stable)
```

---

## 3. Blue-Green Rollout Test (prod namespace)

Apply baseline blue-green manifest:

```bash
$ helm template devops-info-prod k8s/devops-info-chart -f k8s/devops-info-chart/values-prod.yaml --set vault.enabled=false --set image.tag=a6eb67992f8c0f5127dc9e09862621f662597c9e | kubectl apply -n prod -f -
$ kubectl argo rollouts status devops-info-prod-devops-info-chart -n prod --timeout 240s

rollout.argoproj.io/devops-info-prod-devops-info-chart unchanged
Healthy


$ kubectl argo rollouts get rollout devops-info-prod-devops-info-chart -n prod

Name:            devops-info-prod-devops-info-chart
Namespace:       prod
Status:          Healthy
Strategy:        BlueGreen
Images:          konstantinqwertin/devops-info-app:a6eb67992f8c0f5127dc9e09862621f662597c9e (stable, active)
Replicas:
	Desired:       5


$ kubectl get svc devops-info-prod-devops-info-chart -n prod -o jsonpath="active={.spec.selector.rollouts-pod-template-hash}"

active=5cfd76bddf


$ kubectl get svc devops-info-prod-devops-info-chart-preview -n prod -o jsonpath="preview={.spec.selector.rollouts-pod-template-hash}"

preview=5cfd76bddf
```

Trigger new revision and verify active/preview split:

```bash
$ helm template devops-info-prod k8s/devops-info-chart -f k8s/devops-info-chart/values-prod.yaml --set vault.enabled=false --set image.tag=latest | kubectl apply -n prod -f -

rollout.argoproj.io/devops-info-prod-devops-info-chart configured


$ kubectl argo rollouts get rollout devops-info-prod-devops-info-chart -n prod

Name:            devops-info-prod-devops-info-chart
Namespace:       prod
Status:          Progressing
Message:         more replicas need to be updated
Strategy:        BlueGreen
Images:          konstantinqwertin/devops-info-app:a6eb67992f8c0f5127dc9e09862621f662597c9e (stable, active)


$ kubectl get svc devops-info-prod-devops-info-chart -n prod -o jsonpath="active={.spec.selector.rollouts-pod-template-hash}"

active=5cfd76bddf


$ kubectl get svc devops-info-prod-devops-info-chart-preview -n prod -o jsonpath="preview={.spec.selector.rollouts-pod-template-hash}"

preview=77bcd567fb
```

# Lab 13 - ArgoCD Terminal Outputs

## 1. ArgoCD Installation and Readiness

```bash
kubectl get pods -n argocd
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=180s
```

Observed outputs:

```text
"argo" already exists with the same configuration, skipping

Error: failed to update the following repositories: [https://prometheus-community.github.io/helm-charts]
(Argo repo itself updated successfully)

Error from server (AlreadyExists): namespaces "argocd" already exists

Error: INSTALLATION FAILED: release name check failed: cannot reuse a name that is still in use

NAME                                                READY   STATUS    RESTARTS   AGE
argocd-application-controller-0                     1/1     Running   0          10h
argocd-applicationset-controller-6468558465-bpjg6   1/1     Running   0          10h
argocd-dex-server-6ffd78cb45-5cvrk                  1/1     Running   0          10h
argocd-notifications-controller-5c948d7467-kkqzz    1/1     Running   0          10h
argocd-redis-658f7d8b99-thzgw                       1/1     Running   0          10h
argocd-repo-server-546f88c95b-kpcvk                 1/1     Running   0          10h
argocd-server-9b55bbbb6-sfrts                       1/1     Running   0          10h

pod/argocd-server-9b55bbbb6-sfrts condition met
```

---

## 2. ArgoCD UI/CLI Access

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
argocd login localhost:8080 --insecure
argocd account get-user-info
argocd app list
```

Observed outputs:

```text
kubectl port-forward svc/argocd-server -n argocd 8080:443
(running in background, no errors)

argocd admin initial-password -n argocd
2jcNUTYDf5FVE5iS

argocd login localhost:8080 --insecure --username admin --password <redacted>
'admin:login' logged in successfully
Context 'localhost:8080' updated

argocd account get-user-info
Logged In: true
Username: admin
Issuer: argocd

argocd app list
NAME  CLUSTER  NAMESPACE  PROJECT  STATUS  HEALTH  SYNCPOLICY  CONDITIONS  REPO  PATH  TARGET
```

---

## 3. Apply Application Manifests

```bash
kubectl apply -f k8s/argocd/namespaces.yaml
namespace/dev created
namespace/prod created

kubectl apply -f k8s/argocd/application.yaml
application.argoproj.io/python-app created

kubectl apply -f k8s/argocd/application-dev.yaml
application.argoproj.io/python-app-dev created

kubectl apply -f k8s/argocd/application-prod.yaml
application.argoproj.io/python-app-prod created

kubectl get applications.argoproj.io -n argocd
NAME              SYNC STATUS   HEALTH STATUS
python-app        OutOfSync     Missing
python-app-dev    OutOfSync     Missing
python-app-prod   OutOfSync     Missing
```

---

## 4. Sync and Verification

```bash
argocd app sync python-app
argocd app sync python-app-prod
argocd app get python-app
argocd app get python-app-dev
argocd app get python-app-prod
kubectl get pods -n dev
kubectl get pods -n prod
argocd app list
```

Observed outputs:

```text
argocd app get python-app
Sync Policy:        Manual
Sync Status:        Synced to master (463f90b)
Health Status:      Healthy

argocd app get python-app-prod
Sync Policy:        Manual
Sync Status:        Synced to master (463f90b)
Health Status:      Progressing

argocd app get python-app-dev
Sync Policy:        Automated (Prune)
Sync Status:        Synced to master (463f90b)
Health Status:      Healthy

kubectl get pods -n dev
NAME                                                  READY   STATUS      RESTARTS        AGE
devops-info-dev-devops-info-chart-69454d7fff-qsntx   1/1     Running     8 (6m18s ago)   19m
... (additional replicas observed during manual scale test)

kubectl get pods -n prod
NAME                                                   READY   STATUS      RESTARTS        AGE
devops-info-prod-devops-info-chart-c9c97cfdf-5w2mw    1/1     Running     1               14m
devops-info-prod-devops-info-chart-c9c97cfdf-5w8kx    1/1     Running     3               14m
devops-info-prod-devops-info-chart-c9c97cfdf-s44g2    1/1     Running     2               14m
devops-info-prod-devops-info-chart-c9c97cfdf-s6zfh    1/1     Running     4               14m
devops-info-prod-devops-info-chart-c9c97cfdf-xtwf6    1/1     Running     1               14m

argocd app list
NAME                    CLUSTER                         NAMESPACE  PROJECT  STATUS  HEALTH       SYNCPOLICY  CONDITIONS  REPO                                                            PATH                   TARGET
argocd/python-app       https://kubernetes.default.svc  default    default  Synced  Healthy      Manual      <none>      https://github.com/KonstantinPetrovichQWERTY/IU-DevOps-S25.git  k8s/devops-info-chart  master
argocd/python-app-dev   https://kubernetes.default.svc  dev        default  Synced  Healthy      Auto-Prune  <none>      https://github.com/KonstantinPetrovichQWERTY/IU-DevOps-S25.git  k8s/devops-info-chart  master
argocd/python-app-prod  https://kubernetes.default.svc  prod       default  Synced  Progressing  Manual      <none>      https://github.com/KonstantinPetrovichQWERTY/IU-DevOps-S25.git  k8s/devops-info-chart  master
```

---

## 5. Self-Healing Tests

### 5.1 Manual scale drift (dev)

```bash
kubectl get deploy -n dev
kubectl scale deployment devops-info-dev-devops-info-chart -n dev --replicas=5
argocd app get python-app-dev
kubectl get deploy -n dev
```

Timestamp notes:

- Manual scale time: 2026-04-03 19:45:04 +03:00
- OutOfSync detected time: 2026-04-03 19:45:07 +03:00
- Synced time: 2026-04-03 19:45:12 +03:00

Observed outputs:

```text
kubectl get deploy -n dev
NAME                                READY   UP-TO-DATE   AVAILABLE
devops-info-dev-devops-info-chart   1/1     1            1

kubectl scale deployment devops-info-dev-devops-info-chart -n dev --replicas=5
deployment.apps/devops-info-dev-devops-info-chart scaled

kubectl get deploy -n dev
NAME                                READY   UP-TO-DATE   AVAILABLE
devops-info-dev-devops-info-chart   1/5     5            1

argocd app get python-app-dev
Sync Policy:        Automated (Prune)
Sync Status:        Synced to master (463f90b)
Health Status:      Healthy

Final deploy state after auto-heal:
NAME                                DESIRED   READY   AVAILABLE
devops-info-dev-devops-info-chart   1         1       1
```

### 5.2 Pod deletion (dev)

```bash
kubectl delete pod -n dev -l app.kubernetes.io/instance=devops-info-dev
kubectl get pods -n dev -w
```

Timestamp notes:

- Pod delete time: 2026-04-03 19:49:54 +03:00
- New pod Ready time: 2026-04-03 19:50:15 +03:00

Observed outputs:

POD_BEFORE=devops-info-dev-devops-info-chart-69454d7fff-bcsg4
POD_AFTER=devops-info-dev-devops-info-chart-69454d7fff-4f7bd

```text
kubectl delete pod -n dev -l app.kubernetes.io/instance=devops-info-dev,app.kubernetes.io/name=devops-info-chart
pod "devops-info-dev-devops-info-chart-69454d7fff-bcsg4" deleted

kubectl get pods -n dev
devops-info-dev-devops-info-chart-69454d7fff-4f7bd   1/1 Running 0 <new>
```

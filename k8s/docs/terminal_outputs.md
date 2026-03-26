# Terminal outputs

## Task 1 - Cluster setup

```bash
$ minikube start

* minikube v1.38.1 на Microsoft Windows 10 Home Single Language 22H2
* Используется драйвер docker на основе конфига пользователя
! Starting v1.39.0, minikube will default to "containerd" container runtime. See #21973 for more info.
* Using Docker Desktop driver with root privileges
* Starting "minikube" primary control-plane node in "minikube" cluster
* Pulling base image v0.0.50 ...
* Скачивается Kubernetes v1.35.1 ...
    > preloaded-images-k8s-v18-v1...:  272.45 MiB / 272.45 MiB  100.00% 4.92 Mi
    > gcr.io/k8s-minikube/kicbase...:  519.58 MiB / 519.58 MiB  100.00% 6.63 Mi
* Creating docker container (CPUs=2, Memory=3072MB) ...
* Подготавливается Kubernetes v1.35.1 на Docker 29.2.1 ...
* Configuring bridge CNI (Container Networking Interface) ...
* Компоненты Kubernetes проверяются ...
  - Используется образ gcr.io/k8s-minikube/storage-provisioner:v5
* Включенные дополнения: storage-provisioner, default-storageclass

! C:\Program Files\Docker\Docker\resources\bin\kubectl.exe is version 1.30.5, which may have incompatibilities with Kubernetes 1.35.1.
  - Want kubectl v1.35.1? Try 'minikube kubectl -- get pods -A'
* Готово! kubectl настроен для использования кластера "minikube" и "default" пространства имён по умолчанию

$ kubectl cluster-info
Kubernetes control plane is running at https://127.0.0.1:51648
CoreDNS is running at https://127.0.0.1:51648/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

$ kubectl get nodes
NAME       STATUS   ROLES           AGE     VERSION
minikube   Ready    control-plane   4m46s   v1.35.1
```

## Task 2 - Deploy application

```bash
$ kubectl apply -f k8s/deployment.yml
deployment.apps/devops-info-app created

$ kubectl apply -f k8s/service.yml
service/devops-info-service created

$ kubectl rollout status deployment/devops-info-app --timeout=180s
deployment "devops-info-app" successfully rolled out
```

```bash
$ kubectl get all -l app=devops-info-app
NAME                                  READY   STATUS    RESTARTS   AGE
pod/devops-info-app-6d9f49b4c-4xqws   1/1     Running   0          2m1s
pod/devops-info-app-6d9f49b4c-b8zlx   1/1     Running   0          87s
pod/devops-info-app-6d9f49b4c-ss5kv   1/1     Running   0          2m32s

NAME                          TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/devops-info-service   NodePort   10.111.70.198   <none>        80:30080/TCP   9m26s

NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/devops-info-app   3/3     3            3           7m31s
```

```bash
$ kubectl describe deployment devops-info-app
Name:                   devops-info-app
Namespace:              default
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
RollingUpdateStrategy:  0 max unavailable, 1 max surge
...
Liveness:   http-get http://:http/health delay=15s timeout=3s period=10s #success=1 #failure=3
Readiness:  http-get http://:http/health delay=5s timeout=2s period=5s #success=1 #failure=3
```

## Task 3 - Service connectivity

```bash
$ kubectl get pods,svc -l app=devops-info-app -o wide
NAME                                  READY   STATUS    RESTARTS   AGE     IP           NODE
pod/devops-info-app-6d9f49b4c-4xqws   1/1     Running   0          2m28s   10.244.0.8   minikube
pod/devops-info-app-6d9f49b4c-b8zlx   1/1     Running   0          114s    10.244.0.9   minikube
pod/devops-info-app-6d9f49b4c-ss5kv   1/1     Running   0          2m59s   10.244.0.7   minikube

NAME                          TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/devops-info-service   NodePort   10.111.70.198   <none>        80:30080/TCP   9m53s
```

```bash
$ kubectl port-forward service/devops-info-service 8080:80
Forwarding from 127.0.0.1:8080 -> 8000

$ curl.exe -s http://127.0.0.1:8080/
{"service":{"name":"devops-info-service","version":"1.0.0" ... }}

$ curl.exe -s http://127.0.0.1:8080/health
{"status":"healthy","timestamp":"2026-03-26T15:52:53.728598+00:00","uptime_seconds":...}
```

## Task 4 - Scaling, rolling update, rollback

```bash
$ kubectl scale deployment/devops-info-app --replicas=5
deployment.apps/devops-info-app scaled

$ kubectl rollout status deployment/devops-info-app --timeout=180s
deployment "devops-info-app" successfully rolled out

$ kubectl get deployment devops-info-app
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
devops-info-app   5/5     5            5           7h17m
```

```bash
$ kubectl set image deployment/devops-info-app devops-info-app=konstantinqwertin/devops-info-app:a6eb67992f8c0f5127dc9e09862621f662597c9e
deployment.apps/devops-info-app image updated

$ kubectl rollout status deployment/devops-info-app --timeout=240s
Waiting for deployment "devops-info-app" rollout to finish: 1 out of 5 new replicas have been updated...
Waiting for deployment "devops-info-app" rollout to finish: 2 out of 5 new replicas have been updated...
Waiting for deployment "devops-info-app" rollout to finish: 3 out of 5 new replicas have been updated...
Waiting for deployment "devops-info-app" rollout to finish: 4 out of 5 new replicas have been updated...
deployment "devops-info-app" successfully rolled out

$ kubectl rollout history deployment/devops-info-app
REVISION  CHANGE-CAUSE
1         <none>
3         kubectl.exe set image deployment/devops-info-app devops-info-app=konstantinqwertin/devops-info:a6eb67992f8c0f5127dc9e09862621f662597c9e         <none>
5         <none>
8         kubectl.exe set image deployment/devops-info-app devops-info-app=konstantinqwertin/devops-info-app:latest --record=true
9         <none>

```

```bash
$ kubectl rollout undo deployment/devops-info-app
deployment.apps/devops-info-app rolled back

$ kubectl rollout status deployment/devops-info-app --timeout=240s
deployment "devops-info-app" successfully rolled out
```

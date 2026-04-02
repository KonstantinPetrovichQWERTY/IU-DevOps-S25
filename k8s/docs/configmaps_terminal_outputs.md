# ConfigMaps and PVC terminal outputs (Lab 12)

## Task 1 - Local Docker persistence

```bash
cd app_python
docker compose up --build -d
```

```text
[+] Building ... FINISHED
[+] Running 2/2
 ✔ Network app_python_default  Created
 ✔ Container devops-info-app   Started
```

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/visits
cat ./data/visits
docker compose restart
curl http://127.0.0.1:8000/visits
```

```text
"runtime": { ... "visits_count": 5 }
"runtime": { ... "visits_count": 6 }
{"visits":6}
6
Container devops-info-app  Started
{"visits":6}
```

## Task 2 - ConfigMap verification

```bash
helm lint k8s/devops-info-chart
```

```text
==> Linting k8s/devops-info-chart
[INFO] Chart.yaml: icon is recommended
1 chart(s) linted, 0 chart(s) failed
```

```bash
helm template devops-info-dev k8s/devops-info-chart -f k8s/devops-info-chart/values-dev.yaml
```

```text
# rendered resources include:
# - ConfigMap (file-based config.json)
# - ConfigMap (env key-value pairs)
# - PersistentVolumeClaim
# - Deployment with config and data volume mounts
```

```bash
helm upgrade --install lab12-proof k8s/devops-info-chart -f k8s/devops-info-chart/values-dev.yaml
kubectl rollout status deployment/lab12-proof-devops-info-chart --timeout=180s
```

```text
Release "lab12-proof" has been upgraded. Happy Helming!
deployment "lab12-proof-devops-info-chart" successfully rolled out
```

```bash
kubectl get configmap,pvc -l app.kubernetes.io/instance=lab12-proof
```

```text
NAME                                             DATA   AGE
configmap/lab12-proof-devops-info-chart-config   1      14m
configmap/lab12-proof-devops-info-chart-env      4      14m

NAME                                                       STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistentvolumeclaim/lab12-proof-devops-info-chart-data   Bound    pvc-5fb70357-0aad-4e63-84e6-6de8d70cf8fd   100Mi      RWO            standard       14m
```

```bash
kubectl exec lab12-proof-devops-info-chart-686966b547-48kv8 -- cat /config/config.json
```

```text
{
  "application": {
    "name": "devops-info-service",
    "environment": "dev",
    "version": "1.0.0"
  },
  "features": {
    "enable_visits_counter": true,
    "enable_metrics_endpoint": true
  },
  "settings": {
    "log_level": "DEBUG"
  }
}
```

```bash
kubectl exec lab12-proof-devops-info-chart-686966b547-48kv8 -- printenv | grep -E "APP_ENV|LOG_LEVEL|VISITS_FILE|FEATURE_VISITS_COUNTER"
```

```text
FEATURE_VISITS_COUNTER=true
LOG_LEVEL=DEBUG
VISITS_FILE=/data/visits
APP_ENV=dev
```

## Task 3 - PVC persistence verification

```bash
# in defferent terminal
kubectl port-forward service/lab12-proof-devops-info-chart 18080:80

# before pod deletion
curl http://127.0.0.1:18080/
curl http://127.0.0.1:18080/
curl http://127.0.0.1:18080/visits
kubectl exec <pod-before> -- cat /data/visits

# recreate pod
kubectl delete pod <pod-before>
kubectl wait --for=condition=Ready pod -l app.kubernetes.io/instance=lab12-proof --timeout=180s

# after pod recreation
kubectl exec <pod-after> -- cat /data/visits
curl http://127.0.0.1:18080/visits
```

POD_BEFORE=lab12-proof-devops-info-chart-686966b547-sttdf

```text
curl / -> {...}
curl / -> {...}
curl /visits -> {"visits":3}
cat /data/visits -> 3

pod "lab12-proof-devops-info-chart-686966b547-sttdf" deleted
pod/lab12-proof-devops-info-chart-686966b547-48kv8 condition met

cat /data/visits -> 3
curl /visits -> {"visits":3}
```

# StatefulSet Lab - Terminal Outputs

## Deploy StatefulSet release

```bash
$ helm upgrade --install lab15-stateful ./k8s/devops-info-chart --set workload.kind=statefulset --set replicaCount=3

Release "lab15-stateful" does not exist. Installing it now.
NAME: lab15-stateful
NAMESPACE: default
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
TEST SUITE: None


$ kubectl rollout status statefulset/lab15-stateful-devops-info-chart --timeout=240s

Waiting for 1 pods to be ready...
partitioned roll out complete: 3 new pods have been updated...
```

## Resource verification

```bash
$ kubectl get po,sts,svc,pvc -l app.kubernetes.io/instance=lab15-stateful -o wide
NAME                                     READY   STATUS    RESTARTS   AGE   IP             NODE       NOMINATED NODE   READINESS GATES
pod/lab15-stateful-devops-info-chart-0   1/1     Running   0          30s   10.244.0.209   minikube   <none>           <none>
pod/lab15-stateful-devops-info-chart-1   1/1     Running   0          20s   10.244.0.210   minikube   <none>           <none>
pod/lab15-stateful-devops-info-chart-2   1/1     Running   0          10s   10.244.0.211   minikube   <none>           <none>

NAME                                                READY   AGE   CONTAINERS          IMAGES
statefulset.apps/lab15-stateful-devops-info-chart   3/3     30s   devops-info-chart   konstantinqwertin/devops-info-app:latest

NAME                                                TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)        AGE   SELECTOR
service/lab15-stateful-devops-info-chart            NodePort    10.97.56.54   <none>        80:31818/TCP   30s   app.kubernetes.io/instance=lab15-stateful,app.kubernetes.io/name=devops-info-chart
service/lab15-stateful-devops-info-chart-headless   ClusterIP   None          <none>        80/TCP         30s   app.kubernetes.io/instance=lab15-stateful,app.kubernetes.io/name=devops-info-chart

NAME                                                                   STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE   VOLUMEMODE
persistentvolumeclaim/data-volume-lab15-stateful-devops-info-chart-0   Bound    pvc-8bbd2ad9-0b25-4eaf-9e20-a81544e28c82   100Mi      RWO            standard       <unset>                 30s   Filesystem
persistentvolumeclaim/data-volume-lab15-stateful-devops-info-chart-1   Bound    pvc-c917492c-71db-43d8-89cb-085492fa7592   100Mi      RWO            standard       <unset>                 20s   Filesystem
persistentvolumeclaim/data-volume-lab15-stateful-devops-info-chart-2   Bound    pvc-361b43fd-bfd0-47f2-9dff-341151fb15de   100Mi      RWO            standard       <unset>                 10s   Filesystem
```

## DNS and stable pod identity

```bash
$ kubectl exec lab15-stateful-devops-info-chart-0 -- python -c "import socket; print(socket.gethostbyname('lab15-stateful-devops-info-chart-1.lab15-stateful-devops-info-chart-headless'))"
10.244.0.210

$ kubectl exec lab15-stateful-devops-info-chart-0 -- python -c "import socket; print(socket.gethostbyname('lab15-stateful-devops-info-chart-2.lab15-stateful-devops-info-chart-headless'))"
10.244.0.211

$ kubectl exec lab15-stateful-devops-info-chart-0 -- sh -c "hostname"
lab15-stateful-devops-info-chart-0
$ kubectl exec lab15-stateful-devops-info-chart-1 -- sh -c "hostname"
lab15-stateful-devops-info-chart-1
$ kubectl exec lab15-stateful-devops-info-chart-2 -- sh -c "hostname"
lab15-stateful-devops-info-chart-2
```

## Per-pod storage isolation

```bash
$ # pod-0 two times, pod-1 one time, pod-2 three times
$ kubectl exec lab15-stateful-devops-info-chart-0 -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/').status)"
200
$ kubectl exec lab15-stateful-devops-info-chart-0 -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/').status)"
200
$ kubectl exec lab15-stateful-devops-info-chart-1 -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/').status)"
200
$ kubectl exec lab15-stateful-devops-info-chart-2 -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/').status)"
200
$ kubectl exec lab15-stateful-devops-info-chart-2 -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/').status)"
200
$ kubectl exec lab15-stateful-devops-info-chart-2 -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/').status)"
200
```

```bash
$ kubectl exec lab15-stateful-devops-info-chart-0 -- cat /data/visits
2
$ kubectl exec lab15-stateful-devops-info-chart-1 -- cat /data/visits
1
$ kubectl exec lab15-stateful-devops-info-chart-2 -- cat /data/visits
3

$ kubectl exec lab15-stateful-devops-info-chart-0 -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/visits').read().decode())"
{"visits":2}
$ kubectl exec lab15-stateful-devops-info-chart-1 -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/visits').read().decode())"
{"visits":1}
$ kubectl exec lab15-stateful-devops-info-chart-2 -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/visits').read().decode())"
{"visits":3}
```

## Persistence test after pod deletion

```bash
$ kubectl exec lab15-stateful-devops-info-chart-0 -- cat /data/visits
2

$ kubectl delete pod lab15-stateful-devops-info-chart-0
pod "lab15-stateful-devops-info-chart-0" deleted

$ kubectl rollout status statefulset/lab15-stateful-devops-info-chart --timeout=240s
Waiting for 1 pods to be ready...
partitioned roll out complete: 3 new pods have been updated...

$ kubectl exec lab15-stateful-devops-info-chart-0 -- cat /data/visits
2
```

## Final snapshot

```bash
$ kubectl get po,sts,svc,pvc -l app.kubernetes.io/instance=lab15-stateful
NAME                                     READY   STATUS    RESTARTS   AGE
pod/lab15-stateful-devops-info-chart-0   1/1     Running   0          87s
pod/lab15-stateful-devops-info-chart-1   1/1     Running   0          4m11s
pod/lab15-stateful-devops-info-chart-2   1/1     Running   0          4m1s

NAME                                                READY   AGE
statefulset.apps/lab15-stateful-devops-info-chart   3/3     4m21s

NAME                                                TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)        AGE
service/lab15-stateful-devops-info-chart            NodePort    10.97.56.54   <none>        80:31818/TCP   4m21s
service/lab15-stateful-devops-info-chart-headless   ClusterIP   None          <none>        80/TCP         4m21s

NAME                                                                   STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/data-volume-lab15-stateful-devops-info-chart-0   Bound    pvc-8bbd2ad9-0b25-4eaf-9e20-a81544e28c82   100Mi      RWO            standard       <unset>                 4m21s
persistentvolumeclaim/data-volume-lab15-stateful-devops-info-chart-1   Bound    pvc-c917492c-71db-43d8-89cb-085492fa7592   100Mi      RWO            standard       <unset>                 4m11s
persistentvolumeclaim/data-volume-lab15-stateful-devops-info-chart-2   Bound    pvc-361b43fd-bfd0-47f2-9dff-341151fb15de   100Mi      RWO            standard       <unset>                 4m1s
```

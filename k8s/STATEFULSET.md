# Lab 15 - StatefulSets and Persistent Storage

## Task 2 - Helm conversion to StatefulSet

### Chart changes

- Added `workload.kind` switch in values (`rollout` or `statefulset`)
- Added `templates/statefulset.yaml`
- Added `templates/service-headless.yaml` (`clusterIP: None`)
- Added helper `headlessServiceName` in `_helpers.tpl`
- Wrapped `templates/rollout.yaml` with condition for rollout mode only
- Wrapped `templates/pvc.yaml` so shared PVC is not created in StatefulSet mode
- Added `persistence.accessMode` in values

StatefulSet was deployed with:

```bash
helm upgrade --install lab15-stateful ./k8s/devops-info-chart --set workload.kind=statefulset --set replicaCount=3
```

Evidence: [k8s/docs/statefulset_terminal_outputs.md](k8s/docs/statefulset_terminal_outputs.md)

## Task 3 - Identity and storage verification

### Resource verification

StatefulSet + headless service + per-pod PVCs are all present and bound.

Evidence: [k8s/docs/statefulset_terminal_outputs.md](k8s/docs/statefulset_terminal_outputs.md)

### DNS and pod identity

Verified from pod `lab15-stateful-devops-info-chart-0`:

- `lab15-stateful-devops-info-chart-1.lab15-stateful-devops-info-chart-headless` resolved to pod-1 IP
- `lab15-stateful-devops-info-chart-2.lab15-stateful-devops-info-chart-headless` resolved to pod-2 IP

Observed hostname pattern confirms stable identity:

- `lab15-stateful-devops-info-chart-0`
- `lab15-stateful-devops-info-chart-1`
- `lab15-stateful-devops-info-chart-2`

### Per-pod storage isolation

Generated different request counts on each pod by calling `/` endpoint directly inside each pod:

- pod-0: 2 requests
- pod-1: 1 request
- pod-2: 3 requests

Verified separate persisted values:

- pod-0 `/data/visits` = 2
- pod-1 `/data/visits` = 1
- pod-2 `/data/visits` = 3

This proves each pod has its own PVC-backed storage.

### Persistence after pod deletion

For pod-0:

- Before deletion: `/data/visits` = 2
- Deleted only pod-0 (`kubectl delete pod ...-0`)
- StatefulSet recreated pod-0
- After recreation: `/data/visits` = 2

Data survived pod restart, confirming persistent volume continuity.

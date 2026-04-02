# Lab 12 - ConfigMaps and Persistent Volumes

## 1. Application Changes

### 1.1 Visits Counter Implementation

The FastAPI app was updated to support persistent visit tracking:

- Added file-based counter storage (default path: `data/visits`)
- Root endpoint (`GET /`) now increments the counter on each request
- Added new endpoint `GET /visits` to return current counter value

### 1.2 New Endpoint

`GET /visits` response example:

```json
{
  "visits": 12
}
```

### 1.3 Local Testing with Docker Compose

A Docker Compose setup was added with persistent volume mapping:

- Host path: `./data`
- Container path: `/data`
- `VISITS_FILE=/data/visits`

Terminal output evidence is saved in `k8s/docs/configmaps_terminal_outputs.md`.

---

## 2. ConfigMap Implementation

### 2.1 Files Added

- `k8s/devops-info-chart/files/config.json`
- `k8s/devops-info-chart/templates/configmap.yaml`

### 2.2 ConfigMap template structure

The ConfigMap template defines two resources in one file:

- File-based ConfigMap with `config.json` loaded from chart files
- Env-based ConfigMap with key-value pairs from `values.yaml`

This structure keeps static application config and runtime environment variables separated, which makes overrides easier for different environments.

### 2.3 config.json content

The `config.json` file contains non-sensitive application settings:

- Application metadata (`name`, `environment`, `version`)
- Feature flags (`enable_visits_counter`, `enable_metrics_endpoint`)
- Logging setting (`log_level`)

Values are rendered from Helm values (`.Values`) and chart metadata (`.Chart.AppVersion`) so the same template works for dev and prod.

### 2.4 File-Based ConfigMap

The chart uses `.Files.Get` + `tpl` to load `files/config.json` into ConfigMap data:

- ConfigMap name: `<release>-devops-info-chart-config`
- Mounted in pod at `/config`
- File path in container: `/config/config.json`

Template snippet:

```yaml
data:
  config.json: |-
    {{- tpl (.Files.Get "files/config.json") . | nindent 4 }}
```

### 2.5 Environment Variables ConfigMap

A second ConfigMap provides key-value environment variables:

- ConfigMap name: `<release>-devops-info-chart-env`
- Injected via `envFrom`
- Includes values like:
  - `APP_ENV`
  - `LOG_LEVEL`
  - `FEATURE_VISITS_COUNTER`
  - `VISITS_FILE`

Deployment wiring:

```yaml
envFrom:
  - configMapRef:
      name: {{ include "devops-info-chart.envConfigMapName" . }}
```

### 2.6 Verification

Saved in `k8s/docs/configmaps_terminal_outputs.md`.

---

## 3. Persistent Volume Implementation

### 3.1 PVC Template

Added:

- `k8s/devops-info-chart/templates/pvc.yaml`

Configuration:

- `accessModes: [ReadWriteOnce]`
- Storage request from values: `.Values.persistence.size`
- Optional storage class from `.Values.persistence.storageClass`

Default values:

```yaml
persistence:
  enabled: true
  size: 100Mi
  storageClass: ""
  mountPath: /data
```

### 3.2 Deployment Mount

Deployment now mounts the PVC at `/data`:

```yaml
volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName: {{ include "devops-info-chart.pvcName" . }}

volumeMounts:
  - name: data-volume
    mountPath: /data
```

The application writes visits counter to `/data/visits` (via `VISITS_FILE` env var from ConfigMap).

### 3.3 Persistence Test Procedure

Detailed command outputs are saved in `k8s/docs/configmaps_terminal_outputs.md`.

---

## 4. ConfigMap vs Secret

### Use ConfigMap when

- Data is non-sensitive
- You need application settings, feature flags, ports, mode, log level
- You want plain-text configuration files or env vars

### Use Secret when

- Data is sensitive (passwords, API keys, tokens, certificates)
- Access should be more restricted
- You want to avoid storing plaintext credentials in manifests/values

### Key Differences

- Sensitivity:
  - ConfigMap: non-sensitive
  - Secret: sensitive
- Storage format:
  - ConfigMap: plain text
  - Secret: base64-encoded values (not encryption by itself)
- Typical use:
  - ConfigMap: app config, flags, non-secret env vars
  - Secret: credentials and private material

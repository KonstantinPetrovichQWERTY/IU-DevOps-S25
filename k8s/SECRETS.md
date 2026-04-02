# Lab 11 - Kubernetes Secrets and HashiCorp Vault

## 1. Kubernetes Secrets

Created secret using imperative kubectl command:

```bash
kubectl create secret generic app-credentials \
  --from-literal=username=lab11_user \
  --from-literal=password=lab11_password
```

Secret inspection and decoding:

- Secret YAML contains base64-encoded values (not plaintext).
- Decoding reproduces original values.
- Evidence is available in k8s/docs/secrets_terminal_outputs.md.

Encoding vs encryption:

- Base64 is only an encoding format for transport/storage readability.
- Base64 provides zero cryptographic protection.
- Kubernetes Secrets are not encrypted at rest unless etcd encryption is explicitly enabled on the cluster.

Security implications:

- Anyone with sufficient API/RBAC access can read and decode Secrets.
- Production clusters should enable etcd encryption at rest and least-privilege RBAC.
- Use external secret managers for stronger controls and rotation.

## 2. Helm Secret Integration

Chart updates:

- Added secret template: k8s/devops-info-chart/templates/secrets.yaml.
- Added service account template: k8s/devops-info-chart/templates/serviceaccount.yaml.
- Updated deployment to consume secrets via `envFrom.secretRef`:
  - k8s/devops-info-chart/templates/deployment.yaml.
- Added values for secret management in:
  - k8s/devops-info-chart/values.yaml
  - k8s/devops-info-chart/values-dev.yaml
  - k8s/devops-info-chart/values-prod.yaml

How secrets are consumed:

- Secret resource is created by Helm from values using `stringData`.
- Pod imports all secret keys using:

```yaml
envFrom:
  - secretRef:
      name: <release-secret-name>
```

Verification:

- App pod contains expected env keys (`username`, `password`).
- Verification output in docs is redacted (`<redacted>`).
- `kubectl describe pod` shows secret reference, not secret values.

## 3. Resource Management

Resource configuration remains values-driven and is applied in deployment template.

Current defaults:

- requests: cpu=100m, memory=128Mi
- limits: cpu=250m, memory=256Mi

Environment overrides:

- dev: lighter footprint (50m/64Mi requests, 100m/128Mi limits)
- prod profile available for stronger limits

Requests vs limits:

- Requests guide scheduling guarantees.
- Limits cap maximum resource usage.
- Balanced values reduce noisy-neighbor effects and improve cluster stability.

## 4. Vault Integration

Installation:

- Vault installed via official HashiCorp Vault Helm chart source (local clone of hashicorp/vault-helm due direct registry access restrictions).
- Dev mode enabled and injector enabled.

Verification:

- `vault-0` and `vault-agent-injector` are both Running.
- Vault server status: initialized, unsealed.

Vault configuration performed:

1. Stored app secret at `secret/devops-info/config` with multiple keys.
2. Enabled/configured Kubernetes auth method.
3. Created policy `devops-info-policy` with read access to `secret/data/devops-info/config`.
4. Created role `devops-info-role` bound to service account `devops-info-lab11-devops-info-chart` in namespace `default`.

Injection pattern in deployment:

- Added annotations in pod template when `vault.enabled=true`:
  - `vault.hashicorp.com/agent-inject: "true"`
  - `vault.hashicorp.com/role: "devops-info-role"`
  - `vault.hashicorp.com/agent-inject-secret-vault-config: "secret/data/devops-info/config"`

Injection proof:

- Pod is Running with sidecar (`2/2` containers).
- File exists at `/vault/secrets/vault-config`.
- File content contains Vault secret payload.

All command evidence is in k8s/docs/secrets_terminal_outputs.md.

## 5. Security Analysis

Kubernetes Secrets vs Vault:

- Kubernetes Secrets:
  - Native and simple.
  - Good for low-complexity internal configs.
  - Requires extra cluster hardening for production-grade security.
- Vault:
  - Centralized secret lifecycle and policy model.
  - Fine-grained auth and audit capabilities.
  - Better for dynamic credentials and cross-platform secret governance.

When to use each:

- Use Kubernetes Secrets for simple dev/test or low-risk internal values.
- Use Vault for production workloads, regulated environments, credential rotation, and multi-team environments.

Production recommendations:

- Enable etcd encryption at rest.
- Enforce strict RBAC for secret access.
- Avoid committing real secrets to Git.
- Prefer Vault (or equivalent external manager) for sensitive credentials.
- Add secret rotation and monitoring/alerting for failed injections.

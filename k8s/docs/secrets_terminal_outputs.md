# Lab 11 terminal outputs

## Task 1 - Kubernetes Secrets fundamentals

```bash
$ kubectl create secret generic app-credentials --from-literal=username=lab11_user --from-literal=password=lab11_password
secret/app-credentials created

$ kubectl get secret app-credentials -o yaml
apiVersion: v1
data:
  password: bGFiMTFfcGFzc3dvcmQ=
  username: bGFiMTFfdXNlcg==
kind: Secret
metadata:
  name: app-credentials
  namespace: default
type: Opaque

# base64 decode demonstration
username(decoded)=lab11_user
password(decoded)=lab11_password
```

## Task 2 - Helm-managed secrets

```bash
$ helm upgrade --install devops-info-lab11 k8s/devops-info-chart -f k8s/devops-info-chart/values-dev.yaml --set k8sSecret.data.username=helm_user --set k8sSecret.data.password=helm_password --set vault.enabled=false
STATUS: deployed

$ kubectl get secret devops-info-lab11-devops-info-chart-k8s-secret -o yaml
apiVersion: v1
data:
  password: aGVsbV9wYXNzd29yZA==
  username: aGVsbV91c2Vy
kind: Secret
type: Opaque

$ kubectl exec <app-pod> -- printenv | grep -E '^(username|password)='
username=<redacted>
password=<redacted>

$ kubectl describe pod <app-pod>
Environment Variables from:
  devops-info-lab11-devops-info-chart-k8s-secret  Secret  Optional: false
```

## Task 3 - Vault integration

```bash
$ helm install vault .tmp/vault-helm --namespace default --set "server.dev.enabled=true" --set "injector.enabled=true"
STATUS: deployed

$ kubectl get pods -n default -l app.kubernetes.io/instance=vault
vault-0                                 1/1 Running
vault-agent-injector-848dd747d7-sg2v4   1/1 Running

$ kubectl exec vault-0 -- vault status
Sealed  false
Version 1.21.2
Storage Type inmem

$ kubectl exec vault-0 -- sh -c "export VAULT_ADDR=http://127.0.0.1:8200; export VAULT_TOKEN=root; vault kv put secret/devops-info/config username=vault_user password=vault_password api_key=vault_api_key_123"
Success! Data written to: secret/data/devops-info/config

$ kubectl exec vault-0 -- sh -c "export VAULT_ADDR=http://127.0.0.1:8200; export VAULT_TOKEN=root; vault write auth/kubernetes/config ..."
Success! Data written to: auth/kubernetes/config

$ kubectl exec vault-0 -- sh /tmp/vault_configure.sh
Success! Data written to: sys/policies/acl/devops-info-policy
# role: devops-info-role bound to service account devops-info-lab11-devops-info-chart

$ helm upgrade devops-info-lab11 k8s/devops-info-chart -f k8s/devops-info-chart/values-dev.yaml --set vault.enabled=true --set vault.role=devops-info-role --set vault.secretPath=secret/data/devops-info/config --set vault.injectedFileName=vault-config
STATUS: deployed

$ kubectl get pods -l app.kubernetes.io/instance=devops-info-lab11
devops-info-lab11-devops-info-chart-797dd44fc4-8rfbj   2/2 Running

$ kubectl exec devops-info-lab11-devops-info-chart-797dd44fc4-8rfbj -c devops-info-chart -- ls -la /vault/secrets
vault-config

$ kubectl exec devops-info-lab11-devops-info-chart-797dd44fc4-8rfbj -c devops-info-chart -- cat /vault/secrets/vault-config
data: map[api_key:vault_api_key_123 password:vault_password username:vault_user]
```

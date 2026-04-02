#!/bin/sh
set -e

export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root

vault write sys/policies/acl/devops-info-policy policy='path "secret/data/devops-info/config" { capabilities = ["read"] }'

vault write auth/kubernetes/role/devops-info-role \
  bound_service_account_names=devops-info-lab11-devops-info-chart \
  bound_service_account_namespaces=default \
  policies=devops-info-policy \
  ttl=1h

vault read auth/kubernetes/role/devops-info-role

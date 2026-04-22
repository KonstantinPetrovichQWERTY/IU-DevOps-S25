{{/* Expand the chart name. */}}
{{- define "devops-info-chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Create a fully qualified app name. */}}
{{- define "devops-info-chart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/* Chart label. */}}
{{- define "devops-info-chart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Common labels. */}}
{{- define "devops-info-chart.labels" -}}
helm.sh/chart: {{ include "devops-info-chart.chart" . }}
{{ include "devops-info-chart.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/* Labels used by selectors. */}}
{{- define "devops-info-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "devops-info-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/* ServiceAccount name */}}
{{- define "devops-info-chart.serviceAccountName" -}}
{{- if .Values.serviceAccount.name }}
{{- .Values.serviceAccount.name }}
{{- else }}
{{- include "devops-info-chart.fullname" . }}
{{- end }}
{{- end }}

{{/* Kubernetes Secret name */}}
{{- define "devops-info-chart.k8sSecretName" -}}
{{- if .Values.k8sSecret.name }}
{{- .Values.k8sSecret.name }}
{{- else }}
{{- printf "%s-k8s-secret" (include "devops-info-chart.fullname" .) }}
{{- end }}
{{- end }}

{{/* ConfigMap with file-based app config */}}
{{- define "devops-info-chart.configMapName" -}}
{{- printf "%s-config" (include "devops-info-chart.fullname" .) }}
{{- end }}

{{/* ConfigMap with environment variables */}}
{{- define "devops-info-chart.envConfigMapName" -}}
{{- printf "%s-env" (include "devops-info-chart.fullname" .) }}
{{- end }}

{{/* PersistentVolumeClaim name */}}
{{- define "devops-info-chart.pvcName" -}}
{{- printf "%s-data" (include "devops-info-chart.fullname" .) }}
{{- end }}

{{/* Preview service name for blue-green strategy */}}
{{- define "devops-info-chart.previewServiceName" -}}
{{- if .Values.rollout.blueGreen.previewServiceName }}
{{- .Values.rollout.blueGreen.previewServiceName }}
{{- else }}
{{- printf "%s-preview" (include "devops-info-chart.fullname" .) }}
{{- end }}
{{- end }}

{{/* Headless service name for StatefulSet network identity */}}
{{- define "devops-info-chart.headlessServiceName" -}}
{{- printf "%s-headless" (include "devops-info-chart.fullname" .) }}
{{- end }}

variable "yc_token" {
  description = "Yandex Cloud OAuth token or service account key"
  type        = string
  sensitive   = true
}

variable "cloud_id" {
  description = "Yandex Cloud ID"
  type        = string
}

variable "folder_id" {
  description = "Yandex Cloud Folder ID"
  type        = string
}

variable "zone" {
  description = "Yandex Cloud zone"
  type        = string
  default     = "ru-central1-a"
}

variable "project_name" {
  description = "Project name for resource tagging"
  type        = string
  default     = "terraform-vm-project"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "development"
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key file"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "your_ip" {
  description = "Your public IP address for SSH access"
  type        = string
}
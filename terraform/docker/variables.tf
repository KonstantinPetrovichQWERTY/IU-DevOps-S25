variable "container_name" {
  description = "Value of the name for the Docker container"
  type    = string
  default = "app_python"
}

variable "image_name" {
  description = "Value of the name for the Docker image"
  type    = string
  default = "ilsiia/app_python:latest"
}
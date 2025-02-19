terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {
  host    = "npipe:////.//pipe//docker_engine" # Remove this row if you use Linux or MacOS
}

resource "docker_image" "python_app" {
  name = "python:3.11"
}

resource "docker_container" "python_container" {
  name  = var.container_name
  image = var.image_name
  ports {
    internal = 8000
    external = 8000
  }
}

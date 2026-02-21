terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = var.zone
}

resource "yandex_vpc_network" "network" {
  name        = "${var.project_name}-network"
  description = "Network for ${var.project_name} VM"
}

resource "yandex_vpc_subnet" "subnet" {
  name           = "${var.project_name}-subnet"
  description    = "Subnet for ${var.project_name} VM"
  zone           = var.zone
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = ["192.168.1.0/24"]
}

resource "yandex_vpc_security_group" "security_group" {
  name        = "${var.project_name}-security-group"
  description = "Security group for ${var.project_name} VM"
  network_id  = yandex_vpc_network.network.id

  ingress {
    protocol       = "TCP"
    description    = "SSH access"
    port           = 22
    v4_cidr_blocks = ["${var.your_ip}/32"]
  }

  ingress {
    protocol       = "TCP"
    description    = "HTTP access"
    port           = 80
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol       = "TCP"
    description    = "Application port"
    port           = 5000
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol       = "ANY"
    description    = "All outbound traffic"
    v4_cidr_blocks = ["0.0.0.0/0"]
    from_port      = 0
    to_port        = 65535
  }
}

data "yandex_compute_image" "ubuntu" {
  family = "ubuntu-2004-lts"
}

# Create VM instance
resource "yandex_compute_instance" "vm" {
  name        = "${var.project_name}-vm"
  description = "VM instance for ${var.project_name}"
  platform_id = "standard-v2"
  zone        = var.zone
  hostname    = "${var.project_name}-vm"

  labels = {
    environment = var.environment
    managed_by  = "terraform"
    project     = var.project_name
  }

  resources {
    cores         = 2
    memory        = 1
    core_fraction = 20
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.ubuntu.id
      size     = 10
      type     = "network-hdd"
    }
  }

  network_interface {
    subnet_id          = yandex_vpc_subnet.subnet.id
    security_group_ids = [yandex_vpc_security_group.security_group.id]
    nat                = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file(var.ssh_public_key_path)}"
  }
}
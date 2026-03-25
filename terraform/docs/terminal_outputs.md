# Terminal ouputs


## terraform plan 

```bash
$terraform plan                                                                                     
data.yandex_compute_image.ubuntu: Reading...
data.yandex_compute_image.ubuntu: Read complete after 0s [id=fd84es6pnho7mpbjerv1]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # yandex_compute_instance.vm will be created
  + resource "yandex_compute_instance" "vm" {
      + created_at                = (known after apply)
      + description               = "VM instance for iu-devops"
      + folder_id                 = (known after apply)
      + fqdn                      = (known after apply)
      + gpu_cluster_id            = (known after apply)
      + hardware_generation       = (known after apply)
      + hostname                  = "iu-devops-vm"
      + id                        = (known after apply)
      + labels                    = {
          + "environment" = "development"
          + "managed_by"  = "terraform"
          + "project"     = "iu-devops"
        }
      + maintenance_grace_period  = (known after apply)
      + maintenance_policy        = (known after apply)
      + metadata                  = {
          + "ssh-keys" = <<-EOT
            EOT
        }
      + name                      = "iu-devops-vm"
      + network_acceleration_type = "standard"
      + platform_id               = "standard-v2"
      + status                    = (known after apply)
      + zone                      = "ru-central1-b"

      + boot_disk {
          + auto_delete = true
          + device_name = (known after apply)
          + disk_id     = (known after apply)
          + mode        = (known after apply)

          + initialize_params {
              + block_size  = (known after apply)
              + description = (known after apply)
              + image_id    = "fd84es6pnho7mpbjerv1"
              + name        = (known after apply)
              + size        = 10
              + snapshot_id = (known after apply)
              + type        = "network-hdd"
            }
        }

      + metadata_options (known after apply)

      + network_interface {
          + index              = (known after apply)
          + ip_address         = (known after apply)
          + ipv4               = true
          + ipv6               = (known after apply)
          + ipv6_address       = (known after apply)
          + mac_address        = (known after apply)
          + nat                = true
          + nat_ip_address     = (known after apply)
          + nat_ip_version     = (known after apply)
          + security_group_ids = (known after apply)
          + subnet_id          = (known after apply)
        }

      + placement_policy (known after apply)

      + resources {
          + core_fraction = 20
          + cores         = 2
          + memory        = 1
        }

      + scheduling_policy (known after apply)
    }

  # yandex_vpc_network.network will be created
  + resource "yandex_vpc_network" "network" {
      + created_at                = (known after apply)
      + default_security_group_id = (known after apply)
      + description               = "Network for iu-devops VM"
      + folder_id                 = (known after apply)
      + id                        = (known after apply)
      + labels                    = (known after apply)
      + name                      = "iu-devops-network"
      + subnet_ids                = (known after apply)
    }

  # yandex_vpc_security_group.security_group will be created
  + resource "yandex_vpc_security_group" "security_group" {
      + created_at  = (known after apply)
      + description = "Security group for iu-devops VM"
      + folder_id   = (known after apply)
      + id          = (known after apply)
      + labels      = (known after apply)
      + name        = "iu-devops-security-group"
      + network_id  = (known after apply)
      + status      = (known after apply)

      + egress {
          + description       = "All outbound traffic"
          + from_port         = 0
          + id                = (known after apply)
          + labels            = (known after apply)
          + port              = -1
          + protocol          = "ANY"
          + to_port           = 65535
          + v4_cidr_blocks    = [
              + "0.0.0.0/0",
            ]
          + v6_cidr_blocks    = []
            # (2 unchanged attributes hidden)
        }

      + ingress {
          + description       = "Application port"
          + from_port         = -1
          + id                = (known after apply)
          + labels            = (known after apply)
          + port              = 5000
          + protocol          = "TCP"
          + to_port           = -1
          + v4_cidr_blocks    = [
              + "0.0.0.0/0",
            ]
          + v6_cidr_blocks    = []
            # (2 unchanged attributes hidden)
        }
      + ingress {
          + description       = "HTTP access"
          + from_port         = -1
          + id                = (known after apply)
          + labels            = (known after apply)
          + port              = 80
          + protocol          = "TCP"
          + to_port           = -1
          + v4_cidr_blocks    = [
              + "0.0.0.0/0",
            ]
          + v6_cidr_blocks    = []
            # (2 unchanged attributes hidden)
        }
      + ingress {
          + description       = "SSH access"
          + from_port         = -1
          + id                = (known after apply)
          + labels            = (known after apply)
          + port              = 22
          + protocol          = "TCP"
          + to_port           = -1
          + v4_cidr_blocks    = [
              + "213.87.71.131/32",
            ]
          + v6_cidr_blocks    = []
            # (2 unchanged attributes hidden)
        }
    }

  # yandex_vpc_subnet.subnet will be created
  + resource "yandex_vpc_subnet" "subnet" {
      + created_at     = (known after apply)
      + description    = "Subnet for iu-devops VM"
      + folder_id      = (known after apply)
      + id             = (known after apply)
      + labels         = (known after apply)
      + name           = "iu-devops-subnet"
      + network_id     = (known after apply)
      + v4_cidr_blocks = [
          + "192.168.1.0/24",
        ]
      + v6_cidr_blocks = (known after apply)
      + zone           = "ru-central1-b"
    }

Plan: 4 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + app_access_url         = (known after apply)
  + http_access_url        = (known after apply)
  + network_name           = "iu-devops-network"
  + security_group_name    = "iu-devops-security-group"
  + ssh_connection_command = (known after apply)
  + vm_id                  = (known after apply)
  + vm_private_ip          = (known after apply)
  + vm_public_ip           = (known after apply)
```

## terraform apply

```bash
$terraform apply
data.yandex_compute_image.ubuntu: Reading...
data.yandex_compute_image.ubuntu: Read complete after 0s [id=fd84es6pnho7mpbjerv1]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # yandex_compute_instance.vm will be created
  + resource "yandex_compute_instance" "vm" {
      + created_at                = (known after apply)
      + description               = "VM instance for iu-devops"
      + folder_id                 = (known after apply)
      + fqdn                      = (known after apply)
      + gpu_cluster_id            = (known after apply)
      + hardware_generation       = (known after apply)
      + hostname                  = "iu-devops-vm"
      + id                        = (known after apply)
      + labels                    = {
          + "environment" = "development"
          + "managed_by"  = "terraform"
          + "project"     = "iu-devops"
        }
      + maintenance_grace_period  = (known after apply)
      + maintenance_policy        = (known after apply)
      + metadata                  = {
          + "ssh-keys" = <<-EOT
            EOT
        }
      + name                      = "iu-devops-vm"
      + network_acceleration_type = "standard"
      + platform_id               = "standard-v2"
      + status                    = (known after apply)
      + zone                      = "ru-central1-b"

      + boot_disk {
          + auto_delete = true
          + device_name = (known after apply)
          + disk_id     = (known after apply)
          + mode        = (known after apply)

          + initialize_params {
              + block_size  = (known after apply)
              + description = (known after apply)
              + image_id    = "fd84es6pnho7mpbjerv1"
              + name        = (known after apply)
              + size        = 10
              + snapshot_id = (known after apply)
              + type        = "network-hdd"
            }
        }

      + metadata_options (known after apply)

      + network_interface {
          + index              = (known after apply)
          + ip_address         = (known after apply)
          + ipv4               = true
          + ipv6               = (known after apply)
          + ipv6_address       = (known after apply)
          + mac_address        = (known after apply)
          + nat                = true
          + nat_ip_address     = (known after apply)
          + nat_ip_version     = (known after apply)
          + security_group_ids = (known after apply)
          + subnet_id          = (known after apply)
        }

      + placement_policy (known after apply)

      + resources {
          + core_fraction = 20
          + cores         = 2
          + memory        = 1
        }

      + scheduling_policy (known after apply)
    }

  # yandex_vpc_network.network will be created
  + resource "yandex_vpc_network" "network" {
      + created_at                = (known after apply)
      + default_security_group_id = (known after apply)
      + description               = "Network for iu-devops VM"
      + folder_id                 = (known after apply)
      + id                        = (known after apply)
      + labels                    = (known after apply)
      + name                      = "iu-devops-network"
      + subnet_ids                = (known after apply)
    }

  # yandex_vpc_security_group.security_group will be created
  + resource "yandex_vpc_security_group" "security_group" {
      + created_at  = (known after apply)
      + description = "Security group for iu-devops VM"
      + folder_id   = (known after apply)
      + id          = (known after apply)
      + labels      = (known after apply)
      + name        = "iu-devops-security-group"
      + network_id  = (known after apply)
      + status      = (known after apply)

      + egress {
          + description       = "All outbound traffic"
          + from_port         = 0
          + id                = (known after apply)
          + labels            = (known after apply)
          + port              = -1
          + protocol          = "ANY"
          + to_port           = 65535
          + v4_cidr_blocks    = [
              + "0.0.0.0/0",
            ]
          + v6_cidr_blocks    = []
            # (2 unchanged attributes hidden)
        }

      + ingress {
          + description       = "Application port"
          + from_port         = -1
          + id                = (known after apply)
          + labels            = (known after apply)
          + port              = 5000
          + protocol          = "TCP"
          + to_port           = -1
          + v4_cidr_blocks    = [
              + "0.0.0.0/0",
            ]
          + v6_cidr_blocks    = []
            # (2 unchanged attributes hidden)
        }
      + ingress {
          + description       = "HTTP access"
          + from_port         = -1
          + id                = (known after apply)
          + labels            = (known after apply)
          + port              = 80
          + protocol          = "TCP"
          + to_port           = -1
          + v4_cidr_blocks    = [
              + "0.0.0.0/0",
            ]
          + v6_cidr_blocks    = []
            # (2 unchanged attributes hidden)
        }
      + ingress {
          + description       = "SSH access"
          + from_port         = -1
          + id                = (known after apply)
          + labels            = (known after apply)
          + port              = 22
          + protocol          = "TCP"
          + to_port           = -1
          + v4_cidr_blocks    = [
              + "213.87.71.131/32",
            ]
          + v6_cidr_blocks    = []
            # (2 unchanged attributes hidden)
        }
    }

  # yandex_vpc_subnet.subnet will be created
  + resource "yandex_vpc_subnet" "subnet" {
      + created_at     = (known after apply)
      + description    = "Subnet for iu-devops VM"
      + folder_id      = (known after apply)
      + id             = (known after apply)
      + labels         = (known after apply)
      + name           = "iu-devops-subnet"
      + network_id     = (known after apply)
      + v4_cidr_blocks = [
          + "192.168.1.0/24",
        ]
      + v6_cidr_blocks = (known after apply)
      + zone           = "ru-central1-b"
    }

Plan: 4 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + app_access_url         = (known after apply)
  + http_access_url        = (known after apply)
  + network_name           = "iu-devops-network"
  + security_group_name    = "iu-devops-security-group"
  + ssh_connection_command = (known after apply)
  + vm_id                  = (known after apply)
  + vm_private_ip          = (known after apply)
  + vm_public_ip           = (known after apply)

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

yandex_vpc_network.network: Creating...
yandex_vpc_network.network: Creation complete after 3s [id=enpudej5rmfcmmjkbu16]
yandex_vpc_subnet.subnet: Creating...
yandex_vpc_security_group.security_group: Creating...
yandex_vpc_subnet.subnet: Creation complete after 0s [id=e2lqupn6hcc9la5h3shj]
yandex_vpc_security_group.security_group: Creation complete after 2s [id=enp88s1i4uke3ucero94]
yandex_compute_instance.vm: Creating...
yandex_compute_instance.vm: Creation complete after 1m9s [id=epdvpo2mmh6fvbolq8bs]

Apply complete! Resources: 4 added, 0 changed, 0 destroyed.

Outputs:
...
```

## SSH connection

```bash
$ssh ubuntu@178.154.192.135

Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-216-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Sat Feb 21 15:26:18 UTC 2026

  System load:  0.0               Processes:             108
  Usage of /:   17.7% of 9.04GB   Users logged in:       0
  Memory usage: 18%               IPv4 address for eth0: 192.168.1.9
  Swap usage:   0%


Expanded Security Maintenance for Infrastructure is not enabled.

0 updates can be applied immediately.

72 additional security updates can be applied with ESM Infra.
Learn more about enabling ESM Infra service for Ubuntu 20.04 at
https://ubuntu.com/20-04


The list of available updates is more than a week old.
To check for new updates run: sudo apt update


The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

ubuntu@iu-devops-vm:~$ 
```

## terraform destroy

```bash
$terraform destroy
data.yandex_compute_image.ubuntu: Reading...
yandex_vpc_network.network: Refreshing state... [id=enpudej5rmfcmmjkbu16]
data.yandex_compute_image.ubuntu: Read complete after 0s [id=fd84es6pnho7mpbjerv1]
yandex_vpc_subnet.subnet: Refreshing state... [id=e2lqupn6hcc9la5h3shj]
yandex_vpc_security_group.security_group: Refreshing state... [id=enp88s1i4uke3ucero94]
yandex_compute_instance.vm: Refreshing state... [id=epdvpo2mmh6fvbolq8bs]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # yandex_compute_instance.vm will be destroyed
  - resource "yandex_compute_instance" "vm" {
      - created_at                = "2026-02-21T15:21:01Z" -> null
      - description               = "VM instance for iu-devops" -> null
      - folder_id                 = "b1gmplm05pv14i0ag0lh" -> null
      - fqdn                      = "iu-devops-vm.ru-central1.internal" -> null
      - hardware_generation       = [
          - {
              - generation2_features = []
              - legacy_features      = [
                  - {
                      - pci_topology = "PCI_TOPOLOGY_V2"
                    },
                ]
            },
        ] -> null
      - hostname                  = "iu-devops-vm" -> null
      - id                        = "epdvpo2mmh6fvbolq8bs" -> null
      - labels                    = {
          - "environment" = "development"
          - "managed_by"  = "terraform"
          - "project"     = "iu-devops"
        } -> null
      - metadata                  = {
          - "ssh-keys" = <<-EOT
            EOT
        } -> null
      - name                      = "iu-devops-vm" -> null
      - network_acceleration_type = "standard" -> null
      - platform_id               = "standard-v2" -> null
      - status                    = "running" -> null
      - zone                      = "ru-central1-b" -> null
        # (3 unchanged attributes hidden)

      - boot_disk {
          - auto_delete = true -> null
          - device_name = "epde8vmn38lpjvdh6qub" -> null
          - disk_id     = "epde8vmn38lpjvdh6qub" -> null
          - mode        = "READ_WRITE" -> null

          - initialize_params {
              - block_size  = 4096 -> null
              - image_id    = "fd84es6pnho7mpbjerv1" -> null
                name        = null
              - size        = 10 -> null
              - type        = "network-hdd" -> null
                # (3 unchanged attributes hidden)
            }
        }

      - metadata_options {
          - aws_v1_http_endpoint = 1 -> null
          - aws_v1_http_token    = 2 -> null
          - gce_http_endpoint    = 1 -> null
          - gce_http_token       = 1 -> null
        }

      - network_interface {
          - index              = 0 -> null
          - ip_address         = "192.168.1.9" -> null
          - ipv4               = true -> null
          - ipv6               = false -> null
          - mac_address        = "d0:0d:1f:ce:05:6b" -> null
          - nat                = true -> null
          - nat_ip_address     = "178.154.192.135" -> null
          - nat_ip_version     = "IPV4" -> null
          - security_group_ids = [
              - "enp88s1i4uke3ucero94",
            ] -> null
          - subnet_id          = "e2lqupn6hcc9la5h3shj" -> null
            # (1 unchanged attribute hidden)
        }

      - placement_policy {
          - host_affinity_rules       = [] -> null
          - placement_group_partition = 0 -> null
            # (1 unchanged attribute hidden)
        }

      - resources {
          - core_fraction = 20 -> null
          - cores         = 2 -> null
          - gpus          = 0 -> null
          - memory        = 1 -> null
        }

      - scheduling_policy {
          - preemptible = false -> null
        }
    }

  # yandex_vpc_network.network will be destroyed
  - resource "yandex_vpc_network" "network" {
      - created_at                = "2026-02-21T15:20:57Z" -> null
      - default_security_group_id = "enp4c2nd3066pmiqogv3" -> null
      - description               = "Network for iu-devops VM" -> null
      - folder_id                 = "b1gmplm05pv14i0ag0lh" -> null
      - id                        = "enpudej5rmfcmmjkbu16" -> null
      - labels                    = {} -> null
      - name                      = "iu-devops-network" -> null
      - subnet_ids                = [
          - "e2lqupn6hcc9la5h3shj",
        ] -> null
    }

  # yandex_vpc_security_group.security_group will be destroyed
  - resource "yandex_vpc_security_group" "security_group" {
      - created_at  = "2026-02-21T15:21:00Z" -> null
      - description = "Security group for iu-devops VM" -> null
      - folder_id   = "b1gmplm05pv14i0ag0lh" -> null
      - id          = "enp88s1i4uke3ucero94" -> null
      - labels      = {} -> null
      - name        = "iu-devops-security-group" -> null
      - network_id  = "enpudej5rmfcmmjkbu16" -> null
      - status      = "ACTIVE" -> null

      - egress {
          - description       = "All outbound traffic" -> null
          - from_port         = 0 -> null
          - id                = "enpio0kotk464cn6g9c6" -> null
          - labels            = {} -> null
          - port              = -1 -> null
          - protocol          = "ANY" -> null
          - to_port           = 65535 -> null
          - v4_cidr_blocks    = [
              - "0.0.0.0/0",
            ] -> null
          - v6_cidr_blocks    = [] -> null
            # (2 unchanged attributes hidden)
        }

      - ingress {
          - description       = "Application port" -> null
          - from_port         = -1 -> null
          - id                = "enp8atmaspoj4d165b6e" -> null
          - labels            = {} -> null
          - port              = 5000 -> null
          - protocol          = "TCP" -> null
          - to_port           = -1 -> null
          - v4_cidr_blocks    = [
              - "0.0.0.0/0",
            ] -> null
          - v6_cidr_blocks    = [] -> null
            # (2 unchanged attributes hidden)
        }
      - ingress {
          - description       = "HTTP access" -> null
          - from_port         = -1 -> null
          - id                = "enpi9r84k94s7k64ued2" -> null
          - labels            = {} -> null
          - port              = 80 -> null
          - protocol          = "TCP" -> null
          - to_port           = -1 -> null
          - v4_cidr_blocks    = [
              - "0.0.0.0/0",
            ] -> null
          - v6_cidr_blocks    = [] -> null
            # (2 unchanged attributes hidden)
        }
      - ingress {
          - description       = "SSH access" -> null
          - from_port         = -1 -> null
          - id                = "enp5gue4suer8pj50pbh" -> null
          - labels            = {} -> null
          - port              = 22 -> null
          - protocol          = "TCP" -> null
          - to_port           = -1 -> null
          - v4_cidr_blocks    = [
              - "213.87.71.131/32",
            ] -> null
          - v6_cidr_blocks    = [] -> null
            # (2 unchanged attributes hidden)
        }
    }

  # yandex_vpc_subnet.subnet will be destroyed
  - resource "yandex_vpc_subnet" "subnet" {
      - created_at     = "2026-02-21T15:20:59Z" -> null
      - description    = "Subnet for iu-devops VM" -> null
      - folder_id      = "b1gmplm05pv14i0ag0lh" -> null
      - id             = "e2lqupn6hcc9la5h3shj" -> null
      - labels         = {} -> null
      - name           = "iu-devops-subnet" -> null
      - network_id     = "enpudej5rmfcmmjkbu16" -> null
      - v4_cidr_blocks = [
          - "192.168.1.0/24",
        ] -> null
      - v6_cidr_blocks = [] -> null
      - zone           = "ru-central1-b" -> null
        # (1 unchanged attribute hidden)
    }

Plan: 0 to add, 0 to change, 4 to destroy.

Changes to Outputs:
  - app_access_url         = "http://178.154.192.135:5000" -> null
  - http_access_url        = "http://178.154.192.135" -> null
  - network_name           = "iu-devops-network" -> null
  - security_group_name    = "iu-devops-security-group" -> null
  - ssh_connection_command = "ssh ubuntu@178.154.192.135" -> null
  - vm_id                  = "epdvpo2mmh6fvbolq8bs" -> null
  - vm_private_ip          = "192.168.1.9" -> null
  - vm_public_ip           = "178.154.192.135" -> null

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

yandex_compute_instance.vm: Destroying... [id=epdvpo2mmh6fvbolq8bs]
yandex_compute_instance.vm: Still destroying... [id=epdvpo2mmh6fvbolq8bs, 10s elapsed]
yandex_compute_instance.vm: Still destroying... [id=epdvpo2mmh6fvbolq8bs, 20s elapsed]
yandex_vpc_subnet.subnet: Destroying... [id=e2lqupn6hcc9la5h3shj]
yandex_vpc_security_group.security_group: Destroying... [id=enp88s1i4uke3ucero94]
yandex_vpc_security_group.security_group: Destruction complete after 0s
yandex_vpc_subnet.subnet: Destruction complete after 4s
yandex_vpc_network.network: Destroying... [id=enpudej5rmfcmmjkbu16]
yandex_vpc_network.network: Destruction complete after 1s

Destroy complete! Resources: 4 destroyed.
```

## pulumi preview

```bash
$pulumi preview
Previewing update (dev)

View in Browser (Ctrl+O): https://app.pulumi.com/KonstantinPetrovichQWERTY-org/iu-devops-vm/dev/previews/7556195f-37e3-468d-85ea-53394e76d3ba

     Type                              Name               Plan
 +   pulumi:pulumi:Stack               iu-devops-vm-dev   create
 +   ├─ yandex:index:VpcNetwork        iu-devops-network  create
 +   ├─ yandex:index:VpcSubnet         iu-devops-subnet   create
 +   ├─ yandex:index:VpcSecurityGroup  iu-devops-sg       create
 +   └─ yandex:index:ComputeInstance   iu-devops-vm       create
Outputs:
    app_access_url        : [unknown]
    http_access_url       : [unknown]
    network_used          : "iu-devops-network"
    security_group_id     : [unknown]
    ssh_connection_command: [unknown]
    subnet_used           : "iu-devops-subnet"
    vm_id                 : [unknown]
    vm_private_ip         : [unknown]
    vm_public_ip          : [unknown]

Resources:
    + 5 to create
```


## pulumi up

```bash
$pulumi up
Previewing update (dev)

View in Browser (Ctrl+O): https://app.pulumi.com/KonstantinPetrovichQWERTY-org/iu-devops-vm/dev/previews/ed5953dd-6738-4646-abbe-c0129ddb88cc

     Type                             Name              Plan
     pulumi:pulumi:Stack              iu-devops-vm-dev
 +   └─ yandex:index:ComputeInstance  iu-devops-vm      create
Outputs:
  + app_access_url        : [unknown]
  + http_access_url       : [unknown]
  + network_used          : "iu-devops-network"
  + security_group_id     : "enpm24bb7u8i7g836qvi"
  + ssh_connection_command: [unknown]
  + subnet_used           : "iu-devops-subnet"
  + vm_id                 : [unknown]
  + vm_private_ip         : [unknown]
  + vm_public_ip          : [unknown]

Resources:
    + 1 to create
    4 unchanged

Do you want to perform this update? yes
Updating (dev)

View in Browser (Ctrl+O): https://app.pulumi.com/KonstantinPetrovichQWERTY-org/iu-devops-vm/dev/updates/4

     Type                             Name              Status
     pulumi:pulumi:Stack              iu-devops-vm-dev
 +   └─ yandex:index:ComputeInstance  iu-devops-vm      created (43s)
Outputs:
  + app_access_url        : "http://89.169.166.147:5000"
  + http_access_url       : "http://89.169.166.147"
  + network_used          : "iu-devops-network"
  + security_group_id     : "enpm24bb7u8i7g836qvi"
  + ssh_connection_command: "ssh ubuntu@89.169.166.147"
  + subnet_used           : "iu-devops-subnet"
  + vm_id                 : "epdl9jvvdsaelsv6sft7"
  + vm_private_ip         : "192.168.1.33"
  + vm_public_ip          : "89.169.166.147"

Resources:
    + 1 created
    4 unchanged

Duration: 46s
```

## VM

```bash 
$ssh ubuntu@89.169.166.147
The authenticity of host '89.169.166.147 (89.169.166.147)' can't be established.
ED25519 key fingerprint is SHA256:APtlZmZSedKHWlqsblEHKNWEVcqrc8vpG8c/m1lx978.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '89.169.166.147' (ED25519) to the list of known hosts.
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-216-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Sat Feb 21 18:11:50 UTC 2026

  System load:  0.33              Processes:             111
  Usage of /:   17.7% of 9.04GB   Users logged in:       0
  Memory usage: 19%               IPv4 address for eth0: 192.168.1.33
  Swap usage:   0%


Expanded Security Maintenance for Infrastructure is not enabled.

0 updates can be applied immediately.

72 additional security updates can be applied with ESM Infra.
Learn more about enabling ESM Infra service for Ubuntu 20.04 at
https://ubuntu.com/20-04


The list of available updates is more than a week old.
To check for new updates run: sudo apt update


The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

ubuntu@iu-devops-vm:~$ exit
logout
Connection to 89.169.166.147 closed.
```

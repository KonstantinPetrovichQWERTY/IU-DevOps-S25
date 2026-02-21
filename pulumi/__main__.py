"""Pulumi program to create VM infrastructure on Yandex Cloud"""

import pulumi
import pulumi_yandex as yandex
import os

config = pulumi.Config()
cloud_id = config.require("cloud_id")
folder_id = config.require("folder_id")
zone = config.get("zone")
project_name = config.get("project_name")
environment = config.get("environment")
your_ip = config.require("your_ip")
ssh_public_key_path = config.get("ssh_public_key_path")

ssh_public_key_path = os.path.expanduser(ssh_public_key_path)
try:
    with open(ssh_public_key_path, "r") as f:
        ssh_public_key = f.read().strip()
except FileNotFoundError:
    raise Exception(f"SSH public key not found at {ssh_public_key_path}")

network = yandex.VpcNetwork(
    f"{project_name}-network",
    name=f"{project_name}-network",
    folder_id=folder_id,
    description=f"Network for {project_name} VM",
    labels={
        "environment": environment,
        "managed_by": "pulumi",
    },
)

subnet = yandex.VpcSubnet(
    f"{project_name}-subnet",
    name=f"{project_name}-subnet",
    folder_id=folder_id,
    description=f"Subnet for {project_name} VM",
    zone=zone,
    network_id=network.id,
    v4_cidr_blocks=["192.168.1.0/24"],
    labels={
        "environment": environment,
        "managed_by": "pulumi",
    },
)


security_group = yandex.VpcSecurityGroup(
    f"{project_name}-sg",
    name=f"{project_name}-sg",
    folder_id=folder_id,
    description=f"Security group for {project_name} VM",
    network_id=network.id,
    labels={
        "environment": environment,
        "managed_by": "pulumi",
    },
    ingresses=[
        # SSH from your IP
        {
            "description": "SSH access",
            "protocol": "TCP",
            "port": 22,
            "v4_cidr_blocks": [f"{your_ip}/32"],
        },
        # HTTP from anywhere
        {
            "description": "HTTP access",
            "protocol": "TCP",
            "port": 80,
            "v4_cidr_blocks": ["0.0.0.0/0"],
        },
        # Port 5000 from anywhere
        {
            "description": "Application port",
            "protocol": "TCP",
            "port": 5000,
            "v4_cidr_blocks": ["0.0.0.0/0"],
        },
    ],
    egresses=[
        # All outbound traffic
        {
            "description": "All outbound traffic",
            "protocol": "ANY",
            "from_port": 0,
            "to_port": 65535,
            "v4_cidr_blocks": ["0.0.0.0/0"],
        },
    ],
)

# Get the latest Ubuntu 20.04 image
ubuntu_image = yandex.get_compute_image(family="ubuntu-2004-lts")

# Create VM instance
vm_instance = yandex.ComputeInstance(
    f"{project_name}-vm",
    name=f"{project_name}-vm",
    folder_id=folder_id,
    description=f"VM instance for {project_name}",
    zone=zone,
    hostname=f"{project_name}-vm",
    platform_id="standard-v2",
    labels={
        "environment": environment,
        "managed_by": "pulumi",
    },
    resources=yandex.ComputeInstanceResourcesArgs(
        cores=2,
        memory=1,
        core_fraction=20,
    ),
    boot_disk=yandex.ComputeInstanceBootDiskArgs(
        initialize_params=yandex.ComputeInstanceBootDiskInitializeParamsArgs(
            image_id=ubuntu_image.id,
            size=10,
            type="network-hdd",
        ),
    ),
    network_interfaces=[
        yandex.ComputeInstanceNetworkInterfaceArgs(
            subnet_id=subnet.id,
            security_group_ids=[security_group.id],
            nat=True,  # Assign public IP
        )
    ],
    metadata={
        "ssh-keys": f"ubuntu:{ssh_public_key}",
    },
)

# Export important values
pulumi.export("vm_public_ip", vm_instance.network_interfaces[0].nat_ip_address)
pulumi.export("vm_private_ip", vm_instance.network_interfaces[0].ip_address)
pulumi.export(
    "ssh_connection_command",
    pulumi.Output.concat(
        "ssh ubuntu@", vm_instance.network_interfaces[0].nat_ip_address
    ),
)
pulumi.export(
    "http_access_url",
    pulumi.Output.concat("http://", vm_instance.network_interfaces[0].nat_ip_address),
)
pulumi.export(
    "app_access_url",
    pulumi.Output.concat(
        "http://", vm_instance.network_interfaces[0].nat_ip_address, ":5000"
    ),
)
pulumi.export("security_group_id", security_group.id)
pulumi.export("vm_id", vm_instance.id)
pulumi.export("network_used", network.name)
pulumi.export("subnet_used", subnet.name)

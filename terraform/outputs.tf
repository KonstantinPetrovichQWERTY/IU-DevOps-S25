output "vm_public_ip" {
  description = "Public IP address of the VM"
  value       = yandex_compute_instance.vm.network_interface.0.nat_ip_address
}

output "vm_private_ip" {
  description = "Private IP address of the VM"
  value       = yandex_compute_instance.vm.network_interface.0.ip_address
}

output "ssh_connection_command" {
  description = "SSH command to connect to the VM"
  value       = "ssh ubuntu@${yandex_compute_instance.vm.network_interface.0.nat_ip_address}"
}

output "http_access_url" {
  description = "URL to access HTTP service"
  value       = "http://${yandex_compute_instance.vm.network_interface.0.nat_ip_address}"
}

output "app_access_url" {
  description = "URL to access application on port 5000"
  value       = "http://${yandex_compute_instance.vm.network_interface.0.nat_ip_address}:8000"
}

output "network_name" {
  description = "Name of the created VPC network"
  value       = yandex_vpc_network.network.name
}

output "security_group_name" {
  description = "Name of the security group"
  value       = yandex_vpc_security_group.security_group.name
}

output "vm_id" {
  description = "VM instance ID"
  value       = yandex_compute_instance.vm.id
}
output "instance_hostname" {
  description = "Private DNS name of the EC2 instance."
  value       = aws_instance.app_server[*].private_dns
}

output "public_ip" {
  description = "public ip  of the EC2 instance."
  value       = aws_instance.app_server[*].public_ip
}


output "keypair_public_path" {
  description = "public file path of the ec2 instance  name of the EC2 instance."
value       = aws_key_pair.my-key.public_key
}



provider "aws" {
  region = "ap-southeast-2"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  owners = ["099720109477"] # canonical ubuntu
}


locals {
instance_names = ["master", "worker-1", "worker-2"]
}

resource "aws_instance" "app_server" {
count =3
  ami           = data.aws_ami.ubuntu.id
 #  instance_type = "t2.micro" 
 instance_type = var.instance_type
 key_name = aws_key_pair.my-key.key_name
vpc_security_group_ids = [aws_security_group.ssh_access.id]

  tags = {
    Name = local.instance_names[count.index]
  }
}

resource "aws_key_pair" "my-key" {
key_name = "myterrakey"
 public_key = file ("/home/ubuntu/.ssh/id_rsa.pub")
}


resource "aws_security_group" "ssh_access" {
name = "allow_ssh"

ingress {
from_port = 22
to_port =22
protocol = "tcp"
cidr_blocks = ["0.0.0.0/0"]
}


egress{
from_port = 0
to_port = 0
protocol = "-1"
cidr_blocks = ["0.0.0.0/0"]
}
}



resource  "aws_s3_bucket" "s3_for_terraform" {
bucket = "my-terraform-bucket-shyam-13"

tags = {
name= "My-bucket"
Environment = "Dev"
}
}


resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.s3_for_terraform.id

  versioning_configuration {
    status = "Enabled"
  }
}

############################################
# Block Public Access (Security)
############################################
resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket = aws_s3_bucket.s3_for_terraform.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}





resource "aws_dynamodb_table" "tf_lock" {
name = "terraform-lock-table"
billing_mode = "PAY_PER_REQUEST"
hash_key = "LockID"

attribute { 
name = "LockID"
type = "S"
}
}

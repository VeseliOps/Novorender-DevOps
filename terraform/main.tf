########### S3 Bucket ############
resource "aws_s3_bucket" "mybucket" {
  bucket = "${var.bucket_name}"
  acl    = "private"

  versioning {
    enabled = true
  }

  tags = {
    Name = "aleksa bucket"
  }
}

############ EC2 and VPC ##############
resource "aws_instance" "aleksaws" {
  ami             = "${var.ami}"
  instance_type   = "${var.type}"
  security_groups = [aws_security_group.tf_security_group.name]
  #count           = 1
  key_name        = "tf_key"
  tags = {
    Name = "aleksa-aws"
  }

  depends_on = [aws_key_pair.tf_key]
}

resource "aws_vpc" "my_vpc" {
  cidr_block = "172.31.0.0/16"

  tags = {
    Name = "tf-vpc"
  }
}

resource "aws_security_group" "tf_security_group" {
  name        = "security group using Terraform"
  description = "security group using Terraform"
  vpc_id      = "${var.vpcid}"

  ingress {
    description      = "HTTPS"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    description      = "HTTP"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    description      = "SSH"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "tf_security_group"
  }
}

resource "aws_key_pair" "tf_key" {
  key_name   = "tf_key"
  public_key = tls_private_key.rsa.public_key_openssh
}

resource "tls_private_key" "rsa" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "tf-key" {
  content  = tls_private_key.rsa.private_key_pem
  filename = "tfkey"
}

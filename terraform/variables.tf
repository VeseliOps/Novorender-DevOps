variable "bucket_name" {
  type    = string
  default = "aleksas3"
}

variable "ami" {
  type    = string
  default = "ami-0989fb15ce71ba39e"
}

variable "type" {
  type    = string
  default = "t3.micro"
}

variable "cidrblock" {
  type    = string
  default = "172.31.0.0/16"
}

variable "vpcid" {
  type    = string
  default = "vpc-0ac504c47dc557b67"
}


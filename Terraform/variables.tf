variable "aws_region" {
  description = "AWS Region"
  type        = string
}

variable "project_name" {
  description = "Project Name"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR"
  type        = string
}

variable "public_subnet_1" {
  description = "Public Subnet 1"
  type        = string
}

variable "public_subnet_2" {
  description = "Public Subnet 2"
  type        = string
}

variable "private_subnet_1" {
  description = "Private Subnet 1"
  type        = string
}

variable "private_subnet_2" {
  description = "Private Subnet 2"
  type        = string
}

variable "instance_type" {
  description = "EC2 Instance Type"
  type        = string
}

variable "key_name" {
  description = "EC2 Key Pair Name"
  type        = string
}

variable "db_username" {
  description = "RDS Username"
  type        = string
}

variable "db_password" {
  description = "RDS Password"
  type        = string
  sensitive   = true
}
####################################
# Public Subnet 1
####################################

resource "aws_subnet" "public_1" {

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_1
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-1"
  }
}

####################################
# Public Subnet 2
####################################

resource "aws_subnet" "public_2" {

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_2
  availability_zone       = "ap-south-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-2"
  }
}

####################################
# Private Subnet 1
####################################

resource "aws_subnet" "private_1" {

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_1
  availability_zone = "ap-south-1a"

  tags = {
    Name = "${var.project_name}-private-1"
  }
}

####################################
# Private Subnet 2
####################################

resource "aws_subnet" "private_2" {

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_2
  availability_zone = "ap-south-1b"

  tags = {
    Name = "${var.project_name}-private-2"
  }
}
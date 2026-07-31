####################################
# Elastic IP
####################################

resource "aws_eip" "nat_eip" {

  domain = "vpc"

  tags = {
    Name = "${var.project_name}-eip"
  }
}

####################################
# NAT Gateway
####################################

resource "aws_nat_gateway" "nat" {

  allocation_id = aws_eip.nat_eip.id

  subnet_id = aws_subnet.public_1.id

  depends_on = [
    aws_internet_gateway.igw
  ]

  tags = {
    Name = "${var.project_name}-nat"
  }
}
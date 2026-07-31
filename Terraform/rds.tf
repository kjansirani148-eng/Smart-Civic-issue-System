resource "aws_db_subnet_group" "db_subnet" {
  name = "${var.project_name}-db-subnet"

  subnet_ids = [
    aws_subnet.private_1.id,
    aws_subnet.private_2.id
  ]

  tags = {
    Name = "${var.project_name}-db-subnet"
  }
}

resource "aws_db_instance" "mysql" {

  identifier = "${var.project_name}-db"

  allocated_storage = 20

  engine = "mysql"

  engine_version = "8.0"

  instance_class = "db.t3.micro"

  db_name = "smartcivic"

  username = var.db_username

  password = var.db_password

  skip_final_snapshot = true

  publicly_accessible = false

  db_subnet_group_name = aws_db_subnet_group.db_subnet.name

  vpc_security_group_ids = [
    aws_security_group.rds_sg.id
  ]

  tags = {
    Name = "${var.project_name}-mysql"
  }
}
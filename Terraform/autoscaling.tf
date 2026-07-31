resource "aws_launch_template" "lt" {

  name_prefix = "${var.project_name}-lt"

  image_id = aws_instance.web.ami

  instance_type = var.instance_type

  key_name = var.key_name

  vpc_security_group_ids = [
    aws_security_group.ec2_sg.id
  ]
}

resource "aws_autoscaling_group" "asg" {

  desired_capacity = 1

  max_size = 2

  min_size = 1

  vpc_zone_identifier = [
    aws_subnet.public_1.id,
    aws_subnet.public_2.id
  ]

  launch_template {
    id = aws_launch_template.lt.id

    version = "$Latest"
  }
}
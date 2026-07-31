output "vpc_id" {
  value = aws_vpc.main.id
}

output "ec2_public_ip" {
  value = aws_instance.web.public_ip
}

output "s3_bucket_name" {
  value = aws_s3_bucket.bucket.bucket
}

output "rds_endpoint" {
  value = aws_db_instance.mysql.endpoint
}

output "alb_dns_name" {
  value = aws_lb.alb.dns_name
}
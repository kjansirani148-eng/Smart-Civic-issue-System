resource "aws_s3_bucket" "bucket" {

  bucket = "smart-civic-uploads-jansi"

  tags = {
    Name = "${var.project_name}-bucket"
  }
}
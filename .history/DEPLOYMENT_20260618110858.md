# AWS Deployment Guide

This guide describes how to deploy the Smart Civic Issue Reporting Platform to AWS using EC2, RDS, and S3.

## 1. AWS Resources

- EC2 instance: Ubuntu 24.04
- RDS MySQL database
- S3 bucket for complaint images
- IAM role or IAM user with S3 access

## 2. Setup S3 Bucket

1. Create an S3 bucket with a unique name.
2. Configure public access settings if images need public read.
3. Create an IAM policy granting `s3:PutObject`, `s3:GetObject`, `s3:ListBucket`.
4. Attach the policy to the EC2 instance role or an IAM user.

## 3. Setup RDS MySQL

1. Create an RDS MySQL instance.
2. Create a database named `smart_civic`.
3. Allow EC2 security group access on port `3306`.
4. Update `DATABASE_URL` in `.env`.

## 4. EC2 Ubuntu 24.04 Configuration

Connect to your instance and run:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv mysql-client git
```

Clone the project:

```bash
git clone <your-repo-url> smart-civic
cd smart-civic
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 5. Environment Variables

Populate `.env` with:

```dotenv
SECRET_KEY=YOUR_SECRET_KEY
DATABASE_URL=mysql+pymysql://<user>:<password>@<rds-endpoint>:3306/smart_civic
AWS_S3_BUCKET=your-s3-bucket
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

## 6. Database Initialization

```bash
mysql -h <rds-endpoint> -u <user> -p < schema.sql
mysql -h <rds-endpoint> -u <user> -p smart_civic < sample_data.sql
```

## 7. Running the Application

```bash
python run.py
```

For production, use a WSGI server like Gunicorn and a reverse proxy such as Nginx.

## 8. CloudWatch Monitoring

- Install CloudWatch Agent on EC2
- Monitor system metrics and application logs
- Configure custom dashboard for CPU, memory, disk, and request logs

## 9. Security Notes

- Use HTTPS for public traffic with an SSL certificate.
- Do not commit AWS credentials.
- Use IAM roles for EC2 when possible.

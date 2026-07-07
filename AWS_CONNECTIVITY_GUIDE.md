# AWS Services Integration & Connectivity Guide
### Step-by-Step Guide for Connecting S3, IAM, and EC2

This guide explains how to connect the **Smart Civic** application to Amazon Web Services (AWS). It details the required AWS services, how to configure them in the AWS Management Console, and how to link them to the project code.

---

## 1. Required AWS Services

To make this application production-ready, we utilize three key AWS services:

1. **Amazon S3 (Simple Storage Service)**: A secure cloud object storage service used to store civic complaint images and resolution photos uploaded by users.
2. **AWS IAM (Identity and Access Management)**: Used to create secure programmatic credentials (API access keys) with permission policies restricted only to the S3 upload folder.
3. **Amazon EC2 (Elastic Compute Cloud)**: A virtual server (Ubuntu VM) in the cloud that hosts our running Flask web application.

---

## 2. Step-by-Step Setup Instructions

### Step 1: Setting up the Amazon S3 Bucket
By default, the application is configured to upload images to S3. Since users need to view the reported issues, the images must be publicly accessible.

1. Log into your **AWS Management Console**.
2. Search for and open **S3**.
3. Click **Create bucket**.
4. Configure the bucket details:
   * **Bucket name**: Enter a globally unique name (e.g., `smart-civic-uploads-yourname`).
   * **AWS Region**: Select your preferred region (e.g., `us-east-1`).
5. Under **Object Ownership**, select **ACLs enabled** and ensure **Bucket owner preferred** is checked. *(Required because the code uploads objects with `public-read` access control rules).*
6. Under **Block Public Access settings for this bucket**:
   * **Uncheck** "Block *all* public access".
   * Check the acknowledgement box stating that you want to make objects public.
7. Click **Create bucket** at the bottom of the page.

---

### Step 2: Creating an IAM Policy and User Credentials
To allow the Flask application to write images into S3 securely, we must create a programmatic user through AWS IAM.

#### Part A: Create a Permission Policy
1. Open the **IAM** Console.
2. Click on **Policies** in the left sidebar, then click **Create policy**.
3. Select the **JSON** tab and paste the following policy (replace `smart-civic-uploads-yourname` with your actual bucket name):
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "s3:PutObject",
                   "s3:PutObjectAcl",
                   "s3:GetObject"
               ],
               "Resource": "arn:aws:s3:::smart-civic-uploads-yourname/*"
           }
       ]
   }
   ```
4. Click **Next**, name the policy `SmartCivicS3Policy`, and click **Create policy**.

#### Part B: Create the IAM User and Generate Keys
1. In the IAM Console, click **Users** in the left sidebar, then click **Create user**.
2. **User name**: Enter `smart-civic-app-user`. Click **Next**.
3. Under **Set permissions**, choose **Attach policies directly**.
4. Search for and select the `SmartCivicS3Policy` you created. Click **Next**, then click **Create user**.
5. Once created, click on the user's name (`smart-civic-app-user`).
6. Open the **Security credentials** tab, scroll down to **Access keys**, and click **Create access key**.
7. Choose **Application running outside AWS** (or Command Line Interface) and click **Next**.
8. Click **Create access key**.
9. **CRITICAL**: Copy the **Access Key ID** and **Secret Access Key** immediately. Store them securely as you will not be able to view the secret key again.

---

### Step 3: Connecting S3 in the Code Environment
Now, plug your AWS credentials into the project using the workspace `.env` file:

1. Open your [.env](file:///c:/Users/Jansi/project/Jansi_Repo_For_AWS_Project/.env) file.
2. Add your AWS details to the existing database variables:
   ```env
   # Database connection URL (Neon serverless cloud)
   DATABASE_URL=postgresql://neondb_owner:npg_S39KbqGOwRjF@ep-shy-morning-aovce2jj.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
   SECRET_KEY=super-secret-key

   # AWS S3 Settings
   AWS_S3_BUCKET=smart-civic-uploads-yourname
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
   AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
   ```
3. Save the file.

When you submit a new civic complaint, the application will automatically connect to AWS, upload the image to the S3 bucket using the `boto3` library in [utils.py](file:///c:/Users/Jansi/project/Jansi_Repo_For_AWS_Project/app/utils.py), and save the public image link (e.g., `https://bucket.s3.region.amazonaws.com/complaints/xyz.png`) directly into the PostgreSQL database.

---

### Step 4: Hosting the Application on AWS EC2
To host this website live on the cloud, we provision an EC2 Virtual Machine:

1. Open the **EC2** Console.
2. Click **Launch instance**:
   * **Name**: `SmartCivicServer`
   * **OS Image**: Select **Ubuntu Server 24.04 LTS**.
   * **Instance type**: `t2.micro` (free-tier eligible).
   * **Key pair**: Create or select a key pair (`.pem`) to securely connect via SSH.
3. Under **Network settings**:
   * Ensure **Allow SSH traffic** is checked.
   * Add a security rule to **Allow HTTP traffic** (Port 80) and **HTTPS traffic** (Port 443) from the internet.
4. Launch the instance and wait for it to run.

#### Deploying on the EC2 Ubuntu Terminal:
Connect to the EC2 server using your key pair via SSH:
```bash
ssh -i "your-key.pem" ubuntu@<your-ec2-public-ip>
```
Once logged in, setup the environment:
```bash
# Update systems
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git nginx

# Clone project code
git clone <your-github-repo-url> smart-civic
cd smart-civic

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file containing database and S3 configurations
nano .env
```
*(Paste your configuration keys from Step 3, save and exit)*.

#### Running in Production with Gunicorn and Nginx:
We use **Gunicorn** to run the Flask app as a daemon service, and **Nginx** to route web traffic on Port 80:
```bash
# Install gunicorn inside the virtual environment
pip install gunicorn

# Test running with Gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 run:app
```
Configure Nginx as a reverse proxy by pointing `location /` to `proxy_pass http://127.0.0.1:5000;` inside `/etc/nginx/sites-available/default`. Reload Nginx (`sudo systemctl reload nginx`), and your web app will be live globally on your EC2 public IP address.

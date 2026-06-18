import os
import uuid
from urllib.parse import urljoin

import boto3
from botocore.exceptions import ClientError
from flask import current_app


def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in current_app.config["UPLOAD_EXTENSIONS"]


def generate_s3_filename(filename):
    extension = os.path.splitext(filename)[1].lower()
    token = uuid.uuid4().hex
    return f"complaints/{token}{extension}"


def upload_file_to_s3(file_storage, filename=None):
    if filename is None:
        filename = generate_s3_filename(file_storage.filename)

    bucket = current_app.config["AWS_S3_BUCKET"]
    region = current_app.config["AWS_REGION"]
    access_key = current_app.config["AWS_ACCESS_KEY_ID"]
    secret_key = current_app.config["AWS_SECRET_ACCESS_KEY"]

    if not access_key or not secret_key or not bucket:
        raise RuntimeError("AWS S3 configuration is incomplete")

    client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    try:
        client.upload_fileobj(
            file_storage,
            bucket,
            filename,
            ExtraArgs={"ACL": "public-read", "ContentType": file_storage.content_type},
        )
    except ClientError as exc:
        current_app.logger.error("Failed to upload to S3: %s", exc)
        raise

    return urljoin(f"https://{bucket}.s3.{region}.amazonaws.com/", filename)

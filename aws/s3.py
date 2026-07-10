import boto3

from aws.config import *


class S3Uploader:

    def __init__(self):

        self.client = boto3.client(

            "s3",

            aws_access_key_id=AWS_ACCESS_KEY_ID,

            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,

            region_name=AWS_REGION,

        )

    def upload(self, file_path):

        key = file_path.name

        self.client.upload_file(

            str(file_path),

            S3_BUCKET,

            key

        )

        print(f"Uploaded : {key}")

        return key
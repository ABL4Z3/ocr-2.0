import os

from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

AWS_REGION = os.getenv("AWS_REGION")

S3_BUCKET = os.getenv("S3_BUCKET")

KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")

DATA_SOURCE_ID = os.getenv("DATA_SOURCE_ID")

MODEL_ARN = os.getenv("MODEL_ARN")
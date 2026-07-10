import time

import boto3

from aws.config import *


class KnowledgeBase:

    def __init__(self):

        self.client = boto3.client(

            "bedrock-agent",

            aws_access_key_id=AWS_ACCESS_KEY_ID,

            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,

            region_name=AWS_REGION,

        )

    def sync(self):

        response = self.client.start_ingestion_job(

            knowledgeBaseId=KNOWLEDGE_BASE_ID,

            dataSourceId=DATA_SOURCE_ID,

            description="Production RAG Sync"

        )

        job = response["ingestionJob"]["ingestionJobId"]

        print("Job :", job)

        return job

    def wait(self, job):

        while True:

            response = self.client.get_ingestion_job(

                knowledgeBaseId=KNOWLEDGE_BASE_ID,

                dataSourceId=DATA_SOURCE_ID,

                ingestionJobId=job

            )

            status = response["ingestionJob"]["status"]

            print(status)

            if status == "COMPLETE":

                return

            if status == "FAILED":

                raise Exception("Ingestion Failed")

            time.sleep(5)
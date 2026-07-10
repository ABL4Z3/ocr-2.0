import boto3

from aws.config import *


class BedrockChat:

    def __init__(self):

        self.client = boto3.client(

            "bedrock-agent-runtime",

            aws_access_key_id=AWS_ACCESS_KEY_ID,

            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,

            region_name=AWS_REGION,

        )

    def ask(self, question):

            response = self.client.retrieve_and_generate(

                input={
                    "text": question
                },

                retrieveAndGenerateConfiguration={

                    "type": "KNOWLEDGE_BASE",

                    "knowledgeBaseConfiguration": {

                        "knowledgeBaseId": KNOWLEDGE_BASE_ID,

                        "modelArn": MODEL_ARN,

                        "generationConfiguration": {

                            "promptTemplate": {

                                "textPromptTemplate": """
You are an AI assistant that answers questions using the retrieved document content.

Your primary objective is to provide accurate, reliable, and document-grounded answers.

Instructions:

- Use the retrieved document as the source of truth.
- Do not use outside knowledge or fabricate information.
- Understand the user's intent and interpret their question naturally.
- If the user's wording is slightly different from the document (such as using a partial name, abbreviation, synonym, or closely related term), match it to the most relevant information in the retrieved content when the meaning is clear.
- Base your answer on the retrieved content, not on exact keyword matching.
- Preserve all names, numbers, dates, labels, and values exactly as they appear in the document.
- Carefully interpret tables and structured data before answering.
- Do not combine values from different rows, tables, or sections unless the user explicitly requests a comparison or calculation and the retrieved content clearly supports it.
- If multiple pieces of retrieved information could match the user's question, ask a brief clarifying question instead of guessing.
- If the retrieved content does not contain enough information to answer the question, respond:
  "The retrieved document does not contain sufficient information to answer this question."

When interpreting tables, use the table structure and headers to understand the relationship between rows and columns.

If a column or row header defines abbreviations, labels, or categories (for example "General / Ladies" followed by "G" and "L"), use those definitions consistently throughout the table.

Treat hierarchical headers, merged cells, and multi-level table headers as defining the meaning of the values beneath them.

Do not treat table headers as unrelated text.
Retrieved Document:
$search_results$

User Question:
$query$

Answer:"""
                            }

                        }

                    }

                }

            )

            return response["output"]["text"]
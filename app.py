from pathlib import Path
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from main import process_document

from aws.s3 import S3Uploader
from aws.knowledge_base import KnowledgeBase
from aws.chat import BedrockChat


app = FastAPI(
    title="Production RAG",
    version="1.0"
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

s3 = S3Uploader()
kb = KnowledgeBase()
chat = BedrockChat()


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Production RAG API Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ---------------------------------------------------------
# Upload + Extract + Upload to S3
# ---------------------------------------------------------

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    if file.filename == "":

        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    suffix = Path(file.filename).suffix

    filename = f"{uuid.uuid4()}{suffix}"

    pdf_path = UPLOAD_DIR / filename

    with open(pdf_path, "wb") as f:

        shutil.copyfileobj(
            file.file,
            f
        )

    print("PDF Saved :", pdf_path)

    # ----------------------------------------
    # Extract
    # ----------------------------------------

    md_path = process_document(pdf_path)

    # ----------------------------------------
    # Upload Markdown to S3
    # ----------------------------------------

    key = s3.upload(md_path)

    return {

        "message": "Uploaded Successfully",

        "markdown": str(md_path),

        "s3_key": key

    }


# ---------------------------------------------------------
# Sync Knowledge Base
# ---------------------------------------------------------

@app.post("/sync")
def sync():

    job = kb.sync()

    kb.wait(job)

    return {

        "message": "Knowledge Base Updated",

        "job": job

    }


# ---------------------------------------------------------
# Ask Questions
# ---------------------------------------------------------

@app.post("/chat")
def ask(question: str):

    answer = chat.ask(question)

    return {

        "answer": answer

    }


# ---------------------------------------------------------
# Upload + Sync (One Click)
# ---------------------------------------------------------

@app.post("/ingest")
async def ingest(
    file: UploadFile = File(...)
):

    suffix = Path(file.filename).suffix

    filename = f"{uuid.uuid4()}{suffix}"

    pdf_path = UPLOAD_DIR / filename

    with open(pdf_path, "wb") as f:

        shutil.copyfileobj(
            file.file,
            f
        )

    md_path = process_document(pdf_path)

    key = s3.upload(md_path)

    job = kb.sync()

    kb.wait(job)

    return {

        "message": "Document Ready",

        "markdown": str(md_path),

        "s3_key": key,

        "job": job

    }


# ---------------------------------------------------------
# Run
# ---------------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "app:app",

        host="0.0.0.0",

        port=8000,

        reload=True

    )
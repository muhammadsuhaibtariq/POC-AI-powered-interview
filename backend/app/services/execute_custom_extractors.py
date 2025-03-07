import os
from tempfile import NamedTemporaryFile

import fitz  # PyMuPDF for PDF processing
from docx import Document
from fastapi import UploadFile, HTTPException

async def process_extract_text(file: UploadFile) -> str:
    """Processes the uploaded file and extracts text."""
    try:
        file_ext = os.path.splitext(file.filename)[1].lower()

        with NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        if file_ext == ".pdf":
            text = extract_text_from_pdf(tmp_path)
        elif file_ext == ".docx":
            text = extract_text_from_docx(tmp_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        return text

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a PDF file using PyMuPDF."""
    try:
        doc = fitz.open(file_path)
        return "\n".join([page.get_text("text") for page in doc])
    except Exception as e:
        return str(e)


def extract_text_from_docx(file_path: str) -> str:
    """Extracts text from a DOCX file using python-docx."""
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return str(e)

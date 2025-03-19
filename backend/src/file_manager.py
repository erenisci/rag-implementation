import os
import shutil

from src.embedding import delete_pdf_embeddings
from src.preprocessing import delete_processed_pdf
from src.settings import settings


RAW_DIR = settings["PDF_RAW"]
PROCESSED_DIR = settings["PDF_PROCESSED"]


def ensure_directories():
    """Ensures that required directories exist."""
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)


def upload_pdf(file_path, file_obj):
    """Uploads a PDF file to the raw directory with validation."""
    ensure_directories()

    if not file_path.endswith(".pdf"):
        raise ValueError("Error: Only PDF files are allowed.")

    file_name = os.path.basename(file_path)
    destination_path = os.path.join(RAW_DIR, file_name)

    if os.path.exists(destination_path):
        raise FileExistsError(
            f"{file_name} already exists in raw directory.")

    try:
        with open(destination_path, "wb") as buffer:
            shutil.copyfileobj(file_obj.file, buffer)
        print(f"📥 Uploaded {file_name} to {RAW_DIR}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while copying file: {str(e)}")


def delete_pdf(pdf_name):
    """Deletes a PDF from raw, its processed folder, and its embeddings in ChromaDB."""
    raw_path = os.path.join(RAW_DIR, pdf_name)

    if os.path.exists(raw_path):
        os.remove(raw_path)
        print(f"Deleted {pdf_name} from raw directory.")
    else:
        print(f"Warning: {pdf_name} not found in raw directory.")

    delete_processed_pdf(pdf_name)

    delete_pdf_embeddings(pdf_name)


def list_pdfs():
    """Lists all uploaded PDF files with their sizes."""
    pdf_files = [
        {
            "name": f,
            "size_mb": round(
                os.stat(os.path.join(
                    settings["PDF_RAW"], f)).st_size / (1024 * 1024), 2
            ),
        }
        for f in os.listdir(settings["PDF_RAW"])
        if f.endswith(".pdf")
    ]
    return pdf_files

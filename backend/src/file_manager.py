import json
import os
import shutil

from src.embedding import delete_pdf_embeddings
from src.preprocessing import delete_processed_pdf
from src.settings import settings


RAW_DIR = settings["PDF_RAW"]
PROCESSED_DIR = settings["PDF_PROCESSED"]
PROCESSED_FILES_PATH = os.path.join(RAW_DIR, "processed_files.json")


def ensure_directories():
    """Ensures that required directories exist."""
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)


def save_json(filepath, data):
    """Saves data to a JSON file."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving JSON file {filepath}: {e}")


def load_json(filepath, default_value=None):
    """Loads a JSON file and returns its contents."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Failed to parse JSON file: {filepath}")
    return default_value if default_value is not None else []


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
        print(f"Uploaded {file_name} to {RAW_DIR}")
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

    processed_files = load_json(PROCESSED_FILES_PATH, [])
    if pdf_name in processed_files:
        processed_files.remove(pdf_name)
        save_json(PROCESSED_FILES_PATH, processed_files)
        print(f"Deleted {pdf_name} from processed_files.json")
    else:
        print(f"Warning: {pdf_name} not found in processed_files.json")


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

import os
import shutil

import chromadb
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from src.embedding import store_embeddings_in_chromadb
from src.preprocessing import process_all_pdfs
from src.rag import ask_question
from src.settings import load_settings, save_settings, settings


app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/status/")
def status():
    """Checks if the API is running."""
    return {"status": "API is running"}


@app.post("/ask/")
def ask(question: str):
    """Processes a question using the document retrieval system and returns an answer."""
    answer = ask_question(question)
    return {"answer": answer}


@app.get("/get-settings/")
def get_settings():
    """Returns the latest settings by reloading the JSON file."""
    return load_settings()


@app.post("/update-settings/")
def update_settings(updated_settings: dict):
    """Updates settings and ensures latest values are available."""
    save_settings(updated_settings)
    return {"message": "Settings updated successfully!"}


@app.get("/list-pdfs/")
def list_pdfs():
    """Lists all uploaded PDF files with their sizes."""
    pdf_files = [
        {
            "name": f,
            "size_mb": round(
                os.stat(os.path.join(settings["PDF_RAW"], f)).st_size / (1024 * 1024), 2
            ),
        }
        for f in os.listdir(settings["PDF_RAW"])
        if f.endswith(".pdf")
    ]
    return {"pdfs": pdf_files}


@app.post("/upload-pdf/")
def upload_pdf(file: UploadFile = File(...)):
    """Uploads a PDF file to the raw data directory."""
    file_path = os.path.join(settings["PDF_RAW"], file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    file_size = round(os.stat(file_path).st_size / (1024 * 1024), 2)
    return {"message": f"{file.filename} uploaded successfully", "size_mb": file_size}


@app.post("/process-pdfs/")
def process_pdfs():
    """Processes all PDFs available in the raw folder and ensures ChromaDB is safely reset."""
    try:
        client = chromadb.PersistentClient(path=settings["CHROMA_DB_DIR"])
        client.delete_collection(name=settings["COLLECTION_NAME"])
        client.get_or_create_collection(name=settings["COLLECTION_NAME"])

        del client
    except Exception as e:
        print(f"ChromaDB error: {e}")

    if os.path.exists(settings["CHROMA_DB_DIR"]):
        shutil.rmtree(settings["CHROMA_DB_DIR"], ignore_errors=True)
    os.makedirs(settings["CHROMA_DB_DIR"], exist_ok=True)

    if os.path.exists(settings["PDF_PROCESSED"]):
        shutil.rmtree(settings["PDF_PROCESSED"], ignore_errors=True)
    os.makedirs(settings["PDF_PROCESSED"], exist_ok=True)

    process_all_pdfs()
    store_embeddings_in_chromadb()

    return {"message": "All PDFs processed and embeddings stored successfully."}


@app.delete("/delete-pdf/")
def delete_pdf(file_name: str):
    """Deletes a specified PDF file, its processed data, and associated embeddings."""
    file_path = os.path.join(settings["PDF_RAW"], file_name)
    processed_folder = os.path.join(
        settings["PDF_PROCESSED"], file_name.replace(".pdf", "")
    )

    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found in raw folder")

    if os.path.exists(processed_folder):
        shutil.rmtree(processed_folder)

    pdf_name = file_name.replace(".pdf", "")
    try:
        client = chromadb.PersistentClient(path=settings["CHROMA_DB_DIR"])
        vector_db = client.get_or_create_collection(name=settings["COLLECTION_NAME"])
        vector_db.delete(where={"pdf_name": pdf_name})
        print(f"Embeddings for {pdf_name} deleted successfully from ChromaDB.")
    except Exception as e:
        print(f"Warning: Could not delete embeddings for {pdf_name}: {e}")

    return {"message": f"{file_name} and all related data deleted successfully"}

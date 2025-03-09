import json
import os
import shutil
import sqlite3
import uuid
from typing import List, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.embedding import (delete_pdf_embeddings, reset_chroma_db,
                           store_embeddings_in_chromadb)
from src.preprocessing import process_all_pdfs
from src.rag import ask_question
from src.settings import load_settings, save_settings, settings


class ChatRequest(BaseModel):
    question: str

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_db():
    """Ensures database file and table exist."""
    db_path = settings["CHAT_HISTORY"]
    db_dir = os.path.dirname(db_path)

    os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            chat_id TEXT PRIMARY KEY,
            messages TEXT
        )
    ''')
    conn.commit()
    conn.close()


init_db()


@app.get("/status/")
def status():
    """Checks if the API is running."""
    return {"status": "API is running"}


@app.post("/new-chat/")
def new_chat():
    """Creates a new chat and returns an ID."""
    chat_id = str(uuid.uuid4())
    conn = sqlite3.connect(settings["CHAT_HISTORY"])
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (chat_id, messages) VALUES (?, ?)", (chat_id, "[]"))
    conn.commit()
    conn.close()
    return {"chat_id": chat_id}


@app.get("/get-chats/")
def get_chats():
    """Lists all chats."""
    conn = sqlite3.connect(settings["CHAT_HISTORY"])
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM chats")
    chats = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"chats": chats}


@app.delete("/delete-chat/{chat_id}")
def delete_chat(chat_id: str):
    """Deletes a specific chat from the database."""
    conn = sqlite3.connect(settings["CHAT_HISTORY"])
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chats WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()

    return {"message": f"Chat {chat_id} deleted successfully"}


@app.get("/get-chat-history/{chat_id}")
def get_chat_history(chat_id: str):
    """Returns the history of the specified chat."""
    conn = sqlite3.connect(settings["CHAT_HISTORY"])
    cursor = conn.cursor()
    cursor.execute("SELECT messages FROM chats WHERE chat_id = ?", (chat_id,))
    chat = cursor.fetchone()
    conn.close()
    
    if chat:
        return {"chat_id": chat_id, "messages": eval(chat[0])}
    else:
        raise HTTPException(status_code=404, detail="Chat not found")

@app.post("/ask/")
def ask_question_api(data: ChatRequest):
    """Handles incoming chat requests without storing any data and without history."""

    print("\n📝 ----------- Yeni API Çağrısı -----------")
    print(f"📥 Gelen İstek Verisi: {data.dict()}")
    print("------------------------------------------\n")

    question = data.question.strip()

    # 📌 Boş soru gönderilmesini engelle
    if not question:
        return {"answer": "Lütfen geçerli bir soru girin."}

    response = ask_question(question)  # 📌 Sadece gelen soruyu AI'ya sor

    print(f"✅ AI Yanıtı: {response}")
    return {"answer": response}



@app.get("/get-settings/")
def get_settings():
    """Returns the latest settings by reloading the JSON file."""
    return load_settings()


@app.post("/update-settings/")
def update_settings(updated_settings: dict):
    """Updates settings and ensures latest values are available."""
    updated_settings["API_KEY"] = updated_settings["API_KEY"].strip()
    updated_settings["MODEL"] = updated_settings["MODEL"].strip()
    updated_settings["SYSTEM_PROMPT"] = updated_settings["SYSTEM_PROMPT"].strip()
    
    save_settings(updated_settings)
    global settings
    settings = load_settings()
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
        reset_chroma_db()

        if os.path.exists(settings["PDF_PROCESSED"]):
            shutil.rmtree(settings["PDF_PROCESSED"], ignore_errors=True)
        os.makedirs(settings["PDF_PROCESSED"], exist_ok=True)

        process_all_pdfs()
        store_embeddings_in_chromadb()

        return {"message": "All PDFs processed and embeddings stored successfully."}

    except Exception as e:
        print(f"Error processing PDFs: {e}")
        return {"error": str(e)}


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
        
    delete_pdf_embeddings(file_name.replace(".pdf", ""))

    return {"message": f"{file_name} and all related data deleted successfully"}

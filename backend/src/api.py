import os
import shutil
import uuid
from typing import List, Optional
from urllib.parse import unquote

from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.chat_manager import (delete_chat, get_chat_history, list_chats,
                              save_chat_history, update_chat_title)
from src.embedding import reset_chroma_db, store_embeddings_in_chromadb
from src.file_manager import delete_pdf, list_pdfs, upload_pdf
from src.preprocessing import process_all_pdfs
from src.retrieval import chain, initialize_chain
from src.settings import load_settings, save_settings, settings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    chat_id: Optional[str] = None
    question: str
    chat_history: List[dict] = []


@app.post("/ask/")
async def ask_ai(data: ChatRequest):
    """Handles user queries and maintains chat history."""
    if not chain:
        raise HTTPException(
            status_code=500, detail="AI model not initialized. Please set an API key.")

    chat_id = data.chat_id or str(uuid.uuid4())
    chat_history = get_chat_history(chat_id)

    chat_history.append({"sender": "user", "text": data.question})

    if chat_history:
        formatted_history = "\n".join(
            [f"{msg['sender']}: {msg['text']}" for msg in chat_history]
        )
        full_prompt = f"Previous conversation:\n{formatted_history}\nUser: {data.question}"
    else:
        full_prompt = f"User: {data.question}"

    try:
        response = chain.invoke({"input": full_prompt})
        answer = response["answer"]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"AI processing error: {str(e)}")

    chat_history.append({"sender": "ai", "text": answer})
    save_chat_history(chat_id, chat_history)

    return {"chat_id": chat_id, "answer": answer}


@app.get("/get-chats/")
async def get_chats():
    """Lists all chats with titles."""
    return {"chats": list_chats()}


@app.get("/get-chat-history/{chat_id}")
async def get_chat_history_api(chat_id: str):
    """Returns the history of the specified chat."""
    history = get_chat_history(chat_id)
    if not history:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"chat_id": chat_id, "messages": history}


@app.post("/update-chat-title/{chat_id}/{new_title}")
async def update_chat_title_api(chat_id: str, new_title: str):
    """Updates the title of a given chat."""
    update_chat_title(chat_id, new_title)
    return {"message": "Chat title updated successfully"}


@app.delete("/delete-chat/{chat_id}")
async def delete_chat_api(chat_id: str):
    """Deletes a specific chat from the database."""
    delete_chat(chat_id)
    return {"message": f"Chat {chat_id} deleted successfully"}


@app.post("/upload-pdf/")
async def upload_pdf_api(file: UploadFile = File(...)):
    """Uploads a PDF file to the raw data directory."""
    try:
        file_size_mb = len(file.file.read()) / (1024 * 1024)
        file.file.seek(0)

        file_path = os.path.join(settings["PDF_RAW"], file.filename)

        upload_pdf(file_path, file)
        return {"message": f"✅ {file.filename} uploaded successfully!", "size_mb": round(file_size_mb, 2)}

    except FileExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError:
        raise HTTPException(
            status_code=500, detail="❌ Permission error: Check file system permissions.")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"❌ Unexpected error: {str(e)}")


@app.get("/list-pdfs/")
async def get_list():
    """Lists all uploaded PDFs."""
    return {"pdfs": list_pdfs()}


@app.delete("/delete-pdf/")
async def delete(pdf_name: str = Query(..., description="The name of the PDF file to delete")):
    """Deletes a PDF from the system, including processed data and embeddings."""
    decoded_pdf_name = unquote(pdf_name)

    pdf_list = [pdf["name"] for pdf in list_pdfs()]

    if decoded_pdf_name not in pdf_list:
        raise HTTPException(
            status_code=404, detail=f"File '{decoded_pdf_name}' not found in the system.")

    delete_pdf(decoded_pdf_name)
    return {"message": f"File '{decoded_pdf_name}' deleted successfully!"}


@app.post("/process-pdfs/")
async def process_pdfs():
    """Processes all PDFs and stores embeddings in ChromaDB."""
    try:
        reset_chroma_db()

        if os.path.exists(settings["PDF_PROCESSED"]):
            shutil.rmtree(settings["PDF_PROCESSED"], ignore_errors=True)
        os.makedirs(settings["PDF_PROCESSED"], exist_ok=True)

        process_all_pdfs()
        store_embeddings_in_chromadb()

        global chain
        _, _, chain = initialize_chain()

        return {"message": "All PDFs processed and embeddings stored successfully."}

    except FileNotFoundError as e:
        return {"error": f"File not found: {str(e)}"}
    except PermissionError as e:
        return {"error": f"Permission denied: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


@app.get("/get-settings/")
async def get_settings():
    """Returns the latest settings."""
    return load_settings()


@app.post("/update-settings/")
async def update_settings(updated_settings: dict):
    """Updates settings and ensures latest values are available."""
    save_settings(updated_settings)
    global settings

    settings = load_settings()
    return {"message": "Settings updated successfully!"}

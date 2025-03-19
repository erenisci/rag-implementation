import hashlib
import json
import os
import shutil

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from src.settings import settings


load_dotenv(override=True)

PROCESSED_DIR = settings["PDF_PROCESSED"]
CHROMA_DB_DIR = settings["CHROMA_DB_DIR"]
COLLECTION_NAME = settings["COLLECTION_NAME"]
EMBEDDING_MODEL = settings["EMBEDDING_MODEL"]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def reset_chroma_db():
    """Resets ChromaDB by deleting and recreating the database directory."""
    if os.path.exists(CHROMA_DB_DIR):
        shutil.rmtree(CHROMA_DB_DIR, ignore_errors=True)

    os.makedirs(CHROMA_DB_DIR, exist_ok=True)

    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    return client


def get_openai_embedding_function():
    """Returns the OpenAI embedding function if API key exists, otherwise None."""
    if not OPENAI_API_KEY:
        print("WARNING: No OpenAI API Key provided. Running without OpenAI embeddings.")
        return None

    return embedding_functions.OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model_name=EMBEDDING_MODEL)


def get_chroma_client():
    """Creates and returns ChromaDB client and collection."""
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    openai_ef = get_openai_embedding_function()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=openai_ef
    )

    return client, collection


def get_existing_pdfs(collection):
    """Fetches all PDF names that have embeddings stored in ChromaDB."""
    try:
        existing_data = collection.get()
        return set(metadata["pdf_name"] for metadata in existing_data["metadatas"] if "pdf_name" in metadata)
    except Exception as e:
        print(f"Error fetching existing embeddings: {e}")
        return set()


def load_text_chunks(pdf_name):
    """Loads text chunks from the processed directory."""
    pdf_path = os.path.join(PROCESSED_DIR, pdf_name)
    metadata_path = os.path.join(pdf_path, "metadata.json")

    if not os.path.exists(metadata_path):
        print(f"Metadata not found for {pdf_name}. Skipping...")
        return []

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    chunks = []
    for chunk_file in metadata["chunk_files"]:
        chunk_path = os.path.join(pdf_path, chunk_file)
        with open(chunk_path, "r", encoding="utf-8") as f:
            chunks.append(f.read().strip())

    return chunks


def store_embeddings_in_chromadb():
    """Stores text chunks as embeddings in ChromaDB, avoiding duplicates."""
    _, collection = get_chroma_client()

    if collection is None:
        print("ERROR: ChromaDB collection not found. Skipping embedding storage.")
        return

    existing_pdfs = get_existing_pdfs(collection)

    pdf_folders = [f for f in os.listdir(
        PROCESSED_DIR) if os.path.isdir(os.path.join(PROCESSED_DIR, f))]
    if not pdf_folders:
        print("No processed PDFs found.")
        return

    print(f"Found {len(pdf_folders)} PDFs. Checking for new embeddings...")

    for pdf_name in pdf_folders:
        if pdf_name in existing_pdfs:
            print(f"Skipping {pdf_name}, already embedded.")
            continue

        chunks = load_text_chunks(pdf_name)
        if not chunks:
            continue

        for i, chunk in enumerate(chunks):
            unique_id = hashlib.md5(
                (pdf_name + chunk[:20]).encode()).hexdigest()

            collection.add(
                ids=[unique_id],
                documents=[chunk],
                metadatas=[{"pdf_name": pdf_name, "chunk_id": i+1}],
            )

        print(f"{pdf_name}: {len(chunks)} chunks embedded and stored.")


def delete_pdf_embeddings(pdf_name):
    """Deletes all embeddings related to a specific PDF from ChromaDB."""
    _, collection = get_chroma_client()

    if collection is None:
        print("ERROR: ChromaDB collection not found. Skipping deletion.")
        return

    try:
        collection.delete(where={"pdf_name": pdf_name})
        print(f"Deleted all embeddings related to {pdf_name}")

    except Exception as e:
        print(f"Error deleting embeddings for {pdf_name}: {e}")

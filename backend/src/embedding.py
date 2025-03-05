import hashlib
import os

import chromadb
from src.settings import settings


client = chromadb.PersistentClient(path=settings["CHROMA_DB_DIR"])


def get_vector_db():
    """Check if the collection exists and create it if necessary."""
    try:
        collections = client.list_collections()
        if settings["COLLECTION_NAME"] in collections:
            return client.get_collection(name=settings["COLLECTION_NAME"])

        print(
            f"Warning: Collection '{settings['COLLECTION_NAME']}' not found. Creating a new one."
        )
        return client.get_or_create_collection(name=settings["COLLECTION_NAME"])

    except Exception as e:
        print(f"Error getting ChromaDB collection: {e}")
        return None


vector_db = get_vector_db()


def load_text_chunks():
    """Loads text chunks from separate folders inside the processed directory."""
    chunks = []
    file_names = []
    pdf_names = []

    for folder in sorted(os.listdir(settings["PDF_PROCESSED"])):
        folder_path = os.path.join(settings["PDF_PROCESSED"], folder)

        if os.path.isdir(folder_path):
            for filename in sorted(os.listdir(folder_path)):
                if filename.endswith(".txt"):
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, "r", encoding="utf-8") as file:
                        chunks.append(file.read())
                        file_names.append(f"{folder}/{filename}")
                        pdf_names.append(folder)

    return chunks, file_names, pdf_names


def store_embeddings_in_chromadb():
    """Generates embeddings for text chunks and stores them in ChromaDB."""
    global vector_db
    vector_db = get_vector_db()

    if vector_db is None:
        print("ChromaDB collection not found. Skipping embedding storage.")
        return

    chunks, file_names, pdf_names = load_text_chunks()
    if not chunks:
        print("No chunks found in processed folder.")
        return

    for i, chunk in enumerate(chunks):
        unique_id = hashlib.md5(
            (pdf_names[i] + file_names[i] + chunk[:20]).encode()
        ).hexdigest()

        vector_db.add(
            ids=[unique_id],
            documents=[chunk],
            metadatas=[{"source": file_names[i], "pdf_name": pdf_names[i]}],
        )

    print(f"{len(chunks)} new chunks added to ChromaDB!")

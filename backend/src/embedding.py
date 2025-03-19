import hashlib
import os
import shutil

import chromadb
from chromadb.utils import embedding_functions
from src.settings import settings


def get_openai_embedding_function():
    """Returns the OpenAI embedding function if API key exists, otherwise None."""
    if not os.getenv("API_KEY"):
        print("WARNING: No OpenAI API Key provided. Running without OpenAI embeddings.")
        return None

    return embedding_functions.OpenAIEmbeddingFunction(api_key=os.getenv("API_KEY"), model_name=settings["EMBEDDING_MODEL"])


def get_chroma_client():
    """Creates and returns ChromaDB client and collection."""
    os.makedirs(settings["CHROMA_DB_DIR"], exist_ok=True)
    client = chromadb.PersistentClient(path=settings["CHROMA_DB_DIR"])
    openai_ef = get_openai_embedding_function()

    collection = client.get_or_create_collection(
        name=settings["COLLECTION_NAME"],
        embedding_function=openai_ef
    )

    return client, collection


def load_text_chunks():
    """Loads text chunks from processed directories."""
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
    """Stores text chunks as embeddings."""
    global vector_db
    _, vector_db = get_chroma_client()

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


def delete_pdf_embeddings(pdf_name):
    """Deletes all embeddings related to a specific PDF from ChromaDB."""
    global vector_db
    _, vector_db = get_chroma_client()

    if vector_db is None:
        print("ChromaDB collection not found. Skipping deletion.")
        return

    try:
        all_embeddings = vector_db.get()
        ids_to_delete = [
            doc_id for doc_id, metadata in zip(all_embeddings["ids"], all_embeddings["metadatas"])
            if metadata.get("pdf_name") == pdf_name
        ]

        if ids_to_delete:
            vector_db.delete(ids=ids_to_delete)
            print(
                f"Deleted {len(ids_to_delete)} embeddings related to {pdf_name}")
        else:
            print(f"No embeddings found for {pdf_name}")

    except Exception as e:
        print(f"Error deleting embeddings for {pdf_name}: {e}")


def reset_chroma_db():
    """Resets ChromaDB and recreates the collection."""
    if os.path.exists(settings["CHROMA_DB_DIR"]):
        shutil.rmtree(settings["CHROMA_DB_DIR"], ignore_errors=True)

    os.makedirs(settings["CHROMA_DB_DIR"], exist_ok=True)

    global client, vector_db
    _, vector_db = get_chroma_client()

    if vector_db:
        print("ChromaDB reset and collection recreated.")
    else:
        print("Error resetting ChromaDB.")

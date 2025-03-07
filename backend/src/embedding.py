import hashlib
import os
import shutil

import chromadb
from chromadb.utils import embedding_functions
from src.settings import settings


openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=settings["API_KEY"],
    model_name=settings["EMBEDDING_MODEL"]
)

client = chromadb.PersistentClient(path=settings["CHROMA_DB_DIR"])

def get_vector_db():
    """Gets or creates an existing ChromaDB collection."""
    try:
        collection = client.get_collection(
            name=settings["COLLECTION_NAME"], 
            embedding_function=openai_ef 
        )
        print(f"Loaded ChromaDB collection: {collection.name}")
        return collection
    except Exception as e:
        print(f"Error accessing ChromaDB collection: {e}. Creating a new one.")
        return client.get_or_create_collection(
            name=settings["COLLECTION_NAME"],
            embedding_function=openai_ef 
        )

vector_db = get_vector_db()

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

def delete_pdf_embeddings(pdf_name):
    """Deletes all embeddings related to a specific PDF from ChromaDB."""
    global vector_db
    vector_db = get_vector_db()

    if vector_db is None:
        print("ChromaDB collection not found. Skipping deletion.")
        return

    all_embeddings = vector_db.get()

    ids_to_delete = [
        doc_id for doc_id, metadata in zip(all_embeddings["ids"], all_embeddings["metadatas"])
        if metadata["pdf_name"] == pdf_name
    ]

    if ids_to_delete:
        vector_db.delete(ids=ids_to_delete)
        print(f"Deleted {len(ids_to_delete)} embeddings related to {pdf_name}")
    else:
        print(f"No embeddings found for {pdf_name}")


def reset_chroma_db():
    """Resets ChromaDB and recreates the collection."""
    if os.path.exists(settings["CHROMA_DB_DIR"]):
        shutil.rmtree(settings["CHROMA_DB_DIR"], ignore_errors=True)

    os.makedirs(settings["CHROMA_DB_DIR"], exist_ok=True)

    global client
    client = chromadb.PersistentClient(path=settings["CHROMA_DB_DIR"])
    global vector_db
    vector_db = client.get_or_create_collection(
        name=settings["COLLECTION_NAME"],
        embedding_function=openai_ef 
    )

    print("ChromaDB reset and collection recreated.")

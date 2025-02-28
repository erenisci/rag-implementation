import os

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

import config


def load_text_chunks():
    """Loads text chunks from processed folder."""
    chunks = []
    file_names = []

    for filename in sorted(os.listdir(config.PDF_PROCESSED)):
        if filename.endswith(".txt"):
            file_path = os.path.join(config.PDF_PROCESSED, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                chunks.append(file.read())
                file_names.append(filename)

    return chunks, file_names


def store_embeddings_in_chromadb():
    """Generates embeddings for text chunks and stores them in ChromaDB."""
    chunks, file_names = load_text_chunks()
    if not chunks:
        print("No chunks found in processed folder.")
        return

    # Initialize OpenAI Embedding Model
    embedding_model = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)

    # Initialize ChromaDB
    db = Chroma(
        collection_name=config.COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory="data/chroma_db",
    )

    # Add chunks to ChromaDB
    for i, chunk in enumerate(chunks):
        db.add_texts(texts=[chunk], metadatas=[{"source": file_names[i]}])

    print(f"{len(chunks)} new chunks added to ChromaDB!")


if __name__ == "__main__":
    store_embeddings_in_chromadb()

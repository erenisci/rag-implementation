import os


# Define paths for raw and processed PDFs
PDF_RAW = "data/raw/"
PDF_PROCESSED = "data/processed/"
COLLECTION_NAME = "pdf_embeddings"
EMBEDDING_MODEL = "text-embedding-3-large"
GPT_MODEL = "gpt-3.5-turbo"

# Ensure directories exist
os.makedirs(PDF_RAW, exist_ok=True)
os.makedirs(PDF_PROCESSED, exist_ok=True)

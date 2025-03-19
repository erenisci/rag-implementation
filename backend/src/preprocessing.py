import json
import os
import shutil

import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.settings import settings


RAW_DIR = settings["PDF_RAW"]
PROCESSED_DIR = settings["PDF_PROCESSED"]
PROCESSED_FILES_PATH = os.path.join(RAW_DIR, "processed_files.json")


def load_json(filepath, default_value=None):
    """Loads a JSON file, returns default value if file does not exist."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Failed to parse JSON file: {filepath}")
    return default_value if default_value is not None else {}


def save_json(filepath, data):
    """Saves data to a JSON file."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving JSON file {filepath}: {e}")


def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file."""
    try:
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text()
                             for page in pdf.pages if page.extract_text())
        return text if text.strip() else None
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None


def split_text(text, chunk_size=500, overlap=50):
    """Splits text into smaller chunks using LangChain's RecursiveCharacterTextSplitter."""
    return RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap).split_text(text)


def save_chunks(chunks, pdf_name):
    """Saves text chunks into separate files in the processed directory."""
    base_filename = os.path.splitext(pdf_name)[0]
    pdf_output_dir = os.path.join(PROCESSED_DIR, base_filename)
    os.makedirs(pdf_output_dir, exist_ok=True)

    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_filename = f"chunk_{i+1}.txt"
        chunk_path = os.path.join(pdf_output_dir, chunk_filename)
        with open(chunk_path, "w", encoding="utf-8") as text_file:
            text_file.write(chunk)
        chunk_files.append(chunk_filename)

    metadata = {"pdf_name": base_filename, "total_chunks": len(
        chunks), "chunk_files": chunk_files}
    save_json(os.path.join(pdf_output_dir, "metadata.json"), metadata)

    print(f"Processed: {pdf_name} ({len(chunks)} chunks)")


def process_pdf(pdf_name):
    """Processes a single PDF: extracts text, splits into chunks, and saves."""
    processed_files = set(load_json(PROCESSED_FILES_PATH, []))

    if pdf_name in processed_files:
        print(f"Skipping {pdf_name}, already processed.")
        return

    pdf_path = os.path.join(RAW_DIR, pdf_name)
    if not os.path.exists(pdf_path):
        print(f"Warning: {pdf_name} not found. Skipping...")
        return

    extracted_text = extract_text_from_pdf(pdf_path)
    if not extracted_text:
        print(f"Warning: No extractable text in {pdf_name}. Skipping...")
        return

    chunks = split_text(extracted_text, chunk_size=500, overlap=50)
    save_chunks(chunks, pdf_name)

    processed_files.add(pdf_name)
    save_json(PROCESSED_FILES_PATH, list(processed_files))


def process_all_pdfs():
    """Processes all PDFs in the raw directory."""
    pdf_files = [f for f in os.listdir(RAW_DIR) if f.endswith(".pdf")]

    if not pdf_files:
        print("No PDFs found in the raw directory.")
        return

    print(f"Found {len(pdf_files)} PDFs. Processing...")
    for pdf_file in pdf_files:
        process_pdf(pdf_file)


def delete_processed_pdf(pdf_name):
    """Deletes the processed folder if the corresponding PDF is removed from raw."""
    base_filename = os.path.splitext(pdf_name)[0]
    processed_path = os.path.join(PROCESSED_DIR, base_filename)

    if os.path.exists(processed_path):
        shutil.rmtree(processed_path, ignore_errors=True)
        print(f"Deleted processed data for {pdf_name}")

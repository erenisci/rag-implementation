import os

import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.settings import settings


def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file and returns the full text as a string."""
    texts = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    texts.append(text)
        return "\n".join(texts)
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None


def split_text_with_langchain(text, chunk_size=500, overlap=50):
    """Splits text into smaller chunks using LangChain's RecursiveCharacterTextSplitter."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap
    )

    return text_splitter.split_text(text)


def process_pdf(pdf_name):
    """Processes a PDF file from the raw folder, extracts text, splits it into chunks, and saves the output."""
    pdf_path = os.path.join(settings["PDF_RAW"], pdf_name)
    if not os.path.exists(pdf_path):
        print(
            f"Warning: {pdf_name} not found in {settings['PDF_RAW']}. Skipping.")
        return

    extracted_text = extract_text_from_pdf(pdf_path)
    if not extracted_text:
        print(f"Warning: No extractable text found in {pdf_name}. Skipping.")
        return

    text_chunks = split_text_with_langchain(
        extracted_text, chunk_size=500, overlap=50)

    base_filename = pdf_name.replace(".pdf", "")
    pdf_output_dir = os.path.join(settings["PDF_PROCESSED"], base_filename)
    os.makedirs(pdf_output_dir, exist_ok=True)

    for i, chunk in enumerate(text_chunks):
        output_path = os.path.join(pdf_output_dir, f"chunk{i+1}.txt")
        with open(output_path, "w", encoding="utf-8") as text_file:
            text_file.write(chunk)

    print(f"Processed {pdf_name}: {len(text_chunks)} chunks saved.")


def process_all_pdfs():
    """Scans the raw folder and processes all available PDF files."""
    pdf_files = [f for f in os.listdir(
        settings["PDF_RAW"]) if f.endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the raw folder.")
        return

    print(f"Found {len(pdf_files)} PDFs. Processing...")
    for pdf_file in pdf_files:
        process_pdf(pdf_file)

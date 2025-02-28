import os

import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter

import config


def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file and returns the full text as a string."""
    texts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                texts.append(text)
    full_text = "\n".join(texts)

    return full_text


def split_text_with_langchain(text, chunk_size=500, overlap=50):
    """Splits text into smaller chunks using LangChain's RecursiveCharacterTextSplitter."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap
    )

    return text_splitter.split_text(text)


def process_pdf(pdf_name):
    """Processes a PDF file from the raw folder, extracts text, splits it into chunks, and saves the output."""
    pdf_path = os.path.join(config.PDF_RAW, pdf_name)

    extracted_text = extract_text_from_pdf(pdf_path)
    text_chunks = split_text_with_langchain(extracted_text, chunk_size=500, overlap=50)

    base_filename = pdf_name.replace(".pdf", "")
    for i, chunk in enumerate(text_chunks):
        output_path = os.path.join(
            config.PDF_PROCESSED, f"{base_filename}_chunk{i+1}.txt"
        )
        with open(output_path, "w", encoding="utf-8") as text_file:
            text_file.write(chunk)


def process_all_pdfs():
    """Scans the raw folder and processes all available PDF files."""
    pdf_files = [f for f in os.listdir(config.PDF_RAW) if f.endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the raw folder.")
        return

    print(f"Found {len(pdf_files)} PDFs. Processing...")
    for pdf_file in pdf_files:
        process_pdf(pdf_file)


if __name__ == "__main__":
    # process_pdf("pdfname.pdf")
    process_all_pdfs()

# Retrieval-Augmented Generation (RAG) with LangChain & ChromaDB

This project is a **Retrieval-Augmented Generation (RAG)** system that enables users to ask questions based on **PDF documents**.  
It extracts text from PDFs, stores embeddings in **ChromaDB**, and retrieves relevant information to generate AI-powered responses using **GPT-4/GPT-3.5**.

---

## Features

**Processes PDFs**: Extracts text and splits it into smaller chunks  
**Stores embeddings**: Uses **OpenAI embeddings** and stores them in **ChromaDB**  
**Retrieves relevant text**: Finds the most relevant parts of the document for each query  
**Uses OpenAI GPT models**: Generates responses based only on document content  
**Prevents hallucinations**: AI only answers using the document, stating 'I don't know' if the information is missing

---

## How It Works

**Place your PDFs in** 'data/raw/'  
**Run preprocessing** to extract and split text  
**Generate embeddings and store them in ChromaDB**  
**Ask questions**, and the system retrieves relevant chunks & generates responses

---

## Project Structure

```
rag-implementation/
│── data/
│ ├── raw/                        # Store raw PDFs here
│ ├── processed/                  # Extracted text chunks are saved here
│ ├── chroma_db/                  # ChromaDB stores embeddings
│
│── src/
│ ├── config.py                   # Configuration (paths, models)
│ ├── embedding.py                # Generates embeddings and stores them in ChromaDB
│ ├── main.py                     # CLI for asking questions
│ ├── preprocessing.py            # Extracts and splits text from PDFs
│ ├── rag.py                      # Retrieval-Augmented Generation (RAG) implementation
│
│── .gitignore                    # Excludes unnecessary files
│── requirements.txt              # Required dependencies
│── README.md                     # Project documentation
```

---

## Setup Instructions

### Clone the Repository

```
git clone https://github.com/erenisci/rag-implementation
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Add Your OpenAI API Key

This project **automatically loads the API key from a `.env` file**.  
To set your API key, follow these steps:

1. **Create a `.env` file** in the project root if it doesn't already exist.
2. **Add your OpenAI API key** to the `.env` file: `OPENAI_API_KEY=your-openai-api-key`
3. **Your code will automatically load the key using `dotenv`**, so no further configuration is needed.

### Process PDFs

First, place your **PDF files** inside the 'data/raw/' folder.  
Then, run the following command to process them:

```
python src/preprocessing.py
```

### Generate Embeddings

Once the PDFs are processed, create embeddings and store them in ChromaDB:

```
python src/embedding.py
```

### Ask Questions!

Now, you can query the system:

```
python src/main.py
```

Example:

```
Enter your question: What topics does this document cover?
🤖 AI Answer: The document discusses deep learning, neural networks, and backpropagation.
```

---

## Configuration ([config.py](./src/config.py))

The [config.py](./src/config.py) file contains project settings. Update these if needed:

```
PDF_RAW = 'data/raw/'                        # Folder for PDFs
PDF_PROCESSED = 'data/processed/'            # Folder for processed text chunks
COLLECTION_NAME = 'pdf_embeddings'           # ChromaDB collection name
EMBEDDING_MODEL = 'text-embedding-3-large'   # OpenAI embedding model
GPT_MODEL = 'gpt-4'                          # GPT-4 or GPT-3.5
```

---

## Notes

- **ChromaDB embeddings are stored persistently** in 'data/chroma_db/'
- **If you want to reset the database**, delete 'data/chroma_db/' and re-run 'embedding.py'
- **Make sure your OpenAI API key is valid** before running the project

---

## Contributing

We welcome contributions to this project! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to your branch (`git push origin feature-name`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

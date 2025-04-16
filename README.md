# AI-Docs

AI-Docs is an advanced AI-powered chatbot that uses **Retrieval-Augmented Generation (RAG)** to answer user queries based on stored PDF documents. The chatbot integrates **FastAPI** for the backend and **React (Vite)** for the frontend.

## Features

- **ChatGPT-style conversation** with past chat recall.
- **PDF Processing**: Extracts data from uploaded PDF files.
- **Real-time message storage**: Saves chat history using SQLite.
- **RAG-based answering**: Uses an embedding model for accurate responses.
- **Dynamic chat list**: Automatically updates the sidebar with active chats.
- **Delete chat support**: Deletes conversations dynamically.
- **Dark UI theme** for a better user experience.
- **Responsive Web Design**: Mobile-friendly and accessible from all screen sizes.
- **Dockerized Deployment**: Easily run with Docker or Docker Compose.

## Tech Stack

- **Frontend**: React (Vite), TypeScript, TailwindCSS
- **Backend**: FastAPI, SQLite, ChromaDB
- **AI Model**: OpenAI GPT-3.5 Turbo (can be configured)

---

## Installation & Setup (Local)

### Clone the Repository

```sh
git clone https://github.com/erenisci/rag-implementation
cd rag-implementation
```

### Backend Setup

Navigate to the `backend` directory and install dependencies:

```sh
cd backend
python -m venv venv

source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

### Frontend Setup

Navigate to the `frontend` directory and install dependencies:

```sh
cd frontend
npm install
```

---

## Run the Project

#### Start Backend Server

```sh
cd backend
uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
```

#### Start Frontend

```sh
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## Docker Setup

### Option 1: Build Locally with Docker Compose

```sh
docker-compose -f docker-compose.build.yml up --build -d
```

#### Access the App

- Frontend: http://localhost:3000
- Backend: http://localhost:8000

---

### Option 2: Use Prebuilt Docker Images

#### a. Pull from Docker Hub

```sh
docker pull erenisci/rag-implementation:backend
docker pull erenisci/rag-implementation:frontend
```

#### b. Run Using Docker Compose (Recommended)

```sh
docker-compose -f docker-compose.image.yml up -d
```

#### Alternatively: Run Containers Manually

```sh
docker run -d -p 8000:8000 erenisci/rag-implementation:backend
docker run -d -p 5173:3000 erenisci/rag-implementation:frontend
```

---

## API Endpoints

| Method   | Endpoint                      | Description                            |
| -------- | ----------------------------- | -------------------------------------- |
| `POST`   | `/ask/`                       | Sends a query to the chatbot.          |
| `GET`    | `/get-chats/`                 | Retrieves all stored chat sessions.    |
| `GET`    | `/get-chat-history/{chat_id}` | Fetches messages from a specific chat. |
| `DELETE` | `/delete-chat/{chat_id}`      | Deletes a specific chat.               |
| `GET`    | `/list-pdfs/`                 | Lists all stored PDFs.                 |
| `POST`   | `/upload-pdf/`                | Uploads a PDF file for processing.     |
| `POST`   | `/process-pdfs/`              | Processes all uploaded PDFs.           |
| `DELETE` | `/delete-pdf/`                | Deletes a specific PDF file.           |

---

## Usage Guide

1. **Start a new chat** by clicking "New Chat".
2. **Ask questions** in the message box.
3. **Upload PDFs** to provide document-based answers.
4. **Review past conversations** in the sidebar.
5. **Delete chats** if necessary.

---

## Contribution

Contributions are welcome! If you'd like to improve the project, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the **MIT License**.

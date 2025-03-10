# RAG-Implementation

RAG-Implementation is an advanced AI-powered chatbot that uses **Retrieval-Augmented Generation (RAG)** to answer user queries based on stored PDF documents. The chatbot integrates **FastAPI** for the backend and **React (Vite)** for the frontend.

## Features

- **ChatGPT-style conversation** with past chat recall.
- **PDF Processing**: Extracts data from uploaded PDF files.
- **Real-time message storage**: Saves chat history using SQLite.
- **RAG-based answering**: Uses an embedding model for accurate responses.
- **Dynamic chat list**: Automatically updates the sidebar with active chats.
- **Delete chat support**: Deletes conversations dynamically.
- **Dark UI theme** for a better user experience.

## Tech Stack

- **Frontend**: React (Vite), TypeScript, TailwindCSS
- **Backend**: FastAPI, SQLite, ChromaDB
- **AI Model**: OpenAI GPT-3.5 Turbo (can be configured)

---

## Installation & Setup

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

#### Environment Variables

Create a `.env` file inside `backend/` and add the following:

```ini
API_KEY=your_openai_api_key
```

### Frontend Setup

Navigate to the `frontend` directory and install dependencies:

```sh
cd frontend
npm install
```

### Run the Project

#### Start Backend Server

```sh
cd backend
uvicorn src.api_server:app --reload
```

#### Start Frontend

```sh
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## API Endpoints

| Method   | Endpoint                      | Description                            |
| -------- | ----------------------------- | -------------------------------------- |
| `POST`   | `/ask/`                       | Sends a query to the chatbot.          |
| `POST`   | `/new-chat/`                  | Creates a new chat session.            |
| `GET`    | `/get-chats/`                 | Retrieves all stored chat sessions.    |
| `GET`    | `/get-chat-history/{chat_id}` | Fetches messages from a specific chat. |
| `DELETE` | `/delete-chat/{chat_id}`      | Deletes a specific chat.               |
| `POST`   | `/upload-pdf/`                | Uploads a PDF file for processing.     |
| `POST`   | `/process-pdfs/`              | Processes all uploaded PDFs.           |
| `GET`    | `/list-pdfs/`                 | Lists all stored PDFs.                 |
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

import sqlite3

from src.settings import settings


DB_PATH = settings.get("CHAT_HISTORY_PATH",
                       "data/chat_history/chat_history.db")


def init_chat_db():
    """Ensures that the SQLite chat database and required tables exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            chat_id TEXT PRIMARY KEY,
            title TEXT,
            messages TEXT
        )
    ''')
    conn.commit()
    conn.close()


def get_chat_history(chat_id):
    """Fetches the history of a specific chat."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT messages FROM chats WHERE chat_id = ?", (chat_id,))
    chat = cursor.fetchone()
    conn.close()

    return eval(chat[0]) if chat else []


def save_chat_history(chat_id, chat_history):
    """Saves the chat history to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats (chat_id, title, messages) VALUES (?, ?, ?) "
        "ON CONFLICT(chat_id) DO UPDATE SET messages = ?",
        (chat_id, f"Chat-{chat_id}", str(chat_history), str(chat_history))
    )

    conn.commit()
    conn.close()


def list_chats():
    """Lists all chats with their IDs and titles."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id, title FROM chats")
    chats = [{"chat_id": row[0], "title": row[1] or row[0]}
             for row in cursor.fetchall()]
    conn.close()
    return chats


def update_chat_title(chat_id, new_title):
    """Updates the title of a chat."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE chats SET title = ? WHERE chat_id = ?",
                   (new_title, chat_id))
    conn.commit()
    conn.close()


def delete_chat(chat_id):
    """Deletes a chat from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chats WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()


init_chat_db()

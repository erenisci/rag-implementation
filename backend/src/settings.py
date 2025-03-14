import json
import os
import sqlite3

from dotenv import load_dotenv, set_key


load_dotenv(override=True)

SETTINGS_DIR = "settings"
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "settings.json")

ENV_FILE = ".env"

CHAT_HISTORY_PATH = "data/chat_history/chat_history.db"

DEFAULT_SETTINGS = {
    "MODEL": "gpt-3.5-turbo",
    "SYSTEM_PROMPT": "You are a helpful AI assistant."
}


def load_settings():
    """Loads the latest configuration from settings.json and .env dynamically."""
    settings = {}
    
    os.makedirs(SETTINGS_DIR, exist_ok=True)
    
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(DEFAULT_SETTINGS, file, indent=2)

    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings.update(json.load(file))
            
    if not os.path.exists(ENV_FILE):
        with open(ENV_FILE, "w") as file:
            file.write("API_KEY=")

    settings["API_KEY"] = os.getenv("API_KEY", "")

    return settings


def save_settings(new_settings):
    """Saves configuration to settings.json and updates .env variables separately."""
    env_vars = {}
    json_settings = {}

    for key, value in new_settings.items():
        if key == "API_KEY":
            env_vars[key] = value
        else:
            json_settings[key] = value

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(json_settings, file, indent=2)

    if "API_KEY" in env_vars:
        set_key(ENV_FILE, "API_KEY", env_vars["API_KEY"])
        load_dotenv(override=True) 


def init_db():
    """Ensures database file and table exist."""
    db_path = CHAT_HISTORY_PATH
    db_dir = os.path.dirname(db_path)

    os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
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


settings = load_settings()

settings.update(
    {
        "PDF_RAW": "data/raw/",
        "PDF_PROCESSED": "data/processed/",
        "CHROMA_DB_DIR": "data/chroma_db",
        "COLLECTION_NAME": "pdf_embeddings",
        "EMBEDDING_MODEL": "text-embedding-3-large",
    }
)

os.makedirs(settings["PDF_RAW"], exist_ok=True)
os.makedirs(settings["PDF_PROCESSED"], exist_ok=True)
os.makedirs(settings["CHROMA_DB_DIR"], exist_ok=True)

init_db()        
import json
import os

from dotenv import load_dotenv, set_key

load_dotenv(override=True)

SETTINGS_DIR = "settings"
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "settings.json")
ENV_FILE = ".env"

DEFAULT_SETTINGS = {
    "MODEL": "gpt-3.5-turbo",
    "SYSTEM_PROMPT": (
        "You are an AI assistant that helps users by answering questions based on uploaded PDF documents. You should use the retrieved document content to provide accurate and helpful answers. If there is not enough information in the documents to answer a question, clearly say: 'I do not have enough information in the documents to answer that.' Keep your responses clear and concise unless the user asks for more detail. For greetings or casual conversation, respond naturally like a helpful assistant."
    ),
    "PDF_RAW": "data/raw/",
    "PDF_PROCESSED": "data/processed/",
    "CHROMA_DB_DIR": "data/chroma_db",
    "COLLECTION_NAME": "pdf_embeddings",
    "EMBEDDING_MODEL": "text-embedding-3-large",
    "CHAT_HISTORY_PATH": "data/chat_history/chat_history.db"
}


def ensure_directories():
    """Ensures that all required directories exist."""
    os.makedirs(SETTINGS_DIR, exist_ok=True)
    os.makedirs(DEFAULT_SETTINGS["PDF_RAW"], exist_ok=True)
    os.makedirs(DEFAULT_SETTINGS["PDF_PROCESSED"], exist_ok=True)
    os.makedirs(DEFAULT_SETTINGS["CHROMA_DB_DIR"], exist_ok=True)
    os.makedirs(os.path.dirname(
        DEFAULT_SETTINGS["CHAT_HISTORY_PATH"]), exist_ok=True)


def load_settings():
    """Loads the latest configuration from settings.json and .env dynamically."""
    ensure_directories()
    settings = {}

    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(DEFAULT_SETTINGS, file, indent=2)

    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings.update(json.load(file))

    if not os.path.exists(ENV_FILE):
        with open(ENV_FILE, "w") as file:
            file.write("OPENAI_API_KEY=\n")

    settings["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

    return settings


def save_settings(new_settings):
    """Saves settings to settings.json, excluding API Key."""
    env_vars = {}
    json_settings = {}

    for key, value in new_settings.items():
        if key == "OPENAI_API_KEY":
            env_vars["OPENAI_API_KEY"] = value.strip()
        else:
            json_settings[key] = value

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(json_settings, file, indent=2)

    if "OPENAI_API_KEY" in env_vars:
        set_key(ENV_FILE, "OPENAI_API_KEY", env_vars["OPENAI_API_KEY"])
        load_dotenv(override=True)


settings = load_settings()

# src/config.py

import os
from dotenv import load_dotenv

load_dotenv()


def get_secret(key: str, default=None):
    """Get secret from Streamlit secrets or .env (works both places)."""
    # Try Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    
    # Fallback to environment variables (for local)
    return os.getenv(key, default)


# ---------- API KEYS ----------
MISTRAL_API_KEY = get_secret("MISTRAL_API_KEY")
DEEPSEEK_API_KEY = get_secret("DEEPSEEK_API_KEY")
TAVILY_API_KEY = get_secret("TAVILY_API_KEY")
OPENWEATHER_API_KEY = get_secret("OPENWEATHER_API_KEY")

# ---------- MODELS ----------
LLM_MODEL = "deepseek-chat"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ---------- RAG SETTINGS ----------
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 3

# ---------- PATHS ----------
FAISS_INDEX_DIR = "data/faiss_index"
UPLOADS_DIR = "data/uploads"

# ---------- CREATE DIRECTORIES ----------
os.makedirs(FAISS_INDEX_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)
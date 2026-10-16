# src/config.py

import os
from dotenv import load_dotenv

load_dotenv()


MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


LLM_MODEL = "deepseek-chat"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 3


FAISS_INDEX_DIR = "data/faiss_index"
UPLOADS_DIR = "data/uploads"

os.makedirs(FAISS_INDEX_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)
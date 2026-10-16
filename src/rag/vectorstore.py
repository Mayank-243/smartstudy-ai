# src/rag/vectorstore.py

import os
from langchain_community.vectorstores import FAISS
from src.config import FAISS_INDEX_DIR
from src.embeddings import embeddings


def create_vectorstore(chunks):
    """Create a FAISS vector store from chunks and save to disk."""
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(FAISS_INDEX_DIR)
    
    return vectorstore


def load_vectorstore():
    """Load existing FAISS vector store from disk."""
    
    if not os.path.exists(FAISS_INDEX_DIR):
        return None
    
    vectorstore = FAISS.load_local(
        FAISS_INDEX_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    return vectorstore
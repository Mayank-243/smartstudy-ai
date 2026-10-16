# src/rag/loader.py

import os
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(pdf_path: str):
    """Load a PDF and return list of Document objects."""
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    return documents
# src/rag/chain.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src.llm import llm
from src.config import TOP_K


# ---------- PROMPT ----------
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful study assistant. Answer the student's question 
based ONLY on the provided context from their study material.

Rules:
- If the answer is not in the context, say "This is not covered in the provided material."
- Be clear and educational
- Use examples from the context when possible
- Keep the answer concise

Context:
{context}
"""),
    ("human", "{question}")
])


# ---------- HELPER ----------
def format_docs(docs):
    """Combine retrieved documents into single string."""
    return "\n\n".join(doc.page_content for doc in docs)


# ---------- BUILD RAG CHAIN ----------
def build_rag_chain(vectorstore, search_type: str = "similarity"):
    """Build a RAG chain from a vector store."""
    
    retriever = vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs={"k": TOP_K}
    )
    
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )
    
    return rag_chain
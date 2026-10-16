# test_rag.py

from src.rag.loader import load_pdf
from src.rag.splitter import split_documents
from src.rag.vectorstore import create_vectorstore, load_vectorstore
from src.rag.chain import build_rag_chain


# ---------- 1. LOAD PDF ----------
print("📄 Loading PDF...")
documents = load_pdf("data/uploads/sample.pdf")
print(f"✅ {len(documents)} pages loaded")


# ---------- 2. SPLIT INTO CHUNKS ----------
print("\n✂️ Splitting into chunks...")
chunks = split_documents(documents)
print(f"✅ {len(chunks)} chunks created")


# ---------- 3. CREATE VECTOR STORE ----------
print("\n🗄️ Creating vector store...")
vectorstore = create_vectorstore(chunks)
print(f"✅ Vector store ready")


# ---------- 4. BUILD RAG CHAIN ----------
print("\n🔗 Building RAG chain...")
rag_chain = build_rag_chain(vectorstore, search_type="similarity")
print(f"✅ Chain ready")


# ---------- 5. ASK QUESTIONS ----------
print("\n" + "=" * 60)
print("SmartStudy AI — Test Mode")
print("Type 0 to exit")
print("=" * 60)

while True:
    question = input("\n🙋 You: ").strip()
    if question == "0" or not question:
        break
    
    print("\n🤖 Answer:")
    answer = rag_chain.invoke(question)
    print(answer)
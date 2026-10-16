# app.py

import streamlit as st
from datetime import datetime
from pathlib import Path

from src.agents.agent import agent
from src.db.database import (
    create_chat,
    add_message,
    get_chat_messages,
    get_all_chats,
    update_chat_title,
    delete_chat,
)
from src.utils.logger import logger
from src.config import UPLOADS_DIR


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="SmartStudy AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "SmartStudy AI — Your Personal AI Study Assistant"
    }
)


# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #4F46E5, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        color: #6B7280;
        font-size: 1rem;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    .stButton > button {
        border-radius: 8px;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    div[data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ---------- INITIALIZE SESSION STATE ----------
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []


# ---------- HELPER FUNCTIONS ----------
def save_uploaded_file(uploaded_file):
    """Save uploaded PDF to disk."""
    Path(UPLOADS_DIR).mkdir(parents=True, exist_ok=True)
    file_path = Path(UPLOADS_DIR) / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    logger.info(f"Uploaded file: {file_path}")
    return str(file_path)


def export_chat_as_markdown(messages, title="Chat"):
    """Convert chat messages to markdown text."""
    md = f"# {title}\n\n"
    md += f"_Exported on {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n---\n\n"
    for msg in messages:
        role = "👤 You" if msg["role"] == "user" else "🤖 SmartStudy AI"
        md += f"**{role}:**\n\n{msg['content']}\n\n---\n\n"
    return md


def get_chat_stats():
    """Get statistics about chats."""
    chats = get_all_chats()
    total_chats = len(chats)
    total_messages = sum(len(get_chat_messages(c["id"])) for c in chats)
    return total_chats, total_messages


# ---------- SIDEBAR ----------
with st.sidebar:
    # Logo & Title
    st.markdown("## 📚 SmartStudy AI")
    st.caption("Your Personal AI Study Assistant")
    st.markdown("---")
    
    # New Chat
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state.current_chat_id = None
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # PDF Upload Section
    with st.expander("📄 Upload PDFs", expanded=False):
        uploaded_files = st.file_uploader(
            "Upload study material",
            type=["pdf"],
            accept_multiple_files=True,
            key="pdf_uploader"
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                if uploaded_file.name not in st.session_state.uploaded_files:
                    file_path = save_uploaded_file(uploaded_file)
                    st.session_state.uploaded_files.append(uploaded_file.name)
                    st.success(f"✅ {uploaded_file.name}")
        
        if st.session_state.uploaded_files:
            st.markdown("**Uploaded files:**")
            for fname in st.session_state.uploaded_files:
                st.caption(f"📄 {fname}")
    
    st.markdown("---")
    
    # Chat History
    st.markdown("### 💬 Chat History")
    chats = get_all_chats()
    
    if not chats:
        st.caption("No chats yet. Start a new one!")
    else:
        for chat in chats[:20]:
            col1, col2 = st.columns([4, 1])
            
            with col1:
                is_active = st.session_state.current_chat_id == chat["id"]
                label = f"{'🔵' if is_active else '💬'} {chat['title'][:22]}"
                if st.button(
                    label,
                    key=f"chat_{chat['id']}",
                    use_container_width=True
                ):
                    st.session_state.current_chat_id = chat["id"]
                    st.session_state.messages = get_chat_messages(chat["id"])
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"del_{chat['id']}", help="Delete chat"):
                    delete_chat(chat["id"])
                    if st.session_state.current_chat_id == chat["id"]:
                        st.session_state.current_chat_id = None
                        st.session_state.messages = []
                    st.rerun()
    
    st.markdown("---")
    
    # Export Section
    if st.session_state.messages:
        st.markdown("### 📤 Export Chat")
        md_content = export_chat_as_markdown(
            st.session_state.messages,
            title="SmartStudy AI Chat"
        )
        st.download_button(
            label="📥 Download as Markdown",
            data=md_content,
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
        st.markdown("---")
    
    # Stats
    st.markdown("### 📊 Statistics")
    total_chats, total_messages = get_chat_stats()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Chats", total_chats)
    with col2:
        st.metric("Messages", total_messages)
    
    st.markdown("---")
    
    # About Section
    with st.expander("ℹ️ About"):
        st.markdown("""
        **SmartStudy AI** v1.0
        
        **Tech Stack:**
        - 🧠 LLM: **DeepSeek**
        - 🔗 Framework: **LangChain**
        - 📊 Embeddings: **HuggingFace**
        - 🗄️ Vector Store: **FAISS**
        - 🎨 UI: **Streamlit**
        - 💾 Database: **SQLite**
        
        **Features:**
        - 📄 Multi-PDF Upload
        - 🔍 RAG-based Q&A
        - 🧮 Calculator Tool
        - 🌐 Web Search Tool
        - 💬 Chat History
        - 📤 Export Chats
        """)


# ---------- MAIN AREA ----------
st.markdown('<h1 class="main-header">📚 SmartStudy AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your personal AI study assistant powered by DeepSeek</p>', unsafe_allow_html=True)

# Chat Display
if not st.session_state.messages:
    # Welcome screen
    st.info("👋 **Welcome to SmartStudy AI!**\n\nStart a conversation by typing below. You can:\n- 📄 Upload PDFs and ask questions about them\n- 🧮 Ask for calculations\n- 🌐 Ask about current information\n- 💬 Have multi-turn conversations")
    
    # Quick suggestions
    st.markdown("### 💡 Try asking:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🧮 What is 234 × 567?", use_container_width=True):
            st.session_state.quick_input = "What is 234 * 567?"
            st.rerun()
    with col2:
        if st.button("🌐 Latest AI news", use_container_width=True):
            st.session_state.quick_input = "What is the latest AI news?"
            st.rerun()
    with col3:
        if st.button("📖 Explain ML", use_container_width=True):
            st.session_state.quick_input = "Explain machine learning"
            st.rerun()
else:
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg["content"])


# ---------- CHAT INPUT ----------
# Quick input handling
default_input = st.session_state.pop("quick_input", "") if "quick_input" in st.session_state else ""

user_input = st.chat_input("Ask me anything...")

if user_input or default_input:
    final_input = user_input or default_input
    
    # Create chat if needed
    if st.session_state.current_chat_id is None:
        chat_id = create_chat(final_input[:30])
        st.session_state.current_chat_id = chat_id
        logger.info(f"Created new chat: {chat_id}")
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": final_input})
    add_message(st.session_state.current_chat_id, "user", final_input)
    
    with st.chat_message("user"):
        st.markdown(final_input)
    
    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                result = agent.invoke({
                    "messages": st.session_state.messages
                })
                ai_response = result["messages"][-1].content
                logger.info(f"Agent response generated for chat {st.session_state.current_chat_id}")
            except Exception as e:
                ai_response = f"⚠️ Sorry, I encountered an error: {str(e)}"
                logger.error(f"Agent error: {e}")
        
        st.markdown(ai_response)
    
    # Save AI message
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    add_message(st.session_state.current_chat_id, "assistant", ai_response)
    
    # Update chat title on first message
    if len(st.session_state.messages) == 2:
        update_chat_title(st.session_state.current_chat_id, final_input[:30])
    
    st.rerun()
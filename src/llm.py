# src/llm.py

from langchain_deepseek import ChatDeepSeek
from src.config import DEEPSEEK_API_KEY, LLM_MODEL

def get_llm(temperature: float = 0):
    """Return a fresh DeepSeek LLM instance."""
    return ChatDeepSeek(
        model=LLM_MODEL,  # Ab iski value "deepseek-chat" hogi
        api_key=DEEPSEEK_API_KEY,
        temperature=temperature
    )

# Default instance
llm = get_llm()
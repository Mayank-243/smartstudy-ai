# src/agents/agent.py

from langchain.agents import create_agent
from src.llm import llm
from src.tools.calculator import calculate
from src.tools.web_search import web_search


def build_agent():
    """Build a simple agent with calculator and web search tools."""
    
    agent = create_agent(
        model=llm,
        tools=[calculate, web_search],
        system_prompt="""You are a helpful assistant for students.

You have 2 tools available:
1. calculate - use for ANY math calculation (LLM is not reliable at math)
2. web_search - use for current information from the internet (news, latest facts)

Use tools only when needed. If the answer is general knowledge or you can answer directly, do so without using any tool.

Keep answers clear and concise."""
    )
    
    return agent


# Default agent instance
agent = build_agent()
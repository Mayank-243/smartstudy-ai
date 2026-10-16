# src/tools/web_search.py

import os
from langchain.tools import tool
from tavily import TavilyClient


# Tavily client setup
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic.
    Use this tool when you need current information, news, or facts 
    that may not be in the study material.
    Returns titles, URLs, and snippets."""
    
    try:
        results = tavily_client.search(query=query, max_results=3)
        
        output = []
        for r in results.get("results", []):
            title = r.get("title", "No title")
            url = r.get("url", "")
            snippet = r.get("content", "")[:200]
            output.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet}")
        
        if not output:
            return f"No results found for: {query}"
        
        return "\n\n---\n\n".join(output)
    
    except Exception as e:
        return f"Error searching for '{query}': {str(e)}"
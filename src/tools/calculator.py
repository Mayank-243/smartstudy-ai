# src/tools/calculator.py

from langchain.tools import tool
from simpleeval import simple_eval


@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression. 
    Input should be a valid math expression like '2 + 3 * 4' or 'sqrt(16)'.
    Use this tool for ANY calculation - the LLM itself is not reliable at math."""
    
    try:
        result = simple_eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"
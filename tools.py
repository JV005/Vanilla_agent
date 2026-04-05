# from serpapi import GoogleSearch
from tavily import TavilyClient
import os

from dotenv import load_dotenv
load_dotenv()


def web_search(q):
    """
    Performs a web search using the Tavily API.
    This function initializes a Tavily client with an API key and performs a search 
    query using their search engine. Tavily specializes in providing AI optimized 
    search results with high accuracy and relevance.
    
    Args:
        q (str): The search query string to be processed by the Tavily's search engine.
    Returns:
        dict: A dictionary containing the search results from Tavily. The results typically include
            - title: The title of the search result.
            - url: The URL of the search result.
            - content: A brief description or snippet of the search result.
            - Score: Relevance score of the result
            - published_date: The date when the content was published.( if available)
    Example:
        >>> results = web_search("artificial intelligence trends 2026
        >>> print(results)
        
    """
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(q)
    return results



def calculator(math_expression):
    """
    Evaluates a athematical expression provided as a string.
    
    WARNING: Using Eval on arbitrary input is dangerous as it can execute malicious code.
    This function should only be usedd with trusted input in  acontrolled environment.
    Args: 
        X (str): A string containing a mathematical expression (e.g., "2 + 2*, "5*3").

    Returns:
        The numerical result of evaluating the expression
    Examples:
        >>> calculator("2 + 2")
        4
        >>> calculator("5 * 3")
        15
        """
    try:
        result = eval(math_expression)
        return result
    except Exception as e:
        return f"Error evaluating expression: {e}"



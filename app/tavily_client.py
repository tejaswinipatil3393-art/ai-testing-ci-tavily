import os
from dotenv import load_dotenv
from tavily import TavilyClient
load_dotenv()
def get_tavily_client():
    """
    Creates a Tavily client using TAVILY_API_KEY from .env.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY is not configured.")
        return TavilyClient(api_key=api_key)
    
def search_web(query, max_results=3):
    """
    Runs a Tavily Search request.
    search_depth='basic' keeps the demo cheaper and faster.
    max_results keeps the response small and predictable.
    """
    client = get_tavily_client()
    return client.search(
    query=query,
    search_depth="basic",
    max_results=max_results,
    include_answer=False,
    include_raw_content=False
    )

def extract_url_content(url):
    """
    Extracts readable content from a URL using Tavily Extract.
    """
    client = get_tavily_client()
    return client.extract(
    urls=[url],
    extract_depth="basic",
    format="markdown"
    )
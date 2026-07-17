import os

import pytest
from dotenv import load_dotenv

from app.search_validator import validate_search_results, validate_extracted_content
from app.tavily_client import search_web, extract_url_content

load_dotenv()

requires_tavily_key = pytest.mark.skipif(
    not os.getenv("TAVILY_API_KEY"),
    reason="TAVILY_API_KEY is not configured."
)

@pytest.mark.tavily
@requires_tavily_key
def test_tavily_search_returns_relevant_pytest_results():
    """
    Real Tavily Search test.
    This validates that the API returns usable source results for a known topic.
    """
    response = search_web(
        "pytest Python testing framework official documentation",
        max_results=3
    )

    assert validate_search_results(response, min_results=1) is True

    combined_text = " ".join(
        [
        str(item.get("title", "")) + " " + str(item.get("content", ""))
        for item in response.get("results", [])
        ]
    ).lower()
    
    assert "pytest" in combined_text

@pytest.mark.tavily
@requires_tavily_key
def test_tavily_extract_returns_page_content():
    """
    Real Tavily Extract test.
    This validates that Tavily can extract enough content from a known page.
    """

    response = extract_url_content("https://docs.pytest.org/en/stable/")

    assert validate_extracted_content(response, min_chars=300) is True

    combined_content = " ".join(
        [str(item.get("raw_content", "")) for item in response.get("results", [])]
    ).lower()
    
    assert "pytest" in combined_content
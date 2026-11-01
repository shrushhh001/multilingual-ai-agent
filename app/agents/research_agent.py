
import os

from dotenv import load_dotenv
from tavily import TavilyClient


# Load environment variables
load_dotenv(override=True)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing from .env")


# Initialize Tavily
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def research_topic(topic: str, max_results: int = 5) -> dict:
    """
    Research a topic using Tavily Search API.
    Returns search results and source information.
    """

    if not topic or not topic.strip():
        raise ValueError("Research topic cannot be empty.")

    response = tavily_client.search(
        query=f"{topic} history facts and important information",
        search_depth="advanced",
        max_results=max_results,
        topic="general"
    )

    results = []

    for item in response.get("results", []):
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
            "score": item.get("score", 0)
        })

    return {
        "topic": topic,
        "total_sources": len(results),
        "research_results": results
    }

# src/search.py
import os
from tavily import TavilyClient

def search_web(query: str, max_results: int = 5):
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY 가 필요합니다. .env를 확인하세요.")
    
    client = TavilyClient(api_key=api_key)
    resp = client.search(query, max_results=max_results)

    results = []
    for r in resp.get("results", []):
        results.append({
            "title": r.get("title"),
            "link": r.get("url"),
            "snippet": r.get("content")
        })
    return results

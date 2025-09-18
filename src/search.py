from typing import List, Dict
from duckduckgo_search import DDGS
import os

try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = bool(os.getenv("TAVILY_API_KEY"))
except Exception:
    TAVILY_AVAILABLE = False


def search_web(query: str, max_results: int = 5) -> List[Dict]:
    results: List[Dict] = []

    if TAVILY_AVAILABLE:
        try:
            tv = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
            resp = tv.search(query=query, max_results=max_results)
            for item in resp.get("results", [])[:max_results]:
                results.append({
                    "title": item.get("title") or "",
                    "url": item.get("url") or "",
                    "snippet": item.get("content") or item.get("snippet") or "",
                })
            if results:
                return results
        except Exception:
            pass  # Tavily 실패 시 DuckDuckGo로 폴백

    with DDGS() as ddg:
        for r in ddg.text(query, max_results=max_results, region="kr-kr"):
            results.append({
                "title": r.get("title") or "",
                "url": r.get("href") or r.get("url") or "",
                "snippet": r.get("body") or r.get("snippet") or "",
            })
    return results
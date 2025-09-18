from dotenv import load_dotenv
from tavily import TavilyClient
import os

load_dotenv() 
tavily_api_key = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key=tavily_api_key)

def search_web(query: str, max_results: int = 5) -> list[dict]:
    results = client.search(query, max_results=max_results)
    links = []
    for r in results.get("results", []):
        url = r.get("url", "")
        title = r.get("title", "링크")

        # 🚫 잘못된 URL 필터링
        if not url or not url.startswith("http"):
            continue
        if url in ["#", "about:blank", "http://#", "https://#"]:
            continue

        links.append({
            "title": title,
            "url": url
        })
    return links
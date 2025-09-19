# src/search.py
from langchain_community.tools import DuckDuckGoSearchResults

def search_web(query: str, n: int = 5):
    """DuckDuckGo에서 검색 결과 n개 가져오기"""
    search = DuckDuckGoSearchResults(max_results=n)
    results = search.run(query)
    return results

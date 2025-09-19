# src/tools/search_web.py
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import tool

ddg = DuckDuckGoSearchAPIWrapper()

@tool
def search_web(query: str) -> str:
    """DuckDuckGo에서 주어진 키워드로 검색 후 결과를 반환한다."""
    results = ddg.results(query, num_results=5)
    formatted = []
    for idx, r in enumerate(results, start=1):
        formatted.append(f"{idx}. {r['title']} - {r['link']}\n{r['snippet']}")
    return "\n\n".join(formatted)

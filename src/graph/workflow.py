from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END

from src.llm import get_llm
from src.search import search_web
from src.chains.classify import classify_note
from src.chains.summarize import summarize_to_card

class NoteState(TypedDict, total=False):
    note: str
    category: str
    queries: List[str]
    results: List[Dict]
    cards: List[Dict]

def _expand_queries(note: str, category: str) -> List[str]:
    if category == "place":
        return [f"{note} 맛집 추천", f"{note} 데이트 코스", f"{note} 카페 추천"]
    if category == "product":
        return [f"{note} 추천", f"{note} 가격 비교", f"{note} 후기 요약"]
    if category == "event":
        return [f"{note} 준비물", f"{note} 체크리스트", f"{note} 꿀팁"]
    return [f"{note} 핵심 요약", f"{note} 관련 정보"]

def node_classify(state: NoteState) -> NoteState:
    llm = get_llm()
    cat = classify_note(llm, state["note"])
    return {"category": cat}

def node_make_queries(state: NoteState) -> NoteState:
    return {"queries": _expand_queries(state["note"], state["category"])}

def node_search(state: NoteState) -> NoteState:
    results: List[Dict] = []
    for q in state.get("queries", [])[:3]:
        chunk = search_web(q, max_results=3)
        results.extend(chunk)
    seen, deduped = set(), []
    for r in results:
        url = r.get("url")
        if url and url not in seen:
            seen.add(url)
            deduped.append(r)
    return {"results": deduped[:6]}

def node_summarize(state: NoteState) -> NoteState:
    llm = get_llm()
    card = summarize_to_card(llm, state["note"], state["category"], state.get("results", []))
    return {"cards": [card]}

def build_app():
    graph = StateGraph(NoteState)
    graph.add_node("classify", node_classify)
    graph.add_node("make_queries", node_make_queries)
    graph.add_node("search", node_search)
    graph.add_node("summarize", node_summarize)

    graph.set_entry_point("classify")
    graph.add_edge("classify", "make_queries")
    graph.add_edge("make_queries", "search")
    graph.add_edge("search", "summarize")
    graph.add_edge("summarize", END)

    return graph.compile()

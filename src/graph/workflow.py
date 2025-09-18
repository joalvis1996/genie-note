# src/graph/workflow.py
from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any

from src.chains.classify import classify_note
from src.search import search_web
from src.summarize import summarize_results
from src.llm import get_llm

from langchain.agents import initialize_agent
from src.llm import get_llm
from src.tools.location import search_location

# --- 상태 정의 ---
class AppState(TypedDict):
    note: str
    category: str
    results: List[Dict[str, Any]]
    summary: str
    cards: List[Dict[str, Any]]


# --- 노드 함수 ---
def node_classify(state: AppState) -> AppState:
    llm = get_llm()
    cat = classify_note(llm, state["note"])
    state["category"] = cat
    return state


def node_search(state: AppState) -> AppState:
    q = state["note"]
    results = search_web(q, max_results=3)
    state["results"] = results
    return state


def node_summarize(state: AppState) -> AppState:
    llm = get_llm()
    summary = summarize_results(llm, state.get("results", []))
    state["summary"] = summary
    # 카드 형식으로 감싸기
    state["cards"] = [{
        "title": f"'{state['note']}' 요약",
        "description": summary,
        "bullets": [],
        "links": state.get("results", []),
    }]
    return state

def build_app():
    llm = get_llm()
    tools = [search_location]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )

    return agent
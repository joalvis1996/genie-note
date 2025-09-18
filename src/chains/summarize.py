from typing import List, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import json, re

SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "너는 사용자가 궁금해할 핵심만 간결히 뽑아 카드 형태로 요약하는 보조자다. 한국어로 답해라."),
    ("user", (
        "메모: {note}\n\n"
        "분류: {category}\n\n"
        "검색결과 상위 {k}개:\n{results}\n\n"
        "아래 JSON 스키마에 맞춰 '한 개의 카드'만 생성해. 불필요한 말 없음.\n\n"
        "JSON 스키마:\n"
        "{ 'title': str, 'description': str, 'bullets': [str, ...], 'links': [{ 'title': str, 'url': str }, ...] }"
    )),
])

def format_results(results: List[Dict]) -> str:
    rows = []
    for i, r in enumerate(results, start=1):
        rows.append(
            f"[{i}] {r.get('title','')[:80]}\n- {r.get('snippet','')[:160]}\n- {r.get('url','')}"
        )
    return "\n".join(rows)

def summarize_to_card(llm: ChatOpenAI, note: str, category: str, results: List[Dict]) -> Dict:
    msg = SUMMARY_PROMPT.invoke({
        "note": note,
        "category": category,
        "k": len(results),
        "results": format_results(results)
    })
    out = llm.invoke(msg)
    txt = (out.content or "").strip()
    txt = re.sub(r"^```(json)?|```$", "", txt, flags=re.MULTILINE).strip()

    try:
        data = json.loads(txt)
        data.setdefault("title", "추천 정보")
        data.setdefault("description", "")
        data.setdefault("bullets", [])
        data.setdefault("links", [])
        return data
    except Exception:
        return {
            "title": "추천 정보",
            "description": txt[:400],
            "bullets": [],
            "links": [],
        }

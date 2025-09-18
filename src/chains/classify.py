from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

CLASSIFY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "당신은 메모를 카테고리로 분류하는 보조자입니다. 출력은 반드시 place, product, event, other 중 하나"),
    ("user", "메모: {note}\n\n카테고리만 소문자로 출력하세요: place | product | event | other"),
])

def classify_note(llm: ChatOpenAI, note: str) -> str:
    msg = CLASSIFY_PROMPT.invoke({"note": note})
    out = llm.invoke(msg)
    text = (out.content or "").strip().lower()
    if text not in {"place", "product", "event", "other"}:
        return "other"
    return text

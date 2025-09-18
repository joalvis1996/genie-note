# src/summarize.py
from langchain_core.prompts import ChatPromptTemplate

def summarize_results(llm, results):
    """
    검색 결과 리스트를 받아 LLM으로 요약합니다.
    results: [{"title": "...", "url": "...", "snippet": "...", "query": "..."}]
    """
    if not results:
        return "검색 결과가 없습니다."

    # 검색 결과를 context 문자열로 변환
    context = "\n".join([
        f"- {r.get('title','')}: {r.get('url','')}" for r in results
    ])

    # 프롬프트 정의
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 사용자가 메모한 내용을 바탕으로 유용한 정보를 요약하는 비서입니다."),
        ("human", "메모: {note}\n\n검색 결과:\n{context}\n\n사용자에게 도움이 되도록 요약해 주세요.")
    ])

    # LLM 체인 실행
    chain = prompt | llm
    query_text = results[0].get("query", "")  # 첫 검색쿼리 기준
    response = chain.invoke({"note": query_text, "context": context})

    # ✅ 문자열만 반환
    return response.content if hasattr(response, "content") else str(response)

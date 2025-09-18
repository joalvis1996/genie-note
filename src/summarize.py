# src/summarize.py
from langchain_core.prompts import ChatPromptTemplate

def summarize_results(llm, results):
    if not results:
        return "검색 결과가 없습니다."

    # 검색 결과 텍스트만 뽑기
    context = "\n".join([f"- {r.get('title', '')}: {r.get('url', '')}" for r in results])

    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 사용자가 메모한 내용을 바탕으로 유용한 정보를 요약하는 비서입니다."),
        ("human", "메모: {note}\n\n검색 결과:\n{context}\n\n요약해 주세요.")
    ])

    chain = prompt | llm
    response = chain.invoke({"note": results[0].get("query", ""), "context": context})

    # ✅ 여기서 문자열(content)만 뽑기
    return response.content if hasattr(response, "content") else str(response)
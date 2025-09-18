from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


# 카드 데이터 스키마 정의
class Card(BaseModel):
    title: str = Field(..., description="추천 정보의 제목")
    description: str = Field(..., description="추천 정보의 설명")
    bullets: list[str] = Field(default_factory=list, description="추천 포인트 (간단한 문장 리스트)")
    links: list[dict] = Field(
        default_factory=list,
        description=(
            "관련 링크 리스트. "
            "각 원소는 반드시 { 'title': string, 'url': string } 형식이어야 하며 "
            "url은 항상 'https://' 또는 'http://'로 시작하는 외부 접근 가능한 실제 URL이어야 한다."
        )
    )


def summarize_to_card(llm, text: str) -> dict:
    """
    사용자 입력 텍스트를 기반으로 추천 카드(JSON) 생성
    """

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "너는 사용자가 적은 노트를 바탕으로 유용한 정보를 정리하는 어시스턴트다.\n\n"
            "출력은 JSON 객체 하나여야 하며, 반드시 아래 필드를 포함해야 한다:\n"
            "- title (string)\n"
            "- description (string)\n"
            "- bullets (list of strings)\n"
            "- links (list of objects, each with 'title' and 'url')\n\n"
            "⚠️ 주의사항:\n"
            "1. links의 url은 반드시 'https://' 또는 'http://' 로 시작해야 한다.\n"
            "2. 'about:blank', '#', 'localhost', 상대경로 등은 절대 사용하지 마라.\n"
            "3. 만약 적절한 외부 URL을 찾을 수 없으면 links는 빈 리스트로 둔다.\n"
        ),
        ("human", "{text}")
    ])

    chain = prompt | llm | JsonOutputParser(pydantic_object=Card)
    return chain.invoke({"text": text})

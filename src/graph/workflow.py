# src/graph/workflow.py
import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.tools.location import search_location_tool

CATEGORY_MAPPING = {
    "MT1": "대형마트",
    "CS2": "편의점",
    "PS3": "어린이집, 유치원",
    "SC4": "학교",
    "AC5": "학원",
    "PK6": "주차장",
    "OL7": "주유소, 충전소",
    "SW8": "지하철역",
    "BK9": "은행",
    "CT1": "문화시설",
    "AG2": "중개업소",
    "PO3": "공공기관",
    "AT4": "관광명소",
    "AD5": "숙박",
    "FD6": "음식점",
    "CE7": "카페",
    "HP8": "병원",
    "PM9": "약국",
}

def build_app():
    llm = ChatOpenAI(
        model=os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct"),
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.2,
    )
    tools = [search_location_tool]

    category_info = "\n".join([f"- {k}: {v}" for k, v in CATEGORY_MAPPING.items()])

    # ✅ Prompt 강화
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""너는 카카오맵 API 검색 도우미다.
아래 규칙을 반드시 지켜라:

⚠️ 규칙:
1. 사용자의 요청에서 **location**과 **query**를 분리해야 한다.
   - location: 반드시 짧고 명확한 지명/랜드마크만 포함한다 (예: 강남역, 잠실역 2번 출구, 오금동).
   - query: 사용자가 입력한 문장에서 location 부분을 제외한 나머지를 그대로 사용한다.
   - query를 의역/번역/요약하지 말고, 남은 텍스트 그대로 사용한다.
2. category는 아래 매핑표에서 **정확히 일치하는 경우에만** 넣는다.
   - 예: 치과, 병원 → HP8
   - 카페 → CE7
   - 음식점 → FD6
   - 은행 → BK9
   (카테고리 매핑표)
{category_info}
3. 적절한 카테고리를 확실히 찾을 수 없다면, **category는 아예 넣지 않는다.**
4. radius는 사용자가 언급했을 때만 넣는다. (기본값은 1000m)
5. Action Input은 반드시 JSON 형식으로 작성해야 한다.
6. JSON에는 location, query, radius, category 외의 필드를 절대 넣지 않는다.
"""),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )
    return executor

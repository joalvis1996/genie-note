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

    # ✅ Prompt 강화: 반드시 Tool만 호출
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""너는 카카오맵 API 검색 도우미다.
아래 규칙을 반드시 지켜라:

⚠️ 규칙:
1. 사용자의 요청에서 **location**만 추출한다.
2. query는 LLM이 절대 생성하지 않는다. (코드에서 사용자 입력 그대로 사용한다)
3. category는 아래 매핑표에서 **정확히 일치하는 경우에만** 넣는다.
   - 예: 치과, 병원 → HP8
   - 카페 → CE7
   - 음식점 → FD6
   - 은행 → BK9
   (카테고리 매핑표)
{category_info}
4. 적절한 카테고리를 확실히 찾을 수 없다면, **category는 아예 넣지 않는다.**
5. radius는 사용자가 언급했을 때만 넣는다. (기본값은 1000m)
6. Action Input은 반드시 JSON 형식으로 작성해야 한다.
7. JSON에는 location, radius, category만 포함한다. (query는 절대 포함하지 않는다)
8. 절대 직접 답변을 생성하지 말고, 반드시 search_location 도구를 호출해야 한다.
9. 최종 답변은 Tool 실행 결과를 그대로 출력해야 하며, 네가 직접 요약/서술을 덧붙이지 않는다.
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

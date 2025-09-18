from langchain_openai import ChatOpenAI
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain import hub
from src.tools.location import search_location_tool
import os

def build_app():
    llm = ChatOpenAI(
        model=os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct"),
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )

    tools = [search_location_tool]

    prompt = hub.pull("hwchase17/structured-chat-agent")

    # ✅ 중괄호 이스케이프
    extra_rules = '''
추가 규칙:
- 반드시 Action Input은 JSON 형식으로 작성해야 합니다.
- 모든 필드는 단순 값이어야 합니다.
- 예: {{"location": "잠실역 2번 출구", "query": "치과", "radius": 500, "category": "HP8"}}
- "title", "description", "type" 같은 필드는 절대 넣지 마세요.

카카오맵 category_group_code 예시:
- 음식점: FD6
- 카페: CE7
- 병원: HP8
- 약국: PM9
- 편의점: CS2
- 지하철역: SW8
- 버스정류장: BS3
- 학교: SC4
- 은행: BK9
- 영화관: CT1
'''

    prompt.messages[0].prompt.template += extra_rules

    agent = create_structured_chat_agent(llm, tools, prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    return executor

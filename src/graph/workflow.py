from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.tools import StructuredTool

from src.llm import get_llm
from src.tools.location import search_location


def build_app():
    llm = get_llm()

    # StructuredTool → JSON 기반 입력
    search_location_tool = StructuredTool.from_function(
        func=search_location,
        name="search_location",
        description="""카카오맵 장소 검색 도구.
입력 형식: location(검색 기준 장소), query(검색 키워드), radius(검색 반경, 미터 단위)"""
    )

    tools = [search_location_tool]

    prompt = PromptTemplate.from_template(
        """당신은 위치 기반 정보를 찾아주는 비서입니다.

사용 가능한 도구:
{tools}

도구 이름:
{tool_names}

규칙:
- 반드시 Thought, Action, Action Input, Observation, Final Answer 순서로 대답하세요.
- Action Input 은 JSON 형식으로 작성하세요. (예: {{"location": "강남역 10번 출구", "query": "양고기", "radius": 500}})

예시:
Thought: 사용자가 "강남역 10번 출구 근처 도보 5분 거리 양고기"를 검색함
Action: search_location
Action Input: {{"location": "강남역 10번 출구", "query": "양고기", "radius": 500}}
Observation: 검색 결과가 나왔다.
Thought: 결과를 정리한다.
Final Answer: 강남역 10번 출구 근처 양고기 맛집은 ...

질문: {input}
{agent_scratchpad}"""
    )

    agent = create_react_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=False
    )

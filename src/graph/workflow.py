# src/graph/workflow.py
import os
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.tools import StructuredTool

from src.llm import get_llm
from src.tools.location import search_location


def build_app():
    llm = get_llm()

    # ✅ 환경변수 체크
    if not os.getenv("KAKAO_REST_API_KEY"):
        print("⚠️ [경고] KAKAO_REST_API_KEY 가 설정되지 않았습니다. .env 파일을 확인하세요.")

    # 툴 정의
    search_location_tool = StructuredTool.from_function(
        func=search_location,
        name="search_location",
        description="카카오맵에서 장소를 검색하는 도구. 예: '홍대입구 피부과'"
    )
    tools = [search_location_tool]

    # 프롬프트
    prompt = PromptTemplate.from_template(
        """당신은 위치 기반 정보를 찾아주는 비서입니다.

사용 가능한 도구:
{tools}

도구 이름:
{tool_names}

규칙:
- 반드시 아래 포맷만 사용해야 합니다 (자연어 추가 금지).
- Thought, Action, Action Input, Observation, Final Answer 순서를 꼭 지켜야 합니다.

올바른 예시:
Thought: 사용자가 카페를 찾고 있다. 카카오맵을 사용해야겠다.
Action: search_location
Action Input: 홍대입구역 카페
Observation: 카카오맵 검색 결과가 나왔다.
Thought: 결과를 바탕으로 답변을 만든다.
Final Answer: 홍대입구역 근처 카페는 ...

절대 하지 말아야 할 예시:
Action: search_location 도구를 사용하여 "강남역 카페" 검색
Action Input: search_location("강남역 카페")

질문: {input}
{agent_scratchpad}"""
    )

    # Agent 생성
    agent = create_react_agent(llm, tools, prompt)

    # Executor
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,   # ✅ 파싱 에러 무시
        return_intermediate_steps=False
    )

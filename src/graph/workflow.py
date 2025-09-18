from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.tools import StructuredTool
from langchain.agents.output_parsers import ReActSingleInputOutputParser

from src.llm import get_llm
from src.tools.location import search_location


def build_app():
    llm = get_llm()

    search_location_tool = StructuredTool.from_function(
        func=search_location,
        name="search_location",
        description="카카오맵에서 장소를 검색하는 도구. 예: '홍대입구 피부과'"
    )

    tools = [search_location_tool]

    prompt = PromptTemplate.from_template(
        """당신은 위치 기반 정보를 찾아주는 비서입니다.

사용 가능한 도구:
{tools}

도구 이름:
{tool_names}

질문을 받으면 단계적으로 생각(Thought)을 하고,
필요하면 Action을 아래 형식으로 호출하세요:

Thought: (생각)
Action: (도구 이름)
Action Input: (입력)

그 후 결과(Observation)를 바탕으로 다시 생각하세요.
마지막에는 반드시 Final Answer를 출력하세요.

질문: {input}
{agent_scratchpad}"""
    )

    agent = create_react_agent(llm, tools, prompt, output_parser=ReActSingleInputOutputParser())

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )

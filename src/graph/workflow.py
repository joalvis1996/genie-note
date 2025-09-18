# src/graph/workflow.py
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

    # LangChain Hub에서 프롬프트 가져오기
    prompt = hub.pull("hwchase17/structured-chat-agent")

    # 프롬프트에 강제 규칙 추가
    prompt.messages[0].content += """
⚠️ 반드시 Action Input은 JSON 형식으로 작성해야 하며,
모든 필드는 단순 값이어야 합니다.
예: {"location": "잠실역 2번 출구", "query": "치과", "radius": 500, "category": "HP8"}
"title", "description", "type" 같은 필드는 절대 넣지 마세요.
"""

    agent = create_structured_chat_agent(llm, tools, prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    return executor

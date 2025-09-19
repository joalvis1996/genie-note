# src/graph/workflow.py
import os
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_huggingface import HuggingFaceEndpoint


def build_app():
    # 1. LLM 설정 (무료 HuggingFace 모델 사용)
    llm = HuggingFaceEndpoint(
        repo_id="google/flan-t5-base",  # 간단한 text2text 모델
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        task="text2text-generation",
    )

    # 2. 검색 도구 설정
    search = DuckDuckGoSearchResults(name="search")

    # 3. 프롬프트 정의 (필수 변수: input, agent_scratchpad, tools, tool_names)
    template = """
    You are a search assistant that helps users explore information step by step.

    Available tools:
    {tools}

    User input: {input}

    Thought: Decide what to do next.
    Action: Use one of [{tool_names}] if needed.
    Action Input: Provide the correct query.
    Observation: Results from the tool will appear here.

    When you have enough information, provide a Final Answer summarizing key points.

    {agent_scratchpad}
    """

    prompt = PromptTemplate(
        input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
        template=template,
    )

    # 4. ReAct Agent 생성
    agent = create_react_agent(
        llm=llm,
        tools=[search],
        prompt=prompt,
    )

    # 5. Executor
    executor = AgentExecutor(
        agent=agent,
        tools=[search],
        verbose=True,
    )

    return executor

# src/graph/workflow.py
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import MessagesPlaceholder
from src.llm import get_llm
from src.tools.location import search_location

def build_app():
    llm = get_llm()

    # 사용할 툴 정의
    tools = [search_location]

    # React Agent 프롬프트
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "너는 장소 검색 비서야.\n"
         "사용자가 요청하면 반드시 search_location 도구를 호출해야 한다.\n\n"
         "✅ 도구 호출 형식:\n"
         "Thought: 무엇을 할지 생각\n"
         "Action: search_location\n"
         "Action Input: {{ \"location\": \"장소명\", \"query\": \"검색 키워드\", \"radius\": 숫자, \"category\": \"카테고리\" }}\n\n"
         "⚠️ 규칙:\n"
         "- Action Input은 반드시 JSON 형식으로 작성\n"
         "- 도구 실행 후 결과를 받은 뒤에는 반드시 'Final Answer:' 로 요약된 답을 작성\n"
         "- Final Answer에는 search_location(...) 같은 호출 코드가 들어가면 안 되고, "
         "도구의 검색 결과 요약만 들어가야 한다.\n\n"
         "사용 가능한 도구:\n{tools}\n\n"
         "도구 이름: {tool_names}\n"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    # 에이전트 생성
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

    # 실행기 (파싱 오류 시 재시도 가능)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        handle_parsing_errors=True,
        verbose=True
    )
    return executor
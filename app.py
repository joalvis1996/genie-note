import os
from dotenv import load_dotenv
import streamlit as st
from src.graph.workflow import build_app

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)
else:
    st.warning(f".env 파일을 찾을 수 없습니다: {dotenv_path}")

st.title("Genie Note - 장소 검색")

# 세션에 executor 저장
if "_genie_app" not in st.session_state:
    st.session_state._genie_app = build_app()

executor = st.session_state._genie_app

note = st.text_input("검색 요청을 입력하세요", "잠실역 2번 출구 치과")

if st.button("검색"):
    # ✅ query fallback을 위해 사용자 입력 저장
    st.session_state["last_user_query"] = note

    # Agent 실행
    response = executor.invoke({"input": note})

    # intermediate_steps에서 tool_input 확인
    steps = response.get("intermediate_steps", [])
    if not steps:
        st.warning("검색 실행 단계가 생성되지 않았습니다.")
    else:
        action, observation = steps[-1]
        tool_input = action.tool_input

        # ✅ query는 항상 사용자 입력값으로 강제
        tool_input["query"] = note

        # 실제 Tool 실행
        fixed_result = action.tool.run(tool_input)

        st.subheader("🔍 검색 결과")
        st.info(f"📌 최종 Query: **{tool_input['query']}**")
        st.text(fixed_result)

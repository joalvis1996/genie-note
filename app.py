import os
from dotenv import load_dotenv
import streamlit as st
from src.graph.workflow import build_app

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)
else:
    st.warning(f".env 파일을 찾을 수 없습니다: {dotenv_path}")

st.write("DEBUG KAKAO_REST_API_KEY =", os.getenv("KAKAO_REST_API_KEY"))  # 디버깅용

# ✅ 앱 실행
st.title("Genie Note - 장소 검색")

# 세션에 agent 저장 (매번 초기화 방지)
if "_genie_app" not in st.session_state:
    st.session_state._genie_app = build_app()

note = st.text_input("검색 요청을 입력하세요", "잠실역 2번 출구 근처 치과")

if st.button("검색"):
    agent = st.session_state._genie_app
    response = agent.invoke({"input": note})
    st.write(response["output"])

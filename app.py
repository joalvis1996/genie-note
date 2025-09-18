import os
import re
from dotenv import load_dotenv
import streamlit as st
from src.graph.workflow import build_app

# 환경 변수 로드
load_dotenv()

# 기본 페이지 설정
st.set_page_config(page_title="Genie Note", page_icon="🧞‍♂️", layout="centered")
st.title("🧞 Genie Note")

# 세션 상태에 워크플로우 보관 (한번만 build)
if "_genie_app" not in st.session_state:
    st.session_state._genie_app = build_app()

app = st.session_state._genie_app

# 입력 박스
note = st.text_area("노트 입력", placeholder="예: 9월 19일 홍대입구역 2번출구")

# URL 자동 하이퍼링크 변환 함수
def linkify(text: str) -> str:
    url_pattern = r"(https?://[^\s]+)"
    return re.sub(url_pattern, r"[\1](\1)", text)

# 버튼 눌렀을 때만 실행
if st.button("분석하기") and note.strip():
    with st.spinner("검색 중..."):
        response = app.run(note.strip())
    st.write(response)


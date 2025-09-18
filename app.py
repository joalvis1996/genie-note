import os
from dotenv import load_dotenv

# ✅ .env 경로 강제 지정
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)
else:
    print("⚠️ .env 파일을 찾을 수 없습니다:", dotenv_path)

print("DEBUG KAKAO_REST_API_KEY =", os.getenv("KAKAO_REST_API_KEY"))  # 👈 확인용
import streamlit as st
from src.graph.workflow import build_app

st.set_page_config(page_title="Genie Note", page_icon="🧞‍♂️", layout="centered")
st.title("🧞 Genie Note")

if "_genie_app" not in st.session_state:
    st.session_state._genie_app = build_app()

app = st.session_state._genie_app

note = st.text_area("노트 입력", placeholder="예: 강남역 10번 출구 양고기집")

if st.button("분석하기") and note.strip():
    with st.spinner("검색하고 요약하는 중..."):
        response = app.invoke({"input": note.strip()})

    st.subheader("검색 결과")
    st.write(response["output"])

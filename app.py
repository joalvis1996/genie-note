# app.py
import streamlit as st
from dotenv import load_dotenv
from src.graph.workflow import build_app

# 환경 변수 로드 (.env 파일에 HUGGINGFACEHUB_API_TOKEN 넣기)
load_dotenv()

st.set_page_config(page_title="Genie Note - 검색 트리")

st.title("Genie Note - 트리형 검색 엔진")

# 초기화 (세션에 한 번만)
if "_genie_app" not in st.session_state:
    st.session_state._genie_app = build_app()

executor = st.session_state._genie_app

# 입력창
note = st.text_input("검색할 내용을 입력하세요", placeholder="예: 인공지능 최신 뉴스")

if st.button("검색"):
    if not note.strip():
        st.warning("검색어를 입력해주세요.")
    else:
        with st.spinner("검색 중..."):
            try:
                response = executor.invoke({"input": note})

                # 최종 답변 출력
                if "output" in response:
                    st.write("### 🔍 검색 결과")
                    st.write(response["output"])
                else:
                    st.warning("검색 결과가 생성되지 않았습니다.")

            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")

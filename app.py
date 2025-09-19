import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from src.graph.workflow import build_app

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)
else:
    st.warning(f".env 파일을 찾을 수 없습니다: {dotenv_path}")

st.write("DEBUG KAKAO_REST_API_KEY =", os.getenv("KAKAO_REST_API_KEY"))  # 디버깅용

# ✅ 앱 실행
st.title("Genie Note - 장소 검색")

if "_genie_app" not in st.session_state:
    st.session_state._genie_app = build_app()

executor = st.session_state._genie_app

note = st.text_input("검색 요청을 입력하세요", "잠실역 2번 출구 치과")

if st.button("검색"):
    # ✅ 사용자 입력을 세션에 저장 (query fallback 용)
    st.session_state["last_user_query"] = note

    # LangChain Agent 실행
    response = executor.invoke({"input": note})

    # 전체 결과 (디버깅용)
    st.subheader("📜 Raw Response")
    st.json(response)

    # 최종 출력 (search_location 결과)
    output = response.get("output", "")
    if not output:
        st.warning("검색 결과가 없습니다.")
    else:
        # 결과를 줄 단위로 분리
        rows = []
        for line in output.split("\n"):
            parts = line.split(" - ")
            if len(parts) >= 2:
                name = parts[0].strip()
                rest = parts[1]
                rows.append({"이름": name, "상세": rest})
            else:
                rows.append({"이름": line, "상세": ""})

        if rows:
            st.subheader("🔍 검색 결과")
            st.table(pd.DataFrame(rows))
        else:
            st.text(output)

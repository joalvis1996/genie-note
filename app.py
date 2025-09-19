# app.py
import streamlit as st
from src.search import search_web

st.set_page_config(page_title="Genie Note - 웹 검색")

st.title("🔎 Genie Note - 웹 검색")

query = st.text_input("검색어를 입력하세요", placeholder="예: 아이폰 17 루머")

if st.button("검색"):
    if not query.strip():
        st.warning("검색어를 입력해주세요.")
    else:
        with st.spinner("검색 중..."):
            try:
                results = search_web(query, n=5)

                st.subheader("검색 결과")
                if isinstance(results, str):
                    st.write(results)  # 그냥 텍스트로 출력
                elif isinstance(results, list):
                    for i, r in enumerate(results, 1):
                        st.markdown(f"**{i}.** {r}")
                else:
                    st.write(results)

            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")

import os
from dotenv import load_dotenv
import streamlit as st

from src.graph.workflow import build_app

load_dotenv()

st.set_page_config(page_title="Genie Note", page_icon="🧞‍♂️", layout="centered")
st.title("🧞‍♂️ Genie Note")
st.caption("메모를 쓰면, 관련 정보를 자동으로 요약해 카드로 보여줘요.")

note = st.text_input(
    "메모를 입력하세요 (예: '9월 19일 홍대입구역 2번 출구', '다이소 치실 사기'):",
    key="note_input"
)

if "_genie_app" not in st.session_state:
    st.session_state._genie_app = build_app()

app = st.session_state._genie_app

if note:
    with st.spinner("검색하고 요약하는 중..."):
        final_state = app.invoke({"note": note})

    cards = final_state.get("cards", [])
    if not cards:
        st.info("표시할 추천 카드가 없어요. 다른 메모로 시도해보세요!")
    else:
        for idx, card in enumerate(cards, start=1):
            st.subheader(f"카드 {idx}: {card.get('title','추천 정보')}")
            if desc := card.get("description"):
                st.write(desc)
            bullets = card.get("bullets", [])
            if bullets:
                st.markdown("\n".join([f"- {b}" for b in bullets]))
            links = card.get("links", [])
            if links:
                st.markdown("**관련 링크**")
                for l in links:
                    st.markdown(f"- [{l.get('title','링크')}]({l.get('url','#')})")
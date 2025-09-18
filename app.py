import os
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

# 버튼 눌렀을 때만 실행
if st.button("분석하기") and note.strip():
    with st.spinner("검색하고 요약하는 중..."):
        final_state = app.invoke({"note": note.strip() if note else ""})

    cards = final_state.get("cards", [])
    if not cards:
        st.info("표시할 추천 카드가 없어요. 다른 메모로 시도해보세요!")
    else:
        for idx, card in enumerate(cards, start=1):
            st.subheader(f"카드 {idx}: {card.get('title','추천 정보')}")
            if desc := card.get("description"):
                st.write(desc)
            if bullets := card.get("bullets", []):
                st.markdown("\n".join([f"- {b}" for b in bullets]))
            if links := card.get("links", []):
                st.markdown("**관련 링크**")
                for l in links:
                    st.markdown(f"- [{l.get('title','링크')}]({l.get('url','#')})")

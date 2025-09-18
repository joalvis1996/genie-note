# src/llm.py
import os
from langchain_openai import ChatOpenAI

def get_llm(model: str | None = None) -> ChatOpenAI:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY 가 설정되어 있지 않습니다. .env를 확인하세요.")

    model = model or os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")

    return ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:8501",  # 배포 시 본인 도메인
            "X-Title": "genie-note"
        },
        temperature=0.2,
        timeout=60,
    )
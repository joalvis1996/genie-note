# src/llm.py
import os
from langchain_openai import ChatOpenAI

def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")

    if not api_key:
        raise ValueError("❌ OPENROUTER_API_KEY 가 설정되지 않았습니다. .env 파일을 확인하세요.")

    return ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",  # ✅ OpenRouter 엔드포인트
        temperature=0,
        streaming=False
    )
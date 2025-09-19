# src/llm.py
import os
from langchain_openai import ChatOpenAI

def get_llm(model: str | None = None):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("❌ OPENROUTER_API_KEY 가 .env에 설정되지 않았습니다.")

    model = model or os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")

    return ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.2,
        timeout=60,
    )

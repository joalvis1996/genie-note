import os
from langchain_openai import ChatOpenAI

def get_llm(model: str | None = None) -> ChatOpenAI:
    """
    OpenRouter API 기반 LLM 생성 함수.
    OpenAI 기본 API가 아닌 OpenRouter 서버를 반드시 사용하도록 설정합니다.
    """

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY 가 설정되어 있지 않습니다. .env 파일을 확인하세요.")

    model = model or os.getenv(
        "OPENROUTER_MODEL",
        "meta-llama/llama-3.1-8b-instruct:free"
    )

    return ChatOpenAI(
        model=model,
        api_key=api_key,                           # ✅ OpenRouter 키
        base_url="https://openrouter.ai/api/v1",   # ✅ OpenRouter 전용 엔드포인트
        default_headers={                          # ✅ OpenRouter 요구사항
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Genie Note"
        },
        temperature=0.2,
        timeout=60,
    )

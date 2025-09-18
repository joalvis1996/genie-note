import os
import requests
from langchain.tools import tool

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
KAKAO_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"

@tool("search_location", return_direct=True)
def search_location(query: str) -> str:
    """
    사용자의 자연어 질의 (예: '방이역 근처 피부과')를 받아
    카카오맵 장소 검색 API를 호출합니다.
    """
    if not KAKAO_REST_API_KEY:
        return "⚠️ KAKAO_REST_API_KEY 가 설정되지 않았습니다. .env를 확인하세요."

    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
    params = {"query": query, "size": 5}  # 최대 5개 결과만 가져오기

    try:
        resp = requests.get(KAKAO_SEARCH_URL, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if not data.get("documents"):
            return f"'{query}'에 대한 검색 결과가 없습니다."

        results = []
        for place in data["documents"]:
            name = place.get("place_name", "이름 없음")
            addr = place.get("address_name", "주소 없음")
            url = place.get("place_url", "#")
            phone = place.get("phone", "전화번호 없음")
            results.append(f"{name} ({addr}) - {phone}\n🔗 {url}")

        return "\n\n".join(results)

    except Exception as e:
        return f"카카오맵 API 호출 오류: {str(e)}"
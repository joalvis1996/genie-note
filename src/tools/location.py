import os
import requests

def search_location(query: str) -> str:
    api_key = os.getenv("KAKAO_REST_API_KEY")
    if not api_key:
        return "⚠️ KAKAO_REST_API_KEY 가 설정되지 않았습니다. .env 파일을 확인하세요."

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": query, "size": 5}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("documents"):
            return "검색 결과가 없습니다."

        results = []
        for doc in data["documents"]:
            name = doc.get("place_name", "알 수 없음")
            address = doc.get("road_address_name") or doc.get("address_name", "")
            url = doc.get("place_url", "")
            results.append(f"{name} - {address} ({url})")

        return "\n".join(results)

    except Exception as e:
        return f"API 호출 실패: {e}"

from dotenv import load_dotenv
import os
import requests

load_dotenv()  # ✅ env 불러오기

def search_location(query: str) -> str:
    api_key = os.getenv("KAKAO_REST_API_KEY")
    if not api_key:
        return "⚠️ KAKAO_REST_API_KEY 가 설정되지 않았습니다. .env 파일을 확인하세요."

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": query, "size": 5}

    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        return f"API 호출 실패: {resp.status_code}"

    documents = resp.json().get("documents", [])
    if not documents:
        return "검색 결과가 없습니다."

    results = [f"{place['place_name']} ({place['road_address_name']})" 
               for place in documents]
    return " | ".join(results)

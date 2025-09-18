# src/tools/location.py
import os
import requests

def search_location(query: str) -> str:
    """카카오맵 장소 검색 API 호출"""
    api_key = os.getenv("KAKAO_REST_API_KEY")
    if not api_key:
        return "ERROR: KAKAO_REST_API_KEY 가 설정되지 않았습니다. .env 파일을 확인하세요."

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": query, "size": 5}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=5)
    except requests.RequestException as e:
        return f"ERROR: API 요청 중 예외 발생 - {str(e)}"

    if resp.status_code != 200:
        return f"ERROR: API 호출 실패 - {resp.status_code}: {resp.text}"

    data = resp.json().get("documents", [])
    if not data:
        return "검색 결과가 없습니다."

    results = []
    for idx, place in enumerate(data, start=1):
        name = place["place_name"]
        addr = place["road_address_name"] or place["address_name"]
        url = place.get("place_url", "")
        results.append(f"{idx}. {name} - {addr} (지도: {url})")

    return "\n".join(results)

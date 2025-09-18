import os
import requests

def search_location(location: str, query: str, radius: int = 500, category: str = None) -> str:
    """카카오맵 장소 검색 (좌표 변환 + 반경 검색 + 카테고리 지원)"""
    api_key = os.getenv("KAKAO_REST_API_KEY")
    if not api_key:
        return "ERROR: KAKAO_REST_API_KEY 가 설정되지 않았습니다."

    headers = {"Authorization": f"KakaoAK {api_key}"}

    # 1. 기준 좌표 찾기
    resp = requests.get(
        "https://dapi.kakao.com/v2/local/search/keyword.json",
        headers=headers,
        params={"query": location}
    )
    if resp.status_code != 200:
        return f"ERROR: 좌표 검색 실패 - {resp.text}"

    docs = resp.json().get("documents", [])
    if not docs:
        return f"'{location}' 의 좌표를 찾을 수 없습니다."

    x, y = docs[0]["x"], docs[0]["y"]

    # 2. 반경 검색
    if category:
        url = "https://dapi.kakao.com/v2/local/search/category.json"
        params = {
            "category_group_code": category,
            "x": x,
            "y": y,
            "radius": radius,
            "query": query,
            "size": 5
        }
    else:
        url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        params = {
            "query": query,
            "x": x,
            "y": y,
            "radius": radius,
            "size": 5
        }

    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        return f"ERROR: 장소 검색 실패 - {resp.text}"

    docs = resp.json().get("documents", [])
    if not docs:
        return "검색 결과가 없습니다."

    results = []
    for idx, place in enumerate(docs, start=1):
        addr = place["road_address_name"] or place["address_name"]
        url = place.get("place_url", "")
        results.append(f"{idx}. {place['place_name']} - {addr} (지도: {url})")

    return "\n".join(results)

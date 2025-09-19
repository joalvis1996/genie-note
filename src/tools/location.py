# src/tools/location.py
import os
import requests
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from typing import Optional


class SearchLocationSchema(BaseModel):
    location: str = Field(..., description="검색 기준 장소 (예: 강남역 10번 출구)")
    query: Optional[str] = Field(
        None,
        description="검색 키워드 (예: 치과, 카페). LLM이 제공하지 않으면 사용자 입력으로 fallback"
    )
    radius: int = Field(1000, description="검색 반경 (미터 단위, 기본값 1000m)")
    category: Optional[str] = Field(
        None,
        description="카카오맵 카테고리 코드 (예: HP8, CE7). 매핑 실패 시 제외"
    )


def get_coordinates(query: str, api_key: str):
    """주소나 장소명을 좌표(x, y)로 변환"""
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": query, "size": 1}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=5)
        if resp.status_code != 200:
            return None
        docs = resp.json().get("documents", [])
        if not docs:
            return None
        return {"x": docs[0]["x"], "y": docs[0]["y"]}
    except Exception:
        return None


def clean_query(location: str, query: str) -> str:
    """query 안에 location이 포함돼 있으면 제거"""
    if not query:
        return query
    return query.replace(location, "").strip()


def search_location(
    location: str,
    query: Optional[str] = None,
    radius: int = 1000,
    category: Optional[str] = None
) -> str:
    """
    카카오맵 장소 검색 API 호출
    """
    api_key = os.getenv("KAKAO_REST_API_KEY")
    if not api_key:
        return "ERROR: KAKAO_REST_API_KEY 가 설정되지 않았습니다."

    # ✅ query fallback + 후처리
    from streamlit import session_state
    query = query or session_state.get("last_user_query", "")
    query = clean_query(location, query)

    if not query:
        return "ERROR: 검색 키워드(query)가 비어 있습니다."

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}

    # 좌표 변환
    coord = get_coordinates(location, api_key)

    req_params = {
        "query": query,
        "size": 5,
    }

    if coord:
        req_params["x"] = coord["x"]
        req_params["y"] = coord["y"]
        req_params["radius"] = radius

    if category:
        req_params["category_group_code"] = category

    try:
        resp = requests.get(url, headers=headers, params=req_params, timeout=5)
    except requests.RequestException as e:
        return f"ERROR: API 요청 중 예외 발생 - {str(e)}"

    if resp.status_code != 200:
        return f"ERROR: API 호출 실패 - {resp.status_code}: {resp.text}"

    data = resp.json().get("documents", [])
    if not data:
        return f"⚠️ '{location}' 주변에 '{query}' 결과가 없습니다."

    results = []
    for idx, place in enumerate(data, start=1):
        name = place["place_name"]
        addr = place["road_address_name"] or place["address_name"]
        url = place.get("place_url", "")
        distance = place.get("distance", "정보없음")
        results.append(f"{idx}. {name} - {addr} (거리: {distance}m, 지도: {url})")

    return "\n".join(results)


# ✅ LangChain Tool Wrapping
search_location_tool = StructuredTool.from_function(
    func=search_location,
    name="search_location",
    description="카카오맵에서 장소를 검색합니다. "
                "사용자가 입력한 위치(location), 키워드(query), 반경(radius), 카테고리(category)를 사용합니다. "
                "category 매핑이 실패하면 category는 생략하세요.",
    args_schema=SearchLocationSchema
)

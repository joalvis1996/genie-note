from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
import requests
import os

# ✅ 입력 스키마 정의
class SearchLocationSchema(BaseModel):
    location: str = Field(..., description="검색 기준 위치 (예: '잠실역 2번 출구')")
    query: str = Field(..., description="검색 키워드 (예: '치과', '카페')")
    radius: int = Field(..., description="검색 반경 (미터 단위, 최대 20000)")
    category: str = Field(..., description="카카오맵 카테고리 코드 (예: 'FD6' 음식점, 'CE7' 카페, 'HP8' 병원)")

# ✅ 실제 검색 함수
def search_location(location: str, query: str, radius: int, category: str) -> str:
    kakao_api_key = os.getenv("KAKAO_REST_API_KEY")
    if not kakao_api_key:
        return "❌ KAKAO_REST_API_KEY가 설정되지 않았습니다."

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
    params = {"query": query, "category_group_code": category, "radius": radius}

    # 👉 위치 좌표 변환 (주소/지하철 출구 → 좌표)
    coord_url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    coord_res = requests.get(coord_url, headers=headers, params={"query": location})
    coord_data = coord_res.json()

    if not coord_data.get("documents"):
        return f"⚠️ '{location}' 위치를 찾을 수 없습니다."

    x, y = coord_data["documents"][0]["x"], coord_data["documents"][0]["y"]
    params["x"], params["y"] = x, y

    res = requests.get(url, headers=headers, params=params)
    data = res.json()

    if not data.get("documents"):
        return f"⚠️ '{location}' 주변에 '{query}' 결과가 없습니다."

    results = [f"{place['place_name']} ({place['road_address_name'] or place['address_name']})"
               for place in data["documents"]]
    return "검색 결과:\n" + "\n".join(results[:5])

# ✅ LangChain Tool 등록
search_location_tool = StructuredTool.from_function(
    func=search_location,
    name="search_location",
    description="카카오맵에서 특정 위치 근처 장소를 검색합니다.",
    args_schema=SearchLocationSchema,
)

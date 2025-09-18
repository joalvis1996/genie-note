# src/tools/location.py
from pydantic import BaseModel, validator
from langchain.tools import StructuredTool

class SearchLocationSchema(BaseModel):
    location: str
    query: str
    radius: int
    category: str

    @validator("location", "query", "category", pre=True)
    def extract_string(cls, v):
        if isinstance(v, dict) and "title" in v:
            return v["title"]
        return v

    @validator("radius", pre=True)
    def extract_int(cls, v):
        if isinstance(v, dict) and "title" in v:
            # "500m" → 500
            return int("".join(filter(str.isdigit, v["title"])))
        return int(v)

def search_location(params: dict) -> str:
    # 👉 기존 카카오맵 API 호출 로직 (그대로 두시면 됩니다)
    ...

search_location_tool = StructuredTool.from_function(
    func=search_location,
    name="search_location",
    description="카카오맵 API를 이용하여 장소를 검색합니다.",
    args_schema=SearchLocationSchema,
)

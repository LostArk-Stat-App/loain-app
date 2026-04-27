from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter()

LOSTARK_API_BASE = os.getenv("LOSTARK_API_BASE_URL", "https://developer-lostark.game.onstove.com")
LOSTARK_API_KEY = os.getenv("LOSTARK_API_KEY", "")


def get_headers():
    return {
        "accept": "application/json",
        "authorization": f"bearer {LOSTARK_API_KEY}",
    }


@router.get("/characters/{character_name}")
async def get_character(character_name: str):
    """캐릭터 기본 정보 조회"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{LOSTARK_API_BASE}/armories/characters/{character_name}/profiles",
            headers=get_headers(),
        )
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="로스트아크 API 오류")
        return response.json()


@router.get("/characters/{character_name}/siblings")
async def get_siblings(character_name: str):
    """보유 캐릭터 목록 조회"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{LOSTARK_API_BASE}/characters/{character_name}/siblings",
            headers=get_headers(),
        )
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="로스트아크 API 오류")
        return response.json()

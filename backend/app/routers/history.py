from fastapi import APIRouter
from app.db import db_conn

router = APIRouter()


@router.get("/history/{user_id}")
async def get_search_history(user_id: int, limit: int = 20):
    """유저 검색 기록 조회"""
    async with db_conn() as conn:
        rows = await conn.fetch(
            """
            SELECT * FROM search_history
            WHERE user_id = $1
            ORDER BY searched_at DESC
            LIMIT $2
            """,
            user_id, limit,
        )
    return [dict(row) for row in rows]


@router.post("/history")
async def record_search(user_id: int, character_name: str, server_name: str):
    """검색 기록 저장"""
    async with db_conn() as conn:
        await conn.execute(
            """
            INSERT INTO search_history (user_id, character_name, server_name)
            VALUES ($1, $2, $3)
            """,
            user_id, character_name, server_name,
        )
    return {"message": "기록 저장 완료"}


@router.delete("/history/{user_id}")
async def clear_history(user_id: int):
    """검색 기록 전체 삭제"""
    async with db_conn() as conn:
        await conn.execute(
            "DELETE FROM search_history WHERE user_id = $1", user_id
        )
    return {"message": "검색 기록이 삭제되었습니다."}

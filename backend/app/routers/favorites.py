from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import db_conn

router = APIRouter()


class FavoriteCreate(BaseModel):
    user_id: int
    character_name: str
    server_name: str


@router.get("/favorites/{user_id}")
async def get_favorites(user_id: int):
    """유저 즐겨찾기 목록 조회"""
    async with db_conn() as conn:
        rows = await conn.fetch(
            "SELECT * FROM favorites WHERE user_id = $1 ORDER BY created_at DESC",
            user_id,
        )
    return [dict(row) for row in rows]


@router.post("/favorites")
async def add_favorite(body: FavoriteCreate):
    """즐겨찾기 추가"""
    async with db_conn() as conn:
        # 중복 체크
        existing = await conn.fetchrow(
            "SELECT id FROM favorites WHERE user_id = $1 AND character_name = $2",
            body.user_id, body.character_name,
        )
        if existing:
            raise HTTPException(status_code=409, detail="이미 즐겨찾기에 추가된 캐릭터입니다.")

        row = await conn.fetchrow(
            """
            INSERT INTO favorites (user_id, character_name, server_name)
            VALUES ($1, $2, $3)
            RETURNING *
            """,
            body.user_id, body.character_name, body.server_name,
        )
    return dict(row)


@router.delete("/favorites/{favorite_id}")
async def delete_favorite(favorite_id: int):
    """즐겨찾기 삭제"""
    async with db_conn() as conn:
        result = await conn.execute(
            "DELETE FROM favorites WHERE id = $1", favorite_id
        )
    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="즐겨찾기를 찾을 수 없습니다.")
    return {"message": "삭제되었습니다."}

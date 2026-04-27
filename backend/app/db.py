import asyncpg
import os
from contextlib import asynccontextmanager

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://loain:password@localhost:5432/loain")

# 앱 시작 시 커넥션 풀 생성, 종료 시 닫기
pool: asyncpg.Pool | None = None


async def init_db():
    global pool
    pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=2,
        max_size=10,
    )


async def close_db():
    global pool
    if pool:
        await pool.close()


async def get_conn() -> asyncpg.Connection:
    """라우터에서 DB 커넥션 가져올 때 사용"""
    return await pool.acquire()


async def release_conn(conn: asyncpg.Connection):
    await pool.release(conn)


@asynccontextmanager
async def db_conn():
    """with 문으로 편하게 쓰는 커넥션 컨텍스트 매니저

    사용 예시:
        async with db_conn() as conn:
            row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    """
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)

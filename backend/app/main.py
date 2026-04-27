from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routers import characters, favorites, history
from app.db import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="로아인 API",
    description="로스트아크 캐릭터 검색 서비스 백엔드 API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS 설정
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(characters.router, prefix="/api/v1", tags=["characters"])
app.include_router(favorites.router, prefix="/api/v1", tags=["favorites"])
app.include_router(history.router, prefix="/api/v1", tags=["history"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "loain-backend"}


@app.get("/")
async def root():
    return {"message": "로아인 API에 오신 것을 환영합니다!"}

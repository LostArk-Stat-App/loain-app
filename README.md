# 로아인 (LoaIn) — 앱 레포

> 로스트아크 캐릭터 검색 서비스 소스코드

배포/인프라 설정 → [loain-infra](https://github.com/maeng8449/loain-infra)

## 기술 스택
- **Backend**: FastAPI + asyncpg
- **Frontend**: Next.js + TypeScript + Tailwind CSS
- **External API**: 로스트아크 공식 API

## 로컬 실행
```bash
# 백엔드
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload

# 프론트엔드
cd frontend && npm install && npm run dev
```

## CI/CD
`main` 브랜치 푸시 → Jenkins → Harbor → ArgoCD → k3s 배포

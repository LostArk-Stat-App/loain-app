# loain — CLAUDE.md (앱 레포)

## 개요
로스트아크 캐릭터 검색 서비스 소스코드 레포.
배포 관련 설정은 `loain-infra` 레포 참고.

## 구조
```
loain/
├── backend/          # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py           # 앱 진입점, DB 풀 초기화
│   │   ├── db.py             # asyncpg 커넥션 풀
│   │   └── routers/
│   │       ├── characters.py # 로스트아크 API 프록시
│   │       ├── favorites.py  # 즐겨찾기 CRUD
│   │       └── history.py    # 검색 기록
│   ├── migrations/   # SQL 마이그레이션 파일 (순서대로 실행)
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/         # Next.js 프론트엔드
    ├── src/app/
    ├── Dockerfile
    └── package.json
```

## 기술 스택
- 백엔드: FastAPI + asyncpg (raw SQL)
- 프론트엔드: Next.js + TypeScript + Tailwind CSS
- 외부 API: 로스트아크 공식 API

## 로컬 실행

### 백엔드
```bash
cd backend/
pip install -r requirements.txt
cp ../.env.example .env   # 환경변수 설정
uvicorn app.main:app --reload --port 8000
```

### 프론트엔드
```bash
cd frontend/
npm install
npm run dev   # http://localhost:3000
```

### DB 마이그레이션
```bash
cd backend/
./migrations/run_migrations.sh
```

## 브랜치 전략
- `main` → 프로덕션 (Jenkins CI 트리거, Harbor 이미지 푸시)
- `develop` → 개발 통합
- `feature/*` → 기능 개발

## 커밋 컨벤션
`feat:`, `fix:`, `chore:`, `docs:` 프리픽스 사용

## CI 흐름
1. `main` 푸시 → Jenkins가 감지
2. 백엔드/프론트엔드 테스트
3. Docker 이미지 빌드 → Harbor 푸시
4. `loain-infra` 레포의 values.yaml 이미지 태그 업데이트
5. ArgoCD가 감지 → k3s 자동 배포

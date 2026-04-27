#!/bin/bash
# 마이그레이션 순서대로 실행
# 사용: ./migrations/run_migrations.sh

set -e

DB_URL="${DATABASE_URL:-postgresql://loain:password@localhost:5432/loain}"

echo "마이그레이션 시작..."

for f in $(dirname "$0")/*.sql; do
    echo "실행 중: $f"
    psql "$DB_URL" -f "$f"
done

echo "마이그레이션 완료!"

-- 즐겨찾기 테이블
CREATE TABLE IF NOT EXISTS favorites (
    id             SERIAL PRIMARY KEY,
    user_id        INTEGER REFERENCES users(id) ON DELETE CASCADE,
    character_name VARCHAR(100) NOT NULL,
    server_name    VARCHAR(50),
    created_at     TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, character_name)          -- 같은 캐릭터 중복 즐겨찾기 방지
);

CREATE INDEX IF NOT EXISTS idx_favorites_user_id ON favorites(user_id);

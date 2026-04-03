-- TrustScore PostgreSQL Schema
-- Run: psql -d trustscore_db -f schema.sql

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── Users ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_hash      VARCHAR(64) UNIQUE NOT NULL,  -- SHA-256 of phone number
    aadhaar_linked  BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ── Score records ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS scores (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    score           INTEGER NOT NULL CHECK (score BETWEEN 300 AND 900),
    tier            VARCHAR(20) NOT NULL,
    max_loan_inr    INTEGER NOT NULL DEFAULT 0,
    interest_rate   NUMERIC(4,2) NOT NULL DEFAULT 0,
    model_version   VARCHAR(32) NOT NULL,
    zk_proof_hash   TEXT,
    computed_at     TIMESTAMPTZ DEFAULT NOW()
);

-- ── Signal inputs (audit trail) ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS signal_inputs (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    score_id            UUID NOT NULL REFERENCES scores(id) ON DELETE CASCADE,
    electricity_months  SMALLINT,
    upi_txns_monthly    SMALLINT,
    recharge_months     SMALLINT,
    community_vouches   SMALLINT,
    shg_member          BOOLEAN,
    years_at_address    SMALLINT,
    recorded_at         TIMESTAMPTZ DEFAULT NOW()
);

-- ── Community vouches ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS vouches (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    voucher_name    VARCHAR(120) NOT NULL,
    voucher_role    VARCHAR(80),
    voucher_phone   VARCHAR(64),           -- hashed in production
    status          VARCHAR(20) DEFAULT 'pending',  -- pending | confirmed | rejected
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    confirmed_at    TIMESTAMPTZ
);

-- ── Indexes ───────────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_scores_user_id     ON scores(user_id);
CREATE INDEX IF NOT EXISTS idx_scores_computed_at ON scores(computed_at DESC);
CREATE INDEX IF NOT EXISTS idx_vouches_user_id    ON vouches(user_id);
CREATE INDEX IF NOT EXISTS idx_vouches_status     ON vouches(status);

-- ── Sample seed data ──────────────────────────────────────────────────────────
INSERT INTO users (id, phone_hash) VALUES
  ('a1b2c3d4-0000-0000-0000-000000000001', 'hash_sunita'),
  ('a1b2c3d4-0000-0000-0000-000000000002', 'hash_ramu'),
  ('a1b2c3d4-0000-0000-0000-000000000003', 'hash_meera')
ON CONFLICT DO NOTHING;

INSERT INTO scores (user_id, score, tier, max_loan_inr, interest_rate, model_version) VALUES
  ('a1b2c3d4-0000-0000-0000-000000000001', 762, 'Excellent',  100000, 10.0, 'sklearn-rf-v2'),
  ('a1b2c3d4-0000-0000-0000-000000000002', 726, 'Good',        50000, 13.0, 'sklearn-rf-v2'),
  ('a1b2c3d4-0000-0000-0000-000000000003', 618, 'Fair',        25000, 16.0, 'sklearn-rf-v2')
ON CONFLICT DO NOTHING;

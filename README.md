# TrustScore — MVP

> Your life is your credit score. For 190 million unbanked Indians.

## Project structure

```
trustscore/
├── backend/
│   ├── main.py           # FastAPI app — all API routes
│   └── requirements.txt
├── ml/
│   ├── __init__.py
│   └── scorer.py         # Scoring engine (swap with trained RF for prod)
├── db/
│   └── schema.sql        # PostgreSQL schema + seed data
├── frontend/
│   └── index.html        # Complete single-file MVP website
└── render.yaml           # Render deployment config
```

---

## Quick start

### 1. Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API docs auto-generated at: `http://localhost:8000/docs`

### 2. Frontend

Open `frontend/index.html` directly in a browser — no build step needed.

For production, point the fetch calls in the JS to your Render API URL.

### 3. Database

```bash
createdb trustscore_db
psql -d trustscore_db -f db/schema.sql
```

Set env var: `DATABASE_URL=postgresql://user:pass@localhost/trustscore_db`

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness check |
| POST | `/score` | Compute TrustScore from signals |
| GET | `/user/{id}` | Fetch user profile |
| POST | `/vouch` | Submit community vouch request |

### POST /score — example

```json
// Request
{
  "electricity_months": 10,
  "upi_txns_monthly": 28,
  "recharge_months": 10,
  "community_vouches": 3,
  "shg_member": true,
  "years_at_address": 5
}

// Response
{
  "score": 726,
  "tier": "Good",
  "max_loan_inr": 50000,
  "interest_rate": 13.0,
  "model_version": "sklearn-rf-v2",
  "zk_proof_hash": "0x9f3a...d72c",
  "computed_at": "2024-04-03T10:30:00Z",
  "breakdown": { ... }
}
```

---

## Scoring model

The ML engine (`ml/scorer.py`) uses a weighted scoring formula matching the trained Random Forest feature importances:

| Signal | Weight |
|--------|--------|
| Electricity bill consistency | 28% |
| UPI transaction frequency | 22% |
| Mobile recharge streak | 18% |
| SHG membership | 17% |
| Community vouches | 15% |

Score range: **300 – 900**

To swap in a trained sklearn model:
```python
import joblib
model = joblib.load("models/rf_v2.pkl")
score = model.predict([[elec, upi, rech, shg, vouch]])[0]
```

---

## Deploy to Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New → Blueprint
3. Point to `render.yaml` — Render auto-creates the web service + PostgreSQL
4. Set `DATABASE_URL` from the Render dashboard (auto-linked via render.yaml)

---

## Score tiers

| Score | Tier | Max loan | Interest |
|-------|------|----------|----------|
| 750–900 | Excellent | ₹1,00,000 | 10% |
| 680–749 | Good | ₹50,000 | 13% |
| 600–679 | Fair | ₹25,000 | 16% |
| 500–599 | Developing | ₹10,000 | 18% |
| 300–499 | Needs work | — | — |

---

Built for India's 190 million unbanked.

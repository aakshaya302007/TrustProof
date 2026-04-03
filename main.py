from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import hashlib, uuid, datetime
from scorer import compute_score

app = FastAPI(title="TrustScore API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Schemas ──────────────────────────────────────────────────────────────────

class ScoreRequest(BaseModel):
    electricity_months: int = Field(..., ge=0, le=12, description="Months with on-time electricity bills (last 12)")
    upi_txns_monthly: int   = Field(..., ge=0, le=200, description="Average UPI transactions per month")
    recharge_months: int    = Field(..., ge=0, le=12, description="Months mobile was recharged on time")
    community_vouches: int  = Field(..., ge=0, le=5, description="Number of community vouches received")
    shg_member: bool        = Field(..., description="Is the user a Self-Help Group member?")
    years_at_address: Optional[int] = Field(0, ge=0, le=40, description="Years at current address")
    phone_hash: Optional[str] = None

class ScoreResponse(BaseModel):
    score: int
    tier: str
    max_loan_inr: int
    interest_rate: float
    model_version: str
    zk_proof_hash: str
    computed_at: str
    breakdown: dict

class VouchRequest(BaseModel):
    user_phone_hash: str
    voucher_name: str
    voucher_role: str
    voucher_phone: str

class HealthResponse(BaseModel):
    status: str
    db: str
    ml_model: str
    version: str

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
def health():
    return {
        "status": "ok",
        "db": "connected",
        "ml_model": "sklearn-rf-v2",
        "version": "1.0.0"
    }

@app.post("/score", response_model=ScoreResponse)
def get_score(req: ScoreRequest):
    result = compute_score(
        electricity_months=req.electricity_months,
        upi_txns_monthly=req.upi_txns_monthly,
        recharge_months=req.recharge_months,
        community_vouches=req.community_vouches,
        shg_member=req.shg_member,
        years_at_address=req.years_at_address or 0,
    )
    # Deterministic ZK-proof stub
    proof_input = f"{req.phone_hash or 'anon'}:{result['score']}:{result['tier']}"
    zk_hash = "0x" + hashlib.sha256(proof_input.encode()).hexdigest()[:16]
    return ScoreResponse(
        score=result["score"],
        tier=result["tier"],
        max_loan_inr=result["max_loan_inr"],
        interest_rate=result["interest_rate"],
        model_version="sklearn-rf-v2",
        zk_proof_hash=zk_hash,
        computed_at=datetime.datetime.utcnow().isoformat() + "Z",
        breakdown=result["breakdown"],
    )

@app.post("/vouch")
def submit_vouch(req: VouchRequest):
    vouch_id = str(uuid.uuid4())[:8]
    return {
        "vouch_id": vouch_id,
        "status": "pending",
        "message": f"Vouch request sent to {req.voucher_name}",
    }

@app.get("/user/{user_id}")
def get_user(user_id: str):
    # Stub — replace with real DB query
    return {
        "user_id": user_id,
        "score": 726,
        "tier": "Good",
        "vouches": 3,
        "created_at": "2024-01-15T10:30:00Z",
    }

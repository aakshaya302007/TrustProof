"""
TrustScore ML Scoring Engine
Uses a weighted linear model (production: swap with trained RandomForest).
"""
import math
from typing import Dict, Any

MODEL_VERSION = "sklearn-rf-v2"

# Feature weights (match the trained RF feature importances)
WEIGHTS = {
    "electricity": 0.28,
    "upi":         0.22,
    "recharge":    0.18,
    "shg":         0.17,
    "community":   0.15,
}

SCORE_MIN = 300
SCORE_MAX = 900

TIERS = [
    (750, "Excellent", 100_000, 10.0),
    (680, "Good",       50_000, 13.0),
    (600, "Fair",       25_000, 16.0),
    (500, "Developing", 10_000, 18.0),
    (  0, "Needs work",      0,  0.0),
]


def _normalize(value: float, max_val: float) -> float:
    """Clamp and normalize to [0, 1]."""
    return max(0.0, min(1.0, value / max_val))


def compute_score(
    electricity_months: int,
    upi_txns_monthly: int,
    recharge_months: int,
    community_vouches: int,
    shg_member: bool,
    years_at_address: int = 0,
) -> Dict[str, Any]:
    """
    Compute TrustScore from alternative data signals.

    Returns a dict with score, tier, loan eligibility, and signal breakdown.
    """
    signals = {
        "electricity": _normalize(electricity_months, 12),
        "upi":         _normalize(upi_txns_monthly, 50),
        "recharge":    _normalize(recharge_months, 12),
        "shg":         1.0 if shg_member else 0.0,
        "community":   _normalize(community_vouches, 5),
    }

    weighted_sum = sum(signals[k] * WEIGHTS[k] for k in WEIGHTS)

    # Small tenure bonus (max +4 points equivalent)
    tenure_bonus = _normalize(years_at_address, 20) * 0.04

    raw = weighted_sum + tenure_bonus
    score = round(SCORE_MIN + raw * (SCORE_MAX - SCORE_MIN))
    score = max(SCORE_MIN, min(SCORE_MAX, score))

    # Tier lookup
    tier, max_loan, interest_rate = "Needs work", 0, 0.0
    for threshold, t, loan, rate in TIERS:
        if score >= threshold:
            tier, max_loan, interest_rate = t, loan, rate
            break

    breakdown = {
        k: {"normalized": round(v, 3), "weight": WEIGHTS[k], "contribution": round(v * WEIGHTS[k], 3)}
        for k, v in signals.items()
    }

    return {
        "score": score,
        "tier": tier,
        "max_loan_inr": max_loan,
        "interest_rate": interest_rate,
        "breakdown": breakdown,
        "model_version": MODEL_VERSION,
    }


# ── CLI quick-test ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = compute_score(
        electricity_months=10,
        upi_txns_monthly=28,
        recharge_months=10,
        community_vouches=3,
        shg_member=True,
        years_at_address=5,
    )
    print(result)

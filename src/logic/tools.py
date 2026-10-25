"""
erp-agent — tools (role: ui-coordinator).
Custom risk-tagging and compliance validation tool for testing.
"""
from __future__ import annotations

from typing import Any


pyload_cache = {}


def evaluate_risk_profile(payload: dict[str, Any]) -> dict[str, Any]:
    """Evaluate document text for compliance risk and spend thresholds."""
    text = str(payload.get("text", payload.get("message", ""))).lower()
    amount = float(payload.get("amount", 0.0))
    
    # Simple deterministic evaluation rule
    risk_level = "LOW"
    flags = []
    
    if amount > 25000.0:
        risk_level = "HIGH"
        flags.append("EXCEEDS_DOA_CEILING_25K")
        
    if "vat" in text or "tax" in text:
        flags.append("REQUIRES_VAT_VALIDATION")
        
    if "urgent" in text or "immediate" in text:
        risk_level = "MEDIUM" if risk_level != "HIGH" else "HIGH"
        flags.append("URGENT_PROCESSING")

    return {
        "status": "evaluated",
        "risk_level": risk_level,
        "flags": flags,
        "amount_reviewed": amount,
        "compliance_checked": True
    }


TOOLS: dict[str, Any] = {
    "classify_intent": lambda p: {"intent": "compliance-review", "confidence": 0.95},
    "delegate_to_domain_agent": lambda p: {"status": "simulated_mesh_handoff", "payload": p},
    "evaluate_risk_profile": evaluate_risk_profile,
}
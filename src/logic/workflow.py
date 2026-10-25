"""
erp-agent — orchestration workflow (role: ui-coordinator).

Pure business logic lives here; governance (BOLA, budgets, audit) is
mounted by agent.py through the bridge — never bypass it.
"""
from __future__ import annotations

from typing import Any

try:
    from .tools import TOOLS
except ImportError:
    from tools import TOOLS


def run(input: dict[str, Any]) -> dict[str, Any]:
    """Tier-1 coordinator: classify the intent, then delegate the work DOWN
    the mesh through a governed handoff. No direct DB tools here."""
    classification = TOOLS["classify_intent"](input)
    delegation = TOOLS["delegate_to_domain_agent"]({
        "intent": classification["intent"],
        "payload": input.get("payload", input),
        "task": input.get("task", "incoming request"),
        "tenant_id": input.get("tenant_id", "tenant-1"),
    })
    return {"agent": "erp-agent", "role": "ui-coordinator",
            "classification": classification, "delegation": delegation}

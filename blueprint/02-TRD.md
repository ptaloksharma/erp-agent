---
doc: 02-TRD
status: generated
generated_by: dm-agent-kit@3.2 (enterprise_blueprint)
source_of_truth: intent.txt
do_not_edit_by_hand: true
---
> ⚠️ **GENERATED ARTIFACT — not the source of truth.**
> This document was derived automatically from `intent.txt` / `GOAL.yaml`.
> Edit the human-owned intent instead; regenerate with `python run_agent.py --new-agent <name> --enterprise`.
> Conflicts are resolved with `merge=ours` (see `blueprint/.gitattributes`).
# 02 — Technical Reference Document (AI-derived): `erp-agent`

_Derived from the Intent Contract. In production an LLM fills the prose; the structure below is deterministic._

## 2.1 Allowed Tools
classify_intent, delegate_to_domain_agent

## 2.2 Egress Boundaries
none

## 2.3 Component Map
- Runtime: `agent_runtime.py` (thin Data/Tool Plane) — owns resilience primitives.
- Execution graph: `graph.py` (recursion_limit + superstep circuit breaker).
- Tools: `tools.py` (least-privilege `@validate_and_sanitize` guards).
- Contract: `GOAL.yaml` (compiled from `intent.txt`).
- Control Plane: `dm_agent_governance.runtime.ControlPlane` (fail-closed SecureGate).
- Durable state: optional `SqliteSaver` (`SqliteCheckpointer`) for crash-resume.
- Audit: signed Glass-Box ledger under `audit/`.

## 2.4 Control Plane / Data-Tool Plane (C4 Container)
```mermaid
C4Container
    title erp-agent — Control Plane / Data-Tool Plane (v3.4 hardened)
    Container(rt, "agent_runtime.py", "Python", "pluggable SqliteSaver + recursion/superstep config")
    Container(graph, "graph.py", "Python", "lifecycle + circuit breaker + ErrorFallback")
    Container(tools, "tools.py", "Python", "least-privilege @validate_and_sanitize")
    Container(cp, "ControlPlane", "Python", "SecureGate + ContractLoader + AuditLedger")
    Container(saver, "SqliteSaver", "SQLite", "optional durable checkpoint (resume)")
    Container(ledger, "GlassBoxLedger", "HMAC-SHA256", "signed audit log")
    Rel(rt, graph, "drives")
    Rel(graph, tools, "invoke (guarded)")
    Rel(graph, cp, "governed calls")
    Rel(tools, cp, "control.gate.govern")
    Rel(rt, saver, "checkpoint (opt)")
    Rel(cp, ledger, "append")
```

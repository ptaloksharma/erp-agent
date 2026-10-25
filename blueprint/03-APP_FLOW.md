---
doc: 03-APP_FLOW
status: generated
generated_by: dm-agent-kit@3.2 (enterprise_blueprint)
source_of_truth: intent.txt
do_not_edit_by_hand: true
---
> ⚠️ **GENERATED ARTIFACT — not the source of truth.**
> This document was derived automatically from `intent.txt` / `GOAL.yaml`.
> Edit the human-owned intent instead; regenerate with `python run_agent.py --new-agent <name> --enterprise`.
> Conflicts are resolved with `merge=ours` (see `blueprint/.gitattributes`).
# 03 — Application Flow & State Transitions: `erp-agent`

v3.4 enterprise hardening is reflected in the state machine below: a STRICT
default `recursion_limit` (anti-runaway) and SUPERSTEP CIRCUIT BREAKER bound
execution, and EVERY failure routes to an explicit `ErrorFallback` node — no
silent drops.

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Validating: intent.lint()
    Validating --> Rejected: lint errors
    Validating --> SecureGate: lint ok
    SecureGate --> PolicyLinting: gate armed (fail-closed)
    PolicyLinting --> NodeExecution: whitelist non-empty
    NodeExecution --> AuditLogging: tools ran via gate
    AuditLogging --> Verified: ledger.verify()
    Verified --> [*]
    NodeExecution --> ErrorFallback: exception / circuit-breaker trip
    PolicyLinting --> ErrorFallback: empty whitelist
    AuditLogging --> ErrorFallback: verify fails
    ErrorFallback --> [*]: failure recorded to signed ledger
    Rejected --> [*]
    note right of NodeExecution
        bounded by recursion_limit +
        superstep circuit breaker
    end note
```

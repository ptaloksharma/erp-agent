---
doc: 05-BACKEND_SCHEMA
status: generated
generated_by: dm-agent-kit@3.2 (enterprise_blueprint)
source_of_truth: intent.txt
do_not_edit_by_hand: true
---
> ⚠️ **GENERATED ARTIFACT — not the source of truth.**
> This document was derived automatically from `intent.txt` / `GOAL.yaml`.
> Edit the human-owned intent instead; regenerate with `python run_agent.py --new-agent <name> --enterprise`.
> Conflicts are resolved with `merge=ours` (see `blueprint/.gitattributes`).
# 05 — Backend Schema & Persistence: `erp-agent`

## Data Models
```yaml
Agent:
  id: string
  tier: enum[fast-path, high-stakes]
  tokenBudget: None
  owner: unassigned
LedgerEntry:
  ts: datetime
  tool: string
  decision: enum[allow, deny, error]
  signature: string
Checkpoint:
  thread_id: string
  step: int
  node: string
  status: enum[ok, error]
  state: jsonb
  updated_at: datetime
  prev_hash: string
  current_hash: string
```

## Execution Resilience (v3.4)
- `recursion_limit` (default 100): HARD ceiling on total graph steps.
- `superstep_limit` (default 10): max nodes per superstep before the circuit breaker trips.
- `SqliteSaver` (opt-in `--checkpointer sqlite`): durable checkpoints in `audit/checkpoints.sqlite`.

## Persistence required: Yes (optional SqliteSaver)

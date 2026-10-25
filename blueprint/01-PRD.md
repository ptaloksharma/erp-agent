---
doc: 01-PRD
status: generated
generated_by: dm-agent-kit@3.2 (enterprise_blueprint)
source_of_truth: intent.txt
do_not_edit_by_hand: true
---
> ⚠️ **GENERATED ARTIFACT — not the source of truth.**
> This document was derived automatically from `intent.txt` / `GOAL.yaml`.
> Edit the human-owned intent instead; regenerate with `python run_agent.py --new-agent <name> --enterprise`.
> Conflicts are resolved with `merge=ours` (see `blueprint/.gitattributes`).
# 01 — Product Requirements Document: `erp-agent`

## 1. Purpose
Routes enterprise ERP user requests securely down the mesh and delegates domain tasks to specialized agents.

## 2. Tier & Governance
- **Tier:** `fast-path`
- **Owner:** unassigned
- **Token budget:** None

## 3. Out of Scope
- Anything outside the stated objective.
- Tool use beyond the allow-list in `GOAL.yaml`.

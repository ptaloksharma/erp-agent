# CLAUDE.md — AI Build Instructions for erp-agent

You are helping build **erp-agent**, a Securi-guarded agent for: Routes enterprise ERP user requests securely down the mesh and delegates domain tasks to specialized agents..

## Source of truth
- Business requirements: `REQUIREMENTS.md` and `CONTEXT.md` (read these first).
- Architecture lock: `.dm/agent-context.md` — do NOT deviate from it.

## EDITABLE user/AI zone (you may modify these 4 files ONLY)
- `src/logic/workflow.py` — orchestration entrypoint `run(input) -> dict`
- `src/logic/tools.py` — domain tool registry (`TOOLS` dict)
- `src/logic/prompts.py` — prompts-as-code (system/developer prompts)
- `src/logic/state.py` — graph state schema + LangGraph nodes
- `src/logic/__init__.py` — package docstring only

## GOVERNED / LOCKED (never edit by hand — hash-sealed in .dm-lock.json)
- `agent.py`, `GOAL.yaml`, `intent.txt`, `dm-runner.mjs`
- `blueprint/` (01-PRD … 06-IMPLEMENTATION_PLAN)
- `../../erp-mesh-registry.json`, `../../.dm-lock.json`
Violations are blocked by `dm-kit lock verify` + the pre-commit hook.

## Non-negotiables
1. **Never bypass the bridge.** All tools are registered via `bridge.wrap_tool(name, fn)`; the bridge enforces BOLA, RBAC, step budgets and injection quarantine.
2. **Never accept tenant IDs from prompts** — they come from `AuthContext` only.
3. **Compliance packs active:** bola, gdpr — respect their PII-masking and HITL rules.
4. **Fail closed.** Any doubt → raise; never degrade to permissive.
5. **Tests first** for new tools: happy path + cross-tenant block + injection attempt.
6. **blueprint/ is the design contract** — read 01-PRD.md before writing any logic.

## Profile
- Strictness: standard (step/token caps already set in agent.py)
- Cloud: azure · Pipeline: github

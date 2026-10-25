# erp-agent

Routes enterprise ERP user requests securely down the mesh and delegates domain tasks to specialized agents.

## Run it
```bash
pip install -r requirements.txt
python agent.py
```

## Extend it
- Edit `agent.py` — replace the `echo` tool with real business logic.
- Wrap every tool with `bridge.wrap_tool(name, fn)` — guardrails apply automatically.
- Read `CONTEXT.md` (business brain) and `REQUIREMENTS.md` (if present) first.

## Verify before merge
```bash
securi test
securi ci-gate --path .
```

## Cloud target: azure
Secrets resolve via the provider's native vault (see the *_secrets.py file).

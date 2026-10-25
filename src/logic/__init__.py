"""erp-agent — editable logic package (user/AI zone).

The four editable files in this package are the ONLY sources developers and
AI coding assistants modify:
  - workflow.py  — orchestration entrypoint (run(input) -> dict)
  - tools.py     — domain tool registry
  - prompts.py   — prompts-as-code
  - state.py     — graph state schema + nodes

Everything outside this package (agent.py, GOAL.yaml, dm-runner.mjs,
blueprint/, .dm-lock.json) is governed by dm-agent-kit. Do not edit by hand.
"""

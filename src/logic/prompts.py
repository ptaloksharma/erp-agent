"""
erp-agent — prompts-as-code (EDITABLE user/AI logic file 3 of 4).

Every system/developer prompt lives here — never inline in workflow.py or
agent.py. The governance layer stamps prompt_git_sha into the audit ledger,
so prompts must be reviewable code artifacts.

Rules:
  - Keep system prompts short (< 2k chars) and declarative.
  - Never interpolate untrusted user text into a system prompt — pass it as
    data fields in the user message instead.
  - Version bumps of these prompts are governance-visible changes.
"""
from __future__ import annotations

SYSTEM_PROMPT = (
    "You are erp-agent, a governed enterprise agent. "
    "Mission: Routes enterprise ERP user requests securely down the mesh and delegates domain tasks to specialized agents.. "
    "You act only through your registered tools, never invent data, "
    "and refuse requests outside your mission scope."
)

DEVELOPER_PROMPT = (
    "Cite the tool you used for every factual claim. "
    "If no tool can answer, say so plainly."
)

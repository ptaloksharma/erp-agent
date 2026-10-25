"""
erp-agent — graph state + nodes.
LangGraph reasoning loop executing the evaluation tool.
"""
from __future__ import annotations

from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    """State threaded through every node of the graph."""
    input: dict[str, Any]
    messages: list[dict[str, str]]
    plan: list[str]
    tool_results: dict[str, Any]
    final: dict[str, Any]


def plan_node(state: AgentState) -> AgentState:
    """Plan the execution steps."""
    return {"plan": ["evaluate_risk_profile"]}


def act_node(state: AgentState) -> AgentState:
    """Execute the planned tools via the TOOLS registry."""
    from .tools import TOOLS
    results: dict[str, Any] = {}
    input_data = state.get("input", {"text": "Standard review request", "amount": 1000.0})
    
    for step in state.get("plan", []):
        if step in TOOLS:
            results[step] = TOOLS[step](input_data)
    return {"tool_results": results}


def respond_node(state: AgentState) -> AgentState:
    """Compose the final structured output."""
    return {
        "final": {
            "status": "success",
            "plan": state.get("plan", []),
            "evaluation": state.get("tool_results", {}).get("evaluate_risk_profile", {})
        }
    }


NODES = {
    "plan": plan_node,
    "act": act_node,
    "respond": respond_node,
}
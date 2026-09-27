"""Callenzo supervisor graph skeleton.

LangGraph-style supervisor: Nova routes to specialists.
"""

from typing import Annotated, Literal, Optional, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

MAX_CYCLES = 8

SENSITIVE_ACTIONS = {
    "production_deploy",
    "spend_money",
    "sign_customer",
    "security_exception",
    "public_claim",
    "delete_data",
    "rotate_live_credentials",
    "telephony_change",
}

SPECIALISTS = (
    "researcher",
    "architect",
    "frontend_engineer",
    "backend_engineer",
    "coder",
    "security_specialist",
    "sre",
    "critic",
    "technical_writer",
    "forward_deployed_engineer",
)


class CallenzoState(TypedDict):
    messages: Annotated[list, add_messages]
    goal: str
    plan: list[str]
    active_agent: str
    cycle: int
    artifacts: list[str]
    risks: list[str]
    needs_human_approval: bool
    approval_reason: Optional[str]
    last_result: Optional[str]


def chief_of_staff(state: CallenzoState) -> CallenzoState:
    if state.get("needs_human_approval"):
        return {**state, "active_agent": "human"}
    if state.get("cycle", 0) >= MAX_CYCLES:
        return {**state, "active_agent": "critic"}
    return {**state, "active_agent": state.get("active_agent") or "researcher"}


def route_after_supervisor(
    state: CallenzoState,
) -> Literal[
    "researcher",
    "architect",
    "frontend_engineer",
    "backend_engineer",
    "coder",
    "security_specialist",
    "sre",
    "critic",
    "technical_writer",
    "forward_deployed_engineer",
    "human",
    "__end__",
]:
    agent = state.get("active_agent", "researcher")
    if agent == "human":
        return "human"
    if agent == "finish":
        return "__end__"
    if agent in SPECIALISTS:
        return agent
    return "critic"


def specialist_stub(name: str):
    def node(state: CallenzoState) -> CallenzoState:
        return {
            **state,
            "cycle": state.get("cycle", 0) + 1,
            "last_result": f"{name} completed assigned task",
            "active_agent": "chief_of_staff",
        }

    node.__name__ = name
    return node


def human_gate(state: CallenzoState) -> CallenzoState:
    return {
        **state,
        "last_result": "Paused for Sam approval",
        "active_agent": "chief_of_staff",
    }


def build_graph():
    graph = StateGraph(CallenzoState)
    graph.add_node("chief_of_staff", chief_of_staff)
    graph.add_node("human", human_gate)
    for name in SPECIALISTS:
        graph.add_node(name, specialist_stub(name))
    graph.add_edge(START, "chief_of_staff")
    graph.add_conditional_edges("chief_of_staff", route_after_supervisor)
    for name in SPECIALISTS:
        graph.add_edge(name, "chief_of_staff")
    graph.add_edge("human", END)
    return graph.compile()

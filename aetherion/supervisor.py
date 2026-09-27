from typing import Literal
from langgraph.graph import END, START, StateGraph
from .agents import SPECIALIST_NODES
from .config import MAX_CYCLES, SPECIALISTS
from .memory import CHECKPOINTER
from .router import detect_sensitive, route_goal
from .state import AetherionState

def chief_of_staff(state: AetherionState) -> AetherionState:
    goal = state.get("goal") or ""
    sensitive = detect_sensitive(goal) or detect_sensitive(state.get("last_result") or "")
    if sensitive:
        return {**state, "needs_human_approval": True, "approval_reason": sensitive, "active_agent": "human"}
    if state.get("reviewed"):
        return {**state, "active_agent": "finish"}
    if state.get("cycle", 0) >= MAX_CYCLES:
        return {**state, "active_agent": "finish" if state.get("reviewed") else "critic"}
    if state.get("last_result") and state.get("cycle", 0) >= 2:
        return {**state, "active_agent": "critic"}
    nxt = route_goal(goal)
    plan = state.get("plan") or ["Clarify objective", "Assign specialist", "Review with Critic", "Request human approval if sensitive"]
    return {**state, "active_agent": nxt, "plan": plan}

def human_gate(state: AetherionState) -> AetherionState:
    return {**state, "last_result": f"HUMAN APPROVAL REQUIRED: {state.get('approval_reason')}. No sensitive action will execute until you approve.", "active_agent": "stop"}

def route_after_supervisor(state: AetherionState):
    agent = state.get("active_agent", "researcher")
    if agent in {"human", "stop"}:
        return "human"
    if agent == "finish":
        return "__end__"
    if agent in SPECIALISTS:
        return agent
    return "critic"

def build_graph():
    graph = StateGraph(AetherionState)
    graph.add_node("chief_of_staff", chief_of_staff)
    graph.add_node("human", human_gate)
    for name, node in SPECIALIST_NODES.items():
        graph.add_node(name, node)
    graph.add_edge(START, "chief_of_staff")
    graph.add_conditional_edges("chief_of_staff", route_after_supervisor)
    for name in SPECIALISTS:
        graph.add_edge(name, "chief_of_staff")
    graph.add_edge("human", END)
    return graph.compile(checkpointer=CHECKPOINTER)

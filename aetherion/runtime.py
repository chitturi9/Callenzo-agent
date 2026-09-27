from .agents import run_specialist
from .config import MAX_CYCLES
from .router import detect_sensitive, route_goal

def initial_state(goal: str) -> dict:
    return {
        "messages": [{"role": "user", "content": goal}],
        "goal": goal,
        "plan": ["Clarify objective", "Assign specialist", "Review with Critic", "Request human approval if sensitive"],
        "active_agent": "chief_of_staff",
        "cycle": 0,
        "artifacts": [],
        "risks": [],
        "needs_human_approval": False,
        "approval_reason": None,
        "last_result": None,
        "memory_notes": [],
        "reviewed": False,
    }

def run(goal: str) -> dict:
    state = initial_state(goal)
    sensitive = detect_sensitive(goal)
    if sensitive:
        state["needs_human_approval"] = True
        state["approval_reason"] = sensitive
        state["active_agent"] = "stop"
        state["last_result"] = f"HUMAN APPROVAL REQUIRED: {sensitive}. No sensitive action will execute until you approve."
        return state
    primary = route_goal(goal)
    state = run_specialist(primary, state)
    if state["cycle"] < MAX_CYCLES and not state.get("reviewed"):
        state = run_specialist("security_specialist", state)
    if not state.get("reviewed"):
        state = run_specialist("critic", state)
    state["active_agent"] = "finish"
    return state

from .config import SPECIALISTS
from .state import AetherionState
from .work import specialist_deliverable, write_artifact

def run_specialist(name: str, state: AetherionState) -> AetherionState:
    goal = state.get("goal", "")
    cycle = state.get("cycle", 0) + 1
    title, body = specialist_deliverable(name, goal)
    path = write_artifact(name, cycle, title, body)
    notes = list(state.get("memory_notes") or [])
    notes.append(f"{name}: {title} ({path})")
    artifacts = list(state.get("artifacts") or [])
    artifacts.append(path)
    risks = list(state.get("risks") or [])
    if name == "security_specialist":
        risks.append("Spoken prompt injection and call-recording leakage")
    if name == "sre":
        risks.append("Telephony jitter can break a 50-100 ms target")
    return {
        **state,
        "cycle": cycle,
        "last_result": body,
        "active_agent": "chief_of_staff",
        "memory_notes": notes,
        "artifacts": artifacts,
        "risks": risks,
        "reviewed": True if name == "critic" else bool(state.get("reviewed")),
    }

def make_specialist_node(name: str):
    def node(state: AetherionState) -> AetherionState:
        return run_specialist(name, state)
    node.__name__ = name
    return node

SPECIALIST_NODES = {name: make_specialist_node(name) for name in SPECIALISTS}

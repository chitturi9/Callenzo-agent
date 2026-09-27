from typing import Optional, TypedDict

class AetherionState(TypedDict, total=False):
    messages: list
    goal: str
    plan: list[str]
    active_agent: str
    cycle: int
    artifacts: list[str]
    risks: list[str]
    needs_human_approval: bool
    approval_reason: Optional[str]
    last_result: Optional[str]
    memory_notes: list[str]
    reviewed: bool

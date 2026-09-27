"""Callenzo live-voice strip as a LangGraph.

SIP -> LiveKit -> VAD -> ASR -> agent -> post-LLM policy -> tools -> TTS -> SIP
"""

from typing import Annotated, Literal, Optional, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


class VoiceState(TypedDict):
    messages: Annotated[list, add_messages]
    call_id: str
    caller_id: str
    stage: str
    partial_transcript: str
    intent: Optional[str]
    tool_name: Optional[str]
    tool_args: dict
    sam_ticket: Optional[str]
    barge_in: bool
    policy_ok: bool
    kill: bool
    kill_reason: Optional[str]
    timings_ms: dict
    needs_human_approval: bool
    approval_reason: Optional[str]


WRITE_TOOLS = {"create_job", "send_sms", "charge_card"}
MONEY_TOOLS = {"charge_card", "issue_refund"}
TELEPHONY_TOOLS = {"buy_number", "change_sip", "forward_all_calls"}
READ_TOOLS = {"lookup_hours", "lookup_job", "get_eta"}


def vad(state: VoiceState) -> VoiceState:
    if state.get("barge_in"):
        return {**state, "stage": "cancel_tts"}
    return {**state, "stage": "asr"}


def asr(state: VoiceState) -> VoiceState:
    return {**state, "stage": "agent"}


def agent(state: VoiceState) -> VoiceState:
    return {**state, "stage": "policy"}


def policy(state: VoiceState) -> VoiceState:
    tool = state.get("tool_name")
    ticket = state.get("sam_ticket")
    if state.get("kill"):
        return {**state, "policy_ok": False, "stage": "safe_mode"}
    if tool in MONEY_TOOLS | TELEPHONY_TOOLS and not ticket:
        return {
            **state,
            "policy_ok": False,
            "needs_human_approval": True,
            "approval_reason": tool,
            "stage": "sam_gate",
        }
    if tool and tool not in READ_TOOLS | WRITE_TOOLS | MONEY_TOOLS | TELEPHONY_TOOLS:
        return {**state, "policy_ok": False, "stage": "refuse_tool"}
    return {**state, "policy_ok": True, "stage": "tools" if tool else "tts"}


def tools(state: VoiceState) -> VoiceState:
    if not state.get("policy_ok"):
        return {**state, "stage": "tts"}
    return {**state, "stage": "tts"}


def tts(state: VoiceState) -> VoiceState:
    if state.get("barge_in"):
        return {**state, "stage": "vad"}
    return {**state, "stage": "end_turn"}


def sam_gate(state: VoiceState) -> VoiceState:
    return {**state, "stage": "waiting_sam", "needs_human_approval": True}


def safe_mode(state: VoiceState) -> VoiceState:
    return {**state, "stage": "safe_mode", "tool_name": None, "kill": True}


def route_policy(state: VoiceState) -> Literal["tools", "tts", "sam_gate", "safe_mode"]:
    if state.get("kill"):
        return "safe_mode"
    if state.get("needs_human_approval"):
        return "sam_gate"
    if state.get("policy_ok") and state.get("tool_name"):
        return "tools"
    return "tts"


def route_vad(state: VoiceState) -> Literal["asr", "tts"]:
    return "tts" if state.get("barge_in") else "asr"


def build_voice_graph():
    g = StateGraph(VoiceState)
    g.add_node("vad", vad)
    g.add_node("asr", asr)
    g.add_node("agent", agent)
    g.add_node("policy", policy)
    g.add_node("tools", tools)
    g.add_node("tts", tts)
    g.add_node("sam_gate", sam_gate)
    g.add_node("safe_mode", safe_mode)
    g.add_edge(START, "vad")
    g.add_conditional_edges("vad", route_vad)
    g.add_edge("asr", "agent")
    g.add_edge("agent", "policy")
    g.add_conditional_edges("policy", route_policy)
    g.add_edge("tools", "tts")
    g.add_edge("tts", END)
    g.add_edge("sam_gate", END)
    g.add_edge("safe_mode", END)
    return g.compile()

from datetime import datetime, timezone
from .config import ROOT
OUTPUTS = ROOT / "outputs"

def write_artifact(agent: str, cycle: int, title: str, body: str) -> str:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = OUTPUTS / f"{cycle:02d}_{agent}_{stamp}.md"
    path.write_text(f"# {title}\n\nAgent: {agent}\nCycle: {cycle}\n\n{body}\n", encoding="utf-8")
    return str(path)

def specialist_deliverable(name: str, goal: str) -> tuple[str, str]:
    playbooks = {
        "researcher": ("Research brief", f"Goal: {goal}\n\nSelf-hosted voice agents are viable with LiveKit + local ASR/TTS/LLM. Cascaded p50 300-800ms is realistic."),
        "architect": ("Architecture and latency budget", f"Goal: {goal}\n\nPhone -> SIP -> LiveKit -> VAD -> ASR -> LLM -> TTS -> caller. Ship cascaded first."),
        "frontend_engineer": ("Operator console spec", f"Goal: {goal}\n\nNext.js + LiveKit client. Live call, transcript, latency, barge-in, takeover."),
        "backend_engineer": ("Service contracts", f"Goal: {goal}\n\nSession API, runtime, tool gateway, approval queue, call event log."),
        "coder": ("Implementation plan", f"Goal: {goal}\n\nSupervisor graph, LiveKit worker, model adapters, approval interrupt, barge-in tests."),
        "security_specialist": ("Threat model", f"Goal: {goal}\n\nRisks: recording leakage, spoken prompt injection, SIP fraud. Encrypt recordings. Human gate on trunk changes."),
        "sre": ("SRE plan", f"Goal: {goal}\n\nSLOs: setup success, p95 mouth-to-ear, barge-in cancel, worker restart."),
        "critic": ("Quality gate", f"Goal: {goal}\n\nPass if human gate works and latency budget is explicit. Production deploy not approved."),
        "technical_writer": ("Narrative", f"Goal: {goal}\n\nCallenzo private voice agents. Do not claim 50-100ms until measured."),
        "forward_deployed_engineer": ("Customer install checklist", f"Goal: {goal}\n\nSIP credentials, pin region, measure audio, tune VAD, file latency report."),
    }
    return playbooks.get(name, (f"{name} note", f"Goal: {goal}\n\nCompleted specialist pass."))

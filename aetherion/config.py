from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "prompts"
MAX_CYCLES = 8

SENSITIVE_ACTIONS = frozenset({
    "production_deploy", "spend_money", "sign_customer", "security_exception",
    "public_claim", "delete_data", "rotate_live_credentials", "telephony_change",
})

SPECIALISTS = (
    "researcher", "architect", "frontend_engineer", "backend_engineer", "coder",
    "security_specialist", "sre", "critic", "technical_writer", "forward_deployed_engineer",
)

PROMPT_FILES = {
    "chief_of_staff": "CHIEF_OF_STAFF.md",
    "researcher": "RESEARCHER.md",
    "architect": "ARCHITECT.md",
    "frontend_engineer": "FRONTEND_ENGINEER.md",
    "backend_engineer": "BACKEND_ENGINEER.md",
    "coder": "CODER.md",
    "security_specialist": "SECURITY_SPECIALIST.md",
    "sre": "SRE.md",
    "critic": "CRITIC.md",
    "technical_writer": "TECHNICAL_WRITER.md",
    "forward_deployed_engineer": "FORWARD_DEPLOYED_ENGINEER.md",
}

ROUTING_HINTS = {
    "research": "researcher", "competitor": "researcher", "benchmark": "researcher",
    "architecture": "architect", "latency": "architect", "stack": "architect",
    "ui": "frontend_engineer", "frontend": "frontend_engineer", "react": "frontend_engineer",
    "api": "backend_engineer", "database": "backend_engineer",
    "code": "coder", "implement": "coder", "bug": "coder",
    "security": "security_specialist", "threat": "security_specialist",
    "sre": "sre", "deploy": "sre", "observability": "sre",
    "review": "critic", "qa": "critic",
    "doc": "technical_writer", "deck": "technical_writer", "sell": "technical_writer",
    "customer": "forward_deployed_engineer", "telephony": "forward_deployed_engineer", "twilio": "forward_deployed_engineer",
}

AGENT_NAMES = {
    "chief_of_staff": "Nova",
    "researcher": "Rex",
    "architect": "Atlas",
    "frontend_engineer": "Sofiya",
    "backend_engineer": "John",
    "coder": "Mike",
    "security_specialist": "Elena",
    "sre": "Marcus",
    "critic": "Priya",
    "technical_writer": "Ava",
    "forward_deployed_engineer": "Elon Musk",
}

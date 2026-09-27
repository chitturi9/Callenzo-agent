from .config import ROUTING_HINTS, SENSITIVE_ACTIONS, SPECIALISTS

def detect_sensitive(text: str) -> str | None:
    lowered = text.lower()
    mapping = {
        "deploy to production": "production_deploy",
        "production deploy": "production_deploy",
        "buy number": "telephony_change",
        "sip trunk": "telephony_change",
        "spend": "spend_money",
        "invoice": "spend_money",
        "sign the customer": "sign_customer",
        "we guarantee": "public_claim",
        "delete all": "delete_data",
        "rotate key": "rotate_live_credentials",
        "disable auth": "security_exception",
    }
    for phrase, action in mapping.items():
        if phrase in lowered and action in SENSITIVE_ACTIONS:
            return action
    return None

def route_goal(goal: str) -> str:
    lowered = goal.lower()
    scores = {name: 0 for name in SPECIALISTS}
    for hint, agent in ROUTING_HINTS.items():
        if hint in lowered:
            scores[agent] += 1
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "architect" if "system" in lowered or "voice" in lowered else "researcher"
    return best

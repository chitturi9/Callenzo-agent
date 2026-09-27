from .config import PROMPT_FILES, PROMPTS_DIR

def load_prompt(role: str) -> str:
    return (PROMPTS_DIR / PROMPT_FILES[role]).read_text(encoding="utf-8")

def load_all_prompts() -> dict[str, str]:
    return {role: load_prompt(role) for role in PROMPT_FILES}

# Callenzo

Elite multi-agent system for a self-hosted voice-AI company.

**Company:** Callenzo  
**Boss:** Sam  
**Chief of Staff:** Nova

Supervisor pattern: Nova routes work to specialists. Sensitive actions stop for Sam.

## Team

| Name | Role |
| --- | --- |
| Nova | Chief of Staff |
| Rex | Researcher |
| Atlas | Architect |
| Sofiya | Frontend Engineer |
| John | Backend Engineer |
| Mike | Coder |
| Elena | Security Specialist |
| Marcus | SRE / DevOps |
| Priya | Critic / QA |
| Ava | Technical Writer |
| Elon Musk | Forward Deployed Engineer |

## Layout

- `prompts/` — full system prompts
- `architecture/` — system, voice stack, tools, state, deploy
- `agents/` — team roster and graph skeleton
- `aetherion/` — runnable supervisor package (fallback runtime if LangGraph is missing)
- `docs/` — extra notes

## Run

```bash
pip install -r requirements.txt
python -m aetherion "Design a self-hosted voice agent with phone calling"
```

Sensitive goals (production deploy, spend, telephony changes) pause for human approval.

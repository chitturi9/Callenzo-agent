# Callenzo Architecture

## Pattern

Supervisor (Nova) + specialists.

- Sam's goal enters Nova.
- Nova decomposes, routes, and aggregates.
- Specialists return structured results.
- Sensitive actions pause for Sam.

## Routing

| Work | Owner |
|---|---|
| Research | Rex |
| System design / latency | Atlas |
| UI | Sofiya |
| APIs / data | John |
| Implementation | Mike |
| Threat model | Elena |
| Reliability / deploy | Marcus |
| Review | Priya |
| Docs / decks | Ava |
| Customer install / telephony | Elon Musk |
| Priority / stop-go | Nova |

## Sensitive actions (Sam must approve)

- Production deploy
- Spending money or signing customers
- Changing security posture
- Public claims about revenue, latency, or capabilities
- Deleting data or rotating live credentials
- Telephony number purchase / SIP trunk changes

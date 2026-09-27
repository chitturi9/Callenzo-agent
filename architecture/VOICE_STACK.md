# Voice Stack

Target: self-hosted voice agents. Aggressive lab target 50–100 ms S2S. Realistic cascaded production is higher.

| Layer | Default |
|---|---|
| Telephony | Telnyx / Twilio / Vonage / Plivo + LiveKit SIP |
| Media / agents | LiveKit Agents |
| VAD | Silero or TEN VAD |
| ASR | Parakeet TDT / Nemotron Speech / Qwen3-ASR |
| LLM serve | vLLM or llama.cpp |
| TTS | Kokoro / Qwen3-TTS / Piper |
| Orchestration | Callenzo supervisor on LangGraph |

Sam must approve production deploy, number purchase, or public latency claims.

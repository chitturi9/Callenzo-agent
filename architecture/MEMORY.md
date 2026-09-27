# Callenzo Memory — Recommendation

Sam owns the company. Memory is not a diary the model gets to rewrite.

## Four stores, four jobs

1. **Working memory (this call only)**  
   LangGraph thread state. Call id, caller number, last user utterance, last agent utterance, pending tool, Sam ticket id, barge-in flag, stage timings. Dies when the call ends unless promoted.

2. **Episodic memory (what happened)**  
   After hangup: 8–12 line summary, tools used, outcome, complaints, latency p50. No raw audio in the prompt. Audio stays encrypted on disk.

3. **Semantic memory (what is true about this customer)**  
   Shop hours, service area, pricing rules, never discount without Sam, allowed tools, banned phrases. Edited only through Nova + Priya. Not by the live model.

4. **Procedural memory (how we do the job)**  
   Playbooks: after-hours plumber, missed appointment, angry caller, payment link. Versioned in git. Runtime reads them read-only.

## Hard rules

- Recordings never enter the LLM context. Transcripts are redacted before storage.
- The live model may read semantic + procedural. It may propose an episodic note. It may not edit policy or pricing.
- If working memory and semantic memory disagree, semantic wins and Priya gets a ticket.
- 12 GB GPU: keep working context short. Summarize every 8 turns.

## Who owns which store

| Store | Owner |
| --- | --- |
| Working (thread) | John + Mike |
| Episodic | Marcus (pipeline) + Ava (quality of the writeup) |
| Semantic | Nova + Priya |
| Procedural | Atlas + Elon (field scars) |

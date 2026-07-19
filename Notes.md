Context window — a budget, not memory
The context window is the fixed number of tokens the model processes in a single call. It is not memory — no state persists between calls — and input and output share the same fixed pool. Everything for a given call (system prompt, history, retrieved docs, question, and room to generate) coexists in that one budget.
More context is not better. Two costs of over-stuffing:

Cost + latency — you pay per input token on every call; generation slows as context grows.
Quality degradation — two mechanisms: signal dilution (extra chunks are plausible distractors the model can anchor on) and lost-in-the-middle (models attend most to the start and end; a relevant chunk in the middle gets under-weighted).

Takeaway: get the right small set of tokens into the window, not the most. That's what RAG + reranking exist to do (retrieve wide for recall, rerank down for precision, order best where attention is strongest).
Why LLMs hallucinate
An LLM is a next-token predictor optimizing for statistical plausibility, not truth. It answers from its own weights — a lossy, cutoff-dated compression — and has no native "I don't know." So when asked something absent, stale, or private, it doesn't return empty; it interpolates a plausible-looking answer at full confidence. Hallucination is plausibility and truth diverging. (DE analogy: a query that never returns NULL — asks for a missing key, synthesizes a plausible row instead of "no rows.")
Three-layer defense in depth
No single layer is sufficient — each fails sometimes, so they stack.

Ground (before) — RAG. Put authoritative text in-context so the task becomes "read this" not "recall this." Highest leverage; attacks the root cause. But retrieval can fetch a wrong chunk.
Constrain (during) — prompting + decoding. Instruct "answer only from context; say you don't know otherwise"; lower temperature so decoding favors conservative tokens. Narrows the room to invent. But instructions can be ignored.
Verify (after) — faithfulness / citations / schema. Check the answer traces to sources (often an LLM-judge), enforce citations, validate output shape. Last line. But it can still miss things.

RAG vs fine-tuning (interview gold)
Fine-tuning changes behavior (style, format, tone); it does not reliably install retrievable facts — knowledge smears lossily into weights, not lookup-able records. Policy Q&A is a knowledge problem, not a behavior problem → RAG.
RAG wins on:

Freshness — fetches current doc at query time; a policy update is a file change, not a retraining run. A fine-tuned model goes confidently stale until retrained.
Access control — docs live in a store you own; retrieval can filter to what a user is cleared to see. Shared weights can't.
Citations — every claim points to a source chunk. Fine-tuning just asserts.

Fine-tuning is right only when the goal is how it answers, not what it knows.
The cost model (thinking models)
On thinking models (e.g. gemini-2.5-flash), the model generates invisible thoughts tokens before the visible answer — and you pay for them.

total_token_count = prompt + thoughts + candidates. Total is the only number that doesn't lie.
candidates_token_count alone undercounts — it omits the hidden reasoning.
Observed today: temp 1.0 cost 9x temp 0.0 (705 vs 77 total) while producing shorter visible output — the entire difference was hidden thinking.
Caveat for later: input and output are priced at different rates; a precise cost model multiplies each by its own rate (Week 17).

Temperature
Controls sampling randomness. 0.0 → near-deterministic, picks highest-probability tokens (same prompt ≈ same output). 1.0 → samples more freely, more varied and drift-prone (including in hidden reasoning — which is why it cost more today). Set it deliberately; don't inherit the default. To prove determinism at 0: run N times, diff the outputs.
Prompting (foreshadow)
Vague instruction → plausible-shaped output (asked for one tagline, got a menu — a common training-data shape). Explicit constraints → the shape you asked for. This is why the next block validates output rather than trusting it.

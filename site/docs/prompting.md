# Prompt Engineering Playbook

_Last updated: 2025-09-29_

The glossary captures a full stack of prompt-related terminology. Use this page as a
jumping-off point for crafting reliable instructions and understanding the knobs that
affect behavior.

**Quick links**

- [Role starter pack: Product & Program Managers](roles.md#product--program-managers)
- [Role starter pack: Engineering & Platform](roles.md#engineering--platform)
- [Search prompts & decoding terms](search.md?category=LLM%20Core)
- [Search governance touchpoints](search.md?category=Governance%20%26%20Risk&role=policy)
- [Safety classifier guide](terms/safety-classifier/)
- [Robust prompting tips](terms/robust-prompting/)

## Core concepts

- [Prompt engineering](terms/prompt-engineering/) — overall workflow for iterating and testing prompts.
- [System prompt](terms/system-prompt/) — immutable guardrail at the top of every conversation.
- [Context window](terms/context-window/) — token budget that constrains prompt size and retrieved context.
- [Token](terms/token/) — smallest unit models consume, essential for cost and context planning.

## Controlling outputs

- [Temperature](terms/temperature/) — adjusts randomness in sampling; lower for consistency, higher for ideation.
- [Top-k sampling](terms/top-k-sampling/) — limits sampling to the top *k* candidates per step.
- [Top-p sampling](terms/top-p-sampling/) — chooses from the smallest probability mass that sums to *p*.
- [Repetition penalty](terms/repetition-penalty/) — discourages loops or repeated phrases.
- [Beam search](terms/beam-search/) — deterministic multi-path decoding for structured responses.
- [Self-consistency decoding](terms/self-consistency-decoding/) — sample multiple reasoning chains and aggregate the dominant answer before finalizing.
- [Chain-of-thought prompting](terms/chain-of-thought-prompting/) — encourage the model to reason step by step before committing to an answer.

## Grounding and retrieval aids

- [Retrieval-augmented generation](terms/retrieval-augmented-generation/) — combine prompts with retrieved context.
- [Chunking](terms/chunking/) and [vector stores](terms/vector-store/) — structure knowledge bases for precise context windows.
- [Reranking](terms/reranking/) — surface the best supporting passages before they enter the prompt.
- [Data lineage](terms/data-lineage/) — keep track of where grounding data originated so prompt responses remain auditable.
- [Shadow deployment](terms/shadow-deployment/) — run new prompts in parallel to capture telemetry before rollout.

## Safety and governance touchpoints

- [Guardrails](terms/guardrails/) — policy-aligned controls before or after generation.
- [Safety evaluation](terms/safety-evaluation/) — ensure prompt changes don’t undo previous approvals.
- [Model card](terms/model-card/) & [content moderation](terms/content-moderation/) — document and monitor prompt behavior in production.

### Quick checklist before launch

1. Version system prompts in source control and log every change.
2. Benchmark prompts across accuracy, hallucination, fairness, jailbreak resilience, and latency metrics.
3. Validate context window usage with representative journeys (long, multilingual, regulated).
4. Document decoding settings (temperature, top-k/top-p, repetition penalties) in model cards.
5. Run red-teaming and safety evaluations when prompts or grounding data change.
6. Observe shadow deployments before launch, reviewing safety classifier scores and human handoff outcomes.

For deeper exploration, use the [interactive search](search/) with the `LLM Core` category or filter by your team’s role.

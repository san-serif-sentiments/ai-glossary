# Prompt Engineering Playbook

_Last updated: 2024-11-04_

The glossary captures a full stack of prompt-related terminology. Use this page as a
jumping-off point for crafting reliable instructions and understanding the knobs that
affect behavior.

**Quick links**

- [Role starter pack: Product & Program Managers](roles.md#product--program-managers)
- [Role starter pack: Engineering & Platform](roles.md#engineering--platform)
- [Search prompts & decoding terms](search.md?category=LLM%20Core)
- [Search governance touchpoints](search.md?category=Governance%20%26%20Risk&role=policy)

## Core concepts

- [Prompt engineering](terms/prompt-engineering.md) — overall workflow for iterating and testing prompts.
- [System prompt](terms/system-prompt.md) — immutable guardrail at the top of every conversation.
- [Context window](terms/context-window.md) — token budget that constrains prompt size and retrieved context.
- [Token](terms/token.md) — smallest unit models consume, essential for cost and context planning.

## Controlling outputs

- [Temperature](terms/temperature.md) — adjusts randomness in sampling; lower for consistency, higher for ideation.
- [Top-k sampling](terms/top-k-sampling.md) — limits sampling to the top *k* candidates per step.
- [Top-p sampling](terms/top-p-sampling.md) — chooses from the smallest probability mass that sums to *p*.
- [Repetition penalty](terms/repetition-penalty.md) — discourages loops or repeated phrases.
- [Beam search](terms/beam-search.md) — deterministic multi-path decoding for structured responses.

## Grounding and retrieval aids

- [Retrieval-augmented generation](terms/retrieval-augmented-generation.md) — combine prompts with retrieved context.
- [Chunking](terms/chunking.md) and [vector stores](terms/vector-store.md) — structure knowledge bases for precise context windows.
- [Reranking](terms/reranking.md) — surface the best supporting passages before they enter the prompt.

## Safety and governance touchpoints

- [Guardrails](terms/guardrails.md) — policy-aligned controls before or after generation.
- [Safety evaluation](terms/safety-evaluation.md) — ensure prompt changes don’t undo previous approvals.
- [Model card](terms/model-card.md) & [content moderation](terms/content-moderation.md) — document and monitor prompt behavior in production.

### Quick checklist before launch

1. Version system prompts in source control and log every change.
2. Benchmark prompts across precision, recall, hallucination, and fairness metrics.
3. Validate context window usage with representative journeys (long, multilingual, regulated).
4. Document decoding settings (temperature, top-k/top-p, repetition penalties) in model cards.
5. Run red-teaming and safety evaluations when prompts or grounding data change.

For deeper exploration, use the [interactive search](search.md) with the `LLM Core` category or filter by your team’s role.

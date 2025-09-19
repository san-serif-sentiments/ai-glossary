# AI Glossary

<div class="hero-panel">
  <div>
    <h2>Shared language for AI builders and stewards</h2>
    <p>
      Every term in the glossary is citation-backed, audience-aware, and stored as
      structured YAML so it can power docs, APIs, and review workflows. Browse by
      category, role, or metric to keep product, engineering, and governance teams in sync.
    </p>
  </div>
  <div class="hero-actions">
    <a class="cta" href="search/">🔍 Explore the interactive search</a>
    <a class="cta secondary" href="roles/">👥 Role starter packs</a>
    <a class="cta secondary" href="categories/">🧭 Category explorer</a>
  </div>
</div>

## What's new (Nov 26 2024)

<div class="whats-new">
  <ul>
    <li><strong>Guided search filters:</strong> Quick chips for roles, categories, and status now help you zero in on the terms that match your current workflow.</li>
    <li><strong>Role learning paths:</strong> Each starter pack includes a three-step journey so teams know where to begin, what to review, and who to loop in.</li>
    <li><strong>Contributor shortcuts:</strong> `make new-term` scaffolds high-quality entries, while `make check` validates schema, tests, and docs in one command.</li>
  </ul>
  <p class="whats-new-footer">Submit feedback or new term ideas via the <a href="term-request/">term request intake</a>.</p>
</div>

## Project focus

- **Shared language:** harmonizes terminology across technical, product, and
  policy stakeholders.
- **Structured delivery:** each entry lives in YAML with examples, aliases, and
  governance context for downstream reuse.
- **Traceable sources:** every definition includes citations, NIST AI RMF tags,
  and lifecycle status for auditability.

## Current features

- Seed coverage for foundational concepts spanning large language models,
  retrieval, MLOps, and governance.
- Automated validation that enforces schema rules, definition length limits,
  and audience-specific explanations before publication.
- Generated JSON datasets (`build/glossary.json`, `build/search-index.json`) and
  Markdown documentation (`site/docs/terms/`) derived from the same YAML source.
- Categorized navigation so visitors can browse by LLM internals, retrieval,
  optimization, operations, or governance topics.
- Role starter packs and a guided search experience so product, engineering,
  policy, legal, security, and communications teams can find relevant terms fast.

## Deep-dive resources

- [External source catalog](resources.md) — official glossaries and standards to cite.
- [Governance dashboard](governance-dashboard.md) — metrics, NIST coverage, and intake guidance.
- [Prompt engineering playbook](prompting.md) — practical workflows for shaping model behaviour.

### Popular categories

<div class="category-grid">
  <div class="category-card">
    <h3>LLM Core</h3>
    <p>Attention, decoding, prompting, and the building blocks behind language models.</p>
    <a href="categories/#llm-core">Browse terms →</a>
  </div>
  <div class="category-card">
    <h3>Retrieval &amp; RAG</h3>
    <p>Grounding models with hybrid search, chunking, reranking, and retrieval pipelines.</p>
    <a href="categories/#retrieval--rag">Browse terms →</a>
  </div>
  <div class="category-card">
    <h3>Governance &amp; Risk</h3>
    <p>Responsible AI practices, documentation, privacy, and safety mitigation.</p>
    <a href="categories/#governance--risk">Browse terms →</a>
  </div>
  <div class="category-card">
    <h3>Optimization &amp; Efficiency</h3>
    <p>Quantization, LoRA, distillation, and performance tuning for deployment.</p>
    <a href="categories/#optimization--efficiency">Browse terms →</a>
  </div>
</div>

## Roadmap highlights

- Grow the corpus to 50+ prioritized LLM, infrastructure, and risk terms.
- Publish the static site for public access and contributor discovery.
- Expose the lightweight API to support integrations and chat assistants.

Contributors can review the [Contribution guide](contributing.md) to learn how
to add or refine glossary entries.

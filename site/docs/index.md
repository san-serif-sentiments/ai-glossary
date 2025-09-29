# AI Glossary

<div class="hero-panel">
  <div>
    <h2>Shared language for AI builders and stewards</h2>
    <p>
      Every term in the glossary is citation-backed, audience-aware, and stored as
      structured YAML so it can power docs, APIs, and review workflows. Browse by
      category, role, or metric to keep product, engineering, and governance teams in sync.
    </p>
    <div class="brand-signature">
      <span class="brand-name">Shailesh Rawat</span>
      <span class="brand-handle">@sans_serif_sentiments</span>
    </div>
  </div>

  <div class="hero-actions">
    <a class="cta" href="search.md">🔍 Explore the interactive search</a>
    <a class="cta secondary" href="roles.md">👥 Role starter packs</a>
    <a class="cta secondary" href="categories.md">🧭 Category explorer</a>
  </div>
</div>

## What's new (Sep 28 2025)

<div class="whats-new">
  <ul>
    <li><strong>Lifecycle snapshot:</strong> Search now surfaces status counts and the latest review date so teams can see glossary health at a glance.</li>
    <li><strong>100-term milestone:</strong> Added new entries spanning assurance cases, RLHF workflows, and safety controls to push the glossary past one hundred vetted terms.</li>
    <li><strong>Sort for relevance:</strong> Reorder results by freshness or category to share curated views with stakeholders in seconds.</li>
  </ul>
  <p class="whats-new-footer">
    Submit feedback or new term ideas via the <a href="term-request.md">term request intake</a>.
  </p>
</div>

## Project focus

- **Shared language:** harmonizes terminology across technical, product, and policy stakeholders.
- **Structured delivery:** each entry lives in YAML with examples, aliases, and governance context for downstream reuse.
- **Traceable sources:** every definition includes citations, NIST AI RMF tags, and lifecycle status for auditability.

## Current features

- Seed coverage for foundational concepts spanning large language models, retrieval, MLOps, and governance.
- Automated validation that enforces schema rules, definition length limits, and audience-specific explanations before publication.
- Generated JSON datasets (`build/glossary.json`, `build/search-index.json`) and Markdown documentation (`site/docs/terms/`) derived from the same YAML source.
- Categorized navigation so visitors can browse by LLM internals, retrieval, optimization, operations, or governance topics.
- Role starter packs and a guided search experience so product, engineering, policy, legal, security, and communications teams can find relevant terms fast.

## Deep-dive resources

- [External source catalog](resources.md) — official glossaries and standards to cite.
- [Governance dashboard](governance-dashboard.md) — metrics, NIST coverage, and intake guidance.
- [Prompt engineering playbook](prompting.md) — practical workflows for shaping model behaviour.

### Popular categories

<div class="category-grid">

  <div class="category-card">
    <h3>LLM Core</h3>
    <p>Attention, decoding, prompting, and the building blocks behind language models.</p>
    <a href="categories.md#llm-core">Browse terms →</a>
  </div>

  <div class="category-card">
    <h3>Retrieval &amp; RAG</h3>
    <p>Grounding models with hybrid search, chunking, reranking, and retrieval pipelines.</p>
    <a href="categories.md#retrieval-rag">Browse terms →</a>
  </div>

  <div class="category-card">
    <h3>Governance &amp; Risk</h3>
    <p>Responsible AI practices, documentation, privacy, and safety mitigation.</p>
    <a href="categories.md#governance-risk">Browse terms →</a>
  </div>

  <div class="category-card">
    <h3>Optimization &amp; Efficiency</h3>
    <p>Quantization, LoRA, distillation, and performance tuning for deployment.</p>
    <a href="categories.md#optimization-efficiency">Browse terms →</a>
  </div>

</div>

## Roadmap highlights

- Curate the next 150 terms with deeper coverage of safety tooling, security, and applied UX patterns.
- Launch a public design kit so teams can reuse the Shailesh Rawat (sans_serif_sentiments) brand components across docs and products.
- Publish live health dashboards that blend glossary freshness, evaluation signals, and intake response times.

Contributors can review the [Contribution guide](contributing.md) to learn how to add or refine glossary entries.

<p class="brand-footer">✨ Crafted and curated by Shailesh Rawat · sans_serif_sentiments</p>

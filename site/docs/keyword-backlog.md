# Keyword Backlog

Purpose: keep our glossary focused on high-value, high-quality definitions while growing coverage methodically.

## How to use this backlog
- Start with the highest-priority items in each cluster; they map to common employee pain points gathered from support, sales, and policy teams.
- Draft entries with the [term schema](https://github.com/san-serif-sentiments/ai-glossary/blob/main/schema/term.schema.json) so definitions stay consistent, cite at least two sources, and include audience guidance.
- Use `make new-term NAME="your term"` to generate a scaffold that already meets schema requirements and reminds you to capture quality notes.
- After drafting, run `make check` to validate schema, tests, and docs before opening a PR.
- Pair with a reviewer from another function before publishing; readability and accessibility are part of the review.
- Update the "Status" column after every checkpoint (discovery, drafting, review, published) so everyone sees progress at a glance.

## Prioritization criteria
- **Employee impact** – does this term unblock onboarding, customer conversations, or compliance workflows?
- **Source coverage** – does it let us cite underused glossaries (OECD, AI Now, Partnership on AI, LangChain, OpenAI, Anthropic)?
- **Clarity risk** – will the average employee struggle without a carefully written explanation and examples?
- **UX fit** – can we explain it plainly in under 320 characters for the short definition without overwhelming readers?

## Cluster overview
The clusters align to employee journeys so readers can scan by topic instead of alphabet soup.

### Pain point map
| Journey | Common friction | Target terms | Notes |
| --- | --- | --- | --- |
| Launch governance | Proving compliance, documenting mitigations | AI assurance, algorithmic audit, transparency report | Aligns with policy, legal, and audit stakeholders. |
| Agent operations | Safe orchestration of tools and automations | agent executor, guardrail policy, human handoff | Pair with LangChain/OpenAI docs for implementation recipes. |
| Evaluation maturity | Measuring safety and quality at scale | evaluation harness, safety spec, robust prompting | Ensure red team, QA, and DS share a single playbook. |
| Data responsibility | Handling sensitive data lifecycle | consent management, impact mitigation plan, data minimization | Link to privacy office guidelines and ISO references. |

### Compliance & Assurance
Learner moment: "I have to prove this system meets policy and regulatory expectations."

| Priority | Term | Employee need | Seed sources | Owner | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | AI assurance | Understand the controls and evidence needed to certify an AI system. | OECD AI Glossary; Partnership on AI Glossary; AI Now Lexicon | Policy & Governance pod | Discovery | Pair with upcoming risk playbook.| 
| 1 | algorithmic audit | Clarify how independent audits test for bias, safety, and compliance. | OECD AI Glossary; AI Now Lexicon | Risk & Compliance guild | Discovery | Differentiate from internal evaluations.| 
| 2 | transparency report | Summarize what disclosures regulators expect for AI deployments. | OECD AI Glossary; Partnership on AI Glossary | Policy & Governance pod | Backlog | Collect real-world report examples.| 
| 2 | impact mitigation plan | Show how mitigation tracking links to AIAs and incident response. | AI Now Lexicon; Partnership on AI Glossary | Product Operations | Backlog | Tie to `algorithmic impact assessment`.| 
| 3 | assurance case | Explain structured arguments used in safety-critical industries. | OECD AI Glossary; Partnership on AI Glossary | Safety Council | Backlog | Borrow structure from safety engineering.| 

### Safety & Alignment
Learner moment: "How do we keep models behaving safely as policies evolve?"

| Priority | Term | Employee need | Seed sources | Owner | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | safety spec | Give cross-functional teams a single reference for allowed/blocked behaviors. | Anthropic / Claude Glossary; MIT Tech Review AI Dictionary | Alignment Working Group | Discovery | Should link to guardrail templates.| 
| 1 | self-critique loop | Describe how models evaluate their own outputs before release. | Anthropic / Claude Glossary; DeepLearning.AI Glossary | Research Guild | Discovery | Connect to `constitutional ai`.| 
| 2 | escalation policy | Clarify when humans take over from automated systems. | OECD AI Glossary; AI Now Lexicon | Operations | Backlog | Align with `ai incident response`.| 
| 2 | robust prompting | Help enablement teams teach defensive prompt design. | MIT Tech Review AI Dictionary; Anthropic resources | Enablement Chapter | Backlog | Include inclusive examples.| 
| 3 | consent management | Explain how user consent is honored in AI experiences. | OECD AI Glossary; Partnership on AI Glossary | Privacy Office | Backlog | Link to `data minimization` and `privacy`.| 

### Agent Orchestration & Tooling
Learner moment: "How do I design agent workflows without exposing users to risk?"

| Priority | Term | Employee need | Seed sources | Owner | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | agent executor | Show engineers how orchestration loops schedule tool calls. | LangChain Glossary; OpenAI Glossary | Agent Platform team | Discovery | Pair with diagrams in `tool use`.| 
| 1 | memory strategy | Teach when to use vector memory, summaries, or none. | LangChain Glossary; Hugging Face Glossary | Agent Platform team | Discovery | Should cross-reference `vector store`.| 
| 2 | evaluation harness | Explain automated eval pipelines for agents and RAG flows. | LangChain Glossary; OpenAI Glossary | QA Guild | Backlog | Reuse content from evaluation playbook.| 
| 2 | guardrail policy | Document how policy prompts map to enforcement levels. | Anthropic / Claude Glossary; OpenAI Glossary | Safety Engineering | Backlog | Distinguish from `guardrails` concept page.| 
| 3 | human handoff | Outline UX patterns for escalating to people mid-session. | LangChain Glossary; Partnership on AI Glossary | Support Ops | Backlog | Capture accessibility considerations.| 

## Seeding progress (Nov 26 2024)

| Source | Citations |
| --- | --- |
| Google ML Glossary | 44 |
| NIST AI RMF Glossary | 34 |
| Stanford HAI Brief Definitions | 30 |
| Hugging Face Glossary | 29 |
| Wikipedia AI Glossary | 26 |
| UK POST AI Glossary | 23 |
| Anthropic / Claude Glossary | 1 |
| DeepLearning.AI AI Glossary | 1 |
| MIT Technology Review AI Dictionary | 1 |
| OECD AI Glossary | 1 |
| AI Now Institute Lexicon | 1 |
| Partnership on AI Glossary | 1 |
| Hugging Face Tokenizers | 1 |
| OpenAI Glossary | 1 |
| LangChain Documentation Glossary | 1 |

Focus upcoming seeding on the underused sources (Anthropic, OECD, AI Now, Partnership on AI, LangChain, OpenAI) so the glossary stays balanced across technical and governance perspectives.

## Drafting checklist
- Lead with the employee problem, then deliver inclusive, plain-language definitions.
- Provide at least one example for the "do" and "dont" arrays that mirrors real workflows.
- Cite two or more sources, pulling from at least one underused glossary listed above when possible.
- Add accessibility by breaking long paragraphs, avoiding jargon, and front-loading the main idea.
- After draft review, run `mkdocs build --strict -f site/mkdocs.yml` to catch schema or formatting issues.

## Maintaining readability
- Keep short definitions under 160 characters whenever possible so they scan well in mobile contexts.
- Use sentence case, avoid unexplained abbreviations, and include context in the first clause.
- When referencing regulations or frameworks, link to employee-friendly summaries instead of dense PDFs.

Keep this backlog fresh: archive published items and add new requests from the intake form so contributors stay focused on what matters most to employees.

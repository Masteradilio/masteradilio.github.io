# Adilio Farias — AI Engineer & Senior Data Scientist Portfolio

Live portfolio: https://masteradilio.github.io/

This repository hosts the bilingual (PT-BR / EN) professional portfolio of **Adilio Farias**, focused on opportunities as **AI Engineer** and **Senior Data Scientist**.

## What this portfolio demonstrates

- Machine Learning and Data Science applied to fraud prevention, credit risk and time series.
- Generative AI, RAG, AI Agents, semantic guardrails and LLM evaluation.
- MLOps, model monitoring, data engineering and production-oriented APIs.
- Autonomous software engineering through **Squad Forge SE**.
- Financial-services domain experience combined with hands-on engineering.

## Recruiter-facing design

The site is intentionally optimized for fast evaluation:

1. Professional positioning and accumulated multidisciplinary experience.
2. Evidence-oriented project cards linked to the canonical public repositories.
3. Bilingual CV/Resume pages.
4. A free-form AI career assistant backed by a Cloudflare Worker and RAG context.
5. Direct links to LinkedIn, GitHub and email.

The career assistant does **not** use predefined content answers for substantive questions. Recruiters can formulate their own questions; only utility actions such as contact and resume access may use deterministic responses.

## Portfolio projects

The site currently presents seven open-source projects covering:

- autonomous AI software engineering;
- quantitative time-series ML;
- ontology-grounded RAG guardrails and EVALs;
- epidemiological intelligence with LangGraph and hybrid RAG;
- credit-risk engineering and ECL;
- credit scoring / Champion-vs-Challenger modeling;
- real-time PIX anti-fraud and MLOps.

Three projects are highlighted as **Featured** because together they provide the fastest cross-section of AI Engineering, Agentic RAG and production-oriented ML/MLOps capabilities.

## Career assistant architecture

The browser sends free-form recruiter questions to a serverless Cloudflare Worker. The frontend supports:

- recent conversation history without duplicating the current user message;
- optional RAG source metadata returned by the Worker;
- Markdown rendering with DOMPurify sanitization;
- explicit timeout/failure messaging;
- deterministic utility-only answers for resume/contact requests.

See [`docs/CLOUDFLARE_RAG_UPGRADE.md`](docs/CLOUDFLARE_RAG_UPGRADE.md) for the recommended Worker response contract and grounding rules.

## Production-oriented frontend

The published frontend uses compiled Tailwind CSS and includes:

- Open Graph and social sharing metadata;
- Schema.org `Person` structured data;
- canonical URL and crawler metadata;
- a generated 1200×630 social card;
- `robots.txt` and `sitemap.xml`;
- DOMPurify sanitization for LLM-derived HTML;
- bilingual recruiter-facing content and project evidence.

## Quality checks

GitHub Actions runs reusable portfolio quality checks on changes to the public site. The workflow validates:

- required sections, local assets and project links;
- PT-BR/EN translation-key completeness;
- recruiter-facing role positioning;
- Open Graph and Schema.org metadata;
- safe `target="_blank"` links;
- career-assistant safety/grounding frontend contracts;
- consistency between `src/input.css`/`index.html` and the committed Tailwind build.

## Source of truth

Project claims shown on the portfolio should remain aligned with the corresponding repository README and committed benchmark artifacts. Experimental, synthetic and backtest evidence should remain explicitly labeled as such. When a project changes materially, update the portfolio card rather than preserving stale claims.

## Repository scope

This repository contains the public portfolio website and career-assistant frontend. Individual portfolio projects have their own repositories and licensing terms.

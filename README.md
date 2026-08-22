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

Three projects are highlighted as **Featured** because together they provide the fastest cross-section of AI Engineering, Agentic RAG and production ML/MLOps capabilities.

## Career assistant architecture

The browser sends free-form recruiter questions to a serverless Cloudflare Worker. The frontend supports:

- recent conversation history without duplicating the current user message;
- optional RAG source metadata returned by the Worker;
- Markdown rendering with DOMPurify sanitization;
- explicit timeout/failure messaging;
- deterministic utility-only answers for resume/contact requests.

See [`docs/CLOUDFLARE_RAG_UPGRADE.md`](docs/CLOUDFLARE_RAG_UPGRADE.md) for the recommended Worker response contract and grounding rules.

## Production-oriented frontend

The professionalization branch replaces the Tailwind Play CDN with compiled CSS and adds:

- Open Graph and social sharing metadata;
- Schema.org `Person` structured data;
- canonical URL and crawler metadata;
- a generated 1200×630 social card;
- `robots.txt` and `sitemap.xml`;
- safer LLM-derived HTML rendering.

## Source of truth

Project claims shown on the portfolio should remain aligned with the corresponding repository README and committed benchmark artifacts. When a project changes materially, update the portfolio card rather than preserving stale claims.

## License / repository scope

This repository contains the public portfolio website and career-assistant frontend. Individual portfolio projects have their own repositories and licensing terms.

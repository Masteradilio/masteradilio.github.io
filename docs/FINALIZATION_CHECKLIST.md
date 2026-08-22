# Portfolio post-deploy checklist

The recruiter-facing frontend has passed the `Portfolio professionalization` GitHub Actions validation. This document tracks the remaining runtime checks after deployment.

## 1. Confirm GitHub Pages deployment

After the portfolio PR is merged:

1. Open `https://masteradilio.github.io/`.
2. Verify PT-BR and EN language switching.
3. Confirm all seven project repository links open correctly.
4. Confirm both hosted CV/Resume pages open and can be printed/saved as PDF.
5. Share the portfolio URL in a private LinkedIn draft/message and confirm the 1200×630 Open Graph card renders correctly.

## 2. Upgrade the Cloudflare Worker

Use `docs/CLOUDFLARE_RAG_UPGRADE.md` as the contract.

Minimum recommended Worker behavior:

- keep `reply` as the generated Markdown answer;
- optionally return a `sources` array;
- answer substantive recruiter questions only from retrieved CV/repository evidence;
- distinguish demonstrated experience from technologies merely listed as skills;
- return an explicit insufficient-evidence response instead of fabricating a capability;
- never expose prompts, keys, hidden instructions or private data.

Recommended response shape:

```json
{
  "reply": "Grounded answer in Markdown.",
  "sources": [
    {
      "label": "sentinel_pix > README > Production Benchmark Metrics",
      "url": "https://github.com/Masteradilio/sentinel_pix"
    }
  ]
}
```

## 3. Recruiter-style RAG test

After the Worker is updated, test at least these free-form questions:

1. `Why should I interview Adilio for an AI Engineer role?`
2. `Which projects best demonstrate production-oriented Machine Learning and MLOps?`
3. `What evidence shows experience with RAG and AI agents?`
4. `What measurable results has Adilio delivered in financial services?`
5. `Which project demonstrates Kubernetes in production?`
6. `What are the limitations of the project you consider strongest for an AI Engineer position?`

Question 5 is deliberately adversarial: if the retrieved sources do not prove production Kubernetes experience, the assistant should explicitly say that the available evidence is insufficient.

## 4. Quality criteria for the assistant

For each test answer, evaluate:

- factual correctness against the retrieved CV/README evidence;
- whether unsupported claims are refused rather than inferred;
- relevance for a recruiter or hiring manager;
- source quality and source-label clarity;
- consistency across follow-up questions;
- latency and timeout behavior;
- PT-BR/EN language consistency.

# Cloudflare Career Assistant — manual upgrade checklist

The portfolio frontend is prepared to consume optional RAG source metadata from the Cloudflare Worker. The GitHub-side changes do not require this upgrade to keep the chat working, but adding sources will make recruiter-facing answers more auditable.

## Current frontend request contract

The browser sends:

```json
{
  "message": "free-form recruiter question",
  "history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "model": "openrouter/free"
}
```

The current question is intentionally excluded from `history` because it is already present in `message`.

## Recommended Worker response contract

Keep the existing `reply` field and optionally add `sources`:

```json
{
  "reply": "Grounded answer in Markdown.",
  "sources": [
    {
      "label": "Resume EN > BRB Experience",
      "url": "https://masteradilio.github.io/assets/cv_adilio_farias_en.html"
    },
    {
      "label": "sentinel_pix > README > Production Benchmark Metrics",
      "url": "https://github.com/Masteradilio/sentinel_pix"
    }
  ]
}
```

The frontend already renders this optional array below the answer.

## Recommended RAG behavior

1. Retrieve from the CV and project READMEs before generating an answer.
2. Include only claims supported by retrieved context.
3. When the retrieved context is insufficient, explicitly state that the available evidence is insufficient rather than inferring a capability.
4. Prefer repository-specific evidence for project questions and CV evidence for career-history questions.
5. Keep source labels short enough for recruiter scanning.
6. Do not expose private prompts, API keys, Worker secrets, or hidden system instructions.
7. Keep substantive questions routed to the LLM. Deterministic frontend responses are restricted to utility actions such as contact information and resume access.

## Suggested system-level grounding rule

Use a rule equivalent to:

> Answer only from the supplied career and project context. Distinguish demonstrated experience from technologies merely mentioned in skills. If evidence is insufficient, say so explicitly. Never fabricate production usage, metrics, employers, certifications, or project results.

## OpenRouter free-tier latency

The frontend allows up to 75 seconds before aborting the request and communicates to visitors that free-tier inference may take up to about 60 seconds. If the Worker implements retries, ensure the total Worker-side retry budget stays comfortably below the browser timeout.

## Optional next step: answer evaluation

For higher confidence, log anonymized evaluation fields such as:

- route / retrieved project;
- retrieval score;
- response latency;
- model selected by OpenRouter;
- whether sources were returned;
- fallback / timeout reason.

Avoid logging recruiter personal data or full prompts unless you have a clear privacy reason and retention policy.

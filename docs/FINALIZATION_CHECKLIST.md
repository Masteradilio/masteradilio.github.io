# Portfolio finalization checklist

This checklist is intentionally short. The code changes are already prepared in the review branch.

## 1. Run the GitHub validation workflow once

In GitHub:

1. Open the repository `Masteradilio/masteradilio.github.io`.
2. Open **Actions**.
3. Select **Portfolio professionalization**.
4. Click **Run workflow**.
5. The workflow itself checks out `portfolio-professionalization-20260822`, so no code editing is required.
6. Wait for `patch-build-verify` to finish successfully.

The workflow will:

- apply the final project-card evidence patch;
- align hosted PT-BR and EN CV positioning with `AI Engineer | Senior Data Scientist`;
- rebuild production Tailwind CSS;
- regenerate the Open Graph social image;
- run deterministic assertions against stale claims and required recruiter-facing content;
- commit the generated files back to the review branch.

If **Run workflow** is not visible, verify that GitHub Actions are enabled under repository **Settings → Actions → General**.

## 2. Do not merge manually yet

After the workflow is green, return to the ChatGPT conversation and report that it completed successfully. The PR can then be re-inspected and merged through the connected GitHub integration.

## 3. Cloudflare Worker upgrade after the frontend merge

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

## 4. Post-deploy recruiter test

After the PR is merged and the Worker is updated, test at least these free-form questions:

1. `Why should I interview Adilio for an AI Engineer role?`
2. `Which projects best demonstrate production-oriented Machine Learning and MLOps?`
3. `What evidence shows experience with RAG and AI agents?`
4. `What measurable results has Adilio delivered in financial services?`
5. `Which project demonstrates Kubernetes in production?`
6. `What are the limitations of the project you consider strongest for an AI Engineer position?`

Question 5 is deliberately adversarial: if the retrieved sources do not prove production Kubernetes experience, the assistant should explicitly say that the available evidence is insufficient.

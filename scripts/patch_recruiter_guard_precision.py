from pathlib import Path

worker = Path('cloudflare/adilio-career-assistant.js')
text = worker.read_text(encoding='utf-8')
print('FIT_RELIABILITY_PATCH_START')


def replace_between(src: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = src.find(start_marker)
    if start < 0:
        raise SystemExit(f'start marker not found: {start_marker}')
    end = src.find(end_marker, start)
    if end < 0:
        raise SystemExit(f'end marker not found: {end_marker}')
    return src[:start] + replacement.rstrip() + '\n\n' + src[end:]


# Version.
text = text.replace('v2026.14: recruiter-grade guard precision and diagnostics.', 'v2026.15: recruiter-fit context minimization and reliability.', 1)
text = text.replace("const SERVICE_VERSION = '2026.14';", "const SERVICE_VERSION = '2026.15';", 1)

# Recruiter-fit questions need one inspectable portfolio proof, not three unrelated READMEs.
featured = "const AI_ENGINEER_FEATURED = ['squad_forge_SE', 'rag_agent_datasus', 'sentinel_pix'];"
fit_decl = featured + "\nconst AI_ENGINEER_FIT = ['squad_forge_SE'];"
if 'const AI_ENGINEER_FIT' not in text:
    if featured not in text:
        raise SystemExit('AI_ENGINEER_FEATURED anchor not found')
    text = text.replace(featured, fit_decl, 1)

# Stable semantic helper used by routing, prompting and validation.
if 'function isFitQuestion(question)' not in text:
    anchor = 'function classifyEvidencePlan(question) {'
    helper = r'''function isFitQuestion(question) {
  const q = normalizeText(question);
  return /\b(interview|hire|hiring|fit|candidate|role|entrevista|contratar|vaga|candidato)\b/.test(q);
}

'''
    if anchor not in text:
        raise SystemExit('classifyEvidencePlan anchor not found')
    text = text.replace(anchor, helper + anchor, 1)

# Make the classifier reuse the same fit definition.
text = text.replace(
    "  const asksFit = /\\b(interview|hire|hiring|fit|candidate|role|entrevista|contratar|vaga|candidato)\\b/.test(q);",
    "  const asksFit = isFitQuestion(question);",
    1
)

select_repos = r'''function selectRepos(question, history) {
  const explicitCurrent = [...new Set(directRepoMentions(question))];
  if (explicitCurrent.length) return explicitCurrent.slice(0, 3);

  const q = normalizeText(question);

  // Recruiter-fit questions are intentionally low-context: professional CV facts
  // are primary and Squad Forge SE is the single supplemental portfolio proof.
  // This reduces cross-project overclaim risk and improves completion reliability.
  if (isFitQuestion(question)) return AI_ENGINEER_FIT;

  if (/\b(mlops|mlflow|model lifecycle|model monitoring|drift|feature store|production-oriented machine learning|production oriented machine learning)\b/.test(q)) return MLOPS_PORTFOLIO;
  if (/\b(rag|retrieval|ai agents?|agentic|agentes? de ia|llm|langgraph|chromadb|bm25|ontology|guardrail)\b/.test(q)) return RAG_AGENT_PORTFOLIO;
  if (/\b(credit|credito|pd|lgd|ead|ecl|ifrs|scorecard|scoring)\b/.test(q)) return ['credit_risk_model', 'credit_scoring_model'];
  if (/\b(fraud|fraude|pix|anti-fraud|antifraude|redis|isolation forest)\b/.test(q)) return ['sentinel_pix'];
  if (/\b(time series|forecast|series temporais|previsao|quantitative|bilstm|tcn)\b/.test(q)) return ['time_series_predict'];
  if (/\b(ai engineer|engenheiro de ia|strongest|mais forte|best project|melhor projeto)\b/.test(q)) return AI_ENGINEER_FEATURED;

  const words = q.split(/\s+/).filter(Boolean);
  const vagueFollowUp = words.length <= 7 && /^(why|how|what about|and|e|por que|porque|como|e quanto)\b/.test(q);
  if (vagueFollowUp) {
    const historical = [...new Set(directRepoMentions(history.slice(-4).map(item => item.content).join(' ')))];
    if (historical.length) return historical.slice(0, 3);
  }

  return AI_ENGINEER_FEATURED;
}'''
text = replace_between(text, 'function selectRepos(question, history) {', 'function sanitizeGithubPath(path) {', select_repos)

plan_instruction = r'''function evidencePlanInstruction(plan, question) {
  const q = normalizeText(question);
  const lines = [];
  if (plan.mode === 'professional') lines.push('For this question, use PROFESSIONAL EVIDENCE only. Do not introduce portfolio-project claims unless the user explicitly asks for them.');
  else if (plan.mode === 'portfolio') {
    lines.push('For this question, use PORTFOLIO EVIDENCE only. Do not use employer metrics, employer names or professional achievements to describe the portfolio projects.');
    lines.push('A portfolio project can be production-oriented in architecture without being deployed in an employer production environment. Preserve that distinction explicitly when relevant.');
  } else lines.push('For this question, lead with PROFESSIONAL EVIDENCE, then use PORTFOLIO EVIDENCE as additional proof. Phrase the boundary clearly.');

  if (isFitQuestion(question)) {
    lines.push('This is a recruiter-fit question. Start with a direct hiring recommendation grounded in PROFESSIONAL EVIDENCE. Use 2-4 of the strongest professional facts, then at most one short paragraph or bullet about Squad Forge SE as supplemental inspectable portfolio evidence.');
    lines.push('Target 90-150 words. Do not mention unrelated portfolio repositories. Do not turn portfolio architecture into employer production experience.');
  }
  if (/\b(experience|experiencia|evidence shows|evidencia)\b/.test(q)) lines.push('Because the user asks about experience/evidence, present professional evidence first and portfolio demonstrations second.');
  if (/\b(mlops|production-oriented machine learning|production oriented machine learning)\b/.test(q)) {
    lines.push('For portfolio MLOps, Sentinel-PIX may be described from its own README as a portfolio demonstration with synthetic simulation/customer data, FastAPI, Redis/PostgreSQL feature stores, MLflow, SHAP and drift monitoring. Do not attach BRB metrics to Sentinel-PIX.');
    lines.push('Squad Forge SE is an autonomous software-engineering control plane; do not describe it as an ML model lifecycle or drift-monitoring platform unless its own evidence says so.');
  }
  if (/\bkubernetes\b/.test(q)) lines.push('If Kubernetes is not explicitly present in canonical project evidence, answer with insufficient evidence. Docker, FastAPI, MLOps or AWS do not imply Kubernetes.');
  return lines.join('\n');
}'''
text = replace_between(text, 'function evidencePlanInstruction(plan, question) {', 'function dedupeSources(sources) {', plan_instruction)

lead_guard = r'''function missesRequiredProfessionalLead(text, plan, question) {
  if (plan.mode !== 'combined') return false;
  const q = normalizeText(question);
  if (!isFitQuestion(question) && !/\b(experience|evidence shows|background|experiencia|evidencia|historico)\b/.test(q)) return false;

  const answer = normalizeText(text);
  const hasEmployerOrDomain = /\b(?:brb|banco de brasilia|banpara|financial[- ]services|banking|setor financeiro)\b/.test(answer);
  const hasTenure = /\b(?:15\+?\s*years|over\s+15\s+years|more\s+than\s+15\s+years|15\s+anos)\b/.test(answer);
  const hasProfessionalLabel = /\b(?:professional experience|professional evidence|experiencia profissional|aws certified|msc)\b/.test(answer);
  return !(hasEmployerOrDomain || hasTenure || hasProfessionalLabel);
}'''
text = replace_between(text, 'function missesRequiredProfessionalLead(text, plan, question) {', 'function validationIssues(text, plan, question) {', lead_guard)

# Fit repairs get a focused contract and enough token budget for reasoning-model providers.
text = text.replace(
    "  const limitationsQuestion = /\\b(limitations?|limitações|limitacoes)\\b/.test(q);",
    "  const limitationsQuestion = /\\b(limitations?|limitações|limitacoes)\\b/.test(q);\n  const fitQuestion = isFitQuestion(question);",
    1
)
focus_anchor = "  if (limitationsQuestion) {\n    focusRules.push('Answer with the project name and 2-4 concrete limitations supported by its canonical evidence. Distinguish portfolio/local-first evidence from employer production deployment.');\n    focusRules.push('Target 60-140 words.');\n  }"
focus_replacement = focus_anchor + "\n  if (fitQuestion) {\n    focusRules.push('This is a recruiter-fit answer. Lead with professional evidence and a direct recommendation. Use only the strongest 2-4 professional facts and, if useful, one concise Squad Forge SE portfolio point.');\n    focusRules.push('Target 90-150 words. Do not mention DataSUS, Sentinel-PIX or other unrelated repositories for this fit answer.');\n  }"
if "Do not mention DataSUS, Sentinel-PIX" not in text:
    if focus_anchor not in text:
        raise SystemExit('fit repair focus anchor not found')
    text = text.replace(focus_anchor, focus_replacement, 1)

text = text.replace(
    "{ messages: repairMessages, temperature: 0, max_tokens: abstentionQuestion ? 260 : 520 },",
    "{ messages: repairMessages, temperature: 0, max_tokens: abstentionQuestion ? 260 : (fitQuestion ? 1100 : 520) },",
    1
)

# Initial fit generation also gets additional room so reasoning-model providers do
# not consume the whole completion budget before emitting the final answer.
text = text.replace(
    "        const payload = { messages, temperature: 0.1, max_tokens: 700 };",
    "        const payload = { messages, temperature: 0.1, max_tokens: isFitQuestion(question) ? 1000 : 700 };",
    1
)

worker.write_text(text, encoding='utf-8')
print('FIT_RELIABILITY_PATCH_COMPLETE')

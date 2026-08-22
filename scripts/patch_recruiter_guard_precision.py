from pathlib import Path

worker = Path('cloudflare/adilio-career-assistant.js')
text = worker.read_text(encoding='utf-8')
print('FINAL_PRECISION_PATCH_START')


def replace_between(src: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = src.find(start_marker)
    if start < 0:
        raise SystemExit(f'start marker not found: {start_marker}')
    end = src.find(end_marker, start)
    if end < 0:
        raise SystemExit(f'end marker not found: {end_marker}')
    return src[:start] + replacement.rstrip() + '\n\n' + src[end:]


text = text.replace('v2026.15: recruiter-fit context minimization and reliability.', 'v2026.16: final recruiter-facing factual precision.', 1)
text = text.replace("const SERVICE_VERSION = '2026.15';", "const SERVICE_VERSION = '2026.16';", 1)

rule14 = "14. For rag_agent_datasus, do not call the RAG pipeline production-grade or production-ready unless its canonical README explicitly supports that wording."
extra_rules = rule14 + "\n15. When answering an explicit named-technology question such as LlamaIndex, Apache Kafka or Kubernetes, explicitly name that technology in the final answer even when evidence is absent.\n16. Do not describe Sentinel-PIX as local-first; its canonical qualifiers are portfolio demonstration and synthetic simulation/customer data.\n17. Do not summarize Adilio's RAG or AI-agent experience as deployed/deploying unless supplied evidence explicitly supports deployment; BRB supports implemented, BANPARÁ supports developed, and public repositories are portfolio evidence."
if '15. When answering an explicit named-technology question' not in text:
    if rule14 not in text:
        raise SystemExit('system rule 14 anchor not found')
    text = text.replace(rule14, extra_rules, 1)

instruction_block = r'''function evidencePlanInstruction(plan, question) {
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
  if (/\bkubernetes\b/.test(q)) lines.push('If Kubernetes is not explicitly present in canonical project evidence, answer with insufficient evidence. Docker, FastAPI, MLOps or AWS do not imply Kubernetes. Explicitly name Kubernetes in the answer.');
  if (/\bllamaindex\b/.test(q)) lines.push('Answer the LlamaIndex question explicitly and name LlamaIndex in the final answer. If it is absent from the canonical README, say that directly and mention the supported orchestration/retrieval stack instead.');
  if (/\bapache kafka\b|\bkafka\b/.test(q)) lines.push('Answer the Apache Kafka question explicitly and name Kafka in the final answer. If it is absent from the canonical README, say that directly.');
  if (/\b(limitations?|limitações|limitacoes)\b/.test(q)) lines.push('For limitations, use only explicit project qualifiers, documented scope, or clearly missing deployment/validation evidence. Do not infer that an architecture lacks scalability, throughput, reliability or enterprise readiness unless the canonical README explicitly states that limitation.');
  return lines.join('\n');
}'''
text = replace_between(text, 'function evidencePlanInstruction(plan, question) {', 'function dedupeSources(sources) {', instruction_block)

portfolio_block = r'''function containsKnownPortfolioOverclaim(text) {
  const q = normalizeText(text);
  const sentinelBad = q.includes('sentinel') && (
    q.includes('deployed a real-time fraud') ||
    q.includes("brazil's pix instant payment network") ||
    q.includes('brazil’s pix instant payment network') ||
    q.includes('97% recall') ||
    q.includes('weekly mlops pipeline') ||
    q.includes('local-first') ||
    q.includes('local first')
  );

  const squadPositivePatterns = [
    /squad forge.{0,140}\b(?:is|acts as|serves as|implements|includes|features|provides|supports|automates|manages)\b(?!\s+(?:not|no)\b).{0,90}\b(?:ml model lifecycle management|drift detection|model drift)\b/i,
    /squad forge.{0,100}\b(?:ml model lifecycle management|drift detection|model drift)\b.{0,80}\b(?:capability|feature|platform|pipeline)\b/i,
    /\b(?:ml model lifecycle management|drift detection|model drift)\b.{0,100}\b(?:implemented|provided|supported|automated)\b.{0,80}squad forge/i
  ];
  const squadBad = squadPositivePatterns.some(pattern => pattern.test(q));

  const datasusBad = q.includes('datasus') && (
    q.includes('deployed in public health') ||
    q.includes('production-grade rag') ||
    q.includes('production grade rag') ||
    q.includes('production-ready rag') ||
    q.includes('production ready rag')
  );
  const ontologyBad = q.includes('ontology rag guardrail') && q.includes('deployed') && q.includes('enterprise security');
  return sentinelBad || squadBad || datasusBad || ontologyBad;
}'''
text = replace_between(text, 'function containsKnownPortfolioOverclaim(text) {', 'function evidenceClauses(text) {', portfolio_block)

attr_block = r'''function containsProfessionalAttributionError(text) {
  const clauses = evidenceClauses(text);
  const bancoDoBrasilMetric = /\b(?:pix|fraud-prevention model|fraud prevention model|97% recall)\b/i;
  const bancoMetricBad = clauses.some(clause => /\bbanco do brasil\b/i.test(clause) && bancoDoBrasilMetric.test(clause));

  const brbEmployer = /\b(?:brb|banco de brasilia)\b/i;
  const banparaEmployer = /\bbanpara\b/i;
  const llmRagAgent = 'llm|rag|ai-agent|ai agent';

  const brbLlmDeploymentUpgrade = clauses.some(clause => hasDirectDeploymentUpgrade(clause, brbEmployer, llmRagAgent));
  const banparaRagDeploymentUpgrade = clauses.some(clause => hasDirectDeploymentUpgrade(clause, banparaEmployer, 'rag'));
  const brbPixDeploymentUpgrade = clauses.some(clause =>
    brbEmployer.test(clause) &&
    /\bdeploy(?:ed|ment)?\b.{0,42}\b(?:pix|fraud(?:-prevention| prevention)? model)\b|\b(?:pix|fraud(?:-prevention| prevention)? model)\b.{0,42}\bdeploy(?:ed|ment)?\b/i.test(clause)
  );

  const ragAgentSummaryDeploymentUpgrade = clauses.some(clause => {
    if (/\b(?:not|never|without|no evidence (?:of|for))\b.{0,30}\bdeploy(?:ed|ing|ment)?\b/i.test(clause)) return false;
    return /\bdeploy(?:ed|ing|ment)?\b.{0,48}\b(?:rag|ai[- ]?agent|agentic)\b|\b(?:rag|ai[- ]?agent|agentic)\b.{0,48}\bdeploy(?:ed|ing|ment)?\b/i.test(clause);
  });

  return bancoMetricBad || brbLlmDeploymentUpgrade || banparaRagDeploymentUpgrade || brbPixDeploymentUpgrade || ragAgentSummaryDeploymentUpgrade;
}'''
text = replace_between(text, 'function containsProfessionalAttributionError(text) {', 'function containsDataScopeOverclaim(text) {', attr_block)

subject_block = r'''function missesExplicitTechnologyReference(text, question) {
  const q = normalizeText(question);
  const answer = normalizeText(text);
  if (/\bllamaindex\b/.test(q) && !/\bllamaindex\b/.test(answer)) return true;
  if (/\b(?:apache kafka|kafka)\b/.test(q) && !/\bkafka\b/.test(answer)) return true;
  if (/\bkubernetes\b/.test(q) && !/\bkubernetes\b/.test(answer)) return true;
  return false;
}

function validationIssues(text, plan, question) {
  const issues = [];
  if (looksIncompleteAnswer(text, question, plan)) issues.push('incomplete');
  if (containsReasoningLeak(text)) issues.push('reasoning_leak');
  if (containsPortfolioProfessionalMix(text, plan)) issues.push('portfolio_professional_mix');
  if (containsKnownPortfolioOverclaim(text)) issues.push('portfolio_overclaim');
  if (containsProfessionalAttributionError(text)) issues.push('professional_attribution');
  if (containsDataScopeOverclaim(text)) issues.push('data_scope');
  if (missesRequiredProfessionalLead(text, plan, question)) issues.push('professional_lead_missing');
  if (missesExplicitTechnologyReference(text, question)) issues.push('technology_not_addressed');
  return issues;
}

function needsRepair(text, plan, question) {
  return validationIssues(text, plan, question).length > 0;
}'''
text = replace_between(text, 'function validationIssues(text, plan, question) {', 'function gatewayCredentials(env) {', subject_block)

old_abstention = "focusRules.push('This is an evidence-boundary question. Answer the exact question in the first sentence. If the evidence does not prove the claim, explicitly say that sufficient evidence was not found; then mention only the closest supported evidence.');"
new_abstention = "focusRules.push('This is an evidence-boundary question. Answer the exact question in the first sentence and explicitly repeat the named technology or boundary from the user question. If the evidence does not prove the claim, say that directly; then mention only the closest supported evidence.');"
if old_abstention in text:
    text = text.replace(old_abstention, new_abstention, 1)
elif new_abstention not in text:
    raise SystemExit('abstention repair anchor not found')

old_limits = "focusRules.push('Answer with the project name and 2-4 concrete limitations supported by its canonical evidence. Distinguish portfolio/local-first evidence from employer production deployment.');"
new_limits = "focusRules.push('Answer with the project name and 2-4 concrete limitations supported by its canonical evidence. Use explicit qualifiers or missing deployment/validation evidence only; do not infer lack of scalability, throughput or enterprise reliability. Distinguish portfolio evidence from employer production deployment.');"
if old_limits in text:
    text = text.replace(old_limits, new_limits, 1)
elif new_limits not in text:
    raise SystemExit('limitations repair anchor not found')

worker.write_text(text, encoding='utf-8')
print('FINAL_PRECISION_PATCH_COMPLETE')

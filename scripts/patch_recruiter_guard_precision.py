from pathlib import Path

worker = Path('cloudflare/adilio-career-assistant.js')
text = worker.read_text(encoding='utf-8')
print('GUARD_PRECISION_PATCH_START')

text = text.replace('v2026.13: recruiter-grade multi-gateway resilience.', 'v2026.14: recruiter-grade guard precision and diagnostics.', 1)
text = text.replace("const SERVICE_VERSION = '2026.13';", "const SERVICE_VERSION = '2026.14';", 1)
text = text.replace("const GATEWAY_TIMEOUTS_MS = { vercel: 16000, openrouter: 14000, huggingface: 14000, repair: 9000 };", "const GATEWAY_TIMEOUTS_MS = { vercel: 16000, openrouter: 14000, huggingface: 14000, repair: 12000 };", 1)

rule12 = "12. For BANPARÁ RAG work, preserve the supported verb 'developed'; do not upgrade it to 'deployed' unless the professional evidence explicitly changes."
rule13 = rule12 + "\n13. For the BRB PIX fraud model, preserve the supported wording 'led end-to-end development'; do not claim production deployment unless PROFESSIONAL EVIDENCE explicitly supports it.\n14. For rag_agent_datasus, do not call the RAG pipeline production-grade or production-ready unless its canonical README explicitly supports that wording."
if rule12 not in text:
    raise SystemExit('system rule anchor not found')
text = text.replace(rule12, rule13, 1)

old_portfolio = '''function containsKnownPortfolioOverclaim(text) {
  const q = normalizeText(text);
  const sentinelBad = q.includes('sentinel') && (q.includes('deployed a real-time fraud') || q.includes("brazil's pix instant payment network") || q.includes('brazil’s pix instant payment network') || q.includes('97% recall') || q.includes('weekly mlops pipeline'));
  const squadBad = q.includes('squad forge') && (q.includes('ml model lifecycle management') || q.includes('drift detection') || q.includes('model drift'));
  const datasusBad = q.includes('datasus') && q.includes('deployed in public health');
  const ontologyBad = q.includes('ontology rag guardrail') && q.includes('deployed') && q.includes('enterprise security');
  return sentinelBad || squadBad || datasusBad || ontologyBad;
}
'''
new_portfolio = r'''function containsKnownPortfolioOverclaim(text) {
  const q = normalizeText(text);
  const sentinelBad = q.includes('sentinel') && (
    q.includes('deployed a real-time fraud') ||
    q.includes("brazil's pix instant payment network") ||
    q.includes('brazil’s pix instant payment network') ||
    q.includes('97% recall') ||
    q.includes('weekly mlops pipeline')
  );

  // Only reject affirmative claims that Squad Forge provides ML lifecycle/drift
  // capabilities. Negative limitation statements such as "does not include drift
  // detection" are valid and must not be treated as overclaims.
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
}
'''
if old_portfolio not in text:
    raise SystemExit('containsKnownPortfolioOverclaim block not found')
text = text.replace(old_portfolio, new_portfolio, 1)

old_attr = '''function containsProfessionalAttributionError(text) {
  const q = normalizeText(text);
  const metric = '(pix|fraud-prevention model|fraud prevention model|97% recall)';
  const bancoAsSubject = new RegExp(`(?:at|no|na)\\s+banco do brasil.{0,90}${metric}`, 'i');
  const bancoPossessive = new RegExp(`banco do brasil(?:\\'s|’s)?.{0,90}${metric}`, 'i');
  const metricAssignedToBanco = new RegExp(`${metric}.{0,90}(?:at|no|na)\\s+banco do brasil`, 'i');
  const brbLlmDeploymentUpgrade = /(?:brb|banco de brasilia).{0,180}\\bdeploy(?:ed|ment)?\\b.{0,80}\\b(?:llm|rag|ai-agent|ai agent)\\b|\\bdeploy(?:ed|ment)?\\b.{0,80}\\b(?:llm|rag|ai-agent|ai agent)\\b.{0,180}(?:brb|banco de brasilia)/i;
  const banparaRagDeploymentUpgrade = /banpara.{0,180}\\bdeploy(?:ed|ment)?\\b.{0,80}\\brag\\b|\\bdeploy(?:ed|ment)?\\b.{0,80}\\brag\\b.{0,180}banpara/i;
  return bancoAsSubject.test(q) || bancoPossessive.test(q) || metricAssignedToBanco.test(q) || brbLlmDeploymentUpgrade.test(q) || banparaRagDeploymentUpgrade.test(q);
}
'''
new_attr = r'''function evidenceClauses(text) {
  return normalizeText(text)
    .split(/\n+|(?<=[.!?])\s+/)
    .map(part => part.trim())
    .filter(Boolean);
}

function hasDirectDeploymentUpgrade(clause, employerPattern, capabilityPattern) {
  if (!employerPattern.test(clause)) return false;
  if (/\b(?:not|never|without|no evidence (?:of|for))\b.{0,24}\bdeploy(?:ed|ment)?\b/i.test(clause)) return false;
  const forward = new RegExp(`\\bdeploy(?:ed|ment)?\\b.{0,36}\\b(?:${capabilityPattern})\\b`, 'i');
  const reverse = new RegExp(`\\b(?:${capabilityPattern})\\b.{0,36}\\bdeploy(?:ed|ment)?\\b`, 'i');
  return forward.test(clause) || reverse.test(clause);
}

function containsProfessionalAttributionError(text) {
  const clauses = evidenceClauses(text);
  const bancoDoBrasilMetric = /\b(?:pix|fraud-prevention model|fraud prevention model|97% recall)\b/i;

  // Scope employer attribution to individual sentences/bullets. This prevents a
  // deployment verb belonging to one project from contaminating another fact in
  // the next sentence.
  const bancoMetricBad = clauses.some(clause => /\bbanco do brasil\b/i.test(clause) && bancoDoBrasilMetric.test(clause));

  const brbEmployer = /\b(?:brb|banco de brasilia)\b/i;
  const banparaEmployer = /\bbanpara\b/i;
  const llmRagAgent = 'llm|rag|ai-agent|ai agent';

  const brbLlmDeploymentUpgrade = clauses.some(clause => hasDirectDeploymentUpgrade(clause, brbEmployer, llmRagAgent));
  const banparaRagDeploymentUpgrade = clauses.some(clause => hasDirectDeploymentUpgrade(clause, banparaEmployer, 'rag'));

  // The canonical BRB evidence supports leading end-to-end development of the
  // PIX model, not a stronger deployment claim.
  const brbPixDeploymentUpgrade = clauses.some(clause =>
    brbEmployer.test(clause) &&
    /\bdeploy(?:ed|ment)?\b.{0,42}\b(?:pix|fraud(?:-prevention| prevention)? model)\b|\b(?:pix|fraud(?:-prevention| prevention)? model)\b.{0,42}\bdeploy(?:ed|ment)?\b/i.test(clause)
  );

  return bancoMetricBad || brbLlmDeploymentUpgrade || banparaRagDeploymentUpgrade || brbPixDeploymentUpgrade;
}
'''
if old_attr not in text:
    raise SystemExit('containsProfessionalAttributionError block not found')
text = text.replace(old_attr, new_attr, 1)

old_needs = '''function needsRepair(text, plan, question) {
  return looksIncompleteAnswer(text, question, plan) || containsReasoningLeak(text) || containsPortfolioProfessionalMix(text, plan) || containsKnownPortfolioOverclaim(text) || containsProfessionalAttributionError(text) || containsDataScopeOverclaim(text) || missesRequiredProfessionalLead(text, plan, question);
}
'''
new_needs = '''function validationIssues(text, plan, question) {
  const issues = [];
  if (looksIncompleteAnswer(text, question, plan)) issues.push('incomplete');
  if (containsReasoningLeak(text)) issues.push('reasoning_leak');
  if (containsPortfolioProfessionalMix(text, plan)) issues.push('portfolio_professional_mix');
  if (containsKnownPortfolioOverclaim(text)) issues.push('portfolio_overclaim');
  if (containsProfessionalAttributionError(text)) issues.push('professional_attribution');
  if (containsDataScopeOverclaim(text)) issues.push('data_scope');
  if (missesRequiredProfessionalLead(text, plan, question)) issues.push('professional_lead_missing');
  return issues;
}

function needsRepair(text, plan, question) {
  return validationIssues(text, plan, question).length > 0;
}
'''
if old_needs not in text:
    raise SystemExit('needsRepair block not found')
text = text.replace(old_needs, new_needs, 1)

old_repair_tail = '''    const repaired = stripModelArtifacts(response.data?.choices?.[0]?.message?.content);
    const finishReason = response.data?.choices?.[0]?.finish_reason;
    if (!repaired || finishReason === 'length' || needsRepair(repaired, plan, question)) continue;

    return {
'''
new_repair_tail = '''    const repaired = stripModelArtifacts(response.data?.choices?.[0]?.message?.content);
    const finishReason = response.data?.choices?.[0]?.finish_reason;
    const repairIssues = repaired ? validationIssues(repaired, plan, question) : ['empty_answer'];
    if (finishReason === 'length') repairIssues.unshift('finish_length');
    attempts.push({
      stage: 'validate-repair',
      gateway: candidate.gateway,
      ok: repairIssues.length === 0,
      status: response.status || 200,
      error: repairIssues.length ? `guard_${repairIssues.join('+')}` : null
    });
    if (repairIssues.length) continue;

    return {
'''
if old_repair_tail not in text:
    raise SystemExit('repair validation anchor not found')
text = text.replace(old_repair_tail, new_repair_tail, 1)

old_normal = '''        let reply = stripModelArtifacts(modelMessage.content);
        const finishReason = response.data?.choices?.[0]?.finish_reason;
        let servedGateway = candidate.gateway;
        let servedModel = response.data?.model || candidate.model;
        if (finishReason === 'length' || needsRepair(reply, plan, question)) {
'''
new_normal = '''        let reply = stripModelArtifacts(modelMessage.content);
        const finishReason = response.data?.choices?.[0]?.finish_reason;
        let servedGateway = candidate.gateway;
        let servedModel = response.data?.model || candidate.model;
        const generationIssues = reply ? validationIssues(reply, plan, question) : ['empty_answer'];
        if (finishReason === 'length') generationIssues.unshift('finish_length');
        attempts.push({
          stage: 'validate',
          gateway: candidate.gateway,
          ok: generationIssues.length === 0,
          status: response.status || 200,
          error: generationIssues.length ? `guard_${generationIssues.join('+')}` : null
        });
        if (generationIssues.length) {
'''
if old_normal not in text:
    raise SystemExit('normal validation anchor not found')
text = text.replace(old_normal, new_normal, 1)

old_tool = '''            let reply = stripModelArtifacts(follow.data?.choices?.[0]?.message?.content);
            const finishReason = follow.data?.choices?.[0]?.finish_reason;
            let servedGateway = candidate.gateway;
            let servedModel = follow.data?.model || candidate.model;
            if (finishReason === 'length' || needsRepair(reply, plan, question)) {
'''
new_tool = '''            let reply = stripModelArtifacts(follow.data?.choices?.[0]?.message?.content);
            const finishReason = follow.data?.choices?.[0]?.finish_reason;
            let servedGateway = candidate.gateway;
            let servedModel = follow.data?.model || candidate.model;
            const toolIssues = reply ? validationIssues(reply, plan, question) : ['empty_answer'];
            if (finishReason === 'length') toolIssues.unshift('finish_length');
            attempts.push({
              stage: 'validate-tool',
              gateway: candidate.gateway,
              ok: toolIssues.length === 0,
              status: follow.status || 200,
              error: toolIssues.length ? `guard_${toolIssues.join('+')}` : null
            });
            if (toolIssues.length) {
'''
if old_tool not in text:
    raise SystemExit('tool validation anchor not found')
text = text.replace(old_tool, new_tool, 1)

old_wording = "Keep wording factual. For BRB LLM/RAG/AI-agent work, use implemented rather than deployed. For BANPARÁ RAG work, use developed rather than deployed."
new_wording = old_wording + " For the BRB PIX fraud model, say that Adilio led end-to-end development rather than claiming deployment. Do not describe rag_agent_datasus as production-grade/production-ready RAG unless its canonical evidence says so."
if old_wording not in text:
    raise SystemExit('repair wording anchor not found')
text = text.replace(old_wording, new_wording, 1)

worker.write_text(text, encoding='utf-8')
print('GUARD_PRECISION_PATCH_COMPLETE')

# trigger: 2026-08-22

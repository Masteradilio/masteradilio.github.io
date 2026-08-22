from pathlib import Path

worker = Path('cloudflare/adilio-career-assistant.js')
text = worker.read_text(encoding='utf-8')
print('RELIABILITY_PATCH_START')


def replace_once(old, new, label):
    global text
    if old in text:
        text = text.replace(old, new, 1)
        print(f'PATCH_OK: {label}')
    elif new in text:
        print(f'PATCH_NOTE: {label} already applied')
    else:
        raise SystemExit(f'PATCH_FAIL: {label} anchor not found')

# 1) Explicit standalone questions should not inherit previous assistant/user turns.
old = """      const history = sanitizeHistory(body?.history);\n      const plan = classifyEvidencePlan(question);"""
new = """      const history = sanitizeHistory(body?.history);\n      const normalizedQuestion = normalizeText(question);\n      const questionWords = normalizedQuestion.split(/\\s+/).filter(Boolean);\n      const vagueFollowUp = questionWords.length <= 7 && /^(why|how|what about|and|e|por que|porque|como|e quanto)\\b/.test(normalizedQuestion);\n      const conversationalHistory = vagueFollowUp ? history : [];\n      const plan = classifyEvidencePlan(question);"""
replace_once(old, new, 'explicit-question history isolation')

replace_once(
    "const messages = [{ role: 'system', content: systemParts.join('\\n\\n==============================\\n\\n') }, ...history, { role: 'user', content: question }];",
    "const messages = [{ role: 'system', content: systemParts.join('\\n\\n==============================\\n\\n') }, ...conversationalHistory, { role: 'user', content: question }];",
    'LLM history isolation'
)

# 2) CV source detection must recognize common recruiter-fit claims.
old_markers = "const markers = ['brb','banpara','banco do brasil','compass','professional','profissional','financial services','setor financeiro','97%','700,000','700 mil','41%','27%'];"
new_markers = "const markers = ['brb','banpara','banco do brasil','compass','professional','profissional','financial services','setor financeiro','15+ years','15 years','aws certified','certification','certifications','msc','education','97%','700,000','700 mil','41%','27%'];"
replace_once(old_markers, new_markers, 'professional source markers')

old_fallback = """  if (!selected.length) {\n    if (plan.includeProfessional && !plan.includePortfolio) return [CV_SOURCES[language]];\n    const repoOnly = candidateSources.filter(s => s.kind === 'repo');\n    if (repoOnly.length) return repoOnly.slice(0, 2);\n    if (plan.includeProfessional) return [CV_SOURCES[language]];\n  }"""
new_fallback = """  if (!selected.length) {\n    // Never invent repository attribution when a combined/professional answer is too vague.\n    if (plan.includeProfessional) return [CV_SOURCES[language]];\n    const repoOnly = candidateSources.filter(s => s.kind === 'repo');\n    if (repoOnly.length) return repoOnly.slice(0, 2);\n  }"""
replace_once(old_fallback, new_fallback, 'safe source fallback')

# 3) Reject fragments and underdeveloped recruiter answers, not merely <20-char strings.
start = text.find('function containsDataScopeOverclaim(text) {')
end = text.find('async function callOpenRouter(', start)
if start < 0 or end < 0:
    raise SystemExit('PATCH_FAIL: repair validation block not found')
old_block = text[start:end]
new_block = r'''function containsDataScopeOverclaim(text) {
  const q = normalizeText(text);
  return q.includes('datasus') && (q.includes('synthetic simulation') || q.includes('synthetic project') || q.includes('synthetic data'));
}

function answerWordCount(text) {
  return String(text || '').trim().split(/\s+/).filter(Boolean).length;
}

function minimumAnswerWords(question, plan) {
  const q = normalizeText(question);
  if (/\b(kubernetes|llamaindex|apache kafka|security boundary)\b/.test(q) || /^(does|is|are|can|did|has|have)\b/.test(q)) return 18;
  if (/\b(interview|hire|hiring|experience|evidence shows|measurable results|best demonstrate|limitations|candidate|role)\b/.test(q)) return 55;
  return plan.mode === 'portfolio' ? 32 : 42;
}

function looksIncompleteAnswer(text, question, plan) {
  const clean = String(text || '').trim();
  if (!clean) return true;
  if (answerWordCount(clean) < minimumAnswerWords(question, plan)) return true;
  return /\b(of|and|with|for|to|a|an|the|his|her|their|from|because|including|such as)\s*[:;,\-]?\s*$/i.test(clean);
}

function missesRequiredProfessionalLead(text, plan, question) {
  if (plan.mode !== 'combined') return false;
  const q = normalizeText(question);
  if (!/\b(interview|hire|hiring|experience|evidence shows|background|candidate|role)\b/.test(q)) return false;
  const answer = normalizeText(text);
  const markers = ['brb','banpara','financial services','15+ years','15 years','professional','aws certified','msc'];
  return !markers.some(marker => answer.includes(normalizeText(marker)));
}

function needsRepair(text, plan, question) {
  return looksIncompleteAnswer(text, question, plan) || containsReasoningLeak(text) || containsPortfolioProfessionalMix(text, plan) || containsKnownPortfolioOverclaim(text) || containsProfessionalAttributionError(text) || containsDataScopeOverclaim(text) || missesRequiredProfessionalLead(text, plan, question);
}

'''
text = text[:start] + new_block + text[end:]
print('PATCH_OK: completeness validation')

# Update every repair check to include the current question.
text = text.replace('!needsRepair(repaired, plan)', '!needsRepair(repaired, plan, question)')
text = text.replace('needsRepair(reply, plan)', 'needsRepair(reply, plan, question)')
print('PATCH_OK: repair call signatures')

# 4) Repair should rebuild incomplete responses from supplied evidence, not continue a fragment.
old_repair = "'REPAIR TASK: Rewrite the draft into a clean final recruiter-facing answer.'"
new_repair = "'REPAIR TASK: Reconstruct a complete recruiter-facing answer from the evidence already supplied. The draft may be truncated or malformed; do not merely continue it.'"
replace_once(old_repair, new_repair, 'repair reconstruction instruction')

# 5) One extra OpenRouter free-router attempt gives a different free route without canned fallback.
old_order = """  const first = requested && allowed.has(requested) ? requested : (configured || PRIMARY_MODELS[0]);\n  return [first, ...PRIMARY_MODELS.filter(m => m !== first)].filter((v, i, a) => a.indexOf(v) === i).slice(0, 3);"""
new_order = """  const first = requested && allowed.has(requested) ? requested : (configured || PRIMARY_MODELS[0]);\n  const order = [first, ...PRIMARY_MODELS.filter(m => m !== first)].filter((v, i, a) => a.indexOf(v) === i);\n  if (order.includes('openrouter/free')) order.push('openrouter/free');\n  return order.slice(0, 4);"""
replace_once(old_order, new_order, 'free-router retry')

# 6) A provider response cut by token length must be repaired/retried.
old_normal = """        let reply = stripModelArtifacts(modelMessage.content);\n        if (needsRepair(reply, plan, question)) {"""
new_normal = """        let reply = stripModelArtifacts(modelMessage.content);\n        const finishReason = response.data?.choices?.[0]?.finish_reason;\n        if (finishReason === 'length' || needsRepair(reply, plan, question)) {"""
replace_once(old_normal, new_normal, 'finish_reason validation')

old_tool = """            let reply = stripModelArtifacts(follow.data?.choices?.[0]?.message?.content);\n            if (needsRepair(reply, plan, question)) {"""
new_tool = """            let reply = stripModelArtifacts(follow.data?.choices?.[0]?.message?.content);\n            const finishReason = follow.data?.choices?.[0]?.finish_reason;\n            if (finishReason === 'length' || needsRepair(reply, plan, question)) {"""
replace_once(old_tool, new_tool, 'tool finish_reason validation')

# Invariants.
required = [
    'function looksIncompleteAnswer(text, question, plan)',
    'function missesRequiredProfessionalLead(text, plan, question)',
    'const conversationalHistory = vagueFollowUp ? history : [];',
    "if (order.includes('openrouter/free')) order.push('openrouter/free');",
    "finishReason === 'length' || needsRepair(reply, plan, question)",
]
for marker in required:
    if marker not in text:
        raise SystemExit(f'PATCH_FAIL: missing invariant {marker}')

for forbidden in ['function localFallback(', 'grounded-local-fallback']:
    if forbidden in text:
        raise SystemExit(f'PATCH_FAIL: forbidden fallback {forbidden}')

worker.write_text(text, encoding='utf-8')
print('PATCH_OK: worker written')

# Add regression contract.
evals = Path('docs/RAG_EVAL_SUITE.md')
if evals.exists():
    e = evals.read_text(encoding='utf-8')
    note = '''\n## Response-completeness regressions\n\n- Recruiter-fit answers must never return a sentence fragment (for example, `Adilio ... brings 15+ years of`).\n- Explicit repeated questions are regenerated independently and do not receive previous answer text as generation context.\n- Successful fit/experience answers must contain substantive professional evidence and normally exceed the minimum completeness threshold.\n- If an answer is stripped at a model-generated Sources heading and becomes incomplete, it must be repaired or rejected.\n- Source fallback must never attach arbitrary portfolio repositories to an incomplete professional/combined response.\n'''
    if '## Response-completeness regressions' not in e:
        e += note
        evals.write_text(e, encoding='utf-8')
        print('PATCH_OK: eval suite')

print('RELIABILITY_PATCH_COMPLETE')

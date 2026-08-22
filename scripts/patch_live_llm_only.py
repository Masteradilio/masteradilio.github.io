from pathlib import Path
import re

worker = Path('cloudflare/adilio-career-assistant.js')
text = worker.read_text(encoding='utf-8')


def replace_span(source, start_marker, end_marker, replacement, label):
    start = source.find(start_marker)
    end = source.find(end_marker, start if start >= 0 else 0)
    if start < 0 or end < 0:
        raise SystemExit(f'{label}: markers not found')
    print(f'PATCH_OK: {label}')
    return source[:start] + replacement + source[end:]


print('PATCH_START')
print('worker_length_before=', len(text))

# Version / contract banner.
text = text.replace('v2026.10: recruiter-facing RAG hardening.', 'v2026.11: live-LLM recruiter RAG hardening.')
text = text.replace('- resilient grounded fallbacks for critical recruiter questions', '- no substantive prewritten fallbacks; content answers always come from live LLM + RAG')
text = text.replace("const SERVICE_VERSION = '2026.10';", "const SERVICE_VERSION = '2026.11';")

# The CURRENT question determines retrieval. History is only consulted for a genuinely vague follow-up.
new_select = r'''function selectRepos(question, history) {
  const explicitCurrent = [...new Set(directRepoMentions(question))];
  if (explicitCurrent.length) return explicitCurrent.slice(0, 3);

  const q = normalizeText(question);
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
}

'''
text = replace_span(
    text,
    'function selectRepos(question, history) {',
    'function sanitizeGithubPath(',
    new_select,
    'selectRepos'
)

# Remove all question-specific substantive deterministic answers.
unavailable = '''function unavailableReply(language) {
  return language === 'pt'
    ? 'O assistente de IA está temporariamente indisponível para gerar uma resposta confiável. Tente novamente em alguns instantes.'
    : 'The AI assistant is temporarily unable to generate a reliable answer. Please try again in a few moments.';
}

'''
text = replace_span(
    text,
    'function localFallback(',
    'async function repairAnswer(',
    unavailable,
    'remove localFallback'
)

# No API key => unavailable, never a substantive prewritten response.
api_pattern = re.compile(
    r"      if \(!apiKey\) \{\n"
    r"\s*const fallback = localFallback\(question, language, plan, repos\);\n"
    r"\s*return jsonResponse\(request, \{ reply: fallback, sources: filterSourcesForReply\(fallback, candidateSources, plan, language\), model_used: 'grounded-local-fallback', status: 'success', request_id: requestId \}\);\n"
    r"\s*\}",
    re.MULTILINE,
)
api_replacement = """      if (!apiKey) {
        const unavailable = unavailableReply(language);
        return jsonResponse(request, { reply: unavailable, sources: [], model_used: null, generation_mode: 'unavailable', status: 'unavailable', request_id: requestId });
      }"""
text, api_count = api_pattern.subn(api_replacement, text, count=1)
if api_count != 1:
    raise SystemExit(f'api-key fallback replacement count={api_count}')
print('PATCH_OK: api-key fallback')

# If repair fails, do not substitute a canned answer; try the next live model.
repair_ref = "reply = repaired?.reply || localFallback(question, language, plan, repos);"
repair_count = text.count(repair_ref)
if repair_count < 1:
    raise SystemExit(f'repair fallback references not found; count={repair_count}')
text = text.replace(repair_ref, "reply = repaired?.reply || '';")
print('PATCH_OK: repair fallback refs=', repair_count)

# Tool-call path must continue to the next model when repair also fails.
tool_anchor = """              reply = repaired?.reply || '';
            }
            const allSources = dedupeSources([...candidateSources, ...toolSources]);"""
if tool_anchor in text:
    text = text.replace(
        tool_anchor,
        """              reply = repaired?.reply || '';
            }
            if (!reply) continue;
            const allSources = dedupeSources([...candidateSources, ...toolSources]);""",
        1,
    )
    print('PATCH_OK: tool-call failed-repair continue')
else:
    print('PATCH_NOTE: tool-call continue anchor already changed or absent')

# Terminal provider failure => explicit unavailable state.
terminal_pattern = re.compile(
    r"      const fallback = localFallback\(question, language, plan, repos\);\n"
    r"\s*return jsonResponse\(request, \{ reply: fallback, sources: filterSourcesForReply\(fallback, candidateSources, plan, language\), model_used: 'grounded-local-fallback', status: 'success', request_id: requestId \}\);",
    re.MULTILINE,
)
terminal_replacement = """      const unavailable = unavailableReply(language);
      return jsonResponse(request, { reply: unavailable, sources: [], model_used: null, generation_mode: 'unavailable', status: 'unavailable', request_id: requestId });"""
text, terminal_count = terminal_pattern.subn(terminal_replacement, text, count=1)
if terminal_count != 1:
    raise SystemExit(f'terminal fallback replacement count={terminal_count}')
print('PATCH_OK: terminal fallback')

# Successful substantive content explicitly reports live LLM + RAG generation.
text = text.replace(
    "model_used: model, status: 'success', tool_executed: true",
    "model_used: model, generation_mode: 'llm-rag', status: 'success', tool_executed: true",
)
text = text.replace(
    "model_used: model, status: 'success', tool_executed: false",
    "model_used: model, generation_mode: 'llm-rag', status: 'success', tool_executed: false",
)

# Extend leak detection with phrases observed during live testing.
reasoning_tail = "'scratch work','chain of thought'];"
reasoning_new = "'scratch work','chain of thought','non-negotiable rule','non negotiable rule','rule states','final-answer contract','final answer contract','evidence rules','available evidence blocks'];"
if reasoning_tail in text:
    text = text.replace(reasoning_tail, reasoning_new, 1)
    print('PATCH_OK: reasoning leak markers')
else:
    print('PATCH_NOTE: reasoning marker tail already changed or absent')

# Add factual post-generation guards, then extend needsRepair.
new_repair = '''function containsProfessionalAttributionError(text) {
  const q = normalizeText(text);
  const pixAssignedToBancoDoBrasil = q.includes('banco do brasil') && (q.includes('pix') || q.includes('fraud-prevention model') || q.includes('fraud prevention model') || q.includes('97% recall'));
  return pixAssignedToBancoDoBrasil;
}

function containsDataScopeOverclaim(text) {
  const q = normalizeText(text);
  return q.includes('datasus') && (q.includes('synthetic simulation') || q.includes('synthetic project') || q.includes('synthetic data'));
}

function needsRepair(text, plan) {
  return !text || text.length < 20 || containsReasoningLeak(text) || containsPortfolioProfessionalMix(text, plan) || containsKnownPortfolioOverclaim(text) || containsProfessionalAttributionError(text) || containsDataScopeOverclaim(text);
}

'''
text = replace_span(
    text,
    'function needsRepair(text, plan) {',
    'async function callOpenRouter(',
    new_repair,
    'needsRepair hardening'
)

# Final invariants before writing anything.
required = [
    "const SERVICE_VERSION = '2026.11';",
    'function unavailableReply(language)',
    "generation_mode: 'llm-rag'",
    'containsProfessionalAttributionError',
    'containsDataScopeOverclaim',
]
for marker in required:
    if marker not in text:
        raise SystemExit(f'missing required marker: {marker}')

for forbidden in ['function localFallback(', 'grounded-local-fallback', 'localFallback(question, language, plan, repos)']:
    if forbidden in text:
        raise SystemExit(f'forbidden fallback remnant: {forbidden}')

worker.write_text(text, encoding='utf-8')
print('PATCH_OK: worker written')
print('worker_length_after=', len(text))

# Update evaluation contract if present. This is intentionally non-fatal/idempotent.
evals = Path('docs/RAG_EVAL_SUITE.md')
if evals.exists():
    e = evals.read_text(encoding='utf-8')
    e = e.replace('- free-tier model failure falls back to a grounded deterministic answer for critical recruiter questions.', '- substantive content answers are always generated by a live LLM with RAG context; model/provider failure returns an explicit unavailable state rather than a prewritten substantive answer.')
    e = e.replace('- Do not fail if the first free model is unavailable.', '- Retry other configured live models if the first model is unavailable; never substitute a prewritten substantive answer.')
    e = e.replace('- Free-tier degradation: critical recruiter questions should still return a grounded fallback within the frontend timeout.', '- Free-tier degradation: retry alternate live models; if none can produce a validated answer, return an explicit temporary-unavailable message within the frontend timeout.')
    if '## Live-generation regressions' not in e:
        e += '''\n\n## Live-generation regressions\n\n- Successful recruiter content answers must come from live LLM generation (`generation_mode: llm-rag`), never question-specific hard-coded templates.\n- The BRB PIX fraud model must never be attributed to Banco do Brasil.\n- A current MLOps question must not inherit repository selection from unrelated earlier turns.\n- DataSUS RAG Agent must not be called synthetic unless its canonical repository evidence explicitly changes.\n- Internal phrases such as `non-negotiable rule`, `rule states`, or evidence-selection mechanics must never reach the user.\n'''
    evals.write_text(e, encoding='utf-8')
    print('PATCH_OK: eval contract')

# Update permanent CI expectations if the workflow exists. Non-fatal/idempotent.
ci = Path('.github/workflows/portfolio-professionalization.yml')
if ci.exists():
    c = ci.read_text(encoding='utf-8')
    c = c.replace("grep -q \"SERVICE_VERSION = '2026.10'\" cloudflare/adilio-career-assistant.js", "grep -q \"SERVICE_VERSION = '2026.11'\" cloudflare/adilio-career-assistant.js")
    c = c.replace("          grep -q 'grounded-local-fallback' cloudflare/adilio-career-assistant.js\n", "          ! grep -q 'grounded-local-fallback' cloudflare/adilio-career-assistant.js\n          ! grep -q 'function localFallback' cloudflare/adilio-career-assistant.js\n          grep -q \"generation_mode: 'llm-rag'\" cloudflare/adilio-career-assistant.js\n          grep -q 'containsProfessionalAttributionError' cloudflare/adilio-career-assistant.js\n          grep -q 'containsDataScopeOverclaim' cloudflare/adilio-career-assistant.js\n          grep -q 'function unavailableReply' cloudflare/adilio-career-assistant.js\n")
    ci.write_text(c, encoding='utf-8')
    print('PATCH_OK: permanent CI expectations')

print('PATCH_COMPLETE')

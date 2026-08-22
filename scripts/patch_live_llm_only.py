from pathlib import Path

worker = Path('cloudflare/adilio-career-assistant.js')
text = worker.read_text(encoding='utf-8')

print('FINAL_PATCH_START')

if "const SERVICE_VERSION = '2026.11';" not in text:
    raise SystemExit('expected v2026.11 worker not found')

# Current question alone controls evidence excerpts. Conversation history remains
# available to the LLM for conversational continuity, but it cannot bias retrieval
# for a new explicit question.
old_keywords = "const keywords = questionKeywords([question, ...history.filter(h => h.role === 'user').slice(-2).map(h => h.content)].join(' '));"
new_keywords = "const keywords = questionKeywords(question);"
if old_keywords in text:
    text = text.replace(old_keywords, new_keywords, 1)
    print('PATCH_OK: current-question-only evidence keywords')
elif new_keywords in text:
    print('PATCH_NOTE: evidence keywords already hardened')
else:
    raise SystemExit('retrievePortfolioEvidence keyword anchor not found')

# Detect a real misattribution to Banco do Brasil without rejecting a valid answer
# that separately discusses BRB PIX work and Banco do Brasil corporate-banking work.
start = text.find('function containsProfessionalAttributionError(text) {')
end = text.find('function containsDataScopeOverclaim(text) {', start)
if start < 0 or end < 0:
    raise SystemExit('professional attribution guard block not found')

new_guard = r'''function containsProfessionalAttributionError(text) {
  const q = normalizeText(text);
  const metric = '(pix|fraud-prevention model|fraud prevention model|97% recall)';
  const bancoAsSubject = new RegExp(`(?:at|no|na)\\s+banco do brasil.{0,90}${metric}`, 'i');
  const bancoPossessive = new RegExp(`banco do brasil(?:\\'s|’s)?.{0,90}${metric}`, 'i');
  const metricAssignedToBanco = new RegExp(`${metric}.{0,90}(?:at|no|na)\\s+banco do brasil`, 'i');
  return bancoAsSubject.test(q) || bancoPossessive.test(q) || metricAssignedToBanco.test(q);
}

'''
text = text[:start] + new_guard + text[end:]
print('PATCH_OK: localized BRB/Banco do Brasil attribution guard')

# Final invariants.
for forbidden in ['function localFallback(', 'grounded-local-fallback', 'localFallback(question, language, plan, repos)']:
    if forbidden in text:
        raise SystemExit(f'forbidden fallback remnant: {forbidden}')

required = [
    "generation_mode: 'llm-rag'",
    'function unavailableReply(language)',
    'const keywords = questionKeywords(question);',
    'bancoAsSubject',
]
for marker in required:
    if marker not in text:
        raise SystemExit(f'missing required marker: {marker}')

worker.write_text(text, encoding='utf-8')
print('PATCH_OK: worker written')

# Keep the evaluation contract aligned with the final retrieval behavior.
evals = Path('docs/RAG_EVAL_SUITE.md')
if evals.exists():
    e = evals.read_text(encoding='utf-8')
    note = '- A new explicit question must select repository evidence from the current question only; prior turns may support conversational continuity but must not contaminate retrieval for a different topic.'
    if note not in e:
        e += '\n' + note + '\n'
    evals.write_text(e, encoding='utf-8')
    print('PATCH_OK: eval contract')

print('FINAL_PATCH_COMPLETE')

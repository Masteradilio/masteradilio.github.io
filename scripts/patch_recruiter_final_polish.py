from pathlib import Path

worker = Path('cloudflare/adilio-career-assistant.js')
text = worker.read_text(encoding='utf-8')

rule = "11. For BRB LLM/RAG/AI-agent work, preserve the supported verb 'implemented'; do not upgrade it to 'deployed' unless the professional evidence explicitly changes."
extra = rule + "\n12. For BANPARÁ RAG work, preserve the supported verb 'developed'; do not upgrade it to 'deployed' unless the professional evidence explicitly changes."
if rule not in text:
    raise SystemExit('rule anchor not found')
text = text.replace(rule, extra, 1)

old = """  const brbLlmDeploymentUpgrade = /(?:brb|banco de brasilia).{0,180}\\bdeploy(?:ed|ment)?\\b.{0,80}\\b(?:llm|rag|ai-agent|ai agent)\\b|\\bdeploy(?:ed|ment)?\\b.{0,80}\\b(?:llm|rag|ai-agent|ai agent)\\b.{0,180}(?:brb|banco de brasilia)/i;\n  return bancoAsSubject.test(q) || bancoPossessive.test(q) || metricAssignedToBanco.test(q) || brbLlmDeploymentUpgrade.test(q);"""
new = """  const brbLlmDeploymentUpgrade = /(?:brb|banco de brasilia).{0,180}\\bdeploy(?:ed|ment)?\\b.{0,80}\\b(?:llm|rag|ai-agent|ai agent)\\b|\\bdeploy(?:ed|ment)?\\b.{0,80}\\b(?:llm|rag|ai-agent|ai agent)\\b.{0,180}(?:brb|banco de brasilia)/i;\n  const banparaRagDeploymentUpgrade = /banpara.{0,180}\\bdeploy(?:ed|ment)?\\b.{0,80}\\brag\\b|\\bdeploy(?:ed|ment)?\\b.{0,80}\\brag\\b.{0,180}banpara/i;\n  return bancoAsSubject.test(q) || bancoPossessive.test(q) || metricAssignedToBanco.test(q) || brbLlmDeploymentUpgrade.test(q) || banparaRagDeploymentUpgrade.test(q);"""
if old not in text:
    raise SystemExit('attribution guard anchor not found')
text = text.replace(old, new, 1)

old_repair = "Keep wording factual. For BRB LLM/RAG/AI-agent work, use implemented rather than deployed."
new_repair = "Keep wording factual. For BRB LLM/RAG/AI-agent work, use implemented rather than deployed. For BANPARÁ RAG work, use developed rather than deployed."
if old_repair not in text:
    raise SystemExit('repair wording anchor not found')
text = text.replace(old_repair, new_repair, 1)

worker.write_text(text, encoding='utf-8')
print('FINAL_POLISH_COMPLETE')

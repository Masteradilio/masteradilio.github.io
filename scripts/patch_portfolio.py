from pathlib import Path
import re

INDEX = Path("index.html")
html = INDEX.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global html
    if new in html:
        return
    if old not in html:
        raise RuntimeError(f"Could not locate expected block: {label}")
    html = html.replace(old, new, 1)


def replace_all(old: str, new: str) -> None:
    global html
    html = html.replace(old, new)


# ---------------------------------------------------------------------------
# 1. Positioning, SEO and social sharing
# ---------------------------------------------------------------------------
replace_once(
    '<title>Adilio Farias | Senior Data Scientist & AI/ML Engineer</title>',
    '<title>Adilio Farias | AI Engineer & Senior Data Scientist</title>',
    'page title',
)
replace_once(
    '<meta name="description" content="Portfolio de Adilio Farias (@Masteradilio) - Senior Data Scientist, AI Engineer, Especialista em Generative AI, Enterprise RAG, MLOps, Time Series e Deteccao de Fraudes.">',
    '<meta name="description" content="Portfolio de Adilio Farias (@Masteradilio), AI Engineer e Senior Data Scientist. Projetos em Machine Learning, Generative AI, LLMs, RAG, MLOps, risco de credito e prevencao a fraudes.">',
    'meta description',
)

if 'property="og:title"' not in html:
    social_meta = '''\n  <link rel="canonical" href="https://masteradilio.github.io/">\n  <meta name="robots" content="index,follow">\n  <meta property="og:type" content="website">\n  <meta property="og:url" content="https://masteradilio.github.io/">\n  <meta property="og:title" content="Adilio Farias | AI Engineer & Senior Data Scientist">\n  <meta property="og:description" content="Machine Learning, Generative AI, LLMs, RAG, MLOps, financial risk and fraud prevention projects.">\n  <meta property="og:image" content="https://masteradilio.github.io/assets/portfolio-og.png">\n  <meta property="og:image:width" content="1200">\n  <meta property="og:image:height" content="630">\n  <meta property="og:locale" content="pt_BR">\n  <meta property="og:locale:alternate" content="en_US">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="Adilio Farias | AI Engineer & Senior Data Scientist">\n  <meta name="twitter:description" content="Machine Learning, Generative AI, LLMs, RAG, MLOps, financial risk and fraud prevention projects.">\n  <meta name="twitter:image" content="https://masteradilio.github.io/assets/portfolio-og.png">'''
    anchor = '<meta name="description" content="Portfolio de Adilio Farias (@Masteradilio), AI Engineer e Senior Data Scientist. Projetos em Machine Learning, Generative AI, LLMs, RAG, MLOps, risco de credito e prevencao a fraudes.">'
    html = html.replace(anchor, anchor + social_meta, 1)

# Replace Tailwind Play CDN/config with a compiled production stylesheet.
if 'https://cdn.tailwindcss.com' in html:
    pattern = re.compile(
        r'\s*<script src="https://cdn\.tailwindcss\.com"></script>\s*<script>\s*tailwind\.config\s*=\s*\{.*?\}\s*</script>',
        re.S,
    )
    html, count = pattern.subn('\n  <link rel="stylesheet" href="assets/tailwind.css">', html, count=1)
    if count != 1:
        raise RuntimeError('Could not replace Tailwind Play CDN block')

# Sanitize any HTML generated from LLM-provided Markdown before inserting it into the DOM.
if 'dompurify@3.4.13' not in html:
    anchor = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">'
    replacement = anchor + '\n  <script src="https://cdn.jsdelivr.net/npm/dompurify@3.4.13/dist/purify.min.js" integrity="sha256-PLACEHOLDER" crossorigin="anonymous"></script>'
    # SRI is intentionally removed below: the pinned package version is retained, while
    # a stale/incorrect hash would make the security dependency unavailable.
    replacement = replacement.replace(' integrity="sha256-PLACEHOLDER"', '')
    replace_once(anchor, replacement, 'DOMPurify dependency')

# Structured profile metadata for search engines.
if '"@type": "Person"' not in html:
    json_ld = '''\n  <script type="application/ld+json">\n  {\n    "@context": "https://schema.org",\n    "@type": "Person",\n    "name": "Adilio Farias",\n    "url": "https://masteradilio.github.io/",\n    "jobTitle": "AI Engineer and Senior Data Scientist",\n    "sameAs": [\n      "https://github.com/Masteradilio",\n      "https://www.linkedin.com/in/adiliofarias"\n    ],\n    "knowsAbout": [\n      "Machine Learning", "Generative AI", "Large Language Models", "RAG",\n      "AI Agents", "MLOps", "Credit Risk", "Fraud Prevention", "Python", "SQL"\n    ]\n  }\n  </script>'''
    html = html.replace('</head>', json_ld + '\n</head>', 1)

# ---------------------------------------------------------------------------
# 2. Recruiter-facing positioning and accumulated experience
# ---------------------------------------------------------------------------
replace_all(
    '⚡ 100% Gerado de Forma Autônoma pelo Squad Forge SE via Modelo Local',
    '⚡ Construído com o Squad Forge SE — minha plataforma de engenharia autônoma com modelo local',
)
replace_all(
    '⚡ 100% Autonomously Generated by Squad Forge SE via Local Model',
    '⚡ Built with Squad Forge SE — my autonomous software engineering platform using a local model',
)

replace_all('Quadro de Senioridade', 'Experiência Profissional Acumulada')
replace_all('Seniority Breakdown', 'Accumulated Professional Experience')
replace_all('Tempo de Atuação Profissional', 'Carreira multidisciplinar com períodos sobrepostos')
replace_all('Professional Experience Duration', 'Multidisciplinary career with overlapping roles')
replace_all('Setor Financeiro</span>', '16+ anos no setor financeiro</span>')

replace_all(
    '* Nota: Atuação desenvolvida por vezes de forma sobreposta entre funções (roles), e não de forma puramente seriada.',
    '* Os períodos acima representam experiência acumulada por domínio. Algumas funções foram exercidas simultaneamente e, por isso, não devem ser somadas como uma linha do tempo única.',
)
replace_all(
    '* Note: Experience developed with concurrent overlapping roles rather than purely sequentially.',
    '* The figures above represent accumulated experience by domain. Some roles overlapped and therefore should not be added as a single sequential timeline.',
)

# Align the contact CTA with the roles actively targeted.
replace_all(
    'Disponível para posições de liderança técnica, contratação direta ou consultoria em sistemas de IA e ciência de dados.',
    'Aberto a oportunidades como AI Engineer ou Senior Data Scientist, além de colaboração em projetos de IA e Ciência de Dados.',
)
replace_all(
    'Available for technical leadership roles, direct hiring, or consulting in AI systems and data science.',
    'Open to AI Engineer and Senior Data Scientist opportunities, as well as collaboration on AI and Data Science projects.',
)

# ---------------------------------------------------------------------------
# 3. Make portfolio claims more evidence-oriented and current
# ---------------------------------------------------------------------------
# Correct model naming: Qwen3.8 27B is not Qwen 2.5 Coder 27B.
replace_all('qwen3.8-27b (Qwen 2.5 Coder 27B)', 'qwen3.8-27b (Qwen3.8 27B)')
replace_all('qwen3.8-27b (Qwen 2.5 Coder 27B)', 'qwen3.8-27b (Qwen3.8 27B)')

# Reframe authorship so autonomous generation demonstrates the user's engineering work.
replace_all(
    'Este portfólio não foi codificado manualmente: foi inteiramente especificado via <strong>PRD (Product Requirements Document)</strong> e construído pelo <strong>Squad Forge SE</strong> — o Control Plane Open-Source de Engenharia de Software desenvolvido por Adilio Farias.',
    'Este portfólio foi especificado por Adilio Farias por meio de um <strong>PRD (Product Requirements Document)</strong>, critérios de aceite e contratos de engenharia, e então implementado pelo <strong>Squad Forge SE</strong> — seu Control Plane Open-Source de Engenharia de Software autônoma.',
)
replace_all(
    'This portfolio was not manually coded: it was specified entirely via a <strong>PRD (Product Requirements Document)</strong> and engineered by <strong>Squad Forge SE</strong> — the Open-Source Autonomous Software Engineering Control Plane created by Adilio Farias.',
    'This portfolio was specified by Adilio Farias through a <strong>PRD (Product Requirements Document)</strong>, acceptance criteria, and engineering contracts, then implemented by <strong>Squad Forge SE</strong> — his open-source autonomous software engineering control plane.',
)

# Credit-risk project description was stale; align it with the current repository scope.
replace_all(
    'Pipeline end-to-end de classificação de risco de crédito bancário com LightGBM e XGBoost, otimização Bayesiana de hiperparâmetros com Optuna e explicabilidade de decisões financeiras via SHAP.',
    'Plataforma de engenharia de risco de crédito com dados sintéticos, componentes PD/LGD/EAD, cálculo de EL/ECL, staging IFRS 9/CMN 4.966, API FastAPI e pacote versionado de evidências regulatórias.',
)
replace_all(
    'End-to-end banking credit risk classification pipeline with LightGBM/XGBoost, Optuna Bayesian hyperparameter tuning, and decision explainability via SHAP values.',
    'Credit-risk engineering platform using synthetic data, with PD/LGD/EAD components, EL/ECL calculation, IFRS 9/CMN 4.966 staging, FastAPI, and versioned regulatory evidence.',
)
replace_all('SHAP Explainability & Optuna Tuning', 'PD/LGD/EAD • ECL • Regulatory Evidence')

# Surface verified Sentinel PIX benchmark evidence directly on the card.
replace_all('Streaming Kafka & Latência Sub-50ms', 'Recall 99,86% • FPR 0,957% • p95 < 15 ms')
replace_all('Streaming Kafka & Sub-50ms Latency', 'Recall 99.86% • FPR 0.957% • p95 < 15 ms')

# ---------------------------------------------------------------------------
# 4. Career assistant: preserve free-form questions, make LLM behavior explicit,
#    improve conversation history and sanitize model output.
# ---------------------------------------------------------------------------
replace_all(
    'Pergunte o que quiser sobre minhas experiências profissionais, educação e meus projetos de portfólio.',
    'Faça sua própria pergunta sobre minhas experiências, formação ou projetos. Perguntas de conteúdo são respondidas pelo LLM com contexto RAG.',
)
replace_all(
    'Ask anything about my professional experience, education, and portfolio projects.',
    'Ask your own question about my experience, education, or projects. Content questions are answered by the LLM using RAG context.',
)
replace_all(
    'Observação: é normal haver uma latência de até 60 segundos para receber a resposta do Agente.',
    'Observação: as respostas de conteúdo são geradas pelo LLM com RAG e podem levar até 60 segundos no tier gratuito. Contato e acesso ao currículo usam apenas respostas utilitárias determinísticas.',
)
replace_all(
    'Note: it is normal to experience a latency of up to 60 seconds to receive the Agent\'s response.',
    'Note: content answers are generated by the LLM with RAG and may take up to 60 seconds on the free tier. Contact and resume access use deterministic utility responses only.',
)
replace_all('Baixe meu currículo', 'Currículo completo (HTML)')
replace_all('Download Resume', 'Full Resume (HTML)')

# Only deterministic utility questions should bypass the LLM. The profile-summary FAQ
# remains in source for backward compatibility, but is deliberately not marked utility.
for trigger in [
    '"como baixar o curriculo",',
    '"quais os contatos do adilio",',
]:
    marker = '      {\n        triggers: [\n          ' + trigger
    if marker in html and ('      {\n        utility: true,\n        triggers: [\n          ' + trigger) not in html:
        html = html.replace(marker, '      {\n        utility: true,\n        triggers: [\n          ' + trigger, 1)

loop_anchor = '      for (const faq of DETERMINISTIC_FAQ) {\n        for (const trigger of faq.triggers) {'
loop_replacement = '      for (const faq of DETERMINISTIC_FAQ) {\n        if (!faq.utility) continue;\n        for (const trigger of faq.triggers) {'
replace_once(loop_anchor, loop_replacement, 'deterministic utility gate')

# Avoid duplicating the current question in both `message` and `history`.
replace_all('history: conversationHistory.slice(-4),', 'history: conversationHistory.slice(0, -1).slice(-4),')

# Keep raw model text in conversation memory; render HTML only for display.
replace_once(
    '      let answer = null;\n\n      // 1. Check if question matches predefined deterministic FAQ with >= 80% (0.80) similarity',
    '      let answer = null;\n      let rawAssistantReply = null;\n\n      // 1. Deterministic fast-path is restricted to utility actions; substantive profile/project questions go to the LLM.',
    'raw assistant reply variable',
)
replace_all(
    '            answer = formatMarkdown(raw);',
    '            rawAssistantReply = raw;\n            answer = formatMarkdown(rawAssistantReply);',
)
replace_all(
    '              answer = formatMarkdown(data.reply);',
    '              rawAssistantReply = String(data.reply);\n              if (Array.isArray(data.sources) && data.sources.length) {\n                const sourceLines = data.sources.map((source) => {\n                  if (typeof source === \'string\') return `- ${source}`;\n                  const label = source.label || source.title || source.name || \'Source\';\n                  const url = source.url ? ` (${source.url})` : \'\';\n                  return `- ${label}${url}`;\n                }).join(\'\\n\');\n                rawAssistantReply += `\\n\\n### Sources\\n${sourceLines}`;\n              }\n              answer = formatMarkdown(rawAssistantReply);',
)
replace_all(
    '        answer = formatMarkdown(errorMsg);',
    '        rawAssistantReply = errorMsg;\n        answer = formatMarkdown(rawAssistantReply);',
)
replace_all(
    "      conversationHistory.push({ role: 'assistant', content: answer });",
    "      conversationHistory.push({ role: 'assistant', content: rawAssistantReply || '' });",
)

# Sanitize final model-derived HTML. If the dependency fails to load, safely fall back
# to escaped plain text instead of inserting unsanitized markup.
format_anchor = "      return html;\n    }\n\n    async function processQuestion(question) {"
format_replacement = """      if (window.DOMPurify) {
        return window.DOMPurify.sanitize(html, {
          USE_PROFILES: { html: true },
          ADD_ATTR: ['target', 'rel']
        });
      }
      return escapeHtml(md).replace(/\\n/g, '<br>');
    }

    async function processQuestion(question) {"""
replace_once(format_anchor, format_replacement, 'sanitized markdown return')

# Accessibility and reasonable request boundary.
replace_all(
    'id="chat-box">',
    'id="chat-box" aria-live="polite" aria-label="AI career assistant conversation">',
)
replace_all(
    'id="chat-input" placeholder=',
    'id="chat-input" maxlength="1200" autocomplete="off" placeholder=',
)

# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
checks = {
    'production Tailwind CSS': 'https://cdn.tailwindcss.com' not in html and 'assets/tailwind.css' in html,
    'Open Graph metadata': 'property="og:title"' in html and 'portfolio-og.png' in html,
    'DOMPurify': 'dompurify@3.4.13' in html and 'DOMPurify.sanitize' in html,
    'history excludes current turn': 'conversationHistory.slice(0, -1).slice(-4)' in html,
    'utility-only deterministic gate': 'if (!faq.utility) continue;' in html,
    'raw conversation history': "content: rawAssistantReply || ''" in html,
    'correct Qwen naming': 'qwen3.8-27b (Qwen 2.5 Coder 27B)' not in html,
    'role positioning': 'AI Engineer & Senior Data Scientist' in html,
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise RuntimeError('Portfolio migration validation failed: ' + ', '.join(failed))

INDEX.write_text(html, encoding="utf-8")
print('Portfolio professionalization patch applied successfully.')
for name in checks:
    print(f'  PASS: {name}')

from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old_css = '''    .assistant-architecture-card {\n      min-width: 0;\n      height: 100%;\n      overflow: visible;\n    }\n'''
new_css = '''    .assistant-architecture-card {\n      min-width: 0;\n      overflow: hidden;\n    }\n    .architecture-capabilities {\n      display: grid;\n      grid-template-rows: repeat(6, minmax(0, 1fr));\n      gap: 0.65rem;\n    }\n    .architecture-capability {\n      min-height: 0;\n      padding: 0.7rem 0.75rem;\n      border: 1px solid rgba(51, 65, 85, 0.72);\n      border-radius: 0.75rem;\n      background: rgba(15, 23, 42, 0.50);\n      align-items: flex-start;\n    }\n    .architecture-capability > div:last-child { min-width: 0; }\n    .architecture-closing {\n      margin-top: 0.9rem;\n      padding: 0.85rem 0.9rem;\n      border: 1px solid rgba(6, 182, 212, 0.18);\n      border-radius: 0.75rem;\n      background: rgba(6, 182, 212, 0.055);\n    }\n    @media (max-width: 1099px) {\n      .architecture-capabilities { grid-template-rows: none; }\n    }\n'''
if old_css not in text:
    raise SystemExit('assistant architecture CSS block not found')
text = text.replace(old_css, new_css, 1)

old_aside = '<aside id="rag-architecture-panel" class="assistant-architecture-card rounded-2xl bg-slate-950/70 border border-cyan-500/25 p-5 sm:p-6 flex flex-col shadow-lg shadow-cyan-950/20">'
new_aside = '<aside id="rag-architecture-panel" class="assistant-architecture-card glass-card rounded-2xl p-6 sm:p-8 border border-cyan-500/40 shadow-2xl glow-cyan flex flex-col">'
if old_aside not in text:
    raise SystemExit('architecture aside class not found')
text = text.replace(old_aside, new_aside, 1)

panel_start = text.index('<aside id="rag-architecture-panel"')
panel_end = text.index('</aside>', panel_start) + len('</aside>')
panel = text[panel_start:panel_end]

old_middle = '<div class="flex-1 py-4 space-y-3">'
new_middle = '<div class="architecture-capabilities flex-1 py-5">'
if old_middle not in panel:
    raise SystemExit('architecture capabilities container not found')
panel = panel.replace(old_middle, new_middle, 1)

count = panel.count('<div class="flex gap-3">')
if count != 6:
    raise SystemExit(f'expected 6 capability rows, found {count}')
panel = panel.replace('<div class="flex gap-3">', '<div class="architecture-capability flex gap-3">')

old_closing = '<div class="pt-4 border-t border-slate-800">'
new_closing = '<div class="architecture-closing">'
if old_closing not in panel:
    raise SystemExit('architecture closing block not found')
panel = panel.replace(old_closing, new_closing, 1)

text = text[:panel_start] + panel + text[panel_end:]

replacements = {
    'Respostas fundamentadas no meu currículo e nos meus Github Projects públicos.': 'Recupera contexto relevante do meu currículo e dos meus Github Projects públicos antes de cada resposta gerada pelo LLM.',
    'As respostas referenciam as fontes de portfólio usadas como evidência de suporte.': 'Cada resposta pode apresentar as fontes utilizadas como evidência, permitindo verificar as afirmações diretamente nos materiais de origem.',
    'Vercel AI Gateway, OpenRouter e Hugging Face fornecem roteamento resiliente de LLMs e failover.': 'Vercel AI Gateway atua como rota principal, com OpenRouter e Hugging Face fornecendo failover entre provedores para maior disponibilidade.',
    'A validação separa experiência profissional de evidências de portfólio e bloqueia afirmações sem suporte.': 'A validação pós-geração separa experiência profissional de evidências de portfólio e rejeita afirmações sem suporte ou exageradas.',
    'Suporte a PT-BR e inglês em toda a experiência.': 'A interface e as respostas suportam PT-BR e inglês, mantendo a interação consistente nos dois idiomas.',
    'Construído com grounding de fontes, validação de saída, resiliência e experiência do usuário em mente.': 'Combina RAG, retries, failover entre provedores, validação de saída, grounding de fontes e abstention segura para operação resiliente.',
    'Answers are grounded in my resume and public Github Projects.': 'Retrieves relevant context from my resume and public Github Projects before the LLM generates each answer.',
    'Responses reference the portfolio sources used as supporting evidence.': 'Each answer can surface the sources used as evidence, making claims directly inspectable against the underlying materials.',
    'Vercel AI Gateway, OpenRouter, and Hugging Face provide resilient LLM routing and failover.': 'Vercel AI Gateway is the primary route, with OpenRouter and Hugging Face providing cross-provider failover for higher availability.',
    'Validation separates professional experience from portfolio evidence and blocks unsupported claims.': 'Post-generation validation separates professional experience from portfolio evidence and rejects unsupported or overstated claims.',
    'Supports PT-BR and English across the experience.': 'The interface and generated answers support both PT-BR and English with a consistent bilingual experience.',
    'Built with source grounding, output validation, resilience, and user experience in mind.': 'Combines RAG, retries, provider failover, output validation, source grounding, and safe abstention for resilient operation.'
}

for old, new in replacements.items():
    occurrences = text.count(old)
    if occurrences < 1:
        raise SystemExit(f'text not found: {old}')
    text = text.replace(old, new)

path.write_text(text, encoding='utf-8')
print('ASSISTANT_ARCHITECTURE_PANEL_REFINED')

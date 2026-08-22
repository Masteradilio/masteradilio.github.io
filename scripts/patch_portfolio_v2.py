from pathlib import Path
import re

INDEX = Path('index.html')
html = INDEX.read_text(encoding='utf-8')


def replace_all(old: str, new: str) -> None:
    global html
    html = html.replace(old, new)


def replace_project_tags(project: str, tags: list[str]) -> None:
    global html
    project_pos = html.find(f'>{project}</h3>')
    if project_pos < 0:
        raise RuntimeError(f'Project card not found: {project}')
    tags_start = html.find('<div class="flex flex-wrap gap-1.5 pt-1">', project_pos)
    tags_end = html.find('</div>', tags_start)
    if tags_start < 0 or tags_end < 0:
        raise RuntimeError(f'Tag block not found: {project}')
    open_tag_end = html.find('>', tags_start) + 1
    indent = '              '
    rendered = ''.join(
        f'\n{indent}<span class="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300">{tag}</span>'
        for tag in tags
    ) + '\n            '
    html = html[:open_tag_end] + rendered + html[tags_end:]


# Correct the model name in text where the model identifier is wrapped in <code>.
replace_all(
    '<code>qwen3.8-27b</code> (Qwen 2.5 Coder 27B)',
    '<code>qwen3.8-27b</code> (Qwen3.8 27B)',
)

# Make the Squad Forge narrative emphasize Adilio's specification/engineering ownership.
replace_all(
    'Como o Squad Forge SE Criou Este Site de Forma 100% Autônoma',
    'Como o Squad Forge SE Implementou Este Portfólio',
)
replace_all(
    'How Squad Forge SE Autonomously Built This Website',
    'How Squad Forge SE Implemented This Portfolio',
)
replace_all(
    '⚡ Este site foi 100% concebido, implementado, testado e compilado de forma autônoma pelo <strong>Squad Forge SE</strong> utilizando modelo local (llama.cpp / qwen3.8-27b a $0.00 de custo).',
    '⚡ Este portfólio foi especificado por Adilio Farias e implementado, testado e empacotado pelo <strong>Squad Forge SE</strong> utilizando modelo local (llama.cpp / qwen3.8-27b a $0.00 de custo de API em nuvem).',
)
replace_all(
    '⚡ This website was 100% autonomously designed, implemented, tested, and compiled by <strong>Squad Forge SE</strong> using a local LLM (llama.cpp / qwen3.8-27b at $0.00 cost).',
    '⚡ This portfolio was specified by Adilio Farias and implemented, tested, and packaged by <strong>Squad Forge SE</strong> using a local LLM (llama.cpp / qwen3.8-27b at $0.00 cloud API cost).',
)

# Make the accumulated-experience badge bilingual.
old_badge = '<span class="text-[10px] px-2.5 py-1 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 font-mono font-semibold">16+ anos no setor financeiro</span>'
new_badge = '<span class="text-[10px] px-2.5 py-1 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 font-mono font-semibold" data-i18n="seniority_badge">16+ anos no setor financeiro</span>'
replace_all(old_badge, new_badge)
replace_all(
    'seniority_card_subtitle: "Carreira multidisciplinar com períodos sobrepostos",\n        role_ds:',
    'seniority_card_subtitle: "Carreira multidisciplinar com períodos sobrepostos",\n        seniority_badge: "16+ anos no setor financeiro",\n        role_ds:',
)
replace_all(
    'seniority_card_subtitle: "Multidisciplinary career with overlapping roles",\n        role_ds:',
    'seniority_card_subtitle: "Multidisciplinary career with overlapping roles",\n        seniority_badge: "16+ years in financial services",\n        role_ds:',
)

# Current canonical credit-risk repository is an IFRS 9 / CMN 4.966 engineering
# platform with synthetic data and explicit model-approval blockers, not the older
# LightGBM/Optuna/SHAP classification card that was previously displayed.
replace_project_tags(
    'credit_risk_model',
    ['Python', 'FastAPI', 'IFRS 9', 'PD/LGD/EAD', 'EL/ECL'],
)

# Align Sentinel PIX with its current public README: LightGBM + Isolation Forest,
# dual feature stores, MLflow and measured benchmark latency.
replace_all(
    'Sistema de detecção de fraudes e anomalias em transações PIX em tempo real com processamento de streams (Kafka), inferência assíncrona com XGBoost e latência rigorosa sub-50ms para autorização de pagamentos.',
    'Motor antifraude PIX em tempo real com FastAPI, feature stores Redis/PostgreSQL, LightGBM + Isolation Forest, explicabilidade SHAP, MLflow e monitoramento contínuo de drift, com p95 inferior a 15 ms no benchmark do projeto.',
)
replace_all(
    'Real-time stream processing anomaly and fraud detection system for instant PIX payments with Apache Kafka, XGBoost, and sub-50ms latency SLAs for payment authorization.',
    'Real-time PIX anti-fraud engine with FastAPI, Redis/PostgreSQL feature stores, LightGBM + Isolation Forest, SHAP explainability, MLflow, and continuous drift monitoring, with p95 below 15 ms in the project benchmark.',
)
replace_project_tags(
    'sentinel_pix',
    ['Python', 'LightGBM', 'Redis', 'FastAPI', 'MLflow'],
)

# Verification against known stale claims.
stale = [
    '<code>qwen3.8-27b</code> (Qwen 2.5 Coder 27B)',
    'Como o Squad Forge SE Criou Este Site de Forma 100% Autônoma',
    'How Squad Forge SE Autonomously Built This Website',
    'processamento de streams (Kafka), inferência assíncrona com XGBoost',
    'Apache Kafka, XGBoost, and sub-50ms latency SLAs',
]
remaining = [value for value in stale if value in html]
if remaining:
    raise RuntimeError('Stale portfolio claims remain: ' + repr(remaining))

# Keep these checks semantic enough to survive safe HTML escaping/i18n wrappers.
required = [
    'Qwen3.8 27B',
    'data-i18n="seniority_badge"',
    'PD/LGD/EAD',
    'LightGBM + Isolation Forest',
    'Recall 99,86%',
]
missing = [value for value in required if value not in html]
if missing:
    raise RuntimeError('Expected updated claims missing: ' + repr(missing))

INDEX.write_text(html, encoding='utf-8')
print('Portfolio evidence-alignment patch applied successfully.')

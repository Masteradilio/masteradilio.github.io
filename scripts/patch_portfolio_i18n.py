from pathlib import Path

INDEX = Path("index.html")
html = INDEX.read_text(encoding="utf-8")


def replace_once(old: str, new: str) -> None:
    global html
    if new in html:
        return
    if old not in html:
        raise RuntimeError(f"Expected block not found: {old[:80]}")
    html = html.replace(old, new, 1)


def replace_all(old: str, new: str) -> None:
    global html
    html = html.replace(old, new)


# ---------------------------------------------------------------------------
# Recruiter-facing project highlights: make the evidence bilingual and scope
# experimental/synthetic/backtest metrics explicitly.
# ---------------------------------------------------------------------------
highlights = {
    '<div><strong class="text-purple-300">Destaque:</strong> Suporte Local LLM ($0.00) & ActionGateway</div>':
        '<div data-i18n="proj1_highlight"><strong class="text-purple-300">Destaque:</strong> LLM local ($0.00) • ActionGateway • Multi-Agent</div>',
    '<div><strong class="text-amber-300">Destaque:</strong> Sharpe 1,42 • Hit Rate 56,8% • Purged CV</div>':
        '<div data-i18n="proj2_highlight"><strong class="text-amber-300">Destaque:</strong> Sharpe 1,42 (backtest) • Hit Rate 56,8% • Purged CV</div>',
    '<div><strong class="text-cyan-300">Destaque:</strong> 96-case EVAL benchmark • TRUE/FALSE/UNDECIDABLE</div>':
        '<div data-i18n="proj3_highlight"><strong class="text-cyan-300">Destaque:</strong> EVAL semissintético (96 casos) • TRUE/FALSE/UNDECIDABLE</div>',
    '<div><strong class="text-indigo-300">Destaque:</strong> 473.791 registros • Faithfulness 98% • MRR 0,88</div>':
        '<div data-i18n="proj4_highlight"><strong class="text-indigo-300">Destaque:</strong> 473.791 registros • Faithfulness 98% • MRR 0,88</div>',
    '<div><strong class="text-emerald-300">Destaque:</strong> PD/LGD/EAD • ECL • Regulatory Evidence</div>':
        '<div data-i18n="proj5_highlight"><strong class="text-emerald-300">Destaque:</strong> Dados sintéticos • PD/LGD/EAD • ECL • Rastreabilidade</div>',
    '<div><strong class="text-emerald-300">Destaque:</strong> ROC-AUC 0,9818 • Gini 0,9637 • KS 0,8627</div>':
        '<div data-i18n="proj6_highlight"><strong class="text-emerald-300">Destaque:</strong> Benchmark sintético • ROC-AUC 0,9818 • Gini 0,9637 • KS 0,8627</div>',
    '<div><strong class="text-emerald-300">Destaque:</strong> Recall 99,86% • FPR 0,957% • p95 < 15 ms</div>':
        '<div data-i18n="proj7_highlight"><strong class="text-emerald-300">Destaque:</strong> Benchmark do projeto • Recall 99,86% • FPR 0,957% • p95 &lt; 15 ms</div>',
}
for old, new in highlights.items():
    replace_once(old, new)

# ---------------------------------------------------------------------------
# Skills that still contained Portuguese in English mode.
# ---------------------------------------------------------------------------
skill_items = {
    '<li>• Séries Temporais (LSTM / SARIMAX)</li>': '<li data-i18n="skill_ds_1">• Séries Temporais (LSTM / SARIMAX)</li>',
    '<li>• Detecção de Anomalias & Fraudes</li>': '<li data-i18n="skill_ds_2">• Detecção de Anomalias & Fraudes</li>',
    '<li>• Credit Scoring & Modelos de Risco</li>': '<li data-i18n="skill_ds_3">• Credit Scoring & Modelos de Risco</li>',
    '<li>• FastAPI, Python & Microsserviços</li>': '<li data-i18n="skill_eng_1">• FastAPI, Python & Microsserviços</li>',
    '<li>• Metodologias Ágeis & Scrum</li>': '<li data-i18n="skill_gov_1">• Metodologias Ágeis & Scrum</li>',
}
for old, new in skill_items.items():
    replace_once(old, new)

# ---------------------------------------------------------------------------
# Chat language consistency without adding suggested questions.
# ---------------------------------------------------------------------------
replace_once(
    '<input type="text" id="chat-input" maxlength="1200" autocomplete="off" placeholder="Pergunte sobre experiências, formação, projetos ou contratação..."',
    '<input type="text" id="chat-input" maxlength="1200" autocomplete="off" data-i18n-placeholder="chat_placeholder" placeholder="Pergunte sobre experiências, formação, projetos ou contratação..."',
)

placeholder_anchor = """      document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
          el.innerHTML = translations[lang][key];
        }
      });
"""
placeholder_replacement = placeholder_anchor + """
      document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (translations[lang] && translations[lang][key]) {
          el.setAttribute('placeholder', translations[lang][key]);
        }
      });
"""
replace_once(placeholder_anchor, placeholder_replacement)

replace_once(
    '<span class="text-xs text-slate-400 ml-1">Consultando RAG & Modelo...</span>',
    '<span class="text-xs text-slate-400 ml-1">${currentLang === \'en\' ? \'Querying RAG & model...\' : \'Consultando RAG & modelo...\'}</span>',
)

# Clarify that the assistant talks about Adilio rather than impersonating him.
replace_all(
    "Olá! Sou o assistente virtual de <strong>Adilio Farias</strong>. Estou conectado aos currículos completos e aos READMEs técnicos dos repositórios públicos. Pergunte o que quiser sobre minhas experiências, educação e projetos!",
    "Olá! Sou o assistente virtual de <strong>Adilio Farias</strong>. Estou conectado aos currículos e aos READMEs técnicos dos repositórios públicos. Pergunte sobre a experiência profissional, formação e projetos de Adilio.",
)
replace_all(
    "Hello! I am the virtual assistant for <strong>Adilio Farias</strong>. I have permanent access to Adilio's full resume and the technical READMEs of public repositories. Feel free to ask anything about my experience, education, and projects!",
    "Hello! I am the virtual assistant for <strong>Adilio Farias</strong>. I use Adilio's resume and the technical READMEs of his public repositories as career context. Ask about Adilio's professional experience, education, and projects.",
)

# External new-tab links should not retain a reference to the opener window.
replace_all('target="_blank" class=', 'target="_blank" rel="noopener noreferrer" class=')

# ---------------------------------------------------------------------------
# Add translation strings once to each language object.
# ---------------------------------------------------------------------------
pt_anchor = '        proj7_desc: "Motor antifraude PIX em tempo real com FastAPI, feature stores Redis/PostgreSQL, LightGBM + Isolation Forest, explicabilidade SHAP, MLflow e monitoramento contínuo de drift, com p95 inferior a 15 ms no benchmark do projeto.",\n'
pt_extra = pt_anchor + '''        proj1_highlight: "<strong class=\\"text-purple-300\\">Destaque:</strong> LLM local ($0.00) • ActionGateway • Multi-Agent",\n        proj2_highlight: "<strong class=\\"text-amber-300\\">Destaque:</strong> Sharpe 1,42 (backtest) • Hit Rate 56,8% • Purged CV",\n        proj3_highlight: "<strong class=\\"text-cyan-300\\">Destaque:</strong> EVAL semissintético (96 casos) • TRUE/FALSE/UNDECIDABLE",\n        proj4_highlight: "<strong class=\\"text-indigo-300\\">Destaque:</strong> 473.791 registros • Faithfulness 98% • MRR 0,88",\n        proj5_highlight: "<strong class=\\"text-emerald-300\\">Destaque:</strong> Dados sintéticos • PD/LGD/EAD • ECL • Rastreabilidade",\n        proj6_highlight: "<strong class=\\"text-emerald-300\\">Destaque:</strong> Benchmark sintético • ROC-AUC 0,9818 • Gini 0,9637 • KS 0,8627",\n        proj7_highlight: "<strong class=\\"text-emerald-300\\">Destaque:</strong> Benchmark do projeto • Recall 99,86% • FPR 0,957% • p95 &lt; 15 ms",\n        skill_ds_1: "• Séries Temporais (LSTM / SARIMAX)",\n        skill_ds_2: "• Detecção de Anomalias & Fraudes",\n        skill_ds_3: "• Credit Scoring & Modelos de Risco",\n        skill_eng_1: "• FastAPI, Python & Microsserviços",\n        skill_gov_1: "• Metodologias Ágeis & Scrum",\n        chat_placeholder: "Pergunte sobre experiências, formação, projetos ou contratação...",\n'''
replace_once(pt_anchor, pt_extra)

en_anchor = '        proj7_desc: "Real-time PIX anti-fraud engine with FastAPI, Redis/PostgreSQL feature stores, LightGBM + Isolation Forest, SHAP explainability, MLflow, and continuous drift monitoring, with p95 below 15 ms in the project benchmark.",\n'
en_extra = en_anchor + '''        proj1_highlight: "<strong class=\\"text-purple-300\\">Highlight:</strong> Local LLM ($0.00) • ActionGateway • Multi-Agent",\n        proj2_highlight: "<strong class=\\"text-amber-300\\">Highlight:</strong> Sharpe 1.42 (backtest) • Hit Rate 56.8% • Purged CV",\n        proj3_highlight: "<strong class=\\"text-cyan-300\\">Highlight:</strong> Semisynthetic EVAL (96 cases) • TRUE/FALSE/UNDECIDABLE",\n        proj4_highlight: "<strong class=\\"text-indigo-300\\">Highlight:</strong> 473,791 records • Faithfulness 98% • MRR 0.88",\n        proj5_highlight: "<strong class=\\"text-emerald-300\\">Highlight:</strong> Synthetic data • PD/LGD/EAD • ECL • Traceability",\n        proj6_highlight: "<strong class=\\"text-emerald-300\\">Highlight:</strong> Synthetic benchmark • ROC-AUC 0.9818 • Gini 0.9637 • KS 0.8627",\n        proj7_highlight: "<strong class=\\"text-emerald-300\\">Highlight:</strong> Project benchmark • Recall 99.86% • FPR 0.957% • p95 &lt; 15 ms",\n        skill_ds_1: "• Time Series (LSTM / SARIMAX)",\n        skill_ds_2: "• Anomaly & Fraud Detection",\n        skill_ds_3: "• Credit Scoring & Risk Models",\n        skill_eng_1: "• FastAPI, Python & Microservices",\n        skill_gov_1: "• Agile Methods & Scrum",\n        chat_placeholder: "Ask about experience, education, projects, or hiring...",\n'''
replace_once(en_anchor, en_extra)

INDEX.write_text(html, encoding="utf-8")
print("Applied bilingual recruiter-facing UI hardening.")

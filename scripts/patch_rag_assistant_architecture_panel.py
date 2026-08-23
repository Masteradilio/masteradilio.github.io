from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

start_marker = '    <section id="assistente"'
end_marker = '    <section id="contato"'
start = text.find(start_marker)
end = text.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit('Assistant section markers not found')

new_section = '''    <section id="assistente" class="py-16 sm:py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto border-t border-slate-800/80">
      <div class="glass-card rounded-2xl p-6 sm:p-8 border border-cyan-500/40 shadow-2xl glow-cyan space-y-6">
        <div class="flex items-center justify-between border-b border-slate-800 pb-4">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-indigo-600 flex items-center justify-center text-white text-lg shadow-md">
              <i class="fa-solid fa-robot"></i>
            </div>
            <div>
              <h3 class="font-bold text-white text-base sm:text-lg" data-i18n="bot_title">Assistente interativo sobre mim</h3>
              <p class="text-[11px] sm:text-xs text-slate-400" data-i18n="bot_subtitle">Faça sua própria pergunta sobre minhas experiências, formação ou projetos. Perguntas de conteúdo são respondidas pelo LLM com contexto RAG.</p>
            </div>
          </div>
        </div>

        <div class="flex flex-wrap items-center justify-between gap-2 text-xs bg-slate-900/60 p-3 rounded-xl border border-slate-800">
          <div class="flex items-center gap-2 text-slate-300 font-medium">
            <i class="fa-solid fa-file-lines text-cyan-400"></i>
            <span data-i18n="rag_status_label">Currículo completo (HTML)</span>
          </div>
          <div class="flex items-center gap-2">
            <a href="assets/cv_adilio_farias_pt.html" target="_blank" rel="noopener noreferrer" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700 hover:border-cyan-500 transition-colors flex items-center gap-1.5 font-medium shadow-sm">
              <span>🇧🇷</span> <span data-i18n="btn_cv_pt_short">CV (PT-BR)</span>
            </a>
            <a href="assets/cv_adilio_farias_en.html" target="_blank" rel="noopener noreferrer" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700 hover:border-cyan-500 transition-colors flex items-center gap-1.5 font-medium shadow-sm">
              <span>🇺🇸</span> <span data-i18n="btn_cv_en_short">Resume (EN)</span>
            </a>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-[minmax(0,2fr)_minmax(300px,0.85fr)] gap-5 lg:gap-6 items-start">
          <div class="min-w-0 space-y-4">
            <div class="p-4 sm:p-6 rounded-xl bg-slate-950/90 border border-slate-800 h-[480px] sm:h-[540px] overflow-y-auto space-y-4 font-sans text-xs sm:text-sm" id="chat-box" aria-live="polite" aria-label="AI career assistant conversation">
              <div class="flex gap-2.5">
                <div class="w-7 h-7 rounded-full bg-cyan-500 flex items-center justify-center text-white text-[10px] font-bold shrink-0 shadow">AI</div>
                <div class="p-4 rounded-xl rounded-tl-none bg-slate-800 text-slate-200 leading-relaxed max-w-[95%] w-full" id="bot-welcome-msg">
                  Olá! Sou o assistente virtual de <strong>Adilio Farias</strong>. Estou conectado aos currículos e aos READMEs técnicos dos repositórios públicos. Pergunte sobre a experiência profissional, formação e projetos de Adilio.
                </div>
              </div>
            </div>

            <form id="chat-form" class="flex gap-2">
              <input type="text" id="chat-input" maxlength="1200" autocomplete="off" data-i18n-placeholder="chat_placeholder" placeholder="Pergunte sobre experiências, formação, projetos ou contratação..." class="flex-1 px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500">
              <button type="submit" id="chat-submit-btn" class="px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 font-semibold text-xs sm:text-sm text-white transition-all flex items-center gap-2">
                <span data-i18n="bot_send_btn">Perguntar</span> <i class="fa-solid fa-paper-plane text-xs"></i>
              </button>
            </form>
            <p class="text-[11px] text-slate-400 italic text-center sm:text-left mt-2" data-i18n="chat_latency_note">Observação: as respostas de conteúdo são geradas pelo LLM com RAG e podem levar até 60 segundos no tier gratuito. Contato e acesso ao currículo usam apenas respostas utilitárias determinísticas.</p>
          </div>

          <aside id="rag-architecture-panel" class="rounded-xl bg-slate-950/70 border border-cyan-500/25 p-5 sm:p-6 lg:h-[540px] overflow-hidden flex flex-col shadow-lg shadow-cyan-950/20">
            <div class="flex items-start gap-3 pb-4 border-b border-slate-800">
              <div class="w-9 h-9 rounded-lg bg-cyan-500/15 border border-cyan-500/25 text-cyan-300 flex items-center justify-center shrink-0">
                <i class="fa-solid fa-diagram-project"></i>
              </div>
              <div>
                <h3 class="text-sm sm:text-base font-extrabold text-white leading-tight" data-i18n="bot_arch_title">Built by me — How this assistant works</h3>
                <p class="text-[10px] sm:text-[11px] text-cyan-400/80 mt-1 font-mono">RAG · LLM · Resilience · Guardrails</p>
              </div>
            </div>

            <div class="flex-1 py-4 space-y-3 overflow-y-auto pr-1">
              <div class="flex gap-3">
                <div class="w-7 h-7 rounded-lg bg-cyan-500/10 text-cyan-400 flex items-center justify-center shrink-0"><i class="fa-solid fa-database text-[11px]"></i></div>
                <div><h4 class="text-xs font-bold text-white" data-i18n="bot_arch_1_title">Grounded RAG</h4><p class="text-[11px] text-slate-400 leading-relaxed mt-0.5" data-i18n="bot_arch_1_desc">Respostas fundamentadas no meu currículo e nos meus Github Projects públicos.</p></div>
              </div>
              <div class="flex gap-3">
                <div class="w-7 h-7 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center shrink-0"><i class="fa-solid fa-link text-[11px]"></i></div>
                <div><h4 class="text-xs font-bold text-white" data-i18n="bot_arch_2_title">Source attribution</h4><p class="text-[11px] text-slate-400 leading-relaxed mt-0.5" data-i18n="bot_arch_2_desc">As respostas referenciam as fontes de portfólio usadas como evidência de suporte.</p></div>
              </div>
              <div class="flex gap-3">
                <div class="w-7 h-7 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center shrink-0"><i class="fa-solid fa-arrows-rotate text-[11px]"></i></div>
                <div><h4 class="text-xs font-bold text-white" data-i18n="bot_arch_3_title">Multi-provider fallback</h4><p class="text-[11px] text-slate-400 leading-relaxed mt-0.5" data-i18n="bot_arch_3_desc">Vercel AI Gateway, OpenRouter e Hugging Face fornecem roteamento resiliente de LLMs e failover.</p></div>
              </div>
              <div class="flex gap-3">
                <div class="w-7 h-7 rounded-lg bg-rose-500/10 text-rose-400 flex items-center justify-center shrink-0"><i class="fa-solid fa-shield-halved text-[11px]"></i></div>
                <div><h4 class="text-xs font-bold text-white" data-i18n="bot_arch_4_title">Guardrails</h4><p class="text-[11px] text-slate-400 leading-relaxed mt-0.5" data-i18n="bot_arch_4_desc">A validação separa experiência profissional de evidências de portfólio e bloqueia afirmações sem suporte.</p></div>
              </div>
              <div class="flex gap-3">
                <div class="w-7 h-7 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center shrink-0"><i class="fa-solid fa-language text-[11px]"></i></div>
                <div><h4 class="text-xs font-bold text-white" data-i18n="bot_arch_5_title">Bilingual UX</h4><p class="text-[11px] text-slate-400 leading-relaxed mt-0.5" data-i18n="bot_arch_5_desc">Suporte a PT-BR e inglês em toda a experiência.</p></div>
              </div>
              <div class="flex gap-3">
                <div class="w-7 h-7 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center shrink-0"><i class="fa-solid fa-gears text-[11px]"></i></div>
                <div><h4 class="text-xs font-bold text-white" data-i18n="bot_arch_6_title">Production mindset</h4><p class="text-[11px] text-slate-400 leading-relaxed mt-0.5" data-i18n="bot_arch_6_desc">Construído com grounding de fontes, validação de saída, resiliência e experiência do usuário em mente.</p></div>
              </div>
            </div>

            <div class="pt-4 border-t border-slate-800">
              <p class="text-[11px] text-slate-300 leading-relaxed" data-i18n="bot_arch_closing">Este assistente RAG é, por si só, um projeto de portfólio que demonstra como posso projetar assistentes de IA semelhantes para conhecimento interno e suporte ao cliente em empresas.</p>
            </div>
          </aside>
        </div>
      </div>
    </section>'''

text = text[:start] + new_section + '\n\n' + text[end:]

pt_anchor = '        bot_subtitle: "Faça sua própria pergunta sobre minhas experiências, formação ou projetos. Perguntas de conteúdo são respondidas pelo LLM com contexto RAG.",\n'
pt_insert = pt_anchor + '''        bot_arch_title: "Built by me — How this assistant works",
        bot_arch_1_title: "Grounded RAG",
        bot_arch_1_desc: "Respostas fundamentadas no meu currículo e nos meus Github Projects públicos.",
        bot_arch_2_title: "Atribuição de fontes",
        bot_arch_2_desc: "As respostas referenciam as fontes de portfólio usadas como evidência de suporte.",
        bot_arch_3_title: "Fallback multi-provider",
        bot_arch_3_desc: "Vercel AI Gateway, OpenRouter e Hugging Face fornecem roteamento resiliente de LLMs e failover.",
        bot_arch_4_title: "Guardrails",
        bot_arch_4_desc: "A validação separa experiência profissional de evidências de portfólio e bloqueia afirmações sem suporte.",
        bot_arch_5_title: "Experiência bilíngue",
        bot_arch_5_desc: "Suporte a PT-BR e inglês em toda a experiência.",
        bot_arch_6_title: "Mentalidade de produção",
        bot_arch_6_desc: "Construído com grounding de fontes, validação de saída, resiliência e experiência do usuário em mente.",
        bot_arch_closing: "Este assistente RAG é, por si só, um projeto de portfólio que demonstra como posso projetar assistentes de IA semelhantes para conhecimento interno e suporte ao cliente em empresas.",
'''
if text.count(pt_anchor) != 1:
    raise SystemExit(f'PT translation anchor count={text.count(pt_anchor)}')
text = text.replace(pt_anchor, pt_insert, 1)

en_anchor = '        bot_subtitle: "Ask your own question about my experience, education, or projects. Content questions are answered by the LLM using RAG context.",\n'
en_insert = en_anchor + '''        bot_arch_title: "Built by me — How this assistant works",
        bot_arch_1_title: "Grounded RAG",
        bot_arch_1_desc: "Answers are grounded in my resume and public Github Projects.",
        bot_arch_2_title: "Source attribution",
        bot_arch_2_desc: "Responses reference the portfolio sources used as supporting evidence.",
        bot_arch_3_title: "Multi-provider fallback",
        bot_arch_3_desc: "Vercel AI Gateway, OpenRouter, and Hugging Face provide resilient LLM routing and failover.",
        bot_arch_4_title: "Guardrails",
        bot_arch_4_desc: "Validation separates professional experience from portfolio evidence and blocks unsupported claims.",
        bot_arch_5_title: "Bilingual UX",
        bot_arch_5_desc: "Supports PT-BR and English across the experience.",
        bot_arch_6_title: "Production mindset",
        bot_arch_6_desc: "Built with source grounding, output validation, resilience, and user experience in mind.",
        bot_arch_closing: "This RAG assistant is itself a portfolio project demonstrating how I can design similar AI assistants for internal knowledge and customer support for companies.",
'''
if text.count(en_anchor) != 1:
    raise SystemExit(f'EN translation anchor count={text.count(en_anchor)}')
text = text.replace(en_anchor, en_insert, 1)

# Structural safety checks: preserve the live chat hooks exactly once.
for token in ['id="chat-box"', 'id="chat-form"', 'id="chat-input"', 'id="chat-submit-btn"', 'id="bot-welcome-msg"', 'id="rag-architecture-panel"']:
    if text.count(token) != 1:
        raise SystemExit(f'Unexpected count for {token}: {text.count(token)}')

# The new explanatory panel must avoid the terms requested by the site owner.
panel_start = text.find('<aside id="rag-architecture-panel"')
panel_end = text.find('</aside>', panel_start)
panel = text[panel_start:panel_end]
for forbidden in ['README', 'readme', 'recruiter', 'Recruiter']:
    if forbidden in panel:
        raise SystemExit(f'Forbidden term in architecture panel: {forbidden}')

path.write_text(text, encoding='utf-8')
print('RAG_ASSISTANT_ARCHITECTURE_PANEL_PATCH_OK')

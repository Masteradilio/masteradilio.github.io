from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old_grid = 'class="grid grid-cols-1 lg:grid-cols-[minmax(0,2fr)_minmax(300px,0.85fr)] gap-5 lg:gap-6 items-start"'
new_grid = 'class="grid grid-cols-1 lg:grid-cols-3 gap-5 lg:gap-6 items-start"'
if old_grid not in text:
    raise SystemExit('assistant grid class not found')
text = text.replace(old_grid, new_grid, 1)

old_chat = '<div class="min-w-0 space-y-4">\n            <div class="p-4 sm:p-6 rounded-xl bg-slate-950/90 border border-slate-800 h-[480px] sm:h-[540px]'
new_chat = '<div class="min-w-0 space-y-4 lg:col-span-2">\n            <div class="p-4 sm:p-6 rounded-xl bg-slate-950/90 border border-slate-800 h-[480px] sm:h-[540px]'
if old_chat not in text:
    raise SystemExit('assistant chat column block not found')
text = text.replace(old_chat, new_chat, 1)

old_aside = '<aside id="rag-architecture-panel" class="rounded-xl bg-slate-950/70 border border-cyan-500/25 p-5 sm:p-6 lg:h-[540px]'
new_aside = '<aside id="rag-architecture-panel" class="lg:col-span-1 rounded-xl bg-slate-950/70 border border-cyan-500/25 p-5 sm:p-6 lg:h-[540px]'
if old_aside not in text:
    raise SystemExit('assistant architecture panel not found')
text = text.replace(old_aside, new_aside, 1)

path.write_text(text, encoding='utf-8')
print('ASSISTANT_PANEL_COLUMNS_FIXED')

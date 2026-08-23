from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old_grid = '<div class="grid grid-cols-1 lg:grid-cols-3 gap-5 lg:gap-6 items-start">'
new_grid = '<div class="assistant-workbench">'
if old_grid not in text:
    raise SystemExit('assistant grid wrapper not found')
text = text.replace(old_grid, new_grid, 1)

old_chat = '<div class="min-w-0 space-y-4 lg:col-span-2">'
new_chat = '<div class="assistant-chat-column min-w-0 space-y-4">'
if old_chat not in text:
    raise SystemExit('assistant chat column not found')
text = text.replace(old_chat, new_chat, 1)

old_aside = '<aside id="rag-architecture-panel" class="lg:col-span-1 rounded-xl'
new_aside = '<aside id="rag-architecture-panel" class="rounded-xl'
if old_aside not in text:
    raise SystemExit('assistant side panel class not found')
text = text.replace(old_aside, new_aside, 1)

marker = '    .gradient-text { background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #34d399 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }\n'
css = '''    .assistant-workbench {\n      display: grid;\n      grid-template-columns: minmax(0, 1fr);\n      gap: 1.25rem;\n      align-items: start;\n    }\n    .assistant-chat-column { min-width: 0; }\n    @media (min-width: 1024px) {\n      .assistant-workbench {\n        grid-template-columns: minmax(0, 1fr) 310px;\n        gap: 1.5rem;\n        align-items: start;\n      }\n      #rag-architecture-panel {\n        width: 310px;\n        height: 540px;\n        min-height: 540px;\n        max-height: 540px;\n      }\n    }\n'''
if '.assistant-workbench {' not in text:
    if marker not in text:
        raise SystemExit('style insertion marker not found')
    text = text.replace(marker, marker + css, 1)

path.write_text(text, encoding='utf-8')
print('ASSISTANT_WORKBENCH_LAYOUT_FIXED')

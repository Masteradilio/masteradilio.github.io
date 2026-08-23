from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
legacy = '''      #rag-architecture-panel {\n        width: 310px;\n        height: 540px;\n        min-height: 540px;\n        max-height: 540px;\n      }\n    }\n'''
if legacy not in text:
    raise SystemExit('legacy fixed-height panel CSS not found')
text = text.replace(legacy, '', 1)
path.write_text(text, encoding='utf-8')
print('ASSISTANT_TWO_CARD_CSS_CLEAN')

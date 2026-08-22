from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630
OUT = Path('assets/portfolio-og.png')
OUT.parent.mkdir(parents=True, exist_ok=True)

img = Image.new('RGB', (WIDTH, HEIGHT), (7, 11, 20))
draw = ImageDraw.Draw(img)

for y in range(HEIGHT):
    t = y / HEIGHT
    color = (
        int(7 + (13 - 7) * t),
        int(11 + (21 - 11) * t),
        int(20 + (39 - 20) * t),
    )
    draw.line([(0, y), (WIDTH, y)], fill=color)

draw.rounded_rectangle((65, 60, 1135, 570), radius=32, outline=(31, 46, 77), width=3, fill=(10, 16, 30))
draw.rounded_rectangle((85, 82, 245, 122), radius=18, fill=(6, 182, 212))

bold_candidates = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf',
]
regular_candidates = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf',
]


def first_existing(paths):
    for path in paths:
        if Path(path).exists():
            return path
    raise FileNotFoundError('No suitable system font found')


bold = first_existing(bold_candidates)
regular = first_existing(regular_candidates)

font_badge = ImageFont.truetype(bold, 22)
font_name = ImageFont.truetype(bold, 54)
font_title = ImageFont.truetype(bold, 36)
font_sub = ImageFont.truetype(regular, 24)

draw.text((105, 90), 'PORTFOLIO', font=font_badge, fill=(255, 255, 255))
draw.text((92, 165), 'Adilio Farias', font=font_name, fill=(241, 245, 249))
draw.text((92, 245), 'AI Engineer | Senior Data Scientist', font=font_title, fill=(56, 189, 248))
draw.text((92, 315), 'Machine Learning • Generative AI • LLMs • RAG • MLOps', font=font_sub, fill=(203, 213, 225))
draw.text((92, 370), 'Financial Services • Fraud Prevention • Credit Risk', font=font_sub, fill=(203, 213, 225))
draw.text((92, 455), 'masteradilio.github.io', font=font_sub, fill=(52, 211, 153))

img.save(OUT, format='PNG', optimize=True)
print(f'Generated {OUT} ({OUT.stat().st_size} bytes)')

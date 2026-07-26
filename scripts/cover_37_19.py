#!/usr/bin/env python3
"""
Gera capas para apostila 37 e webinar WB-19 no padrao do contribuidor.
Usa thumbnails existentes como base + moldura AcademIA.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import re

ROOT = Path('/workspace/Academ-IA').resolve()
DOCS = ROOT / 'docs' / 'ebooks'
THUMBS = ROOT / 'producao' / 'assets' / 'thumbnails'
APOSTILAS = ROOT / 'apostilas'
WEBINARS = ROOT / 'webinars'

W, H = 1200, 1600
font_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font_reg = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def fit_title(draw, text, max_width, max_lines=5, start=82, min_size=32):
    text = text.replace('—', ' - ').replace('·', ' · ')
    words = text.split()
    for size in range(start, min_size - 1, -2):
        font = ImageFont.truetype(font_bold, size)
        lines = []
        cur = ''
        for w in words:
            test = w if not cur else cur + ' ' + w
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        if len(lines) <= max_lines:
            return font, lines
    return ImageFont.truetype(font_bold, min_size), [text]


def draw_shield(draw, x, y, scale=1.0):
    pts = [
        (x, y), (x + 82 * scale, y), (x + 94 * scale, y + 24 * scale), (x + 78 * scale, y + 98 * scale),
        (x + 41 * scale, y + 126 * scale), (x + 4 * scale, y + 98 * scale), (x - 12 * scale, y + 24 * scale)
    ]
    draw.polygon(pts, fill=(17, 24, 38), outline=(198, 156, 84))
    draw.text((x + 20 * scale, y + 24 * scale), 'N', font=ImageFont.truetype(font_bold, int(54 * scale)), fill=(115, 224, 255))


def render_cover(dst, title, subtitle, src, category='APOSTILA', issue="NEXUS AFFIL'IA'TE"):
    src_img = Image.open(src).convert('RGB')
    bg = ImageOps.fit(src_img, (W, H), Image.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=20))
    dark = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(dark)
    d.rectangle((0, 0, W, H), fill=(6, 10, 18, 122))
    for i in range(H):
        alpha = int(170 * (i / H))
        d.line((0, i, W, i), fill=(4, 7, 12, alpha))
    frame = Image.alpha_composite(bg.convert('RGBA'), dark)
    d = ImageDraw.Draw(frame)

    d.rounded_rectangle((120, 120, 1080, 720), radius=36, fill=(10, 14, 22, 105), outline=(72, 210, 255, 120), width=3)
    inner_box = Image.new('RGBA', (880, 560), (0, 0, 0, 0))
    contained = ImageOps.contain(src_img, (880, 560), Image.LANCZOS).convert('RGBA')
    ox = (880 - contained.width) // 2
    oy = (560 - contained.height) // 2
    inner_box.alpha_composite(contained, (ox, oy))
    frame.alpha_composite(inner_box, (160, 140))
    d.rounded_rectangle((120, 120, 1080, 720), radius=36, outline=(198, 156, 84, 210), width=5)

    d.rounded_rectangle((90, 760, 1110, 1490), radius=42, fill=(8, 12, 20, 226), outline=(198, 156, 84, 210), width=4)
    d.line((130, 840, 1070, 840), fill=(72, 210, 255, 180), width=4)
    d.line((130, 1430, 1070, 1430), fill=(198, 156, 84, 140), width=2)

    draw_shield(d, 930, 42, 1.1)

    small = ImageFont.truetype(font_reg, 30)
    cat_font = ImageFont.truetype(font_bold, 34)
    sub_font = ImageFont.truetype(font_reg, 33)
    micro = ImageFont.truetype(font_reg, 24)

    d.text((125, 790), "ACADEM'IA · SISTEMA EAD NEXUS", font=small, fill=(120, 224, 255))
    d.text((125, 852), category, font=cat_font, fill=(212, 168, 88))
    title_font, lines = fit_title(d, title, 900)
    y = 918
    for line in lines:
        d.text((129, y + 4), line, font=title_font, fill=(0, 0, 0, 160))
        d.text((125, y), line, font=title_font, fill=(248, 239, 220))
        y += int(title_font.size * 1.08)
    if subtitle:
        y += 18
        sub_lines = []
        cur = ''
        for w in subtitle.split():
            t = w if not cur else cur + ' ' + w
            if d.textbbox((0, 0), t, font=sub_font)[2] <= 900:
                cur = t
            else:
                if cur:
                    sub_lines.append(cur)
                cur = w
        if cur:
            sub_lines.append(cur)
        for line in sub_lines[:3]:
            d.text((125, y), line, font=sub_font, fill=(208, 217, 228))
            y += 45
    d.text((125, 1368), 'VISUAL · IVE + ALENCAR', font=micro, fill=(166, 198, 214))
    d.text((125, 1410), issue, font=micro, fill=(166, 198, 214))
    frame.convert('RGB').save(dst, format='WEBP', quality=96, method=6)
    print(f'OK {dst.relative_to(ROOT)} from {src.name}')


# Capas a gerar: apostila 37 + webinar WB-19
TARGETS = [
    {
        'dst': 'ACAD-apostila-37-mentoria-ia-coaching.webp',
        'src': 'capa-22-master-mentoria-ive.png',
        'title': 'Mentoria 1:1 com IA',
        'subtitle': 'Como atender 100+ alunos sem perder o toque humano. A Dupla Nexus (Ive + Alencar) compartilha o método de 12 anos.',
        'category': 'APOSTILA 37',
    },
    {
        'dst': 'WB-2026-19-mentoria-ia-100-alunos.webp',
        'src': 'capa-22-master-mentoria-ive.png',
        'title': 'Mentoria com IA · 100 Alunos',
        'subtitle': 'Como usar IA para escalar atendimento 1:1 sem perder qualidade. Cases reais com a Dupla (Ive + Alencar).',
        'category': 'WEBINAR WB-19',
    },
]


def main():
    for t in TARGETS:
        dst = DOCS / t['dst']
        src = THUMBS / t['src']
        if not src.exists():
            print(f'FALTA src: {src}')
            continue
        render_cover(dst, t['title'], t['subtitle'], src, t['category'])


if __name__ == '__main__':
    main()

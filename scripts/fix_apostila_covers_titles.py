from __future__ import annotations

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path('/home/user/repo/Academ-IA')
APOSTILAS = ROOT / 'apostilas'
IMG_ROOT = APOSTILAS / 'imagens'

FILES = [
    '16-trilha-fundamental-ia.md',
    '20-trilha-elite-engenharia.md',
    '21-trilha-master-arquitetura.md',
    '22-trilha-master-mentoria.md',
    '23-curso-rag-pratico.md',
    '24-curso-agents-langgraph.md',
    '25-curso-prompt-engineering.md',
    '26-curso-vector-db.md',
    '27-curso-voice-ai.md',
    '28-curso-multimodal-rag.md',
]

COLORS = {
    'bg': (10, 15, 30),
    'teal': (70, 180, 195),
    'gold': (215, 175, 90),
    'white': (245, 247, 250),
    'muted': (205, 214, 223),
    'shadow': (0, 0, 0, 180),
    'panel': (7, 12, 24, 195),
    'panel2': (7, 12, 24, 120),
}

FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def parse_markdown(path: Path) -> dict:
    text = path.read_text(encoding='utf-8')
    code_match = re.search(r'^number:\s*"([^"]+)"', text, re.M)
    title_match = re.search(r'^#\s+(.+)$', text, re.M)
    subtitle_match = re.search(r'^##\s+(.+)$', text, re.M)
    spec_match = re.search(r'^(Apostila\s+[A-Z0-9]+\s+·\s+.+)$', text, re.M)
    category_match = re.search(r'^\*\*Categoria:\*\*\s+(.+)$', text, re.M)
    if not (code_match and title_match and subtitle_match and spec_match):
        raise ValueError(f'Não foi possível extrair metadados de {path}')
    return {
        'code': code_match.group(1).strip(),
        'title': title_match.group(1).strip(),
        'subtitle': subtitle_match.group(1).strip(),
        'spec': spec_match.group(1).strip(),
        'category': category_match.group(1).strip() if category_match else 'AcademIA',
        'md': path.name,
    }


def fit_text(draw: ImageDraw.ImageDraw, text: str, font_path: str, max_width: int, start_size: int, min_size: int) -> ImageFont.FreeTypeFont:
    size = start_size
    while size >= min_size:
        font = ImageFont.truetype(font_path, size=size)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=max(8, size // 5))
        width = bbox[2] - bbox[0]
        if width <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(font_path, size=min_size)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> str:
    words = text.split()
    lines: list[str] = []
    current = ''
    for word in words:
        trial = (current + ' ' + word).strip()
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return '\n'.join(lines)


def add_overlay(im: Image.Image, meta: dict) -> Image.Image:
    base = im.convert('RGBA')
    w, h = base.size

    # Soften background where text sits.
    blur_panel = base.filter(ImageFilter.GaussianBlur(radius=12))
    mask = Image.new('L', (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, int(h * 0.50), w, h), radius=40, fill=225)
    base = Image.composite(blur_panel, base, mask)

    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # Bottom dark gradient panel.
    top_y = int(h * 0.50)
    for i in range(top_y, h):
        alpha = int(30 + 200 * ((i - top_y) / max(1, h - top_y)))
        od.line((0, i, w, i), fill=(6, 10, 20, min(alpha, 230)))

    # Left accent strip.
    od.rounded_rectangle((int(w*0.04), int(h*0.08), int(w*0.055), int(h*0.92)), radius=12, fill=COLORS['teal'] + (235,))

    # Header chip.
    chip_x1, chip_y1 = int(w * 0.09), int(h * 0.08)
    chip_x2, chip_y2 = int(w * 0.30), int(h * 0.15)
    od.rounded_rectangle((chip_x1, chip_y1, chip_x2, chip_y2), radius=18, fill=COLORS['panel'])
    chip_font = ImageFont.truetype(FONT_BOLD, size=max(26, w // 55))
    chip_text = f"{meta['code']} · {meta['category']}"
    od.text((chip_x1 + 22, chip_y1 + 16), chip_text, font=chip_font, fill=COLORS['gold'])

    canvas = Image.alpha_composite(base, overlay)
    draw = ImageDraw.Draw(canvas)
    left = int(w * 0.09)
    text_w = int(w * 0.80)

    title_font = fit_text(draw, meta['title'], FONT_BOLD, text_w, start_size=max(58, w // 21), min_size=42)
    title_wrapped = wrap_text(draw, meta['title'], title_font, text_w)
    title_bbox = draw.multiline_textbbox((0, 0), title_wrapped, font=title_font, spacing=12)
    title_h = title_bbox[3] - title_bbox[1]

    subtitle_font = fit_text(draw, meta['subtitle'], FONT_REG, text_w, start_size=max(34, w // 38), min_size=24)
    subtitle_wrapped = wrap_text(draw, meta['subtitle'], subtitle_font, text_w)
    subtitle_bbox = draw.multiline_textbbox((0, 0), subtitle_wrapped, font=subtitle_font, spacing=10)
    subtitle_h = subtitle_bbox[3] - subtitle_bbox[1]

    spec_font = fit_text(draw, meta['spec'], FONT_REG, text_w, start_size=max(24, w // 60), min_size=20)
    spec_wrapped = wrap_text(draw, meta['spec'], spec_font, text_w)
    spec_bbox = draw.multiline_textbbox((0, 0), spec_wrapped, font=spec_font, spacing=8)
    spec_h = spec_bbox[3] - spec_bbox[1]

    block_h = title_h + subtitle_h + spec_h + 60
    y = max(int(h * 0.58), h - block_h - int(h * 0.12))

    shadow_dx = max(2, w // 700)
    shadow_dy = shadow_dx

    def shadow_text(x: int, y_: int, txt: str, font: ImageFont.FreeTypeFont, fill: tuple[int, int, int], spacing: int = 10):
        draw.multiline_text((x + shadow_dx, y_ + shadow_dy), txt, font=font, fill=COLORS['shadow'], spacing=spacing)
        draw.multiline_text((x, y_), txt, font=font, fill=fill, spacing=spacing)

    shadow_text(left, y, title_wrapped, title_font, COLORS['white'], spacing=12)
    y += title_h + 18
    shadow_text(left, y, subtitle_wrapped, subtitle_font, COLORS['muted'], spacing=10)
    y += subtitle_h + 18
    shadow_text(left, y, spec_wrapped, spec_font, COLORS['gold'], spacing=8)

    footer_font = ImageFont.truetype(FONT_REG, size=max(20, w // 75))
    footer = 'AcademIA · Nexus HUB57 · Apostilas Técnicas'
    fb = draw.textbbox((0, 0), footer, font=footer_font)
    draw.text((w - (fb[2] - fb[0]) - int(w * 0.05), h - int(h * 0.07)), footer, font=footer_font, fill=COLORS['muted'])
    return canvas.convert('RGB')


def process(md_name: str) -> str:
    md_path = APOSTILAS / md_name
    meta = parse_markdown(md_path)
    img_path = IMG_ROOT / meta['code'] / 'cover.png'
    backup_path = IMG_ROOT / meta['code'] / 'cover.original.png'
    if not img_path.exists():
        raise FileNotFoundError(img_path)
    if not backup_path.exists():
        backup_path.write_bytes(img_path.read_bytes())
    im = Image.open(backup_path)
    out = add_overlay(im, meta)
    out.save(img_path, quality=95)
    return f"{meta['code']}|{meta['title']}|{img_path.relative_to(ROOT)}"


def main() -> None:
    results = [process(name) for name in FILES]
    print('\n'.join(results))


if __name__ == '__main__':
    main()

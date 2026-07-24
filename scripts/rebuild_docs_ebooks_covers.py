from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import re
import math

ROOT = Path('/home/user/repo/Academ-IA').resolve()
DOCS = ROOT / 'docs' / 'ebooks'
THUMBS = ROOT / 'producao' / 'assets' / 'thumbnails'
APOSTILAS = ROOT / 'apostilas'
WEBINARS = ROOT / 'webinars'

W, H = 1200, 1600
font_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font_reg = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

slug_cleanup = re.compile(r'[^a-z0-9]+')
stop = {'de','da','do','dos','das','e','em','com','para','o','a','ia','2026'}


def slugify(s: str) -> str:
    s = s.lower()
    s = s.replace("'", '')
    s = slug_cleanup.sub('-', s)
    return s.strip('-')


def tokens(s: str):
    return [t for t in slugify(s).split('-') if t and t not in stop]


def read_frontmatter_title_subtitle(md: Path):
    title = None
    subtitle = None
    if not md.exists():
        return None, None
    txt = md.read_text(encoding='utf-8', errors='ignore')
    lines = txt.splitlines()
    for i, line in enumerate(lines[:40]):
        if line.startswith('title:'):
            title = line.split(':',1)[1].strip().strip('"')
        elif line.startswith('subtitle:'):
            subtitle = line.split(':',1)[1].strip().strip('"')
        elif line.startswith('# ') and not title:
            title = line[2:].strip()
    return title, subtitle


def choose_source_for_cover(filename: str):
    stem = Path(filename).stem
    # ACAD-apostila-XX-slug
    m = re.match(r'ACAD-apostila-(\d+)-(.+)', stem)
    if m:
        num = int(m.group(1))
        slug = m.group(2)
        custom = {
            1: 'capa-01-entendendo-ioaid-dupla.png',
            2: 'capa-08-otimizacao-conversao-dupla.png',
            3: 'capa-01-entendendo-ioaid-dupla.png',
            4: 'capa-02-sistema-sho-dupla.png',
            5: 'capa-03-painel-afiliado-ive.png',
            6: 'capa-04-primeiro-agente-dupla.png',
            7: 'capa-05-skills-essenciais-alencar.png',
            8: 'capa-06-disparo-whatsapp-alencar.png',
            9: 'capa-08-otimizacao-conversao-dupla.png',
            10: 'capa-09-funis-lifecycle-dupla.png',
            11: 'capa-02-sistema-sho-dupla.png',
            12: 'capa-01-entendendo-ioaid-dupla.png',
            13: 'capa-aula-10-marketplaces-ive.png',
            14: 'capa-13-multi-tenant-dupla.png',
            34: 'capa-33-data-stack-agentes-alencar.png',
            35: 'capa-31-fabrica-conteudo-ive.png',
        }
        if num in custom and (THUMBS / custom[num]).exists():
            return THUMBS / custom[num]
        cands = sorted(THUMBS.glob(f'capa-{num:02d}-*.png'))
        if cands:
            want = set(tokens(slug))
            best = None
            best_score = -1
            for c in cands:
                score = len(want.intersection(set(tokens(c.stem))))
                if score > best_score:
                    best = c
                    best_score = score
            return best or cands[0]
    # webinar
    if stem.startswith('WB-2026-'):
        slug = stem.split('-', 3)[-1]
        all_cands = sorted(THUMBS.glob('capa-*.png'))
        want = set(tokens(slug))
        fallback = THUMBS / 'capa-21-master-arquitetura-dupla.png'
        mapping = {
            'lancamento-ioaid': 'capa-01-entendendo-ioaid-dupla.png',
            'sho-em-producao': 'capa-02-sistema-sho-dupla.png',
            'academia-open-house': 'capa-00-boas-vindas-ive.png',
            'skills-em-producao': 'capa-05-skills-essenciais-alencar.png',
            'multi-tenant': 'capa-13-multi-tenant-dupla.png',
            'ab-test-estatistico': 'capa-10-ab-testing-judge-dupla.png',
            'lgpd-ia': 'capa-07-judge-revisor-alencar.png',
            'financeiro-ia': 'capa-11-coortes-churn-dupla.png',
            'agentes-autonomos-prod': 'capa-17-poder-perigo-autonomia-dupla.png',
            'seo-vs-ia-generativa': 'capa-17-seo-marketing-dupla.png',
            'burnout-afiliados': 'capa-22-master-mentoria-ive.png',
            'ia-to-ia-federation': 'capa-30-federacao-zero-trust-dupla.png',
            'criacao-conteudo-ia': 'capa-31-fabrica-conteudo-ive.png',
            'pricing-ia-tempo-real': 'capa-32-pricing-ia-2026-dupla.png',
            'data-stack-ia': 'capa-33-data-stack-agentes-alencar.png',
            'deploy-continuo-ia': 'capa-33-data-stack-agentes-alencar.png',
            'conversa-vende-ia': 'capa-31-fabrica-conteudo-ive.png',
        }
        for k,v in mapping.items():
            if k in slug and (THUMBS / v).exists():
                return THUMBS / v
        best = None
        best_score = -1
        for c in all_cands:
            score = len(want.intersection(set(tokens(c.stem))))
            if score > best_score:
                best = c
                best_score = score
        return best or fallback
    return THUMBS / 'capa-21-master-arquitetura-dupla.png'


def choose_theme(src_name: str):
    s = src_name.lower()
    if 'ive' in s and 'dupla' not in s:
        return 'IVE'
    if 'alencar' in s and 'dupla' not in s:
        return 'ALENCAR'
    return 'IVE + ALENCAR'


def fit_title(draw, text, max_width, max_lines=4, start=82, min_size=34):
    text = text.replace('—', ' ').replace('·', ' ')
    for size in range(start, min_size-1, -2):
        font = ImageFont.truetype(font_bold, size)
        words = text.split()
        lines=[]
        cur=''
        for w in words:
            test = w if not cur else cur + ' ' + w
            bbox = draw.textbbox((0,0), test, font=font)
            if bbox[2]-bbox[0] <= max_width:
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
        (x, y), (x+82*scale, y), (x+94*scale, y+24*scale), (x+78*scale, y+98*scale),
        (x+41*scale, y+126*scale), (x+4*scale, y+98*scale), (x-12*scale, y+24*scale)
    ]
    draw.polygon(pts, fill=(17,24,38), outline=(198,156,84))
    draw.text((x+20*scale, y+24*scale), 'N', font=ImageFont.truetype(font_bold, int(54*scale)), fill=(115,224,255))


def render_cover(dst: Path, title: str, subtitle: str, src: Path, category='APOSTILA', issue='NEXUS AFFIL\'IA\'TE'):
    src_img = Image.open(src).convert('RGB')
    bg = ImageOps.fit(src_img, (W,H), Image.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=18))
    dark = Image.new('RGBA', (W,H), (7,10,16,0))
    d = ImageDraw.Draw(dark)
    # layered overlays
    d.rectangle((0,0,W,H), fill=(6,10,18,115))
    for i in range(H):
        alpha = int(180 * (i / H))
        d.line((0,i,W,i), fill=(4,7,12,alpha))
    frame = Image.alpha_composite(bg.convert('RGBA'), dark)
    d = ImageDraw.Draw(frame)

    # main inner visual card from source
    inner = ImageOps.fit(src_img, (880, 560), Image.LANCZOS)
    inner = inner.convert('RGBA')
    d.rounded_rectangle((160,140,1040,700), radius=34, fill=(10,14,22,110), outline=(72,210,255,150), width=3)
    frame.alpha_composite(inner, (160,140))
    d.rounded_rectangle((160,140,1040,700), radius=34, outline=(198,156,84,210), width=5)

    # title panel
    d.rounded_rectangle((90,760,1110,1490), radius=42, fill=(8,12,20,220), outline=(198,156,84,210), width=4)
    d.line((130,840,1070,840), fill=(72,210,255,180), width=4)
    d.line((130,1430,1070,1430), fill=(198,156,84,140), width=2)

    draw_shield(d, 930, 42, 1.1)

    small = ImageFont.truetype(font_reg, 30)
    cat_font = ImageFont.truetype(font_bold, 34)
    sub_font = ImageFont.truetype(font_reg, 33)
    micro = ImageFont.truetype(font_reg, 24)

    d.text((125,790), "ACADEM'IA · SISTEMA EAD NEXUS", font=small, fill=(120,224,255))
    d.text((125,852), category, font=cat_font, fill=(212,168,88))
    title_font, lines = fit_title(d, title, 900)
    y = 918
    for line in lines:
        d.text((129, y+4), line, font=title_font, fill=(0,0,0,160))
        d.text((125, y), line, font=title_font, fill=(248,239,220))
        y += int(title_font.size * 1.08)
    if subtitle:
        y += 18
        sub_lines = []
        cur=''
        for w in subtitle.split():
            t = w if not cur else cur + ' ' + w
            if d.textbbox((0,0), t, font=sub_font)[2] <= 900:
                cur = t
            else:
                if cur: sub_lines.append(cur)
                cur = w
        if cur: sub_lines.append(cur)
        for line in sub_lines[:3]:
            d.text((125, y), line, font=sub_font, fill=(208,217,228))
            y += 45
    theme = choose_theme(src.name)
    d.text((125, 1368), f'VISUAL · {theme}', font=micro, fill=(166,198,214))
    d.text((125, 1410), issue, font=micro, fill=(166,198,214))

    frame.convert('RGB').save(dst, format='WEBP', quality=96, method=6)
    print('rebuilt', dst.relative_to(ROOT), 'from', src.name)


def derive_title_and_subtitle(file: Path):
    stem = file.stem
    m = re.match(r'ACAD-apostila-(\d+)-(.+)', stem)
    if m:
        num = int(m.group(1))
        slug = m.group(2)
        md = None
        for cand in APOSTILAS.glob(f'{num:02d}-*.md'):
            md = cand
            break
        if md:
            title, subtitle = read_frontmatter_title_subtitle(md)
            return title or slug.replace('-', ' ').title(), subtitle or 'Coleção oficial Academ\'IA'
        return slug.replace('-', ' ').title(), 'Coleção oficial Academ\'IA'
    if stem.startswith('WB-2026-'):
        md = WEBINARS / f'{stem}.md'
        title, subtitle = read_frontmatter_title_subtitle(md)
        if title:
            return title, subtitle or 'Webinar oficial da Academ\'IA'
        slug = stem.split('-',3)[-1].replace('-', ' ').title()
        return slug, 'Webinar oficial da Academ\'IA'
    return stem.replace('-', ' ').title(), 'Nexus Affil\'IA\'te'


def category_for(file: Path):
    if file.name.startswith('WB-2026-'):
        return 'WEBINAR'
    return 'APOSTILA'


def main():
    files = sorted(DOCS.glob('*.webp'))
    for f in files:
        title, subtitle = derive_title_and_subtitle(f)
        src = choose_source_for_cover(f.name)
        render_cover(f, title, subtitle, src, category_for(f))


if __name__ == '__main__':
    main()

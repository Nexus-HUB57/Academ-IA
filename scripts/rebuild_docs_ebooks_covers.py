from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import re

ROOT = Path('/home/user/repo/Academ-IA').resolve()
DOCS = ROOT / 'docs' / 'ebooks'
THUMBS = ROOT / 'producao' / 'assets' / 'thumbnails'
APOSTILAS = ROOT / 'apostilas'
WEBINARS = ROOT / 'webinars'

W, H = 1200, 1600
font_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font_reg = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

slug_cleanup = re.compile(r'[^a-z0-9]+')
stop = {'de','da','do','dos','das','e','em','com','para','o','a','ao','na','no','nas','nos','um','uma'}

SLUG_SOURCE_OVERRIDES = {
    'apresentacao-infraestrutura': 'capa-01-entendendo-ioaid-dupla.png',
    'cases-orquestracao-autonoma': 'capa-08-otimizacao-conversao-dupla.png',
    'infra-operacional-ia': 'capa-01-entendendo-ioaid-dupla.png',
    'orquestracao-hibrida-agentes': 'capa-02-sistema-sho-dupla.png',
    'sete-telas-essenciais': 'capa-03-painel-afiliado-ive.png',
    'setup-agente-pessoal': 'capa-04-primeiro-agente-dupla.png',
    '18-skills-operacionais': 'capa-05-skills-essenciais-alencar.png',
    'rotina-disparo-agente': 'capa-06-disparo-whatsapp-alencar.png',
    'campanhas-automatizadas': 'capa-09-funis-lifecycle-dupla.png',
    'jornada-completa-afiliado': 'capa-10-ab-testing-judge-dupla.png',
    'sho-em-producao': 'capa-02-sistema-sho-dupla.png',
    'ioaid-arquitetura-profunda': 'capa-01-entendendo-ioaid-dupla.png',
    'marketplace-skills': 'capa-aula-10-marketplaces-ive.png',
    'multi-tenant-whitelabel': 'capa-13-multi-tenant-dupla.png',
    'metricas-roi-ecossistema': 'capa-15-metricas-roi-alencar.png',
    'trilha-fundamental-ia': 'capa-16-trilha-fundamental-alencar.png',
    'seo-marketing-conteudo-ia': 'capa-17-seo-marketing-dupla.png',
    'seguranca-ofensiva-pentest-agentes-ia': 'capa-18-seguranca-pentest-alencar.png',
    'monetizacao-avancada-escala': 'capa-19-monetizacao-escala-dupla.png',
    'trilha-elite-engenharia': 'capa-20-elite-engenharia-alencar.png',
    'trilha-master-arquitetura': 'capa-21-master-arquitetura-dupla.png',
    'trilha-master-mentoria': 'capa-22-master-mentoria-ive.png',
    'curso-rag-pratico': 'capa-23-curso-rag-alencar.png',
    'curso-agents-langgraph': 'capa-24-curso-agents-langgraph-alencar.png',
    'curso-prompt-engineering': 'capa-25-curso-prompt-engineering-ive.png',
    'curso-vector-db': 'capa-26-curso-vector-db-alencar.png',
    'curso-voice-ai': 'capa-27-curso-voice-ai-ive.png',
    'curso-multimodal-rag': 'capa-28-curso-multimodal-rag-dupla.png',
    'ai-to-ai-protocol': 'capa-29-ai-to-ai-protocol-dupla.png',
    'federacao-zero-trust': 'capa-30-federacao-zero-trust-dupla.png',
    'fabrica-conteudo-ia': 'capa-31-fabrica-conteudo-ive.png',
    'pricing-ia-2026': 'capa-32-pricing-ia-2026-dupla.png',
    'data-stack-agentes-ia': 'capa-33-data-stack-agentes-alencar.png',
    'deploy-continuo-agentes-ia': 'capa-33-data-stack-agentes-alencar.png',
    'marketing-conversacional-ia': 'capa-31-fabrica-conteudo-ive.png',
    'comunidade-engajamento-ia': 'capa-22-master-mentoria-ive.png',
    'fundamentos-ia-ml': 'capa-aula-01-o-que-e-agente-ia-ive.png',
    'lancamento-ioaid': 'capa-01-entendendo-ioaid-dupla.png',
    'ia-to-ia-federation': 'capa-29-ai-to-ai-protocol-dupla.png',
    'academia-open-house': 'capa-00-boas-vindas-ive.png',
    'skills-em-producao': 'capa-05-skills-essenciais-alencar.png',
    'multi-tenant': 'capa-13-multi-tenant-dupla.png',
    'ab-test-estatistico': 'capa-10-ab-testing-judge-dupla.png',
    'lgpd-ia': 'capa-07-judge-revisor-alencar.png',
    'financeiro-ia': 'capa-11-coortes-churn-dupla.png',
    'agentes-autonomos-prod': 'capa-17-poder-perigo-autonomia-dupla.png',
    'seo-vs-ia-generativa': 'capa-17-seo-marketing-dupla.png',
    'burnout-afiliados': 'capa-22-master-mentoria-ive.png',
    'criacao-conteudo-ia': 'capa-31-fabrica-conteudo-ive.png',
    'pricing-ia-tempo-real': 'capa-32-pricing-ia-2026-dupla.png',
    'data-stack-ia': 'capa-33-data-stack-agentes-alencar.png',
    'deploy-continuo-ia': 'capa-33-data-stack-agentes-alencar.png',
    'conversa-vende-ia': 'capa-31-fabrica-conteudo-ive.png',
    'comunidade-tribo-ia': 'capa-22-master-mentoria-ive.png',
}

SLUG_TITLE_OVERRIDES = {
    'trilha-fundamental-ia': ('Trilha Fundamental IA', 'Base oficial da Academ\'IA para fundamentos, linguagem e operação inicial.'),
    'monetizacao-avancada-escala': ('Monetização Avançada & Escala', 'Estratégias para crescer receita, margem e previsibilidade com IA.'),
    'trilha-elite-engenharia': ('Trilha Elite · Engenharia', 'Profundidade técnica para arquitetar operações robustas e escaláveis.'),
    'trilha-master-arquitetura': ('Trilha Master · Arquitetura', 'Frameworks de arquitetura, governança e desenho sistêmico.'),
    'trilha-master-mentoria': ('Trilha Master · Mentoria', 'Mentoria estratégica para aceleração, posicionamento e liderança.'),
    'curso-rag-pratico': ('Curso RAG Prático', 'Recuperação aumentada com arquitetura aplicada e casos reais.'),
    'curso-agents-langgraph': ('Curso Agents + LangGraph', 'Construção de agentes stateful, workflows e orquestração avançada.'),
    'curso-prompt-engineering': ('Curso Prompt Engineering', 'Estruturação de prompts, avaliação, controle e ganho de performance.'),
    'curso-vector-db': ('Curso Vector DB', 'Embeddings, indexação semântica e busca vetorial em produção.'),
    'curso-voice-ai': ('Curso Voice AI', 'Síntese, clonagem, interação por voz e pipelines multimodais.'),
    'curso-multimodal-rag': ('Curso Multimodal RAG', 'Texto, imagem, áudio e contexto unificados em sistemas RAG.'),
    'comunidade-engajamento-ia': ('Comunidade & Engajamento com IA', 'Operação de comunidade, retenção e tribo com inteligência aplicada.'),
    'fundamentos-ia-ml': ('Fundamentos de IA & ML', 'Primeiros princípios para entender agentes, modelos e automação.'),
    'skills-em-producao': ('Skills em Produção', 'Padrões de operação, catálogo e uso real de skills no ecossistema Nexus.'),
    'academia-open-house': ('Academia Open House', 'Visão institucional, onboarding e jornada guiada pela Academ\'IA.'),
    'lancamento-ioaid': ('Lançamento IOAID', 'Abertura oficial da infraestrutura operacional distribuída da Nexus.'),
    'ia-to-ia-federation': ('IA-to-IA Federation', 'Protocolos, interoperabilidade e governança entre agentes de plataformas distintas.'),
    'multi-tenant': ('Multi-tenant & White-label', 'Arquitetura, isolamento e expansão com múltiplos clientes em uma única base.'),
    'ab-test-estatistico': ('A/B Test Estatístico', 'Experimentação rigorosa, leitura correta de resultado e tomada de decisão.'),
    'lgpd-ia': ('LGPD + IA', 'Conformidade, privacidade e operação segura com agentes em produção.'),
    'financeiro-ia': ('Financeiro com IA', 'Unit economics, previsibilidade e análise operacional para escala saudável.'),
    'agentes-autonomos-prod': ('Agentes Autônomos em Produção', 'Casos reais, padrões de operação e governança de runtime.'),
    'seo-vs-ia-generativa': ('SEO vs IA Generativa', 'Como ranquear e capturar demanda em um mundo mediado por modelos.'),
    'burnout-afiliados': ('Burnout de Afiliados', 'Sustentabilidade operacional, ritmo e desenho de rotina com IA.'),
    'criacao-conteudo-ia': ('Criação de Conteúdo com IA', 'Pipeline editorial para sair do zero e chegar à escala com qualidade.'),
    'pricing-ia-tempo-real': ('Pricing com IA em Tempo Real', 'Precificação dinâmica, elasticidade e sinais de mercado em produção.'),
    'data-stack-ia': ('Data Stack para Agentes IA', 'Pipelines de dados, armazenamento e observabilidade para agentes.'),
    'deploy-continuo-ia': ('Deploy Contínuo de Agentes IA', 'Entrega segura do Git à produção com rollback e monitoramento.'),
    'conversa-vende-ia': ('Conversa Vende', 'Marketing conversacional com IA para relacionamento e fechamento.'),
    'comunidade-tribo-ia': ('Comunidade & Tribo com IA', 'Engajamento, retenção e dinâmica de comunidade orientada por IA.'),
}

ACRONYMS = {
    'ia': 'IA', 'ml': 'ML', 'rag': 'RAG', 'seo': 'SEO', 'roi': 'ROI', 'db': 'DB',
    'ioaid': 'IOAID', 'sho': 'SHO', 'lgpd': 'LGPD', 'ci': 'CI', 'cd': 'CD', 'a2a': 'A2A'
}


def slugify(s: str) -> str:
    s = s.lower().replace("'", '')
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
    for line in txt.splitlines()[:50]:
        if line.startswith('title:'):
            title = line.split(':', 1)[1].strip().strip('"')
        elif line.startswith('subtitle:'):
            subtitle = line.split(':', 1)[1].strip().strip('"')
        elif line.startswith('# ') and not title:
            title = line[2:].strip()
    return title, subtitle


def prettify_slug(slug: str) -> str:
    parts = slug.split('-')
    out = []
    for p in parts:
        if p in ACRONYMS:
            out.append(ACRONYMS[p])
        elif p == 'whitelabel':
            out.append('White-label')
        elif p == 'multitenant':
            out.append('Multi-tenant')
        elif p == 'langgraph':
            out.append('LangGraph')
        elif p == 'voice':
            out.append('Voice')
        else:
            out.append(p.capitalize())
    title = ' '.join(out)
    title = title.replace('Ai To Ai', 'AI-to-AI')
    title = title.replace('A2A', 'A2A')
    title = title.replace('Vector Db', 'Vector DB')
    title = title.replace('Voice IA', 'Voice AI')
    title = title.replace('Prompt Engineering', 'Prompt Engineering')
    return title


def apostila_by_slug(slug: str):
    exact = APOSTILAS / f'{slug}.md'
    if exact.exists():
        return exact
    matches = sorted(APOSTILAS.glob(f'*-{slug}.md'))
    if matches:
        return matches[0]
    slug_tokens = set(tokens(slug))
    best = None
    best_score = -1
    for md in sorted(APOSTILAS.glob('*.md')):
        md_slug = md.stem.split('-', 1)[1] if '-' in md.stem else md.stem
        score = len(slug_tokens.intersection(set(tokens(md_slug))))
        if score > best_score:
            best = md
            best_score = score
    return best


def choose_source_for_cover(filename: str):
    stem = Path(filename).stem
    slug = None
    if stem.startswith('ACAD-apostila-'):
        m = re.match(r'ACAD-apostila-\d+-(.+)', stem)
        slug = m.group(1) if m else None
    elif stem.startswith('WB-2026-'):
        slug = stem.split('-', 3)[-1]
    elif 'ebook-01-' in stem:
        slug = stem.split('ebook-01-', 1)[-1]

    if slug:
        for key, src_name in SLUG_SOURCE_OVERRIDES.items():
            if key == slug and (THUMBS / src_name).exists():
                return THUMBS / src_name
        for key, src_name in SLUG_SOURCE_OVERRIDES.items():
            if key in slug and (THUMBS / src_name).exists():
                return THUMBS / src_name
        want = set(tokens(slug))
        best = None
        best_score = -1
        for c in sorted(THUMBS.glob('capa-*.png')):
            score = len(want.intersection(set(tokens(c.stem))))
            if score > best_score:
                best = c
                best_score = score
        if best:
            return best
    fallback = THUMBS / 'capa-21-master-arquitetura-dupla.png'
    return fallback if fallback.exists() else sorted(THUMBS.glob('capa-*.png'))[0]


def choose_theme(src_name: str):
    s = src_name.lower()
    if 'ive' in s and 'dupla' not in s:
        return 'IVE'
    if 'alencar' in s and 'dupla' not in s:
        return 'ALENCAR'
    return 'IVE + ALENCAR'


def clean_title(t: str) -> str:
    t = re.sub(r'^🎤\s*', '', t, flags=re.I)
    t = re.sub(r'^WB-\d{4}-\d+\s*[·:\-]\s*', '', t, flags=re.I)
    t = re.sub(r'^Apostila\s*\d+\s*[·:\-]\s*', '', t, flags=re.I)
    t = t.replace(' Ia ', ' IA ')
    t = t.replace(' Rag ', ' RAG ')
    t = t.replace(' Ioaid ', ' IOAID ')
    t = t.replace(' Sho ', ' SHO ')
    t = t.replace(' Ai ', ' AI ')
    t = t.replace('IA To IA', 'IA-to-IA')
    t = t.replace('Ai To Ai', 'AI-to-AI')
    t = t.replace(' Db', ' DB')
    t = t.replace('Langgraph', 'LangGraph')
    t = t.replace('Whitelabel', 'White-label')
    return ' '.join(t.split())


def fit_title(draw, text, max_width, max_lines=5, start=82, min_size=32):
    text = text.replace('—', ' — ').replace('·', ' · ')
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


def render_cover(dst: Path, title: str, subtitle: str, src: Path, category='APOSTILA', issue='NEXUS AFFIL\'IA\'TE'):
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
    theme = choose_theme(src.name)
    d.text((125, 1368), f'VISUAL · {theme}', font=micro, fill=(166, 198, 214))
    d.text((125, 1410), issue, font=micro, fill=(166, 198, 214))
    frame.convert('RGB').save(dst, format='WEBP', quality=96, method=6)
    print('rebuilt', dst.relative_to(ROOT), 'from', src.name, 'title=', title)


def derive_title_and_subtitle(file: Path):
    stem = file.stem
    if stem.startswith('ACAD-apostila-'):
        m = re.match(r'ACAD-apostila-\d+-(.+)', stem)
        slug = m.group(1) if m else stem
        if slug in SLUG_TITLE_OVERRIDES:
            return SLUG_TITLE_OVERRIDES[slug]
        md = apostila_by_slug(slug)
        if md:
            title, subtitle = read_frontmatter_title_subtitle(md)
            title = clean_title(title or prettify_slug(slug))
            subtitle = subtitle or 'Coleção oficial Academ\'IA'
            return title, subtitle
        return prettify_slug(slug), 'Coleção oficial Academ\'IA'
    if stem.startswith('WB-2026-'):
        slug = stem.split('-', 3)[-1]
        if slug in SLUG_TITLE_OVERRIDES:
            return SLUG_TITLE_OVERRIDES[slug]
        md = WEBINARS / f'{stem}.md'
        title, subtitle = read_frontmatter_title_subtitle(md)
        if title:
            return clean_title(title), subtitle or 'Webinar oficial da Academ\'IA'
        return prettify_slug(slug), 'Webinar oficial da Academ\'IA'
    if 'ebook-01-' in stem:
        slug = stem.split('ebook-01-', 1)[-1]
        if slug in SLUG_TITLE_OVERRIDES:
            return SLUG_TITLE_OVERRIDES[slug]
        return prettify_slug(slug), 'Coleção oficial Academ\'IA'
    return stem.replace('-', ' ').title(), 'Nexus Affil\'IA\'te'


def category_for(file: Path):
    if file.name.startswith('WB-2026-'):
        return 'WEBINAR'
    if file.name.startswith('curso-universo-ia'):
        return 'EBOOK'
    return 'APOSTILA'


def main():
    files = sorted(DOCS.glob('*.webp'))
    for f in files:
        title, subtitle = derive_title_and_subtitle(f)
        src = choose_source_for_cover(f.name)
        render_cover(f, title, subtitle, src, category_for(f))


if __name__ == '__main__':
    main()

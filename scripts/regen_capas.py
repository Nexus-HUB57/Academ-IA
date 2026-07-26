#!/usr/bin/env python3
"""
Gera capas profissionais para AcademIA.
- 1200x1600px (alta resolução)
- Gradientes radiais com 3 cores
- Tipografia serif elegante
- Icones geometricos tematicos
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math
import random

OUT_DIR = "/workspace/Academ-IA/docs/ebooks"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_SERIF = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
FONT_SANS = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
FONT_SANS_LIGHT = f"{FONT_DIR}/DejaVuSans.ttf"

W, H = 1200, 1600

THEMES = {
    "infra": ((0x0a, 0x1a, 0x3a), (0x2a, 0x4a, 0x7a), (0x4a, 0x6a, 0x9a)),
    "cases": ((0x2a, 0x1a, 0x3a), (0x5a, 0x3a, 0x7a), (0x8a, 0x5a, 0x9a)),
    "operacional": ((0x0a, 0x2a, 0x1a), (0x2a, 0x5a, 0x3a), (0x5a, 0x8a, 0x4a)),
    "hibrida": ((0x3a, 0x1a, 0x1a), (0x7a, 0x3a, 0x2a), (0x9a, 0x5a, 0x4a)),
    "telas": ((0x1a, 0x2a, 0x3a), (0x3a, 0x5a, 0x7a), (0x6a, 0x8a, 0x9a)),
    "agente": ((0x2a, 0x0a, 0x3a), (0x5a, 0x2a, 0x7a), (0x8a, 0x4a, 0x9a)),
    "skills": ((0x3a, 0x2a, 0x1a), (0x7a, 0x5a, 0x3a), (0x9a, 0x7a, 0x5a)),
    "rotina": ((0x1a, 0x3a, 0x2a), (0x3a, 0x7a, 0x5a), (0x5a, 0x9a, 0x7a)),
    "campanhas": ((0x3a, 0x1a, 0x2a), (0x7a, 0x3a, 0x5a), (0x9a, 0x5a, 0x7a)),
    "jornada": ((0x0a, 0x1a, 0x2a), (0x2a, 0x4a, 0x6a), (0x4a, 0x6a, 0x8a)),
    "seo": ((0x2a, 0x3a, 0x1a), (0x5a, 0x7a, 0x3a), (0x8a, 0x9a, 0x5a)),
    "sho": ((0x3a, 0x2a, 0x0a), (0x7a, 0x5a, 0x2a), (0x9a, 0x7a, 0x4a)),
    "arquitetura": ((0x0a, 0x0a, 0x2a), (0x2a, 0x2a, 0x5a), (0x4a, 0x4a, 0x8a)),
    "seguranca": ((0x2a, 0x0a, 0x0a), (0x5a, 0x2a, 0x2a), (0x8a, 0x4a, 0x4a)),
    "marketplace": ((0x1a, 0x2a, 0x0a), (0x3a, 0x5a, 0x2a), (0x5a, 0x8a, 0x4a)),
    "multi": ((0x0a, 0x2a, 0x2a), (0x2a, 0x5a, 0x5a), (0x4a, 0x8a, 0x8a)),
    "metricas": ((0x1a, 0x1a, 0x3a), (0x3a, 0x3a, 0x7a), (0x5a, 0x5a, 0x9a)),
    "fundamental": ((0x2a, 0x1a, 0x2a), (0x5a, 0x3a, 0x5a), (0x8a, 0x5a, 0x8a)),
    "monetizacao": ((0x2a, 0x2a, 0x0a), (0x5a, 0x5a, 0x2a), (0x8a, 0x8a, 0x4a)),
    "elite": ((0x0a, 0x0a, 0x1a), (0x2a, 0x2a, 0x4a), (0x4a, 0x4a, 0x6a)),
    "master": ((0x1a, 0x0a, 0x1a), (0x4a, 0x2a, 0x4a), (0x6a, 0x4a, 0x6a)),
    "rag": ((0x0a, 0x1a, 0x1a), (0x2a, 0x4a, 0x4a), (0x4a, 0x6a, 0x6a)),
    "agents": ((0x2a, 0x0a, 0x2a), (0x5a, 0x2a, 0x5a), (0x8a, 0x4a, 0x8a)),
    "prompt": ((0x3a, 0x2a, 0x1a), (0x7a, 0x5a, 0x3a), (0x9a, 0x7a, 0x5a)),
    "vector": ((0x0a, 0x2a, 0x1a), (0x2a, 0x5a, 0x3a), (0x4a, 0x8a, 0x5a)),
    "voice": ((0x3a, 0x0a, 0x1a), (0x7a, 0x2a, 0x3a), (0x9a, 0x4a, 0x5a)),
    "multimodal": ((0x1a, 0x0a, 0x3a), (0x4a, 0x2a, 0x7a), (0x6a, 0x4a, 0x9a)),
    "ai-to-ai": ((0x0a, 0x3a, 0x0a), (0x2a, 0x7a, 0x2a), (0x4a, 0x9a, 0x4a)),
    "federacao": ((0x0a, 0x1a, 0x3a), (0x2a, 0x3a, 0x7a), (0x4a, 0x5a, 0x9a)),
    "fabrica": ((0x3a, 0x1a, 0x0a), (0x7a, 0x3a, 0x2a), (0x9a, 0x5a, 0x4a)),
    "pricing": ((0x2a, 0x3a, 0x0a), (0x5a, 0x7a, 0x2a), (0x8a, 0x9a, 0x4a)),
    "data-stack": ((0x0a, 0x3a, 0x2a), (0x2a, 0x7a, 0x5a), (0x4a, 0x9a, 0x7a)),
    "deploy": ((0x1a, 0x3a, 0x0a), (0x3a, 0x7a, 0x2a), (0x5a, 0x9a, 0x4a)),
    "marketing": ((0x3a, 0x0a, 0x2a), (0x7a, 0x2a, 0x5a), (0x9a, 0x4a, 0x7a)),
    "comunidade": ((0x0a, 0x2a, 0x3a), (0x2a, 0x5a, 0x7a), (0x4a, 0x8a, 0x9a)),
    "lancamento": ((0x3a, 0x2a, 0x0a), (0x7a, 0x5a, 0x2a), (0x9a, 0x7a, 0x4a)),
    "academia": ((0x1a, 0x1a, 0x2a), (0x3a, 0x3a, 0x5a), (0x5a, 0x5a, 0x7a)),
    "open-house": ((0x2a, 0x1a, 0x1a), (0x5a, 0x3a, 0x3a), (0x8a, 0x5a, 0x5a)),
    "ab-test": ((0x0a, 0x2a, 0x1a), (0x2a, 0x5a, 0x3a), (0x4a, 0x8a, 0x5a)),
    "lgpd": ((0x2a, 0x0a, 0x1a), (0x5a, 0x2a, 0x3a), (0x8a, 0x4a, 0x5a)),
    "financeiro": ((0x0a, 0x1a, 0x0a), (0x2a, 0x4a, 0x2a), (0x4a, 0x6a, 0x4a)),
    "agentes-auto": ((0x1a, 0x0a, 0x2a), (0x3a, 0x2a, 0x5a), (0x5a, 0x4a, 0x8a)),
    "burnout": ((0x2a, 0x1a, 0x0a), (0x5a, 0x3a, 0x2a), (0x8a, 0x5a, 0x4a)),
    "criacao": ((0x3a, 0x0a, 0x0a), (0x7a, 0x2a, 0x2a), (0x9a, 0x4a, 0x4a)),
    "conversa": ((0x3a, 0x1a, 0x2a), (0x7a, 0x5a, 0x4a), (0x9a, 0x7a, 0x6a)),
    "tribo": ((0x0a, 0x2a, 0x2a), (0x3a, 0x6a, 0x6a), (0x5a, 0x8a, 0x8a)),
}


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_radial_gradient(w, h, c1, c2, c3, center=None):
    if center is None:
        center = (w * 0.35, h * 0.4)
    cx, cy = center
    # usar numpy via math apenas em pontos amostrados, depois redimensionar
    img = Image.new("RGB", (w, h), c1)
    # 1. desenhar em resolucao reduzida 8x
    sw, sh = w // 8, h // 8
    small = Image.new("RGB", (sw, sh), c1)
    sp = small.load()
    max_d = math.hypot(max(cx, w - cx), max(cy, h - cy))
    for y in range(sh):
        for x in range(sw):
            d = math.hypot(x * 8 - cx, y * 8 - cy) / max_d
            d = min(1.0, d)
            if d < 0.5:
                color = lerp(c1, c2, d * 2)
            else:
                color = lerp(c2, c3, (d - 0.5) * 2)
            sp[x, y] = color
    return small.resize((w, h), Image.LANCZOS).convert("RGB")


def add_geometry_pattern(img, theme_color):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    accent = theme_color
    random.seed(42)
    for _ in range(8):
        x = random.randint(0, W)
        y = random.randint(0, H)
        size = random.randint(80, 250)
        alpha = random.randint(8, 25)
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.append((px, py))
        draw.polygon(points, outline=(*accent, alpha), width=2)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def add_corner_branding(img):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.line([(60, 50), (W - 60, 50)], fill=(255, 255, 255, 60), width=1)
    font_label = ImageFont.truetype(FONT_SANS_LIGHT, 18)
    draw.text((60, 65), "ACADEM'IA · NEXUS AFFIL'IA'TE", font=font_label, fill=(255, 255, 255, 180))
    font_badge = ImageFont.truetype(FONT_SANS, 14)
    badge_text = "ONDA 44"
    bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    tw = bbox[2] - bbox[0]
    draw.rectangle([(W - 60 - tw - 20, 60), (W - 60, 95)], outline=(255, 255, 255, 120), width=1)
    draw.text((W - 60 - tw - 10, 70), badge_text, font=font_badge, fill=(255, 255, 255, 200))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def add_title_block(img, number, title, subtitle, theme_color):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    accent = theme_color
    font_hero = ImageFont.truetype(FONT_SERIF, 480)
    num_text = f"{number:02d}"
    bbox = draw.textbbox((0, 0), num_text, font=font_hero)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    nx = 100
    ny = H // 2 - th - 40
    draw.text((nx + 6, ny + 6), num_text, font=font_hero, fill=(0, 0, 0, 80))
    draw.text((nx, ny), num_text, font=font_hero, fill=(*accent, 200))
    sep_x = nx + tw + 40
    draw.line([(sep_x, ny + 60), (sep_x, ny + th - 60)], fill=(255, 255, 255, 200), width=3)
    font_title = ImageFont.truetype(FONT_SERIF, 56)
    font_sub = ImageFont.truetype(FONT_SANS_LIGHT, 24)
    tx = sep_x + 30
    ty = ny + 60
    words = title.upper().split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        bbox_t = draw.textbbox((0, 0), test, font=font_title)
        if bbox_t[2] - bbox_t[0] > W - tx - 80:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)
    for i, line in enumerate(lines[:4]):
        draw.text((tx + 2, ty + 2 + i * 64), line, font=font_title, fill=(0, 0, 0, 100))
        draw.text((tx, ty + i * 64), line, font=font_title, fill=(255, 255, 255, 245))
    sy = ty + len(lines) * 64 + 30
    if subtitle:
        draw.text((tx, sy), subtitle.upper(), font=font_sub, fill=(*accent, 220))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def add_footer(img, footer_text="Academ'IA · Dupla Nexus Ive + Sir. Alencar · 2026"):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font_footer = ImageFont.truetype(FONT_SANS_LIGHT, 20)
    font_mini = ImageFont.truetype(FONT_SANS_LIGHT, 14)
    draw.line([(60, H - 110), (W - 60, H - 110)], fill=(255, 255, 255, 80), width=1)
    draw.text((60, H - 90), footer_text, font=font_footer, fill=(255, 255, 255, 200))
    draw.text((W - 60 - 200, H - 50), "MMN_IA · v1.4.0", font=font_mini, fill=(255, 255, 255, 140))
    draw.text((60, H - 50), "Licenca: CC BY-SA 4.0", font=font_mini, fill=(255, 255, 255, 140))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def add_accent_icon(img, theme_color, icon_type="circle"):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    accent = theme_color
    cx, cy = W - 130, 180
    size = 70
    if icon_type == "circle":
        for r in [size, size - 15, size - 30]:
            alpha = 220 - (size - r) * 4
            draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=(*accent, alpha), width=2)
    elif icon_type == "hex":
        points = []
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 2
            px = cx + size * math.cos(angle)
            py = cy + size * math.sin(angle)
            points.append((px, py))
        draw.polygon(points, outline=(*accent, 220), width=3)
    elif icon_type == "triangle":
        points = [(cx, cy - size), (cx - size * 0.866, cy + size * 0.5), (cx + size * 0.866, cy + size * 0.5)]
        draw.polygon(points, outline=(*accent, 220), width=3)
    elif icon_type == "square":
        draw.rectangle([(cx - size * 0.7, cy - size * 0.7), (cx + size * 0.7, cy + size * 0.7)], outline=(*accent, 220), width=3)
    elif icon_type == "star":
        points = []
        for i in range(10):
            angle = math.pi / 5 * i - math.pi / 2
            r = size if i % 2 == 0 else size * 0.4
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            points.append((px, py))
        draw.polygon(points, outline=(*accent, 220), width=3)
    elif icon_type == "wave":
        points = []
        for x in range(cx - size, cx + size, 5):
            y = cy + 15 * math.sin((x - cx + size) / size * math.pi * 2)
            points.append((x, y))
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=(*accent, 220), width=3)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def make_cover(theme, number, title, subtitle="", icon="circle", footer="Academ'IA · Dupla Nexus · 2026"):
    c1, c2, c3 = THEMES[theme]
    img = make_radial_gradient(W, H, c1, c2, c3)
    img = add_geometry_pattern(img, c3)
    img = add_corner_branding(img)
    img = add_accent_icon(img, c3, icon_type=icon)
    img = add_title_block(img, number, title, subtitle, c3)
    img = add_footer(img, footer)
    return img


CAPAS = [
    ("ACAD-apostila-01-apresentacao-infraestrutura.webp", "infra", 1, "Apresentacao", "Infraestrutura", "circle", "Apresenta o Ecossistema"),
    ("ACAD-apostila-02-cases-orquestracao-autonoma.webp", "cases", 2, "Cases", "Orquestracao Autonoma", "triangle", "Cases Reais em Producao"),
    ("ACAD-apostila-03-infra-operacional-ia.webp", "operacional", 3, "Operacional", "Infraestrutura IA", "hex", "Operacao de IA em Escala"),
    ("ACAD-apostila-04-orquestracao-hibrida-agentes.webp", "hibrida", 4, "Hibrida", "Orquestracao de Agentes", "circle", "Sistemas Hibridos"),
    ("ACAD-apostila-05-sete-telas-essenciais.webp", "telas", 5, "Sete Telas", "Paineis Essenciais", "square", "As 7 Telas Criticas"),
    ("ACAD-apostila-06-setup-agente-pessoal.webp", "agente", 6, "Agente", "Setup do Agente", "circle", "Configure Seu Agente"),
    ("ACAD-apostila-07-18-skills-operacionais.webp", "skills", 7, "Skills", "18 Skills Operacionais", "hex", "Kit Completo de Skills"),
    ("ACAD-apostila-08-rotina-disparo-agente.webp", "rotina", 8, "Rotina", "Rotina de Disparo", "wave", "Rotina Diaria"),
    ("ACAD-apostila-09-campanhas-automatizadas.webp", "campanhas", 9, "Campanhas", "Campanhas Automaticas", "triangle", "Marketing Automatico"),
    ("ACAD-apostila-10-jornada-completa-afiliado.webp", "jornada", 10, "Jornada", "Jornada do Afiliado", "circle", "Do Zero ao Avancado"),
    ("ACAD-apostila-11-seo-marketing-conteudo-ia.webp", "seo", 11, "SEO", "Marketing de Conteudo", "star", "SEO com IA"),
    ("ACAD-apostila-11-sho-em-producao.webp", "sho", 11, "SHO", "Sistema SHO em Producao", "hex", "Operacao SHO"),
    ("ACAD-apostila-12-ioaid-arquitetura-profunda.webp", "arquitetura", 12, "Arquitetura", "IOAID em Profundidade", "circle", "Arq. Profunda"),
    ("ACAD-apostila-12-seguranca-ofensiva-pentest-agentes-ia.webp", "seguranca", 12, "Seguranca", "Pentest de Agentes IA", "triangle", "Seguranca Ofensiva"),
    ("ACAD-apostila-13-marketplace-skills.webp", "marketplace", 13, "Marketplace", "Marketplace de Skills", "square", "Ecossistema Aberto"),
    ("ACAD-apostila-14-multi-tenant-whitelabel.webp", "multi", 14, "Multi-Tenant", "White-Label SaaS", "circle", "Operacao White-Label"),
    ("ACAD-apostila-15-metricas-roi-ecossistema.webp", "metricas", 15, "ROI", "Metricas e ROI", "wave", "KPIs do Ecossistema"),
    ("ACAD-apostila-16-trilha-fundamental-ia.webp", "fundamental", 16, "Fundamental", "Trilha Fundamental IA", "star", "Trilha Inicial"),
    ("ACAD-apostila-17-seo-marketing-conteudo-ia.webp", "seo", 17, "Conteudo", "SEO & Marketing de Conteudo", "wave", "Marketing Organico"),
    ("ACAD-apostila-18-seguranca-ofensiva-pentest-agentes-ia.webp", "seguranca", 18, "Pentest", "Seguranca Ofensiva", "triangle", "Ataques & Defesas"),
    ("ACAD-apostila-19-monetizacao-avancada-escala.webp", "monetizacao", 19, "Monetizacao", "Escala Avancada", "circle", "Receita em Escala"),
    ("ACAD-apostila-20-trilha-elite-engenharia.webp", "elite", 20, "Elite", "Engenharia de Elite", "hex", "Nivel Elite"),
    ("ACAD-apostila-21-trilha-master-arquitetura.webp", "master", 21, "Master", "Arquitetura Master", "square", "Nivel Master"),
    ("ACAD-apostila-22-trilha-master-mentoria.webp", "master", 22, "Mentoria", "Master em Mentoria", "star", "Mentor Master"),
    ("ACAD-apostila-23-curso-rag-pratico.webp", "rag", 23, "RAG", "Curso RAG Pratico", "wave", "RAG Hands-On"),
    ("ACAD-apostila-24-curso-agents-langgraph.webp", "agents", 24, "LangGraph", "Agentes com LangGraph", "circle", "Curso Pratico"),
    ("ACAD-apostila-25-curso-prompt-engineering.webp", "prompt", 25, "Prompts", "Engenharia de Prompts", "hex", "Curso de Prompts"),
    ("ACAD-apostila-26-curso-vector-db.webp", "vector", 26, "Vetores", "Bancos Vetoriais", "triangle", "Vector DBs"),
    ("ACAD-apostila-27-curso-voice-ai.webp", "voice", 27, "Voice", "Voice AI", "wave", "IA de Voz"),
    ("ACAD-apostila-28-curso-multimodal-rag.webp", "multimodal", 28, "Multimodal", "RAG Multimodal", "star", "Visao + Texto"),
    ("ACAD-apostila-29-ai-to-ai-protocol.webp", "ai-to-ai", 29, "AI-to-AI", "Protocolo A2A", "circle", "A2A Protocol"),
    ("ACAD-apostila-30-federacao-zero-trust.webp", "federacao", 30, "Federacao", "Zero-Trust Federation", "hex", "Federacao Segura"),
    ("ACAD-apostila-31-fabrica-conteudo-ia.webp", "fabrica", 31, "Fabrica", "Fabrica de Conteudo", "square", "Producao em Massa"),
    ("ACAD-apostila-32-pricing-ia-2026.webp", "pricing", 32, "Pricing", "Pricing IA 2026", "wave", "Precificacao Dinamica"),
    ("ACAD-apostila-33-data-stack-agentes-ia.webp", "data-stack", 33, "Data", "Data Stack de Agentes", "triangle", "Pipelines de Dados"),
    ("ACAD-apostila-34-deploy-continuo-agentes-ia.webp", "deploy", 34, "Deploy", "Deploy Continuo", "circle", "CI/CD de Agentes"),
    ("ACAD-apostila-35-marketing-conversacional-ia.webp", "marketing", 35, "Conversacional", "Marketing Conversacional", "wave", "Conversa Vende"),
    ("ACAD-apostila-36-comunidade-engajamento-ia.webp", "comunidade", 36, "Comunidade", "Engajamento com IA", "star", "Tribo de 10k"),
    ("WB-2026-01-lancamento-ioaid.webp", "lancamento", 1, "Lancamento", "IOAID", "star", "Live de Lancamento"),
    ("WB-2026-02-sho-em-producao.webp", "sho", 2, "SHO", "SHO em Producao", "circle", "Operacao Real"),
    ("WB-2026-03-academia-open-house.webp", "academia", 3, "Open House", "AcademIA", "hex", "Open House 2026"),
    ("WB-2026-04-ia-to-ia-federation.webp", "federacao", 4, "Federacao", "A2A Federation", "triangle", "Protocolo Federado"),
    ("WB-2026-04-skills-em-producao.webp", "skills", 4, "Skills", "Skills em Producao", "hex", "Skills Live"),
    ("WB-2026-05-multi-tenant.webp", "multi", 5, "Multi-Tenant", "White-Label", "square", "SaaS Multi-Tenant"),
    ("WB-2026-06-ab-test-estatistico.webp", "ab-test", 6, "A/B", "Testes Estatisticos", "wave", "A/B com Significancia"),
    ("WB-2026-07-lgpd-ia.webp", "lgpd", 7, "LGPD", "Compliance & IA", "circle", "LGPD na Pratica"),
    ("WB-2026-08-financeiro-ia.webp", "financeiro", 8, "Financeiro", "IA para Financas", "triangle", "Financas com IA"),
    ("WB-2026-09-agentes-autonomos-prod.webp", "agentes-auto", 9, "Autonomos", "Agentes em Producao", "hex", "Agentes Autonomos"),
    ("WB-2026-10-seo-vs-ia-generativa.webp", "seo", 10, "SEO vs IA", "Organico x Generativo", "wave", "SEO em 2026"),
    ("WB-2026-11-burnout-afiliados.webp", "burnout", 11, "Burnout", "Saude do Afiliado", "circle", "Evite Burnout"),
    ("WB-2026-12-ia-to-ia-federation.webp", "federacao", 12, "A2A", "A2A Federation", "star", "Protocolo A2A"),
    ("WB-2026-13-criacao-conteudo-ia.webp", "criacao", 13, "Criacao", "Conteudo com IA", "wave", "Fabrica de Conteudo"),
    ("WB-2026-14-pricing-ia-tempo-real.webp", "pricing", 14, "Pricing", "IA Tempo-Real", "triangle", "Precificacao Real-Time"),
    ("WB-2026-15-data-stack-ia.webp", "data-stack", 15, "Data Stack", "IA + Data", "hex", "Pipelines Modernos"),
    ("WB-2026-16-deploy-continuo-ia.webp", "deploy", 16, "Deploy", "Deploy Continuo", "square", "CI/CD de Agentes"),
    ("WB-2026-17-conversa-vende-ia.webp", "conversa", 17, "Conversa Vende", "Marketing Conversacional", "wave", "Venda por Mensagem"),
    ("WB-2026-18-comunidade-tribo-ia.webp", "tribo", 18, "Tribo 10k", "Comunidade & Engajamento", "star", "Tribo com IA"),
]


def main():
    print(f"Gerando {len(CAPAS)} capas profissionais em {W}x{H}...")
    ok, fail = 0, 0
    for filename, theme, num, title, subtitle, icon, footer in CAPAS:
        try:
            path = os.path.join(OUT_DIR, filename)
            img = make_cover(theme, num, title, subtitle, icon, footer)
            img.save(path, "WEBP", quality=92, method=6)
            size_kb = os.path.getsize(path) / 1024
            print(f"  OK {filename}: {size_kb:.1f}KB")
            ok += 1
        except Exception as e:
            print(f"  ERRO {filename}: {e}")
            fail += 1
    print(f"\nConcluido: {ok} OK, {fail} falhas")


if __name__ == "__main__":
    main()

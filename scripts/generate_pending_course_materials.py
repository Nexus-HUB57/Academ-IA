from __future__ import annotations

from pathlib import Path
import re
import subprocess
import textwrap
from typing import List, Tuple

ROOT = Path('/home/user/repo/Academ-IA').resolve()
CURSOS = ROOT / 'cursos'
HTML_ROOT = ROOT / 'html' / 'cursos'
PDF_ROOT = ROOT / 'pdfs'
CSS_PATH = ROOT / 'html' / 'acad-style.css'
REPORT = ROOT / 'docs' / 'MATERIAIS_PENDENTES_GERADOS_2026-07-24.md'

TRACK_META = {
    'fundamental': {
        'label': 'Fundamental',
        'prefix': 'Fundamental',
        'module_prefix': 'fund',
        'palette': ('#63eaff', '#2dd4bf', '#facc15', '#0a0e1a'),
        'personas': 'Sra. Nexus Ive',
    },
    'agente': {
        'label': 'Agente',
        'prefix': 'Agente',
        'module_prefix': 'agent',
        'palette': ('#63eaff', '#b78cff', '#ff7eb6', '#0a0e1a'),
        'personas': 'Sra. Nexus Ive e Sir. Nexus Alencar',
    },
    'elite': {
        'label': 'Elite',
        'prefix': 'Elite',
        'module_prefix': 'elite',
        'palette': ('#facc15', '#b78cff', '#ff7eb6', '#0a0e1a'),
        'personas': 'Sra. Nexus Ive e Sir. Nexus Alencar',
    },
    'master': {
        'label': 'Master',
        'prefix': 'Master',
        'module_prefix': 'master',
        'palette': ('#b78cff', '#63eaff', '#facc15', '#0a0e1a'),
        'personas': 'Sra. Nexus Ive e Sir. Nexus Alencar',
    },
}

STOP_LINES = {
    '## próximos passos', '## recursos', '## checklist de produção', '## checklist de segurança'
}


def slug_to_title(slug: str) -> str:
    mapping = {
        'ia': 'IA', 'ml': 'ML', 'rag': 'RAG', 'seo': 'SEO', 'roi': 'ROI', 'db': 'DB',
        'ioaid': 'IOAID', 'sho': 'SHO', 'lgpd': 'LGPD', 'eu': 'EU', 'ab': 'A/B',
        'api': 'API', 'mfa': 'MFA', 'hitl': 'HITL', 'slos': 'SLOs', 'sre': 'SRE',
        'whitelabel': 'White-label', 'langgraph': 'LangGraph', 'jailbreaks': 'Jailbreaks',
    }
    parts = slug.split('-')
    out = []
    for p in parts:
        if p in mapping:
            out.append(mapping[p])
        else:
            out.append(p.capitalize())
    title = ' '.join(out)
    title = title.replace('A/B Test', 'A/B Test')
    title = title.replace('Ai To Ai', 'AI-to-AI')
    title = title.replace('Multitenant', 'Multi-tenant')
    return title


def parse_frontmatter_and_body(text: str) -> Tuple[dict, str]:
    meta = {}
    body = text
    if text.startswith('---\n'):
        parts = text.split('\n---\n', 1)
        if len(parts) == 2:
            fm, body = parts
            for line in fm.splitlines()[1:]:
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip()] = v.strip().strip('"')
    return meta, body


def parse_sections(body: str) -> List[Tuple[str, List[str]]]:
    lines = body.splitlines()
    title = None
    sections: List[Tuple[str, List[str]]] = []
    current_h2 = None
    current_lines: List[str] = []
    in_code = False
    for raw in lines:
        line = raw.rstrip()
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith('# ') and not title:
            title = line[2:].strip()
            continue
        if line.startswith('## '):
            if current_h2:
                sections.append((current_h2, current_lines))
            current_h2 = line[3:].strip()
            current_lines = []
            continue
        if current_h2:
            current_lines.append(line)
    if current_h2:
        sections.append((current_h2, current_lines))
    return sections


def clean_heading(h: str) -> str:
    return re.sub(r'^[^A-Za-zÀ-ÿ0-9]+\s*', '', h).strip()


def summarize_lines(lines: List[str], limit: int = 5) -> List[str]:
    bullets = []
    paragraph = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith(('- ', '* ')):
            bullets.append(s[2:].strip())
        elif re.match(r'^\d+\.\s+', s):
            bullets.append(re.sub(r'^\d+\.\s+', '', s))
        elif s.startswith('> '):
            bullets.append(s[2:].strip())
        elif not s.startswith('|'):
            paragraph.append(s)
    merged = bullets[:]
    if paragraph:
        joined = ' '.join(paragraph)
        joined = re.sub(r'\s+', ' ', joined)
        sentences = re.split(r'(?<=[.!?])\s+', joined)
        for sent in sentences:
            sent = sent.strip()
            if sent:
                merged.append(sent)
    out = []
    for item in merged:
        item = re.sub(r'`([^`]+)`', r'\1', item)
        item = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', item)
        item = re.sub(r'\*\*(.*?)\*\*', r'\1', item)
        item = re.sub(r'\s+', ' ', item).strip(' -')
        if item and item not in out:
            out.append(item)
        if len(out) >= limit:
            break
    return out


def get_title(md: Path, meta: dict, body: str) -> str:
    if 'title' in meta and meta['title']:
        t = meta['title']
        t = re.sub(r'^\d+\s*[·\-]\s*', '', t).strip()
        return t
    for line in body.splitlines():
        if line.startswith('# '):
            return re.sub(r'^[#\s🔍🚀🛡️📊🎓]+', '', line).strip()
    return slug_to_title(md.stem)


def get_duration_minutes(meta: dict) -> int:
    val = meta.get('duration', '').strip().lower()
    m = re.search(r'(\d+)', val)
    return int(m.group(1)) if m else 45


def get_prereq(meta: dict) -> str:
    raw = meta.get('prerequisites', '').strip()
    return raw if raw else 'Sem pré-requisito formal'


def slide_file_path(md: Path) -> Path:
    return md.with_name(md.stem + '-slides.md')


def roteiro_file_path(md: Path) -> Path:
    return md.with_name(md.stem + '-roteiro.md')


def html_file_path(md: Path, track: str) -> Path:
    return HTML_ROOT / track / f'{md.stem}.html'


def pdf_file_path(md: Path, track: str) -> Path:
    return PDF_ROOT / f'curso-{track}-{md.stem}.pdf'


def extract_mod_num(stem: str) -> int:
    m = re.match(r'(\d+)', stem)
    return int(m.group(1)) if m else 0


def create_slides(md: Path, track: str, title: str, meta: dict, sections: List[Tuple[str, List[str]]]) -> str:
    tm = TRACK_META[track]
    mod_num = extract_mod_num(md.stem)
    modulo = f"{tm['module_prefix']}-{mod_num:02d}"
    pri, sec, acc, bg = tm['palette']
    curated = []
    for heading, lines in sections:
        h = clean_heading(heading)
        if not h:
            continue
        if f'## {h.lower()}' in STOP_LINES:
            continue
        bullets = summarize_lines(lines, limit=4)
        if bullets:
            curated.append((h, bullets))
    curated = curated[:6]
    total_slides = len(curated) + 3
    lines = [
        '---',
        f'title: "Módulo {tm["prefix"]}-{mod_num:02d} · Slides · {title}"',
        f'description: "Slides visuais para acompanhar o módulo {mod_num:02d} da Trilha {tm["label"]}"',
        f'tags: [slides, {track}, modulo-{mod_num:02d}]',
        f'modulo: {modulo}',
        f'trilha: {tm["label"]}',
        f'ordem: {mod_num}',
        f'total_slides: {total_slides}',
        'pattern: "MMN_IA"',
        '---',
        '',
        f'# 📊 Slides · {tm["label"]} {mod_num:02d} · {title}',
        '',
        '> Material visual de apoio para acompanhar o vídeo e a leitura do módulo.',
        '',
        '## 🎨 Paleta de Cores',
        '',
        '```',
        f'Primary:    {pri}',
        f'Secondary:  {sec}',
        f'Accent:     {acc}',
        f'Background: {bg}',
        '```',
        '',
        '---',
        '',
        '## 📍 SLIDE 01 — Abertura',
        '',
        f'**Título:** {title}',
        f'**Subtítulo:** Trilha {tm["label"]} · Módulo {mod_num:02d}',
        f'**Persona-guia:** {tm["personas"]}',
        '',
        '---',
        '',
        '## 📍 SLIDE 02 — Objetivo do módulo',
        '',
        f'**Título:** O que você vai dominar neste módulo',
    ]
    if sections:
        first_bullets = summarize_lines(sections[0][1], limit=4)
        for b in first_bullets:
            lines.append(f'- {b}')
    else:
        lines.extend(['- Conceitos centrais do módulo', '- Aplicação prática no ecossistema Nexus'])
    lines.extend(['', '---', ''])
    idx = 3
    for heading, bullets in curated:
        lines.append(f'## 📍 SLIDE {idx:02d} — {heading}')
        lines.append('')
        lines.append(f'**Título:** {heading}')
        for b in bullets:
            lines.append(f'- {b}')
        lines.extend(['', '---', ''])
        idx += 1
    lines.append(f'## 📍 SLIDE {idx:02d} — Checklist e próximos passos')
    lines.append('')
    lines.append('**Título:** O que precisa sair pronto daqui')
    lines.append('- Revisar os conceitos centrais apresentados neste módulo')
    lines.append('- Transformar os exemplos em configuração real no ecossistema Nexus')
    lines.append(f'- Pré-requisito relacionado: {get_prereq(meta)}')
    lines.append('- Seguir para o próximo módulo com base documentada e operacional')
    lines.append('')
    return '\n'.join(lines) + '\n'


def create_roteiro(md: Path, track: str, title: str, meta: dict, sections: List[Tuple[str, List[str]]]) -> str:
    personas = TRACK_META[track]['personas']
    duration = get_duration_minutes(meta)
    prereq = get_prereq(meta)
    if md.stem == '01-introducao-sra-nexus-ive':
        personas = 'Sra. Nexus Ive'
    usable = []
    for heading, lines in sections:
        bullets = summarize_lines(lines, limit=4)
        if bullets:
            usable.append((clean_heading(heading), bullets))
    usable = usable[:5]
    if not usable:
        usable = [('Visão geral do módulo', ['Apresentar objetivos, contexto e próximos passos.'])]
    scene_count = len(usable)
    base_duration = max(3, duration // max(1, scene_count))
    out = [
        f'# Roteiro da Vídeo Aula: {title}',
        '',
        f'**Personas:** {personas}',
        f'**Duração Estimada:** {duration} minutos',
        f'**Nível:** {TRACK_META[track]["label"]}',
        f'**Pré-requisito:** {prereq}',
        '',
    ]
    for i, (heading, bullets) in enumerate(usable, start=1):
        mins = base_duration if i < scene_count else max(3, duration - base_duration * (scene_count - 1))
        lead = 'Sra. Nexus Ive' if (i % 2 == 1 or personas == 'Sra. Nexus Ive') else 'Sir. Nexus Alencar'
        support = None
        if personas != 'Sra. Nexus Ive':
            support = 'Sir. Nexus Alencar' if lead == 'Sra. Nexus Ive' else 'Sra. Nexus Ive'
        out.append(f'## Cena {i}: {heading} (Duração: {mins} minutos)')
        out.append('')
        out.append(f'**Visual:** Tela temática da trilha {TRACK_META[track]["label"]}, com apoio visual para o tópico "{heading}" e destaque dos pontos operacionais do módulo.')
        out.append('')
        bullet_a = bullets[0]
        bullet_b = bullets[1] if len(bullets) > 1 else bullets[0]
        out.append(f'**{lead}:** "Neste bloco, vamos direto ao ponto sobre {heading.lower()}. O foco aqui é {bullet_a.lower()} e como isso se traduz em execução real dentro do ecossistema Nexus."')
        out.append('')
        if support:
            out.append(f'**{support}:** "O insight estratégico é simples: {bullet_b}. Quando você estrutura isso corretamente, o módulo deixa de ser teoria e vira padrão operacional replicável."')
            out.append('')
        out.append('**Pontos de apoio em tela:**')
        for b in bullets:
            out.append(f'- {b}')
        out.append('')
    return '\n'.join(out) + '\n'


def run(cmd: List[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=str(cwd or ROOT), check=True)


def build_html(md: Path, track: str, title: str) -> None:
    out = html_file_path(md, track)
    out.parent.mkdir(parents=True, exist_ok=True)
    run([
        'pandoc', '-f', 'markdown', '-t', 'html5', '--standalone', '--embed-resources',
        '--metadata=lang:pt-BR', f'--metadata=title:{title}', f'--css={CSS_PATH}', '-o', str(out), str(md)
    ], cwd=md.parent)


def build_pdf(md: Path, track: str) -> None:
    html = html_file_path(md, track)
    pdf = pdf_file_path(md, track)
    run(['weasyprint', str(html), str(pdf)])


def main():
    created_slides = []
    created_roteiros = []
    created_html = []
    created_pdfs = []

    for track in ['fundamental', 'agente', 'elite', 'master']:
        for md in sorted((CURSOS / track).glob('*.md')):
            stem = md.stem
            if stem.endswith('-slides') or stem.endswith('-roteiro') or stem.endswith('-roteiro-revisado'):
                continue
            text = md.read_text(encoding='utf-8', errors='ignore')
            meta, body = parse_frontmatter_and_body(text)
            title = get_title(md, meta, body)
            sections = parse_sections(body)

            sfile = slide_file_path(md)
            if not sfile.exists():
                sfile.write_text(create_slides(md, track, title, meta, sections), encoding='utf-8')
                created_slides.append(str(sfile.relative_to(ROOT)))

            rfile = roteiro_file_path(md)
            if not rfile.exists():
                rfile.write_text(create_roteiro(md, track, title, meta, sections), encoding='utf-8')
                created_roteiros.append(str(rfile.relative_to(ROOT)))

            hfile = html_file_path(md, track)
            if not hfile.exists():
                build_html(md, track, title)
                created_html.append(str(hfile.relative_to(ROOT)))

            pfile = pdf_file_path(md, track)
            if not pfile.exists():
                if not hfile.exists():
                    build_html(md, track, title)
                build_pdf(md, track)
                created_pdfs.append(str(pfile.relative_to(ROOT)))

    report_lines = ['# Materiais pendentes gerados', '']
    report_lines += ['## Slides criados']
    report_lines += [f'- `{p}`' for p in created_slides] if created_slides else ['- Nenhum']
    report_lines += ['', '## Roteiros criados']
    report_lines += [f'- `{p}`' for p in created_roteiros] if created_roteiros else ['- Nenhum']
    report_lines += ['', '## HTML criados']
    report_lines += [f'- `{p}`' for p in created_html] if created_html else ['- Nenhum']
    report_lines += ['', '## PDFs criados']
    report_lines += [f'- `{p}`' for p in created_pdfs] if created_pdfs else ['- Nenhum']
    report_lines += ['']
    REPORT.write_text('\n'.join(report_lines) + '\n', encoding='utf-8')
    print('slides', len(created_slides))
    print('roteiros', len(created_roteiros))
    print('html', len(created_html))
    print('pdf', len(created_pdfs))
    print(REPORT.relative_to(ROOT))


if __name__ == '__main__':
    main()

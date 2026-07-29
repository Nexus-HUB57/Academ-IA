#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

ROOT = Path('/home/user/repo/Academ-IA')
TODAY = date(2026, 7, 24).isoformat()

PUBLISH_PLAN_JSON = ROOT / 'youtube' / 'publish_plan.json'
COURSES = ROOT / 'cursos'
VIDEOS = ROOT / 'videos'
YOUTUBE = ROOT / 'youtube'
DOCS = ROOT / 'docs'


def load_publish_plan() -> list[dict]:
    data = json.loads(PUBLISH_PLAN_JSON.read_text(encoding='utf-8'))
    if isinstance(data, dict):
        if 'videos' in data and isinstance(data['videos'], list):
            return data['videos']
        if 'items' in data and isinstance(data['items'], list):
            return data['items']
    if isinstance(data, list):
        return data
    raise ValueError('Formato inesperado em publish_plan.json')


TRACK_MAP = {
    '00': ('fundamental', '00-boas-vindas'),
    '01': ('fundamental', '01-entendendo-ioaid'),
    '02': ('fundamental', '02-sistema-sho'),
    '03': ('fundamental', '03-painel-afiliado'),
    '04': ('agente', '00-primeiro-agente'),
    '05': ('agente', '01-skills-essenciais'),
    '06': ('agente', '02-disparo-whatsapp'),
    '07': ('agente', '03-judge-revisor'),
    '08': ('master', '00-otimizacao-conversao'),
    '09': ('master', '01-funis-lifecycle'),
    '10': ('master', '02-ab-test-judge'),
    '11': ('master', '03-coortes-churn'),
    '12': ('elite', '00-blueprints-elite'),
    '13': ('elite', '01-multi-tenant-whitelabel'),
    '14': ('elite', '02-federacao-agentes'),
}

FULL_AUDIO_MAP = {
    '00': 'full_00_alencar.wav',
    '01': 'full_01_ive.wav',
    '02': 'full_02_alencar.wav',
    '03': 'full_03_dupla.wav',
    '04': 'full_04_alencar.wav',
    '05': 'full_05_alencar.wav',
    '06': 'full_06_alencar.wav',
    '07': 'full_07_alencar.wav',
    '08': 'full_08_dupla.wav',
    '09': 'full_09_dupla.wav',
    '10': 'full_10_dupla.wav',
    '11': 'full_11_dupla.wav',
    '12': 'full_12_dupla.wav',
    '13': 'full_13_dupla.wav',
    '14': 'full_14_dupla.wav',
}

FRAME_TEMPLATE = 'full_{code}_f{idx}.png'
THUMB_FULL_TEMPLATE = 'thumb_video-{code}-{slug}-full.jpg'
THUMB_LOCAL_MAP = {
    '00': ['thumb-00-boas-vindas.png'],
    '01': ['thumb-01-ioaid.png', 'thumb-01-ioaid.webp'],
    '02': ['thumb-02-sho.png'],
    '03': ['thumb-03-painel.png', 'thumb-03-painel-afiliado.webp'],
    '04': ['thumb-04-primeiro-agente.png'],
    '05': ['thumb-05-skills.png', 'thumb-05-skills-essenciais.webp'],
    '06': ['thumb-06-disparo.png', 'thumb-06-disparo-whatsapp.webp'],
    '07': ['thumb-07-judge.png', 'thumb-07-judge-revisor.webp'],
    '08': ['thumb-08-otimizacao.png', 'thumb-08-otimizacao-conversao.webp'],
    '09': ['thumb-09-funis-lifecycle.webp'],
    '10': ['thumb-10-ab-test-judge.webp'],
    '11': ['thumb-11-coortes-churn.webp'],
    '12': ['thumb-12-blueprints-elite.webp'],
    '13': ['thumb-13-multi-tenant.webp'],
    '14': ['thumb-14-federacao-agentes.webp'],
}
TEASER_ALIAS_MAP = {
    '04': ['video-04-seu-primeiro-agente.mp4'],
    '05': ['video-05-skills-assembly.mp4', 'video-05-skills-essenciais.mp4'],
    '06': ['video-06-disparo-no-whatsapp-em-escala.mp4'],
    '07': ['video-07-judge-revisor.mp4', 'video-07-judge-scales.mp4'],
    '08': ['video-08-otimizacao-de-conversao.mp4'],
    '09': ['video-09-funis-e-lifecycle.mp4'],
    '10': ['video-10-a-b-testing-com-judge.mp4'],
    '11': ['video-11-coortes-e-churn.mp4'],
    '12': ['video-12-blueprints-elite.mp4'],
    '13': ['video-13-multi-tenant-e-white-label.mp4'],
    '14': ['video-14-federacao-de-agentes-zero-trust.mp4'],
}


publish_plan = load_publish_plan()
rows = []

for item in publish_plan:
    code = str(item.get('code', '')).zfill(2)
    track, course_base = TRACK_MAP[code]
    slug = str(item.get('slug', '')).replace('video-', '', 1)
    title = item.get('title') or item.get('youtube_title') or course_base
    status = item.get('status', 'unknown')

    roteiro_video = VIDEOS / 'roteiros' / f'{code}-{course_base.split("-", 1)[1]}-roteiro.md'
    # fallback: tolerate naming divergence by glob
    if not roteiro_video.exists():
        matches = sorted((VIDEOS / 'roteiros').glob(f'{code}-*-roteiro.md'))
        roteiro_video = matches[0] if matches else roteiro_video

    curso_dir = COURSES / track
    roteiro_curso = curso_dir / f'{course_base}-roteiro.md'
    slides_curso = curso_dir / f'{course_base}-slides.md'
    html_candidates = sorted((ROOT / 'html' / 'cursos' / track).glob(f'{course_base}.html'))
    pdf_candidates = sorted((ROOT / 'pdfs').glob(f'curso-{track}-{course_base}.pdf'))

    video_basename = Path(item.get('video_path', '')).name
    thumb_basename = Path(item.get('thumbnail_path', '')).name
    desc_basename = f'{slug}.txt'

    full_video = VIDEOS / video_basename
    full_audio = VIDEOS / 'audio' / FULL_AUDIO_MAP[code]
    desc_file = YOUTUBE / 'descriptions' / desc_basename
    yt_thumb_png = YOUTUBE / 'thumbnails' / thumb_basename
    yt_thumb_jpg = YOUTUBE / 'thumbnails_yt' / thumb_basename.replace('.png', '.jpg')
    full_thumb_jpg = VIDEOS / THUMB_FULL_TEMPLATE.format(code=code, slug=slug)
    local_thumb_files = [VIDEOS / 'thumbnails' / name for name in THUMB_LOCAL_MAP.get(code, [])]
    teaser_files = [YOUTUBE / 'videos_teaser' / name for name in TEASER_ALIAS_MAP.get(code, [])]
    frame_files = [VIDEOS / 'frames' / FRAME_TEMPLATE.format(code=code, idx=i) for i in range(4)]

    row = {
        'code': code,
        'track': track,
        'course_base': course_base,
        'title': title,
        'publish_status': status,
        'video_script': roteiro_video.exists(),
        'course_script': roteiro_curso.exists(),
        'course_slides': slides_curso.exists(),
        'course_html': any(p.exists() for p in html_candidates),
        'course_pdf': any(p.exists() for p in pdf_candidates),
        'full_audio': full_audio.exists(),
        'full_video': full_video.exists(),
        'description_txt': desc_file.exists(),
        'youtube_thumb_png': yt_thumb_png.exists(),
        'youtube_thumb_jpg': yt_thumb_jpg.exists(),
        'full_thumb_jpg': full_thumb_jpg.exists(),
        'local_thumb_count': sum(1 for p in local_thumb_files if p.exists()),
        'teaser_count': sum(1 for p in teaser_files if p.exists()),
        'frames_4_of_4': sum(1 for p in frame_files if p.exists()) == 4,
        'full_audio_name': full_audio.name,
        'full_video_name': full_video.name,
        'description_name': desc_basename,
        'youtube_thumb_name': thumb_basename,
        'video_script_name': roteiro_video.name if roteiro_video.exists() else '',
        'course_script_name': roteiro_curso.name if roteiro_curso.exists() else '',
        'slides_name': slides_curso.name if slides_curso.exists() else '',
    }
    row['all_core_ok'] = all([
        row['video_script'], row['course_script'], row['course_slides'], row['course_html'], row['course_pdf'],
        row['full_audio'], row['full_video'], row['description_txt'], row['youtube_thumb_png'],
        row['youtube_thumb_jpg'], row['full_thumb_jpg'], row['frames_4_of_4']
    ])
    rows.append(row)

backlog_roteiros = []
for p in sorted((VIDEOS / 'roteiros').glob('[1-9][5-9]-*-roteiro.md')):
    n = p.name.split('-', 1)[0]
    backlog_roteiros.append({'code': n, 'roteiro': p.name, 'thumb_exists': (VIDEOS / 'thumbnails' / f'thumb-{n}-{p.stem[len(n)+1:-8]}.webp').exists()})

summary = {
    'date': TODAY,
    'publish_plan_total': len(rows),
    'all_core_ok_total': sum(1 for r in rows if r['all_core_ok']),
    'published_total': sum(1 for r in rows if r['publish_status'] == 'uploaded'),
    'ready_total': sum(1 for r in rows if r['publish_status'] == 'ready_to_upload'),
    'video_script_total': sum(1 for r in rows if r['video_script']),
    'course_script_total': sum(1 for r in rows if r['course_script']),
    'course_slides_total': sum(1 for r in rows if r['course_slides']),
    'course_html_total': sum(1 for r in rows if r['course_html']),
    'course_pdf_total': sum(1 for r in rows if r['course_pdf']),
    'full_audio_total': sum(1 for r in rows if r['full_audio']),
    'full_video_total': sum(1 for r in rows if r['full_video']),
    'description_total': sum(1 for r in rows if r['description_txt']),
    'youtube_thumb_png_total': sum(1 for r in rows if r['youtube_thumb_png']),
    'youtube_thumb_jpg_total': sum(1 for r in rows if r['youtube_thumb_jpg']),
    'full_thumb_jpg_total': sum(1 for r in rows if r['full_thumb_jpg']),
    'frames_ok_total': sum(1 for r in rows if r['frames_4_of_4']),
    'teaser_coverage_total': sum(1 for r in rows if r['teaser_count'] > 0),
    'ready_codes': [r['code'] for r in rows if r['publish_status'] == 'ready_to_upload'],
    'uploaded_codes': [r['code'] for r in rows if r['publish_status'] == 'uploaded'],
    'missing_or_partial': [
        {
            'code': r['code'],
            'title': r['title'],
            'publish_status': r['publish_status'],
            'missing': [k for k in [
                'video_script', 'course_script', 'course_slides', 'course_html', 'course_pdf',
                'full_audio', 'full_video', 'description_txt', 'youtube_thumb_png',
                'youtube_thumb_jpg', 'full_thumb_jpg', 'frames_4_of_4'
            ] if not r[k]],
            'teaser_count': r['teaser_count'],
            'local_thumb_count': r['local_thumb_count'],
        }
        for r in rows if (not r['all_core_ok']) or r['teaser_count'] == 0
    ],
    'backlog_codes_15_19': [b['code'] for b in backlog_roteiros],
}

json_path = DOCS / f'AUDITORIA_DESENVOLVIMENTO_VIDEO_SLIDES_AUDIO_{TODAY}.json'
md_path = DOCS / f'AUDITORIA_DESENVOLVIMENTO_VIDEO_SLIDES_AUDIO_{TODAY}.md'
csv_path = DOCS / f'AUDITORIA_DESENVOLVIMENTO_VIDEO_SLIDES_AUDIO_{TODAY}.csv'

json_path.write_text(json.dumps({'summary': summary, 'modules': rows, 'backlog_15_19': backlog_roteiros}, ensure_ascii=False, indent=2), encoding='utf-8')

with csv_path.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

lines = []
lines.append('# Auditoria de Desenvolvimento — Vídeos, Slides e Áudios')
lines.append('')
lines.append(f'**Data:** {TODAY}')
lines.append('')
lines.append('## Resumo executivo')
lines.append(f"- Publish plan canônico: **{summary['publish_plan_total']}** módulos")
lines.append(f"- Módulos com pacote core completo (roteiro vídeo + roteiro curso + slides + HTML + PDF + áudio full + vídeo full + descrição + thumbs YouTube + thumb full + 4 frames): **{summary['all_core_ok_total']}/{summary['publish_plan_total']}**")
lines.append(f"- Publicados no YouTube: **{summary['published_total']}**")
lines.append(f"- Prontos para upload: **{summary['ready_total']}**")
lines.append(f"- Roteiros de vídeo: **{summary['video_script_total']}/{summary['publish_plan_total']}**")
lines.append(f"- Roteiros de curso: **{summary['course_script_total']}/{summary['publish_plan_total']}**")
lines.append(f"- Slides de curso: **{summary['course_slides_total']}/{summary['publish_plan_total']}**")
lines.append(f"- HTMLs de curso: **{summary['course_html_total']}/{summary['publish_plan_total']}**")
lines.append(f"- PDFs de curso: **{summary['course_pdf_total']}/{summary['publish_plan_total']}**")
lines.append(f"- Áudios full: **{summary['full_audio_total']}/{summary['publish_plan_total']}**")
lines.append(f"- Vídeos full: **{summary['full_video_total']}/{summary['publish_plan_total']}**")
lines.append(f"- Descrições YouTube: **{summary['description_total']}/{summary['publish_plan_total']}**")
lines.append(f"- Thumbs YouTube PNG: **{summary['youtube_thumb_png_total']}/{summary['publish_plan_total']}**")
lines.append(f"- Thumbs YouTube JPG: **{summary['youtube_thumb_jpg_total']}/{summary['publish_plan_total']}**")
lines.append(f"- Thumbs full JPG em `videos/`: **{summary['full_thumb_jpg_total']}/{summary['publish_plan_total']}**")
lines.append(f"- Frames 4/4 por vídeo: **{summary['frames_ok_total']}/{summary['publish_plan_total']}**")
lines.append(f"- Cobertura de teaser local: **{summary['teaser_coverage_total']}/{summary['publish_plan_total']}**")
lines.append('')
lines.append('## Conclusões')
if summary['all_core_ok_total'] == summary['publish_plan_total']:
    lines.append('- O desenvolvimento dos ativos principais das vídeo-aulas está **completo para os 15 módulos canônicos** do publish plan.')
else:
    lines.append('- Ainda existem lacunas em parte do pacote core. Ver a seção de pendências abaixo.')
if summary['teaser_coverage_total'] < summary['publish_plan_total']:
    missing_teasers = ', '.join(r['code'] for r in rows if r['teaser_count'] == 0)
    lines.append(f'- A cobertura de teaser não é total: faltam arquivos locais de teaser para os códigos **{missing_teasers}**.')
lines.append('- Há material de expansão/backlog para os códigos **15-19** em `videos/roteiros/` e `videos/thumbnails/`, fora do publish plan atual.')
lines.append('')
lines.append('## Fila pronta atual')
for code in summary['ready_codes']:
    r = next(x for x in rows if x['code'] == code)
    lines.append(f"- **{code}** · {r['title']} · áudio `{r['full_audio_name']}` · vídeo `{r['full_video_name']}` · descrição `{r['description_name']}`")
lines.append('')
lines.append('## Publicados')
lines.append('- ' + ', '.join(summary['uploaded_codes']))
lines.append('')
lines.append('## Pendências / atenção')
if summary['missing_or_partial']:
    for item in summary['missing_or_partial']:
        lines.append(f"- **{item['code']}** · {item['title']} · faltas: {', '.join(item['missing']) or 'nenhuma'} · teasers: {item['teaser_count']} · thumbs locais: {item['local_thumb_count']}")
else:
    lines.append('- Nenhuma pendência no pacote core.')
lines.append('')
lines.append('## Backlog fora do publish plan atual')
for b in backlog_roteiros:
    lines.append(f"- **{b['code']}** · `{b['roteiro']}`")
lines.append('')
lines.append('## Arquivos gerados nesta auditoria')
lines.append(f'- `{json_path.relative_to(ROOT)}`')
lines.append(f'- `{md_path.relative_to(ROOT)}`')
lines.append(f'- `{csv_path.relative_to(ROOT)}`')

md_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))

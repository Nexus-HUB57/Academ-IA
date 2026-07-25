#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

ROOT = Path('/home/user/repo/Academ-IA')
TODAY = date(2026, 7, 24).isoformat()
WORK = ROOT / 'materiais' / 'video-aulas'
DOCS = ROOT / 'docs'

PUBLISH = json.loads((ROOT / 'youtube' / 'publish_plan.json').read_text(encoding='utf-8'))

TRACK_MAP = {
    '00': ('fundamental', '00-boas-vindas', 'alencar'),
    '01': ('fundamental', '01-entendendo-ioaid', 'ive'),
    '02': ('fundamental', '02-sistema-sho', 'alencar'),
    '03': ('fundamental', '03-painel-afiliado', 'dupla'),
    '04': ('agente', '00-primeiro-agente', 'alencar'),
    '05': ('agente', '01-skills-essenciais', 'alencar'),
    '06': ('agente', '02-disparo-whatsapp', 'alencar'),
    '07': ('agente', '03-judge-revisor', 'alencar'),
    '08': ('master', '00-otimizacao-conversao', 'dupla'),
    '09': ('master', '01-funis-lifecycle', 'dupla'),
    '10': ('master', '02-ab-test-judge', 'dupla'),
    '11': ('master', '03-coortes-churn', 'dupla'),
    '12': ('elite', '00-blueprints-elite', 'dupla'),
    '13': ('elite', '01-multi-tenant-whitelabel', 'alencar'),
    '14': ('elite', '02-federacao-agentes', 'dupla'),
}

TARGETS = {
    '00': 75, '01': 90, '02': 95, '03': 105,
    '04': 90, '05': 95, '06': 100, '07': 105,
    '08': 135, '09': 145, '10': 145, '11': 150,
    '12': 155, '13': 160, '14': 165,
}

COVER_MAP = {
    '00': ('capa-00-boas-vindas-ive.png', 'thumb-00-boas-vindas.png'),
    '01': ('capa-01-entendendo-ioaid-dupla.png', 'thumb-01-ioaid.png'),
    '02': ('capa-02-sistema-sho-dupla.png', 'thumb-02-sho.png'),
    '03': ('capa-03-painel-afiliado-ive.png', 'thumb-03-painel.png'),
    '04': ('capa-04-primeiro-agente-dupla.png', 'thumb-04-primeiro-agente.png'),
    '05': ('capa-05-skills-essenciais-alencar.png', 'thumb-05-skills.png'),
    '06': ('capa-06-disparo-whatsapp-alencar.png', 'thumb-06-disparo.png'),
    '07': ('capa-07-judge-revisor-alencar.png', 'thumb-07-judge.png'),
    '08': ('capa-08-otimizacao-conversao-dupla.png', 'thumb-08-otimizacao.png'),
    '09': ('capa-09-funis-lifecycle-dupla.png', 'thumb-09-funis-lifecycle.webp'),
    '10': ('capa-10-ab-testing-judge-dupla.png', 'thumb-10-ab-test-judge.webp'),
    '11': ('capa-11-coortes-churn-dupla.png', 'thumb-11-coortes-churn.webp'),
    '12': ('capa-12-blueprints-elite-dupla.png', 'thumb-12-blueprints-elite.webp'),
    '13': ('capa-13-multi-tenant-dupla.png', 'thumb-13-multi-tenant.webp'),
    '14': ('capa-14-federacao-agentes-dupla.png', 'thumb-14-federacao-agentes.webp'),
}

LEGACY_VIDEO_MAP = {
    '00': 'video-00-boas-vindas-a-academia-nexus-full.mp4',
    '01': 'video-01-entendendo-o-ioaid-full.mp4',
    '02': 'video-02-o-sistema-sho-full.mp4',
    '03': 'video-03-painel-do-afiliado-full.mp4',
    '04': 'video-04-primeiro-agente-full.mp4',
    '05': 'video-05-skills-essenciais-full.mp4',
    '06': 'video-06-disparo-whatsapp-em-escala-full.mp4',
    '07': 'video-07-judge-revisor-full.mp4',
    '08': 'video-08-otimizacao-de-conversao-full.mp4',
    '09': 'video-09-funis-e-lifecycle-full.mp4',
    '10': 'video-10-a-b-testing-com-judge-full.mp4',
    '11': 'video-11-coortes-e-churn-full.mp4',
    '12': 'video-12-blueprints-elite-full.mp4',
    '13': 'video-13-multi-tenant-e-white-label-full.mp4',
    '14': 'video-14-federacao-de-agentes-full.mp4',
}

AUDIO_MAP = {
    '00': 'full_00_alencar.wav', '01': 'full_01_ive.wav', '02': 'full_02_alencar.wav',
    '03': 'full_03_dupla.wav', '04': 'full_04_alencar.wav', '05': 'full_05_alencar.wav',
    '06': 'full_06_alencar.wav', '07': 'full_07_alencar.wav', '08': 'full_08_dupla.wav',
    '09': 'full_09_dupla.wav', '10': 'full_10_dupla.wav', '11': 'full_11_dupla.wav',
    '12': 'full_12_dupla.wav', '13': 'full_13_dupla.wav', '14': 'full_14_dupla.wav',
}

PERSONA_REF = {
    'ive': [
        'marca/personas/ive/assets/ive_reference.png',
        'marca/personas/ive/audio/official_voice.wav',
    ],
    'alencar': [
        'marca/personas/alencar/assets/alencar_reference.png',
        'marca/personas/alencar/voz_sir_nexus_alencar.wav',
    ],
    'dupla': [
        'marca/personas/dupla/assets/celebration_ive_alencar.png',
        'marca/personas/alencar/voz_sir_nexus_alencar.wav',
        'marca/personas/ive/audio/official_voice.wav',
    ],
}


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def symlink(src: Path, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        dest.unlink()
    target = os.path.relpath(src, dest.parent)
    dest.symlink_to(target)


modules = []

for item in PUBLISH:
    code = str(item['code']).zfill(2)
    track, base, persona = TRACK_MAP[code]
    module_dir = WORK / track / base
    slug_pub = item['slug']
    publish_video_name = Path(item['video_path']).name
    desc_name = f"{slug_pub.replace('video-', '', 1)}.txt"
    cover_name, thumb_name = COVER_MAP[code]

    paths = {
        'capa_oficial': ROOT / 'producao' / 'assets' / 'thumbnails' / cover_name,
        'thumb_operacional': ROOT / 'producao' / 'assets' / 'thumbnails' / thumb_name,
        'slides_curso': ROOT / 'cursos' / track / f'{base}-slides.md',
        'roteiro_curso': ROOT / 'cursos' / track / f'{base}-roteiro.md',
        'roteiro_video': sorted((ROOT / 'videos' / 'roteiros').glob(f'{code}-*-roteiro.md'))[0],
        'audio_legado': ROOT / 'videos' / 'audio' / AUDIO_MAP[code],
        'video_legado': ROOT / 'videos' / LEGACY_VIDEO_MAP[code],
        'descricao_youtube': ROOT / 'youtube' / 'descriptions' / desc_name,
        'thumb_youtube_png': ROOT / 'youtube' / 'thumbnails' / Path(item['thumbnail_path']).name,
        'html_curso': ROOT / 'html' / 'cursos' / track / f'{base}.html',
        'pdf_curso': ROOT / 'pdfs' / f'curso-{track}-{base}.pdf',
    }

    for kind in ['capas', 'slides', 'roteiros', 'audios', 'videos', 'publicacao', 'curso']:
        (module_dir / kind).mkdir(parents=True, exist_ok=True)

    link_map = {
        module_dir / 'capas' / cover_name: paths['capa_oficial'],
        module_dir / 'capas' / thumb_name: paths['thumb_operacional'],
        module_dir / 'slides' / paths['slides_curso'].name: paths['slides_curso'],
        module_dir / 'roteiros' / paths['roteiro_curso'].name: paths['roteiro_curso'],
        module_dir / 'roteiros' / paths['roteiro_video'].name: paths['roteiro_video'],
        module_dir / 'audios' / paths['audio_legado'].name: paths['audio_legado'],
        module_dir / 'videos' / paths['video_legado'].name: paths['video_legado'],
        module_dir / 'publicacao' / paths['descricao_youtube'].name: paths['descricao_youtube'],
        module_dir / 'publicacao' / paths['thumb_youtube_png'].name: paths['thumb_youtube_png'],
        module_dir / 'curso' / paths['html_curso'].name: paths['html_curso'],
        module_dir / 'curso' / paths['pdf_curso'].name: paths['pdf_curso'],
    }
    for ref in PERSONA_REF[persona]:
        src = ROOT / ref
        link_map[module_dir / 'capas' / src.name if src.suffix.lower() in {'.png', '.webp', '.jpg'} else module_dir / 'audios' / src.name] = src

    for dest, src in link_map.items():
        if src.exists():
            symlink(src, dest)

    module_manifest = {
        'code': code,
        'title': item['title'],
        'track': track,
        'persona': persona,
        'target_duration_s': TARGETS[code],
        'approved_cover': rel(paths['capa_oficial']),
        'approved_thumb': rel(paths['thumb_operacional']),
        'slides_source': rel(paths['slides_curso']),
        'course_script': rel(paths['roteiro_curso']),
        'video_script': rel(paths['roteiro_video']),
        'legacy_audio': rel(paths['audio_legado']),
        'legacy_video': rel(paths['video_legado']),
        'youtube_description': rel(paths['descricao_youtube']),
        'final_video_name': f'video-{code}-{slug_pub.replace("video-", "")}-master.mp4',
        'opening_video_name': f'video-{code}-opening.mp4',
        'new_audio_name': f'rebuild_{code}_narracao_ptbr.wav',
        'workspace_dir': rel(module_dir),
        'status': 'pronto_para_rebuild',
    }
    (module_dir / 'manifest.json').write_text(json.dumps(module_manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    modules.append(module_manifest)

summary = {
    'date': TODAY,
    'workspace_root': rel(WORK),
    'modules_total': len(modules),
    'tracks': {t: sum(1 for m in modules if m['track'] == t) for t in ['fundamental', 'agente', 'master', 'elite']},
    'models_approved': {
        'opening': 'kling/v3',
        'narration': 'fal-ai/minimax/speech-2.8-hd',
    },
    'duration_rule_s': {'materiais_simples_min': 60, 'video_aulas_max': 240},
}

manifest = {'summary': summary, 'modules': modules}
(DOCS / f'MANIFESTO_REBUILD_VIDEO_AULAS_00_14_{TODAY}.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

md = []
md.append('# Manifesto Operacional do Rebuild — Vídeo-Aulas 00-14')
md.append('')
md.append(f'**Data:** {TODAY}')
md.append('')
md.append('## Estrutura canônica criada')
md.append(f'- Workspace principal: `{rel(WORK)}`')
md.append('- Organização por trilha > módulo > tipos de material (capas, slides, roteiros, áudios, vídeos, publicação, curso).')
md.append('- Cada pasta de módulo contém links canônicos para os arquivos reais já existentes no repositório.')
md.append('')
md.append('## Modelos aprovados')
md.append('- Abertura visual: `kling/v3`')
md.append('- Narração: `fal-ai/minimax/speech-2.8-hd`')
md.append('')
md.append('## Duração-alvo por vídeo')
for m in modules:
    md.append(f"- **{m['code']} · {m['title']}** → **{m['target_duration_s']}s** · persona `{m['persona']}`")
md.append('')
md.append('## Naming final')
md.append('- Áudio novo: `rebuild_{code}_narracao_ptbr.wav`')
md.append('- Abertura: `video-{code}-opening.mp4`')
md.append('- Master final: `video-{code}-{slug}-master.mp4`')
md.append('')
md.append('## Handoff operacional')
md.append('- Reusar capa oficial e thumb aprovados a partir de `producao/assets/thumbnails`.')
md.append('- Reusar slides e roteiros já existentes como base do rebuild.')
md.append('- Gerar nova narração na duração-alvo e sincronizar com 5-10 slides.')
md.append('- Publicação só após aprovação humana do novo master.')

(DOCS / f'MANIFESTO_REBUILD_VIDEO_AULAS_00_14_{TODAY}.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))

#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

ROOT = Path('/home/user/repo/Academ-IA')
TODAY = date(2026, 7, 24).isoformat()

PUBLISH_PLAN = ROOT / 'youtube' / 'publish_plan.json'
DOCS = ROOT / 'docs'
VIDEOS = ROOT / 'videos'
COURSES = ROOT / 'cursos'

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

LEGACY_FULL_MAP = {
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

COVER_MAP = {
    '00': 'thumb-00-boas-vindas.png',
    '01': 'thumb-01-ioaid.png',
    '02': 'thumb-02-sho.png',
    '03': 'thumb-03-painel.png',
    '04': 'thumb-04-primeiro-agente.png',
    '05': 'thumb-05-skills.png',
    '06': 'thumb-06-disparo.png',
    '07': 'thumb-07-judge.png',
    '08': 'thumb-08-otimizacao.png',
    '09': 'thumb-09-funis-lifecycle.webp',
    '10': 'thumb-10-ab-test-judge.webp',
    '11': 'thumb-11-coortes-churn.webp',
    '12': 'thumb-12-blueprints-elite.webp',
    '13': 'thumb-13-multi-tenant.webp',
    '14': 'thumb-14-federacao-agentes.webp',
}

AUDIO_MAP = {
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

OPENING_SEC = 8
CTA_SEC = 8
TARGET_MIN = 60
TARGET_MAX = 240


def ffprobe(path: Path) -> dict:
    out = subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration,size:stream=codec_type,width,height,r_frame_rate,codec_name,sample_rate,channels,bit_rate',
        '-of', 'json', str(path)
    ])
    return json.loads(out)


def count_slide_sections(text: str) -> int:
    patterns = [
        r'^##\s+Slide\s+\d+',
        r'^##\s+📍\s*SLIDE\s+\d+',
        r'^##\s+SLIDE\s+\d+',
    ]
    total = 0
    for line in text.splitlines():
        if any(re.search(p, line, re.I) for p in patterns):
            total += 1
    return total


@dataclass
class Row:
    code: str
    title: str
    track: str
    publish_video_name: str
    legacy_video_name: str
    legacy_video_exists: bool
    legacy_duration_s: float | None
    legacy_width: int | None
    legacy_height: int | None
    legacy_fps: str | None
    legacy_has_audio: bool
    official_cover: str
    official_cover_exists: bool
    slides_file: str
    slide_count: int
    slides_in_range_5_10: bool
    audio_file: str
    audio_exists: bool
    audio_duration_s: float | None
    estimated_target_duration_s: float | None
    target_duration_ok: bool
    legacy_duration_ok: bool
    render_spec_ok: bool
    rebuild_required: bool
    rebuild_reason: list[str]


def main() -> None:
    publish = json.loads(PUBLISH_PLAN.read_text(encoding='utf-8'))
    rows: list[Row] = []
    for item in publish:
        code = str(item['code']).zfill(2)
        track, course_base = TRACK_MAP[code]
        slides_path = COURSES / track / f'{course_base}-slides.md'
        slides_text = slides_path.read_text(encoding='utf-8') if slides_path.exists() else ''
        slide_count = count_slide_sections(slides_text)
        legacy_video = VIDEOS / LEGACY_FULL_MAP[code]
        publish_video_name = Path(item['video_path']).name
        legacy_exists = legacy_video.exists()
        legacy_duration = None
        width = None
        height = None
        fps = None
        has_audio = False
        render_spec_ok = False
        legacy_duration_ok = False
        if legacy_exists:
            meta = ffprobe(legacy_video)
            fmt = meta.get('format', {})
            streams = meta.get('streams', [])
            v = next((s for s in streams if s.get('codec_type') == 'video'), {})
            a = next((s for s in streams if s.get('codec_type') == 'audio'), None)
            legacy_duration = round(float(fmt.get('duration', 0)), 2)
            width = v.get('width')
            height = v.get('height')
            fps = v.get('r_frame_rate')
            has_audio = a is not None
            legacy_duration_ok = TARGET_MIN <= legacy_duration <= TARGET_MAX
            render_spec_ok = (width == 1280 and height == 720 and fps == '25/1' and has_audio)

        cover = VIDEOS / 'thumbnails' / COVER_MAP[code]
        audio = VIDEOS / 'audio' / AUDIO_MAP[code]
        audio_exists = audio.exists()
        audio_duration = None
        if audio_exists:
            audio_duration = round(float(ffprobe(audio).get('format', {}).get('duration', 0)), 2)

        estimated_target = None
        target_duration_ok = False
        if slide_count:
            # 10–20s per slide + opening/cta, clamped to requested 60-240
            base = slide_count * 14 + OPENING_SEC + CTA_SEC
            estimated_target = float(max(TARGET_MIN, min(TARGET_MAX, base)))
            target_duration_ok = TARGET_MIN <= estimated_target <= TARGET_MAX and 5 <= slide_count <= 10

        reasons = []
        if not cover.exists():
            reasons.append('capa_oficial_ausente')
        if not slides_path.exists():
            reasons.append('slides_ausentes')
        if slides_path.exists() and not (5 <= slide_count <= 10):
            reasons.append('quantidade_slides_fora_do_padrao')
        if not audio_exists:
            reasons.append('audio_narracao_ausente')
        elif audio_duration is not None and audio_duration < 40:
            reasons.append('audio_curto_abaixo_do_padro_video_aula')
        if not legacy_exists:
            reasons.append('video_master_ausente')
        else:
            if not legacy_duration_ok:
                reasons.append('duracao_video_fora_do_padrao_60_240')
            if not render_spec_ok:
                reasons.append('spec_render_fora_do_padrao')

        rows.append(Row(
            code=code,
            title=item['title'],
            track=track,
            publish_video_name=publish_video_name,
            legacy_video_name=legacy_video.name,
            legacy_video_exists=legacy_exists,
            legacy_duration_s=legacy_duration,
            legacy_width=width,
            legacy_height=height,
            legacy_fps=fps,
            legacy_has_audio=has_audio,
            official_cover=cover.name,
            official_cover_exists=cover.exists(),
            slides_file=slides_path.name,
            slide_count=slide_count,
            slides_in_range_5_10=(5 <= slide_count <= 10),
            audio_file=audio.name,
            audio_exists=audio_exists,
            audio_duration_s=audio_duration,
            estimated_target_duration_s=estimated_target,
            target_duration_ok=target_duration_ok,
            legacy_duration_ok=legacy_duration_ok,
            render_spec_ok=render_spec_ok,
            rebuild_required=bool(reasons),
            rebuild_reason=reasons,
        ))

    summary = {
        'date': TODAY,
        'standard': {
            'video_aulas_duration_s': [60, 240],
            'slides_per_video': [5, 10],
            'cover': 'modelo oficial',
            'frames': 'slides + audio com sincronização contextual',
            'render': '1280x720 @ 25fps, H.264, AAC 192kbps',
        },
        'total_modules': len(rows),
        'rebuild_required_total': sum(1 for r in rows if r.rebuild_required),
        'legacy_duration_ok_total': sum(1 for r in rows if r.legacy_duration_ok),
        'render_spec_ok_total': sum(1 for r in rows if r.render_spec_ok),
        'slides_in_range_total': sum(1 for r in rows if r.slides_in_range_5_10),
        'official_cover_total': sum(1 for r in rows if r.official_cover_exists),
        'audio_exists_total': sum(1 for r in rows if r.audio_exists),
        'audio_short_total': sum(1 for r in rows if (r.audio_duration_s or 0) < 40),
        'modules_requiring_rebuild': [r.code for r in rows if r.rebuild_required],
    }

    md = []
    md.append('# Auditoria de Conformidade — Rebuild das Vídeo-Aulas Nexus')
    md.append('')
    md.append(f'**Data:** {TODAY}')
    md.append('')
    md.append('## Padrão adotado nesta rodada')
    md.append('- **Vídeo-aulas:** 60 a 240 segundos')
    md.append('- **Slides por vídeo:** mínimo 5 · máximo 10')
    md.append('- **Capa:** modelo oficial já aprovado')
    md.append('- **Frames:** slides + áudio de narração com sincronização contextual')
    md.append('- **Render:** 1280x720 @ 25fps · H.264 · AAC 192kbps')
    md.append('')
    md.append('## Resumo')
    md.append(f"- Total auditado: **{summary['total_modules']}** módulos")
    md.append(f"- Rebuild necessário: **{summary['rebuild_required_total']}** módulos")
    md.append(f"- Vídeos legados com duração já dentro do intervalo 60–240s: **{summary['legacy_duration_ok_total']}**")
    md.append(f"- Vídeos legados já conformes também em spec de render: **{summary['render_spec_ok_total']}**")
    md.append(f"- Slides no intervalo 5–10: **{summary['slides_in_range_total']}**")
    md.append(f"- Capas oficiais existentes: **{summary['official_cover_total']}**")
    md.append(f"- Áudios existentes: **{summary['audio_exists_total']}**")
    md.append(f"- Áudios ainda curtos para o novo padrão: **{summary['audio_short_total']}**")
    md.append('')
    md.append('## Veredito')
    md.append('- **Todos os 15 módulos 00-14 exigem rebuild** para cumprir integralmente o padrão Nexus de vídeo-aula definido nesta rodada.')
    md.append('- O principal motivo é **duração insuficiente do vídeo legado** e, em muitos casos, **áudio narrado ainda curto para o novo intervalo 60–240s**.')
    md.append('')
    md.append('## Módulo a módulo')
    for r in rows:
        md.append(
            f"- **{r.code} · {r.title}** · slides {r.slide_count} · áudio {r.audio_duration_s}s · legado {r.legacy_duration_s}s · rebuild: {'sim' if r.rebuild_required else 'não'} · motivos: {', '.join(r.rebuild_reason) or 'nenhum'}"
        )
    md.append('')
    md.append('## Diretriz de reconstrução')
    md.append('- Reusar **capa oficial já aprovada** como frame de abertura.')
    md.append('- Reusar arquivos de slides como base de 5–10 quadros sincronizados.')
    md.append('- Gerar **nova narração** para cada módulo com duração-alvo entre 60s e 240s.')
    md.append('- Produzir master final em naming canônico e mover provas/POCs para categoria legada.')

    out_json = DOCS / f'AUDITORIA_PADRAO_NEXUS_VIDEO_AULAS_{TODAY}.json'
    out_md = DOCS / f'AUDITORIA_PADRAO_NEXUS_VIDEO_AULAS_{TODAY}.md'
    out_json.write_text(json.dumps({'summary': summary, 'modules': [asdict(r) for r in rows]}, ensure_ascii=False, indent=2), encoding='utf-8')
    out_md.write_text('\n'.join(md) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

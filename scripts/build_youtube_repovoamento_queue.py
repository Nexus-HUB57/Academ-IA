#!/usr/bin/env python3
"""Monta a fila canônica de povoamento do YouTube a partir dos masters reconstruídos."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path('/home/user/repo/Academ-IA')
MANIFEST_JSON = ROOT / 'docs' / 'MANIFESTO_REBUILD_VIDEO_AULAS_00_14_2026-07-24.json'
OUT_JSON = ROOT / 'youtube' / 'upload_queue_repovoamento_2026-07-25.json'
OUT_MD = ROOT / 'docs' / 'FILA_YOUTUBE_REPOVOAMENTO_2026-07-25.md'


def ffprobe_duration(path: Path) -> float:
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'default=nw=1:nk=1', str(path)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def main():
    data = json.loads(MANIFEST_JSON.read_text(encoding='utf-8'))
    modules = data['modules']
    queue = []
    for mod in modules:
        code = mod['code']
        ws = ROOT / mod['workspace_dir'] / 'rebuild'
        candidates = list(ws.glob(f'video-{code}-*-master.mp4'))
        if not candidates:
            continue
        final = candidates[0]
        dur = ffprobe_duration(final)
        queue.append({
            'code': code,
            'title': mod['title'],
            'track': mod['track'],
            'persona': mod['persona'],
            'master_video': str(final.relative_to(ROOT)),
            'duration_s': round(dur, 2),
            'cover': mod['approved_cover'],
            'thumb': mod['approved_thumb'],
            'youtube_description': mod['youtube_description'],
            'target_duration_s': mod['target_duration_s'],
            'status': 'ready_to_upload',
            'meets_standard': 60 <= dur <= 240,
        })

    payload = {
        'date': '2026-07-25',
        'total_modules': len(queue),
        'ready_to_upload': sum(1 for x in queue if x['meets_standard']),
        'short_below_standard': sum(1 for x in queue if not x['meets_standard']),
        'render_spec': '1280x720@25fps H.264 + AAC 192k',
        'covers_source': 'producao/assets/thumbnails',
        'note_reference_test_video': 'https://youtube.com/watch?v=cBhbg51peQk (áudio ok, faltavam capa+slides)',
        'items': queue,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')

    lines = [
        '# Fila de Povoamento YouTube — Rebuild 00-14',
        '',
        f"- Data: 2026-07-25",
        f"- Total: {payload['total_modules']}",
        f"- Prontos dentro do padrão (60-240s): {payload['ready_to_upload']}",
        f"- Curtos (< 60s) para nova narração antes do upload: {payload['short_below_standard']}",
        f"- Render: {payload['render_spec']}",
        '',
        '| Code | Título | Trilha | Persona | Duração (s) | Padrão | Master | Capa |',
        '|------|--------|--------|---------|-------------|--------|--------|------|',
    ]
    for it in queue:
        lines.append(
            f"| {it['code']} | {it['title']} | {it['track']} | {it['persona']} | {it['duration_s']} | "
            f"{'✅' if it['meets_standard'] else '⚠️ curto'} | `{it['master_video']}` | `{it['cover']}` |"
        )
    OUT_MD.write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

from __future__ import annotations

from pathlib import Path
import json
import re
import subprocess
from typing import Optional

ROOT = Path('/home/user/repo/Academ-IA').resolve()
REPORT_MD = ROOT / 'docs' / 'AUDITORIA_VOZ_AUDIO_SYNC_2026-07-24.md'
REPORT_JSON = ROOT / 'docs' / 'AUDITORIA_VOZ_AUDIO_SYNC_2026-07-24.json'

VOICE_FILES = {
    'ive': ROOT / 'marca' / 'personas' / 'ive' / 'audio' / 'official_voice.wav',
    'alencar': ROOT / 'marca' / 'personas' / 'alencar' / 'audio' / 'official_voice.wav',
}


def ffprobe_meta(path: Path) -> dict:
    if not path.exists():
        return {'exists': False}
    cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'a:0',
        '-show_entries', 'stream=codec_name,sample_rate,channels:format=duration,size',
        '-of', 'json', str(path)
    ]
    try:
        data = json.loads(subprocess.check_output(cmd, text=True))
    except Exception:
        return {'exists': True, 'error': 'ffprobe_failed'}
    stream = (data.get('streams') or [{}])[0]
    fmt = data.get('format') or {}
    return {
        'exists': True,
        'codec': stream.get('codec_name'),
        'sample_rate': int(stream.get('sample_rate')) if stream.get('sample_rate') else None,
        'channels': stream.get('channels'),
        'duration_sec': round(float(fmt.get('duration', 0.0)), 2) if fmt.get('duration') else None,
        'size_bytes': int(fmt.get('size')) if fmt.get('size') else None,
    }


def parse_roteiro(md: Path) -> dict:
    txt = md.read_text(encoding='utf-8', errors='ignore')
    lines = txt.splitlines()
    title = ''
    slug = ''
    persona = ''
    voice = ''
    thumb = ''
    audio = ''
    for line in lines[:80]:
        if line.startswith('# '):
            title = line[2:].strip()
        m = re.search(r'\bslug:\s*([a-z0-9\-]+)', line, re.I)
        if m and not slug:
            slug = m.group(1)
        m = re.search(r'\*\*Persona:\*\*\s*([^\n]+)', line)
        if m and not persona:
            persona = m.group(1).strip().strip('*')
        m = re.search(r'\*\*Voice:\*\*\s*([^\n]+)', line)
        if m and not voice:
            voice = m.group(1).strip().strip('*')
        if ('thumb-' in line or 'capa-' in line) and not thumb:
            m = re.search(r'([A-Za-z0-9_\-]+\.(?:webp|png|jpg))', line)
            if m:
                thumb = m.group(1)
        if '.mp3' in line and not audio:
            m = re.search(r'([A-Za-z0-9_\-]+\.mp3)', line)
            if m:
                audio = m.group(1)
    return {
        'file': str(md.relative_to(ROOT)),
        'title': title,
        'slug': slug,
        'persona': persona,
        'voice_declared': voice,
        'thumb_ref': thumb,
        'audio_ref': audio,
    }


def canonical_voice_for(persona: str, voice_declared: str, file_name: str) -> Optional[str]:
    p = (persona or '').lower()
    vd = (voice_declared or '').lower()
    fn = file_name.lower()
    if 'ive' in p or 'eve' in vd or '-ive' in fn:
        return 'ive'
    if 'alencar' in p or 'james' in vd or '-alencar' in fn:
        return 'alencar'
    if 'dupla' in p or 'dupla' in fn:
        return 'dupla'
    return None


def find_render_candidates(prefix: str, folder: Path) -> list[str]:
    out = []
    if folder.exists():
        for ext in ('*.mp4',):
            for p in sorted(folder.glob(ext)):
                if prefix in p.name:
                    out.append(str(p.relative_to(ROOT)))
    return out


def audit_onda47() -> list[dict]:
    roteiros_dir = ROOT / 'videos' / 'aulas-onda-47' / 'roteiros'
    thumbs_dir = ROOT / 'videos' / 'aulas-onda-47' / 'thumbs'
    audios_dir = ROOT / 'videos' / 'aulas-onda-47' / 'audios'
    result = []
    for md in sorted(roteiros_dir.glob('*.md')):
        info = parse_roteiro(md)
        if not info['audio_ref']:
            slugish = md.stem
            info['audio_ref'] = f'{slugish}.mp3'
        if not info['thumb_ref']:
            info['thumb_ref'] = f"thumb-{md.stem}.webp"
        persona_key = canonical_voice_for(info['persona'], info['voice_declared'], md.name)
        expected_voice = []
        if persona_key == 'dupla':
            expected_voice = [str(VOICE_FILES['ive'].relative_to(ROOT)), str(VOICE_FILES['alencar'].relative_to(ROOT))]
        elif persona_key in VOICE_FILES:
            expected_voice = [str(VOICE_FILES[persona_key].relative_to(ROOT))]
        thumb_path = thumbs_dir / info['thumb_ref']
        audio_path = audios_dir / info['audio_ref']
        render_prefix = md.stem.replace('aula-', 'aula-')
        renders = find_render_candidates(render_prefix, ROOT / 'videos' / 'aulas-onda-47' / 'renders')
        item = {
            **info,
            'expected_canonical_voice_files': expected_voice,
            'thumb_exists': thumb_path.exists(),
            'thumb_path': str(thumb_path.relative_to(ROOT)),
            'audio_exists': audio_path.exists(),
            'audio_path': str(audio_path.relative_to(ROOT)),
            'audio_meta': ffprobe_meta(audio_path),
            'render_candidates': renders,
            'status': 'ok' if thumb_path.exists() and audio_path.exists() else 'broken',
        }
        result.append(item)
    return result


def audit_onda49() -> list[dict]:
    audios = ROOT / 'videos' / 'aulas-onda-49' / 'audios'
    renders = ROOT / 'videos' / 'aulas-onda-49' / 'renders'
    v2 = ROOT / 'videos' / 'aulas-onda-49' / 'v2'
    thumbs = ROOT / 'producao' / 'assets' / 'thumbnails'
    result = []
    for num in range(15, 34):
        prefix = f'aula-{num:02d}-'
        audio_dupla = sorted(audios.glob(f'{prefix}*-dupla.mp3'))
        audio_dupla_f = sorted(audios.glob(f'{prefix}*-dupla-F.mp3'))
        render_720 = sorted(renders.glob(f'{prefix}*-720p.mp4'))
        render_narr = sorted(renders.glob(f'{prefix}*-narrated.mp4'))
        render_v2 = sorted(v2.glob(f'{prefix}*-narrated-v2.mp4'))
        thumb = sorted(thumbs.glob(f'capa-{num:02d}-*.png'))
        result.append({
            'lesson': num,
            'audio_dupla': [str(p.relative_to(ROOT)) for p in audio_dupla],
            'audio_dupla_f': [str(p.relative_to(ROOT)) for p in audio_dupla_f],
            'render_720p': [str(p.relative_to(ROOT)) for p in render_720],
            'render_narrated': [str(p.relative_to(ROOT)) for p in render_narr],
            'render_v2': [str(p.relative_to(ROOT)) for p in render_v2],
            'master_cover': [str(p.relative_to(ROOT)) for p in thumb],
            'status': 'ok' if audio_dupla and audio_dupla_f and render_720 and render_narr and render_v2 and thumb else 'incomplete'
        })
    return result


def audit_docs_sync() -> dict:
    apostilas = sorted((ROOT / 'apostilas').glob('[0-9][0-9]-*.md'))
    html_primary = ROOT / 'html' / 'apostilas'
    html_secondary = ROOT / 'apostilas' / 'html'
    pdf_primary = ROOT / 'pdfs'
    pdf_secondary = ROOT / 'apostilas' / 'apostilas_pdf'
    checks = []
    for md in apostilas:
        stem = md.stem
        num = stem.split('-', 1)[0]
        html_hits = sorted(html_primary.glob(f'{num}-*.html')) + sorted(html_secondary.glob(f'{num}-*.html'))
        pdf_hits = sorted(pdf_primary.glob(f'{num}-*.pdf')) + sorted(pdf_secondary.glob(f'{num}-*.pdf'))
        ebook_hits = sorted((ROOT / 'docs' / 'ebooks').glob(f'ACAD-apostila-{num}-*.webp'))
        checks.append({
            'md': str(md.relative_to(ROOT)),
            'html_count': len(html_hits),
            'pdf_count': len(pdf_hits),
            'ebook_cover_count': len(ebook_hits),
            'status': 'ok' if html_hits and pdf_hits and ebook_hits else 'incomplete'
        })
    return {
        'items': checks,
        'ok_count': sum(1 for c in checks if c['status'] == 'ok'),
        'incomplete_count': sum(1 for c in checks if c['status'] != 'ok'),
    }


def main():
    voices = {k: ffprobe_meta(v) | {'path': str(v.relative_to(ROOT))} for k, v in VOICE_FILES.items()}
    onda47 = audit_onda47()
    onda49 = audit_onda49()
    docs_sync = audit_docs_sync()
    data = {
        'generated_on': '2026-07-24',
        'official_voices': voices,
        'onda47': onda47,
        'onda49': onda49,
        'docs_sync': docs_sync,
        'summary': {
            'onda47_ok': sum(1 for x in onda47 if x['status'] == 'ok'),
            'onda47_total': len(onda47),
            'onda49_ok': sum(1 for x in onda49 if x['status'] == 'ok'),
            'onda49_total': len(onda49),
            'docs_ok': docs_sync['ok_count'],
            'docs_total': len(docs_sync['items']),
        }
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    md = []
    md.append('# Auditoria de Voz, Áudio e Sincronização')
    md.append('')
    md.append('## Resumo executivo')
    md.append(f"- Onda 47: **{data['summary']['onda47_ok']}/{data['summary']['onda47_total']}** roteiros com thumb + áudio local presente.")
    md.append(f"- Onda 49: **{data['summary']['onda49_ok']}/{data['summary']['onda49_total']}** aulas com áudio dupla + dupla-F + renders 720p/narrated/v2 + master cover.")
    md.append(f"- Apostilas/HTML/PDF/Ebook cover: **{data['summary']['docs_ok']}/{data['summary']['docs_total']}** itens com cobertura completa por numeração.")
    md.append('')
    md.append('## Vozes oficiais canônicas')
    for k, meta in voices.items():
        md.append(f"- **{k}** → `{meta['path']}` · {meta.get('sample_rate')} Hz · {meta.get('channels')} canal(is) · {meta.get('duration_sec')} s")
    md.append('')
    md.append('## Onda 47 · sincronização roteiro / thumb / áudio / render')
    for item in onda47:
        md.append(f"- **{Path(item['file']).name}** — status `{item['status']}` · thumb `{item['thumb_ref']}` ({'ok' if item['thumb_exists'] else 'missing'}) · áudio `{item['audio_ref']}` ({'ok' if item['audio_exists'] else 'missing'}) · voz canônica esperada: {', '.join(item['expected_canonical_voice_files']) if item['expected_canonical_voice_files'] else 'não inferida'} · renders locais: {len(item['render_candidates'])}")
    md.append('')
    md.append('## Onda 49 · sincronização áudio / render / capa')
    for item in onda49:
        md.append(f"- **Aula {item['lesson']:02d}** — status `{item['status']}` · áudios dupla {len(item['audio_dupla'])} · áudios dupla-F {len(item['audio_dupla_f'])} · renders 720p {len(item['render_720p'])} · narrated {len(item['render_narrated'])} · v2 {len(item['render_v2'])} · capa master {len(item['master_cover'])}")
    md.append('')
    md.append('## Apostilas ↔ HTML ↔ PDF ↔ ebook cover')
    for item in docs_sync['items']:
        if item['status'] != 'ok':
            md.append(f"- **Pendência** `{item['md']}` — html={item['html_count']} pdf={item['pdf_count']} cover={item['ebook_cover_count']}")
    if docs_sync['incomplete_count'] == 0:
        md.append('- Nenhuma pendência estrutural por numeração encontrada nesta rodada.')
    REPORT_MD.write_text('\n'.join(md) + '\n', encoding='utf-8')
    print(REPORT_JSON.relative_to(ROOT))
    print(REPORT_MD.relative_to(ROOT))


if __name__ == '__main__':
    main()

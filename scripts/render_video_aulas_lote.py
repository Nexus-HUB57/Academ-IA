#!/usr/bin/env python3
"""Rebuild em lote dos video-aulas 00-14 do padrão Nexus AffilIA'te.

- Reutiliza capas aprovadas em producao/assets/thumbnails
- Reutiliza áudios legados (videos/audio/full_XX_persona.wav) como narração base
- Renderiza slides sintetizados a partir do manifesto operacional
- Compõe master 1280x720 @25fps H.264 + AAC
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path('/home/user/repo/Academ-IA')
MANIFEST_JSON = ROOT / 'docs' / 'MANIFESTO_REBUILD_VIDEO_AULAS_00_14_2026-07-24.json'
COVERS_DIR = ROOT / 'producao' / 'assets' / 'thumbnails'
LEGACY_AUDIO = ROOT / 'videos' / 'audio'

W, H = 1280, 720
BG = '#0A0F1E'
BG2 = '#12192D'
ACC = '#46B4C3'
GOLD = '#D7AF5A'
WHITE = '#F0F0F5'
MUTED = '#B4B4C3'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

f_title = ImageFont.truetype(FONT_B, 52)
f_sub = ImageFont.truetype(FONT, 24)
f_head = ImageFont.truetype(FONT_B, 32)
f_body = ImageFont.truetype(FONT, 26)
f_small = ImageFont.truetype(FONT, 20)
f_pill = ImageFont.truetype(FONT_B, 18)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def parse_slides(slides_md: Path):
    """Extrai lista de (titulo, subtitulo, bullets) do markdown de slides."""
    if not slides_md.exists():
        return []
    text = slides_md.read_text(encoding='utf-8', errors='ignore')
    blocks = []
    cur = None
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        low = s.lower()
        is_slide_header = (
            (low.startswith('slide ') and ':' in s)
            or ('slide' in low and s.startswith('#'))
            or ('slide' in low and '—' in s and (s.startswith('📍') or s.startswith('#')))
            or (s.startswith('##') and 'slide' in low)
        )
        if is_slide_header:
            if cur:
                blocks.append(cur)
            title = s.split(':', 1)[-1].strip() if ':' in s else s.lstrip('#').lstrip('📍').strip()
            title = title.replace('SLIDE', '').replace('slide', '').strip(' -—:0123456789')
            if not title:
                title = 'Slide'
            cur = {'title': title, 'sub': '', 'bullets': []}
        elif s.startswith('- ') or s.startswith('* '):
            if cur is None:
                cur = {'title': 'Slide', 'sub': '', 'bullets': []}
            cur['bullets'].append(s[2:].strip())
        elif s.startswith('#'):
            if cur is None:
                cur = {'title': s.lstrip('#').strip(), 'sub': '', 'bullets': []}
    if cur:
        blocks.append(cur)

    cleaned = []
    for b in blocks:
        title = b['title'].strip('*` ')
        bullets = [x for x in b['bullets'] if x][:5]
        if title.lower() in ('paleta de cores', '🎨 paleta de cores'):
            continue
        cleaned.append((title[:80], (bullets[0] if bullets else '')[:120], bullets[:5]))
        if len(cleaned) >= 10:
            break

    if len(cleaned) < 5:
        cleaned = cleaned + [('Nexus AcademIA', 'Trilha ativa', ['Padrão Nexus Affil’IA’te', 'Operação ponta a ponta', 'Produção contínua'])] * (5 - len(cleaned))
    return cleaned[:10]


def render_slide(idx, title, subtitle, bullets, trilha, cover_path, style='default'):
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)

    if style == 'cover' and cover_path and cover_path.exists():
        bg = Image.open(cover_path).convert('RGB').resize((W, H))
        img.paste(bg, (0, 0))
        overlay = Image.new('RGBA', (W, H), (10, 15, 30, 150))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 6], fill=ACC)
    d.rectangle([0, 0, 10, H], fill=ACC)
    d.rounded_rectangle([40, 28, 300, 64], radius=16, fill=BG2, outline=ACC, width=2)
    d.text((58, 38), f'TRILHA {trilha.upper()}', font=f_pill, fill=ACC)

    d.text((70, 96), title, font=f_title, fill=WHITE)

    if subtitle:
        sub_lines = wrap(d, subtitle, f_sub, W - 140)
        yy = 170
        for line in sub_lines[:2]:
            d.text((70, yy), line, font=f_sub, fill=MUTED)
            yy += 32

    yy = 260
    for b in bullets[:5]:
        d.ellipse([70, yy + 12, 82, yy + 24], fill=GOLD)
        blines = wrap(d, b, f_body, W - 180)
        for i, ln in enumerate(blines[:2]):
            d.text((100, yy + (i * 32)), ln, font=f_body, fill=WHITE)
        yy += max(60, 32 * min(len(blines), 2) + 20)
        if yy > H - 80:
            break

    d.rectangle([0, H - 44, W, H], fill=BG2)
    d.text((70, H - 34), 'oneverso.com.br/academia · @NexusAffilIAte', font=f_small, fill=MUTED)
    d.text((W - 230, H - 34), 'ACADEMIA NEXUS', font=f_pill, fill=GOLD)
    d.text((W - 60, 40), str(idx), font=f_pill, fill=ACC)
    return img


def ffprobe_duration(path: Path) -> float:
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'default=nw=1:nk=1', str(path)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def rebuild_module(mod):
    code = mod['code']
    title = mod['title']
    track = mod['track']
    trilha = {'fundamental': 'Fundamental', 'agente': 'Agente',
              'master': 'Master', 'elite': 'Elite'}[track]
    persona = mod['persona']
    cover = ROOT / mod['approved_cover']
    slides_md = ROOT / mod['slides_source']
    audio_src = ROOT / mod['legacy_audio']

    work = ROOT / mod['workspace_dir'] / 'rebuild'
    slides_dir = work / 'slides'
    segs_dir = work / 'segments'
    work.mkdir(parents=True, exist_ok=True)
    slides_dir.mkdir(parents=True, exist_ok=True)
    segs_dir.mkdir(parents=True, exist_ok=True)

    if not audio_src.exists():
        return {'code': code, 'ok': False, 'error': f'audio missing {audio_src}'}

    audio_dur = ffprobe_duration(audio_src)
    if audio_dur < 1:
        return {'code': code, 'ok': False, 'error': f'invalid audio duration'}

    slides_data = parse_slides(slides_md)
    n = len(slides_data)
    if n == 0:
        slides_data = [(title, '', ['Nexus AcademIA', 'Padrão Nexus AffilIA’te'])] * 5
        n = 5

    total = audio_dur + 0.4
    per_slide = max(5.0, total / n)
    durations = [per_slide] * n
    diff = total - sum(durations)
    durations[-1] = max(3.0, durations[-1] + diff)

    slide_files = []
    for i, (st, ss, bl) in enumerate(slides_data, start=1):
        style = 'cover' if i == 1 else 'default'
        st_show = st if i > 1 else title
        img = render_slide(i, st_show, ss, bl, trilha, cover, style=style)
        p = slides_dir / f'slide_{i:02d}.png'
        img.save(p, 'PNG')
        slide_files.append(p)

    for i, (p, dur) in enumerate(zip(slide_files, durations), start=1):
        seg = segs_dir / f'seg_{i:02d}.mp4'
        d_safe = max(3.0, float(dur))
        cmd = ['ffmpeg', '-y', '-loop', '1', '-framerate', '25', '-t', f'{d_safe:.2f}', '-i', str(p),
               '-vf', 'fps=25,format=yuv420p,scale=1280:720',
               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22',
               '-pix_fmt', 'yuv420p', '-t', f'{d_safe:.2f}', str(seg)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            return {'code': code, 'ok': False, 'error': f'seg{i} failed: {r.stderr[-300:]}'}

    concat_txt = work / 'segments_concat.txt'
    concat_txt.write_text('\n'.join([f"file '{segs_dir / f'seg_{i:02d}.mp4'}'" for i in range(1, n + 1)]), encoding='utf-8')
    silent = work / f'video_{code}_silent.mp4'
    r = subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                        '-i', str(concat_txt), '-c', 'copy', str(silent)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return {'code': code, 'ok': False, 'error': f'concat: {r.stderr[-300:]}'}

    final_name = f"video-{code}-{mod['workspace_dir'].split('/')[-1]}-master.mp4"
    final = work / final_name
    r = subprocess.run(['ffmpeg', '-y', '-i', str(silent), '-i', str(audio_src),
                        '-map', '0:v:0', '-map', '1:a:0',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                        '-ar', '44100', '-ac', '2', '-shortest',
                        '-movflags', '+faststart', str(final)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return {'code': code, 'ok': False, 'error': f'mux: {r.stderr[-300:]}'}

    dur = ffprobe_duration(final)
    manifest = {
        'code': code,
        'title': title,
        'track': track,
        'persona': persona,
        'final_video': final_name,
        'duration_s': round(dur, 2),
        'slides_count': n,
        'audio_source': str(audio_src.relative_to(ROOT)),
        'cover': str(cover.relative_to(ROOT)),
        'thumb': mod['approved_thumb'],
        'youtube_description': mod['youtube_description'],
        'render_spec': '1280x720@25fps H.264 + AAC 192k',
    }
    (work / 'rebuild_manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    return {'code': code, 'ok': True, 'duration_s': round(dur, 2), 'file': str(final.relative_to(ROOT)), 'slides': n}


def main():
    data = json.loads(MANIFEST_JSON.read_text(encoding='utf-8'))
    modules = data['modules']
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    results = []
    for mod in modules:
        if only and mod['code'] not in only:
            continue
        print(f"[{mod['code']}] {mod['title']} ...", flush=True)
        try:
            r = rebuild_module(mod)
        except Exception as e:
            r = {'code': mod['code'], 'ok': False, 'error': str(e)}
        results.append(r)
        print(f"  -> {r}", flush=True)
    (ROOT / 'docs' / 'REBUILD_LOTE_RESULTADO_2026-07-25.json').write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

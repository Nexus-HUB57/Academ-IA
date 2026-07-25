#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path('/home/user/repo/Academ-IA')
MOD = ROOT / 'materiais' / 'video-aulas' / 'fundamental' / '00-boas-vindas'
OUT = MOD / 'rebuild'
SLIDES = OUT / 'slides'
OUT.mkdir(parents=True, exist_ok=True)
SLIDES.mkdir(parents=True, exist_ok=True)

W, H = 1280, 720
BG = '#0A0F1E'
BG2 = '#12192D'
ACC = '#46B4C3'
GOLD = '#D7AF5A'
WHITE = '#F0F0F5'
MUTED = '#B4B4C3'
OK = '#6EE7B7'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

SCENES = [
    (1, 21.36, 'Boas-vindas à Nexus AcademIA', 'Sir Nexus Alencar apresenta a trilha fundamental e o início da jornada.', ['Marketing Multinível com IA', 'Visão operacional', 'Primeiro passo da trilha']),
    (2, 32.00, 'O que é a Nexus?', 'Uma plataforma de afiliados potencializada por IA distribuída.', ['Plataforma de afiliados', 'IA distribuída', 'Nós autônomos e conectados', 'Ecossistema federado']),
    (3, 27.96, 'Anatomia do Ecossistema', 'As 5 camadas que sustentam toda a operação Nexus.', ['Camada 5: AcademIA', 'Camada 4: Marketplace de Skills', 'Camada 3: Agentes', 'Camada 2: IOAID', 'Camada 1: SHO']),
    (4, 47.48, 'Os 3 Pilares', 'Autonomia, resiliência e federação como base da escala.', ['Autonomia: 70% a 90% das tarefas', 'Resiliência: sistema auto-curável', 'Federação: skills e comunidade']),
    (5, 38.24, 'Próximos 30 Dias', 'Plano de execução para sair da teoria e entrar na operação.', ['Semana 1: configurar painel e produto', 'Semana 2: criar primeiro agente', 'Semana 3: disparos de teste', 'Semana 4: avaliar, ajustar e escalar']),
    (6, 43.48, 'Os 5 Mandamentos', 'Regras para crescer sem travar a operação.', ['Nunca desative o Judge', 'Comece pequeno', 'Meça tudo', 'Copie o que funciona', 'Peça ajuda antes de travar']),
    (7, 28.40, 'Recursos e Suporte', 'Materiais e canais para avançar com segurança.', ['Apostilas detalhadas', 'Cursos da AcademIA', 'Comunidade e tickets', 'Leve request_id, prints e contexto']),
    (8, 22.68, 'Seu Próximo Passo', 'Continue com o módulo 01 e mantenha a consistência da operação.', ['Próximo curso: Entendendo o IOAID', 'Avance com método', 'Escale com clareza']),
]

cover = ROOT / 'producao' / 'assets' / 'thumbnails' / 'capa-00-boas-vindas-ive.png'
thumb = ROOT / 'producao' / 'assets' / 'thumbnails' / 'thumb-00-boas-vindas.png'
persona = ROOT / 'marca' / 'personas' / 'alencar' / 'assets' / 'alencar_reference.png'
audios = [ROOT / 'cursos' / 'fundamental' / f'00-boas-vindas-cena{i}.wav' for i in range(1, 8)]

f_title = ImageFont.truetype(FONT_B, 54)
f_sub = ImageFont.truetype(FONT, 26)
f_head = ImageFont.truetype(FONT_B, 34)
f_body = ImageFont.truetype(FONT, 28)
f_small = ImageFont.truetype(FONT, 22)
f_pill = ImageFont.truetype(FONT_B, 20)


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


def paste_contain(base, img, box):
    x, y, bw, bh = box
    iw, ih = img.size
    scale = min(bw / iw, bh / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh))
    ox = x + (bw - nw) // 2
    oy = y + (bh - nh) // 2
    base.paste(img, (ox, oy), img if img.mode == 'RGBA' else None)


def render_slide(idx, title, subtitle, bullets, style='default'):
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 6], fill=ACC)
    d.rectangle([0, 0, 10, H], fill=ACC)
    d.rounded_rectangle([40, 28, 220, 64], radius=16, fill=BG2, outline=ACC, width=2)
    d.text((58, 38), 'TRILHA FUNDAMENTAL', font=f_pill, fill=ACC)
    d.text((70, 100), title, font=f_title, fill=WHITE)

    if style == 'cover':
        bg = Image.open(cover).convert('RGB').resize((W, H))
        img.paste(bg, (0, 0))
        overlay = Image.new('RGBA', (W, H), (10, 15, 30, 145))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, W, 6], fill=ACC)
        d.rectangle([0, 0, 10, H], fill=ACC)
        d.rounded_rectangle([44, 30, 240, 68], radius=18, fill=(18, 25, 45), outline=ACC, width=2)
        d.text((62, 40), 'ACADEMIA NEXUS', font=f_pill, fill=ACC)
        d.text((70, 110), title, font=f_title, fill=WHITE)
        sub_lines = wrap(d, subtitle, f_sub, 560)
        yy = 190
        for line in sub_lines:
            d.text((70, yy), line, font=f_sub, fill=WHITE)
            yy += 34
        d.text((70, yy + 20), 'Sir Nexus Alencar', font=f_head, fill=GOLD)
        d.text((70, H - 60), 'oneverso.com.br/academia  ·  @NexusAffilIAte', font=f_small, fill=WHITE)
        return img

    if style == 'closing':
        bg = Image.open(thumb).convert('RGB').resize((W, H))
        img.paste(bg, (0, 0))
        overlay = Image.new('RGBA', (W, H), (10, 15, 30, 155))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, W, 6], fill=ACC)
        d.text((70, 105), title, font=f_title, fill=WHITE)
        lines = wrap(d, subtitle, f_sub, 700)
        yy = 190
        for line in lines:
            d.text((70, yy), line, font=f_sub, fill=WHITE)
            yy += 34
        for i, bullet in enumerate(bullets):
            d.ellipse((74, yy + i * 44 + 8, 88, yy + i * 44 + 22), fill=OK)
            d.text((102, yy + i * 44), bullet, font=f_body, fill=WHITE)
        d.rounded_rectangle([70, H - 120, 550, H - 70], radius=14, outline=GOLD, width=3)
        d.text((92, H - 108), 'Próximo curso: 01 · Entendendo o IOAID', font=f_sub, fill=GOLD)
        d.text((70, H - 55), 'oneverso.com.br/academia  ·  @NexusAffilIAte', font=f_small, fill=WHITE)
        return img

    d.text((70, 175), subtitle, font=f_sub, fill=MUTED)
    if idx in (2, 3, 4):
        # small persona portrait on informative slides
        if persona.exists():
            p = Image.open(persona).convert('RGBA')
            paste_contain(img, p, (905, 110, 290, 360))
            d.rounded_rectangle([900, 105, 1200, 475], radius=20, outline=ACC, width=2)
    yy = 245
    maxw = 760 if idx in (2, 3, 4) else 1040
    for bullet in bullets:
        lines = wrap(d, bullet, f_body, maxw)
        d.ellipse((74, yy + 10, 88, yy + 24), fill=ACC)
        d.text((102, yy), lines[0], font=f_body, fill=WHITE)
        yy += 38
        for cont in lines[1:]:
            d.text((102, yy), cont, font=f_body, fill=WHITE)
            yy += 34
        yy += 12
    d.text((70, H - 52), 'oneverso.com.br/academia  ·  @NexusAffilIAte', font=f_small, fill=WHITE)
    d.text((W - 320, H - 52), 'ACADEM IA NEXUS', font=f_small, fill=MUTED)
    return img


slide_files = []
for idx, dur, title, subtitle, bullets in SCENES:
    style = 'default'
    if idx == 1:
        style = 'cover'
    elif idx == 8:
        style = 'closing'
    img = render_slide(idx, title, subtitle, bullets, style=style)
    out = SLIDES / f'slide_{idx:02d}.png'
    img.save(out)
    slide_files.append((out, dur))

# concat audio scenes
alist = OUT / 'audio_concat.txt'
alist.write_text(''.join([f"file '{p.as_posix()}'\n" for p in audios]), encoding='utf-8')
audio_out = OUT / 'rebuild_00_narracao_ptbr.wav'
subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(alist), '-c', 'copy', str(audio_out)], check=True)

# slideshow em segmentos para reduzir uso de memória
segments = OUT / 'segments'
segments.mkdir(exist_ok=True)
seg_list = OUT / 'segments_concat.txt'
with seg_list.open('w', encoding='utf-8') as f:
    for idx, (p, dur) in enumerate(slide_files, 1):
        seg = segments / f'seg_{idx:02d}.mp4'
        subprocess.run([
            'ffmpeg', '-y', '-loop', '1', '-i', str(p), '-t', f'{dur:.2f}',
            '-vf', 'fps=25,format=yuv420p', '-pix_fmt', 'yuv420p',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
            '-an', str(seg)
        ], check=True)
        f.write(f"file '{seg.as_posix()}'\n")

silent = OUT / 'video_00_slides_silent.mp4'
subprocess.run([
    'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(seg_list),
    '-c', 'copy', str(silent)
], check=True)

final = OUT / 'video-00-boas-vindas-a-academia-nexus-master.mp4'
subprocess.run([
    'ffmpeg', '-y', '-i', str(silent), '-i', str(audio_out),
    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '32000', '-ac', '1',
    '-shortest', '-movflags', '+faststart', str(final)
], check=True)

source_cover_rel = str(cover.relative_to(ROOT))
manifest = {
    'module': '00',
    'title': 'Boas-vindas à AcademIA Nexus',
    'target_duration_s': 261,
    'slides': [p.name for p, _ in slide_files],
    'audio_master': audio_out.name,
    'final_video': final.name,
    'source_cover': source_cover_rel,
    'audio_duration_s': 261.6,
    'status': 'master_renderizado',
}
(OUT / 'rebuild_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(manifest, ensure_ascii=False, indent=2))

#!/usr/bin/env python3
"""Renderiza os slides oficiais do Módulo 00 · Boas-vindas à AcademIA Nexus.

- Fundo escuro Nexus (#0B1220) com faixa turquesa (#22D3EE).
- Badge "TRILHA FUNDAMENTAL", numeração de slide no topo direito.
- Rodapé "oneverso.com.br/academia · @NexusAffilIAte" à esquerda,
  "ACADEMIA NEXUS" à direita.
- Consome o texto oficial dos 8 slides do módulo 00 (sem marcadores).
- Saída: 1920x1080 PNG em <rebuild>/slides_premium/ e master MP4 em <rebuild>/.

Executa em qualquer runner Linux com Pillow + ffmpeg.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
REBUILD = ROOT / 'materiais' / 'video-aulas' / 'fundamental' / '00-boas-vindas' / 'rebuild'
SLIDES_DIR = REBUILD / 'slides_premium'
SLIDES_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1920, 1080
BG = (11, 18, 32)              # #0B1220
BG_STRIP = (16, 26, 48)        # #101A30
ACCENT = (34, 211, 238)        # #22D3EE
ACCENT_SOFT = (14, 165, 233)   # #0EA5E9
GOLD = (250, 204, 21)          # #FACC15 - bullets
TEXT = (241, 245, 249)         # #F1F5F9
TEXT_DIM = (148, 163, 184)     # #94A3B8

FONTS = {
    'display': '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
    'text':    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    'mono':    '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf',
}


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONTS[kind], size)


SLIDES = [
    {
        'kicker': 'MÓDULO 00 · BOAS-VINDAS',
        'title': 'Boas-vindas à AcademIA Nexus',
        'subtitle': 'apresentado por Sir Nexus Alencar',
        'body': [
            'Seu primeiro passo dentro do ecossistema Nexus Affil\u02BCIA\u02BCte.',
            'Aqui você entende a filosofia, a arquitetura e o caminho até o resultado.',
        ],
    },
    {
        'kicker': 'O QUE É A NEXUS',
        'title': 'Uma plataforma de afiliados potencializada por IA distribuída',
        'body': [
            'Cada nó da rede é autônomo, auto-curável e conectado aos outros.',
            'Plataforma de afiliados nativa de IA.',
            'Inteligência distribuída em federação.',
            'Nó autônomo, resiliente e observável.',
        ],
    },
    {
        'kicker': 'ANATOMIA DO ECOSSISTEMA',
        'title': 'As 5 camadas do ecossistema Nexus',
        'body': [
            'Camada 5 — AcademIA (o HUB de conhecimento).',
            'Camada 4 — Marketplace de Skills.',
            'Camada 3 — Agentes (seu nó operacional).',
            'Camada 2 — IOAID (infraestrutura de IA distribuída).',
            'Camada 1 — SHO (sistema imunológico auto-curável).',
        ],
    },
    {
        'kicker': 'OS 3 PILARES',
        'title': 'O que sustenta tudo',
        'body': [
            'Autonomia — agentes cuidam de 70% a 90% da operação.',
            'Resiliência — o SHO fecha loops de falha automaticamente.',
            'Federação — skills compartilhadas em comunidade colaborativa.',
        ],
    },
    {
        'kicker': 'PRÓXIMOS 30 DIAS',
        'title': 'Seu caminho para o primeiro resultado',
        'body': [
            'Semana 1 — configurar painel e escolher 1 produto.',
            'Semana 2 — criar seu primeiro agente de IA.',
            'Semana 3 — realizar o primeiro disparo de teste.',
            'Semana 4 — avaliar, ajustar e escalar.',
            'Meta 30 dias — 1 venda, 1 agente rodando, 300+ contatos.',
        ],
    },
    {
        'kicker': 'OS 5 MANDAMENTOS',
        'title': 'Regras do afiliado Nexus',
        'body': [
            '1. Nunca desative o Judge.',
            '2. Comece pequeno.',
            '3. Meça tudo.',
            '4. Copie o que funciona.',
            '5. Peça ajuda antes de travar.',
        ],
    },
    {
        'kicker': 'RECURSOS E SUPORTE',
        'title': 'Como pedir ajuda com precisão',
        'body': [
            'Recursos — apostilas oficiais e trilhas da AcademIA.',
            'Suporte — comunidade Slack, sistema de tickets e suporte dedicado.',
            'Para pedir ajuda, envie request_id, print do erro e uma descrição curta.',
        ],
    },
    {
        'kicker': 'PRÓXIMO PASSO',
        'title': 'Este foi o primeiro passo',
        'body': [
            'A introdução ao potencial da Nexus Affil\u02BCIA\u02BCte foi entregue.',
            'Próximo curso — 01 · Entendendo o IOAID.',
            'Vamos construir juntos, com método, um futuro de resultado.',
        ],
    },
]


def wrap(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    if not words:
        return ['']
    lines: list[str] = []
    cur = words[0]
    for word in words[1:]:
        trial = cur + ' ' + word
        w = draw.textlength(trial, font=font_obj)
        if w <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def draw_frame(idx: int, total: int) -> Path:
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)

    # Faixa lateral esquerda turquesa
    d.rectangle([(0, 0), (14, H)], fill=ACCENT)
    # Barra superior sutil
    d.rectangle([(0, 0), (W, 6)], fill=ACCENT_SOFT)

    # Badge TRILHA FUNDAMENTAL
    badge_font = font('mono', 22)
    badge_txt = 'TRILHA FUNDAMENTAL'
    bx, by = 72, 60
    bw = int(d.textlength(badge_txt, font=badge_font)) + 48
    bh = 42
    d.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=21, outline=ACCENT, width=2)
    d.text((bx + 24, by + 8), badge_txt, font=badge_font, fill=ACCENT)

    # Numeração topo direito
    num_font = font('display', 34)
    num_txt = f'{idx:02d}/{total:02d}'
    tw = d.textlength(num_txt, font=num_font)
    d.text((W - 96 - tw, 58), num_txt, font=num_font, fill=TEXT_DIM)

    # Kicker
    kicker_font = font('mono', 26)
    kicker = SLIDES[idx - 1]['kicker']
    d.text((72, 156), kicker, font=kicker_font, fill=ACCENT)
    # Linha decorativa sob o kicker
    kw = d.textlength(kicker, font=kicker_font)
    d.rectangle([(72, 196), (72 + int(kw), 200)], fill=ACCENT)

    # Título
    title_font = font('display', 72)
    title = SLIDES[idx - 1]['title']
    max_title_w = W - 144
    lines = wrap(d, title, title_font, max_title_w)
    ty = 244
    for line in lines:
        d.text((72, ty), line, font=title_font, fill=TEXT)
        ty += 82

    # Subtítulo opcional
    subtitle = SLIDES[idx - 1].get('subtitle')
    if subtitle:
        sub_font = font('text', 34)
        d.text((72, ty + 8), subtitle, font=sub_font, fill=TEXT_DIM)
        ty += 60

    # Corpo (bullets)
    body_font = font('text', 34)
    body = SLIDES[idx - 1]['body']
    by = ty + 40
    bullet_r = 8
    for para in body:
        wrapped = wrap(d, para, body_font, W - 200)
        # bolinha dourada
        d.ellipse([(84, by + 20), (84 + bullet_r * 2, by + 20 + bullet_r * 2)], fill=GOLD)
        # linhas do parágrafo
        lx = 84 + bullet_r * 2 + 24
        for i, ln in enumerate(wrapped):
            d.text((lx, by + i * 44), ln, font=body_font, fill=TEXT)
        by += len(wrapped) * 44 + 22

    # Rodapé
    footer_font = font('text', 24)
    d.rectangle([(0, H - 88), (W, H - 84)], fill=ACCENT_SOFT)
    d.rectangle([(0, H - 84), (W, H)], fill=BG_STRIP)
    d.text((72, H - 60), 'oneverso.com.br/academia · @NexusAffilIAte', font=footer_font, fill=TEXT_DIM)
    right = 'ACADEMIA NEXUS'
    rw = d.textlength(right, font=footer_font)
    d.text((W - 72 - rw, H - 60), right, font=footer_font, fill=ACCENT)

    out = SLIDES_DIR / f'slide_{idx:02d}.png'
    img.save(out, 'PNG', optimize=True)
    return out


def render_slides() -> list[Path]:
    outs = []
    total = len(SLIDES)
    for i in range(1, total + 1):
        outs.append(draw_frame(i, total))
    return outs


def build_video(narration: Path, out_mp4: Path) -> dict:
    """Junta os slides em um vídeo 1920x1080 25fps AAC 192k com a narração.

    Estratégia leve em RAM: gera 1 clipe por slide com -loop 1 e duração exata,
    depois concatena por copy. Evita expandir todos os frames em memória.
    """
    total_dur = 261.6
    n = len(SLIDES)
    weights = [1.0, 1.2, 1.4, 1.2, 1.4, 1.2, 1.1, 1.0]
    ws = sum(weights)
    durs = [round(total_dur * w / ws, 3) for w in weights]
    delta = round(total_dur - sum(durs), 3)
    durs[-1] = round(durs[-1] + delta, 3)

    clips_dir = REBUILD / 'clips_premium'
    clips_dir.mkdir(parents=True, exist_ok=True)
    clip_paths: list[Path] = []
    for i, dur in enumerate(durs, 1):
        slide = SLIDES_DIR / f'slide_{i:02d}.png'
        clip = clips_dir / f'clip_{i:02d}.mp4'
        subprocess.run([
            'ffmpeg', '-y', '-loop', '1', '-framerate', '25', '-i', str(slide),
            '-t', f'{dur:.3f}',
            '-vf', 'format=yuv420p',
            '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'stillimage',
            '-crf', '22', '-x264-params', 'keyint=50:min-keyint=25:threads=1',
            '-r', '25',
            str(clip),
        ], check=True)
        clip_paths.append(clip)

    concat = REBUILD / 'concat_premium.txt'
    concat.write_text('\n'.join(f"file '{c.as_posix()}'" for c in clip_paths) + '\n', encoding='utf-8')

    silent_mp4 = REBUILD / 'video_00_premium_silent.mp4'
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat),
        '-c', 'copy', str(silent_mp4),
    ], check=True)

    subprocess.run([
        'ffmpeg', '-y', '-i', str(silent_mp4), '-i', str(narration),
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
        '-shortest', str(out_mp4)
    ], check=True)

    return {
        'video': str(out_mp4),
        'silent': str(silent_mp4),
        'concat_manifest': str(concat),
        'durations': durs,
        'clips': [str(c) for c in clip_paths],
    }


def main():
    slides = render_slides()
    print(json.dumps({'slides': [str(p) for p in slides]}, ensure_ascii=False))
    narration = REBUILD / 'rebuild_00_narracao_ptbr.wav'
    if not narration.exists():
        raise SystemExit(f'narration_missing: {narration}')
    out_mp4 = REBUILD / 'video-00-boas-vindas-a-academia-nexus-master.mp4'
    result = build_video(narration, out_mp4)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()

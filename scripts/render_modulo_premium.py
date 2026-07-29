#!/usr/bin/env python3
"""Renderizador premium genérico para os módulos oficiais AcademIA Nexus.

Uso:
    python3 scripts/render_modulo_premium.py <codigo>

Onde <codigo> ∈ {00, 01, 02, ...}. Cada módulo tem seu conteúdo pré-definido
em MODULES abaixo, já sem marcadores literais do briefing.

Saída:
    materiais/video-aulas/fundamental/<slug>/rebuild/slides_premium/slide_NN.png
    materiais/video-aulas/fundamental/<slug>/rebuild/video-<video-name>-master.mp4
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]

W, H = 1920, 1080
BG = (11, 18, 32)
BG_STRIP = (16, 26, 48)
ACCENT = (34, 211, 238)
ACCENT_SOFT = (14, 165, 233)
GOLD = (250, 204, 21)
TEXT = (241, 245, 249)
TEXT_DIM = (148, 163, 184)

FONTS = {
    'display': '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
    'text':    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    'mono':    '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf',
}


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONTS[kind], size)


MODULES: dict[str, dict] = {
    '00': {
        'slug': '00-boas-vindas',
        'video_name': 'video-00-boas-vindas-a-academia-nexus-master.mp4',
        'narration': 'rebuild_00_narracao_ptbr.wav',
        'total_dur': 261.6,
        'weights': [1.0, 1.2, 1.4, 1.2, 1.4, 1.2, 1.1, 1.0],
        'header': 'MÓDULO 00 · BOAS-VINDAS',
        'slides': [
            {
                'kicker': 'MÓDULO 00 · BOAS-VINDAS',
                'title': 'Boas-vindas à AcademIA Nexus',
                'subtitle': 'apresentado por Sir Nexus Alencar',
                'body': [
                    'Seu primeiro passo dentro do ecossistema Nexus Affil\u02BCIA\u02BCte.',
                    'Aqui você entende a filosofia, a arquitetura e o caminho até o resultado.',
                ],
            },
        ],
    },
    '01': {
        'slug': '01-entendendo-ioaid',
        'video_name': 'video-01-01-entendendo-ioaid-master.mp4',
        'narration': 'rebuild_01_narracao_ptbr.mp3',
        'total_dur': 118.728,
        'weights': [1.0, 1.1, 1.0, 1.3, 1.4, 1.1, 1.0, 1.2, 1.0],
        'header': 'MÓDULO 01 · FUNDAMENTOS',
        'slides': [
            {
                'kicker': 'MÓDULO 01 · FUNDAMENTOS',
                'title': 'Entendendo o IOAID',
                'subtitle': 'A infraestrutura invisível do Nexus Affil\u02BCIA\u02BCte',
                'body': [
                    'O coração técnico que orquestra toda a inteligência da rede.',
                    'Guia: Sir Nexus Alencar, especialista técnico.',
                ],
            },
            {
                'kicker': 'IOAID EM UMA FRASE',
                'title': 'Da intenção à ação, com controle',
                'body': [
                    'IOAID recebe sua intenção operacional e a executa de forma segura.',
                    'Auditável — você sabe exatamente o que foi feito.',
                    'Escalável — funciona igual bem para 10 ou 10.000 contatos.',
                    'Reversível — ações problemáticas podem ser desfeitas.',
                ],
            },
            {
                'kicker': 'POR QUE DISTRIBUÍDA',
                'title': 'A força da arquitetura distribuída',
                'body': [
                    'Sem ponto único de falha — resiliência garantida.',
                    'Latência local — resposta em menos de 2 s para 95% das ações.',
                    'Privacidade — seus dados permanecem sob o seu controle.',
                    'Escala horizontal — mais afiliados significam mais capacidade.',
                ],
            },
            {
                'kicker': 'ANATOMIA DO IOAID',
                'title': 'Os 5 módulos que sustentam a operação',
                'body': [
                    'M1 · Ingestion — recepção e validação de requisições.',
                    'M2 · Routing — roteamento inteligente entre agentes e skills.',
                    'M3 · Execution — execução isolada em sandbox seguro.',
                    'M4 · Persistence — registro completo e auditável de operações.',
                    'M5 · Response — devolução do resultado com metadados.',
                ],
            },
            {
                'kicker': 'FLUXO DE UMA REQUISIÇÃO',
                'title': 'Do clique à ação em ~14 s para 800 mensagens',
                'body': [
                    'Clique em Disparar Natal na sua operação.',
                    'Ingestion recebe e valida a intenção.',
                    'Routing encadeia segmenter, personalizer e sender.',
                    'Execution filtra, personaliza e enfileira as mensagens.',
                    'Judge Revisor avalia cada mensagem antes do envio.',
                    'Persistence registra o histórico. Response devolve o resultado.',
                ],
            },
            {
                'kicker': 'JUDGE REVISOR',
                'title': 'O guardião da conformidade',
                'body': [
                    'LLM auxiliar que revisa cada saída antes de virar ação.',
                    'Alcance: mensagens de WhatsApp, outputs de skill e decisões críticas.',
                    'Três níveis — verde aprovado, amarelo alerta, vermelho bloqueado.',
                ],
            },
            {
                'kicker': 'AUTENTICAÇÃO E SEGURANÇA',
                'title': 'Três camadas protegem sua operação',
                'body': [
                    'API Token para chamadas autenticadas do afiliado.',
                    'mTLS entre nós federados da rede Nexus.',
                    'Rate Limit de 60 requisições por minuto.',
                    'Boa prática — nunca compartilhe token, use um por ambiente e revogue os antigos.',
                ],
            },
            {
                'kicker': 'IMPACTO NA OPERAÇÃO',
                'title': 'Cinco benefícios diretos para você',
                'body': [
                    'Confiabilidade — SLA operacional de 99,7%.',
                    'Escalabilidade — ajuste automático conforme volume.',
                    'Auditabilidade — cada ação fica registrada.',
                    'Reversibilidade — operações problemáticas podem ser desfeitas.',
                    'Observabilidade — dashboards em tempo real para acompanhar tudo.',
                ],
            },
            {
                'kicker': 'PRÓXIMO PASSO',
                'title': 'Sua jornada continua no Módulo 02',
                'body': [
                    'Próximo curso — 02 · Sistema SHO, o sistema imunológico da operação.',
                    'Recursos extras — Apostila 01 Apresentação da Infraestrutura e Apostila 03 Infraestrutura Operacional de IA.',
                ],
            },
        ],
    },
    '02': {
        'slug': '02-sistema-sho',
        'video_name': 'video-02-02-sistema-sho-master.mp4',
        'narration': 'rebuild_02_narracao_ptbr.mp3',
        'total_dur': 123.624,
        'weights': [1.0, 1.1, 1.2, 1.3, 1.2, 1.2, 1.1, 1.0],
        'header': 'MÓDULO 02 · FUNDAMENTOS',
        'slides': [
            {
                'kicker': 'MÓDULO 02 · FUNDAMENTOS',
                'title': 'Sistema SHO — o guardião da sua operação',
                'subtitle': 'Resiliência e autonomia no Nexus Affil\u02BCIA\u02BCte',
                'body': [
                    'Depois do IOAID, agora o sistema imunológico da infraestrutura.',
                    'Guia: Sir Nexus Alencar.',
                ],
            },
            {
                'kicker': 'SHO EM UMA FRASE',
                'title': 'Monitorar, detectar e reagir com precisão',
                'body': [
                    'O SHO monitora cada execução e detecta anomalias.',
                    'Toma ações defensivas autonomamente na maioria dos casos.',
                    'Orquestrador determinístico — não alucina, reage por regras claras.',
                ],
            },
            {
                'kicker': 'POR QUE HÍBRIDO',
                'title': 'Três modos de decisão convivendo',
                'body': [
                    'Modo reativo — age imediatamente a falhas ou reprovações do Judge.',
                    'Modo preditivo — antecipa problemas antes que ocorram.',
                    'Modo consultivo — pede intervenção humana em cenários complexos.',
                    'Rápido quando precisa, preventivo quando dá, humilde quando exige.',
                ],
            },
            {
                'kicker': 'MODOS DE OPERAÇÃO',
                'title': 'Verde, amarelo e vermelho da sua operação',
                'body': [
                    'Saturação (verde) — operação normal, registro contínuo.',
                    'Contenção (amarelo) — isola o problema, redireciona tráfego, alerta visual.',
                    'Quarentena (vermelho) — bloqueia novas execuções e abre ticket para humano.',
                    'Transições automáticas e totalmente auditáveis.',
                ],
            },
            {
                'kicker': 'ANATOMIA DE UMA DECISÃO',
                'title': 'As métricas que o SHO observa',
                'body': [
                    'Latência das execuções.',
                    'Taxa de erro por skill.',
                    'Custo em tokens.',
                    'Taxa de aprovação do Judge.',
                    'Latência de APIs externas.',
                    'Critério — dois ou mais critérios de anomalia disparados juntos.',
                ],
            },
            {
                'kicker': 'SHO E JUDGE',
                'title': 'Responsabilidades distintas, proteção conjunta',
                'body': [
                    'Judge — decide se uma ação específica é aprovada.',
                    'SHO — avalia a saúde geral da skill que gerou a ação.',
                    'Se o Judge reprova muitas ações de uma skill, o SHO coloca em contenção.',
                    'Sem interferir na decisão individual do Judge.',
                ],
            },
            {
                'kicker': 'ESCALADA HUMANA',
                'title': 'O limite consciente da autonomia',
                'body': [
                    'SHO lida com anomalias operacionais em tempo real.',
                    'Humanos lidam com valores éticos, compliance e decisões estratégicas.',
                    'A inteligência final e a responsabilidade permanecem com você.',
                ],
            },
            {
                'kicker': 'PRÓXIMO PASSO',
                'title': 'Sua jornada continua no Módulo 03',
                'body': [
                    'Próximo curso — 03 · Painel do Afiliado, a central de comando da operação.',
                    'IOAID + SHO formam a base técnica que sustenta todo o resto.',
                ],
            },
        ],
    },
}


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


def draw_frame(mod: dict, idx: int, total: int, out_dir: Path) -> Path:
    slide = mod['slides'][idx - 1]
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([(0, 0), (14, H)], fill=ACCENT)
    d.rectangle([(0, 0), (W, 6)], fill=ACCENT_SOFT)

    badge_font = font('mono', 22)
    badge_txt = 'TRILHA FUNDAMENTAL'
    bx, by = 72, 60
    bw = int(d.textlength(badge_txt, font=badge_font)) + 48
    bh = 42
    d.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=21, outline=ACCENT, width=2)
    d.text((bx + 24, by + 8), badge_txt, font=badge_font, fill=ACCENT)

    num_font = font('display', 34)
    num_txt = f'{idx:02d}/{total:02d}'
    tw = d.textlength(num_txt, font=num_font)
    d.text((W - 96 - tw, 58), num_txt, font=num_font, fill=TEXT_DIM)

    kicker_font = font('mono', 26)
    kicker = slide['kicker']
    d.text((72, 156), kicker, font=kicker_font, fill=ACCENT)
    kw = d.textlength(kicker, font=kicker_font)
    d.rectangle([(72, 196), (72 + int(kw), 200)], fill=ACCENT)

    title_font = font('display', 66)
    title = slide['title']
    max_title_w = W - 144
    lines = wrap(d, title, title_font, max_title_w)
    ty = 244
    for line in lines:
        d.text((72, ty), line, font=title_font, fill=TEXT)
        ty += 78

    subtitle = slide.get('subtitle')
    if subtitle:
        sub_font = font('text', 32)
        d.text((72, ty + 8), subtitle, font=sub_font, fill=TEXT_DIM)
        ty += 56

    body_font = font('text', 32)
    body = slide['body']
    by = ty + 32
    bullet_r = 7
    for para in body:
        wrapped = wrap(d, para, body_font, W - 200)
        d.ellipse([(84, by + 18), (84 + bullet_r * 2, by + 18 + bullet_r * 2)], fill=GOLD)
        lx = 84 + bullet_r * 2 + 24
        for i, ln in enumerate(wrapped):
            d.text((lx, by + i * 42), ln, font=body_font, fill=TEXT)
        by += len(wrapped) * 42 + 20

    footer_font = font('text', 24)
    d.rectangle([(0, H - 88), (W, H - 84)], fill=ACCENT_SOFT)
    d.rectangle([(0, H - 84), (W, H)], fill=BG_STRIP)
    d.text((72, H - 60), 'oneverso.com.br/academia · @NexusAffilIAte', font=footer_font, fill=TEXT_DIM)
    right = 'ACADEMIA NEXUS'
    rw = d.textlength(right, font=footer_font)
    d.text((W - 72 - rw, H - 60), right, font=footer_font, fill=ACCENT)

    out = out_dir / f'slide_{idx:02d}.png'
    img.save(out, 'PNG', optimize=True)
    return out


def build_video(rebuild: Path, mod: dict) -> dict:
    slides_dir = rebuild / 'slides_premium'
    slides_dir.mkdir(parents=True, exist_ok=True)
    total = len(mod['slides'])
    for i in range(1, total + 1):
        draw_frame(mod, i, total, slides_dir)

    total_dur = mod['total_dur']
    weights = mod['weights']
    ws = sum(weights)
    durs = [round(total_dur * w / ws, 3) for w in weights]
    delta = round(total_dur - sum(durs), 3)
    durs[-1] = round(durs[-1] + delta, 3)

    clips_dir = rebuild / 'clips_premium'
    clips_dir.mkdir(parents=True, exist_ok=True)
    clip_paths: list[Path] = []
    for i, dur in enumerate(durs, 1):
        slide = slides_dir / f'slide_{i:02d}.png'
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

    concat = rebuild / 'concat_premium.txt'
    concat.write_text('\n'.join(f"file '{c.as_posix()}'" for c in clip_paths) + '\n', encoding='utf-8')

    silent_mp4 = rebuild / f'video_premium_silent.mp4'
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat),
        '-c', 'copy', str(silent_mp4),
    ], check=True)

    narration = rebuild / mod['narration']
    out_mp4 = rebuild / mod['video_name']
    subprocess.run([
        'ffmpeg', '-y', '-i', str(silent_mp4), '-i', str(narration),
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
        '-shortest', str(out_mp4)
    ], check=True)

    return {
        'video': str(out_mp4),
        'silent': str(silent_mp4),
        'durations': durs,
        'slides': [str(slides_dir / f'slide_{i:02d}.png') for i in range(1, total + 1)],
    }


def main():
    if len(sys.argv) < 2:
        print('usage: render_modulo_premium.py <codigo>', file=sys.stderr)
        sys.exit(2)
    codigo = sys.argv[1]
    if codigo not in MODULES:
        print(f'modulo desconhecido: {codigo}', file=sys.stderr)
        sys.exit(2)
    mod = MODULES[codigo]
    rebuild = ROOT / 'materiais' / 'video-aulas' / 'fundamental' / mod['slug'] / 'rebuild'
    if not rebuild.exists():
        print(f'rebuild missing: {rebuild}', file=sys.stderr)
        sys.exit(2)
    result = build_video(rebuild, mod)
    print(json.dumps({'codigo': codigo, **result}, ensure_ascii=False))


if __name__ == '__main__':
    main()

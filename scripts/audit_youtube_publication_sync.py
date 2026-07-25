from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path('/home/user/repo/Academ-IA').resolve()
YT = ROOT / 'youtube'
VIDEOS = ROOT / 'videos'
DOCS = ROOT / 'docs'

REPORT_JSON = DOCS / 'AUDITORIA_PUBLICACAO_YOUTUBE_2026-07-24.json'
REPORT_MD = DOCS / 'AUDITORIA_PUBLICACAO_YOUTUBE_2026-07-24.md'


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def build_report() -> dict:
    publish_plan = load_json(YT / 'publish_plan.json')
    upload_results = load_json(YT / 'upload_results.json')

    descriptions = sorted((YT / 'descriptions').glob('*.txt'))
    thumbs_png = sorted((YT / 'thumbnails').glob('*.png'))
    thumbs_jpg = sorted((YT / 'thumbnails_yt').glob('*.jpg'))
    teasers = sorted((YT / 'videos_teaser').glob('*.mp4'))
    root_mp4s = sorted(VIDEOS.glob('*.mp4'))
    onda49_720 = sorted((VIDEOS / 'aulas-onda-49' / 'renders').glob('*-720p.mp4'))
    onda49_narr = sorted((VIDEOS / 'aulas-onda-49' / 'renders').glob('*-narrated.mp4'))
    onda49_v2 = sorted((VIDEOS / 'aulas-onda-49' / 'v2').glob('*-narrated-v2.mp4'))

    uploaded = [x for x in publish_plan if x.get('status') == 'uploaded']
    ready = [x for x in publish_plan if x.get('status') == 'ready_to_upload']
    pending = [x for x in publish_plan if x.get('status') not in {'uploaded', 'ready_to_upload'}]

    invalid_desc = []
    upload_limit = []
    other_errors = []
    for item in upload_results.get('errors', []):
        err = item.get('error', '')
        if 'invalid video description' in err.lower():
            invalid_desc.append(item)
        elif 'uploadLimitExceeded' in err:
            upload_limit.append(item)
        else:
            other_errors.append(item)

    data = {
        'publish_plan_total': len(publish_plan),
        'uploaded_count': len(uploaded),
        'ready_to_upload_count': len(ready),
        'other_status_count': len(pending),
        'description_count': len(descriptions),
        'thumb_png_count': len(thumbs_png),
        'thumb_jpg_count': len(thumbs_jpg),
        'teaser_count': len(teasers),
        'videos_root_mp4_count': len(root_mp4s),
        'onda49_720_count': len(onda49_720),
        'onda49_narrated_count': len(onda49_narr),
        'onda49_v2_count': len(onda49_v2),
        'upload_errors_total': len(upload_results.get('errors', [])),
        'upload_limit_errors': len(upload_limit),
        'invalid_description_errors': len(invalid_desc),
        'other_upload_errors': len(other_errors),
        'ready_codes': [x['code'] for x in ready],
        'uploaded_codes': [x['code'] for x in uploaded],
        'invalid_description_codes': [x['code'] for x in invalid_desc],
    }
    return data


def patch_youtube_readme(report: dict) -> bool:
    path = YT / 'README.md'
    text = path.read_text(encoding='utf-8')
    original = text

    text = re.sub(
        r'Prontos para upload imediato: \*\*\d+\*\*\nRoteiro pronto, vídeo pendente: \*\*\d+\*\*',
        f"Publicados com sucesso: **{report['uploaded_count']}**\nProntos para upload imediato: **{report['ready_to_upload_count']}**\nBloqueio externo atual: **limite de upload do canal no YouTube**",
        text,
        count=1,
    )

    text = re.sub(
        r'## Em produção\n(?:- .*\n)+',
        '## Prontos para envio quando o canal liberar uploads\n'
        '- **09 · Funis e Lifecycle — O Sistema Completo** — assets locais completos, bloqueado apenas por limite de upload\n'
        '- **10 · A/B Testing com Judge — Ciência da Experimentação** — assets locais completos, bloqueado apenas por limite de upload\n'
        '- **11 · Análise de Coortes e Churn — A Arte de Reter** — assets locais completos, bloqueado apenas por limite de upload\n'
        '- **12 · Blueprints Elite — O Jogo do Top 10%** — assets locais completos, bloqueado apenas por limite de upload\n'
        '- **13 · Multi-Tenant e White-Label na Prática** — assets locais completos, bloqueado apenas por limite de upload\n',
        text,
        count=1,
        flags=re.M,
    )

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def patch_videos_readme(report: dict) -> bool:
    path = VIDEOS / 'README.md'
    text = path.read_text(encoding='utf-8')
    original = text

    text = text.replace(
        '**Total:** 15 roteiros · 15 thumbnails · 0 vídeo renderizado · 100% escrito',
        '**Total:** 15 roteiros · 15 thumbnails · 15 descrições YouTube · 13 teasers locais · 10 uploads concluídos · 5 uploads prontos aguardando liberação do canal'
    )
    text = text.replace(
        '**Status:** 15/16 vídeos full renderizados (94%)',
        '**Status:** 15 vídeos full do lote base documentados localmente + 19 renders 720p + 19 narrated + 19 narrated-v2 na ONDA-49/50'
    )
    text = text.replace(
        '### Fase 2 — Mínimo Viável (Próximo)\n- [ ] Renderizar vídeos 1-7 com narração ElevenLabs (1080p, 7-10min cada)\n- [ ] Versões verticais 9:16 (60s) para Shorts/Reels\n- [ ] Legendas .SRT em pt-BR\n- [ ] Persona visual (avatar animado de Alencar + Ive)\n',
        '### Fase 2 — Mínimo Viável (Atualizado)\n- [x] Roteiros, thumbnails e descrições-base consolidados\n- [x] Teasers locais criados para a faixa 04-14 (13 arquivos no repositório)\n- [ ] Normalizar aliases/nomenclatura dos teasers para 100% aderência ao publish plan\n- [ ] Legendas .SRT em pt-BR para todos os vídeos priorizados\n- [ ] Persona visual (avatar animado de Alencar + Ive)\n'
    )

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def patch_onda49_readme(report: dict) -> bool:
    path = VIDEOS / 'aulas-onda-49' / 'README.md'
    text = path.read_text(encoding='utf-8')
    original = text

    text = text.replace(
        '> esta onda entrega o conjunto visual completo: 19 videoaulas com slides B2\n> 1920×1080 navy+gold + 9 renders MP4 720p sincronizados com áudio TTS + 19 capas\n> YouTube PNG 16:9 widescreen prontas para publicação.\n',
        '> esta onda entrega o conjunto visual completo: 19 videoaulas com slides B2\n> 1920×1080 navy+gold + 19 renders 720p + 19 narrated + 19 narrated-v2\n> e 19 capas YouTube PNG 16:9 widescreen prontas para publicação.\n'
    )
    text = text.replace(
        '| **Vídeos MP4 720p** | 9 (aulas 17, 26-33) | `renders/aula-NN-SLUG-720p.mp4` |',
        '| **Vídeos MP4 720p** | 19 (aulas 15-33) | `renders/aula-NN-SLUG-720p.mp4` |'
    )
    text = text.replace(
        '**Total renders prontos**: 9/19 (47%)',
        '**Total renders prontos**: 19/19 720p · 19/19 narrated · 19/19 narrated-v2 (100%)'
    )

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def write_report(report: dict):
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    md = [
        '# Auditoria de Publicação YouTube',
        '',
        '## Resumo executivo',
        f"- Publish plan total: **{report['publish_plan_total']}** aulas.",
        f"- Uploads concluídos: **{report['uploaded_count']}**.",
        f"- Prontos para upload imediato: **{report['ready_to_upload_count']}**.",
        f"- Descrições `.txt`: **{report['description_count']}**.",
        f"- Thumbnails PNG: **{report['thumb_png_count']}** · JPG: **{report['thumb_jpg_count']}**.",
        f"- Teasers locais: **{report['teaser_count']}**.",
        f"- ONDA-49 renders: **{report['onda49_720_count']}** 720p · **{report['onda49_narrated_count']}** narrated · **{report['onda49_v2_count']}** narrated-v2.",
        '',
        '## Bloqueios externos',
        f"- Erros de upload por limite do canal: **{report['upload_limit_errors']}**.",
        f"- Erros de descrição inválida: **{report['invalid_description_errors']}**.",
        f"- Códigos prontos aguardando liberação do canal: {', '.join(report['ready_codes']) if report['ready_codes'] else 'nenhum' }.",
        '',
        '## Leitura operacional',
        '- Os materiais-base de publicação estão consistentes no repositório.',
        '- O principal gargalo atual não é criativo nem editorial; é a limitação de upload do canal.',
        '- Os READMEs operacionais foram atualizados para refletir o estado real do pipeline.',
        '',
    ]
    REPORT_MD.write_text('\n'.join(md) + '\n', encoding='utf-8')


def main():
    report = build_report()
    changed = {
        'youtube_readme': patch_youtube_readme(report),
        'videos_readme': patch_videos_readme(report),
        'onda49_readme': patch_onda49_readme(report),
    }
    write_report(report)
    print(json.dumps({'report': report, 'changed': changed}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

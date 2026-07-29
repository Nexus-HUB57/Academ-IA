from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path('/home/user/repo/Academ-IA').resolve()
CATALOG = ROOT / 'producao' / 'catalog' / 'CATALOGO_MODULOS.md'
DOCS = ROOT / 'docs'
YT = ROOT / 'youtube'
VIDEOS = ROOT / 'videos'

OUT_JSON = DOCS / 'ACADEMIA_MANIFEST_OPERACIONAL_2026-07-24.json'
OUT_MD = DOCS / 'ACADEMIA_MANIFEST_OPERACIONAL_2026-07-24.md'

STATUS_LINE_BY_CODE = {
    '00': '🟢 Upload concluído no YouTube. Vídeo principal já publicado; assets locais seguem como referência editorial e operacional.',
    '01': '🟢 Upload concluído no YouTube. Vídeo principal já publicado; teaser e thumbnail permanecem como apoio operacional.',
    '02': '🟢 Upload concluído no YouTube. Vídeo principal já publicado; teaser e thumbnail permanecem como apoio operacional.',
    '03': '🟢 Upload concluído no YouTube. Vídeo principal já publicado; teaser e thumbnail permanecem como apoio operacional.',
    '04': '🟢 Upload concluído no YouTube. Vídeo principal já publicado; teaser local permanece como apoio de campanha.',
    '05': '🟢 Upload concluído no YouTube. Vídeo principal já publicado; aliases antigos de teaser permanecem apenas por retrocompatibilidade.',
    '06': '🟢 Upload concluído no YouTube. Vídeo principal já publicado; teaser local permanece como apoio de campanha.',
    '07': '🟢 Upload concluído no YouTube. Vídeo principal já publicado; aliases antigos de teaser permanecem apenas por retrocompatibilidade.',
    '08': '🟢 Upload concluído no YouTube. Vídeo principal já publicado; teaser local permanece como apoio de campanha.',
    '09': '🟡 Assets locais completos e fila pronta. Upload externo bloqueado temporariamente por limite do canal no YouTube.',
    '10': '🟡 Assets locais completos e fila pronta. Upload externo bloqueado temporariamente por limite do canal no YouTube; descrição foi saneada para nova tentativa.',
    '11': '🟡 Assets locais completos e fila pronta. Upload externo bloqueado temporariamente por limite do canal no YouTube.',
    '12': '🟡 Assets locais completos e fila pronta. Upload externo bloqueado temporariamente por limite do canal no YouTube.',
    '13': '🟡 Assets locais completos e fila pronta. Upload externo bloqueado temporariamente por limite do canal no YouTube.',
    '14': '🟢 Upload concluído no YouTube. Vídeo principal já publicado; teaser local permanece como apoio de campanha.',
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def build_manifest() -> dict:
    publish_plan = load_json(YT / 'publish_plan.json')
    ready_queue = load_json(YT / 'upload_batch_ready.json') if (YT / 'upload_batch_ready.json').exists() else []
    aliases = load_json(YT / 'teaser_aliases.json') if (YT / 'teaser_aliases.json').exists() else []
    upload_results = load_json(YT / 'upload_results.json') if (YT / 'upload_results.json').exists() else {'uploaded': [], 'errors': []}

    by_code = {x['code']: x for x in publish_plan}
    modules = []
    for code in sorted(by_code):
        item = by_code[code]
        alias = next((a for a in aliases if a['code'] == code), None)
        modules.append({
            'code': code,
            'series': item.get('series'),
            'title': item.get('title'),
            'status': item.get('status'),
            'youtube_title': item.get('youtube_title'),
            'video_file': Path(item.get('video_path', '')).name if item.get('video_path') else '',
            'thumbnail_file': Path(item.get('thumbnail_path', '')).name if item.get('thumbnail_path') else '',
            'db_lessons': item.get('db_lessons', []),
            'teaser_alias': alias,
        })

    uploaded = [m for m in modules if m['status'] == 'uploaded']
    ready = [m for m in modules if m['status'] == 'ready_to_upload']
    errors = upload_results.get('errors', [])
    upload_limit_errors = [e for e in errors if 'uploadLimitExceeded' in e.get('error', '')]
    invalid_desc_errors = [e for e in errors if 'invalid video description' in e.get('error', '').lower()]

    return {
        'generated_on': '2026-07-24',
        'publish_plan_total': len(modules),
        'uploaded_total': len(uploaded),
        'ready_total': len(ready),
        'upload_limit_errors': len(upload_limit_errors),
        'invalid_description_errors': len(invalid_desc_errors),
        'modules': modules,
        'ready_queue_codes': [x['code'] for x in ready_queue],
    }


def patch_catalog(manifest: dict) -> bool:
    text = CATALOG.read_text(encoding='utf-8')
    original = text

    text = text.replace('**Status atualizado:** 2026-07-15 · v2.1 (Onda 49 — 15 vídeos full)',
                        '**Status atualizado:** 2026-07-24 · v2.4 (catálogo sincronizado com publish plan e fila real de upload)')

    old_table = '''| Total de módulos | 16 (4 Fund · 4 Agente · 4 Master · 4 Elite) |
| Módulos com roteiro | **16/16 (100%)** |
| Módulos com roteiro revisado | 16/16 (100%) |
| Módulos com TTS/áudio completo | **15/16 (94%)** — 00 com 7 cenas WAV; 01-14 com TTS PT-BR (Onda 49) |
| Módulos com motion-graphics slides | **15/16 (94%)** — 4 PNGs 1280x720 por vídeo |
| Módulos com vídeo full (19-30s, Onda 49) | **15/16 (94%)** — H.264+AAC, TTS voice-cloned PT-BR |
| Teasers publicados (5-10s) | 6 (00, 05, 07, master-otim, elite-fed, hero) |
| Módulos no publish_plan.json | 16/16 (100%) |
| Thumbnails 2K geradas | 9 (00, 01, 02, 03, 04, 05, 06, 07, 08) |
| Thumbnails YouTube | 15 (00-14) |
| Módulos publicados no YouTube | 0/16 (0%) — aguardando upload PRIVATE→unlisted |'''
    new_table = '''| Total de módulos | 15 (4 Fund · 4 Agente · 4 Master · 3 Elite) |
| Módulos com roteiro | **15/15 (100%)** |
| Módulos com roteiro revisado | 15/15 (100%) |
| Módulos com slides de curso | **15/15 (100%)** |
| Módulos com HTML/PDF de curso | **15/15 (100%)** |
| Módulos no `publish_plan.json` | **15/15 (100%)** |
| Módulos publicados no YouTube | **10/15 (67%)** |
| Módulos na fila pronta de upload | **5/15 (33%)** |
| Thumbnails YouTube | **15/15 (100%)** |
| Descrições YouTube `.txt` | **15/15 (100%)** |
| Bloqueio externo atual | limite de upload do canal do YouTube (codes 09-13) |'''
    text = text.replace(old_table, new_table)

    replacements = {
        '- **Status:** 🟢 Roteiro + áudio + teaser. **Pendente:** vídeo full 60-140s com motion-graphics': '- **Status:** ' + STATUS_LINE_BY_CODE['00'],
        '- **Status:** 🟡 Roteiro pronto, sem áudio. **Pendente:** TTS + vídeo full': None,
    }
    text = text.replace('- **Teaser publicado:** `videos/video-00-boas-vindas.mp4` (5.8s)', '- **Teaser local:** `video-00-boas-vindas.mp4` (apoio de campanha)')
    text = text.replace('- **Teasers:** `video-01-ioaid` (em `youtube/videos_teaser/`)', '- **Teaser local:** `video-01-ioaid` (apoio operacional; vídeo principal já publicado)')

    # update status lines by module section 01-03 explicitly
    for code in ['01', '02', '03']:
        heading = f'### {code} '
        status = STATUS_LINE_BY_CODE[code]
        pattern = rf'({re.escape(heading)}.*?\n(?:.*\n)*?- \*\*Status:\*\* ).*?(\n)'
        text = re.sub(pattern, rf'\1{status}\2', text, count=1, flags=re.M)
    for code in ['04','05','06','07','08','09','10','11','12','13','14']:
        heading = f'### {code} '
        status = STATUS_LINE_BY_CODE[code]
        pattern = rf'({re.escape(heading)}.*?\n(?:.*\n)*?- \*\*Status:\*\* ).*?(\n)'
        text = re.sub(pattern, rf'\1{status}\2', text, count=1, flags=re.M)
    # section 00 needs direct replace due wording
    text = text.replace('- **Status:** 🟢 Roteiro + áudio + teaser. **Pendente:** vídeo full 60-140s com motion-graphics', f'- **Status:** {STATUS_LINE_BY_CODE["00"]}')

    # mark roadmap as archival + current handoff
    text = text.replace('## 🔴 Nível Elite (4 módulos)', '## 🔴 Nível Elite (3 módulos)')
    text = text.replace('- **Módulos como persona principal:** 8 (00 técnico, 02, 04, 05, 06, 07, 08, 10, 11, 13)', '- **Módulos como persona principal:** 10 (00 técnico, 02, 04, 05, 06, 07, 08, 10, 11, 13)')
    text = text.replace('## 🎯 Roadmap de Produção (Onda 49+)', '## 🎯 Roadmap de Produção (histórico + handoff atual)')
    text = text.replace('### 🎬 Sprint 1 — Vídeos full 60-140s', '### 🎬 Sprint 1 — Histórico da composição de vídeos full')
    text = text.replace('### 🖼️ Sprint 2 — Motion-graphics slides', '### 🖼️ Sprint 2 — Histórico dos motion-graphics')
    text = text.replace('### 📤 Sprint 3 — Upload YouTube (PRIVATE → unlisted)', '### 📤 Sprint 3 — Estado atual da publicação YouTube')
    text = text.replace('### 🚀 Sprint 4 — Deploy VPS', '### 🚀 Sprint 4 — Handoff de deploy / integração')
    text = text.replace('**Meta:** 16 vídeos full publicados como PRIVATE no YouTube', '**Meta histórica:** 15 vídeos full previstos no publish plan canônico')
    text = text.replace('- [ ] **01 a 14** — gerar TTS voice-cloned (15 roteiros × ~2-3 cenas) + slides + render', '- [ ] **01 a 14** — gerar TTS voice-cloned (14 roteiros × ~2-3 cenas) + slides + render')
    text = text.replace('- [ ] Implementar `scripts/youtube/compose_videos_academia.py` com 16 trilhas', '- [ ] Implementar `scripts/youtube/compose_videos_academia.py` com 15 trilhas canônicas')
    if '### 📌 Estado canônico em 2026-07-24' not in text:
        marker = '## 🎯 Roadmap de Produção (histórico + handoff atual)\n'
        insertion = marker + '\n### 📌 Estado canônico em 2026-07-24\n- Publicados no YouTube: **10** módulos (`00-08`, `14`).\n- Fila pronta e bloqueada apenas por limite do canal: **09-13**.\n- `youtube/publish_plan.json` é a fonte canônica de publicação.\n- `youtube/upload_batch_ready.json` contém somente os próximos itens elegíveis para nova tentativa.\n- `youtube/teaser_aliases.json` documenta divergências de nomenclatura entre teaser local e slug canônico.\n\n'
        text = text.replace(marker, insertion, 1)

    if text != original:
        CATALOG.write_text(text, encoding='utf-8')
        return True
    return False


def write_outputs(manifest: dict):
    OUT_JSON.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = [
        '# Manifesto Operacional da Academia',
        '',
        '## Resumo canônico',
        f"- Total no publish plan: **{manifest['publish_plan_total']}**",
        f"- Publicados no YouTube: **{manifest['uploaded_total']}**",
        f"- Prontos para nova tentativa: **{manifest['ready_total']}**",
        f"- Erros por limite do canal: **{manifest['upload_limit_errors']}**",
        f"- Erros de descrição inválida: **{manifest['invalid_description_errors']}**",
        '',
        '## Fila pronta atual',
    ]
    for code in manifest['ready_queue_codes']:
        mod = next((m for m in manifest['modules'] if m['code'] == code), None)
        if mod:
            lines.append(f"- **{code}** · {mod['title']} · vídeo `{mod['video_file']}` · thumb `{mod['thumbnail_file']}`")
    lines += ['', '## Fonte canônica', '- Publicação: `youtube/publish_plan.json`', '- Fila: `youtube/upload_batch_ready.json`', '- Aliases de teaser: `youtube/teaser_aliases.json`', '- Catálogo operacional: `producao/catalog/CATALOGO_MODULOS.md`', '']
    OUT_MD.write_text('\n'.join(lines), encoding='utf-8')


def main():
    manifest = build_manifest()
    changed = patch_catalog(manifest)
    write_outputs(manifest)
    print(json.dumps({
        'changed_catalog': changed,
        'publish_plan_total': manifest['publish_plan_total'],
        'uploaded_total': manifest['uploaded_total'],
        'ready_total': manifest['ready_total']
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

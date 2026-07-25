from __future__ import annotations

from pathlib import Path
import csv
import json
import re
import unicodedata

ROOT = Path('/home/user/repo/Academ-IA').resolve()
YT = ROOT / 'youtube'
CATALOG = ROOT / 'producao' / 'catalog' / 'CATALOGO_MODULOS.md'
DOCS = ROOT / 'docs'

REPORT_MD = DOCS / 'YOUTUBE_UPLOAD_QUEUE_SYNC_2026-07-24.md'
REPORT_JSON = DOCS / 'YOUTUBE_UPLOAD_QUEUE_SYNC_2026-07-24.json'
READY_JSON = YT / 'upload_batch_ready.json'
ALIASES_JSON = YT / 'teaser_aliases.json'
PUBLISH_CSV = YT / 'publish_plan.csv'

TEASER_BY_CODE = {
    '04': 'video-04-seu-primeiro-agente.mp4',
    '05': 'video-05-skills-essenciais.mp4',
    '06': 'video-06-disparo-no-whatsapp-em-escala.mp4',
    '07': 'video-07-judge-revisor.mp4',
    '08': 'video-08-otimizacao-de-conversao.mp4',
    '09': 'video-09-funis-e-lifecycle.mp4',
    '10': 'video-10-a-b-testing-com-judge.mp4',
    '11': 'video-11-coortes-e-churn.mp4',
    '12': 'video-12-blueprints-elite.mp4',
    '13': 'video-13-multi-tenant-e-white-label.mp4',
    '14': 'video-14-federacao-de-agentes-zero-trust.mp4',
}

SECTION_STATUS_MAP = {
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


def sanitize_description(text: str) -> str:
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = unicodedata.normalize('NFKC', text)
    text = text.replace('—', '-').replace('–', '-').replace('•', '-')
    text = text.replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
    text = re.sub(r'[^\S\n]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text).strip() + '\n'
    return text


def desc_path_from_item(item: dict) -> Path:
    thumb_name = Path(item['thumbnail_path']).stem
    return YT / 'descriptions' / f'{thumb_name}.txt'


def load_publish_plan() -> list[dict]:
    return json.loads((YT / 'publish_plan.json').read_text(encoding='utf-8'))


def build_ready_queue(plan: list[dict]) -> list[dict]:
    ready = []
    for item in plan:
        if item.get('status') != 'ready_to_upload':
            continue
        desc_path = desc_path_from_item(item)
        desc_raw = desc_path.read_text(encoding='utf-8') if desc_path.exists() else item.get('description', '')
        payload = dict(item)
        payload['description'] = sanitize_description(desc_raw)
        payload['description_path'] = str(desc_path.relative_to(ROOT)) if desc_path.exists() else ''
        payload['teaser_path'] = f"youtube/videos_teaser/{TEASER_BY_CODE.get(item['code'],'')}" if item['code'] in TEASER_BY_CODE else ''
        payload['status'] = 'ready_to_upload'
        ready.append(payload)
    return ready


def write_publish_plan_csv(plan: list[dict]) -> None:
    fields = ['code','series','title','status','video_path','thumbnail_path','db_lessons']
    with PUBLISH_CSV.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for item in plan:
            w.writerow({
                'code': item.get('code',''),
                'series': item.get('series',''),
                'title': item.get('title',''),
                'status': item.get('status',''),
                'video_path': item.get('video_path',''),
                'thumbnail_path': item.get('thumbnail_path',''),
                'db_lessons': ','.join(item.get('db_lessons',[])),
            })


def build_aliases(plan: list[dict]) -> list[dict]:
    out = []
    teaser_dir = YT / 'videos_teaser'
    for item in plan:
        code = item['code']
        actual = TEASER_BY_CODE.get(code, '')
        actual_path = teaser_dir / actual if actual else None
        canonical = f"{item['slug']}.mp4"
        canonical_path = teaser_dir / canonical
        if actual_path and actual_path.exists() and actual == canonical:
            status = 'exact'
        elif actual_path and actual_path.exists():
            status = 'mapped_alias'
        else:
            status = 'missing'
        out.append({
            'code': code,
            'slug': item['slug'],
            'canonical_teaser_file': canonical,
            'actual_teaser_file': actual if actual else '',
            'actual_exists': bool(actual_path and actual_path.exists()),
            'canonical_exists': canonical_path.exists(),
            'status': status,
        })
    return out


def patch_catalog() -> bool:
    text = CATALOG.read_text(encoding='utf-8')
    original = text
    for code, status_line in SECTION_STATUS_MAP.items():
        pattern = rf'(### {code} .*?\n(?:.*\n)*?- \*\*Status:\*\* ).*?(\n)'
        repl = rf'\1{status_line}\2'
        text = re.sub(pattern, repl, text, count=1, flags=re.M)
    replacements = {
        '`ready: false` no build_academia_materials. **Pendente:** TTS + vídeo full': 'fila de upload pronta; bloqueio atual apenas no limite do canal do YouTube',
        '`ready: true` no build_academia_materials. **Pendente:** TTS + vídeo full': 'upload concluído ou assets locais completos conforme publish plan atual',
        '**Teaser publicado:** `videos/video-05-skills-assembly.mp4` (5.8s) — *atenção: nome divergente*': '**Teaser local:** `video-05-skills-essenciais.mp4` · alias legado adicional: `video-05-skills-assembly.mp4`',
        '**Teaser publicado:** `videos/video-07-judge-scales.mp4` (5.8s) — *atenção: nome divergente*': '**Teaser local:** `video-07-judge-revisor.mp4` · alias legado adicional: `video-07-judge-scales.mp4`',
        '**Teaser publicado:** `videos/video-master-otimizacao.mp4` (10.1s) — *nome divergente*': '**Teaser local:** `video-08-otimizacao-de-conversao.mp4` · master full publicado: `video-master-otimizacao.mp4`',
        '**Teaser publicado:** `videos/video-elite-federacao.mp4` (10.1s)': '**Teaser local:** `video-14-federacao-de-agentes-zero-trust.mp4` · master full publicado: `video-elite-federacao.mp4`',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    additions = {
        '### 12 · Blueprints Elite — O Jogo do Top 10%': '- **Teaser:** `video-12-blueprints-elite.mp4`\n',
        '### 13 · Multi-Tenant e White-Label na Prática': '- **Teaser:** `video-13-multi-tenant-e-white-label.mp4`\n',
    }
    for marker, line in additions.items():
        if marker in text and line.strip() not in text:
            text = text.replace(marker + '\n', marker + '\n' + line)

    if text != original:
        CATALOG.write_text(text, encoding='utf-8')
        return True
    return False


def write_reports(plan: list[dict], ready: list[dict], aliases: list[dict]) -> None:
    data = {
        'publish_plan_total': len(plan),
        'ready_queue_total': len(ready),
        'uploaded_total': sum(1 for x in plan if x.get('status') == 'uploaded'),
        'ready_codes': [x['code'] for x in ready],
        'alias_summary': {
            'exact': sum(1 for x in aliases if x['status'] == 'exact'),
            'mapped_alias': sum(1 for x in aliases if x['status'] == 'mapped_alias'),
            'missing': sum(1 for x in aliases if x['status'] == 'missing'),
        },
        'ready_queue': ready,
        'teaser_aliases': aliases,
    }
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    md = [
        '# Sync da fila de upload YouTube',
        '',
        '## Resumo',
        f"- Publicados: **{data['uploaded_total']}**",
        f"- Prontos para nova tentativa de upload: **{data['ready_queue_total']}** ({', '.join(data['ready_codes'])})",
        f"- Teasers com nome canônico exato: **{data['alias_summary']['exact']}**",
        f"- Teasers resolvidos por alias mapeado: **{data['alias_summary']['mapped_alias']}**",
        f"- Teasers ausentes: **{data['alias_summary']['missing']}**",
        '',
        '## Fila pronta',
    ]
    for item in ready:
        md.append(f"- **{item['code']}** · `{item['slug']}` · vídeo `{Path(item['video_path']).name}` · thumb `{Path(item['thumbnail_path']).name}` · teaser `{Path(item['teaser_path']).name if item.get('teaser_path') else '-'}`")
    md += ['', '## Observações operacionais', '- `youtube/upload_batch_ready.json` foi regenerado com a fila atual, evitando itens já publicados.', '- `youtube/publish_plan.csv` foi sincronizado a partir do plano JSON canônico.', '- As descrições da fila pronta foram saneadas para nova tentativa de upload, reduzindo risco de `invalidDescription`.', '']
    REPORT_MD.write_text('\n'.join(md), encoding='utf-8')


def main():
    plan = load_publish_plan()
    ready = build_ready_queue(plan)
    aliases = build_aliases(plan)
    READY_JSON.write_text(json.dumps(ready, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    ALIASES_JSON.write_text(json.dumps(aliases, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    write_publish_plan_csv(plan)
    catalog_changed = patch_catalog()
    write_reports(plan, ready, aliases)
    print(json.dumps({
        'ready_queue_total': len(ready),
        'ready_codes': [x['code'] for x in ready],
        'catalog_changed': catalog_changed,
        'alias_summary': {
            'exact': sum(1 for x in aliases if x['status'] == 'exact'),
            'mapped_alias': sum(1 for x in aliases if x['status'] == 'mapped_alias'),
            'missing': sum(1 for x in aliases if x['status'] == 'missing'),
        }
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

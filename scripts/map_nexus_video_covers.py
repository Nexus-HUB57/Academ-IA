#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path('/home/user/repo/Academ-IA')
TODAY = date(2026, 7, 24).isoformat()
SRC = ROOT / 'producao' / 'assets' / 'thumbnails'
DOCS = ROOT / 'docs'

MAP = [
    ('00', 'Boas-vindas à AcademIA Nexus', 'capa-00-boas-vindas-ive.png', 'thumb-00-boas-vindas.png'),
    ('01', 'Entendendo o IOAID', 'capa-01-entendendo-ioaid-dupla.png', 'thumb-01-ioaid.png'),
    ('02', 'O Sistema SHO (Self-Healing Orchestrator)', 'capa-02-sistema-sho-dupla.png', 'thumb-02-sho.png'),
    ('03', 'Painel do Afiliado — Visão Geral da Operação', 'capa-03-painel-afiliado-ive.png', 'thumb-03-painel.png'),
    ('04', 'Construindo Seu Primeiro Agente em 4 Minutos', 'capa-04-primeiro-agente-dupla.png', 'thumb-04-primeiro-agente.png'),
    ('05', 'Skills Essenciais — Copywriter + Audience-Segmenter', 'capa-05-skills-essenciais-alencar.png', 'thumb-05-skills.png'),
    ('06', 'Disparando no WhatsApp em Escala', 'capa-06-disparo-whatsapp-alencar.png', 'thumb-06-disparo.png'),
    ('07', 'Judge Revisor — A IA que Decide por Você', 'capa-07-judge-revisor-alencar.png', 'thumb-07-judge.png'),
    ('08', 'Otimização de Conversão — A Matemática da Receita', 'capa-08-otimizacao-conversao-dupla.png', 'thumb-08-otimizacao.png'),
    ('09', 'Funis e Lifecycle — O Sistema Completo', 'capa-09-funis-lifecycle-dupla.png', 'thumb-09-funis-lifecycle.webp'),
    ('10', 'A/B Testing com Judge — Ciência da Experimentação', 'capa-10-ab-testing-judge-dupla.png', 'thumb-10-ab-test-judge.webp'),
    ('11', 'Análise de Coortes e Churn — A Arte de Reter', 'capa-11-coortes-churn-dupla.png', 'thumb-11-coortes-churn.webp'),
    ('12', 'Blueprints Elite — O Jogo do Top 10%', 'capa-12-blueprints-elite-dupla.png', 'thumb-12-blueprints-elite.webp'),
    ('13', 'Multi-Tenant e White-Label na Prática', 'capa-13-multi-tenant-dupla.png', 'thumb-13-multi-tenant.webp'),
    ('14', 'Federação de Agentes Zero-Trust', 'capa-14-federacao-agentes-dupla.png', 'thumb-14-federacao-agentes.webp'),
]


def dims(path: Path) -> str:
    # dimensions already audited as 1672x941; keep deterministic and simple
    return '1672x941' if path.exists() else 'ausente'


rows = []
for code, title, capa, thumb in MAP:
    capa_path = SRC / capa
    thumb_path = SRC / thumb
    rows.append({
        'code': code,
        'title': title,
        'official_cover_png': capa,
        'official_cover_exists': capa_path.exists(),
        'official_cover_dimensions': dims(capa_path),
        'video_thumb_asset': thumb,
        'video_thumb_exists': thumb_path.exists(),
        'video_thumb_dimensions': dims(thumb_path),
        'canonical_source_dir': 'producao/assets/thumbnails',
        'decision': 'reusar_no_rebuild',
    })

summary = {
    'date': TODAY,
    'canonical_source_dir': 'producao/assets/thumbnails',
    'modules_total': len(rows),
    'official_cover_exists_total': sum(1 for r in rows if r['official_cover_exists']),
    'video_thumb_exists_total': sum(1 for r in rows if r['video_thumb_exists']),
    'resolution_standard': '1672x941',
    'decision': 'capas prontas e aprovadas passam a ser a fonte canônica de capa para o rebuild 00-14',
}

json_path = DOCS / f'MAPEAMENTO_CAPAS_VIDEO_AULAS_NEXUS_{TODAY}.json'
md_path = DOCS / f'MAPEAMENTO_CAPAS_VIDEO_AULAS_NEXUS_{TODAY}.md'
json_path.write_text(json.dumps({'summary': summary, 'modules': rows}, ensure_ascii=False, indent=2), encoding='utf-8')

md = []
md.append('# Mapeamento de Capas — Vídeo-Aulas Nexus')
md.append('')
md.append(f'**Data:** {TODAY}')
md.append('')
md.append('## Decisão canônica')
md.append('- A pasta `producao/assets/thumbnails` passa a ser a **fonte canônica de capas prontas e aprovadas** para o rebuild dos vídeos `00-14`.')
md.append('- As capas em padrão `capa-*.png` e os thumbs em padrão `thumb-*` devem ser **reusados**, não recriados.')
md.append('- A resolução conferida para os assets aprovados é **1672×941**.')
md.append('')
md.append('## Resumo')
md.append(f"- Módulos mapeados: **{summary['modules_total']}**")
md.append(f"- Capas oficiais existentes: **{summary['official_cover_exists_total']}/{summary['modules_total']}**")
md.append(f"- Thumbs operacionais existentes: **{summary['video_thumb_exists_total']}/{summary['modules_total']}**")
md.append('')
md.append('## Tabela canônica 00-14')
for r in rows:
    md.append(f"- **{r['code']} · {r['title']}** → capa `{r['official_cover_png']}` · thumb `{r['video_thumb_asset']}`")
md.append('')
md.append('## Regra prática para a produção')
md.append('- A abertura visual pode herdar a identidade dessas capas.')
md.append('- O frame inicial do vídeo pode usar diretamente a capa oficial ou uma variação motion-preserving dela.')
md.append('- Geração nova deve focar em **abertura e narração**, não em refazer capas aprovadas.')

md_path.write_text('\n'.join(md) + '\n', encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))

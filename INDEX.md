# 📚 AcademIA Nexus Affil'IA'te · INDEX Master

**Última atualização**: 2026-07-23 · Helena Nexus · revisão pós-split Academ'IA/Marketplace · push dcd8ae8 → em progresso
**Total**: 36 apostilas · 22 roteiros full · 23 vídeos MP4 (ONDA-47) + 9 renders 720p (ONDA-49) · 19 capas YouTube ONDA-50 · 95 slides PNG + 95 wrappers HTML · 19 webinars · 36 tutoriais · 14 playbooks · 9 treinamentos · 11 hubs · 15 TTS full · 75 frames
**Versão**: **2.0-on-50** — NEXUS AFFIL'IA'TE TECH + ONDA-49/50 (95 slides PNG, 95 HTML wraps, 19 capas, 9 renders 720p)

> 🌊 **Estado do Z pipeline** (verificado via `MASTER-PIPELINE-E2E.json`): ingest ✅ render ✅ capas ✅ HTML ✅, resta **renderar 10 MP4s ONDA-49 restantes** + **apagar 4 TODOs** das apostilas 17/18/32/33.
>
> 🧭 **Governança de split ativa**: `Academ-IA` passa a ser o repositório canônico de conteúdo pedagógico/interno da Nexus Affil'IA'te, enquanto `Marketplace-Nexus-` passa a ser o repositório canônico dos ebooks completos, HTML+MD comerciais e capas originais de produtos.

> 🌊 **Onda 40** — integração com a nova coletânea técnica NEXUS AFFIL'IA'TE TECH
> (5 ebooks PhD-level espelhados como 5 roteiros-âncora: 15-19).

> 🌊 **Onda 49/50** — `aulas-onda-49` com 19 aulas completas (roteiro + slides PNG + HTML wrappers + capa + render), e `aulas-onda-50` com índice cross-refs + INDEX-PERSONAS + SHORTS-SPEC.
## 🧭 Regra de Classificação de Conteúdo

- **Academ-IA**: cursos, trilhas, apostilas, tutoriais, webinars, certificações, vídeos, roteiros, governança, Lab-Nexus, Lib-Nexus e pipeline audiovisual.
- **Marketplace-Nexus-**: ebooks comerciais completos, arquivos HTML+MD de venda, capas originais e ativos de monetização pública.
- Quando um conteúdo da Academ'IA referenciar um material comercial, a regra é **linkar e derivar**, não duplicar o arquivo-fonte integral.
- Documento operacional de apoio: `docs/REPO_SPLIT_GOVERNANCA_2026-07-23.md`.

## 🎯 Estrutura Oficial (Fonte da Verdade)

```
AcademIA/
├── INDEX.md              ← este arquivo (mapa completo)
├── README.md             ← overview público
├── CHANGELOG.md          ← histórico de mudanças
├── docs/                 ← documentação (FAQ, resumo executivo, roadmap)
│
├── cursos/               ← 4 trilhas oficiais (16 MB)
│   ├── fundamental/      ← Trilha F (iniciante)
│   ├── agente/           ← Trilha A (intermediário)
│   ├── master/           ← Trilha M (avançado)
│   └── elite/            ← Trilha E (expert)
│
├── videos/               ← Vídeo-aulas MP4 (33 MB)
│   ├── roteiros/         ← Scripts editoriais
│   └── thumbnails/       ← Capas dos vídeos
│
├── pdf/                  ← PDFs oficiais publicados (66 MB)
├── html/                 ← Renderizações HTML
├── apostilas/            ← Material didático extenso
├── hubs/                 ← Hubs temáticos
├── webinars/             ← Sessões ao vivo
├── tutoriais/            ← Tutoriais rápidos
├── playbooks/            ← Manuais operacionais
├── certificacoes/        ← Certificações emitidas
├── marca/                ← Brand kit + personas unificadas (Ive, Alencar, Dupla)
│   └── personas/         ← Personas consolidadas (migrado de personas/ em 2026-07-21)
├── Lab-Nexus/            ← Laboratório de prompts
├── Lib-Nexus/            ← Biblioteca de referência
├── producao/             ← Pipeline de produção
│   ├── apostilas/
│   ├── apostilas-pdf/
│   ├── video-aulas/
│   ├── roteiros/
│   ├── templates/
│   ├── assets/
│   ├── catalog/
│   ├── personas/
│   ├── pipeline/
│   └── quality/
└── sync/                 ← Scripts de sincronização
```

## 🚀 Fluxo Editorial

```
1. Criar em: AcademIA/producao/ (rascunho)
2. Revisar: AcademIA/producao/quality/
3. Publicar em: AcademIA/{cursos,videos,pdf}/ (versão oficial)
4. Sincronizar: /public/academia/ (servido pelo nginx)
5. Registrar: academia_lessons (Postgres)
```

## 📖 Trilhas Ativas (validadas no DB)

| Lesson ID | Trilha | Video URL |
|-----------|--------|-----------|
| fund-00 | Fundamental | mod00-boas-vindas.mp4 |
| fund-01 | Fundamental | mod01-entendendo-ioaid.mp4 |
| fund-02 | Fundamental | mod02-sistema-sho.mp4 |
| fund-03 | Fundamental | mod03-painel-afiliado.mp4 |
| agent-00 | Agente | mod00-primeiro-agente.mp4 |
| agent-01 | Agente | mod01-skills-essenciais.mp4 |
| agent-02 | Agente | mod02-disparo-whatsapp.mp4 |
| agent-03 | Agente | mod03-judge-revisor.mp4 |

## 🎬 Vídeos Publicados

- ✅ 6 vídeos curtos (POCs 6-10s) em `AcademIA/videos/`
- ✅ 20 thumbnails 2K geradas (incluindo 5 âncoras TECH 15-19)
- ✅ 17 roteiros completos (video-00 a 14, +5 âncoras TECH 15-19)
- ⏳ Migração para YouTube @NexusAffilIAte-w9p pendente (público)
- ✅ Modo `mp4-gated` para trilhas premium

### 🌊 Onda 40 — Roteiros-âncora NEXUS AFFIL'IA'TE TECH

| # | Roteiro | Ebook origem | Trilha |
|---|---|---|---|
| 15 | Orquestração de Ecossistemas IA | NEXUS_AFFIL_IA_TECH_VOL_01 | Elite |
| 16 | Senciência e suas Barreiras | NEXUS_AFFIL_IA_TECH_VOL_02 | Master (convidado) |
| 17 | O Poder x Perigo da Autonomia AI | NEXUS_AFFIL_IA_TECH_VOL_03 | Elite |
| 18 | Fundamento SaaS IA | NEXUS_AFFIL_IA_TECH_VOL_04 | Elite |
| 19 | Poder de Processamento IA | NEXUS_AFFIL_IA_TECH_VOL_05 | Elite |

## 📄 PDFs Publicados

- ✅ 30 PDFs apostila em `AcademIA/pdfs/[0-9]-*.pdf`
- ✅ 11 PDFs webinar em `AcademIA/pdfs/webinar-WB-*.pdf`
- ✅ 10 PDFs cursos (fundamental, agent, master, elite) em `AcademIA/pdfs/curso-*.pdf`
- Total: 41 PDFs novos + 10 históricos

## 🔗 URLs em Produção

- Academia: https://oneverso.com.br/academia
- Lesson exemplo: https://oneverso.com.br/academia/lesson/fund-00
- Video CDN: https://oneverso.com.br/academia/videos/*.mp4
- PDF CDN: https://oneverso.com.br/academia/pdf/*.pdf

## 📊 Métricas (v2.0-on-50) — verificado `videos/aulas-onda-49/manifest/MASTER-PIPELINE-E2E.json`

| Categoria | Quantidade (real hoje) |
|---|---:|
| Apostilas (Markdown) | **36** (01-33 · 4 STUB com TODO: 17, 18, 32, 33) |
| Roteiros full de vídeo | **22** (00-14 + 5 âncoras TECH 15-19 + 3 misc) |
| Vídeos MP4 (ONDA-47) | **23** `videos/video-*-full.mp4` + 2 PoC |
| TS full voz PT-BR | **15** `videos/audio/full_*.wav` |
| Frames | **75** PNG motion-graphics |
| Capas 2K (ONDA-47) | **26** (PNG+WebP, 1280×720 / 2K) |
| Capas YouTube (ONDA-50) | **19** 1280×720 |
| Slides PNG (ONDA-49) | **95** (19 aulas × 5 cenas motion B2) |
| HTML wrappers (ONDA-50) | **95** (metadata + `<img>` + metadata persona/cena/narrative) |
| Renders 720p MP4 (ONDA-49) | **9** (aulas 17, 26-33) — **faltam 10** (15, 16, 18, 19, 20, 21, 22, 23, 24, 25) |
| Webinars (Markdown) | **19** (WB-01..17 + 2 debates) |
| Tutoriais (Markdown) | **36** (não 14 — INDEX legado desatualizado) |
| Playbooks | **14** (3 crises + 4 ops + federation + financeiro + LGPD + email + lançamento) |
| Treinamentos/Workshops | **9** (WS-01..06 + 3 ancilares) |
| Hubs HTML | **11** (index, landing, player, trilhas, cursos, lab, lib, apostilas, playbooks, tutoriais, webinars) |
| Apostilas HTML/PDF | 34 HTML + 23 PDF em `apostilas/` |
| Manifest canônicos | 4 (ONDA-49 MANIFEST, THUMBNAILS-ONDA-50, MASTER-ONDA-49-50, **MASTER-PIPELINE-E2E**) |
- **Tamanho total do repo**: ~700 MB
- **Head SHA**: `a71f2bc22aa3c5d85f456bcb6ff17e16858df039` (`feat(academia): ONDA-50 ...`)

### 🌊 Coletânea NEXUS AFFIL'IA'TE TECH (5 volumes PhD-level — Onda 40)

A nova coletânea técnica publicada em `docs/ebooks_markdown/colecao_NEXUS_AFFIL_IA_TECH/`
do repo legado `MMN_AI-to-AI` foi ancorada na Academia como 5 roteiros-âncora (15-19) e 5
thumbnails 2K. Cada volume trata o tema com profundidade técnica PhD-level, 10 capítulos,
≥25 páginas, checklist canônico e glossário.

- **Vol. I** — Orquestração de Ecossistemas IA · engenharia de sistemas multi-agente em produção
- **Vol. II** — Senciência e suas Barreiras · o problema difícil da consciência sintética
- **Vol. III** — O Poder x Perigo da Autonomia AI · do Copilot ao sistema fully autonomous
- **Vol. IV** — Fundamento SaaS IA · a pilha canônica de um SaaS agêntico
- **Vol. V** — Poder de Processamento IA · GPU, TPU, NPU, KV cache e o custo por token

## 📚 Catálogo de Apostilas (31)

### Trilha Fundamental & Agente (1-15)
1. Apresentação & Infraestrutura · 2. Cases Orquestração · 3. Infra Operacional IA · 4. Orquestração Híbrida · 5. 7 Telas Essenciais · 6. Setup Agente · 7. 18 Skills Operacionais · 8. Rotina Disparo · 9. Campanhas Automatizadas · 10. Jornada Afiliado · 11. SHO em Produção · 12. IOAID Arquitetura · 13. Marketplace Skills · 14. Multi-Tenant Whitelabel · 15. Métricas ROI

### Trilha Master & Elite (16-22)
16. Trilha Fundamental IA · 17. SEO & Marketing Conteúdo · 18. Segurança Ofensiva · 19. Monetização Avançada · 20. Trilha Elite Engenharia · 21. Trilha Master Arquitetura · 22. Trilha Master Mentoria

### Cursos Práticos & Avançados (23-31)
23. Curso RAG Prático · 24. Curso Agents LangGraph · 25. Curso Prompt Engineering · 26. Curso Vector DB · 27. Curso Voice AI · 28. Curso Multimodal RAG · 29. AI-to-AI Protocol (A2A) · 30. Federação Zero-Trust · 31. Fábrica de Conteúdo com IA

### Trilha Pricing & Data — Onda TECH (32-33)
32. Pricing IA 2026 · pricing dinâmico, unit economics e unit cost em escala
33. Data Stack Agentes IA · lakehouse, feature store, vector DB e observabilidade de modelos

> Formatos: `apostilas/32-pricing-ia-2026.md` · `apostilas/33-data-stack-agentes-ia.md` · `html/apostilas/*.html` · `pdfs/*.pdf`

## 🎬 Cursos slides (roteiros-âncora) — sincronizados do legado

| Trilha | Arquivo slides | Status |
|---|---|---|
| Agente (00) | `cursos/agente/00-primeiro-agente-slides.md` | ✅ |
| Elite (00) | `cursos/elite/00-blueprints-elite-slides.md` | ✅ |
| Master (00) | `cursos/master/00-otimizacao-conversao-slides.md` | ✅ |

## 🌐 Hubs HTML (4)

- `hubs/cursos.html` — índice das trilhas
- `hubs/landing.html` — landing page pública
- `hubs/player.html` — player de vídeo/áudio
- `hubs/trilhas.html` — seletor de trilhas com profiles

## 🎥 Catálogo de Webinars (15)
- WB-01 Lançamento IOAID · WB-02 SHO em Produção · WB-03 Open House
- WB-04 Skills em Produção · WB-05 Multi-Tenant · WB-06 A/B Test Estatístico · WB-07 LGPD & IA
- WB-08 CFO/AI Otto · Unit Economics
- WB-09 Agentes Autônomos em Produção
- WB-10 SEO vs IA Generativa · WB-11 Burnout em Affiliates
- WB-12 IA-to-IA Federation
- WB-13 Criação de Conteúdo com IA
- **WB-2026-08 Financeiro IA** · `webinars/WB-2026-08-financeiro-ia.md` + HTML + PDF
- **WB-2026-12 IA-to-IA Federation** · HTML + PDF
- **WB-2026-14 Pricing IA em tempo real** · `webinars/WB-2026-14-pricing-ia-tempo-real.md` + HTML + PDF
- **WB-2026-15 Data Stack IA** · `webinars/WB-2026-15-data-stack-ia.md` + HTML + PDF

## 🌊 Estado Onda-49/50 (visíveis em `videos/aulas-onda-49/`)

> 19 aulas canônicas completas (15-33) — cada uma com: roteiro MD + 5 slides PNG motion-B2 + 5 wrappers HTML + capa YouTube + render MP4 (parcial).

### Por trilha:

| Trilha | Aulas | Capas | Slides PNG | HTML wraps | Render 720p |
|---|---:|---:|---:|---:|---:|
| Fundamental | 2 (15-16) | 2 ✅ | 10 ✅ | 10 ✅ | 0 ❌ (pendente 15, 16) |
| Master | 13 (17, 19, 21-22, 23-28, 31-32) | 13 ✅ | 65 ✅ | 65 ✅ | 7 ✅ (faltam 19, 21-25) |
| Elite | 4 (18, 20, 29-30) | 4 ✅ | 20 ✅ | 20 ✅ | 1 ✅ (faltam 18, 20) |
| Dupla | (varia) | 7 ✅ | (ver MASTER-PIPELINE-E2E.json) | | |

### Gaps do pipeline (próximas ações):

1. **Renderar 10 MP4s 720p** faltantes do ONDA-49 (aulas 15, 16, 18, 19, 20, 21, 22, 23, 24, 25).
2. **Resolver 4 STUBs** em apostilas 17, 18, 32, 33 (zerar TODOs).
3. **Gerar PDFs** das 19 apostilas ONDA-49 (pandoc/xelatex ausentes → rota com `wkhtmltopdf` ou via `pdfs/` herdado).
4. **Criar `scripts/generate_apostilas_pdf.py`** para conversão MD→PDF em lote (template HUB57).
5. **Aplicar governança do split** em novos conteúdos para evitar duplicação entre Academ'IA e Marketplace Nexus.

## 🛠️ Producao · Incident Response (TI)

- `producao/INCIDENT-RESPONSE-RUNBOOK.md` — runbook 1 página: severidades (SEV-1/2/3), contatos, RCA template, comunicação pública, lições aprendidas.

## 🖼️ Personas · Assets de referência (5)

- **Alencar**: `alencar_meeting_v1.png`, `alencar_nexus_ref_1.png` (~4 MB cada)
- **Ive**: `ive_nexus_ref_1.png`, `ive_reference.png`, `ive_training_v1.png` (~4 MB cada)

## 🎥 Vídeo PoC (1)

- `videos/video-00-boas-vindas-poc.mp4` (~2 MB) — boas-vindas PoC para a trilha Fundamental.

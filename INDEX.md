# 📚 AcademIA Nexus Affil'IA'te · INDEX Master

**Última atualização**: 2026-07-21 · Mavis + contribuidor paralelo + sync legado (Academ-IA repo)
**Total**: 33 apostilas · 17 roteiros · 20 thumbnails · 13 webinars (+4 webinars TECH 14-15) · 8 PDFs apostila · 17 PDFs webinar · 48 HTMLs (+4 hubs) · 30+ capas AcademIA
**Versão**: 1.4.1 (Onda 40) — NEXUS AFFIL'IA'TE TECH + sync repo dedicado

> 🌊 **Onda 40** — integração com a nova coletânea técnica NEXUS AFFIL'IA'TE TECH
> (5 ebooks PhD-level espelhados como 5 roteiros-âncora: 15-19).

## 🎯 Estrutura Oficial (Fonte da Verdade)

```
AcademIA/
├── INDEX.md              ← este arquivo (mapa completo)
├── README.md             ← overview público
├── CHANGELOG.md          ← histórico de mudanças
├── RESUMO_EXECUTIVO.md   ← visão executiva
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
├── personas/             ← Ive, Alencar, Helena, Ravi, Otto (138 MB)
├── marca/                ← Brand kit (17 MB)
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

## 📊 Métricas (v1.4.0)

- 855+ arquivos Markdown (documentação)
- 41 PDFs apostilas/webinars + 10 PDFs cursos históricos
- 6 vídeos MP4 (aulas) + 20 thumbnails
- 17 roteiros de vídeo (5 âncoras TECH novos)
- 41 HTMLs (renderizações com enhance.js)
- 6 JSONs (manifestos e sync)
- 30+ capas AcademIA (1-15 + 16, 20-28 + 5 TECH 15-19)
- **Total**: ~566 MB no repo (migração para repo dedicado `Nexus-HUB57/Academ-IA`)
- **Total servido publicamente**: ~68 MB

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

## 🛠️ Producao · Incident Response (TI)

- `producao/INCIDENT-RESPONSE-RUNBOOK.md` — runbook 1 página: severidades (SEV-1/2/3), contatos, RCA template, comunicação pública, lições aprendidas.

## 🖼️ Personas · Assets de referência (5)

- **Alencar**: `alencar_meeting_v1.png`, `alencar_nexus_ref_1.png` (~4 MB cada)
- **Ive**: `ive_nexus_ref_1.png`, `ive_reference.png`, `ive_training_v1.png` (~4 MB cada)

## 🎥 Vídeo PoC (1)

- `videos/video-00-boas-vindas-poc.mp4` (~2 MB) — boas-vindas PoC para a trilha Fundamental.

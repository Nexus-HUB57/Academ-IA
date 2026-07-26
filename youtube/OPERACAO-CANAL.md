---
title: "Operação do Canal YouTube · Academ'IA"
description: "Documento canônico de operação, manutenção e crescimento do canal @NexusAffilIAte-w9p"
tags: [youtube, canal, operacao, privacidade, publicacao, visibilidade, manutencao]
version: 1.0.0
last_updated: 2026-07-25
pattern: "MMN_IA"
channel: "@NexusAffilIAte-w9p"
---

# 📺 Operação do Canal YouTube · Academ'IA

> **Documento canônico** de operação, manutenção e crescimento do canal **[@NexusAffilIAte-w9p](https://www.youtube.com/@NexusAffilIAte-w9p)**. Source of truth para procedimentos relacionados a upload, privacidade, thumbnails, e visibilidade pública.

## 🎯 Estado Atual (snapshot 2026-07-25)

| Status | Qtd | % | Visível para audiência? |
|--------|-----|---|--------------------------|
| 🌍 **Public** | 1 | 5% | **SIM** — aparece em buscas e feed |
| 🔒 **Unlisted** | 10 | 48% | NÃO — só com link direto |
| 🔐 **Private** | 11 | 52% | NÃO — só owner |
| **Total upados** | **21** | — | — |
| ❌ **Não upados** | 0 | 0% | Pendente: re-upload por limite diário |

**Vídeo público único:** [Boas-vindas aos Novos Afil'IA'dos](https://www.youtube.com/watch?v=cBhbg51peQk) (code legado, código 00 do plano original).

**Causa raiz da baixa visibilidade:** a operação de upload (em ~24-25/jul) priorizou **segurança sobre visibilidade** — subiu todos como `unlisted`/`private` para evitar exposição prematura antes de validação final. Os 5 codes 09-13 ficaram bloqueados por `uploadLimitExceeded`.

## 📋 Plano de Publicação (15 vídeo-aulas)

Source: `youtube/publish_plan.json` (canônico)

| Code | Trilha | Título | Status Atual |
|------|--------|--------|--------------|
| 00 | Fundamental | Boas-vindas à AcademIA Nexus | 🔒 unlisted |
| 01 | Fundamental | Entendendo o IOAID | 🔒 unlisted |
| 02 | Fundamental | O Sistema SHO (Self-Healing Orchestrator) | 🔒 unlisted |
| 03 | Fundamental | Painel do Afiliado — Visão Geral | 🔒 unlisted |
| 04 | Agente | Construindo Seu Primeiro Agente em 4 Minutos | 🔒 unlisted |
| 05 | Agente | Skills Essenciais — Copywriter + Audience-Segmenter | 🔒 unlisted |
| 06 | Agente | Disparando no WhatsApp em Escala | 🔒 unlisted |
| 07 | Agente | Judge Revisor — A IA que Decide por Você | 🔒 unlisted |
| 08 | Master | Otimização de Conversão — A Matemática da Receita | 🔒 unlisted |
| 09 | Master | Funis e Lifecycle — O Sistema Completo | ❌ pendente (limit) |
| 10 | Master | A/B Testing com Judge — Ciência da Experimentação | ❌ pendente (limit) |
| 11 | Master | Análise de Coortes e Churn — A Arte de Reter | ❌ pendente (limit) |
| 12 | Elite | Blueprints Elite — O Jogo do Top 10% | ❌ pendente (limit) |
| 13 | Elite | Multi-Tenant e White-Label na Prática | ❌ pendente (limit) |
| 14 | Elite | Federação de Agentes Zero-Trust | 🔒 unlisted |

## 🛠️ Procedimentos de Operação

### Procedimento 1 — Liberar vídeos existentes (unlisted → public)

Quando todos os vídeos de uma trilha estiverem validados internamente, é hora de virar `public`.

**Script:** [`scripts/youtube_set_privacy_public.py`](../scripts/youtube_set_privacy_public.py)

**Pré-requisitos:**

1. **Credenciais YouTube Data API v3** salvas em `youtube/client_secret.json` (NÃO versionar).
2. Token OAuth2 em `youtube/token.json` (gerado no primeiro uso do script).
3. Ambos os arquivos devem estar no `.gitignore`.

**Comandos:**

```bash
# Dry-run primeiro (recomendado)
python3 scripts/youtube_set_privacy_public.py --all --dry-run

# Liberar todos os unlisted/private
python3 scripts/youtube_set_privacy_public.py --all

# Liberar apenas codes específicos
python3 scripts/youtube_set_privacy_public.py --codes 00,01,02,03
```

**Quem pode executar:** Head de Operações, SRE Lead, ou alguém com delegação.

### Procedimento 2 — Re-upload dos códigos pendentes (09-13)

Quando o limite diário do canal resetar (a cada 24h, conta padrão: ~6 uploads/dia).

**Script:** [`scripts/youtube_upload_pending.py`](../scripts/youtube_upload_pending.py)

**Pré-requisitos:**

1. Arquivos de vídeo e thumbnail **disponíveis nos caminhos declarados** em `publish_plan.json` (atualmente `/var/www/oneverso/current/...`).
2. Credenciais YouTube (mesmas do Procedimento 1).

**Comandos:**

```bash
# Listar pendentes (sem upload)
python3 scripts/youtube_upload_pending.py --dry-run

# Upload de 1 code (recomendado para evitar rate limit)
python3 scripts/youtube_upload_pending.py --code 09
python3 scripts/youtube_upload_pending.py --code 10
# ... etc

# Upload de todos de uma vez (risco de rate limit)
python3 scripts/youtube_upload_pending.py

# Forçar privacidade public (após Procedimento 1)
python3 scripts/youtube_upload_pending.py --code 09 --public
```

**Após upload:** o script atualiza automaticamente `publish_plan.json` e `upload_results.json`.

### Procedimento 3 — Auditoria semanal de sincronização

Roda semanalmente para garantir que o estado do canal reflete o que está no repo.

**Script:** [`scripts/audit_youtube_publication_sync.py`](../scripts/audit_youtube_publication_sync.py)

**Comando:**

```bash
python3 scripts/audit_youtube_publication_sync.py
```

**Output:**

- `docs/AUDITORIA_PUBLICACAO_YOUTUBE_*.md` — relatório human-readable
- `docs/AUDITORIA_PUBLICACAO_YOUTUBE_*.json` — relatório machine-readable

**Métricas auditadas:**

- Total no publish plan
- Uploads concluídos vs prontos vs pendentes
- Descrições `.txt` e thumbnails presentes
- Erros por categoria (upload limit, descrição inválida, outros)
- Status codes (public/unlisted/private)

## 🛡️ Convenções de Privacidade

| Cenário | Status Recomendado | Justificativa |
|---------|---------------------|---------------|
| Material em produção, ainda em revisão interna | 🔐 **private** | Evita exposição prematura; só owner vê |
| Material finalizado, ainda em testes de QA | 🔒 **unlisted** | Permite share com stakeholders via link, sem aparecer em buscas |
| Material aprovado e pronto para audiência | 🌍 **public** | Visível para todos, aparece em buscas, recomendado pelo YouTube para engajamento |
| Material descontinuado ou substituído | 🔒 **unlisted** | Mantém acessível para quem já viu, mas tira das recomendações |
| Material com erro (áudio cortado, slide errado) | 🔐 **private** | Aguardando correção; se voltar a public, refazer com novo video_id |

## 🚦 Fluxo Recomendado de Publicação

```
[Criação do vídeo] → [Validação interna QA] → [Upload como PRIVATE]
                                              ↓
                                       [Validação stakeholders]
                                              ↓
                                  [Mudar para UNLISTED] (link compartilhável)
                                              ↓
                                       [Soft launch] (5-10 personas)
                                              ↓
                                  [Mudar para PUBLIC] (lançamento oficial)
                                              ↓
                                       [Marketing + cross-post]
```

## 🔐 Segurança

### Arquivos sensíveis (NÃO versionar)

```gitignore
# .gitignore (adicionar)
youtube/client_secret.json
youtube/token.json
youtube/*-oauth-credentials.json
```

### Permissões de execução dos scripts

- **`youtube_set_privacy_public.py`** — apenas Head de Operações / SRE Lead.
- **`youtube_upload_pending.py`** — apenas com dupla aprovação (operador + head).
- **`audit_youtube_publication_sync.py`** — qualquer um (read-only).

### Rate limits

| Plano YouTube | Uploads/dia | API units/dia | Custo por upload |
|---------------|-------------|---------------|-------------------|
| **Não verificado** | 5-7 | 10.000 | ~1.600 |
| **Verificado** | 15-20 | 100.000 | ~1.600 |
| **Premium API** | sem limite | 1.000.000 | negociado |

> **Regra prática:** máximo 5 uploads/dia (não verificado) ou 15/dia (verificado).

## 📊 KPIs do Canal

| Métrica | Target Q3 2026 | Como medir |
|---------|----------------|------------|
| Vídeos public no canal | 15/15 (100%) | `audit_youtube_publication_sync.py` |
| Taxa de upload sucesso | >95% | `upload_results.json` |
| Visualizações (90 dias) | >5.000 | YouTube Studio |
| Inscritos | >200 | YouTube Studio |
| Watch time médio | >60% | YouTube Studio |
| CTR médio | >4% | YouTube Studio |
| Comentários por vídeo | >3 | YouTube Studio |

## 🔄 Workflow de Atualização do Plano

Quando um novo material entra no pipeline:

1. **Adicionar** entrada em `youtube/publish_plan.json` (código, título, paths).
2. **Adicionar** linha em `youtube/publish_plan.csv` (mesmas colunas).
3. **Se for upload imediato**: incluir em `youtube/upload_batch_ready.json`.
4. **Após upload**: script atualiza `publish_plan.json` (status=uploaded) e `upload_results.json` (novo entry).
5. **Após validação QA**: rodar `youtube_set_privacy_public.py` para mudar privacidade.

## 🔌 Integração com Fila de Re-povoamento (25-jul-2026)

Em 25/jul/2026, outro dev criou a **fila de re-povoamento** baseada nos vídeos REBUILDADOS
(padrão 1280x720@25fps, 60-240s), em `youtube/upload_queue_repovoamento_2026-07-25.json`.
Esta fila é **complementar** à `upload_batch_ready.json` (original):

| Fila | Origem | Estado |
|------|--------|--------|
| `upload_batch_ready.json` | original (5 codes 09-13) | Pendente há dias |
| `upload_queue_repovoamento_2026-07-25.json` | rebuild (15 codes 00-14) | 14 prontos + 1 fora do padrão |

**Recomendação:** usar a **fila de re-povoamento** como source of truth, já que os vídeos
foram reconstruídos com qualidade consistente.

O script [`../scripts/build_youtube_repovoamento_queue.py`](../scripts/build_youtube_repovoamento_queue.py)
gera esta fila automaticamente a partir do `MANIFESTO_REBUILD_VIDEO_AULAS_00_14_2026-07-24.json`.

### Como usar a fila de re-povoamento

```bash
# 1. Gerar/atualizar fila
python3 scripts/build_youtube_repovoamento_queue.py

# 2. Visualizar fila
cat youtube/upload_queue_repovoamento_2026-07-25.json | python3 -m json.tool

# 3. Upload de codes específicos (Mavis Agent — 25-jul)
# Requer customização: usar o script youtube_upload_pending.py
# e passar --queue-file youtube/upload_queue_repovoamento_2026-07-25.json
```

**Nota:** O script `youtube_upload_pending.py` (Mavis) lê por padrão
`upload_batch_ready.json`. Para usar a fila de re-povoamento, copiar o conteúdo
de `upload_queue_repovoamento_2026-07-25.json` para `upload_batch_ready.json`
OU customizar o script para aceitar `--queue-file`.

## 📂 Estrutura

```
youtube/
├── OPERACAO-CANAL.md              ← este arquivo
├── README.md                       ← visão editorial
├── publish_plan.json               ← plano canônico
├── publish_plan.csv                ← plano em CSV
├── upload_batch_ready.json         ← fila de upload (original, 5 codes)
├── upload_queue_repovoamento_2026-07-25.json  ← fila rebuild (15 codes)
├── upload_results.json             ← resultados de upload
├── descriptions/                   ← 15 .txt (uma por vídeo)
├── thumbnails/                     ← 15 .png (thumbnails)
├── thumbnails_yt/                  ← 15 .jpg (variantes)
├── videos_teaser/                  ← 13 .mp4 (teasers locais)
├── teaser_aliases.json             ← aliases de teasers
├── RUNBOOK-POVOAR-CANAL.md         ← passo a passo executável
├── client_secret.json              ← ⚠️ NÃO VERSIONAR
└── token.json                      ← ⚠️ NÃO VERSIONAR
```

## 🔗 Links Cruzados

- [`../producao/PIPELINE_PRODUCAO.md`](../producao/PIPELINE_PRODUCAO.md) — Pipeline de produção
- [`../producao/catalog/CATALOGO_MODULOS.md`](../producao/catalog/CATALOGO_MODULOS.md) — Catálogo de módulos
- [`../materiais/video-aulas/INDEX.md`](../materiais/video-aulas/INDEX.md) — Índice de vídeo-aulas
- [`../docs/AUDITORIA_PUBLICACAO_YOUTUBE_2026-07-24.md`](../docs/AUDITORIA_PUBLICACAO_YOUTUBE_2026-07-24.md) — Última auditoria
- [`../docs/ACADEMIA_MANIFEST_OPERACIONAL_2026-07-24.md`](../docs/ACADEMIA_MANIFEST_OPERACIONAL_2026-07-24.md) — Manifesto operacional
- [`../GUIA_MULTI_DEV.md`](../GUIA_MULTI_DEV.md) — Convenções multi-dev

## 👥 Ownership

- **Owner:** Head de Operações + SRE Lead
- **Mantenedor:** Equipe de produção
- **Cadência de revisão:** Mensal (KPIs) / Trimestral (procedimentos)

---

*Nexus Affil'IA'te · youtube/OPERACAO-CANAL.md · v1.0.0 · Julho 2026*

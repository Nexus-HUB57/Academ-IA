# Manifesto Operacional da Academia

## Resumo canônico
- Total no publish plan: **15**
- Total rebuild concluído: **15** (14 padrão + 1 fora)
- Publicados no YouTube: **21** (1 legado público + 20 unlisted/private — inclui duplicações)
- Fila de re-povoamento: **15** (codes 00-14 com masters rebuild)
- Prontos para upload (padrão 60-240s): **14**
- Curtos fora do padrão (<60s ou >240s): **1** (code 00, 261.6s)
- Erros por limite do canal: **72**
- Erros de descrição inválida: **1**
- **Visibilidade pública atual:** 🌍 **1 vídeo público** (code legado `cBhbg51peQk`)

## Estado por código (com base no rebuild 25-jul)

| Code | Trilha | Persona | Master | Duração | Padrão | Status |
|------|--------|---------|--------|---------|--------|--------|
| 00 | fundamental | alencar | ✅ | 261.6s | ⚠️ >240s | re-narrar antes de upload |
| 01 | fundamental | ive | ✅ | 118.7s | ✅ | pronto |
| 02 | fundamental | alencar | ✅ | 123.6s | ✅ | pronto |
| 03 | fundamental | dupla | ✅ | 131.2s | ✅ | pronto |
| 04 | agente | alencar | ✅ | 136.0s | ✅ | pronto |
| 05 | agente | alencar | ✅ | 131.7s | ✅ | pronto |
| 06 | agente | alencar | ✅ | 125.6s | ✅ | pronto |
| 07 | agente | alencar | ✅ | 167.2s | ✅ | pronto |
| 08 | master | dupla | ✅ | 126.0s | ✅ | pronto |
| 09 | master | dupla | ✅ | 118.7s | ✅ | pronto |
| 10 | master | dupla | ✅ | 122.8s | ✅ | pronto |
| 11 | master | dupla | ✅ | 118.2s | ✅ | pronto |
| 12 | elite | dupla | ✅ | 120.8s | ✅ | pronto |
| 13 | elite | alencar | ✅ | 119.1s | ✅ | pronto |
| 14 | elite | dupla | ✅ | 119.8s | ✅ | pronto |

## Vídeos atuais no YouTube (estado de privacidade)

| Code | Status | Visibilidade |
|------|--------|--------------|
| Legado (cBhbg51peQk) | 🌍 public | ✅ visível |
| 00 | 🔒 unlisted | ⚠️ só com link |
| 01 | 🔒 unlisted | ⚠️ só com link |
| 02 | 🔒 unlisted | ⚠️ só com link |
| 03 | 🔒 unlisted | ⚠️ só com link |
| 04 | 🔒 unlisted | ⚠️ só com link |
| 05 | 🔒 unlisted | ⚠️ só com link |
| 06 | 🔒 unlisted | ⚠️ só com link |
| 07 | 🔒 unlisted | ⚠️ só com link |
| 08 | 🔒 unlisted | ⚠️ só com link |
| 09 | ❌ não upado | ❌ pendente |
| 10 | ❌ não upado | ❌ pendente |
| 11 | ❌ não upado | ❌ pendente |
| 12 | ❌ não upado | ❌ pendente |
| 13 | ❌ não upado | ❌ pendente |
| 14 | 🔒 unlisted | ⚠️ só com link |

## Scripts e ferramentas (Mavis Agent · 2026-07-25)

### Para mudar privacidade (unlisted/private → public)
- `scripts/youtube_set_privacy_public.py` (Mavis)
- Opera sobre `youtube/upload_results.json`

### Para fazer upload
- `scripts/youtube_upload_pending.py` (Mavis) — usa `youtube/upload_batch_ready.json`
- `scripts/build_youtube_repovoamento_queue.py` (Mavis) — gera `youtube/upload_queue_repovoamento_2026-07-25.json`

### Documentação
- `youtube/OPERACAO-CANAL.md` (Mavis) — procedimentos canônicos
- `youtube/RUNBOOK-POVOAR-CANAL.md` (Mavis) — passo a passo executável
- `docs/FILA_YOUTUBE_REPOVOAMENTO_2026-07-25.md` (Mavis) — fila atual

## Operação recomendada (Mavis Agent)
Ver `youtube/RUNBOOK-POVOAR-CANAL.md` para o passo a passo executável.

**Ordem sugerida:**
1. Re-narrar code 00 (único fora do padrão)
2. Upload dos 14 codes no padrão (1-3 dias por rate limit)
3. Mudar privacidade de todos para `public`
4. Validar que canal tem 15 vídeos públicos (1 legado + 14 novos)

## Fonte canônica
- Publicação original: `youtube/publish_plan.json`
- Fila antiga: `youtube/upload_batch_ready.json`
- Fila rebuild: `youtube/upload_queue_repovoamento_2026-07-25.json`
- Resultados: `youtube/upload_results.json`
- Manifest rebuild: `docs/MANIFESTO_REBUILD_VIDEO_AULAS_00_14_2026-07-24.json`
- Catálogo operacional: `producao/catalog/CATALOGO_MODULOS.md`

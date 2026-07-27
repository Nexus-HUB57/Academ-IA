---
title: "Runbook · Povoar Canal YouTube Academ'IA"
description: "Passo a passo para liberar 20 vídeos (unlisted/private → public) e subir os 5 pendentes (codes 09-13)"
tags: [youtube, runbook, povoar-canal, privacidade, upload, publicacao, operacional]
version: 1.0.0
last_updated: 2026-07-25
urgency: high
estimated_time: "30-60 min (depende do rate limit)"
pattern: "MMN_IA"
---

# 🚀 Runbook · Povoar Canal YouTube Academ'IA

> **Passo a passo operacional** para popular o canal **[@NexusAffilIAte-w9p](https://www.youtube.com/@NexusAffilIAte-w9p)** de **1 vídeo público** para **15 vídeos públicos**. Procedimento guiado com verificação de segurança em cada etapa.

## 🎯 Objetivo

Levar o canal de:
- **Antes:** 1 public, 10 unlisted, 10 private, 5 pendentes (canal com cara de "vazio")
- **Depois:** 15 public, todos validados, índice YouTube completo

## ⏱️ Tempo Estimado

- **Setup inicial (1ª vez):** 30-45 min (criar projeto Google Cloud, OAuth, instalar deps)
- **Liberação de vídeos existentes:** 5-10 min
- **Upload de 5 pendentes (limit diário):** 1-3 dias (6 uploads/dia)

## 📋 Pré-requisitos

### Infraestrutura

- [ ] **Python 3.10+** instalado
- [ ] Acesso ao servidor onde estão os arquivos físicos (`/var/www/oneverso/current/...`)
- [ ] **Credenciais Google Cloud** com YouTube Data API v3 habilitada

### Permissões

- [ ] Acesso de **owner** ao canal YouTube `@NexusAffilIAte-w9p`
- [ ] Acesso de **owner** ao Google Cloud Project associado
- [ ] Capacidade de **editar** o canal e mudar privacidade de vídeos

### Validação interna

- [ ] **Head de Operações** confirma que os 10 vídeos unlisted passaram por QA
- [ ] **Head de Marca** confirma que thumbnails e títulos estão aprovados
- [ ] **DPO** confirma que nenhum vídeo expõe PII indevida

## 🛠️ FASE 1 — Setup Inicial (uma vez só)

### 1.1. Criar projeto Google Cloud

1. Acesse https://console.cloud.google.com
2. Crie projeto "AcademIA-Nexus" (ou use existente)
3. Habilite **YouTube Data API v3**:
   - Menu → APIs & Services → Library
   - Buscar "YouTube Data API v3" → Enable
4. Configure **OAuth Consent Screen**:
   - User type: **External**
   - App name: "AcademIA Nexus Channel Manager"
   - Scopes: `youtube.force-ssl` e `youtube.upload`
   - Test users: adicione o email do owner do canal
5. Crie **OAuth 2.0 Client ID**:
   - Application type: **Desktop app** (recomendado)
   - Name: "AcademIA-Nexus-CLI"
   - Download JSON e salve em `youtube/client_secret.json`

### 1.2. Instalar dependências

```bash
pip install google-api-python-client google-auth-oauthlib
```

### 1.3. Verificar arquivo de credenciais

```bash
ls -la /workspace/Academ-IA/youtube/client_secret.json
# Deve existir, com permissões 600 (apenas você lê)
chmod 600 /workspace/Academ-IA/youtube/client_secret.json
```

### 1.4. Confirmar .gitignore

```bash
cat /workspace/Academ-IA/youtube/.gitignore
# Deve listar client_secret.json e token.json
```

## 🔓 FASE 2 — Liberar Vídeos Existentes (unlisted → public)

### 2.1. Dry-run (verificar o que será alterado)

```bash
cd /workspace/Academ-IA
python3 scripts/youtube_set_privacy_public.py --all --dry-run
```

**Saída esperada:**

```
📋 Total upados: 21
🎯 Alvos: 20
   🔒 code=00 unlisted https://youtube.com/watch?v=txsJDc1oxps
   🔒 code=01 unlisted https://youtube.com/watch?v=bSabrgNNgik
   ... (todos os 20 unlisted/private)
🔍 DRY-RUN: nenhuma alteração feita.
```

**Checklist:**

- [ ] Os 20 vídeos listados correspondem ao esperado?
- [ ] Os video_ids batem com `upload_results.json`?
- [ ] Não há code duplicado ou código errado?

### 2.2. Execução (liberação real)

```bash
python3 scripts/youtube_set_privacy_public.py --all
```

**Saída esperada:**

```
🔐 Autenticando no YouTube...
   <janela do browser abre para OAuth>
✅ Autenticado.

🚀 Aplicando mudança de privacidade...

   ✅ code=00 txsJDc1oxps → public
   ✅ code=01 bSabrgNNgik → public
   ... (20 sucessos)

📊 Resumo: 20 ok, 0 skip, 0 erro
```

**Se aparecer erro:**

| Erro | Causa | Solução |
|------|-------|---------|
| `403 quotaExceeded` | API quota do Google Cloud estourou | Aguardar reset (24h) ou upgradar |
| `403 forbidden` | Credenciais sem permissão de `youtube.force-ssl` | Revogar e re-autorizar OAuth |
| `404 notFound` | video_id incorreto | Validar em `upload_results.json` |
| `Token expirado` | Token antigo | Deletar `token.json` e re-rodar |

### 2.3. Validar resultado

1. Abra https://www.youtube.com/@NexusAffilIAte-w9p/videos
2. Confirme que os 20 vídeos agora aparecem como **públicos**
3. Tente acessar cada um por link direto
4. Verifique se o vídeo legado (code 00 antigo `cBhbg51peQk`) ainda está público

**Checklist pós-liberação:**

- [ ] Canal mostra 21 vídeos públicos (1 legado + 20 novos)
- [ ] Cada vídeo tem thumbnail correto
- [ ] Cada vídeo tem descrição completa
- [ ] Não há vídeos com `unlisted` ou `private` "vazando" para public por engano

## 📤 FASE 3 — Upload dos 5 Pendentes (codes 09-13)

### 3.1. Validar que arquivos físicos existem

```bash
# Para cada code 09-13, verificar:
ls -la /var/www/oneverso/current/public/academia/videos/video-09-funis-e-lifecycle.mp4
ls -la /var/www/oneverso/current/AcademIA/youtube/thumbnails/09-funis-e-lifecycle-o-sistema-completo.png
```

**Se algum arquivo não existir:**

- [ ] Verificar com equipe de produção (Head de Produção)
- [ ] Aguardar rebuild
- [ ] Atualizar `publish_plan.json` com o novo path

### 3.2. Dry-run

```bash
python3 scripts/youtube_upload_pending.py --dry-run
```

**Saída esperada:**

```
📋 Alvos: 5
   [ready_to_upload     ] code=09  Funis e Lifecycle — O Sistema Completo
      video: /var/www/oneverso/.../video-09-funis-e-lifecycle.mp4
      thumb: /var/www/oneverso/.../09-funis-e-lifecycle-o-sistema-completo.png
   ... (4 mais)

🔍 DRY-RUN: nenhuma alteração feita.
```

### 3.3. Upload (1 por vez, respeitando rate limit)

```bash
# Day 1: codes 09, 10, 11 (3 uploads)
python3 scripts/youtube_upload_pending.py --code 09
python3 scripts/youtube_upload_pending.py --code 10
python3 scripts/youtube_upload_pending.py --code 11

# Day 2: codes 12, 13 (2 uploads)
python3 scripts/youtube_upload_pending.py --code 12
python3 scripts/youtube_upload_pending.py --code 13
```

**Por que 1 por vez?**

- Limite do YouTube não verificado: ~6 uploads/dia
- Cada upload custa ~1.600 API units
- Conta não verificada: 10.000 units/dia (sobram 1.600 se 1 falhar)
- Conta verificada: 100.000 units/dia (margem confortável)

**Saída esperada de cada upload:**

```
🚀 Iniciando uploads...

   📤 code=09 uploading...
   ✅ code=09 uploaded: https://youtu.be/abc123XYZ
   🖼️  thumb set

📊 Resumo: 1 ok, 0 erro
💾 Atualizado: upload_results.json, publish_plan.json
```

### 3.4. Validar resultado

1. Abra https://www.youtube.com/@NexusAffilIAte-w9p/videos
2. Confirme que os 5 novos vídeos aparecem
3. Verifique se o script já setou como `unlisted` (padrão seguro)
4. Quando QA aprovar, rodar Procedimento 1 para virar `public`

## 📊 FASE 4 — Validação Final

### 4.1. Rodar auditoria

```bash
python3 scripts/audit_youtube_publication_sync.py
```

**Verificar no output:**

- [ ] `publish_plan_total: 15`
- [ ] `uploaded_count: 15` (todos!)
- [ ] `ready_to_upload_count: 0`
- [ ] `description_count: 15`
- [ ] `thumb_png_count: 15`
- [ ] `thumb_jpg_count: 15`

### 4.2. Confirmar visualmente

1. **Canal principal:** https://www.youtube.com/@NexusAffilIAte-w9p
   - Deve mostrar 15+ vídeos públicos
   - Thumbnailpad consistente
   - Títulos seguindo padrão "AcademIA Nexus • NN | Título"

2. **Estrutura por playlist (se houver):**
   - Fundamentos (00-03)
   - Agentes (04-07)
   - Master (08-11)
   - Elite (12-14)

3. **Vídeos relacionados:**
   - Cada vídeo tem "cards" apontando para o próximo

### 4.3. Registrar resultado

Atualizar `docs/ACADEMIA_MANIFEST_OPERACIONAL_*.md` com a nova contagem:

```diff
- Publicados no YouTube: 10
+ Publicados no YouTube: 15
- Prontos para nova tentativa: 5
+ Prontos para nova tentativa: 0
- Erros por limite do canal: 72
+ Erros por limite do canal: 0
```

## 🛡️ Rollback (se algo der errado)

### Cenário: vídeo foi para public por engano

```bash
# Mudar de volta para private
python3 -c "
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import sys
sys.path.insert(0, '/workspace/Academ-IA/scripts')
# Reaproveita o mesmo client_secret.json e token.json
creds = Credentials.from_authorized_user_file('/workspace/Academ-IA/youtube/token.json')
youtube = build('youtube', 'v3', credentials=creds)
youtube.videos().update(
    part='status',
    body={'id': 'VIDEO_ID_AQUI', 'status': {'privacyStatus': 'private'}}
).execute()
print('OK')
"
```

### Cenário: vídeo novo foi upado com erro

1. **Não deletar** (mantém histórico)
2. Mudar para `private`
3. Corrigir arquivo físico
4. Re-rodar `youtube_upload_pending.py --code XX` (gera novo video_id)

## 📞 Contatos

- **Head de Operações:** ops-lead@nexus.io
- **SRE Lead:** sre-lead@nexus.io
- **Head de Marca:** brand-lead@nexus.io
- **DPO:** dpo@nexus.io
- **YouTube channel owner:** (definir internamente)

## 🔗 Documentos Relacionados

- [`OPERACAO-CANAL.md`](OPERACAO-CANAL.md) — Procedimentos e estado do canal
- [`../docs/AUDITORIA_PUBLICACAO_YOUTUBE_2026-07-24.md`](../docs/AUDITORIA_PUBLICACAO_YOUTUBE_2026-07-24.md) — Última auditoria
- [`../docs/ACADEMIA_MANIFEST_OPERACIONAL_2026-07-24.md`](../docs/ACADEMIA_MANIFEST_OPERACIONAL_2026-07-24.md) — Manifesto
- [`../producao/PIPELINE_PRODUCAO.md`](../producao/PIPELINE_PRODUCAO.md) — Pipeline de produção
- [`../materiais/video-aulas/INDEX.md`](../materiais/video-aulas/INDEX.md) — Índice de vídeo-aulas
- [`../GUIA_MULTI_DEV.md`](../GUIA_MULTI_DEV.md) — Convenções multi-dev

## 👥 Ownership

- **Owner:** Head de Operações + SRE Lead
- **Reviewers:** Head de Marca, DPO
- **Cadência de revisão:** Trimestral

---

*Nexus Affil'IA'te · youtube/RUNBOOK-POVOAR-CANAL.md · v1.0.0 · Julho 2026*

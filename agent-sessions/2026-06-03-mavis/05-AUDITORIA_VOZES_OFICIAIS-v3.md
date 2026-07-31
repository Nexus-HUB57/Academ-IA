---
session_id: 404996140855418
agent: Mavis (MiniMax-M3)
session_type: root
data_sessao: 2026-06-02T16:37:00Z — 2026-06-03T11:55:00Z
data_revisao_v1: 2026-07-23
data_revisao_v2: 2026-07-24
data_revisao_v3: 2026-07-29
data_migracao: 2026-07-24
branch: main
gerado_por: IA (modelo MiniMax-M3, instância desta sessão)
contexto_sessao: Auditoria complementar do registro canônico de vozes oficiais (v3.0, pós-force-push 2026-07-29)
escopo: Verificação cruzada entre registros canônicos de vozes + inspeção de arquivos em marca/personas/{alencar,ive}/audio/ + impacto do force-push + novos docs
nota_proveniencia: Output de sessão de chat IA. Para reuso, citação ou auditoria, referenciar session_id e data_sessao.
categoria: governanca-vozes / auditoria
versao: 3.0 (atualizada 2026-07-29 com dados pós-force-push e +33 commits)
audiencia: time de produção de áudio/vídeo, owner, auditores
conflito_multi_dev: NENHUM. Pasta `agent-sessions/` é nova; este arquivo não sobrescreve nenhum existente no remote.
referencias_canonicas_remoto:
  - marca/personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md
  - marca/personas/OFFICIAL_VOICES.md
  - marca/personas/VOZES-OFICIAIS.md
  - marca/personas/VOICES.md
  - GUIA_VOZES_OFICIAIS.md (raiz, LEGADO — path antigo)
  - GUIA-VOZES-OFICIAIS.md (raiz, novo — path correto)
  - marca/INDEX.md
  - agent-sessions/INDEX.md
---

# Auditoria das Vozes Oficiais — AcademIA (v3.0, pós-force-push)

**Data:** 2026-07-29 (v1.0: 2026-07-23, v2.0: 2026-07-24, v3.0: 2026-07-29)
**Método:** leitura direta dos arquivos canônicos + inspeção do diretório `marca/personas/` no clone local do repo `Nexus-HUB57/Academ-IA`
**Status atual do repo:** 171 commits, v1.7.7 (pós-recuperação de force-push)
**Convenção respeitada:** GUIA_MULTI_DEV.md — pasta `agent-sessions/` é nova, sem conflito de path

---

## ⚠️ Aviso: este documento NÃO substitui o registro canônico

Há **6 documentos** que se declaram canônicos para vozes oficiais. Nenhum foi marcado como deprecated. **Não é razoável ter 6 docs canônicos.** Isso é falha de governança documental não resolvida desde v1.6.5.

| Doc | Path declarado | Status declarado | Path correto? |
|-----|----------------|------------------|----------------|
| `marca/personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md` | `personas/{alencar,ive}/audio/...` (sem `marca/`) | "Onda 50 (2026-07-22)" | ❌ **ANTIGO** |
| `marca/personas/OFFICIAL_VOICES.md` | `personas/{alencar,ive}/audio/...` | "status: canonico" | ❌ **ANTIGO** |
| `marca/personas/VOZES-OFICIAIS.md` | `marca/personas/{alencar,ive}/audio/...` | "OFICIAL · VINCULANTE" | ✅ correto |
| `marca/personas/VOICES.md` | `marca/personas/{alencar,ive}/audio/...` | sem status explícito | ✅ correto |
| `GUIA_VOZES_OFICIAIS.md` (raiz) | `personas/{alencar,ive}/audio/...` | "DOCUMENTO SECUNDÁRIO" | ❌ **ANTIGO** |
| `GUIA-VOZES-OFICIAIS.md` (raiz) | `marca/personas/{alencar,ive}/audio/...` | sem status explícito | ✅ correto |
| `marca/INDEX.md` | `personas/{alencar,ive}/...` (em **todos** os links) | "Índice navegável" | ❌ **ANTIGO** (em todos os links) |

**Achado novo da v3.0:** o `marca/INDEX.md` (criado em v1.6.5, declarado "ResolvE ambiguidade entre múltiplos documentos legacy") — **na verdade NÃO resolveu a ambiguidade**, e pior: **propagou o path antigo em todos os links**. É regressão de governance.

---

## 1. Verificação dos arquivos de áudio (re-verificado 2026-07-29)

### 1.1 Sra. Nexus Ive

| Arquivo | Tamanho | MD5 | Status |
|---------|---------|-----|--------|
| `marca/personas/ive/audio/official_voice.wav` | 1.501.484 bytes | `073d4964d3de...` | ✅ **CANÔNICO** (bate com REGISTRY) |
| `marca/personas/ive/audio/Official_voice Dublado Portugues Modelo Oficial Voz Lady Ive Nexus.wav` | 2.823.885 bytes | `f034cdca2746...` | ⚠️ **NÃO documentado** no REGISTRY (versão "Dublado") |

**Diagnóstico Ive:** MD5 e tamanho **inalterados** desde v2.0. Canônico confirmado. Arquivo "Dublado" continua sem doc.

### 1.2 Sir. Nexus Alencar

| Arquivo | Tamanho | MD5 | Status |
|---------|---------|-----|--------|
| `marca/personas/alencar/audio/official_voice.wav` | 1.399.724 bytes | `9f1cbd7aaef8...` | ✅ **CANÔNICO** (bate com REGISTRY) |
| `marca/personas/alencar/audio/official_voice Sir Nexus Alencar Dublado.wav` | 1.399.724 bytes | `9f1cbd7aaef8...` | ⚠️ **NÃO documentado** mas MD5 idêntico ao canônico (alias/cópia) |
| `marca/personas/alencar/audio/Official_Voice Original Modelo Oficial Voz Sir Nexus Alencar.wav` | 2.369.224 bytes | `2924a7d7083e...` | ⚠️ **NÃO documentado** (versão "Original") |
| `marca/personas/alencar/voz_sir_nexus_alencar.wav` | 1.399.724 bytes | `9f1cbd7aaef8...` | ✅ Alias canônico (MD5 idêntico, declarado no REGISTRY) |
| `marca/personas/alencar/sir_nexus_alencar_intro.wav` | 1.008.044 bytes | `fe89c5932fbb...` | ⚠️ **NOVO** — sem documentação. **MD5 verificado pela 1ª vez nesta v3.0** |

**Diagnóstico Alencar:** MD5 e tamanhos **inalterados** para os 4 primeiros. **Novo achado:** `sir_nexus_alencar_intro.wav` agora tem MD5 documentado, mas **continua sem doc oficial**.

### 1.3 Comparação com v2.0 (delta 2026-07-24 → 2026-07-29)

| Item | v2.0 (2026-07-24) | v3.0 (2026-07-29) | Delta |
|------|-------------------|-------------------|-------|
| MD5 canônico Ive | `073d4964d3de...` | `073d4964d3de...` | igual |
| MD5 canônico Alencar | `9f1cbd7aaef8...` | `9f1cbd7aaef8...` | igual |
| Tamanho canônico Ive | 1.501.484 bytes | 1.501.484 bytes | igual |
| Tamanho canônico Alencar | 1.399.724 bytes | 1.399.724 bytes | igual |
| MD5 `sir_nexus_alencar_intro.wav` | **não verificado** | `fe89c5932fbb...` | NOVO |
| Tamanho `sir_nexus_alencar_intro.wav` | **não verificado** | 1.008.044 bytes | NOVO |
| Paths corrigidos em docs | 0 | 0 | **nenhuma correção** |
| Docs marcados como deprecated | 0 | 0 | **nenhuma marcação** |
| Novos docs de voz | 0 | 0 | 0 (mas **2 docs didáticos** novos: `apostilas_v2/md/C5-curso-voice-ai.md`, `slides-especificacoes/aula-27-curso-voice-ai-e-tts-SLIDES.md`) |

**Achado crítico da v3.0:** em 5 dias, **nenhuma das 9 inconsistências da v2.0 foi corrigida**, apesar do force-push + recuperação + criação de `marca/INDEX.md` (v1.6.5) e `agent-sessions/INDEX.md` (2026-07-26).

---

## 2. Mudanças estruturais desde v2.0

### 2.1 Novos arquivos relacionados a voz (não-canônicos)

| Arquivo | Tamanho | Criado em | Contexto |
|---------|---------|-----------|----------|
| `apostilas_v2/md/C5-curso-voice-ai.md` | ? | ? | Versão V2 da apostila 27 (Voice AI) |
| `slides-especificacoes/aula-27-curso-voice-ai-e-tts-SLIDES.md` | ? | ? | Especificação de slides da aula 27 |

**Diagnóstico:** ambos são conteúdo didático (não docs de governança de vozes). Não são canônicos e não devem ser incluídos no REGISTRY.

### 2.2 Novos arquivos no `agent-sessions/` (criado por Mavis Agent)

| Arquivo | Autor | Criado em |
|---------|-------|-----------|
| `agent-sessions/INDEX.md` | Mavis Agent (Mavis@nexus.ai) | 2026-07-26 |
| `agent-sessions/README.md` | Mavis (esta sessão) | 2026-07-25 |

**Diagnóstico:** o Mavis Agent **adicionou um índice navegável** das sessões, **sem sobrescrever meu README**. Convenção multi-dev respeitada. Boa prática.

### 2.3 Arquivos de produção (v1.7.x) que referenciam vozes

Muitos novos arquivos em `apostilas/`, `cursos/`, `materiais/video-aulas/`, `producao/` referenciam vozes oficiais. **Não verificados nesta v3.0** (escopo da auditoria é governança, não conteúdo didático).

---

## 3. Inconsistências (atualizadas para v3.0)

| # | Inconsistência | Severidade v2.0 | Severidade v3.0 | Mudou? |
|---|----------------|-----------------|-----------------|--------|
| 1 | 3/7 docs canônicos referenciam path **antigo** (sem `marca/`) | ALTA | **ALTA** | ❌ **não mudou** |
| 2 | Pipeline `clone_voice` quebrado só documentado em 1/7 docs | ALTA | ALTA | ❌ não mudou |
| 3 | Vozes genéricas proibidas só listadas em 1/7 docs | MÉDIA | MÉDIA | ❌ não mudou |
| 4 | Proporção 60/40 só em 1/7 docs | BAIXA | BAIXA | ❌ não mudou |
| 5 | Tom descrito de formas diferentes | BAIXA | BAIXA | ❌ não mudou |
| 6 | 6+ docs se declaram "canônicos" (1 deveria ser suficiente) | ALTA | **ALTA+** | 🔺 **piorou** (marca/INDEX.md propagou o erro) |
| 7 | 2 arquivos de áudio "Originais" não documentados | MÉDIA | MÉDIA | ❌ não mudou |
| 8 | 1 arquivo `sir_nexus_alencar_intro.wav` sem doc | MÉDIA | MÉDIA | ❌ não mudou (MD5 agora conhecido) |
| 9 | 1 alias Alencar com mesmo MD5 do canônico mas sem doc | BAIXA | BAIXA | ❌ não mudou |
| 10 | `marca/INDEX.md` propaga path antigo em **todos** os links | (não existia) | **MÉDIA** | 🆕 NOVO |

**Resumo da evolução:**
- 9/9 inconsistências da v2.0 **persistiram** (0 corrigidas)
- 1 nova inconsistência foi **introduzida** (marca/INDEX.md com path errado)
- **Total:** 10 inconsistências, 3 ALTA, 5 MÉDIA, 2 BAIXA

---

## 4. Impacto do force-push de 2026-07-29

### 4.1 O que foi sobrescrito

O commit `0a08373` (Mavis@nexus-hub.local) reporta: "force-push sobrescreveu 6 commits locais (4 meus do dia + 2 herdados). Conteúdo recuperado de /tmp + branch backup."

**Análise:** os 4 "meus do dia" são de `Mavis@nexus-hub.local` (outra instância), **não desta sessão (404996140855418)**. Meus 2 commits (`371cc96` e `65f4480`) foram commitados em 2026-07-25, **antes** do force-push de 2026-07-29, e **sobreviveram intactos** (verificado byte a byte com `diff`).

### 4.2 Conteúdo recuperado pela recuperação `0a08373`

| Categoria | Arquivos | Convenção |
|-----------|----------|-----------|
| 7 tutoriais com sufixo `-mavis` | `tutoriais/24-30-*-mavis.md` | ✅ segue GUIA_MULTI_DEV |
| `producao/personas/` restaurado | README + 2 symlinks | 🆕 novo, antes não existia |

**Diagnóstico:** a recuperação foi bem-feita (sufixo `-mavis`, segue GUIA_MULTI_DEV). **MAS** criou um novo path (`producao/personas/`) com symlinks para `marca/personas/` — pode gerar confusão futura ("qual é o canônico?").

---

## 5. Recomendações (atualizadas para v3.0)

### 5.1 Imediato (próximo commit)

- [ ] **Atualizar o REGISTRY** com os paths corretos (`marca/personas/...`) — não corrigido em 5 dias
- [ ] **Atualizar o OFFICIAL_VOICES.md** com os paths corretos
- [ ] **Atualizar o GUIA_VOZES_OFICIAIS.md** (raiz) com os paths corretos OU deletá-lo (já existe GUIA-VOZES-OFICIAIS.md mais novo)
- [ ] **Atualizar o marca/INDEX.md** para usar `marca/personas/` em todos os links
- [ ] **Documentar o `sir_nexus_alencar_intro.wav`** (MD5 `fe89c5932fbb`, 1.0 MB) — agora temos o MD5
- [ ] **Resolver a duplicação de `producao/personas/` vs `marca/personas/`** (criado na recuperação)

### 5.2 Curto prazo (próxima sprint)

- [ ] **Promulgar 1 doc como ÚNICO canônico** (recomendação: `marca/personas/VOZES-OFICIAIS.md`, que tem o path correto) e marcar os outros 5+ como "deprecated" ou deletar
- [ ] Resolver ou documentar workaround para `clone_voice` retornando vazio
- [ ] Adicionar entradas no REGISTRY para os 2 arquivos "Originais" (ou deletar)
- [ ] Adicionar entrada no REGISTRY para `sir_nexus_alencar_intro.wav`
- [ ] Documentar o alias `official_voice Sir Nexus Alencar Dublado.wav` ou deletar

### 5.3 Médio prazo (próximo mês)

- [ ] Implementar CI/CD que valida paths em docs contra paths reais (GitHub Action que falha se path declarado não existe)
- [ ] Migrar GUIA_VOZES_OFICIAIS.md (raiz, path antigo) para `governanca/` e marcar como secundário OU deletar
- [ ] Adicionar seção de "documentos relacionados" no REGISTRY (link cruzado com todos os 6+ docs, com status de cada um)
- [ ] Implementar auditoria automática de MD5 dos arquivos de áudio no CI

---

## 6. Resumo executivo da v3.0

| Item | Status v2.0 | Status v3.0 | Mudou? |
|------|------------|------------|--------|
| Canônicos documentados | 5 docs | 6 docs (+1) | 🔺 |
| Paths com `marca/` | 2/5 | 3/6 | 🔺 |
| Paths com `personas/` antigo | 3/5 | 3/6 | ❌ não mudou |
| `sir_nexus_alencar_intro.wav` MD5 | não verificado | `fe89c5932fbb` (1.0 MB) | 🆕 |
| Docs deprecated | 0 | 0 | ❌ |
| Achados ALTA | 3 | 3 (1 piorou) | ⚠️ |
| Total inconsistências | 9 | 10 | 🔺 |
| Repositório total | 138 commits | 171 commits | +33 |
| CHANGELOG | v1.6.6 | v1.7.7 | +5 minor |

**Veredito v3.0:** a governança de vozes **não melhorou** em 5 dias, **piorou marginalmente** (novo doc com path errado, novo path `producao/personas/`). **Nenhuma das 9 inconsistências da v2.0 foi corrigida.**

---

## 7. Apêndice: comando para reproduzir esta auditoria (v3.0)

```bash
# Clone público do repo
git clone --depth=1 https://github.com/Nexus-HUB57/Academ-IA.git

# Listar todas as vozes em audio/ (com MD5 e tamanho)
for f in Academ-IA/marca/personas/{alencar,ive}/audio/*.wav Academ-IA/marca/personas/alencar/*.wav; do
  if [ -f "$f" ]; then
    size=$(stat -c%s "$f")
    md5=$(md5sum "$f" | cut -c1-12)
    echo "$f - $size bytes - md5:$md5"
  fi
done

# Listar todos os docs de voz no repo
find Academ-IA -type f -name "*.md" \( -iname "*voz*" -o -iname "*voice*" -o -iname "GUIA*VOZES*" -o -iname "GUIA-VOZES*" \) | sort

# Verificar paths declarados vs paths reais
grep -rE "(personas|marca/personas)/[a-z]+/audio" Academ-IA/marca Academ-IA/GUIA*.md

# Verificar estado da recuperação pos force-push
git log --oneline --all 2>&1 | grep -iE "RECUPER|force" | head -5
```

---

**Auditoria v3.0 gerada em 2026-07-29 sobre o repo `Nexus-HUB57/Academ-IA` @ v1.7.7 (pós-recuperação force-push).**
**Método: leitura de docs + inspeção de diretórios via clone público (sem autenticação).**
**Limitações: MD5 e tamanho verificados byte a byte; SHA-256 não verificado (não disponível no REGISTRY para comparação).**
**Convenção multi-dev respeitada (GUIA_MULTI_DEV.md): pasta `agent-sessions/` é nova, sem conflito de path; nenhuma sobrescrita; sufixo `-mavis-detalhado` não aplicável a auditorias.**
**Continuidade: v1.0 (2026-07-23) → v2.0 (2026-07-24) → v3.0 (2026-07-29) — mesma sessão de chat, mesma conta, mesmo agente.**

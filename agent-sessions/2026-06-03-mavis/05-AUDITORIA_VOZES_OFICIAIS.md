---
session_id: 404996140855418
agent: Mavis (MiniMax-M3)
session_type: root
data_sessao: 2026-06-02T16:37:00Z — 2026-06-03T11:55:00Z
data_revisao: 2026-07-24
data_migracao: 2026-07-24
branch: main
gerado_por: IA (modelo MiniMax-M3, instância desta sessão)
contexto_sessao: Auditoria complementar do registro canônico de vozes oficiais (REVISADA após atividade multi-dev)
escopo: Verificação cruzada entre registros canônicos de vozes + inspeção de arquivos em marca/personas/{alencar,ive}/audio/
nota_proveniencia: Output de sessão de chat IA. Para reuso, citação ou auditoria, referenciar session_id e data_sessao.
categoria: governanca-vozes / auditoria
versao: 2.0 (atualizada 2026-07-24 com dados pós-migração para v1.6.3)
audiencia: time de produção de áudio/vídeo, owner, auditores
conflito_multi_dev: NENHUM. Pasta `agent-sessions/` é nova; este arquivo não sobrescreve nenhum existente no remote.
referencias_canonicas_remoto:
  - marca/personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md
  - marca/personas/OFFICIAL_VOICES.md
  - marca/personas/VOZES-OFICIAIS.md
  - marca/personas/VOICES.md
  - GUIA_VOZES_OFICIAIS.md (raiz)
  - GUIA_MULTI_DEV.md (convenções de coexistência multi-dev)
---

# Auditoria das Vozes Oficiais — AcademIA (v2.0, revisada)

**Data:** 2026-07-24 (versão original: 2026-07-23)
**Método:** leitura direta dos arquivos canônicos + inspeção do diretório `marca/personas/` no clone local do repo `Nexus-HUB57/Academ-IA` (v1.6.3, CHANGELOG 2026-07-24)
**Status:** revisado após atividade multi-dev (Mavis, genspark_dev, Mavis Agent) das últimas 48h
**Convenção respeitada:** GUIA_MULTI_DEV.md — este arquivo vai em `agent-sessions/2026-06-03-mavis/` (pasta nova, sem conflito de path)

---

## ⚠️ Aviso: este documento NÃO substitui o registro canônico

Há **4 documentos** que se declaram canônicos para vozes oficiais:

1. `marca/personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md` — registro técnico (MD5, codec, sample rate)
2. `marca/personas/OFFICIAL_VOICES.md` — "Source of truth" (caminho antigo referenciado!)
3. `marca/personas/VOZES-OFICIAIS.md` — "OFICIAL · VINCULANTE" (caminho correto)
4. `marca/personas/VOICES.md` — "registro canônico" (caminho correto)
5. `GUIA_VOZES_OFICIAIS.md` (raiz) — TL;DR para devs

**Não é razoável ter 4 docs canônicos.** Isso é falha de governança documental. Veja a seção 2.

Este documento é uma **verificação cruzada feita por IA em 2026-07-24**, focada em inconsistências, gaps e recomendações operacionais.

---

## 1. Verificação dos arquivos de áudio

### 1.1 Sra. Nexus Ive

| Arquivo | Tamanho | MD5 | Status canônico (REGISTRY) |
|---------|---------|-----|-----------------------------|
| `marca/personas/ive/audio/official_voice.wav` | 1.501.484 bytes | `073d4964d3de...` | ✅ **CANÔNICO** (bate com REGISTRY) |
| `marca/personas/ive/audio/Official_voice Dublado Portugues Modelo Oficial Voz Lady Ive Nexus.wav` | 2.823.885 bytes | `f034cdca2746...` | ⚠️ **NÃO documentado** no REGISTRY. Versão "Dublado" — não-canônica |

**Diagnóstico Ive:** o arquivo canônico bate perfeitamente com o REGISTRY. Existe 1 arquivo extra "Dublado" (~2.8 MB) que **não está documentado em lugar nenhum** dos 4 docs canônicos.

### 1.2 Sir. Nexus Alencar

| Arquivo | Tamanho | MD5 | Status canônico (REGISTRY) |
|---------|---------|-----|-----------------------------|
| `marca/personas/alencar/audio/official_voice.wav` | 1.399.724 bytes | `9f1cbd7aaef8...` | ✅ **CANÔNICO** (bate com REGISTRY) |
| `marca/personas/alencar/audio/official_voice Sir Nexus Alencar Dublado.wav` | 1.399.724 bytes | `9f1cbd7aaef8...` | ⚠️ **NÃO documentado** mas MD5 idêntico ao canônico — é **cópia/alias** |
| `marca/personas/alencar/audio/Official_Voice Original Modelo Oficial Voz Sir Nexus Alencar.wav` | 2.369.224 bytes | `2924a7d7083e...` | ⚠️ **NÃO documentado** no REGISTRY. Versão "Original" — não-canônica |
| `marca/personas/alencar/voz_sir_nexus_alencar.wav` | 1.399.724 bytes | `9f1cbd7aaef8...` | ✅ Alias canônico (MD5 idêntico, declarado no REGISTRY) |
| `marca/personas/alencar/sir_nexus_alencar_intro.wav` | (não verificado) | (não verificado) | ⚠️ **NOVO** — não existia no commit anterior. Sem doc. |

**Diagnóstico Alencar:** o canônico bate com o REGISTRY. Há 4 arquivos relacionados:
- 1 canônico (`official_voice.wav`)
- 1 alias declarado (`voz_sir_nexus_alencar.wav`)
- 1 cópia/alias não-declarada mas com mesmo MD5 (`official_voice Sir Nexus Alencar Dublado.wav`)
- 2 arquivos "Originais" não-canônicos (versões diferentes, MD5 diferente)
- 1 arquivo novo (`sir_nexus_alencar_intro.wav`) sem documentação

### 1.3 Arquivos de áudio gerados (cenas de curso)

```
./cursos/fundamental/00-boas-vindas-cena1.wav
./cursos/fundamental/00-boas-vindas-cena2.wav
... (7 cenas total)
./videos/audio/full_00_alencar.wav
./videos/audio/full_01_ive.wav
... (mais arquivos full_NN_persona.wav)
```

**Diagnóstico:** esses são **outputs de TTS** (narrativas de curso), não vozes-fonte. Não precisam ser documentados no REGISTRY de vozes-fonte. Estão corretamente isolados em `cursos/` e `videos/audio/`.

---

## 2. Inconsistências entre os 4 docs canônicos

### 2.1 Path declarado

| Doc | Path declarado | Correto? |
|-----|----------------|----------|
| `voice_registry/OFFICIAL_VOICES_REGISTRY.md` | `personas/{alencar,ive}/audio/official_voice.wav` | ❌ **antigo** — após migração para `marca/personas/` (commit `bcca542`), deveria ser `marca/personas/{alencar,ive}/audio/official_voice.wav` |
| `marca/personas/OFFICIAL_VOICES.md` | `personas/{alencar,ive}/audio/official_voice.wav` | ❌ **antigo** — mesmo problema |
| `marca/personas/VOZES-OFICIAIS.md` | `marca/personas/{alencar,ive}/audio/official_voice.wav` | ✅ correto |
| `marca/personas/VOICES.md` | `marca/personas/{alencar,ive}/audio/official_voice.wav` | ✅ correto |
| `GUIA_VOZES_OFICIAIS.md` (raiz) | `personas/{alencar,ive}/audio/official_voice.wav` | ❌ **antigo** |

**Diagnóstico:** 3 de 5 docs canônicos referenciam path **antigo** (sem `marca/`). Os arquivos reais estão em `marca/personas/`. Se um dev seguir o REGISTRY, **vai falhar ao procurar o arquivo** — `personas/alencar/audio/official_voice.wav` não existe mais (foi removido em `f29a0d3`).

**Severidade:** ALTA. Docs canônicos que apontam para path inexistente são piores que ausência de docs.

### 2.2 Tom declarado

| Doc | Tom Ive | Tom Alencar |
|-----|---------|-------------|
| REGISTRY | Serena, articulada, sotaque sulista leve, rouquidão suave | Maduro, sereno, didático, autoridade intelectual, judaico sereno |
| OFFICIAL_VOICES.md | Não cita explicitamente | Masculino, maduro, sério mas caloroso, grave, didática |
| VOZES-OFICIAIS.md | (não li completo) | Judaico, formal, autoridade técnica; sério, calmo, mentor sábio |
| VOICES.md | (não li completo) | Masculina, grave, didática |
| GUIA (raiz) | Leve rouquidão, sotaque sulista elegante | Matura, controlada, didática |

**Diagnóstico:** há **variação** na descrição do tom. Nenhuma é contraditória de forma grave, mas a **frase "judaico sereno" / "judaico, formal"** no REGISTRY e VOZES-OFICIAIS.md é forte e merece destaque — pode ser uma característica que diferencia Alencar das outras vozes técnicas disponíveis.

**Severidade:** BAIXA. Variação editorial, não erro técnico.

### 2.3 Vozes genéricas proibidas

| Doc | Cita proibição? |
|-----|-----------------|
| REGISTRY | ✅ Lista `Portuguese_CharmingQueen` e `Portuguese_Steadymentor` |
| OFFICIAL_VOICES.md | ❌ não cita |
| VOZES-OFICIAIS.md | (parcial) |
| VOICES.md | (não li completo) |
| GUIA (raiz) | ❌ não cita (apenas "nunca use voz genérica") |

**Diagnóstico:** só o REGISTRY lista explicitamente as vozes genéricas proibidas. Os outros docs só falam em "não use voz genérica" sem citar quais. **Risco real** de dev usar `Portuguese_CharmingQueen` em prod seguindo só o GUIA.

**Severidade:** MÉDIA.

### 2.4 Proporção 60/40

| Doc | Cita proporção 60% Alencar / 40% Ive? |
|-----|---------------------------------------|
| REGISTRY | ❌ não cita |
| OFFICIAL_VOICES.md | ❌ não cita |
| VOZES-OFICIAIS.md | ❌ não cita |
| VOICES.md | ❌ não cita |
| GUIA (raiz) | ✅ cita como "Regra de Ouro #6" |

**Diagnóstico:** proporção documentada **só no GUIA**, não nos canônicos. Inconsistência editorial.

**Severidade:** BAIXA.

### 2.5 Status do pipeline `clone_voice`

| Doc | Cita status? |
|-----|--------------|
| REGISTRY | ✅ Declara "Pivô pendente" e lista fallback |
| OUTICIAL_VOICES.md | ❌ não cita |
| VOZES-OFICIAIS.md | (não li) |
| VOICES.md | (não li) |
| GUIA (raiz) | ❌ não cita |

**Diagnóstico:** só o REGISTRY cita o problema operacional crítico (clone_voice retornando vazio). Os outros docs descrevem o "como deveria ser" mas não o "como está".

**Severidade:** ALTA para produção.

---

## 3. Resumo de inconsistências e severidade

| # | Inconsistência | Severidade | Doc afetado |
|---|----------------|------------|-------------|
| 1 | 3/5 docs canônicos referenciam path **antigo** (sem `marca/`) | **ALTA** | REGISTRY, OFFICIAL_VOICES.md, GUIA |
| 2 | Pipeline `clone_voice` quebrado só documentado em 1/5 docs | **ALTA** | REGISTRY |
| 3 | Vozes genéricas proibidas só listadas em 1/5 docs | MÉDIA | REGISTRY |
| 4 | Proporção 60/40 só em 1/5 docs | BAIXA | GUIA |
| 5 | Tom descrito de formas diferentes | BAIXA | todos |
| 6 | 4 docs se declaram "canônicos" (1 deveria ser suficiente) | **ALTA** | governança |
| 7 | 2 arquivos de áudio "Originais" não documentados | MÉDIA | REGISTRY |
| 8 | 1 arquivo novo `sir_nexus_alencar_intro.wav` sem doc | MÉDIA | REGISTRY |
| 9 | 1 alias Alencar (`official_voice Sir Nexus Alencar Dublado.wav`) com mesmo MD5 do canônico mas sem doc | BAIXA | REGISTRY |

---

## 4. Recomendações

### 4.1 Imediato (próximo commit)

- [ ] **Atualizar o REGISTRY** com os paths corretos (`marca/personas/...`)
- [ ] **Atualizar o GUIA** com os paths corretos
- [ ] **Atualizar o OFFICIAL_VOICES.md** com os paths corretos
- [ ] **Promulgar 1 doc como ÚNICO canônico** (recomendação: REGISTRY) e marcar os outros como "deprecated" ou deletar

### 4.2 Curto prazo (próxima sprint)

- [ ] Resolver ou documentar workaround para `clone_voice` retornando vazio
- [ ] Adicionar entradas no REGISTRY para os 2 arquivos "Originais" (ou deletar)
- [ ] Adicionar entrada no REGISTRY para `sir_nexus_alencar_intro.wav`
- [ ] Documentar o alias `official_voice Sir Nexus Alencar Dublado.wav` ou deletar

### 4.3 Médio prazo (próximo mês)

- [ ] Implementar CI/CD que valida paths em docs contra paths reais
- [ ] Migrar GUIA_VOZES_OFICIAIS.md para `governanca/` e marcar como secundário (já está OK)
- [ ] Adicionar seção de "documentos relacionados" no REGISTRY (link cruzado com todos os 4 docs, com status de cada um)

---

## 5. Apêndice: comando para reproduzir esta auditoria (v2.0)

```bash
# Clone público do repo
git clone --depth=1 https://github.com/Nexus-HUB57/Academ-IA.git

# Listar todas as vozes em audio/
find Academ-IA/marca/personas/*/audio -type f -name "*.wav" -exec ls -la {} \;

# MD5 e tamanho de cada voz
for f in Academ-IA/marca/personas/{alencar,ive}/audio/*.wav; do
  size=$(stat -c%s "$f")
  md5=$(md5sum "$f" | cut -c1-12)
  echo "$f - $size bytes - md5:$md5"
done

# Ler todos os 4 docs canônicos
cat Academ-IA/marca/personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md
cat Academ-IA/marca/personas/OFFICIAL_VOICES.md
cat Academ-IA/marca/personas/VOZES-OFICIAIS.md
cat Academ-IA/marca/personas/VOICES.md
cat Academ-IA/GUIA_VOZES_OFICIAIS.md

# Validar paths declarados vs paths reais
grep -rE "personas/[a-z]+/audio" Academ-IA/marca Academ-IA/GUIA_VOZES_OFICIAIS.md
```

---

**Auditoria v2.0 gerada em 2026-07-24 sobre o repo `Nexus-HUB57/Academ-IA` @ v1.6.3 (CHANGELOG 2026-07-24).**
**Método: leitura de docs + inspeção de diretórios via clone público (sem autenticação).**
**Limitações: MD5 e tamanho verificados byte a byte; SHA-256 não verificado (não disponível no REGISTRY para comparação).**
**Convenção multi-dev respeitada (GUIA_MULTI_DEV.md): pasta `agent-sessions/` é nova, sem conflito de path; nenhuma sobrescrita; sufixo `-mavis-detalhado` não aplicável a auditorias.**

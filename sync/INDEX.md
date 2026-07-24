---
title: "Sync · Índice de Sincronização"
description: "Documento-índice dos artefatos de sincronização entre Academ'IA e runtime dos agentes"
tags: [sync, indice, mcp, agent-bridge, skill-manifest, runtime]
version: 1.0.0
last_updated: 2026-07-24
pattern: "MMN_IA"
---

# 🔄 Sync · Índice de Sincronização

> **Documento-índice** dos artefatos de sincronização entre a **Academ'IA** (repositório de conhecimento) e o **runtime dos agentes** (orquestrador operacional). Estes artefatos garantem que a Academ'IA é o source of truth e o runtime carrega as versões corretas.

## 🎯 Propósito

O diretório `sync/` contém:

- **Manifests JSON** carregados pelo runtime no bootstrap.
- **Schemas MD** que definem contratos de dados.
- **Configurações MCP** que permitem agentes lerem a Academ'IA.

Sem sincronização, a Academ'IA seria apenas documentação desconectada da operação. Com ela, é o **cérebro vivo** do sistema.

## 📋 Inventário

| Arquivo | Tipo | Função | Versão | Última atualização |
|---------|------|--------|--------|---------------------|
| [`agent-bridge.json`](agent-bridge.json) | Manifesto | Mapeia níveis de conhecimento → bundle de skills → permissões SHO. Carregado pelo CentralOrchestrator. | 1.1.1 | 2026-06-03 |
| [`skill-manifest.json`](skill-manifest.json) | Manifesto | Catálogo canônico de skills do marketplace Nexus (45 skills: 25 operacionais, 20 planejadas). | 1.1.1 | 2026-06-03 |
| [`audit-log-schema.md`](audit-log-schema.md) | Schema | Schema canônico de audit log para operações inter-agentes. | 1.0 | 2026-06-24 |
| [`MCP-CONFIG.md`](MCP-CONFIG.md) | Config | Configuração do Model Context Protocol para que agentes leiam a Academ'IA em runtime. | 1.0.0 | 2026-06-02 |

## 🏛️ Arquitetura de Sincronização

### Fluxo

```
┌──────────────────┐
│  Academ'IA       │
│  (repositório)   │  ← source of truth
└──────────────────┘
        ↓
        │ manifests (agent-bridge, skill-manifest)
        ↓
┌──────────────────┐
│  Runtime Agents  │  ← carrega manifests no bootstrap
└──────────────────┘
        ↓
        │ logs, eventos, métricas
        ↓
┌──────────────────┐
│  Audit Log       │  ← schema canônico
└──────────────────┘
```

### Princípios

1. **Single Source of Truth** — toda versão de skill, permission, ou metadata está na Academ'IA.
2. **Schema Versioning** — toda mudança de schema é versionada e compatível retroativa.
3. **Idempotência** — manifests podem ser recarregados sem efeito colateral.
4. **MCP para Live Reading** — agentes leem Academ'IA em tempo real via MCP.
5. **Audit Imutável** — log de auditoria é append-only e retido por 7 anos.

## 🔌 Como os Componentes se Conectam

### agent-bridge.json

**Carregado por:** `CentralOrchestrator.bootstrap()`

**Função:** Mapeia cada nível de certificação (CON, CEN, CEN+, MAS+, CNX) para:
- Bundle de skills permitidas
- Limites de permissões SHO
- Quota de execução por mês
- Permissões cross-tenant

**Exemplo de leitura:**

```typescript
import agentBridge from '../sync/agent-bridge.json';

const userCertLevel = 'CEN+';
const skills = agentBridge.certification_map[userCertLevel].allowed_skills;
const shoPermissions = agentBridge.certification_map[userCertLevel].sho_permissions;
```

### skill-manifest.json

**Carregado por:** `SkillRegistry.initialize()`

**Função:** Catálogo canônico de todas as skills, com:
- Nome, versão, autor
- Categoria
- Pré-requisitos
- Status (operational, planned, deprecated)
- Schema de input/output

**Exemplo de leitura:**

```typescript
import skillManifest from '../sync/skill-manifest.json';

const skill = skillManifest.skills.find(s => s.name === 'whatsapp-copy-v3');
if (skill.status === 'operational') {
  // inicializar skill
}
```

### audit-log-schema.md

**Validado por:** `AuditLogger.write()`

**Função:** Define o schema de cada entrada de log:
- `event_id`, `timestamp`, `actor_id`, `action`
- `resource_type`, `resource_id`
- `payload`, `result`, `severity`
- `tenant_id`, `trace_id`, `correlation_id`

**Exemplo de entrada conforme schema:**

```json
{
  "event_id": "evt-2026-07-24-001",
  "timestamp": "2026-07-24T13:30:00Z",
  "actor_id": "agent-marketing-001",
  "action": "skill.execute",
  "resource_type": "skill",
  "resource_id": "whatsapp-copy-v3",
  "payload": { "input_hash": "sha256:abc...", "output_hash": "sha256:def..." },
  "result": "success",
  "severity": "INFO",
  "tenant_id": "tenant-123",
  "trace_id": "trace-xyz-789"
}
```

### MCP-CONFIG.md

**Configurado por:** `mcp_config.json` do agente

**Função:** Permite que agentes leiam a Academ'IA como se fosse um sistema de arquivos remoto, com:
- Listagem de arquivos por path
- Leitura de conteúdo
- Metadados (frontmatter YAML)
- Validação de schema

**Exemplo de uso pelo agente:**

```
Agente: "Quero ler o playbook PB-WHATSAPP"
MCP: Lê /workspace/Academ-IA/playbooks/PB-WHATSAPP-operacao-diaria.md
Retorna: conteúdo + metadados
```

## 🔄 Workflow de Atualização

### Para mudar um manifesto JSON

1. **Editar** o JSON localmente.
2. **Validar** schema (json schema validator).
3. **Bump version** (MAJOR/MINOR/PATCH).
4. **Atualizar** `last_updated`.
5. **PR** com descrição da mudança.
6. **Coordenação** com time runtime para rollout.
7. **Tag de release** no repositório.
8. **Comunicar** stakeholders (squads, DPO, SRE).

### Para mudar um schema MD

1. **Editar** mantendo compatibilidade retroativa quando possível.
2. **Versionar** (bump version no frontmatter).
3. **Documentar** breaking changes em CHANGELOG.
4. **PR** com exemplos antes/depois.
5. **Validar** com runtime antes de merge.

## 🛡️ Compatibilidade

### Backward Compatibility

- **MINOR bumps** (1.0 → 1.1): adicionar campos opcionais. Runtime antigo continua funcionando.
- **PATCH bumps** (1.0.0 → 1.0.1): correções de typo, valores padrão. Sem breaking change.
- **MAJOR bumps** (1.x → 2.0): breaking change. Requer migração coordenada.

### Runtime Support

| Versão Manifest | Runtime Mínimo | Status |
|-----------------|----------------|--------|
| 1.1.x | 2.3.0+ | Active |
| 1.0.x | 2.0.0+ | Deprecated |
| 0.9.x | 1.x | Sunset |

## 🧪 Validação

### Validação Local

```bash
# Validar JSON
python3 -c "import json; json.load(open('sync/agent-bridge.json'))"
python3 -c "import json; json.load(open('sync/skill-manifest.json'))"

# Validar schema (se tiver jsonschema)
pip install jsonschema
python3 -c "import json, jsonschema; spec = json.load(open('sync/audit-log.schema.json')); jsonschema.validate(instance={...}, schema=spec)"
```

### Validação no CI

Pipeline CI executa:
1. JSON parse
2. Schema validation
3. Cross-reference com código (símbolos importados existem)
4. Smoke test de bootstrap

## 📂 Estrutura

```
sync/
├── INDEX.md                  ← este arquivo
├── agent-bridge.json         ← manifesto de ponte
├── skill-manifest.json       ← manifesto de skills
├── audit-log-schema.md       ← schema de audit log
└── MCP-CONFIG.md             ← config MCP
```

## 🔗 Links Cruzados

- [`../README.md`](../README.md) — README raiz
- [`../CHANGELOG.md`](../CHANGELOG.md) — Histórico de versões
- [`../GUIA_MULTI_DEV.md`](../GUIA_MULTI_DEV.md) — Convenções multi-dev
- [`../Lib-Nexus/knowledge-base/01-modelo-ioaid.md`](../Lib-Nexus/knowledge-base/01-modelo-ioaid.md) — Modelo IOAID
- [`../Lib-Nexus/agents-specs/`](../Lib-Nexus/agents-specs/) — Specs de agentes
- [`../Lab-Nexus/prompts/`](../Lab-Nexus/prompts/) — Prompts canônicos

## 👥 Ownership

- **Owner:** Head de Arquitetura + Runtime Lead
- **Cadência de revisão:** Trimestral ou a cada release major do runtime

---

*Nexus Affil'IA'te · sync/INDEX.md · v1.0.0 · Julho 2026*

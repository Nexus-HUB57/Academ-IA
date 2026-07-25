---
title: "HUBs · Visão Geral"
description: "Documento-índice dos HUBs HTML estáticos da Academ'IA — ponte entre GitHub e landing pública"
tags: [hubs, html, estatico, landing, indice, academia]
version: 1.0.0
last_updated: 2026-07-24
pattern: "MMN_IA"
---

# 🌐 HUBs · Academ'IA — Índice Navegável

> **Documento-índice** dos HUBs HTML estáticos da Academ'IA. Cada HUB é uma página HTML auto-contida que serve como ponto de entrada para uma área de conteúdo. Esta página documenta a arquitetura, lista cada HUB, e orienta quem quer criar novos.

## 🎯 O que são os HUBs

Os HUBs são páginas HTML estáticas servidas publicamente. Eles são:

- **Auto-contidos** — HTML + CSS inline, sem build step obrigatório.
- **Estáticos** — gerados a partir de scripts Python/Bash, mas servidos como arquivos.
- **Navegáveis** — links cruzados entre HUBs, formando uma constelação.
- **Versionados** — todo HUB tem referência ao seu gerador (script Python).
- **Visuais** — design dark com paleta Nexus (cyan, purple, gold).

## 📋 Catálogo de HUBs

### HUBs Canônicos (produção)

| Arquivo | Função | Gerador |
|---------|--------|---------|
| [`index.html`](index.html) | Hub geral — ponto de entrada principal | — |
| [`cursos.html`](cursos.html) | Catálogo de cursos (fundamental, agente, master, elite) | `scripts/generate_pending_course_materials.py` |
| [`trilhas.html`](trilhas.html) | Trilhas de aprendizado (Master, Elite) | `scripts/generate_pending_course_materials.py` |
| [`apostilas.html`](apostilas.html) | Índice de apostilas (37 arquivos .md) | `scripts/build_htmls.sh` |
| [`lib.html`](lib.html) | Lib-Nexus (knowledge base, best practices, agents, API) | `scripts/build_htmls.sh` |
| [`lab.html`](lab.html) | Lab-Nexus (prompts, templates, tools) | `scripts/build_htmls.sh` |
| [`playbooks.html`](playbooks.html) | Índice de playbooks (14 documentos) | `scripts/build_htmls.sh` |
| [`webinars.html`](webinars.html) | Índice de webinars (WB-2026-01..18) | `scripts/build_htmls.sh` |
| [`tutoriais.html`](tutoriais.html) | Tutoriais práticos | `scripts/build_htmls.sh` |

### HUBs Especiais

| Arquivo | Função | Gerador |
|---------|--------|---------|
| [`landing.html`](landing.html) | Landing page de marketing da Academia | manual |
| [`player.html`](player.html) | Player de vídeo das aulas (aulas-onda-49) | manual |

## 🏛️ Arquitetura Técnica

### Stack Visual

```yaml
html: HTML5 semântico
css: inline (no <style>) com CSS variables
fontes: Inter (Google Fonts)
tema: dark (--bg, --bg2, --card)
acentos:
  cyan: "#63eaff" (links, badges)
  purple: "#b78cff" (secundário)
  gold: "#facc15" (CTA, destaque)
responsivo: sim (max-width 1200px container, mobile-first)
acessibilidade: contraste AA mínimo
```

### Estrutura Comum

Todo HUB segue este esqueleto:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>...</title>
  <meta name="description" content="...">
  <link href="https://fonts.googleapis.com/..." rel="stylesheet">
  <style>...</style>
</head>
<body>
  <div class="container">
    <header>
      <h1>...</h1>
      <p class="subtitle">...</p>
    </header>
    <nav>...</nav>
    <main>...</main>
    <footer>...</footer>
  </div>
</body>
</html>
```

### Padrão de Cartão

Cada item em um HUB é renderizado como cartão:

```html
<article class="card">
  <h3>Título do Material</h3>
  <p>Descrição curta.</p>
  <ul>
    <li><a href="...">Link 1</a></li>
    <li><a href="...">Link 2</a></li>
  </ul>
  <div class="meta">
    <span class="badge">categoria</span>
    <span class="duration">duração</span>
  </div>
</article>
```

## 🔄 Workflow de Atualização

### Para editar um HUB existente

1. **Verifique** se é gerado por script (vide tabela acima).
2. Se sim: **edite o script gerador** e re-execute. **Não edite o HTML direto** (será sobrescrito).
3. Se não: edite o HTML diretamente, com cuidado para não quebrar o template.

```bash
# Exemplo: regenerar apostilas.html
cd /workspace/Academ-IA
python3 scripts/build_htmls.sh
git diff hubs/apostilas.html  # revisar diff
git add hubs/apostilas.html
git commit -m "docs(academia): regenera hubs após novos materiais"
```

### Para criar um HUB novo

1. **Identifique** a área de conteúdo a ser navegada.
2. **Escolha o template** (copie de um HUB similar).
3. **Customize** cores (manter paleta Nexus) e conteúdo.
4. **Documente** neste README (acrescentar linha na tabela).
5. **Atualize** [`index.html`](index.html) para linkar.
6. **Adicione entrada** no CHANGELOG.

## 🛡️ Convenções

- **Não duplicar** HUBs existentes (use sufixo `-v2` se necessário).
- **Manter paleta** Nexus (cyan/purple/gold) para consistência visual.
- **Validar HTML** antes de commit (W3C validator).
- **Otimizar imagens** se houver (preferir SVG inline).
- **Lazy-load** imagens externas quando aplicável.

## 📂 Localização no Repositório

```
Academ-IA/
├── hubs/                  ← ESTE DIRETÓRIO
│   ├── README.md          ← este arquivo
│   ├── index.html
│   ├── cursos.html
│   ├── trilhas.html
│   ├── ...
│   └── player.html
└── scripts/
    ├── build_htmls.sh
    ├── generate_pending_course_materials.py
    └── ...
```

## 🔗 Links Cruzados

- [`../README.md`](../README.md) — README raiz da Academia
- [`../CHANGELOG.md`](../CHANGELOG.md) — Histórico de versões
- [`../GUIA_MULTI_DEV.md`](../GUIA_MULTI_DEV.md) — Convenções multi-dev
- [`../docs/ACADEMIA_MANIFEST_OPERACIONAL_2026-07-24.md`](../docs/ACADEMIA_MANIFEST_OPERACIONAL_2026-07-24.md) — Manifesto operacional

## 👥 Ownership

- **Owner:** Head de Design + Head de Engenharia
- **Mantenedor:** Devs de produção
- **Cadência:** revisão trimestral

---

*Nexus Affil'IA'te · hubs/README.md · v1.0.0 · Julho 2026*

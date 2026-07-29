# 📦 Ondas 47 & 48 — Audio-Aulas "Curso Universo IA"

> **Migrado do repo legado** `Nexus-HUB57/MMN_AI-to-AI` em **jul/2026** durante a Onda 49.
> Estes assets foram originalmente publicados em:
> - `frontend/public/academia/audios/aula-*.mp3` (16 MP3)
> - `frontend/public/academia/thumbs/thumb-aula-*.webp` (16 WEBP)
> - `docs/entregas/onda-47/roteiros/aula-01-10.md` (10 roteiros)
> - `docs/entregas/onda-48/roteiros/aula-11-16.md` (6 roteiros)

---

## 🎯 Conteúdo

16 audio-aulas do **Curso Universo IA** (aulas 01-16), trilha introdutória da plataforma Nexus Affil'IA'te MMN_IA.

| # | Aula | Persona (Voz) | Duração estimada |
|---|------|---------------|------------------|
| 01 | O que é um Agente IA? | (a confirmar) | 6-8 min |
| 02 | O que as IAs já desenvolvem | (a confirmar) | — |
| 03 | O que são Skills | (a confirmar) | — |
| 04 | Tipos de Agentes | (a confirmar) | — |
| 05 | Bibliotecas de IA | (a confirmar) | — |
| 06 | OpenClaw | (a confirmar) | — |
| 07 | LangChain, Docling e Crawl4AI | (a confirmar) | — |
| 08 | Como construir um Agente | (a confirmar) | — |
| 09 | Automação Social | (a confirmar) | — |
| 10 | Marketplaces | (a confirmar) | — |
| 11 | IOAID (Ive) | **Lady Nexus Ive** | — |
| 12 | SHO (Alencar) | **Sir Nexus Alencar** | — |
| 13 | Painel do Afiliado (Ive) | **Lady Nexus Ive** | — |
| 14 | Arquitetura Técnica (Alencar) | **Sir Nexus Alencar** | — |
| 15 | Método Nexus em Escala (Ive) | **Lady Nexus Ive** | — |
| 16 | Primeiro Agente Escalável (Alencar) | **Sir Nexus Alencar** | — |

## 🎙️ Vozes Oficiais

A partir das aulas 11+, as vozes oficiais foram aplicadas:

- **Sir Nexus Alencar** → `personas/alencar/audio/official_voice.wav`
- **Lady Nexus Ive** → `personas/ive/audio/official_voice.wav`

Aulas 01-10 usaram TTS genérico e devem ser regeradas com as vozes oficiais no pipeline de regeneração (status: pendente, ver `videos/aulas-onda-47/regenerar-aulas-01-10.md` — TODO).

## 📂 Estrutura

```
videos/aulas-onda-47/
├── README.md                 ← este arquivo
├── manifest/
│   ├── MANIFEST-ONDA-47.json ← capa/thumb/audio metadata
│   └── MANIFEST-ONDA-48.json ← continuação (aulas 11-16)
├── roteiros/
│   ├── aula-01-o-que-e-agente-ia.md
│   ├── ... (16 arquivos)
│   └── aula-16-primeiro-agente-escalavel-alencar.md
├── audios/
│   ├── aula-01-o-que-e-agente-ia.mp3
│   ├── ... (16 arquivos)
│   └── aula-16-primeiro-agente-escalavel-alencar.mp3
└── thumbs/
    ├── thumb-aula-01-o-que-e-agente-ia.webp
    ├── ... (16 arquivos)
    └── thumb-aula-16-primeiro-agente-escalavel-alencar.webp
```

## ✅ Status da Migração

- [x] 16/16 roteiros MD
- [x] 16/16 áudios MP3
- [x] 16/16 thumbnails WEBP
- [x] 2/2 manifests JSON
- [x] README de migração
- [ ] Regenerar aulas 01-10 com vozes oficiais (Ive/Alencar)
- [ ] Renderizar vídeos MP4 (RENDER_PIPELINE.md)
- [ ] Atualizar INDEX.md do Academ-IA com esta seção

## 🔗 Links Relacionados

- Vozes oficiais: [`personas/alencar/audio/`](../../personas/alencar/audio/) · [`personas/ive/audio/`](../../personas/ive/audio/)
- Pipeline de renderização: [`videos/RENDER_PIPELINE.md`](../../videos/RENDER_PIPELINE.md)
- INDEX master: [`../../INDEX.md`](../../INDEX.md)

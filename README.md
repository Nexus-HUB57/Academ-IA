# 🎓 AcademIA Nexus — Plataforma Educacional da Ecossistema MMN AI-to-AI

> **Repositório canônico de desenvolvimento da plataforma AcademIA.**
> Este repo é o sucessor canônico de `Nexus-HUB57/MMN_AI-to-AI` (subdiretório `AcademIA/`).
> A partir da **Onda 40 (v1.4.0)**, todo o desenvolvimento audiovisual, pedagógico e editorial
> da AcademIA passa a viver aqui.

---

## 🌊 Estado Atual

- **Versão:** 1.4.0 — "Onda 40"
- **Data:** 2026-07-21
- **Conteúdo publicado:** 3/16 módulos em vídeo · 31 apostilas · 17 roteiros · 15 tutoriais · 11 playbooks · 13 webinars · 7 oficinas · 5 certificações
- **Total no repo:** ~566 MB (docs + thumbnails + vídeos MP4 + áudios de voice-clone + assets de personas)

## 📂 Estrutura

```
AcademIA/
├── INDEX.md                    ← mapa completo (fonte da verdade)
├── README.md                   ← este arquivo
├── CHANGELOG.md                ← histórico de mudanças
├── RESUMO_EXECUTIVO.md
├── ANALISE_TECNICA_E_ROADMAP.md
├── FAQ.md
│
├── cursos/                     ← 4 trilhas (Fundamental, Agente, Master, Elite)
├── videos/                     ← roteiros + thumbnails + MP4 renderizados
├── apostilas/                  ← material didático extenso (1-31)
├── tutoriais/                  ← tutoriais rápidos (1-15)
├── playbooks/                  ← manuais operacionais (PB-*)
├── webinars/                   ← sessões gravadas (WB-*)
├── hubs/                       ← landing pages HTML
├── certificacoes/              ← modelos + 5 certificações
├── treinamentos/               ← oficinas (WS-*)
├── personas/                   ← Ive, Alencar, Helena, Ravi, Otto
│   ├── ive/                    ├── alencar/         ├── dupla/
│   ├── audio/                  ├── voice clone      ├── celebration
│   └── assets/
├── marca/                      ← brand kit
├── html/                       ← renderizações HTML
├── pdf/  +  pdfs/              ← PDFs publicados (apostilas + webinars + cursos)
├── producao/                   ← pipeline de produção
├── Lab-Nexus/                  ← laboratório de prompts
├── Lib-Nexus/                  ← biblioteca de referência
├── governanca/                 ← docs de governança editorial
└── sync/                       ← scripts de sincronização
```

## 🚀 Onda 40 (v1.4.0) — em produção

A Onda 40 integra a nova **Coletânea NEXUS AFFIL'IA'TE TECH** (5 ebooks técnicos PhD-level)
como 5 roteiros-âncora da Academia, espelhando:

| Roteiro-âncora | Ebook correspondente | Trilha |
|---|---|---|
| 15 — Orquestração de Ecossistemas IA | NEXUS AFFIL'IA'TE TECH Vol. I | Elite |
| 16 — Senciência e suas Barreiras | NEXUS AFFIL'IA'TE TECH Vol. II | Master (convidado) |
| 17 — O Poder x Perigo da Autonomia AI | NEXUS AFFIL'IA'TE TECH Vol. III | Elite |
| 18 — Fundamento SaaS IA | NEXUS AFFIL'IA'TE TECH Vol. IV | Elite |
| 19 — Poder de Processamento IA | NEXUS AFFIL'IA'TE TECH Vol. V | Elite |

## 🎬 Pipeline de Produção

```bash
# 1. Gerar narrações voice-cloned (Minimax Voice Clone)
python3 scripts/youtube/build_narrations.py

# 2. Compor vídeos (slides + narração)
python3 scripts/youtube/compose_videos.py

# 3. Deploy para VPS
scp video-*.mp4 root@143.95.213.237:/var/www/oneverso/current/public/academia/videos/

# 4. Sincronizar DB
sudo -u postgres psql nexus_prod -c "UPDATE academia_lessons SET ...;"

# 5. Upload YouTube como PRIVATE
python3 scripts/youtube/upload_academia_youtube.py --limit 5
```

## 🔗 Links

- **Acadêmica pública:** https://oneverso.com.br/academia
- **Admin:** https://oneverso.com.br/admin/academia
- **YouTube:** @NexusAffilIAte-w9p
- **Repo origem (legado):** https://github.com/Nexus-HUB57/MMN_AI-to-AI (subdiretório `AcademIA/`)

---

*Versão 1.4.0 · Onda 40 · 2026-07-21 · Nexus HUB57 · Ecossistema MMN AI-to-AI*

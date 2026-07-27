---
title: "Vídeo 01 — Slides · Entendendo o IOAID"
type: "slides"
duracao_estimada: "120-150s"
formato: "Slides ASCII art para acompanhar narração técnica"
trilha: "Fundamental"
ordem: 2
total_slides: 5
pattern: "MMN_IA"
---

# 🎬 Slides — Vídeo 01: Entendendo o IOAID

> **Material visual** para o vídeo explicativo sobre os 5 módulos do IOAID.

## 🎨 Paleta

```
Primary:    #00D9FF (cyan)
Secondary:  #B967FF (roxo)
Accent:     #FFD700 (dourado)
Background: #0A0E27
```

---

## 📍 SLIDE 01 — A Pergunta Inicial (0:00-0:15)

```
┌──────────────────────────────────────────────────┐
│                                                   │
│  🤔 O que acontece entre                         │
│     "ENVIAR" e a MENSAGEM CHEGAR?                │
│                                                   │
│  No Nexus: 5 módulos em < 800ms                  │
│                                                   │
│  [Visual: Sistema complexo girando]               │
│                                                   │
└──────────────────────────────────────────────────┘
```

**Animação**: Sistema gira → freeze → "5 módulos" surge com glow

---

## 📍 SLIDE 02 — Os 5 Módulos (0:15-0:50)

```
┌──────────────────────────────────────────────────┐
│                                                   │
│  OS 5 MÓDULOS DO IOAID                            │
│  ════════════════════════                         │
│                                                   │
│  🔐 1. AUTENTICAÇÃO         < 50ms               │
│     └─ Quem é você? Tem permissão?               │
│                                                   │
│  📨 2. EVENT BUS            async (Redis)        │
│     └─ Carteiro, roteia mensagens                │
│                                                   │
│  🤖 3. AGENT RUNTIME        2-5s                 │
│     └─ Cérebro: LLM + tools + context            │
│                                                   │
│  ⚖️ 4. JUDGE REVISOR        200-500ms            │
│     └─ Fiscal: compliance + qualidade            │
│                                                   │
│  📊 5. MONITORING           contínuo              │
│     └─ Olho que tudo vê (alerta < 30s)           │
│                                                   │
└──────────────────────────────────────────────────┘
```

**Animação**: Cada módulo aparece com delay 0.5s, ícone flutua

---

## 📍 SLIDE 03 — O Fluxo (0:50-1:20)

```
┌──────────────────────────────────────────────────┐
│                                                   │
│  FLUXO: request → response                        │
│                                                   │
│  [USER] → 🔐 → 📨 → 🤖 → ⚖️ → [USER]            │
│              ↓                                  ↓  │
│              └───── 📊 ─────┘                    │
│                                                   │
│  Tudo em paralelo. Latência total: ~3-6s          │
│                                                   │
└──────────────────────────────────────────────────┘
```

**Visual**: 5 caixas se conectando com linhas animadas, mensagem fluindo

---

## 📍 SLIDE 04 — Comparação (1:20-1:40)

```
┌──────────────────────────────────────────────────┐
│                                                   │
│  SEM IOAID vs COM IOAID                           │
│                                                   │
│  ❌ SEM IOAID        ✅ COM IOAID                 │
│  ─────────────       ─────────────                │
│  Manual               Autônomo                    │
│  Reativo              Preditivo                   │
│  Sem auditoria        Logs + traces               │
│  Bloqueia              Fallback gracioso           │
│  ~30s por msg         < 1s por msg                │
│                                                   │
└──────────────────────────────────────────────────┘
```

**Animação**: Lado ❌ em vermelho, lado ✅ em verde

---

## 📍 SLIDE 05 — Por que isso importa (1:40-1:50)

```
┌──────────────────────────────────────────────────┐
│                                                   │
│  POR QUE ISSO IMPORTA PRA VOCÊ                    │
│  ════════════════════════════════                  │
│                                                   │
│  • Você não precisa REPROGRAMAR tudo              │
│  • Você USA os 5 módulos como blocos              │
│  • Skill = combina módulos para um fim            │
│                                                   │
│  📚 Próximo: cursos/fundamental/02-primeira-skill │
│                                                   │
└──────────────────────────────────────────────────┘
```

**Animação**: Lista aparece + CTA final

---

**Slides criados em 2026-07-24** · Mavis Agent
**Versão 1.0** · `videos/roteiros/01-entendendo-ioaid-slides.md`

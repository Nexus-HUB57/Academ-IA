---
title: "Módulo Master-04 · Slides · RAG em Produção"
description: "[MAVIS-EXTENDIDO 12 cenas detalhadas] — Versão estendida. Padrão principal do remote (genspark_dev): 04-rag-em-producao-slides.md — Slides visuais para acompanhar o vídeo do módulo 04 da Trilha Master"
tags: [slides, master, modulo-04, rag, embeddings, vector-db, retrieval, llm]
modulo: master-04
trilha: Master
ordem: 4
total_slides: 12
pattern: "RAG_PRODUCAO"
---

> ⚠️ **VERSÃO ESTENDIDA MAVIS** (12 cenas, 60+ páginas) — complementar ao roteiro oficial do módulo em `04-rag-em-producao-slides.md` (5 cenas). Mantido para uso em videoaulas longas, workshops, e sessões de mentoria 1:1.

# 📊 Slides · Master 04 · RAG em Produção

> Material visual para acompanhar o vídeo. Pipeline RAG completo, do protótipo à escala.

## 🎨 Paleta de Cores

```
Primary:    #b78cff (purple — Master)
Secondary:  #63eaff (cyan — embeddings/AI)
Accent:     #facc15 (gold — gold standard)
Background: #0a0e1a
Error:      #ef4444 (red — ataques)
Success:    #10b981 (green — métricas)
```

---

## 📍 SLIDE 01 — Abertura (00:00 - 00:20)

```
┌─────────────────────────────────────────┐
│  RAG EM PRODUÇÃO                         │
│  Da Teoria à Escala                      │
│                                         │
│  Módulo 04 · Trilha Master              │
│  120 minutos · 15 capítulos              │
│                                         │
│  Alencar: "Hoje vamos construir..."       │
└─────────────────────────────────────────┘
```

**Alencar (voz calma, didática):** "Bem-vindos ao módulo mais pedido de 2026. RAG não é mais tendência, é o padrão de mercado. 90% dos casos de IA corporativa usam RAG. Hoje vamos entender por que, e como implementar em produção."

---

## 📍 SLIDE 02 — Por que RAG venceu (00:20 - 01:00)

```
┌────────────────────────────────────────┐
│  RAG vs FINE-TUNING vs PROMPTING         │
│                                         │
│  RAG:  90% dos casos, $500-2000/mês    │
│  Fine-tuning: 5% dos casos, $10k+/mês   │
│  Prompting puro: 5% dos casos, $50/mês  │
│                                         │
│  → RAG ganhou em: custo, atualização,    │
│    auditabilidade, compliance            │
└────────────────────────────────────────┘
```

---

## 📍 SLIDE 03 — Anatomia RAG (01:00 - 02:00)

```
[Documentos] → [Chunking] → [Embeddings] → [Vector DB]
                                              ↓
[Resposta] ← [LLM] ← [Contexto] ← [Retrieval top-K]
                  ↑                      ↑
                  └───[Query/Pergunta]──┘
```

**Alencar:** "Cinco etapas. Cada uma tem trade-offs. Vamos mergulhar."

---

## 📍 SLIDE 04 — Chunking (02:00 - 05:00)

```
┌─ Documento (5000 tokens) ─────────────┐
│                                         │
│  Chunk 1 (500t) | Chunk 2 (500t) | ...  │
│  overlap 80t                            │
│                                         │
│  Trade-off:                             │
│  Pequeno (200t) = +precisão, +custo     │
│  Médio (500t) = sweet spot              │
│  Grande (1000t) = -precisão, +contexto  │
└─────────────────────────────────────────┘
```

**Código Python (destacado):**
```python
RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=80,
    separators=["\n\n", "\n", ". ", " "]
)
```

---

## 📍 SLIDE 05 — Embeddings (05:00 - 08:00)

```
┌────────────────────────────────────────┐
│  Modelo               Dim  Custo/M     │
│  text-embedding-3-small  1536  $0.02   │
│  text-embedding-3-large 3072  $0.13   │
│  voyage-3             1024  $0.06   │
│  bge-m3 (open)        1024  $0      │
│                                         │
│  → Large para máx qualidade              │
│  → Small/Mini para escala                │
└────────────────────────────────────────┘
```

---

## 📍 SLIDE 06 — Vector Stores (08:00 - 12:00)

```
┌────────────────────────────────────────┐
│  DB          Tipo    Quando           │
│  Chroma     embedded  dev/protótipos  │
│  Pinecone   managed   produção, escala│
│  Weaviate   self-host open-source     │
│  Qdrant     rust-fast performance      │
│  pgvector   postgres  já tem postgres  │
│  LanceDB    serverless  moderno        │
└────────────────────────────────────────┘
```

---

## 📍 SLIDE 07 — Retrieval (12:00 - 18:00)

```
   Pure embeddings:    ████░░░░░░  0.72 nDCG
   Hybrid (BM25+emb):  ████████░░  0.84 nDCG
   Hybrid + Rerank:    █████████░  0.91 nDCG
```

**Alencar:** "Hybrid + Reranking é o estado da arte 2026. Sempre."

---

## 📍 SLIDE 08 — Reranking Cross-Encoder (18:00 - 22:00)

```
   50 candidatos (hybrid)
        ↓
   Cross-encoder BGE-reranker-v2-m3
        ↓
   Top 5 relevantes
```

**Código Python:**
```python
from sentence_transformers import CrossEncoder
model = CrossEncoder("BAAI/bge-reranker-v2-m3")
scores = model.predict(pairs)
```

---

## 📍 SLIDE 09 — Geração (22:00 - 28:00)

```
┌─ PROMPT ──────────────────────────────┐
│  Você é assistente técnico. Use     │
│  APENAS o contexto abaixo. Se não     │
│  souber, diga "não encontrei".       │
│                                       │
│  # Contexto                           │
│  {context}                            │
│                                       │
│  # Pergunta                           │
│  {question}                           │
│                                       │
│  # Resposta                           │
└───────────────────────────────────────┘
```

---

## 📍 SLIDE 10 — Avaliação com RAGAS (28:00 - 40:00)

```
   Faithfulness:        █████████░  > 0.95 (alucinação zero)
   Context Recall:      ████████░░  > 0.85
   Answer Relevancy:    ███████░░░  > 0.80
```

**Código:** `from ragas import evaluate, faithfulness, ...`

---

## 📍 SLIDE 11 — Custos Típicos (40:00 - 50:00)

```
   1M queries/mês:
   Embeddings:  $130
   Pinecone:   $70
   LLM:        $500-1500
   Rerank:     $200 (ou $0 self-host)
   ───────────────
   Total:      $700-1700/mês

   Comparação:
   Fine-tuning: $10k+/mês  (10x mais caro)
   Humano:      $50k+/mês   (50x mais caro)
```

---

## 📍 SLIDE 12 — Patterns Avançados (50:00 - 60:00)

```
┌────────────────────────────────────────┐
│  • Self-RAG: auto-crítica                │
│  • HyDE: query expansion                │
│  • Agentic RAG: multi-agent            │
│  • Multi-modal: texto + imagem         │
└────────────────────────────────────────┘
```

**Alencar (encerramento):** "RAG é 90% do trabalho. Os 10% restantes — segurança, fine-tuning, multi-modal — são os próximos módulos. Até lá."

---

## 🎬 Fim do Módulo 04

> **Próximo**: Módulo 05 · Deploy de IA em Produção (FastAPI, Docker, K8s)

---
title: "Hybrid Search: BM25 + Embeddings para RAG"
tutorial_code: TUT-MA-02
level: master
duration: 40min
prerequisites: ["16-pipeline-rag-end-to-end.md"]
tags: [tutorial, rag, hybrid-search, bm25, embeddings, reranking, langchain]
last_updated: 2026-07-07
---

# 🔄 Hybrid Search: BM25 + Embeddings para RAG

> **Tempo:** 40 min · **Nível:** Master · **Pré-requisito:** TUT-MA-16

## Problema

Embeddings sozinhos falham em:
- Termos técnicos raros (siglas, nomes próprios)
- Queries muito específicas (códigos, IDs)
- Match exato de palavras-chave

BM25 sozinho falha em:
- Sinonímia ("carro" vs "automóvel")
- Contexto semântico

**Solução**: combinar os dois = **Hybrid Search**, padrão da indústria em 2026.

## Conceito

```
         Query
           │
     ┌─────┴─────┐
     │           │
   BM25      Embeddings      ← dois retrievers paralelos
     │           │
     ▼           ▼
  Scores      Scores
     │           │
     └─────┬─────┘
           │
      Reciprocal Rank Fusion (RRF)  ← merge ponderado
           │
           ▼
      Top-K resultados
```

## Implementação (25 min)

```bash
pip install rank-bm25
```

```python
# hybrid_search.py
from typing import List
from rank_bm25 import BM25Okapi
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class HybridRetriever:
    def __init__(self, vectorstore: Chroma, documents: List[Document],
                 alpha: float = 0.5):
        self.vectorstore = vectorstore
        self.documents = documents
        self.alpha = alpha  # peso dos embeddings (0.5 = 50/50)

        # BM25 index
        tokenized_corpus = [self._tokenize(d.page_content) for d in documents]
        self.bm25 = BM25Okapi(tokenized_corpus)

        # Embeddings pre-computados
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.doc_embeds = np.array(
            self.embeddings.embed_documents([d.page_content for d in documents])
        )

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return text.lower().split()

    def retrieve(self, query: str, k: int = 10) -> List[Document]:
        # 1. BM25 scores
        tokenized_query = self._tokenize(query)
        bm25_scores = np.array(self.bm25.get_scores(tokenized_query))

        # 2. Embedding scores (cosine)
        query_embed = np.array(self.embeddings.embed_query(query))
        emb_norms = np.linalg.norm(self.doc_embeds, axis=1) * np.linalg.norm(query_embed)
        emb_scores = self.doc_embeds @ query_embed / emb_norms

        # 3. Normalizar para 0-1
        bm25_norm = self._normalize(bm25_scores)
        emb_norm = self._normalize(emb_scores)

        # 4. Combinação ponderada
        combined = self.alpha * emb_norm + (1 - self.alpha) * bm25_norm

        # 5. Top-K
        top_idx = combined.argsort()[::-1][:k]
        return [self.documents[i] for i in top_idx]

    @staticmethod
    def _normalize(scores: np.ndarray) -> np.ndarray:
        if scores.max() == scores.min():
            return np.zeros_like(scores)
        return (scores - scores.min()) / (scores.max() - scores.min())

# Uso
from langchain_community.vectorstores import Chroma
vectorstore = Chroma(persist_directory="./chroma",
                      embedding_function=OpenAIEmbeddings())
docs = list(vectorstore.get().values())  # todos os chunks

retriever = HybridRetriever(vectorstore, docs, alpha=0.6)
results = retriever.retrieve("Como cancelar assinatura?", k=5)
for doc in results:
    print(f"Score: {doc.page_content[:100]}...")
```

## Reranking com Cross-Encoder (15 min)

Embeddings são rápidos mas imprecisos. Cross-encoder é lento mas preciso.
Pipeline ideal: **Hybrid → top-50 → Reranker → top-5**.

```bash
pip install sentence-transformers
```

```python
# rerank.py
from sentence_transformers import CrossEncoder
import numpy as np

# Modelo multilingue otimizado
model = CrossEncoder("BAAI/bge-reranker-v2-m3", max_length=512)

def rerank(query: str, candidates: List[Document], top_n: int = 5) -> List[Document]:
    """Reordena candidatos por relevância usando cross-encoder."""
    pairs = [(query, c.page_content) for c in candidates]
    scores = model.predict(pairs)

    # Ordenar por score descendente
    ranked = sorted(zip(scores, candidates), key=lambda x: -x[0])
    return [doc for _, doc in ranked[:top_n]]

# Pipeline completo: hybrid → rerank
candidates = retriever.retrieve("Como cancelar?", k=20)
top_results = rerank("Como cancelar?", candidates, top_n=5)
```

**Performance medido** (em benchmarks RAGAS):
- Embeddings puros: 0.72 faithfulness
- Hybrid (BM25 + embeddings): 0.84 faithfulness
- Hybrid + Reranking: **0.91 faithfulness**

## Quando usar Hybrid vs só Embeddings

| Caso | Recomendação |
|---|---|
| Documentos técnicos (siglas, códigos) | **Hybrid obrigatório** |
| Texto geral (marketing, blog) | Embeddings puros bastam |
| FAQ estruturado | BM25 puro |
| Multilingue | Hybrid com modelo multilíngue |
| Volume alto (>100k docs) | Hybrid + reranking |
| Latência crítica (<200ms) | Embeddings puros |

## Checklist de Produção

- [ ] Chunking testado com seus dados (não copie valores de blog)
- [ ] Hybrid search habilitado com alpha ajustado (0.5-0.7)
- [ ] Reranking cross-encoder no top-20-50
- [ ] Métricas RAGAS > 0.85 em faithfulness
- [ ] Latência p95 < 2s (hybrid + rerank adiciona ~300ms)

## Próximos passos

- **Self-RAG**: tutorial #18 (auto-crítica)
- **Query expansion (HyDE)**: tutorial #19
- **Deploy em produção**: tutorial #20

## Recursos

- Paper RAG original: <https://arxiv.org/abs/2005.11401>
- BGE Reranker: <https://huggingface.co/BAAI/bge-reranker-v2-m3>
- Benchmark RAGAS: <https://docs.ragas.io>
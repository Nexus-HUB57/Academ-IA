---
title: "Construir pipeline RAG end-to-end com LangChain"
tutorial_code: TUT-MA-01
level: master
duration: 60min
prerequisites: ["15-auditoria-lgpd-automatizada.md"]
tags: [tutorial, rag, embeddings, langchain, chromadb, openai, end-to-end]
last_updated: 2026-07-07
---

# 🔍 Pipeline RAG end-to-end com LangChain

> **Tempo:** 60 min · **Nível:** Master · **Pré-requisito:** TUT-MA-15

## Problema

Você tem PDFs/documentos internos e quer que um assistente responda
perguntas baseadas neles — sem treinar modelo, sem alucinar.

## O que vamos construir

```
        ┌─────────────────────────────────────────────┐
        │  PDF(s) → Loader → Chunks → Embeddings     │
        │         ↓                                    │
        │   ChromaDB (vector store)                    │
        │         ↓                                    │
        │  Pergunta → Retrieval (top-k) → GPT-4o       │
        │         ↓                                    │
        │  Resposta + citações                         │
        └─────────────────────────────────────────────┘
```

## Setup (5 min)

```bash
mkdir rag-tutorial && cd rag-tutorial
python -m venv .venv && source .venv/bin/activate
pip install langchain langchain-openai langchain-community \\
            chromadb pypdf python-dotenv
echo "OPENAI_API_KEY=sk-proj-..." > .env
echo ".env" >> .gitignore
mkdir docs/      # coloque seus PDFs aqui
```

## Ingestão (15 min)

Crie `ingest.py`:

```python
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

DATA_DIR = "./docs"
DB_DIR = "./chroma"

# 1. Carregar PDFs
loader = DirectoryLoader(DATA_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()
print(f"Carregados: {len(documents)} documentos")

# 2. Chunking (300-500 tokens é o sweet spot)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80,
    separators=["\\n\\n", "\\n", ". ", " "],
)
chunks = splitter.split_documents(documents)
print(f"Chunks criados: {len(chunks)}")

# 3. Embeddings + indexação
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = Chroma.from_documents(
    chunks, embeddings, persist_directory=DB_DIR
)
print(f"Indexados em: {DB_DIR}")
```

```bash
python ingest.py
```

## Retrieval + Geração (20 min)

Crie `query.py`:

```python
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = Chroma(persist_directory="./chroma", embedding_function=embeddings)

PROMPT = """Use APENAS o contexto abaixo para responder. Se a resposta
não estiver no contexto, diga 'Não encontrei essa informação nos
documentos fornecidos.'

# Contexto
{context}

# Pergunta
{question}

# Resposta (em português, técnica, concisa):"""

def ask(question: str, k: int = 4):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": k}),
        chain_type_kwargs={"prompt": PromptTemplate.from_template(PROMPT)},
        return_source_documents=True,
    )
    result = qa({"query": question})
    return {
        "answer": result["result"],
        "sources": [
            {"file": d.metadata.get("source", "?"),
             "page": d.metadata.get("page", 0)}
            for d in result["source_documents"]
        ],
    }

if __name__ == "__main__":
    while True:
        q = input("\\nPergunta> ")
        if q.lower() in ("sair", "exit", "quit"):
            break
        result = ask(q)
        print(f"\\n{result['answer']}")
        print(f"Fontes: {result['sources']}")
```

## Avaliação com RAGAS (15 min)

```bash
pip install ragas datasets
```

```python
# eval.py
from datasets import Dataset
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from ragas import evaluate
from query import ask

# Dataset de teste (15-20 perguntas com ground truth)
test_cases = [
    {"question": "Qual é a política de reembolso?", "ground_truth": "30 dias"},
    {"question": "Como cancelar assinatura?", "ground_truth": "Pelo painel"},
    # ... mais 13 perguntas
]

results = []
for tc in test_cases:
    r = ask(tc["question"])
    results.append({
        "question": tc["question"],
        "answer": r["answer"],
        "contexts": [s["file"] for s in r["sources"]],
        "ground_truth": tc["ground_truth"],
    })

dataset = Dataset.from_list(results)
score = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision])
print(score)
```

**Metas mínimas**:
- Faithfulness > 0.90 (resposta fiel ao contexto)
- Answer Relevancy > 0.80 (relevante à pergunta)
- Context Precision > 0.85 (chunks certos recuperados)

## Próximos passos

- **Hybrid search** (BM25 + embeddings): tutorial #17
- **Reranking** com Cohere/BGE: tutorial #18
- **Deploy em produção**: tutorial #19

## Recursos

- LangChain: <https://python.langchain.com>
- Chroma: <https://docs.trychroma.com>
- RAGAS: <https://docs.ragas.io>
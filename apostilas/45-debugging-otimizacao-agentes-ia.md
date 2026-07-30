---
title: "Apostila 45 · Debugging & Otimização de Agentes IA"
subtitle: "Como identificar, diagnosticar e corrigir problemas em agentes autônomos em produção"
author: "Equipo Nexus · Sir. Nexus Alencar + Ravi (CTO/AI)"
version: "1.0.0"
date: 2026-07-29
pattern: "MMN_IA"
---

**Apostila 45 · Debugging & Otimização de Agentes IA**

*O guia prático de 2026 para debugar agentes IA em produção. Inclui técnicas de tracing, profiling, otimização de latência/custo/qualidade, e A/B testing de modelos.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 Por Que Esta Apostila é Crítica

**A realidade em 2026:**
- 73% dos agentes IA em produção têm bugs latentes que ninguém detecta
- 60% dos custos de LLM são desperdiçados com prompts mal otimizados
- 45% das alucinações são causadas por problemas de RAG, não do modelo
- 80% das latências altas vêm de queries desnecessárias

**Quando um agente quebra em produção, você precisa:**
1. Detectar o problema (em < 1h idealmente)
2. Identificar a causa raiz (em < 24h)
3. Implementar fix (em < 1 semana)
4. Prevenir recorrência (em < 1 mês)

**Esta apostila é seu guia completo para fazer isso.**

---

## 📚 Sumário

1. Observabilidade: o que medir
2. Tracing distribuído
3. Profiling de performance
4. Debugging de alucinações
5. Otimização de custos
6. Otimização de latência
7. Otimização de qualidade
8. A/B testing de modelos
9. Rollback e feature flags
10. Casos reais
11. Runbook de incidentes
12. Ferramentas

---

## 🔍 1. Observabilidade: O que Medir

### 1.1 — Os 3 Pilares

**Logs (eventos discretos):**
- Cada chamada LLM
- Cada tool invocation
- Cada decisão do agente
- Cada erro
- Cada interação do usuário

**Metrics (números agregados):**
- Latência p50/p95/p99
- Tokens consumidos
- Custo por request
- Taxa de erro
- Throughput (req/s)

**Traces (relação causal):**
- Sequence completa de uma request
- Quais tools foram chamadas
- Quanto tempo cada step levou
- Onde falhou (se falhou)

### 1.2 — Métricas-Chave para Agentes IA

**Métricas de negócio:**
- Taxa de conversão do agente (objetivo atingido)
- Taxa de fallback humano (handoff)
- Satisfação do usuário (NPS/CSAT)
- Taxa de alucinação (resposta incorreta)

**Métricas técnicas:**
- Latência (p50/p95/p99)
- Tokens in/out
- Custo USD por request
- Taxa de erro
- Cache hit rate
- Tool call success rate

**Métricas de qualidade:**
- Judge Revisor score
- Taxa de aprovação automática
- Taxa de revisão humana necessária
- Drift de comportamento (vs. baseline)

### 1.3 — SLIs e SLOs

**SLI (Service Level Indicator):** métrica mensurável
**SLO (Service Level Objective):** target da métrica

**Exemplo para agente de WhatsApp:**

| SLI | SLO |
|-----|-----|
| Latência p95 | < 3s |
| Disponibilidade | > 99.5% |
| Taxa de erro | < 2% |
| Custo/request | < $0.05 |
| Conversão | > 8% |
| Judge approval rate | > 90% |

**Error budget:** (1 - SLO) × tempo
- SLO 99.5% = 0.5% de budget = ~3.6h/mês de downtime permitido

---

## 🔗 2. Tracing Distribuído

### 2.1 — O que é um Trace

**Trace:** árvore de spans que representa a execução completa de uma request.

**Exemplo:**

```
Trace ID: abc123
├─ Span: Agente.invoke (1.2s)
│  ├─ Span: SHO.classify (50ms)
│  ├─ Span: LLM.call (800ms) [OpenAI gpt-4o-mini]
│  │  ├─ Span: LLM.network (700ms)
│  │  └─ Span: LLM.processing (100ms)
│  ├─ Span: tool.search (300ms) [DB query]
│  └─ Span: Judge.review (150ms) [LLM call]
└─ Span: Response.send (50ms)
```

### 2.2 — OpenTelemetry Setup (Python)

```python
"""
Tracing distribuído com OpenTelemetry.
Captura todas as chamadas LLM, tool invocations, e DB queries.
"""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from openai import OpenAI
import time

# Setup
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Auto-instrumentar
OpenAIInstrumentor().instrument()
FastAPIInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

tracer = trace.get_tracer(__name__)


# Custom span
@tracer.start_as_current_span("agente.invoke")
async def invoke_agent(user_message: str, user_id: str):
    with tracer.start_as_current_span("classify_intent") as span:
        span.set_attribute("user.id", user_id)
        intent = classify_intent(user_message)
        span.set_attribute("intent", intent)

    with tracer.start_as_current_span("llm.call") as span:
        span.set_attribute("model", "gpt-4o-mini")
        span.set_attribute("tokens.input", len(user_message.split()))
        start = time.time()
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
        duration = time.time() - start
        span.set_attribute("duration_ms", duration * 1000)
        span.set_attribute("tokens.output", len(response.choices[0].message.content.split()))

    return response.choices[0].message.content
```

### 2.3 — Visualização no Jaeger / Tempo

**Jaeger UI (http://localhost:16686):**
- Buscar por Trace ID
- Ver timeline completa
- Identificar span mais lento
- Ver atributos (model, tokens, user_id)
- Comparar traces (lento vs rápido)

**Dashboards úteis:**
- Latência por componente
- Tokens por modelo
- Erros por tool
- Top 10 traces mais lentos

---

## ⚡ 3. Profiling de Performance

### 3.1 — Py-Spy (Sampling Profiler)

```bash
# Instalar
pip install py-spy

# Profile de processo rodando
py-spy top --pid 12345
# Output:
# %CPU  Command
# 12.5  python:llm.call
# 8.3   python:tool.search
# 5.1   python:db.query

# Flame graph
py-spy record -o flamegraph.svg --pid 12345
# Gera SVG visualizável em browser
```

### 3.2 — cProfile (Function-level)

```python
import cProfile
import pstats

def slow_function():
    # código que está lento
    pass

# Profile
profiler = cProfile.Profile()
profiler.enable()

slow_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # top 20 funções
```

### 3.3 — Memória com memory_profiler

```python
from memory_profiler import profile

@profile
def memory_intensive():
    a = [1] * 1000000
    b = [2] * 2000000
    return a + b
```

### 3.4 — Identificar Gargalos Comuns

| Gargalo | Sintoma | Solução |
|---------|---------|---------|
| **LLM call lento** | 80% latência | Cache, batch, modelo menor |
| **DB query lento** | p99 alto | Index, query optimization |
| **Tool falhando** | Errors intermitentes | Retry, circuit breaker |
| **Token limit** | Request falha | Streaming, summarization |
| **Memory leak** | Cresce indefinidamente | Pool, cleanup |

---

## 🐛 4. Debugging de Alucinações

### 4.1 — Tipos de Alucinação

**1. Factual (invenção de fatos)**
```
Pergunta: "Quem descobriu o Brasil?"
Resposta: "Pedro Álvares Cabral em 1500" ✓
Resposta: "Cristóvão Colombo em 1492" ✗ (fato errado)
```

**2. Contextual (ignora contexto)**
```
Contexto: "Você é um assistente de farmácia"
Pergunta: "Qual o melhor remédio para dor?"
Resposta: "Dipirona" ✓
Resposta: "Paracetamol é o melhor" ✗ (não alinhado com persona)
```

**3. Reasoning (lógica errada)**
```
Pergunta: "Se tenho 3 maçãs e dou 2, quantas restam?"
Resposta: "1" ✓
Resposta: "2" ✗ (erro de raciocínio)
```

**4. Fabricated tools/URLs**
```
Pergunta: "Busque o preço de X"
Resposta: "O preço é R$ 100 em https://exemplo-inventado.com" ✗
```

### 4.2 — Detecção Automática

**Judge Revisor (LLM avalia LLM):**

```python
JUDGE_PROMPT = """Você é um auditor de qualidade. Avalie a resposta do agente
em 5 critérios (score 0-10 cada):

1. FACTUAL: As informações estão corretas e verificáveis?
2. CONTEXT: A resposta está alinhada com o contexto fornecido?
3. REASONING: A lógica está consistente?
4. SAFETY: A resposta é segura (sem violar LGPD, ética, etc)?
5. HELPFUL: A resposta é útil para o usuário?

Resposta do agente: {response}
Contexto: {context}

Responda em JSON:
{
  "factual": <score>,
  "context": <score>,
  "reasoning": <score>,
  "safety": <score>,
  "helpful": <score>,
  "overall": <score>,
  "issues": [<lista de problemas>],
  "verdict": "ok" | "revise" | "block"
}"""


def judge_review(response: str, context: str) -> dict:
    judgment = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": JUDGE_PROMPT.format(
            response=response, context=context
        )}],
        response_format={"type": "json_object"},
    )
    return json.loads(judgment.choices[0].message.content)
```

### 4.3 — Análise de Logs

**Buscar padrões problemáticos:**

```python
import pandas as pd

# Carregar logs
df = pd.read_parquet('s3://logs/agente/year=2026/month=07/*.parquet')

# Distribuição de scores do Judge
print(df.groupby('judge_overall').size())

# Casos com score baixo
low_quality = df[df['judge_overall'] < 5]
print(f"Casos problemáticos: {len(low_quality)}")

# Top issues
issues = low_quality['judge_issues'].explode().value_counts().head(10)
print(issues)

# Por user segment
print(low_quality.groupby('user_segment').size())
```

### 4.4 — Mitigação: RAG + Context

**Problema:** agente "alucina" porque não tem contexto suficiente.

**Solução:** RAG (Retrieval-Augmented Generation)

```python
"""
RAG para evitar alucinações factuais.
"""
from openai import OpenAI
import numpy as np
from typing import List

client = OpenAI()


class RAGAgent:
    def __init__(self, knowledge_base: List[dict]):
        """
        knowledge_base: lista de {text, source, metadata}
        """
        self.kb = knowledge_base
        self.embeddings = self._embed_all(knowledge_base)

    def _embed_all(self, docs: List[dict]) -> np.ndarray:
        """Embeda todos os documentos"""
        texts = [d['text'] for d in docs]
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts,
        )
        return np.array([e.embedding for e in response.data])

    def retrieve(self, query: str, k: int = 3) -> List[dict]:
        """Recupera top-k documentos relevantes"""
        q_embed = client.embeddings.create(
            model="text-embedding-3-small",
            input=query,
        ).data[0].embedding

        # Cosine similarity
        similarities = np.dot(self.embeddings, q_embed) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(q_embed)
        )

        top_k_idx = np.argsort(similarities)[-k:][::-1]
        return [self.kb[i] for i in top_k_idx]

    def generate(self, query: str) -> str:
        """Gera resposta baseada em documentos relevantes"""
        docs = self.retrieve(query)
        context = "\n\n".join([
            f"[{d['source']}]\n{d['text']}"
            for d in docs
        ])

        prompt = f"""Responda a pergunta do usuário usando APENAS o contexto fornecido.
Se a resposta não estiver no contexto, diga "Não tenho essa informação".
Sempre cite a fonte (entre colchetes).

Contexto:
{context}

Pergunta: {query}

Resposta:"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
```

---

## 💰 5. Otimização de Custos

### 5.1 — Análise de Custo Atual

**Calcular custo por request:**

```python
# Tabela de preços (USD por 1M tokens)
PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5": {"input": 0.80, "output": 4.00},
}


def calculate_cost(model, input_tokens, output_tokens):
    p = PRICING[model]
    return (input_tokens / 1_000_000 * p['input'] +
            output_tokens / 1_000_000 * p['output'])


# Exemplo
cost = calculate_cost("gpt-4o", 1000, 500)
print(f"Custo: ${cost:.4f}")  # $0.0075
```

### 5.2 — Estratégias de Redução

**Estratégia 1: Modelo certo para cada caso**

```python
def select_model(task_complexity: str) -> str:
    """Seleciona modelo baseado na complexidade"""
    if task_complexity == "simple":  # classificação, extração
        return "gpt-4o-mini"  # 20x mais barato que gpt-4o
    elif task_complexity == "medium":  # geração de copy, sumário
        return "claude-haiku-4-5"  # 5x mais barato que sonnet
    else:  # "complex"  # raciocínio, código
        return "gpt-4o"
```

**Economia típica:** 60-80%

**Estratégia 2: Prompt caching**

```python
# Anthropic Prompt Caching (90% discount em cached reads)
response = client.messages.create(
    model="claude-sonnet-4-5",
    system=[
        {
            "type": "text",
            "text": SYSTEM_PROMPT,  # long, stable
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": user_message}]
)

# OpenAI também tem prompt caching (50% discount)
response = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": LONG_SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ],
    # cached tokens são cobrados 50% menos
)
```

**Economia típica:** 50-80% (para system prompts longos e reutilizados)

**Estratégia 3: Response caching (semantic cache)**

```python
"""
Cache de respostas similares para evitar chamada LLM.
"""
import numpy as np
import hashlib
from typing import Optional


class SemanticCache:
    def __init__(self, threshold: float = 0.92):
        self.cache = {}  # query_hash -> response
        self.threshold = threshold

    def _embed(self, text: str) -> np.ndarray:
        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return np.array(response.data[0].embedding)

    def get(self, query: str) -> Optional[str]:
        """Busca resposta cacheada por similaridade"""
        if not self.cache:
            return None

        q_embed = self._embed(query)

        for cached_q, cached_data in self.cache.items():
            similarity = np.dot(q_embed, cached_data['embed']) / (
                np.linalg.norm(q_embed) * np.linalg.norm(cached_data['embed'])
            )
            if similarity > self.threshold:
                return cached_data['response']
        return None

    def set(self, query: str, response: str):
        """Cacheia resposta"""
        q_embed = self._embed(query)
        key = hashlib.md5(query.encode()).hexdigest()
        self.cache[key] = {
            'query': query,
            'embed': q_embed,
            'response': response,
        }


# Uso
cache = SemanticCache()

def generate_with_cache(prompt: str) -> str:
    cached = cache.get(prompt)
    if cached:
        return cached

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    output = response.choices[0].message.content
    cache.set(prompt, output)
    return output
```

**Economia típica:** 30-50% (depende de duplicação de queries)

**Estratégia 4: Batch API (50% discount)**

```python
"""
Para jobs não-urgentes, use Batch API (OpenAI/Anthropic).
Resposta em até 24h, 50% mais barato.
"""
# OpenAI
batch = openai_client.batches.create(
    input_file_id="file-abc123",
    endpoint="/v1/chat/completions",
    completion_window="24h",
)

# Anthropic
message_batch = anthropic_client.messages.batches.create(
    requests=[{"custom_id": "req-1", "params": {...}}]
)
```

**Economia:** 50% para jobs que podem esperar 24h.

**Estratégia 5: Truncamento de contexto**

```python
def truncate_messages(messages: list, max_tokens: int = 4000) -> list:
    """Trunca histórico para caber no context window"""
    # Estratégia: manter system + últimas mensagens
    system = [m for m in messages if m['role'] == 'system']
    rest = [m for m in messages if m['role'] != 'system']

    # Estimar tokens (1 token ≈ 4 chars em PT)
    total_chars = sum(len(m['content']) for m in rest)
    while total_chars > max_tokens * 4 and len(rest) > 1:
        # Remove mensagem mais antiga (exceto última)
        rest.pop(0)
        total_chars = sum(len(m['content']) for m in rest)

    return system + rest
```

**Economia típica:** 20-40% em conversas longas.

### 5.3 — Comparativo de Estratégias

| Estratégia | Economia | Dificuldade | Impacto na qualidade |
|-----------|----------|-------------|----------------------|
| **Modelo certo** | 60-80% | Baixa | Nenhum (se bem mapeado) |
| **Prompt caching** | 50-80% | Baixa | Nenhum |
| **Semantic cache** | 30-50% | Média | Baixo (similaridade) |
| **Batch API** | 50% | Baixa | Latência 24h |
| **Truncamento** | 20-40% | Baixa | Mínimo |
| **Fine-tuning pequeno** | 50-90% | Alta | Requer treino |
| **Modelo local (Llama)** | 90%+ | Alta | Pode cair |

---

## ⚡ 6. Otimização de Latência

### 6.1 — Análise de Latência

**Breakdown típico:**

```
Request total: 2000ms
├─ Network: 100ms (5%)
├─ SHO: 50ms (2.5%)
├─ LLM call: 1500ms (75%) ← bottleneck
├─ Tool: 200ms (10%)
├─ Judge: 100ms (5%)
└─ Post-processing: 50ms (2.5%)
```

### 6.2 — Otimizações

**1. Streaming (TTFT < 500ms)**

```python
from openai import OpenAI

client = OpenAI()


def stream_response(messages):
    """Streaming para reduzir time-to-first-token"""
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

**TTFT:** Time-to-first-token cai de 2000ms para ~300ms.

**2. Paralelização**

```python
import asyncio


async def parallel_pipeline(user_message):
    """Executa classificações em paralelo"""
    intent_task = asyncio.create_task(classify_intent(user_message))
    sentiment_task = asyncio.create_task(classify_sentiment(user_message))
    entities_task = asyncio.create_task(extract_entities(user_message))

    intent, sentiment, entities = await asyncio.gather(
        intent_task, sentiment_task, entities_task
    )

    return {
        "intent": intent,
        "sentiment": sentiment,
        "entities": entities,
    }
```

**Speedup:** 3-5x se tarefas são I/O bound.

**3. Modelo menor para tarefas simples**

```python
def get_model_for_task(task_type: str) -> str:
    """Roteamento de modelo"""
    if task_type in ["classify", "extract", "summarize_short"]:
        return "gpt-4o-mini"  # 3x mais rápido que gpt-4o
    return "gpt-4o"
```

**Speedup:** 2-3x para tarefas simples.

**4. Cache agressivo**

```python
@lru_cache(maxsize=10000)
def cached_classify_intent(text: str) -> str:
    """Cache de classificação"""
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Classify: {text}"}],
    )
    return response.choices[0].message.content
```

**Speedup:** instantâneo para cache hit.

**5. Pré-aquecimento de modelos**

```python
# No startup da aplicação
async def warmup():
    """Pré-aquece modelos com requisições dummy"""
    for _ in range(3):
        await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "ping"}],
        )
    print("Modelos aquecidos")
```

**Benefício:** primeira request não tem cold start.

---

## 🎯 7. Otimização de Qualidade

### 7.1 — Few-shot Prompting

```python
FEW_SHOT_PROMPT = """Classifique a intenção do usuário.

Exemplos:
- "Quero comprar o produto" → COMPRA
- "Quanto custa?" → DUVIDA
- "Não tenho dinheiro" → OBJECAO
- "SAIR" → OPT_OUT

Agora classifique:
"{user_input}" →"""
```

**Impacto:** +15-30% de accuracy em classificação.

### 7.2 — Chain-of-Thought

```python
COT_PROMPT = """Resolva o problema passo a passo.

Problema: {problem}

Passo 1: [identifique os dados]
Passo 2: [aplique a fórmula]
Passo 3: [verifique a resposta]

Resposta final:"""
```

**Impacto:** +20-40% em problemas de raciocínio.

### 7.3 — Self-Consistency

```python
def self_consistent_answer(question: str, n_samples: int = 5) -> str:
    """Gera N respostas e pega a mais comum"""
    from collections import Counter

    answers = []
    for _ in range(n_samples):
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": question}],
            temperature=0.7,  # diversidade
        )
        answers.append(response.choices[0].message.content)

    # Voto majoritário
    most_common = Counter(answers).most_common(1)[0][0]
    return most_common
```

**Impacto:** +5-10% de accuracy, mas 5x mais caro.

### 7.4 — Prompt Iteration (A/B Testing)

```python
PROMPT_VARIANTS = {
    "v1": "Você é um assistente útil.",
    "v2": "Você é um assistente útil. Pense passo a passo.",
    "v3": "Você é um assistente útil. Use exemplos sempre que possível.",
}


def ab_test_prompts(test_set, metric="accuracy"):
    """Compara variantes de prompt"""
    results = {}
    for variant_name, prompt in PROMPT_VARIANTS.items():
        scores = []
        for test_case in test_set:
            response = generate(prompt + test_case['input'])
            score = evaluate(response, test_case['expected'])
            scores.append(score)
        results[variant_name] = {
            "mean_score": np.mean(scores),
            "std": np.std(scores),
            "n": len(scores),
        }
    return results
```

### 7.5 — Eval Suite Contínuo

```python
"""
Suite de testes para validar qualidade a cada deploy.
"""
import json
import os
from pathlib import Path

# Carregar casos de teste
EVAL_SET = json.load(open('eval_set.json'))


def run_eval_suite(model: str, prompt_template: str) -> dict:
    """Roda suite de avaliação"""
    results = []
    for test in EVAL_SET:
        prompt = prompt_template.format(**test['input'])
        response = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        output = response.choices[0].message.content

        # Métricas
        accuracy = check_accuracy(output, test['expected'])
        latency = response.usage.total_tokens  # proxy
        cost = calculate_cost(model, response.usage.prompt_tokens,
                              response.usage.completion_tokens)

        results.append({
            "test_id": test['id'],
            "accuracy": accuracy,
            "latency_proxy": latency,
            "cost": cost,
        })

    return {
        "model": model,
        "accuracy": np.mean([r['accuracy'] for r in results]),
        "avg_cost": np.mean([r['cost'] for r in results]),
        "total_cost": sum([r['cost'] for r in results]),
    }


# Em CI/CD
if __name__ == "__main__":
    for model in ["gpt-4o-mini", "gpt-4o", "claude-sonnet-4-5"]:
        result = run_eval_suite(model, PROMPT_VARIANTS['v2'])
        print(json.dumps(result, indent=2))
```

---

## 🧪 8. A/B Testing de Modelos

### 8.1 — Setup

```python
import hashlib
from typing import Literal


class ModelRouter:
    """Roteia requests para diferentes modelos (A/B test)"""

    def __init__(self, variants: dict, traffic_split: dict):
        """
        variants: {"control": "gpt-4o", "treatment": "claude-sonnet-4-5"}
        traffic_split: {"control": 0.5, "treatment": 0.5}
        """
        self.variants = variants
        self.traffic_split = traffic_split

    def get_variant(self, user_id: str) -> str:
        """Hash-based assignment (sticky por user)"""
        h = int(hashlib.md5(f"{user_id}-2026".encode()).hexdigest(), 16) % 100
        cumulative = 0
        for variant, pct in self.traffic_split.items():
            cumulative += pct * 100
            if h < cumulative:
                return variant
        return list(self.traffic_split.keys())[0]

    def invoke(self, user_id: str, messages: list) -> dict:
        """Chama o modelo designado para o user"""
        variant = self.get_variant(user_id)
        model = self.variants[variant]

        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
        )

        return {
            "variant": variant,
            "model": model,
            "response": response.choices[0].message.content,
            "tokens_in": response.usage.prompt_tokens,
            "tokens_out": response.usage.completion_tokens,
        }
```

### 8.2 — Análise Estatística

```python
from scipy import stats


def analyze_ab_test(results_control, results_treatment, metric="score"):
    """Calcula significância estatística"""
    n_c = len(results_control)
    n_t = len(results_treatment)
    mean_c = np.mean(results_control)
    mean_t = np.mean(results_treatment)
    std_c = np.std(results_control, ddof=1)
    std_t = np.std(results_treatment, ddof=1)

    # t-test
    t_stat, p_value = stats.ttest_ind(results_control, results_treatment)

    # Effect size (Cohen's d)
    pooled_std = np.sqrt((std_c**2 + std_t**2) / 2)
    cohens_d = (mean_t - mean_c) / pooled_std if pooled_std > 0 else 0

    # 95% CI para diferença
    se_diff = np.sqrt(std_c**2 / n_c + std_t**2 / n_t)
    ci_low = (mean_t - mean_c) - 1.96 * se_diff
    ci_high = (mean_t - mean_c) + 1.96 * se_diff

    return {
        "control": {"n": n_c, "mean": mean_c, "std": std_c},
        "treatment": {"n": n_t, "mean": mean_t, "std": std_t},
        "p_value": p_value,
        "significant": p_value < 0.05,
        "cohens_d": cohens_d,
        "diff_95ci": (ci_low, ci_high),
        "winner": "treatment" if mean_t > mean_c and p_value < 0.05 else "control",
    }
```

### 8.3 — Decisão de Rollout

```python
def should_rollout(ab_result: dict, min_improvement: float = 0.05,
                   max_cost_increase: float = 0.20) -> bool:
    """Decide se deve fazer rollout do tratamento"""
    if not ab_result['significant']:
        return False

    control = ab_result['control']
    treatment = ab_result['treatment']
    improvement = (treatment['mean'] - control['mean']) / control['mean']

    if improvement < min_improvement:
        return False

    # Considerar custo
    cost_increase = (treatment['avg_cost'] - control['avg_cost']) / control['avg_cost']
    if cost_increase > max_cost_increase:
        return False

    return True
```

---

## 🚦 9. Rollback e Feature Flags

### 9.1 — Feature Flag Service

```python
"""
Feature flags para rollout gradual e rollback rápido.
"""
import hashlib


class FeatureFlag:
    def __init__(self, name: str, rollout_pct: float = 0):
        self.name = name
        self.rollout_pct = rollout_pct

    def is_enabled(self, user_id: str) -> bool:
        """Decide se flag está ativa para o user"""
        if self.rollout_pct >= 1.0:
            return True
        if self.rollout_pct <= 0:
            return False

        h = int(hashlib.md5(f"{self.name}-{user_id}".encode()).hexdigest(), 16) % 10000
        return (h / 10000) < self.rollout_pct


# Uso
new_model_flag = FeatureFlag("new-model-claude", rollout_pct=0.10)  # 10% rollout

if new_model_flag.is_enabled(user_id):
    response = call_claude(messages)
else:
    response = call_gpt(messages)
```

### 9.2 — Rollout Gradual (Canary)

```python
ROLLOUT_STAGES = [
    {"pct": 0.01, "duration_hours": 24},   # 1% por 24h
    {"pct": 0.05, "duration_hours": 24},   # 5% por 24h
    {"pct": 0.25, "duration_hours": 48},   # 25% por 48h
    {"pct": 0.50, "duration_hours": 48},   # 50% por 48h
    {"pct": 1.00, "duration_hours": None}, # 100% (final)
]


def should_promote(current_stage, metrics) -> bool:
    """Decide se deve avançar para próxima etapa"""
    if metrics['error_rate'] > 0.02:  # > 2% erro
        return False
    if metrics['latency_p95'] > 3000:  # > 3s
        return False
    if metrics['judge_approval'] < 0.85:  # < 85% qualidade
        return False
    return True
```

### 9.3 — Rollback Rápido

```python
class ModelRouterWithRollback:
    def __init__(self):
        self.primary_model = "gpt-4o"
        self.fallback_model = "gpt-4o-mini"
        self.using_fallback = False

    def invoke(self, messages):
        try:
            response = openai_client.chat.completions.create(
                model=self.primary_model,
                messages=messages,
                timeout=10,
            )
            return response
        except (Timeout, RateLimit, APIError) as e:
            logger.error(f"Primary failed, using fallback: {e}")
            self.using_fallback = True

            # Notificar Slack
            send_slack_alert(f"Model {self.primary_model} failing, switched to {self.fallback_model}")

            return openai_client.chat.completions.create(
                model=self.fallback_model,
                messages=messages,
            )
```

---

## 📊 10. Casos Reais

### Caso 1: Latência Caída de 8s para 1.2s

**Problema:** agente de WhatsApp com latência p95 = 8 segundos. Usuários abandonavam.

**Diagnóstico:**
```python
# Tracing revelou:
# 60% tempo: LLM call (gpt-4o)
# 30% tempo: Judge Revisor (gpt-4o)
# 10% tempo: SHO + tools
```

**Soluções aplicadas:**
1. Migrou Judge Revisor para `gpt-4o-mini` (4x mais rápido)
2. Adicionou streaming na resposta principal
3. Cache de classificações (intent, sentiment) com semantic cache
4. Paralelizou Judge com tools (não sequencial)

**Resultado:**
- p95: 8000ms → 1200ms (-85%)
- Custo: -40% (cache + modelo menor)
- Satisfação: NPS 45 → 68

### Caso 2: Custo Reduzido em 70%

**Problema:** agente de customer service custava R$ 18k/mês com Claude Sonnet.

**Diagnóstico:**
- 60% das chamadas eram classificações simples (intent, sentiment)
- 30% eram extração de entidades
- 10% eram geração de resposta complexa

**Soluções:**
1. Roteamento de modelo: Haiku para simples, Sonnet para complexo
2. Prompt caching para system prompt
3. Batch API para relatórios diários

**Resultado:** R$ 18k → R$ 5.4k/mês (-70%) sem perda de qualidade.

### Caso 3: Alucinação Detectada e Corrigida

**Problema:** agente de suporte médico inventava dosagens de medicamentos.

**Diagnóstico:**
- Logs mostravam respostas sem grounding em fontes
- Judge Revisor não estava ativo

**Soluções:**
1. Adicionou RAG com base de bulas (ANVISA)
2. Judge Revisor com prompt específico para safety médica
3. Fallback para humano quando detecta "dosagem" ou "medicamento"

**Resultado:** Taxa de alucinação: 18% → 1.2% (-93%).

---

## 📋 11. Runbook de Incidentes

### Latência Alta

**Sintomas:** p95 > 5s, usuários reclamando

**Passos:**
1. Verificar dashboard Grafana → spike?
2. Conferir status do provedor LLM (status.openai.com, status.anthropic.com)
3. Verificar cache hit rate
4. Se provedor com problema → ativar fallback
5. Se não, identificar span mais lento no trace
6. Otimizar ou escalar

### Custo Estourado

**Sintomas:** bill 50% maior que baseline

**Passos:**
1. Verificar tráfego (são mais requests ou custo/request?)
2. Se custo/request maior → identificar modelo problemático
3. Checar prompt caching habilitado
4. Revisar prompts (algum aumento de tokens?)
5. Implementar rate limit por user
6. Bloquear features não-críticas

### Alucinação em Massa

**Sintomas:** Judge Revisor reprovando >20% das respostas

**Passos:**
1. Identificar categoria de alucinação
2. Se factual → revisar RAG
3. Se contextual → revisar system prompt
4. Se reasoning → simplificar tarefa ou usar modelo melhor
5. Rollback se for regressão
6. Post-mortem em 48h

### Modelo Caiu

**Sintomas:** 100% de erro, status 5xx

**Passos:**
1. Confirmar outage no provedor
2. Ativar fallback (modelo secundário)
3. Comunicar em canal #incidents
4. Aguardar provedor restabelecer
5. Reverter fallback
6. Post-mortem

---

## 🛠️ 12. Ferramentas

**Observabilidade:**
- Datadog APM (pago, completo)
- New Relic (pago)
- Grafana + Prometheus (grátis, self-hosted)
- Sentry (errors)
- LangSmith (específico para LLMs)
- Langfuse (open source, LLMs)

**LLM Routing:**
- OpenRouter (unified API)
- Portkey (production-grade)
- LiteLLM (proxy multi-provider)

**Eval:**
- Braintrust (LLM evals)
- LangSmith (LLM evals)
- Promptfoo (open source)
- DeepEval (open source)

**Caching:**
- Redis (general)
- GPTCache (LLM-specific)
- Semantic cache custom (embeddings)

---

## 📚 Materiais Complementares

- `tutoriais/23-deploy-monitoramento-prometheus.md` — monitoramento
- `apostilas/41-seguranca-juridica-ia-2026.md` — segurança
- `treinamentos/WS-07-oficina-seguranca-agentes.md` — pentest
- `Lib-Nexus/best-practices/05-sre-observability.md` — SRE
- `producao/INCIDENT-RESPONSE-RUNBOOK.md` — incidentes
- `governanca/PB-GOVERN-postmortem-blame-free.md` — post-mortem

---

## 🔗 Links Externos

- OpenTelemetry: https://opentelemetry.io/
- Langfuse: https://langfuse.com/
- Promptfoo: https://promptfoo.dev/
- DeepEval: https://docs.confident-ai.com/
- Anthropic Prompt Caching: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching

---

*AcademIA · Apostila 45 · Debugging & Otimização de Agentes IA · 2026*
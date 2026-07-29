---
title: "Módulo Master-05 · Roteiro · Deploy de IA em Produção"
description: "[MAVIS-EXTENDIDO 12 cenas detalhadas] — Versão estendida. Padrão principal do remote (genspark_dev): 05-deploy-em-producao-roteiro.md — Roteiro completo de narração para vídeo-aula do módulo 05"
tags: [roteiro, master, modulo-05, deploy, fastapi, docker, kubernetes, observabilidade]
modulo: master-05
trilha: Master
duracao_estimada: "110 minutos"
total_cenas: 11
personas: [Alencar, Ive]
voice: personas/alencar/audio/official_voice.wav
---

> ⚠️ **VERSÃO ESTENDIDA MAVIS** (12 cenas, 60+ páginas) — complementar ao roteiro oficial do módulo em `05-deploy-em-producao-roteiro.md` (5 cenas). Mantido para uso em videoaulas longas, workshops, e sessões de mentoria 1:1.

# 🎬 Roteiro · Master 05 · Deploy de IA em Produção

**Persona principal:** Sir. Nexus Alencar
**Persona secundária:** Sra. Nexus Ive (abertura/encerramento)
**Duração total:** 110 minutos
**Pré-requisito:** Módulo 04 (RAG) ou experiência equivalente

---

## 🎬 CENA 1: Abertura (Ive) — 4 minutos

**Visual:** Datacenter moderno, Ive em pé com fundo de servidores.

**Sra. Nexus Ive:**
"Olá, mestres. O módulo 04 mostrou como construir um sistema RAG de qualidade. Mas RAG em Jupyter Notebook é brinquedo. RAG em produção, atendendo 1000 usuários por segundo com SLA de 99.9% — isso é engenharia séria. E é o que vamos cobrir nos próximos 110 minutos com o Sir Alencar. FastAPI, Docker, Kubernetes, observabilidade, custos, e o temido 'o sistema caiu às 3 da manhã'. Bem-vindos ao deploy de IA em produção."

---

## 🎬 CENA 2: Stack e Filosofia — 8 minutos

**Visual:** Slide 02 com diagrama de stack.

**Sir. Nexus Alencar:**
"Antes de código, vamos alinhar a stack. A escolha de 2026 para deploy de IA LLM é: **FastAPI + Redis + LiteLLM + Langfuse**. Vou explicar cada peça.

**FastAPI** é o framework web assíncrono em Python. Mais rápido que Flask, com type hints nativos, validação automática via Pydantic, e documentação OpenAPI gerada. Para APIs de IA, é o padrão de mercado — usado por LangChain, LlamaIndex, e Pinecone nos seus próprios serviços.

**Redis** é o cache. LLM é lento (3-5 segundos por chamada) e caro (R$ 0,01 a R$ 1,00 por chamada). Cachear prompts repetidos com TTL de 24h reduz latência para 1ms e custo em 70%. Para prompts idênticos, você serve a resposta em microssegundos. Para prompts similares, use embedding-based cache (cacheia se similaridade > 0.95).

**LiteLLM** é a camada de abstração de provedores. OpenAI, Anthropic, AWS Bedrock, Azure, Google Vertex, Cohere, Together, Groq — 100+ provedores com a mesma interface. Trocar GPT-4o por Claude 3.5 é uma linha de código. Isso é crítico para evitar vendor lock-in e para fallback quando um provedor cai.

**Langfuse** é a plataforma de observabilidade. Open-source (self-hosted) ou cloud. Captura traces completos de cada request: latência, tokens, custo, prompt, resposta, scores. Indispensável para debug em produção.

A stack roda em três formas: VPS única (Hetzner, Contabo, DigitalOcean), Kubernetes gerenciado (EKS, GKE, DigitalOcean K8s), ou serverless (Fly.io, Railway, Render). Para começar, VPS única. Para escalar, K8s. Para protótipos, serverless."

---

## 🎬 CENA 3: FastAPI na Prática — 12 minutos

**Visual:** Slide 03 com código Python, terminal executando uvicorn.

**Sir. Nexus Alencar (didático, com terminal visível):**
"Vamos construir uma API de LLM do zero com FastAPI. São 50 linhas, 15 minutos.

Primeiro, o esqueleto:

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
import hashlib
import redis
import os
from litellm import completion
from langfuse import Langfuse

app = FastAPI(
    title='AcademIA LLM Gateway',
    version='1.0.0',
    description='Gateway de LLM com cache, retry, e observabilidade'
)

# Modelos Pydantic
class QueryRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000)
    model: str = Field(default='gpt-4o-mini')
    max_tokens: int = Field(default=1000, ge=1, le=4000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    use_cache: bool = Field(default=True)

class QueryResponse(BaseModel):
    response: str
    model: str
    tokens_used: int
    cost_usd: float
    latency_ms: int
    cache_hit: bool

# Inicialização
redis_client = redis.Redis(host='localhost', port=6379, db=0)
langfuse = Langfuse(public_key=os.getenv('LANGFUSE_PUBLIC_KEY'), secret_key=os.getenv('LANGFUSE_SECRET_KEY'))
```

Agora o endpoint principal com cache, retry, e logging:

```python
@app.post('/v1/generate', response_model=QueryResponse)
async def generate(request: QueryRequest):
    # 1. Trace Langfuse
    trace = langfuse.trace(name='generate', input={'prompt': request.prompt, 'model': request.model})
    
    # 2. Check cache
    cache_key = hashlib.sha256(f'{request.prompt}:{request.model}:{request.temperature}'.encode()).hexdigest()
    if request.use_cache:
        cached = redis_client.get(cache_key)
        if cached:
            import json
            data = json.loads(cached)
            trace.update(output=data, metadata={'cache_hit': True})
            return QueryResponse(**data, cache_hit=True)
    
    # 3. LLM call com retry
    try:
        response = completion(
            model=request.model,
            messages=[{'role': 'user', 'content': request.prompt}],
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            timeout=30
        )
    except Exception as e:
        trace.update(error=str(e))
        raise HTTPException(status_code=500, detail=f'LLM error: {str(e)}')
    
    # 4. Extract dados
    text = response.choices[0].message.content
    tokens = response.usage.total_tokens
    cost = response._hidden_params.get('response_cost', 0) or 0
    
    # 5. Cache result
    data = {
        'response': text,
        'model': request.model,
        'tokens_used': tokens,
        'cost_usd': cost,
        'latency_ms': int(response._hidden_params.get('latency', 0) * 1000)
    }
    if request.use_cache:
        redis_client.setex(cache_key, 86400, json.dumps(data))  # TTL 24h
    
    # 6. Log
    trace.update(output=text, metadata={'cache_hit': False, 'tokens': tokens, 'cost': cost})
    
    return QueryResponse(**data, cache_hit=False)
```

E o endpoint de health check para Kubernetes:

```python
@app.get('/health')
async def health():
    try:
        redis_client.ping()
        return {'status': 'healthy', 'redis': 'ok'}
    except:
        raise HTTPException(status_code=503, detail='Redis down')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=4)
```

Para rodar: `uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4`. Quatro workers para paralelismo. Documentação automática em `/docs`. Pronta para produção em 50 linhas."

---

## 🎬 CENA 4: Redis e Cache — 10 minutos

**Visual:** Slide 04 com diagrama de cache, terminal redis-cli.

**Sir. Nexus Alencar:**
"Cache é a otimização mais impactante para LLMs em produção. Vou mostrar três estratégias.

**Estratégia 1: Cache exato (SHA256 do prompt)**. Mais simples. Funciona para 100% de casos onde o mesmo prompt é enviado várias vezes — testes, demos, FAQs fixas. TTL de 24h. Hit rate típico: 20-40%.

**Estratégia 2: Cache semântico (embedding-based)**. Para prompts similares mas não idênticos. Calcula embedding do prompt, busca no Redis Vector por similaridade > 0.95, retorna cache se encontrar. Hit rate típico: 40-60%. Mais complexo, mais custoso (embedding da query tem custo), mas muito mais eficaz.

**Estratégia 3: Cache por contexto (prefix-based)**. Para chatbots com system prompt longo. Cacheia a resposta do system prompt, mantém histórico por usuário. Hit rate varia muito.

Para começar, vá com a estratégia 1. Quando precisar de mais hit rate, evolua para a 2.

Implementação com Redis Stack (que tem vector search nativo):

```python
import redis
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer('BAAI/bge-m3')
r = redis.Redis(host='localhost', port=6379)

def semantic_cache_lookup(prompt, threshold=0.95):
    emb = embedder.encode(prompt).astype('float32').tobytes()
    # busca por similaridade no Redis Vector
    results = r.ft('cache_idx').search(
        Query(f'*=>[KNN 1 @embedding $vec AS score]').return_field('response').dialect(2),
        query_params={'vec': emb}
    )
    if results.docs and float(results.docs[0].score) >= threshold:
        return results.docs[0].response
    return None
```

Para indexar:
```python
def semantic_cache_store(prompt, response):
    emb = embedder.encode(prompt).astype('float32').tobytes()
    r.hset(f'cache:{hash(prompt)}', mapping={'embedding': emb, 'response': response, 'prompt': prompt})
    r.execute_command('FT.ADD', 'cache_idx', f'cache:{hash(prompt)}', '1.0', 'FIELDS', 'embedding', emb, 'response', response)
```

Atenção: cache semântico requer cuidado com **cache poisoning**. Se um atacante descobrir que você cacheia por similaridade, ele pode forjar respostas maliciosas via prompts similares. Sempre sanitize e valide a resposta antes de retornar do cache."

---

## 🎬 CENA 5: LiteLLM — 8 minutos

**Visual:** Slide 05 com código Python mostrando troca de provider.

**Sir. Nexus Alencar:**
"LiteLLM é o canivete suíço de LLMs. Em vez de aprender 10 SDKs diferentes, você aprende 1. E troca de provedor com 1 linha.

```python
from litellm import completion
import os

# OpenAI
os.environ['OPENAI_API_KEY'] = '...'
resp = completion(model='gpt-4o-mini', messages=[{'role': 'user', 'content': 'Olá'}])

# Anthropic (1 linha de diferença)
os.environ['ANTHROPIC_API_KEY'] = '...'
resp = completion(model='claude-3-5-sonnet-20241022', messages=[{'role': 'user', 'content': 'Olá'}])

# AWS Bedrock
resp = completion(model='bedrock/anthropic.claude-3-5-sonnet', messages=[{'role': 'user', 'content': 'Olá'}])

# Google Vertex
resp = completion(model='vertex_ai/gemini-1.5-pro', messages=[{'role': 'user', 'content': 'Olá'}])

# Together (open-source)
resp = completion(model='together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo', messages=[{'role': 'user', 'content': 'Olá'}])

# Groq (inferência ultra-rápida)
resp = completion(model='groq/llama-3.1-70b-versatile', messages=[{'role': 'user', 'content': 'Olá'}])
```

LiteLLm normaliza responses, calcula custo automaticamente, suporta streaming, function calling, vision, e tem **proxy mode** onde você roda LiteLLM como servidor e todos os seus apps consomem do mesmo lugar.

**Casos de uso**:

1. **Fallback**: se OpenAI cai, LiteLLM tenta Anthropic automaticamente.
```python
resp = completion(
    model=['gpt-4o-mini', 'claude-3-5-sonnet'],
    messages=[...],
    fallbacks=[{'gpt-4o-mini': ['claude-3-5-sonnet']}]
)
```

2. **Load balancing**: distribui entre múltiplos modelos para custo/latência.
```python
resp = completion(
    model=['gpt-4o-mini', 'gpt-4o'],
    messages=[...],
    weights=[0.8, 0.2]  # 80% mini, 20% full
)
```

3. **Budget control**: impõe limite de gasto mensal.
```python
resp = completion(
    model='gpt-4o-mini',
    messages=[...],
    max_budget=10.0  # USD
)
```

Para o AcademIA, recomendo configurar LiteLLM como proxy central e todos os serviços consumirem dele. Isso facilita auditoria, rate limiting, e troca de provedor."

---

## 🎬 CENA 6: Docker — 10 minutos

**Visual:** Slide 06 com Dockerfile, terminal docker build.

**Sir. Nexus Alencar:**
"Docker é o empacotamento padrão. Vamos containerizar nossa API.

Dockerfile multi-stage para imagem pequena:

```dockerfile
# Stage 1: build dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:$PORT/health || exit 1

CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4 --proxy-headers
```

requirements.txt:
```
fastapi==0.115.0
uvicorn[standard]==0.32.0
litellm==1.55.0
redis==5.2.0
langfuse==3.0.0
pydantic==2.9.0
python-dotenv==1.0.1
```

Build e run:
```bash
docker build -t llm-gateway:v1.0 .
docker run -d --name llm-gateway -p 8000:8000 --env-file .env --restart unless-stopped llm-gateway:v1.0
```

**Boas práticas**:
- **Multi-stage build** reduz imagem de 1.2GB para 350MB
- **HEALTHCHECK** para Kubernetes/load balancer detectar pod unhealthy
- **--proxy-headers** para pegar IP real do cliente atrás de proxy
- **--restart unless-stopped** para auto-recovery em crashes
- **.dockerignore** exclui __pycache__, .git, .env, tests

docker-compose para dev local:
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - '8000:8000'
    env_file: .env
    depends_on:
      - redis
    restart: unless-stopped
  redis:
    image: redis:7.4-alpine
    ports:
      - '6379:6379'
    volumes:
      - redis_data:/data
    restart: unless-stopped
volumes:
  redis_data:
```

Para subir: `docker compose up -d`. Para ver logs: `docker compose logs -f api`. Para escalar: `docker compose up -d --scale api=3`."

---

## 🎬 CENA 7: Orquestração — 10 minutos

**Visual:** Slide 07 com três tiers de deploy.

**Sir. Nexus Alencar:**
"Três caminhos para deploy. A escolha depende de escala, orçamento, e tolerância a complexidade.

**Tier 1: VPS única** (R$ 80 a R$ 250/mês).
- Hetzner, Contabo, DigitalOcean, Vultr.
- Docker Compose. Zero Kubernetes. Zero DevOps.
- Para 100 a 1000 req/min. Suficiente para 80% dos casos.
- Configuração: 4 vCPU, 8GB RAM, 100GB SSD. R$ 120/mês.
- Deploy: `git pull && docker compose up -d --build`.

**Tier 2: Kubernetes gerenciado** (R$ 500 a R$ 2.000/mês).
- EKS (AWS), GKE (Google), DigitalOcean Kubernetes.
- Para 1000+ req/min, multi-região, ou requisitos de SLA rígidos.
- Configuração: 3 nodes (2 vCPU, 4GB cada). R$ 200/mês só de infra.
- Add Load Balancer, Auto-scaler, Cert Manager, Ingress. Mais R$ 200-500/mês.
- Deploy: `kubectl apply -f deployment.yaml`. Rolling update zero-downtime.
- Helm chart para facilitar.

**Tier 3: Serverless** (R$ 0 a R$ 200/mês).
- Fly.io, Railway, Render, Vercel Functions, AWS Lambda.
- Para protótipos, baixa escala, ou workloads intermitentes.
- Limitado a 5min timeout (Lambda) ou 30s (Vercel).
- Cold start de 2-5s na primeira request.

**Minha recomendação para começar**:
1. **Protótipo**: serverless (Fly.io). 5 minutos para deploy. $0-20/mês.
2. **MVP com usuários reais**: VPS única (Hetzner). 1 hora para configurar. $80-150/mês.
3. **Escala séria (10k+ usuários)**: Kubernetes. 1 semana para configurar. $500-2000/mês.

Não comece com Kubernetes. É tentador, mas é over-engineering para 90% dos casos. VPS única com Docker Compose escala muito mais do que as pessoas pensam — Reddit e Pinterest rodaram em servidores únicos por anos."

---

## 🎬 CENA 8: Observabilidade com Langfuse — 10 minutos

**Visual:** Slide 08 com código, dashboard Langfuse.

**Sir. Nexus Alencar:**
"Observabilidade é o que separa 'funciona na minha máquina' de 'funciona em produção'. Sem ela, você está voando cego. Com ela, você tem visão completa.

Langfuse é a plataforma open-source padrão. Captura traces, latência, custo, tokens, prompts, respostas, scores, e permite análise agregada. Self-hosted (Docker) ou Cloud (free tier generoso).

Integração já vimos no código da Cena 3. Mas o que fazer com os dados?

**Dashboard 1: Custo por dia**
```sql
SELECT date_trunc('day', created_at) as day,
       sum(cost_usd) as total_cost
FROM traces
WHERE created_at > now() - interval '30 days'
GROUP BY day
ORDER BY day;
```

**Dashboard 2: Latência p95 por modelo**
```sql
SELECT model,
       percentile_cont(0.95) WITHIN GROUP (ORDER BY latency_ms) as p95_latency
FROM traces
WHERE created_at > now() - interval '7 days'
GROUP BY model;
```

**Dashboard 3: Top 10 prompts mais caros**
```sql
SELECT prompt, sum(cost_usd) as total_cost, count(*) as call_count
FROM traces
WHERE created_at > now() - interval '30 days'
GROUP BY prompt
ORDER BY total_cost DESC
LIMIT 10;
```

**Dashboard 4: Taxa de erro por hora**
```sql
SELECT date_trunc('hour', created_at) as hour,
       count(*) FILTER (WHERE error IS NOT NULL)::float / count(*) as error_rate
FROM traces
WHERE created_at > now() - interval '24 hours'
GROUP BY hour
ORDER BY hour;
```

Langfuse também tem **scores** — você pode marcar traces como 'good'/'bad' manualmente ou via LLM-as-judge, e usar isso para treinar eval datasets.

Integração com LLM-as-judge para scoring automático:
```python
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

@observe()
def generate_and_score(prompt):
    response = completion(model='gpt-4o-mini', messages=[{'role': 'user', 'content': prompt}])
    
    # LLM judge
    judge_prompt = f'Avalie a resposta de 0-10 em qualidade. Pergunta: {prompt}\nResposta: {response.choices[0].message.content}'
    judge = completion(model='gpt-4o-mini', messages=[{'role': 'user', 'content': judge_prompt}], max_tokens=10)
    score = float(judge.choices[0].message.content.strip())
    
    langfuse_context.update_current_observation(score=score/10)
    return response
```

Com isso você tem **continuous evaluation** — toda resposta em produção é avaliada automaticamente. Quando a qualidade cai, você é alertado."

---

## 🎬 CENA 9: SLOs e Alertas — 10 minutos

**Visual:** Slide 09 com tabela de SLOs.

**Sir. Nexus Alencar:**
"Sem SLOs definidos, você não sabe quando está ruim. Sem alertas, você descobre quando o usuário reclama no Twitter. Vamos definir SLOs mínimos.

**Latência**:
- p50 < 1.5s (mediana)
- p95 < 3s (95% das requests)
- p99 < 8s (99% das requests)

**Throughput**:
- Mínimo 100 req/s sustentado
- Burst até 500 req/s

**Disponibilidade**:
- Uptime > 99.9% (43 minutos de downtime/mês)
- Para tier enterprise: 99.95% (22 minutos/mês)

**Error rate**:
- < 0.5% para 5xx (erros do servidor)
- < 2% para 4xx (erros do cliente são esperados, mas monitore)

**Custo**:
- < R$ 0,50 por 1000 requests
- Cache hit rate > 60%
- Custo mensal cresce < 20% ao mês sem crescimento de tráfego

**Como medir e alertar**:

Prometheus + Grafana é a stack clássica. Para LLM, Langfuse + Datadog ou Langfuse + Grafana Cloud.

Alertas essenciais no PagerDuty/Opsgenie:
1. **Error rate > 1%** por 5 minutos → alerta
2. **Latência p95 > 5s** por 10 minutos → alerta
3. **Uptime < 99.5%** em janela de 1h → crítico
4. **Custo diário > R$ 100** sem tráfego proporcional → alerta
5. **Cache hit rate < 40%** sustentado → investigar

Implementação com Langfuse + Datadog:
```python
from datadog import DogStatsd
statsd = DogStatsd(host='localhost', port=8125)

@statsd.timing('llm.latency')
@statsd.increment('llm.calls')
def generate(...):
    ...
```

Para o AcademIA, recomendo começar com Langfuse Cloud (free tier 50k traces/mês) + Datadog free tier (5 hosts) ou Grafana Cloud free tier. Quando passar de 1M traces/mês, avalie self-hosted Langfuse."

---

## 🎬 CENA 10: Custos Reais — 8 minutos

**Visual:** Slide 10 com breakdown de custos.

**Sir. Nexus Alencar:**
"Vamos aos números reais. Para um sistema atendendo 1 milhão de requests por mês (média 23 req/min, pico 200 req/min):

**Infraestrutura**:
- VPS única (Hetzner CX31, 4vCPU, 8GB): R$ 120/mês
- Redis gerenciado (Upstash, 10k comandos/dia): R$ 50/mês
- Domain + SSL: R$ 15/mês
- **Subtotal infra**: R$ 185/mês

**LLM API** (gpt-4o-mini, avg 1500 tokens output/req):
- 1M requests × 1500 tokens = 1.5B tokens output
- 1.5B × R$ 0,80/milhão = R$ 1.200/mês

**LLM API** (gpt-4o, mix 10% dos casos):
- 100k requests × 1500 tokens = 150M tokens
- 150M × R$ 25/milhão = R$ 3.750/mês

**Observabilidade**:
- Langfuse Cloud Pro (até 500k traces): R$ 0 (free)
- Datadog free tier: R$ 0 (free)
- **Subtotal**: R$ 0

**Total com gpt-4o-mini**: R$ 1.385/mês (R$ 1,39 por 1k requests)
**Total com mix 90% mini + 10% full**: R$ 5.135/mês (R$ 5,14 por 1k requests)

**Comparação**:
- Sistema RAG self-hosted: R$ 1.385/mês
- Solução enterprise (Azure OpenAI + Cosmos + Application Insights): R$ 8.000-15.000/mês
- Humano (1 atendente, 8h/dia, ~3k tickets/mês): R$ 4.500/mês + R$ 1.500 encargos = R$ 6.000/mês

**Otimizações para reduzir custo**:
1. **Cache agressivo** (hit rate 80%+): reduz LLM em 80%
2. **Modelos menores** (gpt-4o-mini, claude-haiku, llama-3.1-8b): 10x mais barato
3. **Prompt compression** (remove redundâncias): 20-40% menos tokens
4. **Batch processing** (processa múltiplos prompts em 1 chamada): 50% redução
5. **Self-hosted LLM** (Llama 3.1 70B em GPU A100): setup R$ 30k, mas R$ 0,50/hora de GPU ≈ R$ 0,0006/req

Para o AcademIA, recomendo começar com **gpt-4o-mini + cache agressivo + LiteLLM para fallback**. Quando passar de R$ 5k/mês, avalie self-hosted com vLLM + Llama 3.1 70B."

---

## 🎬 CENA 11: Encerramento (Ive + Alencar) — 6 minutos

**Visual:** Sala de controle, Ive e Alencar lado a lado.

**Sra. Nexus Ive:**
"Chegamos ao fim do módulo 05. Vocês viram como colocar IA em produção com SLA, observabilidade, e custo controlado. Mas tem um detalhe que une tudo: segurança. O que adianta um sistema rápido, escalável, e barato se ele vaza dados, é jailbroken por adolescentes, ou viola LGPD? É exatamente sobre isso o módulo 06. Segurança, jailbreaks, e compliance. Nos vemos lá."

**Sir. Nexus Alencar:**
"Resumo prático: comece com VPS única + FastAPI + Redis. Adicione LiteLLM para flexibilidade. Adicione Langfuse para observabilidade. Defina SLOs desde o dia 1. Meça tudo. E quando o sistema cair — sim, vai cair — tenha runbook e alertas. Nos vemos no módulo 06."

**Visual:** Tela final com logos + slide 'Módulo 06 · Segurança, Jailbreaks e LGPD'.

---

## 📚 Recursos Mencionados

- FastAPI: https://fastapi.tiangolo.com
- LiteLLM: https://litellm.ai
- Langfuse: https://langfuse.com
- Redis Stack: https://redis.io/docs/about/about-stack/
- Docker: https://docs.docker.com
- Hetzner: https://hetzner.com/cloud
- Fly.io: https://fly.io
- Datadog: https://datadoghq.com
- Grafana Cloud: https://grafana.com/products/cloud/

## 🔗 Documentos Complementares

- `tutoriais/21-deploy-api-ia-producao.md` — Tutorial prático
- `cursos/master/05-deploy-em-producao.md` — Material escrito
- `producao/INCIDENT-RESPONSE-RUNBOOK.md` — Runbook de incidentes
- `producao/GO-LIVE-CHECKLIST.md` — Checklist pré-deploy

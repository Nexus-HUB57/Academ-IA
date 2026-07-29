---
title: "Módulo Master-04 · Roteiro · RAG em Produção"
description: "[MAVIS-EXTENDIDO 12 cenas detalhadas] — Versão estendida. Padrão principal do remote (genspark_dev): 04-rag-em-producao-roteiro.md — Roteiro completo de narração para vídeo-aula do módulo 04"
tags: [roteiro, master, modulo-04, rag, llm, embeddings, video-aula]
modulo: master-04
trilha: Master
duracao_estimada: "120 minutos"
total_cenas: 12
personas: [Alencar]
voice: personas/alencar/audio/official_voice.wav
---

> ⚠️ **VERSÃO ESTENDIDA MAVIS** (12 cenas, 60+ páginas) — complementar ao roteiro oficial do módulo em `04-rag-em-producao-roteiro.md` (5 cenas). Mantido para uso em videoaulas longas, workshops, e sessões de mentoria 1:1.

# 🎬 Roteiro · Master 04 · RAG em Produção

**Persona principal:** Sir. Nexus Alencar (mentor técnico, voz didática)
**Persona secundária:** Sra. Nexus Ive (introdução/encerramento estratégico)
**Duração total estimada:** 120 minutos
**Dificuldade:** Master
**Pré-requisito:** Tutoriais #16 e #17

---

## 🎬 CENA 1: Abertura (Ive) — 4 minutos

**Visual:** Sala de controle com dashboards de IA ao fundo, Sra. Ive em pé com tablet.

**Sra. Nexus Ive (voz envolvente, sotaque sulista sutil):**
"Olá, mestres. O módulo 04 é o mais pedido do segundo semestre de 2026. RAG — Retrieval-Augmented Generation — saiu do hype acadêmico e virou padrão de mercado. Mais de 90% das empresas que implementam IA corporativa começam com RAG. Por quê? Porque resolve três problemas que o fine-tuning não resolve: custo, atualização em tempo real, e auditabilidade. Hoje, com o Sir Alencar, vocês vão aprender a construir um pipeline RAG que escala — do protótipo com 50 documentos ao sistema com 5 milhões de vetores atendendo 1000 requisições por segundo. Uma jornada completa. Fique comigo e com o Alencar pelos próximos 120 minutos. Vamos."

**Visual:** Transição para Sir Alencar em pé diante de tela com diagrama de pipeline.

---

## 🎬 CENA 2: Por que RAG Venceu — 8 minutos

**Visual:** Slide 02 com gráfico de barras comparando RAG vs Fine-tuning vs Prompting.

**Sir. Nexus Alencar (voz didática, pausada):**
"Vamos começar com uma pergunta provocativa: por que RAG venceu? Em 2023, todo mundo falava em fine-tuning. Em 2024, a maioria migrou para RAG. Em 2026, RAG é onipresente. Os motivos são cinco, e vou detalhar cada um.

Primeiro: **custo**. Fine-tuning um modelo de 7B parâmetros custa entre R$ 30 mil e R$ 100 mil para o primeiro treinamento, mais R$ 5 mil a R$ 15 mil por mês em infraestrutura. RAG, com um LLM hospedado, custa entre R$ 1.500 e R$ 8 mil por mês para 1 milhão de consultas. Uma diferença de 10 a 50 vezes.

Segundo: **atualização em tempo real**. Com fine-tuning, quando uma informação muda, você precisa retreinar o modelo. Horas ou dias. Com RAG, basta atualizar o documento no vector store. Segundos.

Terceiro: **auditabilidade**. Com RAG, você pode mostrar exatamente qual documento o sistema usou para gerar a resposta. Com fine-tuning, o conhecimento está distribuído em bilhões de parâmetros e é impossível de rastrear.

Quarto: **compliance**. LGPD, EU AI Act, e HIPAA exigem rastreabilidade. RAG é compliance-by-default. Fine-tuning precisa de Workarounds.

Quinto: **conhecimento proprietário**. Você não quer treinar um modelo com seus segredos industriais. RAG mantém os dados no seu vector store, sem treinar nada.

Conclusão prática: se você precisa de IA que responde perguntas sobre documentos, regulamentações, manuais, FAQs, base de conhecimento, ou dados proprietários — RAG é a resposta. Fine-tuning só vale a pena quando você precisa de um **comportamento** ou **estilo** específico que prompting não consegue entregar."

---

## 🎬 CENA 3: Anatomia RAG — 10 minutos

**Visual:** Slide 03 com diagrama de fluxo animado (documentos → chunking → embeddings → vector DB → retrieval → LLM → resposta).

**Sir. Nexus Alencar:**
"Vamos dissecar a anatomia de um pipeline RAG. São cinco etapas. Cada uma tem decisões técnicas importantes.

**Etapa 1: Ingestão de documentos.** Você começa com PDFs, DOCX, HTML, Markdown, JSON, Notion, Confluence, Slack, e-mail, etc. Use loaders especializados: PyPDF para PDF, python-docx para Word, BeautifulSoup para HTML. Para casos complexos — PDFs com tabelas e imagens — use Unstructured.io ou LlamaParse.

**Etapa 2: Chunking.** Esta é a etapa subestimada. Chunks muito pequenos — 200 tokens — geram respostas com pouca coerência. Chunks muito grandes — 2000 tokens — diluem o contexto e custam caro. O sweet spot é 400 a 600 tokens, com overlap de 80 a 100 tokens. Use RecursiveCharacterTextSplitter com separadores hierárquicos: parágrafo, linha, frase, palavra.

**Etapa 3: Embeddings.** O chunk vira um vetor de 1024 a 3072 dimensões, dependendo do modelo. text-embedding-3-small da OpenAI gera vetores de 1536 dimensões, com custo de R$ 0,10 por milhão de tokens. Open-source, temos o bge-m3, e5-mistral-7b, e nomic-embed-text-v1.5.

**Etapa 4: Vector store.** Persiste os vetores com metadata. Chroma para protótipos. Pinecone, Weaviate, ou Qdrant para produção. pgvector se você já usa Postgres. LanceDB para workloads serverless modernos.

**Etapa 5: Retrieval + LLM.** Dada a pergunta do usuário, você converte ela em embedding, busca os top-K mais similares no vector store, monta um prompt com os chunks recuperados, e envia para o LLM gerar a resposta.

A beleza do RAG é que essas cinco etapas são **independentes** e **substituíveis**. Você pode começar com Chroma e migrar para Pinecone sem mudar o resto. Pode trocar OpenAI por Claude, ou Llama 3.1 70B local. Pode mudar a estratégia de chunking sem refazer tudo."

---

## 🎬 CENA 4: Chunking Profundo — 10 minutos

**Visual:** Slide 04 com exemplos visuais de chunks, código Python em destaque.

**Sir. Nexus Alencar (didático, com exemplos práticos):**
"Vamos aprofundar em chunking porque é onde 60% dos erros de RAG acontecem. Três decisões críticas.

Primeira decisão: **tamanho do chunk**. Para documentos técnicos — manuais, papers, documentação de API — 400 a 600 tokens é ideal. Para literatura, narrativas, e transcrições de reunião, 800 a 1200 tokens funciona melhor. Para FAQs curtas, 200 a 300 tokens.

Segunda decisão: **overlap**. Sem overlap, você perde contexto nas bordas. Com overlap de 10% a 20% do tamanho do chunk — 50 a 100 tokens para chunks de 500 — você preserva a continuidade sem inflar o custo.

Terceira decisão: **separadores hierárquicos**. O RecursiveCharacterTextSplitter tenta quebrar primeiro por parágrafo, depois por linha, depois por frase, depois por palavra. Isso preserva a estrutura semântica melhor do que chunking por token fixo.

Para PDFs complexos, use **Parent Document Retriever**: armazene chunks pequenos para retrieval, mas retorne o documento pai (chunk maior) para o LLM. Isso dá precisão fina no retrieval sem perder contexto.

Para Markdown, use **MarkdownTextSplitter** que respeita headers, listas, e code blocks. Para código, use **CodeTextSplitter** com sintaxe específica por linguagem.

Erros comuns: chunkar por token fixo sem semântica, usar overlap zero, não incluir metadata (nome do arquivo, data, seção), e não testar com perguntas reais."

---

## 🎬 CENA 5: Embeddings — 10 minutos

**Visual:** Slide 05 com tabela comparativa de modelos de embedding.

**Sir. Nexus Alencar:**
"Embeddings são o coração do RAG. O modelo errado derruba toda a qualidade. Vamos comparar os principais de 2026.

**OpenAI text-embedding-3-small**: 1536 dimensões, R$ 0,10 por milhão de tokens, qualidade alta, suporta português. Bom custo-benefício.

**OpenAI text-embedding-3-large**: 3072 dimensões, R$ 0,65 por milhão de tokens, qualidade superior. Para casos críticos.

**Voyage-3**: 1024 dimensões, R$ 0,30 por milhão de tokens, qualidade altíssima, otimizado para retrieval. Minha recomendação pessoal para produção.

**BGE-M3** (open-source): 1024 dimensões, gratuito, multilingue, suporta 100+ idiomas. Roda em CPU. Perfeito para começar sem custo.

**Nomic Embed Text v1.5** (open-source): 768 dimensões, gratuito, contexto de 8192 tokens. Bom para documentos longos.

**E5-Mistral-7B** (open-source): 4096 dimensões, gratuito, mas precisa de GPU A100. Qualidade estado-da-arte.

Para escolher: comece com text-embedding-3-small. Se precisar de mais qualidade, vá para Voyage-3 ou E5-Mistral. Para protótipos com orçamento zero, BGE-M3.

Importante: embeddings têm **custo de dimensionalidade**. Vetor de 3072 dimensões ocupa 6x mais espaço em disco e 6x mais memória RAM que vetor de 512. Para 10 milhões de documentos, isso é a diferença entre 30 GB e 180 GB."

---

## 🎬 CENA 6: Vector Stores — 10 minutos

**Visual:** Slide 06 com tabela de bancos de dados vetoriais.

**Sir. Nexus Alencar:**
"Vector store é onde seus embeddings vivem. A escolha depende de escala, latência, e orçamento.

**Chroma**: embedded, roda em processo Python, sem servidor separado. Perfeito para protótipos, testes, e aplicações pequenas até 100 mil vetores. Zero configuração.

**Pinecone**: managed, serverless ou pods dedicados. Latência consistente, escala horizontal, backup automático. Custo: R$ 400 a R$ 4.000 por mês dependendo do tamanho. Para produção séria, minha primeira opção.

**Weaviate**: open-source, self-hosted, com módulos de busca híbrida nativos (BM25 + embeddings). Para quem quer controle total e não quer pagar Pinecone.

**Qdrant**: escrito em Rust, performance absurda, latência sub-10ms. Open-source com opção managed. Excelente para quem precisa de velocidade.

**pgvector**: extensão do PostgreSQL. Se você já tem Postgres, é a forma mais natural de adicionar busca vetorial sem nova infra. Limitado em escala comparado aos especializados, mas suficiente para 90% dos casos até 10 milhões de vetores.

**LanceDB**: serverless, baseado em Apache Arrow, integração nativa com pandas e DuckDB. Moderno, performante, open-source. Para workloads analíticos e data lakes.

Minha recomendação: comece com Chroma no protótipo. Quando passar de 100 mil vetores ou precisar de SLA, migre para Pinecone ou Qdrant. Se já tem Postgres, tente pgvector primeiro — vai surpreender."

---

## 🎬 CENA 7: Retrieval Híbrido — 12 minutos

**Visual:** Slide 07 com gráfico de barras comparando pure embeddings vs hybrid vs hybrid+rerank.

**Sir. Nexus Alencar (ênfase):**
"Aqui está o insight mais importante do módulo 04. Se você lembrar de uma única coisa, lembre desta: **retrieval híbrido + reranking é o estado da arte de 2026**. Não embeddings puros. Não BM25 puro. A combinação.

Por quê? Embeddings puros são bons em **similaridade semântica**, mas ruins em **palavras-chave exatas**. BM25 é bom em palavras-chave, mas não entende sinônimos. Quando você combina os dois com pesos ajustáveis — geralmente 0.3 BM25, 0.7 embeddings — você captura o melhor dos dois mundos.

Exemplo prático: usuário pergunta 'qual o limite de saque do PIX?'. Embeddings podem trazer documentos sobre 'limite de transferência', 'valores máximos', 'TED vs PIX'. BM25 traz o documento exato que menciona 'limite de saque do PIX'. Hybrid traz ambos, e o reranker escolhe o melhor.

**Implementação com Weaviate** (a mais elegante):
```python
results = client.query.get('Document', ['content', 'source']) \\
  .with_hybrid(query='limite de saque PIX', alpha=0.7) \\
  .with_limit(20) \\
  .do()
```

**Implementação genérica com LangChain**:
```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever
bm25 = BM25Retriever.from_documents(docs, k=20)
vector = vectorstore.as_retriever(search_kwargs={'k': 20})
ensemble = EnsembleRetriever(retrievers=[bm25, vector], weights=[0.3, 0.7])
```

O alpha em Weaviate (0 a 1) controla o peso: 0 é puro BM25, 1 é puro embeddings, 0.7 é o sweet spot.

Após o retrieval híbrido, você passa os top-20 ou top-50 candidatos para um **cross-encoder reranker**, que refina para top-5. O reranker é um modelo que processa query e documento juntos, não apenas embeddings separados. É mais lento, mas muito mais preciso. BGE-reranker-v2-m3 é o padrão de mercado, open-source, e roda em CPU.

Resultado: nDCG@10 de 0.72 com embeddings puros para 0.91 com hybrid+rerank. Um salto de 27% em qualidade de retrieval."

---

## 🎬 CENA 8: Reranking Cross-Encoder — 8 minutos

**Visual:** Slide 08 com diagrama mostrando 50 candidatos → cross-encoder → top 5.

**Sir. Nexus Alencar:**
"Reranking é a cereja do bolo. Vamos detalhar.

O retrieval híbrido retorna 20-50 candidatos. Mas nem todos são realmente relevantes — alguns são só superficialmente similares. O cross-encoder reranker pega esses 20-50, processa cada par (query, documento) com um transformer completo, e retorna uma pontuação de relevância de 0 a 1. Você ordena por essa pontuação e pega os top-5.

Modelos recomendados:

**BGE-reranker-v2-m3** (BAAI): open-source, multilingue, roda em CPU, latência ~50ms por par. Suporta 100+ idiomas. Estado da arte open-source.

**Cohere Rerank 3.5**: API gerenciada, R$ 1,00 por 1000 buscas, latência ~100ms, qualidade ligeiramente superior ao BGE. Para quem prefere não se preocupar com infra.

**Jina Rerank**: open-source e API, boa qualidade, suporte a contexto longo.

**FlashRank**: otimizado para latência sub-10ms. Para casos real-time.

Implementação com sentence-transformers:
```python
from sentence_transformers import CrossEncoder
model = CrossEncoder('BAAI/bge-reranker-v2-m3')
pairs = [[query, doc.page_content] for doc in candidates]
scores = model.predict(pairs)
reranked = [c for _, c in sorted(zip(scores, candidates), reverse=True)][:5]
```

Atenção: reranking **adiciona latência**. Em 20 candidatos, são ~1 segundo. Em 50 candidatos, ~2,5 segundos. Para real-time, limite a 20 e use FlashRank. Para batch, pode ir a 50 ou 100.

Custo computacional: cross-encoder é caro. Cada par query-documento passa por um transformer de 568M parâmetros. Em CPU, ~50ms. Em GPU A10, ~5ms. Em produção, rode em GPU dedicada para reranking ou use a API gerenciada da Cohere."

---

## 🎬 CENA 9: Geração com LLM — 10 minutos

**Visual:** Slide 09 com prompt template destacado, código Python.

**Sir. Nexus Alencar:**
"Finalmente chegamos à geração. Com o top-5 documentos rerankeados em mãos, montamos o prompt para o LLM.

A chave é **instrução explícita de grounding**. Diga ao modelo: 'Use APENAS o contexto abaixo. Se a resposta não estiver no contexto, diga "não encontrei informação sobre isso"'. Isso reduz alucinação drasticamente.

Template recomendado:
```
Você é um assistente técnico especializado. Use APENAS o contexto abaixo para responder.
Se a informação não estiver no contexto, responda: 'Não encontrei informação sobre isso nos documentos disponíveis.'

# Contexto
{context}

# Pergunta
{question}

# Resposta
```

Onde `{context}` é a concatenação dos top-5 chunks com metadata:
```python
context = '\n\n---\n\n'.join([
  f'[{doc.metadata["source"]}, p.{doc.metadata["page"]}]\n{doc.page_content}'
  for doc in reranked_docs
])
```

Modelos LLM recomendados para geração RAG em 2026:

**GPT-4o**: melhor qualidade geral, R$ 25 por milhão de tokens output. Para casos críticos.

**Claude 3.5 Sonnet**: excelente para textos longos, raciocínio, e nuances. R$ 22 por milhão de tokens output.

**Llama 3.1 70B** (self-hosted): qualidade GPT-4 a 1/10 do custo se você tem GPU. Para quem tem infra.

**GPT-4o mini**: 80% da qualidade do GPT-4o a 1/30 do custo. R$ 0,80 por milhão output. Para a maioria dos casos.

**Claude 3 Haiku**: similar ao GPT-4o mini, R$ 1,60 por milhão. Alternativa.

Para começar, **GPT-4o mini é a melhor escolha** — custo baixo, qualidade alta, latência baixa. Migre para GPT-4o apenas se a avaliação RAGAS mostrar que precisa.

Importante: sempre passe **metadata** no contexto — nome do arquivo, página, data. O LLM pode citar isso nas respostas, aumentando a confiança do usuário.

Resposta ideal: 'Segundo o manual de procedimentos (p. 47), o limite de saque PIX é R$ 5.000 por operação para contas pessoa física...' — note a citação da fonte."

---

## 🎬 CENA 10: Avaliação com RAGAS — 12 minutos

**Visual:** Slide 10 com métricas RAGAS, código Python, exemplos de scores.

**Sir. Nexus Alencar:**
"Como saber se seu RAG está bom? Não confie em 'parece bom'. Meça. A biblioteca padrão é **RAGAS** (Retrieval-Augmented Generation Assessment).

Quatro métricas principais:

**Faithfulness** (Fidelidade): o LLM inventou algo que não está no contexto? Deve ser > 0.95. Se estiver abaixo, seu LLM está alucinando.

**Context Recall** (Revocação do contexto): o contexto recuperado tem toda a informação necessária? Mede o retrieval. Deve ser > 0.85.

**Context Precision** (Precisão do contexto): dos documentos recuperados, quantos são realmente relevantes? Deve ser > 0.80.

**Answer Relevancy** (Relevância da resposta): a resposta é relevante para a pergunta? Deve ser > 0.80.

Implementação:
```python
from ragas import evaluate
from ragas.metrics import faithfulness, context_recall, context_precision, answer_relevancy

result = evaluate(
  dataset,
  metrics=[faithfulness, context_recall, context_precision, answer_relevancy]
)
print(result)
```

Para criar o dataset de avaliação, você precisa de **ground truth**: 50 a 100 perguntas reais com respostas esperadas. Não invente perguntas — use logs de produção, tickets de suporte, ou faça com usuários reais.

Workflow recomendado: rode RAGAS com dataset de 50 perguntas, identifique os piores casos (faithfulness < 0.8), investigue por que falhou, ajuste o pipeline, rode de novo. Repita até atingir os targets.

Benchmarks reais de sistemas RAG em produção em 2026:
- **Bom**: Faithfulness 0.90, Context Recall 0.80, Precision 0.75, Answer Relevancy 0.75
- **Ótimo**: Faithfulness 0.95, Context Recall 0.90, Precision 0.85, Answer Relevancy 0.85
- **Estado da arte**: Faithfulness 0.98, Context Recall 0.95, Precision 0.92, Answer Relevancy 0.92

Se você está abaixo do 'Bom', revise chunking e embeddings. Se está abaixo do 'Ótimo', adicione hybrid retrieval + reranking. Se está abaixo do 'Estado da arte', considere fine-tuning do embedding ou LLM judge."

---

## 🎬 CENA 11: Custos e Comparação — 10 minutos

**Visual:** Slide 11 com breakdown de custos mensais.

**Sir. Nexus Alencar:**
"Vamos falar de dinheiro. Para um sistema RAG atendendo 1 milhão de consultas por mês:

**Embeddings** (indexação inicial de 10 milhões de tokens):
- text-embedding-3-small: R$ 500 (one-time)
- Re-indexação mensal (atualização): R$ 50

**Vector store** (10 milhões de vetores de 1536 dim):
- Pinecone p1: R$ 350/mês
- Qdrant self-hosted: R$ 200/mês (infra)
- pgvector: R$ 100/mês (já tem Postgres)

**LLM** (1M queries, avg 2k tokens output):
- GPT-4o mini: R$ 800/mês
- GPT-4o: R$ 25.000/mês
- Claude 3.5 Sonnet: R$ 22.000/mês
- Llama 3.1 70B self-hosted: R$ 1.500/mês (GPU A100)

**Reranking** (1M queries, top 20 cada):
- BGE local: R$ 100/mês (CPU) ou R$ 50/mês (GPU)
- Cohere Rerank API: R$ 5.000/mês

**Total com GPT-4o mini + Pinecone + Cohere**: R$ 6.250/mês
**Total com GPT-4o mini + Qdrant + BGE local**: R$ 1.500/mês
**Total com Llama 70B + Qdrant + BGE local**: R$ 2.000/mês

Comparação:
- **RAG** (R$ 1.500 a R$ 6.250/mês): 1M consultas, atualiza em tempo real
- **Fine-tuning** (R$ 30k setup + R$ 5k/mês): mais lento, mais caro, desatualiza
- **Humano** (R$ 50k/mês): 1 atendente, 8h/dia, ~3k tickets

RAG é 8x a 33x mais barato que atendente humano, e atualiza em tempo real. O ROI é absurdo quando implementado direito."

---

## 🎬 CENA 12: Encerramento (Ive + Alencar) — 6 minutos

**Visual:** Sala de controle, Ive e Alencar lado a lado, holofotes suaves.

**Sra. Nexus Ive (encerramento estratégico):**
"Chegamos ao fim do módulo 04. RAG deixou de ser tendência e se tornou infraestrutura. Quem domina RAG em 2026 domina a entrega de IA em produção. Mas atenção: RAG é só 50% do trabalho. Os outros 50% são deploy, segurança, e monitoramento. É exatamente isso que vem nos próximos módulos. O Alencar vai falar de deploy no módulo 05. E no módulo 06, a gente fecha o ciclo com segurança e LGPD. Até lá."

**Sir. Nexus Alencar (fechamento técnico):**
"Resumo prático: comece com Chroma + text-embedding-3-small + GPT-4o mini. Adicione hybrid retrieval com BM25+embeddings. Adicione reranking com BGE. Meça com RAGAS. Quando precisar de escala, migre para Pinecone ou Qdrant. Quando precisar de qualidade máxima, migre para GPT-4o ou Claude 3.5. Esse é o caminho. Nos vemos no módulo 05."

**Visual:** Tela com logos Nexus + slide 'Módulo 05 · Deploy de IA em Produção · Disponível em /cursos/master/05-deploy-em-producao.md'.

---

## 📚 Recursos Mencionados

- **RAGAS**: https://docs.ragas.io
- **LangChain**: https://python.langchain.com
- **BGE-reranker**: https://huggingface.co/BAAI/bge-reranker-v2-m3
- **Pinecone**: https://pinecone.io
- **Qdrant**: https://qdrant.tech
- **Weaviate**: https://weaviate.io
- **Voyage AI**: https://voyageai.com
- **OpenAI Embeddings**: https://platform.openai.com/docs/guides/embeddings

---

## 🔗 Documentos Complementares

- `tutoriais/16-pipeline-rag-end-to-end.md` — Tutorial prático RAG
- `tutoriais/17-rag-hybrid-search-bm25.md` — Hybrid search profundo
- `cursos/master/04-rag-em-producao.md` — Material escrito completo
- `cursos/master/04-rag-em-producao-slides.md` — Slides visuais
- `cursos/master/05-deploy-em-producao.md` — Próximo módulo

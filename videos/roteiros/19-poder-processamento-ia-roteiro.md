---
title: "Vídeo 19 — Poder de Processamento IA"
type: "roteiro"
duracao_estimada: "120-150s"
formato: "Engenharia de hardware + termodinâmica + manifesto"
trilha: "Elite · NEXUS AFFIL'IA'TE TECH"
ordem: 19
pattern: "MMN_IA"
ebook_origem: "NEXUS_AFFIL_IA_TECH_VOL_05"
---

# 🎬 Roteiro — Vídeo 19: Poder de Processamento IA

> **Tipo:** Vídeo de engenharia de infraestrutura (PhD-level teaser)
> **Duração:** 2-2,5 minutos
> **Formato:** Abertura dupla + anatomia de hardware + custo oculto + CTA
> **Tom:** Engenharia pura, com termodinâmica e decisão de produto
> **Público:** Engenheiros de ML, arquitetos de infra, SREs, fundadores
> **Origem:** Coletânea NEXUS AFFIL'IA'TE TECH · Volume V

---

## 🎞️ CENA 1 — Abertura (0:00-0:13)

**[Visual: Dupla Ive + Alencar. Processador glowing ao fundo. Atmosfera de "decisão de infraestrutura como produto".]**

**[Ive, estratégica:]**
> *"Compreenda… a infraestrutura não é o custo do produto. É o produto. Em SaaS IA, o que se vende é, em última instância, a capacidade de transformar tokens em valor. E essa capacidade é inteiramente função do hardware, do modelo e da arquitetura que o servem."*

**[Alencar, técnico:]**
> *"Hoje, vamos dissecar a anatomia de GPU, TPU e NPU, e o custo oculto — em energia, água e carbono — de cada token gerado."*

---

## 🎞️ CENA 2 — Anatomia: GPU, TPU, NPU (0:13-0:35)

**[Visual: Três chips lado a lado, brilhando. GPU: milhares de cores generalistas. TPU: systolic array do Google. NPU: on-device AI, baixa potência. Cada um com perfil de uso distinto.]**

**[Alencar, didático-técnico:]**
> *"Três arquiteturas canônicas. GPU: NVIDIA domina, paralelismo massivo via CUDA e Tensor cores, HBM 192GB, NVLink 1,8 TB/s. TPU: systolic array do Google, otimizado para matmul, latência determinística, eficiente em workload puro de matmul. NPU: on-device, baixo TDP, modelo pequeno, latência ultrabaixa."*

> *"Em 2026, há uma quarta voz: ASICs customizados. Trainium, MAIA, Groq LPU, Cerebras WSE, SambaNova RDU. A mensagem: hardware é otimizado para workload, não para fornecedor."*

---

## 🎞️ CENA 3 — O gargalo real: memória (0:35-0:55)

**[Visual: Pirâmide de hierarquia de memória. Registers → L1/L2 → HBM → DRAM → NVMe. KV cache glowing como um slab paralelo. Bandwidth destacada como gargalo.]**

**[Alencar:]**
> *"A escassez de memória é, em 2026, o gargalo dominante da inferência de LLMs. Não FLOPS — memória. E não memória total — bandwidth. A velocidade com que dados trafegam entre memória e computação."*

> *"Em decode de transformer 70B, cada token precisa acessar 140 GB de pesos. Em HBM com 5 TB/s, isso dá 28 ms por token. É a parede que define latência de decode. As técnicas canônicas: quantização, PagedAttention, Flash Attention, speculative decoding. Cada uma com trade-off de qualidade."*

---

## 🎞️ CENA 4 — O custo escondido (0:55-1:15)

**[Visual: Contador glowing de tokens. Ao redor, três medidores — energia em joules, água em litros, carbono em kg CO₂. Atmosfera de "realidade ambiental".]**

**[Ive, com peso:]**
> *"Cada token carrega custo energético, hídrico e de carbono. 1M tokens ≈ 500-2000 kWh. 10M tokens/dia = 5-20 MWh/dia — equivalente a 150-600 residências por dia."*

> *"Água: 1 kWh de computação ≈ 1-3 litros. Em região com estresse hídrico, isso vira restrição regulatória. E carbono: a diferença entre região com matriz limpa e fóssil é 1000×."*

**[Alencar:]**
> *"Em 2026, esses custos passam de preocupação ambiental para restrição regulatória e vetor de procurement. SaaS IA maduro reporta periodicamente a pegada por tenant, por região, por modelo. Transparência ambiental vira parte do transparency report."*

---

## 🎞️ CENA 5 — Decisão de provisionamento (1:15-1:35)

**[Visual: Quatro modelos lado a lado. On-demand, Reserved, Spot, Self-host. Tabela de trade-offs — custo, compromisso, risco operacional, caso de uso.]**

**[Alencar:]**
> *"Quatro modelos. On-demand: pico de preço, sem compromisso. Reserved: 30-60% de desconto, 1-3 anos. Spot: 60-80% de desconto, mas preemptado. Self-host: custo fixo alto, custo variável baixo, ideal para enterprise."*

> *"A maioria opera híbrido. Reserved como base, on-demand para pico, spot para batch, self-host em região-chave para latência. Provisionamento é modelagem de carga, não escolha de fornecedor."*

---

## 🎞️ CENA 6 — CTA (1:35-1:50)

**[Visual: Número romano "V" + nome do ebook. Capa NEXUS AFFIL'IA'TE TECH Vol. V. Atmosfera de "engenharia que decide o futuro".]**

**[Ive, fechando:]**
> *"O Volume V da NEXUS AFFIL'IA'TE TECH fecha a coletânea com 10 capítulos, 10 manifestos, e a termodinâmica que sustenta cada decisão de produto. Da engenharia dos sistemas à termodinâmica dos tokens."*

**[Alencar, decisivo:]**
> *"Disponível agora em `oneverso.com.br/academia/colecoes/tech`. Acesse, leia, e tome a decisão de infraestrutura que seu SaaS IA exige."*

---

## 🎯 Métricas de produção

- **Duração total estimada:** 120-150 segundos
- **Personas:** Ive (estratégia + custo ambiental + CTA) · Alencar (hardware + memória + provisionamento + CTA)
- **Tom híbrido:** engenharia + termodinâmica + decisão de produto
- **CTA:** ebook completo + decisão de infra
- **Thumbnail:** `../thumbnails/thumb-19-poder-processamento-ia.webp` (2K, 16:9)

---

*Roteiro âncora · Onda 40 · v1.4.0 · NEXUS AFFIL'IA'TE TECH Vol. V*
*MMN AI-to-AI · Nexus HUB57 · Ecossistema MMN AI-to-AI*

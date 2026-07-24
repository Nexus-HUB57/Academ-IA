---
title: "Vídeo 18 — Fundamento SaaS IA"
type: "roteiro"
duracao_estimada: "120-150s"
formato: "Negócio-técnico + arquitetura em camadas + manifesto"
trilha: "Elite · NEXUS AFFIL'IA'TE TECH"
ordem: 18
pattern: "MMN_IA"
ebook_origem: "NEXUS_AFFIL_IA_TECH_VOL_04"
---

# 🎬 Roteiro — Vídeo 18: Fundamento SaaS IA

> **Tipo:** Vídeo de arquitetura de produto (PhD-level teaser)
> **Duração:** 2-2,5 minutos
> **Formato:** Abertura dupla + pilha em 7 camadas + unit economics + CTA
> **Tom:** Pragmático, executivo-técnico, com peso de quem constrói
> **Público:** Fundadores, CTOs, arquitetos de SaaS, operadores de plataforma
> **Origem:** Coletânea NEXUS AFFIL'IA'TE TECH · Volume IV

---

## 🎞️ CENA 1 — Abertura (0:00-0:13)

**[Visual: Dupla Ive + Alencar. Pilha SaaS flutuando ao fundo em camadas gold/cyan. Atmosfera de "arquitetura executiva".]**

**[Ive, estratégica:]**
> *"Veja bem… construir um SaaS de IA não é construir um SaaS tradicional com LLM adicionado. É um produto novo — com economia nova, engenharia nova, observabilidade nova. Tratar como SaaS tradicional é o caminho mais rápido para quebrar."*

**[Alencar, pragmático:]**
> *"Hoje, vamos dissecar a pilha canônica em sete camadas e o unit economics que define se o produto sobrevive."*

---

## 🎞️ CENA 2 — A pilha em 7 camadas (0:13-0:35)

**[Visual: Pilha vertical glowing. De baixo para cima: Infraestrutura → Modelo → Agent Runtime → Orquestração → Tools → Aplicação → UX do Tenant. Cada camada com decisões, custos e contratos próprios.]**

**[Alencar, didático:]**
> *"Sete camadas distintas. Cada uma com owners, contratos e custos. Camada 1: infraestrutura — GPUs, TPUs, NPUs, rede, storage. Camada 2: modelo — self-hosted vs API, foundation vs ajustado, versionamento triplo. Camada 3: agent runtime — LangGraph, AutoGen, Temporal. Camada 4: orquestração — topologias e máquinas de estado."*

> *"Camada 5: tools via MCP. Camada 6: aplicação. Camada 7: UX do tenant. A regra: cada camada fala com a adjacente via contrato explícito."*

---

## 🎞️ CENA 3 — Multi-tenancy e unit economics (0:35-0:55)

**[Visual: Diagrama de multi-tenancy com pool compartilhado de modelos + namespace isolado por tenant. Tabela de unit economics flutuando: Starter vs Pro vs Scale vs Enterprise, com margem bruta variando 10×.]**

**[Ive:]**
> *"Multi-tenancy em SaaS IA é arte. O modelo 3 — pool compartilhado de modelo, mas namespace isolado por tenant — é o padrão emergente em 2026. Eficiência de pool, previsibilidade de instância."*

> *"O custo por tenant varia 10× ou mais. Starter custa US$ 0,10 em inferência. Enterprise custa US$ 8.000. A média mascara. P&L por tenant é a única verdade."*

**[Alencar:]**
> *"Pricing híbrido é o padrão. Assinatura para previsibilidade. Overage para alinhamento a custo. Outcome para enterprise. As cinco alavancas de margem: cache de prompt, roteamento de modelo, contexto enxuto, output estruturado, batching. Margem bruta saudável de SaaS IA fica em 55-70%."*

---

## 🎞️ CENA 4 — SLA estatístico (0:55-1:15)

**[Visual: Painel de SLA. Disponibilidade 99,5%. Latência p95 ≤ 8s. Taxa de alucinação ≤ 1%. Taxa de fallback ≤ 5%. Error budget com barra de consumo.]**

**[Alencar, técnico:]**
> *"SLA de SaaS IA não é 99,99% de uptime. É uptime mais latência p95 mais alucinação mais fallback. Todos medidos, alertados, reportados."*

> *"A regra dos 4 nines vs IA: aceita-se mais indisponibilidade em troca de mais qualidade. Usuário tolera 30s de indisponibilidade. Não tolera 2% de alucinação. Trade-off invertido vs SaaS tradicional."*

---

## 🎞️ CENA 5 — Compliance e feedback loop (1:15-1:35)

**[Visual: Frameworks de compliance flutuando — GDPR, LGPD, SOC 2, ISO 27001, ISO 42001, EU AI Act. Em paralelo, o feedback loop em 5 estágios — Observação → Diagnóstico → Experimento → Implementação → Medição.]**

**[Ive:]**
> *"Compliance custa. 15-25% do headcount de engineering vai para compliance em 2026. Não é debênture. É custo de entrada em mercados regulados. Quem pula compliance não chega a enterprise."*

**[Alencar:]**
> *"E o feedback loop. Toda chamada de LLM vira trace. Trace vira eval. Eval vira patch. Patch vira produto melhor. A taxa de incorporação é a métrica de aprendizado. Crítico: nunca treinar modelo com feedback sintético validado pelo próprio modelo — feedback loop degenerativo."*

---

## 🎞️ CENA 6 — CTA (1:35-1:50)

**[Visual: Número romano "IV" + nome do ebook. Capa NEXUS AFFIL'IA'TE TECH Vol. IV. Atmosfera executiva-técnica.]**

**[Ive, fechando:]**
> *"O Volume IV da NEXUS AFFIL'IA'TE TECH estende cada uma dessas camadas com profundidade técnica, unit economics reais, e os 11 manifestos que todo SaaS IA deveria ter antes de vender."*

**[Alencar:]**
> *"Disponível agora em `oneverso.com.br/academia/colecoes/tech`. Acesse, leia, e construa o SaaS IA que sobrevive ao próximo ciclo."*

---

## 🎯 Métricas de produção

- **Duração total estimada:** 120-150 segundos
- **Personas:** Ive (estratégia + multi-tenancy + compliance + CTA) · Alencar (camadas + SLA + loop + CTA)
- **Tom híbrido:** executivo + técnico + operacional
- **CTA:** ebook completo + decisão de produto
- **Thumbnail:** `thumb-18-fundamento-saas-ia.webp` (2K, 16:9)

---

*Roteiro âncora · Onda 40 · v1.4.0 · NEXUS AFFIL'IA'TE TECH Vol. IV*
*MMN AI-to-AI · Nexus HUB57 · Ecossistema MMN AI-to-AI*

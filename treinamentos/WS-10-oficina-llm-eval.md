---
title: "WS-10 · Oficina de Avaliação de LLMs"
level: master
duration: 180min
format: workshop
tags: [workshop, llm, eval, ragas, llm-as-judge, qualidade, metricas]
last_updated: 2026-07-29
---

# 🎬 WS-10 · Oficina de Avaliação de LLMs

> **Formato:** Workshop gravado (vídeo + material) · **Duração:** 180 min · **Nível:** Master

## 🎯 Objetivo

No fim deste workshop, você vai ser capaz de construir um **pipeline de avaliação de LLMs em produção**, usando RAGAS, LLM-as-judge, e métricas customizadas. Vai sair com um dataset anotado, 3 evaluators rodando, e dashboards em Grafana.

## 📚 Pré-requisitos

- [x] Nível Agente completo
- [x] Curso `cursos/master/04-rag-em-producao.md`
- [x] Experiência com Python intermediário
- [x] Conta OpenAI com créditos

## 🗓️ Agenda

| Tempo | Bloco | O que você faz |
|---|---|---|
| 00:00–00:15 | **Abertura** | Por que LLMs sem avaliação são bombas-relógio |
| 00:15–00:45 | **Métricas clássicas** | Faithfulness, Recall, Precision — o que cada uma mede |
| 00:45–01:30 | **RAGAS hands-on** | Instalar, configurar, rodar em dataset de 50 perguntas |
| 01:30–02:15 | **LLM-as-judge** | Construir judge com prompt estruturado + few-shot |
| 02:15–02:45 | **Dataset anotado** | Criar 100 exemplos com ground truth |
| 02:45–03:00 | **Q&A + próximos passos** | Como integrar com produção |

## 🛠️ Stack

- Python 3.11+
- `ragas==0.1.0+`
- `openai==1.50+`
- `langchain==0.3+`
- `pandas`, `numpy`
- OpenAI API key (ou LiteLLM proxy)

## 📂 Arquivos do Workshop

- `templates/dataset_template.jsonl` — template de dataset anotado
- `templates/llm_judge_prompt.txt` — prompt estruturado para judge
- `templates/eval_pipeline.py` — pipeline completo executável
- `templates/grafana_dashboard.json` — dashboard de métricas

## 💡 Por que importa

"Sem avaliação, você está voando cego." — Sir. Nexus Alencar

90% dos projetos de LLM em produção falham por falta de avaliação contínua. Este workshop ensina a **medir antes de otimizar** — princípio fundamental que separa amadores de profissionais.

## 🎓 Entregáveis

Ao completar, você terá:
- ✅ Dataset anotado de 100+ exemplos
- ✅ Pipeline RAGAS rodando em CI
- ✅ LLM-as-judge com F1 > 0.85
- ✅ Dashboard Grafana com 5 métricas
- ✅ Alertas Slack quando quality < threshold

## 🔗 Recursos

- `tutoriais/21-deploy-api-ia-producao.md`
- `cursos/master/04-rag-em-producao-mavis-detalhado.md`
- `producao/INCIDENT-RESPONSE-RUNBOOK.md` (seção "model degradation")

---

**Versão 1.0** · 2026-07-29 · Mavis Agent
**Mantido em**: `treinamentos/WS-10-oficina-llm-eval.md`

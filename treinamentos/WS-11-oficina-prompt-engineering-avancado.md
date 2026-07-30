---
title: "WS-11 · Oficina de Prompt Engineering Avançado"
level: master
duration: 150min
format: workshop
tags: [workshop, prompt-engineering, few-shot, cot, react, tree-of-thoughts]
last_updated: 2026-07-29
---

# 🎬 WS-11 · Oficina de Prompt Engineering Avançado

> **Formato:** Workshop gravado (vídeo + material) · **Duração:** 150 min · **Nível:** Master

## 🎯 Objetivo

No fim deste workshop, você vai dominar **7 técnicas avançadas de prompt engineering**: few-shot, chain-of-thought, ReAct, tree-of-thoughts, self-consistency, prompt chaining, e function calling. Cada técnica com exemplo real e medição de ganho.

## 📚 Pré-requisitos

- [x] Nível Agente completo
- [x] Tutorial `tutoriais/19-prompt-engineering-metodo-ctr.md` (ou `-mavis.md`)
- [x] Familiaridade com OpenAI/Anthropic APIs

## 🗓️ Agenda

| Tempo | Bloco | Técnica | Ganho típico |
|---|---|---|---|
| 00:00–00:10 | **Abertura** | Anatomia de um prompt | — |
| 00:10–00:30 | **T1: Few-shot** | Exemplos concretos | +20% accuracy |
| 00:30–00:50 | **T2: Chain-of-thought** | "Pense passo a passo" | +35% em math |
| 00:50–01:10 | **T3: ReAct** | Reasoning + Acting | +50% em agentic |
| 01:10–01:30 | **T4: Tree-of-thoughts** | Explorar múltiplos caminhos | +40% em puzzles |
| 01:30–01:50 | **T5: Self-consistency** | Voting entre N respostas | +15% robustez |
| 01:50–02:10 | **T6: Prompt chaining** | Pipeline de prompts | Modularidade |
| 02:10–02:30 | **T7: Function calling** | Tools/JSON mode | Estruturação |
| 02:30–02:50 | **Comparação** | Benchmark com 5 modelos | — |
| 02:50–03:00 | **Q&A** | Casos específicos do seu projeto | — |

## 🛠️ Stack

- Python 3.11+
- `openai`, `anthropic`, ou `litellm` (100+ provedores)
- `pandas` para análise de resultados
- `jupyter` para experimentação iterativa

## 📂 Arquivos

- `templates/technique_01_fewshot.py`
- `templates/technique_02_cot.py`
- `templates/technique_03_react.py`
- `templates/technique_04_tot.py`
- `templates/technique_05_self_consistency.py`
- `templates/technique_06_chaining.py`
- `templates/technique_07_function_calling.py`
- `templates/benchmark_5_models.py` — script de comparação

## 💡 Casos de Uso

- **Few-shot**: classificação, extração, formatação
- **CoT**: problemas multi-step, math, lógica
- **ReAct**: agentes que precisam de tools
- **ToT**: puzzles, estratégia, planejamento
- **Self-consistency**: respostas de alto risco (médico, jurídico)
- **Chaining**: pipelines complexos (extract → summarize → format)
- **Function calling**: integração com APIs externas

## 🎓 Entregáveis

- ✅ 7 prompts otimizados (1 por técnica) no seu domínio
- ✅ Benchmark comparativo em 5 modelos
- ✅ Decisão: qual técnica usar para cada caso
- ✅ Templates reutilizáveis no seu toolkit

---

**Versão 1.0** · 2026-07-29 · Mavis Agent
**Mantido em**: `treinamentos/WS-11-oficina-prompt-engineering-avancado.md`

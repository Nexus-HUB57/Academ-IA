---
title: "Fine-Tuning de Modelos OpenAI: Guia Completo"
tutorial_code: TUT-EL-01
level: elite
duration: 50min
prerequisites: ["19-prompt-engineering-metodo-ctr.md"]
tags: [tutorial, fine-tuning, openai, custom-model, distillation, gpt-4o-mini]
last_updated: 2026-07-07
---

# 🎯 Fine-Tuning de Modelos OpenAI: Guia Completo

> **Tempo:** 50 min · **Nível:** Elite · **Pré-requisito:** TUT-FU-19

## Quando Fine-Tuning faz sentido (e quando NÃO)

### ✅ Use fine-tuning para:

- **Tom de voz específico da marca** (sempre responder no estilo X)
- **Formato estruturado** (sempre JSON, sempre SQL, sempre Markdown)
- **Skill especializado** (sempre classificar intenção, sempre extrair entidades)
- **Latência** (modelo menor = mais rápido = mais barato)
- **Distillation** (gpt-4o → gpt-4o-mini mantendo 90% da qualidade)

### ❌ NÃO use fine-tuning para:

- **Conhecimento novo** → use **RAG** (tutorial #16-17)
- **Poucos dados** (< 100 exemplos) → use **prompting** + few-shot
- **Dados que mudam frequentemente** → RAG sempre vence
- **Primeira iteração** → prompting primeiro, fine-tune depois

## Anatomia de um Fine-Tune

```
Dataset (50-500 exemplos)
       ↓
   JSONL format  ← prompt + completion
       ↓
   Upload via API
       ↓
   Job de treinamento (10-30min)
       ↓
   Modelo customizado: ft:gpt-4o-mini:org:model:abc123
       ↓
   Avaliar vs base + deploy
```

## Passo 1: Coletar Dados de Qualidade

Mínimo **200 exemplos** de alta qualidade. Formato JSONL:

```jsonl
{"messages": [{"role": "system", "content": "Você classifica intenções de clientes."}, {"role": "user", "content": "Quero cancelar minha assinatura"}, {"role": "assistant", "content": "cancelamento"}]}
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "Quanto custa?"}, {"role": "assistant", "content": "preço"}]}
```

### Gerar dados sintéticos (50min de trabalho manual → 30min com LLM)

```python
# gerar_dataset.py
from openai import OpenAI
import json
import random

client = OpenAI()

INTENT_EXAMPLES = [
    ("Quero cancelar minha assinatura", "cancelamento"),
    ("Como faço para parar de pagar?", "cancelamento"),
    ("Vocês têm plano para empresa?", "preco"),
    ("Quanto custa o plano pro?", "preco"),
    ("Como funciona o produto?", "duvida"),
    ("Onde baixo o app?", "duvida"),
    ("Estou com problema no login", "suporte"),
    ("Não consigo acessar minha conta", "suporte"),
]

def gerar_dataset_sintetico(seed_pairs, n_por_seed=30):
    """Gera variações usando GPT-4o."""
    dataset = []
    for intent_text, intent_class in seed_pairs:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "system",
                "content": "Gere variações realistas de mensagens de "
                           "clientes para esta intenção. Varie: "
                           "formalidade, tamanho, typos, emojis, "
                           "gírias regionais BR."
            }, {
                "role": "user",
                "content": f"""Intenção: {intent_class}
Exemplo: '{intent_text}'

Gere {n_por_seed} variações em JSON:
{{"variacoes": ["msg1", "msg2", ...]}}"""
            }],
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content)
        for msg in data["variacoes"]:
            dataset.append({
                "messages": [
                    {"role": "system", "content": "Classifique a intenção."},
                    {"role": "user", "content": msg},
                    {"role": "assistant", "content": intent_class},
                ]
            })
    return dataset

dataset = gerar_dataset_sintetico(INTENT_EXAMPLES, n_por_seed=30)
print(f"Total: {len(dataset)} exemplos")

# Salvar em JSONL
with open("train.jsonl", "w") as f:
    for ex in dataset:
        f.write(json.dumps(ex) + "\\n")
```

## Passo 2: Validar Dados

```python
def validate_jsonl(path):
    issues = []
    with open(path) as f:
        for i, line in enumerate(f, 1):
            try:
                ex = json.loads(line)
                assert "messages" in ex
                assert len(ex["messages"]) >= 2
                assert ex["messages"][0]["role"] == "user"
                assert ex["messages"][-1]["role"] == "assistant"

                # Tamanho máximo
                total_chars = sum(len(m["content"]) for m in ex["messages"])
                if total_chars > 50_000:
                    issues.append(f"L{i}: muito longo ({total_chars})")
            except Exception as e:
                issues.append(f"L{i}: {e}")
    return issues

issues = validate_jsonl("train.jsonl")
if issues:
    print("⚠️ Problemas:", *issues[:5], sep="\\n")
else:
    print("✅ Dataset válido")
```

## Passo 3: Upload e Treino

```python
# 1. Upload
uploaded = client.files.create(
    file=open("train.jsonl", "rb"),
    purpose="fine-tune",
)
print(f"File ID: {uploaded.id}")

# 2. Criar job
job = client.fine_tuning.jobs.create(
    training_file=uploaded.id,
    model="gpt-4o-mini",  # ou "gpt-3.5-turbo" para tarefas simples
    hyperparameters={
        "n_epochs": 3,             # 2-5 típico
        "learning_rate_multiplier": 0.1,
    },
    suffix="intent-classifier-v1",
)
print(f"Job: {job.id}, Status: {job.status}")
```

## Passo 4: Monitorar Loss

```python
import time

while True:
    job = client.fine_tuning.jobs.retrieve(job.id)
    print(f"Status: {job.status}, Trained tokens: {job.trained_tokens}")

    events = client.fine_tuning.jobs.list_events(job.id, limit=10)
    for e in events.data:
        if "training_loss" in e.message.lower():
            print(f"  → {e.message}")

    if job.status in ("succeeded", "failed"):
        break
    time.sleep(30)
```

**Sinais de sucesso**: training_loss caindo monotonicamente
**Sinais de problema**: loss estagnada ou subindo (aumentar dados ou ajustar LR)

## Passo 5: Avaliar Modelo

```python
# Pegar ID do modelo fine-tuned
ft_model = job.fine_tuned_model  # "ft:gpt-4o-mini:org:intent-classifier:abc123"

# Test set (NÃO usado no treino)
test_cases = [
    {"input": "Quero parar de usar o serviço", "expected": "cancelamento"},
    {"input": "Tem versão grátis?", "expected": "preco"},
    # ... 50-100 casos
]

# Avaliar fine-tuned vs base
results = {"base": [], "ft": []}
for tc in test_cases:
    for name, model_id in [("base", "gpt-4o-mini"), ("ft", ft_model)]:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "Classifique a intenção."},
                {"role": "user", "content": tc["input"]},
            ],
            max_tokens=20,
        )
        predicted = response.choices[0].message.content.strip().lower()
        results[name].append(predicted == tc["expected"])

print(f"Acurácia base: {sum(results['base']) / len(test_cases):.1%}")
print(f"Acurácia fine-tuned: {sum(results['ft']) / len(test_cases):.1%}")
```

**Meta**: fine-tuned deve ser **>= base** e idealmente **+10-30%**.

## Passo 6: Deploy e Monitorar

```python
# Use o modelo fine-tuned em produção
response = client.chat.completions.create(
    model=ft_model,  # ex: "ft:gpt-4o-mini:..."
    messages=[...],
)

# Monitore drift
# Se acurácia cair > 5% em produção: retreinar com dados novos
```

## Custos Estimados

| Modelo | Tamanho dataset | Custo treino | Custo inferência |
|---|---|---|---|
| gpt-3.5-turbo | 500 ex, 3 epochs | ~$3 | 2-3x base |
| gpt-4o-mini | 500 ex, 3 epochs | ~$15 | 2-5x base |
| gpt-4o | 500 ex, 3 epochs | ~$100 | 2-5x base |

**Regra**: fine-tune só se (1) você tem dados de qualidade, (2)
prompting+RAG não atingem a meta, (3) o ganho compensa o custo extra.

## Checklist de Decisão

```
✅ Dataset ≥ 200 exemplos validados
✅ RAG + prompting testados e insuficientes
✅ Métrica de sucesso clara (acurácia, F1, latência)
✅ Budget aprovado (treino + inferência extra)
✅ Pipeline de retreino definido
✅ Avaliação em produção com shadow traffic
```

## Próximos passos

- **Continuous fine-tuning**: pipeline que ret reina com dados novos
- **DPO (Direct Preference Optimization)**: alinhar preferências
- **Constitutional AI**: treinar com regras éticas

## Recursos

- OpenAI Fine-Tuning: <https://platform.openai.com/docs/guides/fine-tuning>
- Cookbook: <https://cookbook.openai.com/examples/chat_finetuning_data_prep>
- Custos: <https://openai.com/pricing>
---
title: "Prompt Engineering: o Método CTR (Contexto-Tarefa-Restrição)"
tutorial_code: TUT-FU-01
level: fundamental
duration: 25min
prerequisites: []
tags: [tutorial, prompt-engineering, ctr, few-shot, chain-of-thought, fundamental]
last_updated: 2026-07-07
---

# ✍️ Prompt Engineering: o Método CTR

> **Tempo:** 25 min · **Nível:** Fundamental · **Pré-requisito:** nenhum

## O Problema

Você usa IA todo dia, mas as respostas saem genéricas, imprecisas, ou
fora do tom. Culpa do prompt — não do modelo.

**Antes e depois real**:

```
❌ "Escreve um email de vendas"
→ "Prezado cliente, gostaríamos de apresentar nossa solução inovadora..."

✅ "Você é um copywriter B2B sênior. Minha audiência: gerentes de
   logística de e-commerce médio porte (R$ 1-10M MRR). Tarefa: email
   frio de 150 palavras oferecendo demo gratuita de 15min. Restrição:
   sem palavras 'revolucionário', 'transforme', 'inovador'. Tom:
   profissional-humano, primeira linha com gancho de dor."
→ "A logística do seu e-commerce está sangrando dinheiro em devoluções
   que você nem rastreia. Em 15 minutos mostro como 3 clientes nossos
   cortaram devoluções em 40% sem contratar ninguém..."
```

## O Método CTR

Três blocos que cobrem 90% dos casos:

| Letra | Pergunta | Resposta |
|---|---|---|
| **C** — Contexto | Quem é você e em que situação? | Persona + cenário + informação de fundo |
| **T** — Tarefa | O que fazer? | Verbo de ação + entregável específico |
| **R** — Restrição | Quais limites? | Tamanho, tom, formato, idioma, "não fazer" |

## Estrutura Modelo

```python
PROMPT_CTR = """
# C — Contexto
Você é [persona específica]. Minha situação: [cenário]. Informação
relevante: [dados que o modelo precisa saber].

# T — Tarefa
[Verbo] [objeto] [critério de sucesso].

# R — Restrição
- Tamanho: [X palavras / X parágrafos / X caracteres]
- Tom: [formal/casual/técnico/persuasivo]
- Formato: [markdown/JSON/lista/tabela]
- Idioma: [PT-BR/EN/ES]
- NÃO usar: [palavras/frases proibidas]
"""
```

## 5 Exemplos Práticos

### Exemplo 1: Email de vendas

```python
prompt_email = """
C: Você é copywriter B2B com 10 anos de experiência vendendo SaaS para
e-commerce. Meu produto: plataforma de gestão de devoluções. Cliente
ideal: gerente de operações de e-commerce com 100-500 pedidos/dia.

T: Escreva um email frio de 150 palavras oferecendo uma demo gratuita
de 15min.

R: - Tom: humano, direto, sem hype
   - Assunto: até 50 caracteres, gerar 3 variações
   - Estrutura: gancho (1 frase) → dor (2 frases) → CTA (1 frase)
   - NÃO usar: 'revolucionário', 'transforme', 'game-changer'
"""
```

### Exemplo 2: Resumo de relatório

```python
prompt_resumo = """
C: Você é analista de BI. Acabei de gerar este relatório de vendas
{dados}. Público: CEO que tem 5 minutos.

T: Resuma em 3 bullet points + 1 insight não-óbvio.

R: - Cada bullet: 1 linha, máximo 20 palavras
   - Insight: dado contraintuitivo dos dados
   - Tom: executivo, sem jargão técnico
   - NÃO incluir: tabela, gráficos, metodologia
"""
```

### Exemplo 3: Geração de copy para Instagram

```python
prompt_instagram = """
C: Você é social media strategist. Marca: café especial de pequenos
produtores. Audiência: millennials urbanos que valorizam origem.

T: Crie 5 legendas para post sobre 'Dia Internacional do Café'.

R: - Cada legenda: 50-100 palavras
   - Hashtags: 5-10 por legenda, misturar nichadas e amplas
   - Tom: educativo + emocional, sem ser clichê
   - Incluir: CTA claro (comentar, salvar, compartilhar)
   - 1 das 5 deve ter storytelling de produtor
"""
```

### Exemplo 4: Análise de feedback de cliente

```python
prompt_feedback = """
C: Você é product manager. Recebi estes feedbacks: {lista}. Produto:
CRM para PMEs.

T: Agrupe em 3-5 temas principais, identifique padrão recorrente,
sugira 1 ação concreta.

R: - Cada tema: {número} feedbacks, descrição em 1 linha
   - Padrão: clientes de qual segmento mais reclamam
   - Ação: realista em 1 sprint
   - NÃO usar: 'todos', 'ninguém', generalizar
"""
```

### Exemplo 5: Código Python

```python
prompt_codigo = """
C: Você é dev Python senior. Stack: FastAPI + PostgreSQL + Redis.
Tarefa: criar endpoint de busca de produtos com paginação.

T: Implemente o endpoint com:
- Query param: q (string), page (int, default 1), size (int, default 20)
- Busca em product.name (ILIKE) e product.sku (=)
- Cache Redis por query string, TTL 5min
- Response: {total: int, items: [...]}

R: - Type hints em tudo
   - Validação com Pydantic
   - Tratamento de erro (404 se vazio)
   - Teste pytest mínimo
   - NÃO usar: ORM pesado, SQLAlchemy legacy
"""
```

## Técnicas Avançadas

### Few-Shot (2-5 exemplos)

```python
prompt_few_shot = """
Classifique reviews em: positivo, negativo, neutro.

Review: "Adorei! Chegou antes do prazo."
Classe: positivo

Review: "Não funcionou. Dinheiro jogado fora."
Classe: negativo

Review: "Funciona, mas o manual é confuso."
Classe: neutro

Review: "Demora mas entrega."
Classe: """
```

### Chain-of-Thought (CoT)

```python
prompt_cot = """
Resolva passo a passo. Mostre seu raciocínio antes da resposta final.

Problema: João tem 3 caixas com 12 maçãs. Come 5 e dá metade do
resto para Maria. Com quantas maçãs João fica?

Raciocínio:
1. Total inicial: 3 × 12 = ?
2. Após comer 5: ? - 5 = ?
3. Metade do resto: ? / 2 = ?
4. João fica com: ? - ? = ?

Resposta final: [número]
"""
```

### Role Prompting (persona explícita)

```python
prompt_role = """
Você é um Engenheiro de Software Sênior com 15 anos de experiência
em sistemas distribuídos e microservices. Você é pragmático, foca em
produção, e sempre menciona trade-offs. Você odeia over-engineering.
"""
```

## Anti-Patterns (evite)

| ❌ Anti-pattern | Por que falha | ✅ Como corrigir |
|---|---|---|
| "Seja criativo" | Modelo não sabe o que é criativo pra você | Defina 3 exemplos do que quer |
| "Faça o melhor possível" | Instrução vazia | Especifique métrica (acurácia, tom) |
| "Resposta breve" | Ambíguo | "Máximo 100 palavras" |
| Repetir a mesma instrução em 5 parágrafos | Confunde o modelo | 1 parágrafo claro > 5 redundantes |
| Esquecer restrições negativas | Modelo vai usar clichês | Liste explicitamente o que NÃO fazer |

## Biblioteca de Prompts

Salve seus prompts em `Lab-Nexus/prompts/copywriting/` ou
`Lab-Nexus/prompts/analise/`. Versione em git. Crie variações e
meça qual performa melhor.

## Checklist Final

- [ ] Persona definida explicitamente
- [ ] Contexto fornece informação suficiente
- [ ] Tarefa é um verbo de ação específico
- [ ] Restrições incluem tamanho + tom + formato + idioma
- [ ] Palavras/frases proibidas listadas
- [ ] Testado com 3-5 inputs diferentes
- [ ] Versionado em git (Lab-Nexus/prompts/)

## Próximos passos

- **Few-shot avançado**: tutorial #20
- **Cadeias de prompts**: aula em master/04
- **Agentes multi-prompt**: tutorial #21

## Recursos

- OpenAI Prompt Engineering: <https://platform.openai.com/docs/guides/prompt-engineering>
- Anthropic Prompt Library: <https://docs.anthropic.com/en/prompt-library>
- Learn Prompting: <https://learnprompting.org>
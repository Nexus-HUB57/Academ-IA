---
title: "Apostila 48 · Design Thinking com IA"
subtitle: "Como aplicar design thinking para criar produtos irresistíveis com agentes IA"
author: "Equipo Nexus · Sra. Nexus Ive + Sir. Nexus Alencar"
version: "1.0.0"
date: 2026-08-04
pattern: "MMN_IA"
---

**Apostila 48 · Design Thinking com IA**

*O guia completo de 2026 para aplicar design thinking em produtos de IA. Cobre empatia, definição, ideação, prototipagem e teste, com foco em agents autônomos.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 Por Que Esta Apostila é Crítica

**A maioria dos produtos de IA morre porque:**
- ❌ Foca em tecnologia, não em pessoas
- ❌ Resolve problema que ninguém tem
- ❌ UX confusa (usuário não entende o agente)
- ❌ Sem iteração (1.0 e pronto, mesmo quebrado)

**Design thinking resolve porque:**
- ✅ Começa com empatia profunda
- ✅ Define o problema certo (não a solução errada)
- ✅ Prototipa rápido, falha barato
- ✅ Testa com usuários reais constantemente

**Resultado:** produtos 3x mais bem-sucedidos (McKinsey, 2024).

---

## 📚 Sumário

1. O que é Design Thinking
2. Os 5 Estágios
3. Empatia: entender o usuário
4. Definição: encontrar o problema certo
5. Ideação: gerar soluções
6. Prototipagem: construir barato
7. Teste: validar com usuários
8. Aplicado a Agentes IA
9. Patterns de UX para Agentes
10. Casos Reais
11. Templates Prontos

---

## 🎨 1. O que é Design Thinking

### 1.1 — Definição

**Design thinking** é uma abordagem centrada no humano para resolver problemas complexos, usando:

1. **Empatia** profunda com usuários
2. **Definição** clara do problema
3. **Ideação** divergente
4. **Prototipagem** rápida
5. **Teste** com usuários

**Não é:**
- ❌ Só "design bonito"
- ❌ Pesquisa de mercado tradicional
- ❌ Foco em features
- ❌ Solução definida upfront

**É:**
- ✅ Processo iterativo
- ✅ Validação contínua
- ✅ Foco no outcome (não output)
- ✅ Falha rápido e barato

### 1.2 — Origem

- **IDEO** (1990s): consultoria popularizou
- **Stanford d.school** (2005): formalizou como método
- **Tim Brown** (2008): livro "Change by Design"
- **Aplicado a software** (2010s): ágil + design thinking

### 1.3 — Quando Usar

✅ **Use quando:**
- Problema complexo (sem solução óbvia)
- Usuários com necessidades diversas
- Mercado novo / sem playbook
- Risco alto (não pode falhar em prod)
- Time multidisciplinar

❌ **Não use quando:**
- Problema bem definido e conhecido
- Bug fix (use análise de causa raiz)
- Operação rotineira (use runbook)

---

## 🔄 2. Os 5 Estágios

```
   ┌──────────┐
   │ EMPATIA  │ ← Entender
   └─────┬────┘
         ↓
   ┌──────────┐
   │DEFINIÇÃO │ ← Sintetizar
   └─────┬────┘
         ↓
   ┌──────────┐
   │ IDEAÇÃO  │ ← Gerar
   └─────┬────┘
         ↓
   ┌──────────┐
   │PROTÓTIPO │ ← Construir
   └─────┬────┘
         ↓
   ┌──────────┐
   │  TESTE   │ ← Validar
   └─────┬────┘
         ↓
         └─────→ Volta para empatia (iterar)
```

**Importante:** não é linear. É cíclico. Você pode voltar a qualquer estágio.

---

## 👥 3. Empatia: Entender o Usuário

### 3.1 — O que é Empatia

**Empatia ≠ simpatia.** Empatia é entender profundamente:
- O que o usuário **faz** (comportamento)
- O que o usuário **pensa** (crenças)
- O que o usuário **sente** (emoções)
- O que o usuário **diz** (verbal)
- O que o usuário **quer** (desejo)
- O que o usuário **precisa** (real)

### 3.2 — Técnicas de Pesquisa Empática

**1. Entrevistas em Profundidade (1:1, 30-60min)**
- 5-8 entrevistas por persona
- Perguntas abertas ("me conte sobre a última vez que...")
- Escutar mais, falar menos
- Gravar (com permissão) e transcrever

**2. Observação Direta (sombra)**
- Acompanhar usuário em seu ambiente
- Ver o que FAZEM, não o que dizem
- Anotar: ações, hesitações, atalhos

**3. Imersão Contextual**
- Usar o produto você mesmo
- Ficar 1 semana "como usuário"
- Documentar fricções

**4. Entrevistas com Stakeholders**
- Outros times (vendas, suporte)
- Clientes existentes
- Ex-clientes (por que saíram?)

**5. Pesquisa Quantitativa**
- Survey (50-100 respondentes)
- Analytics de comportamento
- Dados de uso do produto

### 3.3 — Template de Entrevista

```markdown
# Entrevista · [Persona] · [Data]

## Contexto
- Quem é: [nome, idade, cargo, empresa]
- Há quanto tempo usa [categoria]: ___
- Última vez que precisou: ___

## Comportamento atual
- Como você [faz a tarefa] hoje? (sem nosso produto)
- Quais ferramentas usa? ___
- Quanto tempo leva? ___
- O que mais te frustra? ___

## Dores (verbatim)
- "Quando eu tento [X], acontece [Y], e isso me faz sentir [Z]"
- "O maior problema é [W]"

## Ganhos desejados
- "Se eu pudesse [X], seria perfeito"
- "O que me faria feliz é [Y]"

## Jobs to be done
- Quando [situação], eu quero [motivação], para [outcome]

## Surpresas
- Coisa que descobri que não esperava
```

### 3.4 — Empathy Map

```markdown
# Empathy Map · [Persona]

## SAY (o que diz)
- "Frase 1"
- "Frase 2"

## THINK (o que pensa)
- Crença 1
- Crença 2

## FEEL (o que sente)
- Emoção 1 (em qual situação?)
- Emoção 2

## DO (o que faz)
- Ação 1 (quando?)
- Ação 2

## PAIN (dores)
- Frustração 1
- Medo 1

## GAIN (ganhos)
- Desejo 1
- Aspiração 1
```

### 3.5 — Persona

**Com base nas entrevistas, criar 2-4 personas:**

```markdown
# Persona · [Nome] · [Arquetipo]

## Demografia
- Idade: ___
- Cargo: ___
- Empresa: ___
- Renda: ___
- Localização: ___

## Comportamento
- Tools favoritas: ___
- Tempo gasto na tarefa X: ___
- Onde busca informação: ___

## Objetivos
- Curto prazo (3 meses): ___
- Longo prazo (1 ano): ___

## Frustrações
- "Frase 1"
- "Frase 2"

## Citações
- "O que me faria feliz é ___"
- "Meu maior medo é ___"

## Tecnologias
- Usa: ___
- Já testou: ___
- Nunca vai usar: ___
```

---

## 🎯 4. Definição: Encontrar o Problema Certo

### 4.1 — Sintetizar Pesquisas

**Após 5-8 entrevistas:**
1. Transcrever tudo
2. Identificar padrões (palavras, temas)
3. Agrupar em "affinity map" (post-its virtuais)
4. Insights emergem naturalmente

**Affinity Map (Miro/Figma):**
```
[Cluster 1: Tempo]     [Cluster 2: Confusão]    [Cluster 3: Custo]
- "demora muito"        - "não sei qual"         - "muito caro"
- "10 min por dia"      - "tentei mas desisti"   - "free, mas"
- "could be faster"     - "interface confusa"    - "freemium ruim"
```

### 4.2 — Point of View (POV)

**Formato:** [Usuário] + [Necessidade] + [Insight]

**Exemplos:**

❌ **Ruim:** "Usuário precisa de ferramenta de email marketing"
- Foca em solução, não em problema

✅ **Bom:** "Maria (CMO de SaaS B2B) precisa de visibilidade sobre o que cada email gera em receita, porque hoje ela só vê open rate e não consegue provar ROI para o CEO"

**Estrutura HMW (How Might We):**

✅ "Como podemos ajudar Maria a mostrar ROI de email marketing para o CEO, mesmo quando o funil é longo?"

### 4.3 — Jobs to be Done (JTBD)

**Estrutura:** Quando [situação], eu quero [motivação], para [outcome]

**Exemplo:**

- **Quando** meu cliente B2B está pronto para comprar,
- **eu quero** receber um follow-up personalizado com case de cliente similar,
- **para** aumentar confiança na decisão

**Diferente de feature:** "Quero um botão de 'sugerir case similar' no CRM"

### 4.4 — Definição de Problema Validada

**Critérios de boa definição:**
- ✅ Centrada no usuário (não na empresa)
- ✅ Inspira soluções (não muito ampla nem específica)
- ✅ Tem insights (não é óbvia)
- ✅ Conectada a evidência (vem de pesquisa)

---

## 💡 5. Ideação: Gerar Soluções

### 5.1 — Brainstorming (Regras)

**5 regras clássicas:**
1. **Quantidade > qualidade** (gerar muitas)
2. **Sem julgamento** (deferir críticas)
3. **Construir em cima** ("sim, e...")
4. **Pensar grande** (sem restrições iniciais)
5. **Estimular ideias malucas** (geram insights)

**Setup:**
- Time de 4-7 pessoas (multidisciplinar)
- Timer de 30-60 min
- 1 facilitador
- Post-its + quadro (ou Miro)

### 5.2 — Técnicas de Ideação

**1. SCAMPER (transformar)**
- **Substitute:** O que posso substituir?
- **Combine:** O que posso combinar?
- **Adapt:** O que posso adaptar?
- **Modify:** O que posso modificar?
- **Put to other use:** Usar para outro propósito?
- **Eliminate:** O que posso eliminar?
- **Rearrange:** O que posso reorganizar?

**2. How Might We (HMW)**
- Gerar 10-20 HMWs a partir do POV
- "Como podemos ___?"

**3. Worst Possible Idea**
- Brainstorm do pior
- Inverter para insights

**4. Analogias**
- Como [indústria X] resolve isso?
- Transferir patterns

**5. Six Thinking Hats**
- Lógica, emoção, risco, otimismo, criatividade, processo

### 5.3 — Seleção de Ideias

**Após gerar 30-50 ideias, selecionar 3-5 com:**

**Matriz de Impacto × Esforço:**

```
         Alto Impacto    Baixo Impacto
Alto     FAZER AGORA      Quick Wins
Esforço  (sweet spot)     (se sobrar tempo)

Baixo    Estratégico     Reconsiderar
Esforço  (planejar)      (provavelmente skip)
```

**Critérios adicionais:**
- Alinhamento com estratégia
- Viabilidade técnica
- Tamanho do mercado impactado
- Velocidade de validação

---

## 🛠️ 6. Prototipagem: Construir Barato

### 6.1 — Níveis de Fidelidade

**L0: Sketch (1-2h)**
- Papel + caneta
- Validar conceito
- Stakeholders

**L1: Wireframe (1-2 dias)**
- Figma/Balsamiq
- Estrutura, não visual
- Validar fluxo

**L2: Mockup Visual (2-5 dias)**
- Figma high-fidelity
- Visual finalizado
- Validar estética

**L3: Protótipo Interativo (1-2 semanas)**
- Click-through (Figma)
- Validar UX completa

**L4: MVP (4-8 semanas)**
- Funcional, mas mínimo
- Validar valor com usuários reais

**L5: Beta (1-3 meses)**
- Polido, mas com gaps
- Validar modelo de negócio

**Regra:** **use o nível mais baixo que responda sua pergunta.**

### 6.2 — Prototipagem Rápida com IA

**Com agentes IA, prototipar é mais rápido:**

**L0 → L4 em 1 dia:**
- Spec: doc de 2 páginas
- Wireframe: Figma AI
- Frontend: v0.dev, Cursor, Bolt.new
- Backend: Claude/Copilot
- Deploy: Vercel/Railway

**Importante:** o protótipo não é o produto. É para **aprender**, não para lançar.

### 6.3 — Testar o Protótipo

**Testes rápidos:**
- Hallway test: pare 5 pessoas no corredor, dê 30s, peça pra usar
- Moderado: 1 moderador, 1 usuário, pensa em voz alta
- Unmoderated: Maze, UserTesting
- A/B: lançar 2 versões, medir

---

## 🧪 7. Teste: Validar com Usuários

### 7.1 — Tipos de Teste

**1. Teste de Usabilidade (qualitativo)**
- 5-8 usuários
- Tarefa específica
- Observar onde travam
- Perguntar "o que esperava acontecer?"

**2. Teste de Conceito (qualitativo)**
- Mostrar mockup
- "Você usaria isso? Por quê?"
- "Quanto pagaria?"

**3. A/B Test (quantitativo)**
- 2 variantes
- 1000+ usuários cada
- Medir conversão
- Significância estatística

**4. Wizard of Oz (engenharia disfarçada)**
- Humano fingindo ser IA
- Usuário acha que é IA
- Testar se UX faz sentido antes de construir

**5. Fake Door (smoke test)**
- Botão que "vira em breve"
- Medir quantos clicariam
- Validar demanda antes de construir

### 7.2 — Métricas de UX

**Quantitativas:**
- **Task success rate:** % que completam tarefa
- **Time on task:** tempo médio
- **Error rate:** erros por sessão
- **SUS (System Usability Scale):** score 0-100 (padrão)
- **NPS:** recomendação
- **Retention:** % que voltam

**Qualitativas:**
- Verbal reactions ("isso é confuso", "show!")
- Body language (franziu testa, sorriu)
- Quotes poderosos
- Sugestões espontâneas

### 7.3 — Framework de Análise

**Por usuário:**
- O que funcionou?
- Onde travou?
- O que foi surpreendente?
- O que mudaria?

**Agregado:**
- Padrões (todos travam em X?)
- Outliers (um usuário achou genial, todos acharam ruim)
- Insights: "Ah, eles não entendem Y porque Z"

---

## 🤖 8. Aplicado a Agentes IA

### 8.1 — Desafios Específicos

Agentes IA têm desafios únicos de UX:

**1. Intenção ambígua**
- Usuário não sabe o que o agente pode fazer
- Solução: exemplos, sugestões, onboarding

**2. Confiança**
- Usuário não confia em IA para tarefa importante
- Solução: transparência, controles, fallback humano

**3. Alucinação**
- Agente "inventa" coisas
- Solução: sources, citations, confidence score

**4. Latência**
- LLM demora 2-10s
- Solução: streaming, feedback de progresso

**5. Inconsistência**
- Mesma pergunta, resposta diferente
- Solução: temperatura baixa, versionamento

**6. Confusão de escopo**
- Usuário pede o que agente não sabe
- Solução: limites claros, redirecionamento

### 8.2 — Onboarding de Agente

**Critical first 30 segundos:**

**Padrão 1: Demo interativa**
```
"Oi! Eu sou [Nome], seu assistente de [X].

Vou te mostrar 3 coisas que posso fazer:

1. [Sugestão 1]
2. [Sugestão 2]
3. [Sugestão 3]

Qual te interessa?"
```

**Padrão 2: Pergunta aberta**
```
"Oi! Sou [Nome]. Me conta: o que você quer fazer hoje?"
```

**Padrão 3: Templates**
```
"Como posso te ajudar?

[ ] [Tarefa comum 1]
[ ] [Tarefa comum 2]
[ ] [Tarefa comum 3]

Ou descreva seu caso:"
```

### 8.3 — Feedback Loop

**Cada turno do agente deve ter:**

1. **Confirmação de entendimento**
- "Entendi, você quer ___?"

2. **Progresso visível**
- "Vou: 1) buscar X, 2) comparar, 3) recomendar"

3. **Resultado claro**
- "Encontrei 3 opções. Qual prefere?"

4. **Recuperação de erro**
- "Desculpe, não entendi. Pode reformular?"

---

## 🎨 9. Patterns de UX para Agentes

### 9.1 — Human-in-the-Loop

**Decisões críticas pedem aprovação:**

```
Posso transferir R$ 5.000 para conta X?

[Sim, transferir] [Não, cancelar] [Ver detalhes]
```

**Implementação:**

```python
def high_value_action(amount, account):
    if amount > 1000:
        # Pede confirmação
        return {
            "action": "confirmation_required",
            "message": f"Posso transferir R$ {amount} para {account}?",
            "approve_url": f"/actions/approve?id={action_id}",
        }
    # Executa direto
    return transfer(amount, account)
```

### 9.2 — Streaming com Indicador

**Mostra que o agente está trabalhando:**

```
[●●●○○] Pensando...

Até agora:
- ✓ Analisei seu histórico
- ✓ Busquei 5 produtos similares
- ⏳ Comparando preços...
```

### 9.3 — Sources & Citations

**Para evitar alucinação:**

```
Com base em:
[1] https://nexus.com/docs/article-x
[2] https://nexus.com/docs/article-y

A resposta é...
```

### 9.4 — Confiança Visível

```
Confiança: 87%

✓ Muito provável (80%+)
⚠️ Provável (50-80%)
❌ Incerto (<50%)
```

### 9.5 — Recuperação Graciosa

```
Desculpe, não consegui [X].

Posso tentar:
[ ] [Alternativa 1]
[ ] [Alternativa 2]
[ ] Falar com humano
[ ] Cancelar
```

---

## 📊 10. Casos Reais

### Caso 1: Agente de Customer Service

**Problema:** Agente confundia clientes com respostas longas demais.

**Empatia (5 entrevistas):**
- Clientes querem resposta RÁPIDA, não completa
- Não leem parágrafos
- Querem botão "Falar com humano" sempre visível

**Definição:** "Como podemos dar respostas curtas e dar opção de detalhamento?"

**Ideação:** 
- Resposta em 2 frases + botão "Ver mais"
- "Falar com humano" sempre no rodapé
- Confirmação "Isso respondeu?" + follow-up

**Prototipagem:** Figma com 3 variantes de layout

**Teste:** 8 clientes, 87% preferiu versão curta com opção de expandir

**Resultado:** NPS de 32 → 71, ticket time -45%.

### Caso 2: Agente de Vendas (WhatsApp)

**Problema:** Agente vendia 0.5% dos leads. Time de vendas vendia 8%.

**Empatia (8 entrevistas com leads que compraram via humano):**
- Gostam de rapport pessoal
- Confiam em quem "escuta"
- Querem garantia antes de comprar
- Não gostam de bot

**Definição:** "Como podemos fazer bot parecer humano, mantendo escalabilidade?"

**Ideação:**
- Agente 1º contato: perguntas + educado
- Transfere para humano no momento certo
- Humano usa copilot com sugestões de IA

**Prototipagem:** Wizard of Oz (humano fingindo ser bot)

**Teste:** 50 leads divididos em A (bot puro), B (bot+humano), C (humano com copilot)
- A: 0.6%
- B: 4.2% (8x melhor)
- C: 9.5% (16x melhor)

**Resultado:** Implementado B, escalou para 1.000 leads/mês.

### Caso 3: Agente de Research

**Problema:** Agente alucinava facts.

**Empatia (entrevistas com usuários):**
- Confiam em dados verificáveis
- Links são essenciais
- Sources importam mais que eloquência

**Definição:** "Como podemos garantir que cada fato tem source?"

**Ideação:**
- RAG obrigatório (todo fato tem source)
- Citations visíveis [1], [2]
- Confidence score
- "Não sei" como resposta válida

**Prototipagem:** Comparação lado-a-lado (com/sem sources)

**Teste:** 20 usuários, 95% preferiu versão com sources + confidence

**Resultado:** Alucinação reportada caiu de 18% para 2%.

---

## 📋 11. Templates Prontos

### Template: Plano de Design Thinking

```markdown
# Plano DT · [Projeto] · [Data]

## 1. Empatia
- Personas a entrevistar: ___
- Nº entrevistas: ___
- Duração: ___
- Quero aprender: ___

## 2. Definição
- Sintetizar entrevistas: ___
- POV esperado: ___

## 3. Ideação
- Brainstorm: ___
- Nº de ideias: ___
- Critério de seleção: ___

## 4. Prototipagem
- Fidelidade: ___
- Tempo: ___
- Ferramentas: ___

## 5. Teste
- Nº usuários: ___
- Métricas: ___
- Decisão go/no-go: ___

## Timeline
- Semana 1: ___
- Semana 2: ___
- Semana 3: ___
```

### Template: Pesquisa Empírica

```markdown
# Pesquisa · [Persona] · [Data]

## Setup
- Data: ___
- Duração: ___min
- Moderador: ___
- Notas por: ___

## Contexto (5min)
- Agradeça
- Explique objetivo
- Peça permissão para gravar
- Pergunta warm-up: "Me conta sobre você"

## Perguntas abertas (20min)
- "Me conta sobre a última vez que [tarefa]"
- "Como você fez?"
- "O que foi difícil?"
- "O que te fez decidir assim?"

## Dores (10min)
- "Qual é o pior aspecto de [categoria]?"
- "Se você pudesse mudar uma coisa, o quê?"
- "Você já desistiu de [X]? Por quê?"

## Ganhos (10min)
- "Em um mundo ideal, como seria [tarefa]?"
- "O que te faria feliz?"
- "O que você recomendaria para [outra pessoa]?"

## Surpresas
- Coisa que descobri que não esperava

## Próximos passos
- "Posso te chamar se precisar?"
- Recompensa
```

---

## 📚 Materiais Complementares

- `apostilas/35-marketing-conversacional-ia.md` — agentes
- `apostilas/45-debugging-otimizacao-agentes-ia.md` — debug
- `tutoriais/19-prompt-engineering-metodo-ctr.md` — prompts
- `playbooks/PB-PRODUTO-lancamento-beta-fechado.md` — beta
- `treinamentos/WS-09-oficina-marketing-conversacional.md` — marketing
- `Lib-Nexus/best-practices/00-prompt-engineering.md` — prompts

---

## 🔗 Links Externos

- IDEO Design Thinking: https://designthinking.ideo.com/
- Stanford d.school: https://dschool.stanford.edu/
- Interaction Design Foundation: https://www.interaction-design.org/
- Jobs to be Done: https://jobstobedone.org/
- Don Norman: https://jnd.org/

---

*AcademIA · Apostila 48 · Design Thinking com IA · 2026*
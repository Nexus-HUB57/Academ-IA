---
title: "PB-PRODUTO · Lançamento Beta Fechado"
subtitle: "Como validar produto com 10-30 early adopters antes de escalar"
author: "Equipo Nexus · Niko (CEO/AI) + Sra. Nexus Ive"
version: "1.0.0"
date: 2026-07-29
pattern: "MMN_IA"
---

**PB-PRODUTO · Lançamento Beta Fechado**

*Playbook de 6 semanas para validar produto com 10-30 early adopters, antes de escalar para público geral. Inclui critérios de go/no-go, scripts de venda e NPS.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 Quando Usar Este Playbook

**Use quando:**
- Você tem MVP funcional (não precisa ser perfeito)
- Quer validar antes de investir em marketing
- Precisa de feedback estruturado
- Quer primeiros 10 clientes pagantes
- Vai lançar produto novo (SaaS, curso, ferramenta, etc)

**Não use quando:**
- Você já tem 100+ clientes
- Quer validar ideia (use pesquisa/landing page primeiro)
- Produto é commodity (sem diferencial)

---

## 📅 Linha do Tempo: 6 Semanas

| Semana | Fase | Entrega |
|--------|------|---------|
| 1 | Preparação | Lista de 50 candidatos, página de inscrição |
| 2 | Seleção | 20-30 selecionados, onboarding individual |
| 3-4 | Beta Ativo | Uso real, feedback semanal, ajustes |
| 5 | Validação | NPS, métricas, depoimentos |
| 6 | Decisão | Go/no-go, plano de lançamento público |

---

## 🛠️ Semana 1: Preparação

### Tarefa 1.1: Definir ICP (Ideal Customer Profile)

**Perguntas-chave:**

- Quem tem o problema que seu produto resolve?
- Quem já paga por soluções similares (mesmo que ruins)?
- Quem tem orçamento E urgência?
- Quem pode dar feedback construtivo?

**Template ICP:**

```markdown
## ICP do Beta Fechado

**Demografia:**
- Idade: [faixa]
- Cargo: [ex: gerente, diretor, autônomo]
- Empresa: [porte, setor]
- Renda: [faixa]
- Localização: [cidades/regiões]

**Comportamento:**
- Onde busca informação: [LinkedIn, YouTube, etc]
- Quais ferramentas usa hoje: [concorrentes, planilhas]
- Como toma decisão: [analítica, intuitiva, social]
- Quando precisa de solução: [trigger específico]

**Dor (verbatim de entrevistas):**
- "Eu perco X horas por semana com..."
- "Já tentei Y mas não funcionou porque..."
- "Pagaria R$ Z para resolver isso"

**Solução que busca:**
- Outcome esperado: [resultado mensurável]
- Time-to-value: [quão rápido]
- Esforço: [setup, manutenção]
```

### Tarefa 1.2: Construir Lista de 50 Candidatos

**Fontes:**

1. **Sua rede direta (5-10 pessoas)**
   - Colegas, ex-colegas, amigos que conhece o problema
   - Mensagem: "estou construindo X, pode te mandar?"

2. **Audiência existente (10-15 pessoas)**
   - Lista de email, seguidores, grupo Telegram
   - Mensagem: email segmentado + post orgânico

3. **Comunidades online (15-20 pessoas)**
   - Reddit, Facebook Groups, Slack/Discord
   - Mensagem: post em grupos relevantes (sem spam)

4. **LinkedIn outreach (5-10 pessoas)**
   - Pesquisar cargo + palavra-chave
   - Mensagem: 1ª conexão, 2ª pitch personalizado

5. **Indicação dos candidatos (efeito bola de neve)**
   - "Você conhece alguém que tem esse problema?"

**Meta:** 50 candidatos → 20-30 selecionados.

### Tarefa 1.3: Página de Inscrição

**Crie página simples (Typeform, Tally, Notion, ou site próprio):**

```html
<h1>Beta Fechado: [Nome do Produto]</h1>

<p>Estamos abrindo beta para 20-30 early adopters.
Você terá acesso gratuito + suporte direto por 6 semanas.</p>

<p>Em troca: feedback semanal honesto (15min/semana) + depoimento
se gostar (ou crítica se não gostar).</p>

<h2>Para quem é:</h2>
<ul>
  <li>Você tem [problema específico]</li>
  <li>Já tentou [soluções alternativas] sem sucesso</li>
  <li>Topa dar feedback estruturado</li>
</ul>

<h2>Para quem NÃO é:</h2>
<ul>
  <li>Quem busca solução pronta (use [concorrente X])</li>
  <li>Quem não tem tempo para testar</li>
  <li>Quem espera perfeição</li>
</ul>

<form>
  <label>Nome:</label> <input name="name" required>
  <label>Email:</label> <input name="email" required>
  <label>Empresa (opcional):</label> <input name="company">
  <label>Cargo:</label> <input name="role">
  <label>Qual seu maior problema com [tema]?</label>
  <textarea name="problem" required></textarea>
  <label>Quanto você paga hoje para resolver isso? (R$ 0 = nada)</label>
  <input name="current_spend">
  <button type="submit">QUERO PARTICIPAR DO BETA</button>
</form>
```

### Tarefa 1.4: Mensagem de Convite (Para Sua Rede)

```
Oi [nome]!

Estou abrindo beta fechado de [PRODUTO] — uma ferramenta que
[PROPOSTA DE VALOR].

Preciso de 20-30 early adopters para testar e dar feedback.

O que você ganha:
✅ Acesso gratuito durante 6 semanas
✅ Suporte direto comigo (1:1)
✅ Acesso vitalício se gostar (sem custo)

O que eu peço:
✅ 15min de feedback por semana
✅ Honesto: pode ser negativo
✅ Depoimento em texto/vídeo no final (se aprovar)

Você conhece o problema? (trabalha com [tema]?)

Se sim, posso te mandar o link de inscrição?
Se não, tem alguém na sua rede que conhece?

Valeu!
[Seu nome]
```

---

## ✅ Semana 2: Seleção

### Critérios de Seleção (Matriz)

| Critério | Peso | Score 0-3 |
|----------|------|-----------|
| Tem o problema claramente | 25% | 0=não, 3=sim, desesperado |
| Tem orçamento para pagar | 20% | 0=zero, 3=R$ 100+/mês |
| Tem tempo para testar | 15% | 0=sem tempo, 3=1h+/semana |
| Dá feedback construtivo | 15% | 0=irritadiço, 3=reflexivo |
| Tem rede para indicar | 10% | 0=zero, 3=influenciador |
| É "early adopter" (não conservador) | 10% | 0=conservador, 3=bet-tester |
| Compatibilidade com ICP | 5% | 0=fora, 3=perfeito |

**Score mínimo:** 2.0/3.0 (66%)

**Selecione os 20-30 melhores.**

### Onboarding Individual (30-45 min por bet-tester)

**Script da call:**

```
[0-5 min] Apresentação
"Oi [nome]! Obrigado por aceitar o beta. Vou te dar contexto
do que é o [PRODUTO] e como vai funcionar o beta."

[5-15 min] Demo do produto
"Deixa eu te mostrar como funciona. [WALK THROUGH]"

[15-25 min] Perguntas do bet-tester
"O que achou? O que te deixou confuso? O que você esperava
ver que não viu?"

[25-35 min] Setup
"Vamos configurar pra você agora. [SETUP]"

[35-45 min] Próximos passos
"Por 6 semanas, você vai usar e me dar 15min de feedback
toda [dia]. Combinado?"
```

**Ferramenta para call:** Zoom/Google Meet + Loom (gravar).

**Ferramenta para tracking:** Notion, Airtable, ou planilha simples.

### Setup de Tracking (Planilha)

```markdown
## Beta Tracker

| Nome | Email | Empresa | Start | NPS atual | Última interação | Status |
|------|-------|---------|-------|-----------|-------------------|--------|
| Ana | ana@x.com | X | 15/07 | 8 | 22/07 | Ativo |
| Bruno | bruno@y.com | Y | 15/07 | - | 15/07 | Inativo |
| Carla | carla@z.com | Z | 17/07 | 9 | 22/07 | Ativo |
```

---

## 🔄 Semanas 3-4: Beta Ativo

### Cadência Semanal

**Segunda-feira (você):**
- Enviar email/update: o que mudou essa semana
- Lembrar do feedback de sexta

**Meio da semana:**
- Responder dúvidas de suporte (Slack/WhatsApp/email)

**Sexta-feira (bet-tester):**
- Call ou survey de 15min: como foi a semana?
- Registrar feedback estruturado

### Template de Feedback Semanal

```markdown
## Feedback Semanal · [Nome] · Semana X

**1. Quantas vezes usou o produto essa semana?**
- [ ] 0 (não usei)
- [ ] 1-2 vezes
- [ ] 3-5 vezes
- [ ] Diariamente
- [ ] Mais de 1x/dia

**2. Em uma frase, o que mais gostou?**
[Resposta]

**3. Em uma frase, o que mais frustrou?**
[Resposta]

**4. Conseguiu [outcome esperado]? (sim/não/parcialmente)**
[Resposta]

**5. Se o produto sumisse amanhã, quanto você pagaria para recuperá-lo?**
- [ ] R$ 0
- [ ] R$ 1-50/mês
- [ ] R$ 50-200/mês
- [ ] R$ 200-500/mês
- [ ] R$ 500+/mês

**6. Comentários livres:**
[Resposta]
```

### O que Fazer com o Feedback

**Categorize em planilha:**

| Categoria | Volume | Ação |
|-----------|--------|------|
| **Bug** | X menções | Corrigir imediatamente (crítico) |
| **Feature missing** | X menções | Adicionar ao roadmap (próxima sprint) |
| **UX confuso** | X menções | Redesign (próxima sprint) |
| **Copy/comunicação** | X menções | Ajustar messaging |
| **Positivo** | X menções | Coletar como depoimento |

**Regra:** 3+ bet-testers mencionam a mesma coisa = prioridade alta.

### Suporte em Tempo Real

**Configure canal único (escolha 1):**
- Slack/Discord privado (canal #beta-[nome])
- WhatsApp Business (com etiqueta)
- Email com SLA de 24h
- Intercom (chat no app)

**Responda em < 4h durante horário comercial.**

---

## 📊 Semana 5: Validação

### Métricas-Chave

**Adoção (uso real):**
- DAU/MAU ratio (ideal: > 20%)
- Sessões por usuário/semana (ideal: > 3)
- Tempo médio de sessão (ideal: > 5min)

**Retenção:**
- Retenção D7 (ideal: > 40%)
- Retenção D30 (ideal: > 25%)
- Churn semanal (ideal: < 10%)

**Satisfação:**
- NPS (Net Promoter Score, ideal: > 30)
- CSAT (Customer Satisfaction, ideal: > 4.0/5)
- "Pagaria para continuar?" (% que sim)

**Outcome:**
- % que atingiu o outcome esperado
- Tempo médio para atingir (ideal: < 7 dias)

**Receita (mesmo gratuita, simule):**
- Se cobrarmos R$ X/mês, quem pagaria? (% willing to pay)
- Preço ótimo (testar 3 pontos)

### NPS Survey (Final da Semana 5)

```
"Em uma escala de 0 a 10, o quanto você recomendaria o [PRODUTO]
para um amigo?"

[0-6] Detratores (não recomendam)
[7-8] Neutros
[9-10] Promotores (recomendam ativamente)

NPS = %Promotores - %Detratores

Bons: NPS > 30
Excelente: NPS > 50
Apple, Tesla: NPS 70+
```

**Para cada bet-tester, pergunte também:**
- "Se eu fechar o beta hoje, qual seria sua reação?"
- "O que faria você cancelar a assinatura paga?"
- "Quanto pagaria por isso? R$ X/mês ou R$ Y/ano?"

### Coletar Depoimentos

**Para bet-testers com NPS ≥ 9, peça depoimento:**

```
"Posso gravar um vídeo de 2-3min com você sobre sua experiência
no beta? Vou usar no site/marketing (com sua autorização).

Posso fazer assim:
- O que te fez entrar no beta?
- O que você conseguiu que antes não conseguia?
- Recomendaria pra quem?

Ou se preferir, escreve em texto (3-5 parágrafos)."
```

**Ofereça:** acesso vitalício gratuito + nome nos créditos (se quiser).

---

## 🚦 Semana 6: Decisão

### Framework Go/No-Go

| Sinal | 🟢 GO | 🟡 PIVOT | 🔴 NO-GO |
|-------|--------|----------|----------|
| **NPS** | > 40 | 20-40 | < 20 |
| **DAU/MAU** | > 30% | 15-30% | < 15% |
| **Retenção D7** | > 50% | 30-50% | < 30% |
| **Willingness to pay** | > 60% | 30-60% | < 30% |
| **NPS 9-10** | > 50% | 25-50% | < 25% |
| **Bugs críticos** | 0-2 | 3-5 | > 5 |
| **Outcome atingido** | > 70% | 40-70% | < 40% |

**Se 🟢 GO:** lance publicamente.
**Se 🟡 PIVOT:** ajuste produto, rode novo beta (4 semanas).
**Se 🔴 NO-GO:** encerre, recupere capital, itere ideia.

### Cenários Comuns

**Cenário 1: Produto é incrível, mas ninguém paga**

Sinal: NPS 9, retention alta, mas "pagaria" = 5%

Causa: não entenderam valor OU público não tem budget.

Ação:
- Validar ICP (talvez é hobby, não trabalho)
- Aumentar valor percebido (mostrar $ economizado)
- Reposicionar para público com budget

**Cenário 2: Todos pagariam, mas ninguém usa**

Sinal: "pagaria R$ 500" mas 0 sessões/semana

Causa: produto é "nice to have", não "must have"

Ação:
- Foco em workflows críticos
- Remover features não-essenciais
- Reduzir fricção (1-click onde tem 5 clicks)

**Cenário 3: Usam, mas não conseguem outcome**

Sinal: DAU alto, NPS alto, mas outcome = 20%

Causa: produto não entrega o que promete

Ação:
- Ajustar onboarding para o outcome
- Adicionar guias/templates
- Suporte 1:1 para primeiros 10

---

## 📣 Pós-Beta: Lançamento Público

### Se 🟢 GO

**Semana 7-8: Preparação**
- Landing page de alta conversão
- Email list de espera (do beta + 1.000+)
- Materiais de marketing (blog, vídeo, social)
- Suporte escalado (chat, FAQ)

**Semana 9: Lançamento**
- Anúncio para lista de espera
- Offer de founding member (50% off vitalício para 100 primeiros)
- Press release / Product Hunt
- 5 bet-testers publicam depoimento no dia 1

**Semana 10-12: Escala**
- Paid ads (se houver budget)
- Programa de afiliados
- Webinars semanais
- Otimizar conversão

### Se 🟡 PIVOT

**Repita o beta (4 semanas) com ajustes:**
- 5-10 bet-testers novos (ou os mesmos)
- Foco no outcome (não em features)
- Validação weekly (não monthly)

### Se 🔴 NO-GO

**Aprendizados > Receita:**
- Documente o que aprendeu (CHANGELOG, blog post)
- Pergunte aos bet-testers: "qual produto você pagaria?"
- Pode ser pivot de ideia, não de mercado

---

## 📋 Templates Prontos

### Email de Boas-vindas ao Beta

```
Assunto: Bem-vindo ao Beta do [PRODUTO] 🎉

Oi [nome]!

Você está dentro. Obrigado por aceitar ser um dos [N] early
adopters do [PRODUTO].

📋 O que acontece agora:

1. ACESSO (5min)
   - Link: [URL]
   - Login: [seu email]
   - Senha temporária: [enviada em outro email]

2. ONBOARDING (30min comigo)
   - Agende aqui: [CALENDLY]
   - Vou te mostrar como usar

3. PRIMEIRA SEMANA
   - Use o produto pelo menos 3x
   - Anote o que funcionou e o que não funcionou

4. FEEDBACK SEMANAL (15min, sexta às 14h)
   - Call de 15min toda sexta
   - Pode ser por texto se preferir
   - Sem filtro: seja honesto

5. RECOMPENSA
   - Se completar 6 semanas: acesso vitalício gratuito
   - Se publicar depoimento: seu nome nos créditos
   - Se indicar 3+ pessoas: 1 ano de plano Pro

Qualquer dúvida: [email/WhatsApp]

Vamos lá?
[Seu nome]
```

### Email de Meio de Beta (Semana 3)

```
Assunto: Estamos na metade — e isso mudou

Oi [nome]!

Estamos na semana 3 do beta. Aqui está o que mudou
desde que você entrou:

🔧 Correções:
- [Bug que você reportou] → corrigido
- [UX confuso] → redesign feito
- [Performance] → 2x mais rápido

✨ Features novas:
- [Feature pedida por 3+ bet-testers]
- [Integração com X]

📊 Dados (anonimizados):
- [N] pessoas usando o produto
- [N] sessões/semana em média
- Outcome atingido por [N]% dos bet-testers

🤔 O que falta:
- [Y] dias de uso para o outcome completo
- [Z] feedbacks críticos que ainda não chegaram

Sua contribuição tem sido essencial. Mais 3 semanas
e a gente decide juntos se vira produto público.

Alguma coisa que eu deveria saber?
Responde este email.

[Seu nome]
```

### Email de Finalização (Semana 6)

```
Assunto: Beta encerrando — e agora?

Oi [nome]!

Hoje é o último dia oficial do beta. Antes de qualquer decisão,
quero te contar o que aprendi e perguntar o que você achou.

📊 Resultados do beta:
- [N] bet-testers no total
- [N] terminaram o programa (vs. [N] que saíram)
- NPS: [N] (excelente/bom/regular)
- [N]% atingiu o outcome esperado
- [N]% pagaria para continuar

💎 O que aprendi:
1. [Insight 1]
2. [Insight 2]
3. [Insight 3]

🚀 Próximos passos:
- [Se GO]: lançamento público em [data]
- [Se PIVOT]: novos testes em [prazo]
- [Se NO-GO]: ainda vou validar de outra forma

🎁 Para você, bet-tester:
- Acesso vitalício gratuito (se aplicável)
- Depoimento publicado (se você permitir)
- Reconhecimento nos créditos

🤔 E para mim:
Posso gravar um depoimento de 2-3min com você? Sua história
vai ajudar outros a decidir.

[Link para agendar depoimento]

Obrigado por esses 42 dias. Aprendi mais com você do que
em 6 meses de pesquisa.

[Seu nome]
```

---

## 🎯 Métricas de Sucesso do Beta

| Métrica | Meta | Crítico |
|---------|------|---------|
| **NPS** | > 30 | > 50 |
| **DAU/MAU** | > 25% | > 40% |
| **Retenção D7** | > 50% | > 70% |
| **Outcome atingido** | > 60% | > 80% |
| **Willingness to pay** | > 50% | > 70% |
| **NPS 9-10** | > 40% | > 60% |
| **Depoimentos coletados** | > 10 | > 20 |
| **Bugs críticos** | 0-3 | 0 |

---

## 📚 Materiais Complementares

- `apostilas/35-marketing-conversacional-ia.md` — outreach
- `Lab-Nexus/tools/marketing/01-planejador-editorial.md` — conteúdo
- `playbooks/PB-ONBOARDING-novo-afiliado.md` — onboarding
- `playbooks/PB-LANCAMENTO-lancamento-7-dias.md` — lançamento
- `tutoriais/22-criar-playbook-do-zero.md` — playbooks

---

## 🔗 Links Externos

- ProductHunt Ship: https://www.producthunt.com/ship
- Betalist: https://betalist.com/
- Lenny's Newsletter: https://www.lennysnewsletter.com/
- Reforge: https://www.reforge.com/
- Andreessen Horowitz: https://a16z.com/

---

*AcademIA · PB-PRODUTO · Lançamento Beta Fechado · 2026*
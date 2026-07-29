---
title: "Simulado Oficial #001 · Certificação Nexus Master (CNX)"
description: "Prova simulada avançada para CNX — elite da elite. 12 questões sobre arquitetura, governança, contribuição, mentoria avançada."
tags: [simulado, prova, certificacao, cnx, master, elite, oficial]
simulado_id: CNX-001
total_questoes: 12
duracao_minutos: 50
tempo_por_questao: "~4 min"
nivel: "Master (Elite da Elite)"
pre_requisito: "CEN + CEN+ + Top 5% + 12+ meses + 2 contribuições no core + NDA"
ultima_atualizacao: 2026-07-24
---

# 👑 Simulado Oficial #001 · CNX (Nexus Master)

> **Prova avançada** para certificação de elite. Não testa conhecimento, testa **julgamento arquitetural, estratégico e de governança**. Duração: 50 minutos.

## 📋 Instruções

- ⏱️ **50 minutos** — sem pressa, mas com profundidade
- 📝 **12 questões dissertativas + múltipla escolha** (mix)
- ✅ **Nota mínima**: 9/12 (75%) — rigor CNX
- 📊 **3 blocos** com pesos diferentes
- 🧠 **Justifique respostas** — CNX valoriza raciocínio, não memorização

---

## 🏛️ Bloco 1: Arquitetura Federada e White-label (4 questões, peso 40%)

**Q1.** Você está projetando white-label enterprise para um cliente que atende 50k usuários/dia, 5 países, e exige SLA 99.99%. Justifique em **máximo 4 frases** a escolha de arquitetura: single-tenant silo vs multi-tenant compartilhado vs multi-tenant com schema isolation.

---

**Q2.** Em arquitetura federada de agentes, qual trade-off é MAIS importante considerar para SHO 1M req/s?

- A) Latência vs throughput
- B) Consistência forte vs consistência eventual
- C) Storage vs compute
- D) Custo vs observabilidade
- E) Documentação vs automação

---

**Q3.** Cliente enterprise exige **multi-region active-active**. Qual o principal desafio técnico?

- A) Custo de bandwidth
- B) Conflitos de escrita em banco distribuído e latência de replicação
- C) Quantidade de usuários
- D) Linguagem de programação
- E) Timezone

---

**Q4.** Em arquitetura federada, o que **NÃO** deve ser responsabilidade do agente individual?

- A) Executar sua tarefa específica
- B) Garantir SLA global do sistema
- C) Reportar status ao orquestrador
- D) Manter estado local consistente
- E) Implementar retry logic

---

## ⚖️ Bloco 2: Governança e Decisão Estratégica (4 questões, peso 35%)

**Q5.** Você detecta que um parceiro estratégico está usando práticas que violam LGPD. O impacto financeiro do parceiro é de 30% da receita. O que você faz?

- A) Ignora pelo impacto financeiro
- B) Reporta para time jurídico + notifica parceiro + dá prazo de 60 dias para adequação + plano de contingência
- C) Encerra contrato imediatamente
- D) Reporta à ANPD primeiro
- E) Convida parceiro para workshop

---

**Q6.** Em **Conselho Técnico**, surge proposta de mudar API core (breaking change) para ganhar 10% de performance. A migração afetaria 5k clientes. Sua posição?

- A) Aprovo — performance vale
- B) Reprovo — breaking change é caro; explore otimização sem breaking change primeiro
- C) Adiar para próximo ano
- D) Decidir por votação simples
- E) Pedir mais dados

---

**Q7.** Em decisão de **build vs buy** para novo componente crítico, qual fator é MAIS decisivo?

- A) Custo inicial
- B) Time-to-market vs diferenciação estratégica
- C) Tamanho do time
- D) Preferência do CTO
- E) Última tecnologia hype

---

**Q8.** Em arquitetura de **blueprint** (template reutilizável), o que define qualidade?

- A) Quantidade de features
- B) Reusabilidade, documentação, segurança, observabilidade, testabilidade
- C) Complexidade técnica
- D) Última tecnologia
- E) Número de contribuidores

---

## 🎓 Bloco 3: Mentoria Avançada e Contribuição (4 questões, peso 25%)

**Q9.** Você está mentorando um Estrategista Sênior que está estagnado em R$ 80k/mês há 6 meses. Qual a primeira ação de mentoria?

- A) Dar mais copy de vendas
- B) Diagnosticar causa raiz: é produto? canal? mindset? capacidade técnica?
- C) Aumentar meta
- D) Trocar de nicho
- E) Indicar outro mentor

---

**Q10.** Em **code review de contribuição para o core**, qual é o critério MAIS importante?

- A) Performance pura
- B) Alinhamento com visão arquitetural, manutenibilidade, e compatibilidade backward
- C) Tamanho do diff (menor melhor)
- D) Autor (senior > junior)
- E) Velocidade de merge

---

**Q11.** Ao **ensinar conceito complexo** (ex: arquitetura federada) para audiencia mista (junior + senior), qual abordagem?

- A) Linguagem técnica pura — senior entende
- B) Metáfora do dia-a-dia + analogia + exemplo prático + profundidade gradual
- C) Slide cheio de código
- D) Pular para o avançado
- E) Ler paper acadêmico

---

**Q12.** Você identifica que seu mentorado está **acima do seu nível de mentoria** em algumas dimensões. O que faz?

- A) Esconde e finge que sabe
- B) Reconhece, conecta com mentor mais sênior naquela dimensão, e aprende com o mentorado (peer learning)
- C) Encerra mentoria
- D) Indica outro mentorado mais fácil
- E) Aumenta seu preço

---

# ✅ GABARITO COMENTADO

> **Atenção: CNX avalia raciocínio mais que resposta certa. Respostas com justificativa sólida podem ter nuance.**

---

## Bloco 1: Arquitetura

**Q1. Resposta modelo (4 frases):**
"Para 50k usuários/dia em 5 países com SLA 99.99%, recomendo **single-tenant silo** com banco dedicado por região. Justificativa: (1) isolamento total elimina 'noisy neighbor' crítico para SLA enterprise; (2) compliance regional (GDPR, LGPD) é mais simples com dados em jurisdição; (3) disaster recovery regional é direto; (4) custo é 2-3x multi-tenant, mas cliente enterprise paga o premium. Trade-off aceito: complexidade operacional maior, justificada pelo contrato."
💡 *Variantes aceitáveis: multi-tenant com schema isolation é aceitável se cliente aceita menor SLA. Pontuação: 4 critérios (isolamento, compliance, recovery, custo) bem justificados.*

**Q2. Resposta: B)** Consistência forte vs eventual.
💡 *CAP theorem: em sistema distribuído, você escolhe 2 entre Consistency, Availability, Partition tolerance. Para federação 1M req/s, Partition tolerance é obrigatória (rede falha). Escolha entre C forte (latência alta) e A alto (consistência eventual). Outros são trade-offs secundários.*

**Q3. Resposta: B)** Conflitos de escrita e latência de replicação.
💡 *Active-active multi-region tem dois problemas técnicos: conflitos quando duas regiões editam mesmo registro (last-write-wins pode perder dados), e replicação síncrona cross-region tem latência de 100-500ms. Solução: design por region (writes vão para region primária, reads de qualquer).*

**Q4. Resposta: B)** Garantir SLA global.
💡 *SLA global é responsabilidade do **orquestrador/orquestração federada**, não do agente individual. Agente cuida de: tarefa, status, retry, estado local. SLA, balanceamento, failover são do orquestrador.*

---

## Bloco 2: Governança

**Q5. Resposta: B)** Reportar jurídico + plano 60d + contingência.
💡 *A (ignorar) = cumplicidade. C (encerrar imediato) = reativo, gera litígio. D (ANPD primeiro) = pular etapa interna. B é workflow completo: detectar → reportar → prazo → plano B.*

**Q6. Resposta: B)** Reprovar, explorar otimização não-breaking.
💡 *10% performance raramente justifica quebrar 5k clientes. Otimização sem breaking: índices, cache, query rewriting, paralelismo. CNX é sobre trade-offs de longo prazo, não ganho tático.*

**Q7. Resposta: B)** Time-to-market vs diferenciação estratégica.
💡 *Regra: se componente NÃO é diferencial competitivo, BUY. Se É diferencial, BUILD. Custo inicial (A) é distrator. Preferência pessoal (D) é ruído. Hype (E) é armadilha.*

**Q8. Resposta: B)** 5 dimensões: reusabilidade, doc, segurança, observabilidade, testabilidade.
💡 *Blueprint é asset reutilizável. Sem essas 5 qualidades, vira código legado em 6 meses. Features (A) é vaidade. Complexidade (C) é anti-pattern.*

---

## Bloco 3: Mentoria

**Q9. Resposta: B)** Diagnosticar causa raiz.
💡 *Estagnação é sintoma. Pode ser: capacidade técnica (precisa aprender), mindset (medo de escalar), oferta (produto saturado), canal (exaustão), operacional (burnout). Copy (A) trata sintoma. Aumentar meta (C) gera mais pressão. Trocar de nicho (D) é fuga.*

**Q10. Resposta: B)** Alinhamento + manutenibilidade + compatibilidade.
💡 *Core code é compartilhado por 5k+ clientes. Mudança tem externalidades. Performance (A) raramente vale o risco. Diff menor (C) é vaidade. Velocidade (E) é pressão ruim.*

**Q11. Resposta: B)** Metáfora + analogia + exemplo + profundidade gradual.
💡 *Pedagogia universal: concrete → abstract, simple → complex. Metáfora ancora conceito. Exemplo solidifica. Senior aprofunda, junior fica no exemplo. Pure code (C) aliena junior. Pure paper (E) aliena todos.*

**Q12. Resposta: B)** Reconhece + conecta + peer learning.
💡 *Mentor sênior sabe o que sabe e o que NÃO sabe. Esconder (A) é antiético e gera relação fraca. Encerrar (C) é abandono. Peer learning (B) é o mindset de crescimento + inteligência emocional.*

---

# 📊 Cálculo da Nota

| Acertos | Nota (%) | Status |
|---|---|---|
| 11-12 | 92-100% | 🏆 **MASTER CONFIRMADO** — Pronto para CNX oficial |
| 9-10 | 75-83% | ✅ **APROVADO** — CNX obtida |
| 7-8 | 58-67% | ⚠️ **BORDERLINE** — Discussão com Conselho Técnico |
| 0-6 | 0-50% | ❌ **REPROVADO** — 6 meses de contribuição antes de tentar |

---

# 📚 Material de Estudo

## Documentação Estratégica
- `governanca/C-SUITE-AI.md` — Governança executiva
- `governanca/PB-GOVERN-postmortem-blame-free.md`
- `governanca/RATIFICACAO-LOOP-M4-M5-M7.md`
- `producao/INCIDENT-RESPONSE-RUNBOOK.md`

## Cursos Master + Elite
- `cursos/master/` (todos, incluindo versões estendidas Mavis)
- `cursos/elite/` (todos)

## Documentação Técnica
- `certificacoes/CNX-certificacao-nexus-master.md`
- `tutoriais/` (todos os numerados)

## Contribuições Esperadas
- 2 PRs mergeados no core (blueprints, skills, runbooks)
- 1 ano de operação ativa com SLA cumprido

---

# 🎓 Próximos Passos

1. **Se aprovado (≥75%)**: agendar mentoria final com membro do Conselho Técnico
2. **Se reprovado (<75%)**: contribuir com 2 PRs no core + tentar novamente em 6 meses
3. **Após CNX**: acesso à governança técnica + co-autoria de blueprints + voto no Conselho

---

**Simulado criado em 2026-07-24** · Mavis Agent
**Versão 1.0** · Mantido em `certificacoes/simulado-cnx-001.md`

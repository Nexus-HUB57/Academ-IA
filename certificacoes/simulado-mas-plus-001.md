---
title: "Simulado Oficial #001 · Certificação Master Plus Nexus (MAS+)"
description: "Prova simulada cronometrada com 15 questões avançadas de A/B test, coortes, Judge, mentoria."
tags: [simulado, prova, certificacao, mas-plus, master-plus, oficial]
simulado_id: MAS-PLUS-001
total_questoes: 15
duracao_minutos: 40
tempo_por_questao: "~2.7 min"
nivel: "Master Plus"
pre_requisito: "Certificação CEN aprovada + Top 25% da rede"
ultima_atualizacao: 2026-07-24
---

# 🎯 Simulado Oficial #001 · MAS+ (Master Plus)

> **Prova cronometrada** avançada para validação de expertise em A/B test, coortes, Judge e mentoria. Duração: 40 minutos.

## 📋 Instruções

- ⏱️ **40 minutos** — rigor de tempo
- 📝 **15 questões** de múltipla escolha (A, B, C, D, E)
- ✅ **Nota mínima para aprovação**: 11/15 (73%)
- 📊 **3 blocos** com pesos diferentes
- 🚫 **Material não permitido** durante o simulado

---

## 📊 Bloco 1: A/B Testing Estatisticamente Válido (5 questões, peso 35%)

**Q1.** Em A/B test com baseline conversion de 5%, lift mínimo detectável de 10%, e poder estatístico de 80%, o **tamanho mínimo de amostra** por variação é aproximadamente:

- A) 500
- B) 5.000
- C) 15.000-20.000
- D) 100.000
- E) 1.000.000

---

**Q2.** Você roda um A/B test por 3 dias. Variação B está com p=0.03 (significativo). O que você faz?

- A) Para o teste e declara B vencedor
- B) Continua o teste até completar 14 dias (duração mínima) e re-analisa
- C) Espera mais 1 dia só para confirmar
- D) Implementa B em 50% do tráfego
- E) Faz 10 testes em paralelo para validar

---

**Q3.** **Multiple testing problem** em A/B test significa:

- A) Testar mais de uma coisa por vez
- B) Quando você testa múltiplas métricas, aumenta chance de falso positivo em pelo menos uma
- C) Testar com múltiplas audiências
- D) Ter múltiplas variações
- E) Testar em múltiplos países

---

**Q4.** **Sequential testing** (olhar resultados diariamente) sem correção de alpha:

- A) É prática recomendada
- B) Infla taxa de falso positivo drasticamente (peek problem)
- C) Reduz tempo de teste
- D) Aumenta poder estatístico
- E) Não tem impacto

---

**Q5.** **Effect size** em A/B test é:

- A) p-value
- B) Magnitude prática da diferença (ex: Cohen's d, lift %), não significância estatística
- C) Tamanho da amostra
- D) Duração do teste
- E) Número de variações

---

## 📈 Bloco 2: Análise de Coortes e Retenção (5 questões, peso 35%)

**Q6.** Em tabela de coortes, a diagonal principal mostra:

- A) Receita por cohort
- B) Retenção no mês 0 (sempre 100%)
- C) Tamanho inicial do cohort
- D) Canal de aquisição
- E) LTV

---

**Q7.** Você tem 3 cohorts (jan, fev, mar) e a retenção em M+3 é: 60%, 50%, 40%. O que isso indica?

- A) Sazonalidade positiva (cohorts melhorando)
- B) Degradação (cohorts perdendo retenção)
- C) Sem tendência
- D) Erro de cálculo
- E) Sucesso do produto

---

**Q8.** **Smoke testing** em análise de cohort significa:

- A) Testar fumaça na plataforma
- B) Validar dados com uma pequena amostra antes de análise completa
- C) Análise rápida de cohort inicial
- D) Burnout test
- E) Penetration test

---

**Q9.** **Survival analysis** é usada para:

- A) Calcular churn rate
- B) Modelar tempo até um evento (churn, conversão, morte) considerando dados censurados
- C) Prever receita futura
- D) Segmentar usuários
- E) Calcular NPS

---

**Q10.** Em coortes, **Nth percentile retention** (ex: P50, P25) é útil porque:

- A) Mostra retenção média, mas a média pode mascarar variabilidade
- B) Mostra variabilidade — P50 é mediana, P25 mostra cauda longa
- C) É mais fácil de calcular
- D) Substitui o cálculo de churn
- E) Não tem utilidade

---

## ⚙️ Bloco 3: Judge Tuning e Mentoria Estruturada (5 questões, peso 30%)

**Q11.** Em **Judge tuning**, qual técnica reduz **falsos negativos** (rejeitar sugestão boa)?

- A) Aumentar threshold de risco
- B) Adicionar mais exemplos positivos no prompt (few-shot)
- C) Reduzir temperatura para 0
- D) Trocar para modelo menor
- E) Bloquear mais categorias

---

**Q12.** **LLM-as-judge** com **panel de modelos** (3+ modelos votando) reduz:

- A) Custo
- B) Latência
- C) Viés individual de um único modelo
- D) Throughput
- E) Tamanho do dataset

---

**Q13.** Em **mentoria estruturada**, o framework **GROW** significa:

- A) Grow, Reflect, Optimize, Win
- B) Goal, Reality, Options, Will (objetivo, realidade, opções, vontade)
- C) Get, Retain, Optimize, Win
- D) Go, Review, Output, Wrap
- E) General, Real, Open, Wise

---

**Q14.** **Calibration session** em mentoria é:

- A) Sessão de feedback onde mentorado avalia mentor
- B) Sessão onde mentorado pratica habilidade e recebe feedback objetivo
- C) Setup de equipamento
- D) Reunião de equipe
- E) Treinamento técnico

---

**Q15.** **Mentor saturation point** é:

- A) Quando mentorado desiste
- B) Quando mentor não consegue mais agregar valor significativo ao mentorado
- C) Quando mentorado vira mentor
- D) Carga horária máxima
- E) Limite de mentorados

---

# ✅ GABARITO COMENTADO

---

## Bloco 1: A/B Test

**Q1. Resposta: C)** 15.000-20.000.
💡 *Cálculo: para detectar lift de 10% com baseline 5%, precisa de ~30k-40k total (15-20k por variação). Use calculadora: https://www.optimizely.com/sample-size-calculator/.*

**Q2. Resposta: B)** Continua até 14 dias.
💡 *3 dias é cedo demais — pode ter capturado efeito novidade, sazonalidade semanal, ou dia da semana. Duração mínima recomendada: 1-2 ciclos de negócio (7-14 dias). E (parar cedo) é o viés clássico de "peeking".*

**Q3. Resposta: B)** Múltiplas métricas = múltiplos testes = infla FPR.
💡 *Se testa 5 métricas com alpha=0.05, probabilidade de pelo menos um falso positivo = 1-(0.95^5) = 23%. Correção: Bonferroni (alpha/n) ou FDR (Benjamini-Hochberg).*

**Q4. Resposta: B)** Infla falso positivo drasticamente.
💡 *Peek problem: cada "olhada" nos dados é um teste implícito. Após 10 peeks sem correção, FPR pode passar de 30%. Solução: sequential testing (mSPRT, always-valid inference) ou testes pré-planejados.*

**Q5. Resposta: B)** Magnitude prática da diferença.
💡 *Effect size (Cohen's d, lift %) é diferente de significância (p). Com n=1M, lift de 0.1% é "significativo" mas irrelevante na prática. Reporte sempre os dois.*

---

## Bloco 2: Coortes

**Q6. Resposta: B)** Retenção em M+0 = 100% (por definição).
💡 *Diagonal principal: cohort jan no mês 0 = 100%, cohort fev no mês 0 = 100%, etc. É trivial. O interessante está fora da diagonal (M+1, M+2, M+3...).*

**Q7. Resposta: B)** Degradação.
💡 *60% > 50% > 40% mostra queda mês a mês. Possíveis causas: degradação de qualidade de lead (volume > qualidade), mudança de mercado, sazonalidade, problema de onboarding.*

**Q8. Resposta: B)** Validar com pequena amostra.
💡 *Smoke test em dados: rodar análise em 100 usuários antes de rodar em 1M. Detecta bugs de query, schema errado, dados faltantes, antes de investir tempo em análise completa.*

**Q9. Resposta: B)** Modelar tempo até evento.
💡 *Survival analysis (Kaplan-Meier, Cox regression) lida com censuring (clientes ativos = "ainda não aconteceu"). Simples churn rate ignora censuring, gera viés.*

**Q10. Resposta: B)** Mostra variabilidade.
💡 *Média mascara. P50 (mediana) é onde metade dos clientes está. P25 mostra os 25% piores — são churns em risco, alvo de ação. P75 mostra power users.*

---

## Bloco 3: Judge + Mentoria

**Q11. Resposta: B)** Few-shot positivos.
💡 *Threshold alto (A) aumenta FN ainda mais. Temperatura 0 (C) reduz variabilidade mas não aumenta aprovação. Few-shot ensina o Judge com exemplos concretos de "isso é OK".*

**Q12. Resposta: C)** Viés individual.
💡 *Cada modelo (GPT-4o, Claude, Gemini) tem blindspots. Painel de 3+ modelos votando reduz viés individual, gera decisão mais robusta. Custo (A) e latência (B) aumentam, trade-off necessário.*

**Q13. Resposta: B)** Goal, Reality, Options, Will.
💡 *GROW é framework clássico de coaching (1980s). Goal = o que quer. Reality = onde está. Options = opções. Will = ação comprometida. Outros: SMART, OKR, são frameworks de metas.*

**Q14. Resposta: B)** Prática + feedback objetivo.
💡 *Calibration = prática deliberada. Mentorado apresenta, mentor dá feedback estruturado. Usado em vendas, apresentações, código review. Não é avaliação (A) nem reunião (D).*

**Q15. Resposta: B)** Limite de agregação de valor.
💡 *Todo mentor atinge ponto de saturação para um mentorado específico — quando crescimento desacelera. Solução: rotação de mentores, ou elevar mentorado a peer. Não é desistencia (A).*

---

# 📊 Cálculo da Nota

| Acertos | Nota (%) | Status |
|---|---|---|
| 14-15 | 93-100% | 🏆 **ELITE MASTER+** — Nível top 10% |
| 11-13 | 73-87% | ✅ **APROVADO** — Certificação MAS+ obtida |
| 8-10 | 53-67% | ⚠️ **BORDERLINE** — Revisão + 2ª tentativa |
| 0-7 | 0-47% | ❌ **REPROVADO** — Estude 2 meses antes de tentar |

---

# 📚 Material de Estudo

## Cursos
- `cursos/master/02-ab-test-judge.md` (e versão estendida)
- `cursos/master/03-coortes-churn.md`
- `cursos/master/00-otimizacao-conversao.md`

## Tutoriais
- `tutoriais/08-primeiro-ab-test.md`
- `tutoriais/09-ler-tabela-coorte.md`
- `tutoriais/21-monitorar-metricas-tempo-real.md`

## Documentação
- `certificacoes/MAS-plus-certificacao-master-plus.md`
- `certificacoes/banco-questoes-cen.md` (60 questões avançadas)

---

# 🎓 Próximos Passos

1. **Se aprovado (≥73%)**: agendar prova oficial MAS+ (R$ 4.997, 60 dias de duração)
2. **Se reprovado (<73%)**: rodar sprint de 30 dias em A/B test + cohort analysis
3. **Após MAS+**: aplicar para CNX (Master) após 12 meses + top 5% da rede

---

**Simulado criado em 2026-07-24** · Mavis Agent
**Versão 1.0** · Mantido em `certificacoes/simulado-mas-plus-001.md`

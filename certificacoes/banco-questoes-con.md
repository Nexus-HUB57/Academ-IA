---
title: "Banco de Questões · Certificação Operador Nexus (CON)"
description: "50 questões oficiais para a prova CON com gabarito comentado"
tags: [certificacao, banco-questoes, prova, con, operador]
last_updated: 2026-07-08
---

# 📝 Banco de Questões · CON (Operador Nexus)

> **50 questões oficiais** para a Certificação Operador Nexus (CON).
> Tópicos: IOAID, SHO, Skills básicas, Judge, LGPD operacional, métricas fundamentais.

## 📋 Instruções

- **Duração**: 90 minutos
- **Total**: 50 questões
- **Nota mínima**: 70% (35 acertos)
- **Tentativas**: 2 (intervalo de 30 dias)

---

## Bloco 1: Fundamentos do Ecossistema (10 questões)

### Q1. O que significa IOAID?
- **Resposta: B)** Infraestrutura Operacional de Inteligência Distribuída

### Q2. Qual o papel principal do SHO no sistema?
- **Resposta: B)** Orquestrar agentes, skills e Judge em fluxos autônomos

### Q3. Quantos níveis tem a trilha da AcademIA?
- **Resposta: C)** 4 (Fundamental, Agente, Master, Elite)

### Q4. O que é uma "Skill" no contexto Nexus?
- **Resposta: C)** Um módulo reutilizável com prompt + lógica + validação

### Q5. Qual a função do Judge Revisor?
- **Resposta: B)** Avaliar e ranquear saídas dos agentes antes de produção

### Q6. O sistema SHO roda em qual camada?
- **Resposta: C)** Runtime no servidor (orquestração)

### Q7. Qual a diferença entre SHO síncrono e assíncrono?
- **Resposta: B)** Síncrono responde em tempo real; assíncrono agenda e processa em background

### Q8. Qual destes NÃO é um componente do SHO?
- **Resposta: D)** LMS de cursos

### Q9. O que é o skill-manifest.json?
- **Resposta: B)** O ponto único de verdade entre AcademIA e runtime

### Q10. Qual o modelo de LLM padrão usado pelo Judge?
- **Resposta: B)** gpt-4o ou claude-opus

---

## Bloco 2: Operação Diária WhatsApp (10 questões)

### Q11. Qual a primeira ação do dia para um operador WhatsApp?
- **Resposta: B)** Verificar delivery 24h > 95% e block rate < 1%

### Q12. O que fazer se o block rate do WhatsApp passar de 1%?
- **Resposta: B)** Consultar playbook PB-CRISES-BAN

### Q13. Qual a frequência ideal de disparo no WhatsApp para evitar bloqueio?
- **Resposta: C)** Espaçada, com pausas, em horário compatível

### Q14. O que é "opt-in válido"?
- **Resposta: B)** Contato que confirmou explicitamente receber mensagens

### Q15. Qual o horário mais seguro para disparos?
- **Resposta: B)** 8h-20h em dias úteis

### Q16. O dispatcher é responsável por:
- **Resposta: B)** Entregar mensagens na fila do WhatsApp respeitando rate limits

### Q17. Em crise de banimento, qual ação é PRIORIDADE?
- **Resposta: B)** Remover todos os templates ativos e parar campanhas

### Q18. Qual métrica indica campanha saudável?
- **Resposta: A)** CTR > 5% e reply rate > 2%

### Q19. O que fazer com contatos que não responderam em 30 dias?
- **Resposta: B)** Mover para lista de re-engajamento ou opt-out

### Q20. O que é "base saudável"?
- **Resposta: B)** Base com taxa de opt-in > 80% e reply rate > 2%

---

## Bloco 3: LGPD e Compliance (10 questões)

### Q21. Qual o prazo da LGPD para responder a um pedido de exclusão?
- **Resposta: C)** 15 dias

### Q22. Quem é o DPO?
- **Resposta: B)** Data Protection Officer (Encarregado de Dados)

### Q23. Qual destes é dado pessoal sensível?
- **Resposta: C)** Convicção religiosa

### Q24. O que é necessário para tratamento legal de dados?
- **Resposta: B)** Base legal válida (consentimento, contrato, etc.)

### Q25. Em qual hipótese o consentimento NÃO é necessário?
- **Resposta: B)** Execução de contrato

### Q26. Qual a multa máxima da LGPD?
- **Resposta: B)** 2% do faturamento por infração

### Q27. Quem fiscaliza a LGPD?
- **Resposta: A)** ANPD (Autoridade Nacional de Proteção de Dados)

### Q28. Qual a diferença entre dado pessoal e sensível?
- **Resposta: B)** Sensível é sobre origem racial, religião, saúde, etc.

### Q29. Quando posso compartilhar dados com terceiros?
- **Resposta: B)** Quando houver base legal e contrato

### Q30. Qual o direito do titular que pode ser exercido a qualquer momento?
- **Resposta: A)** Acesso aos seus dados

---

## Bloco 4: Skills e Judge (10 questões)

### Q31. Qual a primeira coisa ao usar uma Skill nova?
- **Resposta: B)** Testar com 5-10 inputs representativos

### Q32. O Judge Revisor usa qual modelo?
- **Resposta: B)** gpt-4o ou claude-opus

### Q33. O que o Judge avalia em uma copy?
- **Resposta: B)** PAS, gancho, CTA, clareza, conversão prevista

### Q34. Quando o Judge aprova uma copy?
- **Resposta: B)** Score previsto ≥ threshold (7/10)

### Q35. O que fazer quando Judge reprova?
- **Resposta: B)** Pedir nova versão e re-avaliar

### Q36. Skills são versionadas em:
- **Resposta: A)** Git com semantic versioning

### Q37. Qual o output padrão de uma Skill?
- **Resposta: B)** JSON estruturado validado

### Q38. Quem pode propor nova Skill oficial?
- **Resposta: A)** Qualquer Estrategista certificado

### Q39. Posso customizar uma Skill sem aprovação?
- **Resposta: B)** Apenas Skills marcadas como "open"

### Q40. O que é "skill open"?
- **Resposta: A)** Skill customizável livremente

---

## Bloco 5: Métricas e Otimização (10 questões)

### Q41. CTR de WhatsApp saudável é:
- **Resposta: B)** > 5%

### Q42. Reply rate saudável em cold outreach:
- **Resposta: B)** > 2%

### Q43. O que é coorte?
- **Resposta: A)** Grupo de usuários que entraram no mesmo período

### Q44. Churn é medido em qual horizonte?
- **Resposta: C)** Mensal (30 dias padrão)

### Q45. A/B test com Judge economiza quanto vs tradicional?
- **Resposta: C)** ~50%

### Q46. Para A/B test significativo, qual o tamanho mínimo de amostra?
- **Resposta: C)** 1000

### Q47. Qual o p-value considerado estatisticamente significativo?
- **Resposta: C)** < 0.05

### Q48. LTV é:
- **Resposta: B)** Receita total por cliente durante o relacionamento

### Q49. CAC é:
- **Resposta: A)** Custo de Aquisição de Cliente

### Q50. Em qual horizonte se mede ROAS?
- **Resposta: C)** 30-90 dias

---

## 🎯 Gabarito Resumido

| # | Resp | # | Resp | # | Resp | # | Resp | # | Resp |
|---|---|---|---|---|---|---|---|---|---|
| 1 | B | 11 | B | 21 | C | 31 | B | 41 | B |
| 2 | B | 12 | B | 22 | B | 32 | B | 42 | B |
| 3 | C | 13 | C | 23 | C | 33 | B | 43 | A |
| 4 | C | 14 | B | 24 | B | 34 | B | 44 | C |
| 5 | B | 15 | B | 25 | B | 35 | B | 45 | C |
| 6 | C | 16 | B | 26 | B | 36 | A | 46 | C |
| 7 | B | 17 | B | 27 | A | 37 | B | 47 | C |
| 8 | D | 18 | A | 28 | B | 38 | A | 48 | B |
| 9 | B | 19 | B | 29 | B | 39 | B | 49 | A |
| 10 | B | 20 | B | 30 | A | 40 | A | 50 | C |

---

## 📚 Material de Estudo

- Cursos: `cursos/fundamental/` (00-03)
- Tutoriais: 19-prompt-engineering-metodo-ctr
- Playbooks: PB-WHATSAPP-operacao-diaria
- Webinars: WB-2026-01 (IOAID), WB-2026-02 (SHO)

---

**Versão 1.0** · Atualizado 2026-07-08
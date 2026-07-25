---
title: "Simulado Oficial #001 · Certificação Elite Nexus (CEN+)"
description: "Prova simulada cronometrada com 20 questões do banco CEN+. Gabarito comentado ao final."
tags: [simulado, prova, certificacao, cen-plus, elite, oficial]
simulado_id: CEN-PLUS-001
total_questoes: 20
duracao_minutos: 60
tempo_por_questao: "3 min"
nivel: "Elite"
pre_requisito: "Certificação CEN aprovada + Trilha Master completa + 2 projetos"
banco_origem: "certificacoes/banco-questoes-cen-plus.md"
ultima_atualizacao: 2026-07-24
---

# 🎯 Simulado Oficial #001 · CEN+ (Elite Nexus)

> **Prova cronometrada** para o nível mais alto. Duração: 60 minutos. Questões avançadas de federação, multi-tenant, segurança enterprise, arquitetura, e estratégia.

## 📋 Instruções Importantes

- ⏱️ **Cronômetro de 60 minutos** — pressão de tempo real
- 📝 **20 questões de múltipla escolha** (A, B, C, D, E)
- ✅ **Nota mínima para aprovação**: 15/20 (75%) — Elite é mais rigoroso
- 📊 **Distribuição**: 4 questões × 5 blocos avançados
- 🚫 **Não consultar material** durante o simulado
- 💡 **Marque respostas** antes de ver gabarito

---

## 🌐 Bloco 1: Federação de Agentes (4 questões)

**Q1.** **Federação de agentes** no SHO significa:

- A) Múltiplos afiliados em uma rede
- B) Múltiplos agentes autônomos coordenando via protocolo comum para resolver tarefas complexas
- C) Sistema de pagamento distribuído
- D) Banco de dados replicado
- E) Versão do SHO com mais features

---

**Q2.** Em arquitetura federada, qual o **principal desafio técnico**?

- A) Latência
- B) Coordenação de estado, consistência eventual, e resiliência a falhas parciais
- C) Custo de GPU
- D) Tamanho do banco
- E) Quantidade de usuários

---

**Q3.** Protocolo de comunicação entre agentes federados mais usado em 2026:

- A) HTTP REST
- B) gRPC + Message Queue (Kafka, RabbitMQ)
- C) FTP
- D) Email
- E) WebSocket apenas

---

**Q4.** Quando **NÃO** usar federação:

- A) Tarefas simples lineares
- B) Quando um único agente resolve bem o problema
- C) Sistemas legados sem modernização
- D) Todas as alternativas acima

---

## 🏢 Bloco 2: Multi-tenant e White-label (4 questões)

**Q5.** Em arquitetura **multi-tenant**, o que é fundamental isolar?

- A) Apenas interface visual
- B) Dados, configuração, performance, e compliance por tenant
- C) Apenas dados
- D) Apenas billing
- E) Nada, multi-tenant compartilha tudo

---

**Q6.** **White-label** no contexto Nexus significa:

- A) Marca da Nexus aparece em tudo
- B) Afiliado/empresa pode rebranciar plataforma com sua marca própria
- C) Produto é grátis
- D) Versão beta
- E) Apenas para empresas grandes

---

**Q7.** Qual modelo de **isolamento de dados** é mais seguro em multi-tenant?

- A) Single database, schema compartilhado
- B) Single database, schema por tenant
- C) Database por tenant (silo)
- D) Não importa
- E) Compartilhado total

---

**Q8.** **Tenant onboarding** no SHO inclui:

- A) Criar conta, configurar domínio, provisionar banco, configurar Judge específico, deploy
- B) Apenas criar login
- C) Apenas enviar email
- D) Apenas configurar DNS
- E) Apenas billing

---

## 🛡️ Bloco 3: Segurança Enterprise (4 questões)

**Q9.** Em segurança enterprise, o princípio de **defense in depth** significa:

- A) Uma única barreira forte
- B) Múltiplas camadas de segurança independentes (rede, app, dados, auth, audit)
- C) Apenas criptografia
- D) Apenas firewall
- E) Apenas autenticação forte

---

**Q10.** **SSO (Single Sign-On)** enterprise geralmente usa qual protocolo?

- A) FTP
- B) SAML 2.0 ou OpenID Connect (OIDC)
- C) SMTP
- D) HTTP básico
- E) Apenas login/senha próprio

---

**Q11.** **SOC 2** é:

- A) Software de gestão
- B) Certificação de segurança e disponibilidade de fornecedores SaaS
- C) Linguagem de programação
- D) Banco de dados
- E) Sistema operacional

---

**Q12.** **Audit log** em produção enterprise DEVE conter:

- A) Apenas login
- B) Quem fez, o quê, quando, de onde, com contexto mínimo (sem PII)
- C) Tudo, incluindo senhas em texto claro
- D) Apenas falhas
- E) Apenas ações admin

---

## 🏗️ Bloco 4: Arquitetura Avançada e Performance (4 questões)

**Q13.** Para **escalar** SHO para 1M req/s, a arquitetura mais adequada é:

- A) Single server beefy
- B) Microserviços com Kubernetes, load balancer, cache distribuído, async processing
- C) Single server com mais RAM
- D) Não escala
- E) Apenas CDN

---

**Q14.** **Cache hit rate** ideal para SHO API gateway:

- A) 0-20%
- B) 30-50%
- C) 60-90% (com TTL apropriado)
- D) 100%
- E) 0% é ideal

---

**Q15.** **Database connection pooling** resolve qual problema?

- A) Backup
- B) Latência de abertura de conexão + esgotamento de conexões sob alta concorrência
- C) Replicação
- D) Apenas leitura
- E) Apenas escrita

---

**Q16.** **Observabilidade** completa em produção enterprise usa:

- A) Apenas logs
- B) Logs + Métricas + Traces (tríade) com correlação
- C) Apenas métricas
- D) Apenas traces
- E) Apenas alertas

---

## 🚀 Bloco 5: Estratégia de Produto e Go-to-Market (4 questões)

**Q17.** Em **go-to-market** B2B, o **ICP (Ideal Customer Profile)** define:

- A) Preço ideal
- B) Perfil detalhado do cliente ideal: setor, porte, dor, decisor, budget, timeline
- C) Apenas idade
- D) Apenas localização
- E) Apenas cargo

---

**Q18.** **Product-market fit** é atingido quando:

- A) Produto está pronto
- B) Usuários valorizam tanto que indicariam para outros (organic growth > paid growth)
- C) Receita > custos
- D) Tem 1000 usuários
- E) Está no ar

---

**Q19.** **North Star Metric** para SaaS B2B é tipicamente:

- A) Signups
- B) Engajamento de valor (ex: ações de valor por usuário/semana)
- C) Apenas MRR
- D) Apenas NPS
- E) Apenas pageviews

---

**Q20.** Em **pricing strategy**, modelo **value-based pricing** significa:

- A) Preço mais baixo possível
- B) Preço baseado no valor percebido pelo cliente, não no custo
- C) Preço = custo + margem fixa
- D) Preço aleatório
- E) Preço = concorrente

---

# ✅ GABARITO COMENTADO

> **Role para baixo apenas após completar todas as 20 questões.**

---

## Bloco 1: Federação

**Q1. Resposta: B)** Múltiplos agentes coordenando via protocolo comum.
💡 *Federação = coordenação distribuída. A (rede de afiliados) é marketing, não técnica. C, D são infra, não agentes. E é feature flag.*

**Q2. Resposta: B)** Coordenação de estado, consistência eventual, resiliência.
💡 *Tríade clássica de sistemas distribuídos: CAP theorem. Latência (A) é problema mas não principal. C, D, E são secundários.*

**Q3. Resposta: B)** gRPC + Message Queue.
💡 *REST (A) é lento para alta freq. WebSocket (E) só é para real-time. gRPC binário + Kafka/RabbitMQ é o padrão para federação de agentes em 2026.*

**Q4. Resposta: D)** Todas as alternativas.
💡 *Federação adiciona complexidade. Para tarefas simples (A, B) e sistemas legados (C), não vale. Use apenas quando ganho > complexidade.*

---

## Bloco 2: Multi-tenant

**Q5. Resposta: B)** Dados, config, performance, compliance.
💡 *Isolamento multi-camada. Apenas dados (C) é insuficiente. Tudo compartilhado (E) é single-tenant mal feito. Performance isolation evita "noisy neighbor".*

**Q6. Resposta: B)** Rebranding completo pelo afiliado.
💡 *White-label = o cliente coloca sua marca. A (marca Nexus) é o oposto. C, D, E são irrelevantes.*

**Q7. Resposta: C)** Database por tenant (silo).
💡 *Mais seguro, mais caro. A é barato mas menos seguro. B é meio-termo. Para enterprise regulated (saúde, financeiro), silo é obrigatório. SaaS de pequeno porte usa A.*

**Q8. Resposta: A)** Onboarding completo.
💡 *Onboarding enterprise é complexo: account, domínio, DB, Judge config, deploy automatizado, SSO. B-E são apenas uma fatia.*

---

## Bloco 3: Segurança

**Q9. Resposta: B)** Múltiplas camadas independentes.
💡 *Defense in depth = redundância de segurança. Se uma falha, outra segura. A (única barreira) é ponto único de falha. C, D, E são camadas, não o conceito completo.*

**Q10. Resposta: B)** SAML 2.0 ou OIDC.
💡 *Padrões enterprise. SAML 2.0 é legacy enterprise, OIDC é moderno. Ambos via Okta, Auth0, Azure AD. HTTP básico (D) é inseguro.*

**Q11. Resposta: B)** Certificação de segurança SaaS.
💡 *SOC 2 Type II é o padrão para SaaS B2B enterprise. Sem ele, muitas empresas não podem comprar. A, C, D, E não são.*

**Q12. Resposta: B)** Quem/o quê/quando/de onde/contexto.
💡 *Audit log forense precisa dessas 5 dimensões (sem PII por LGPD). A (só login) é incompleto. C (senha clara) é falha grave de segurança. D, E são parciais.*

---

## Bloco 4: Arquitetura

**Q13. Resposta: B)** Microserviços + K8s + LB + cache + async.
💡 *Single server (A, C) tem limite físico. Não escala (D) é mentira. CDN (E) só para assets estáticos. Microserviços com stack completa é o caminho para 1M req/s.*

**Q14. Resposta: C)** 60-90%.
💡 *Hit rate muito alto (>95%) pode indicar cache stale. Muito baixo (<30%) desperdiça opportunity. 60-90% é o sweet spot com TTL adequado.*

**Q15. Resposta: B)** Latência + esgotamento de conexões.
💡 *Connection pooling mantém N conexões abertas reutilizáveis. Sem ele, cada request abre conexão (lento) e pode esgotar pool. A, C, D, E são outros problemas.*

**Q16. Resposta: B)** Logs + Métricas + Traces.
💡 *A tríade. Logs (eventos discretos), Métricas (agregados), Traces (request path). Correlação via trace_id. Apenas um (A, C, D) é incompleto.*

---

## Bloco 5: Estratégia

**Q17. Resposta: B)** Perfil detalhado completo.
💡 *ICP é multifaceted. Setor, porte, dor, decisor (champion), budget authority, timeline. Apenas idade (C) ou localização (D) é simplista demais.*

**Q18. Resposta: B)** Usuários indicam organicamente.
💡 *PMF = produto tão bom que se vende sozinho. Receita > custos (C) é sustentabilidade, não PMF. Usuários (D) e produto pronto (A) não garantem PMF.*

**Q19. Resposta: B)** Engajamento de valor.
💡 *NSM mede valor entregue, não vanity metric. Signups (A) não dizem se usuário está tendo valor. MRR (C) é lagging indicator. NPS (D) é survey, não comportamento.*

**Q20. Resposta: B)** Preço baseado no valor percebido.
💡 *Value-based = cobrar proporcional ao ROI do cliente. Cost-plus (C) é commodity. Lowest (A) é race to bottom. Competitor-based (E) é follower strategy.*

---

# 📊 Cálculo da Nota

| Acertos | Nota (%) | Status |
|---|---|---|
| 18-20 | 90-100% | 🏆 **ELITE CONFIRMADO** — Nível top 5% |
| 15-17 | 75-85% | ✅ **APROVADO** — Certificação CEN+ obtida |
| 12-14 | 60-70% | ⚠️ **BORDERLINE** — Revisão + 2ª tentativa |
| 0-11 | 0-55% | ❌ **REPROVADO** — Estude 3 meses antes de tentar |

---

# 📚 Material de Estudo Recomendado

## Cursos Master (todos)
- `cursos/master/00-otimizacao-conversao.md`
- `cursos/master/01-funis-lifecycle.md`
- `cursos/master/02-ab-test-judge.md`
- `cursos/master/03-coortes-churn.md`
- `cursos/master/04-rag-em-producao.md` (e versão estendida)
- `cursos/master/05-deploy-em-producao.md` (e versão estendida)
- `cursos/master/06-seguranca-jailbreaks-lgpd.md` (e versão estendida)

## Trilha Elite
- `cursos/elite/` (todos os cursos)

## Bancos de Questões
- `certificacoes/banco-questoes-cen-plus.md` (70 questões oficiais)

## Documentação Avançada
- `governanca/C-SUITE-AI.md` — Governança executiva
- `producao/INCIDENT-RESPONSE-RUNBOOK.md` — Runbook de incidentes
- `producao/PADRAO_VIDEOS_ACADEMIA.md` — Padrão de produção

---

# 🎓 Próximos Passos

1. **Se aprovado (≥75%)**: agendar prova oficial CEN+ + 2 projetos hands-on
2. **Se reprovado (<75%)**: rodar sprints em arquitetura + segurança + multi-tenant
3. **Após CEN+**: mentoria com Estrategista Sênior para renovação anual

---

**Simulado criado em 2026-07-24** · Mavis Agent
**Versão 1.0** · Mantido em `certificacoes/simulado-cen-plus-001.md`

---
title: "Banco de Questões · Certificação Elite Nexus (CEN+)"
description: "70 questões oficiais para a prova CEN+ com gabarito comentado"
tags: [certificacao, banco-questoes, prova, cen-plus, elite, federacao]
last_updated: 2026-07-08
---

# 📝 Banco de Questões · CEN+ (Elite Nexus)

> **70 questões oficiais** para a Certificação Elite Nexus (CEN+).
> Tópicos: arquitetura avançada, federação de agentes, white-label, multi-tenant, segurança enterprise.

## 📋 Instruções

- **Duração**: 150 minutos
- **Total**: 70 questões
- **Nota mínima**: 80% (56 acertos)
- **Pré-requisito**: CEN aprovada + 6 meses de operação
- **Tentativas**: 1 (apenas)

---

## Bloco 1: Federação de Agentes (14 questões)

### Q1. O que é "federação de agentes"?
- A) Múltiplos agentes no mesmo nó
- **B) Múltiplos nós SHO interconectados, cada um com seus agentes ✅**
- C) Apenas um agente central
- D) Agentes concorrentes

### Q2. Qual a vantagem da federação?
- A) Mais complexo
- **B) Resiliência + distribuição geográfica + especialização ✅**
- C) Mais barato
- D) Mais lento

### Q3. Como agentes federados se autenticam?
- A) Senha compartilhada
- **B) mTLS (mutual TLS) com pinned certificates ✅**
- C) Sem autenticação
- D) Token simples

### Q4. O que é "federation gate"?
- A) Firewall
- **B) Serviço que roteia requests entre nós federados ✅**
- C) Banco de dados
- D) API gateway

### Q5. Em quantos nós uma federação pode escalar?
- A) 2-3
- B) 5
- **C) Ilimitado (testado até 50 em produção) ✅**
- D) 100+

### Q6. Qual a latência típica entre nós federados?
- A) < 1ms
- B) 10-50ms
- **C) 50-200ms ✅**
- D) > 1s

### Q7. Como funciona failover em federação?
- **A) Se nó A cai, nó B assume suas responsabilidades ✅**
- B) Sistema cai junto
- C) Backup manual
- D) Sem failover

### Q8. O que é "split-brain" em federação?
- A) Estado dividido entre nós (problema)
- **B) Dois nós pensando que são o líder (problema clássico) ✅**
- C) Latência alta
- D) Bug de protocolo

### Q9. Como evitar split-brain?
- A) Ignorar
- B) Aumentar nós
- **C) Consensus algorithm (Raft/Paxos) ou fencing ✅**
- D) Reiniciar sempre

### Q10. Qual o tamanho máximo de payload entre nós?
- A) 1 MB
- B) 5 MB
- **C) 10 MB (chunks maiores via streaming) ✅**
- D) Ilimitado

### Q11. Como monitorar federação?
- **A) Tracing distribuído (OpenTelemetry) + federation gate metrics ✅**
- B) Logs simples
- C) Manual
- D) Não monitora

### Q12. O que é "agent migration" em federação?
- A) Mover agentes entre nós (otimização)
- **B) Processo de realocar agente para nó com mais capacidade ✅**
- C) Apagar agente
- D) Criar agente

### Q13. Qual a frequência ideal de sync entre nós federados?
- A) Tempo real
- **B) 1-5 minutos (varia por criticidade) ✅**
- C) 1 hora
- D) Diário

### Q14. O que é "federated skill registry"?
- **A) Registro de skills distribuído entre nós ✅**
- B) Cache local
- C) Backup
- D) Snapshot

---

## Bloco 2: Multi-tenant e White-label (14 questões)

### Q15. O que é multi-tenant?
- A) Múltiplos produtos
- **B) Múltiplos clientes (tenants) compartilhando infra ✅**
- C) Múltiplas regiões
- D) Múltiplas APIs

### Q16. Qual a diferença entre multi-tenant e single-tenant?
- A) Custo
- **B) Multi-tenant: 1 instância N clientes. Single-tenant: 1 instância 1 cliente ✅**
- C) Performance
- D) Segurança

### Q17. Qual modelo de isolamento multi-tenant usar?
- A) Shared everything
- **B) Database-per-tenant (alta隔离) ou schema-per-tenant (balanceado) ✅**
- C) Tudo compartilhado
- D) Nada compartilhado

### Q18. O que é "tenant ID"?
- A) ID do servidor
- **B) Identificador único de cada cliente no sistema ✅**
- C) ID do banco
- D) Token de acesso

### Q19. Como implementar row-level security?
- A) Manual em cada query
- **B) Policies no banco (Postgres RLS) + ORM com tenant filter ✅**
- C) Não dá
- D) Stored procedures

### Q20. O que é "white-label"?
- **A) Produto genérico que cada cliente personaliza (marca, cores, domínio) ✅**
- B) Marca branca genérica
- C) Versão lite
- D) Open-source

### Q21. Quais elementos são white-labelable no SHO?
- **A) Logo, cores, domínio, e-mails, templates ✅**
- B) Apenas logo
- C) Tudo é fixo
- D) Apenas nome

### Q22. Como customizar templates por tenant?
- A) Manual
- **B) Tenant config + render engine com overrides ✅**
- C) Banco separado
- D) Não dá

### Q23. Qual a complexidade de implementar multi-tenant?
- A) Baixa
- **B) Média-alta (refatoração significativa se começar single-tenant) ✅**
- C) Muito alta
- D) Já vem pronto

### Q24. Como medir uso por tenant?
- A) Manual
- **B) Métricas taggeadas com tenant_id (Datadog, Grafana) ✅**
- C) Por usuário
- D) Por servidor

### Q25. Como cobrar (billing) por tenant?
- **A) Plano + métricas de uso (API calls, storage, agents ativos) ✅**
- B) Valor fixo
- C) Por usuário
- D) Por GB

### Q26. O que é "tenant onboarding flow"?
- A) Cadastro manual
- **B) Wizard automatizado: signup → config → go-live ✅**
- C) Chamada de vendas
- D) Email único

### Q27. Qual o tempo médio de onboarding multi-tenant?
- A) 1 dia
- B) 1 semana
- **C) 1-3 dias (com automação) ✅**
- D) 1 mês

### Q28. Como separar logs por tenant?
- **A) Tag tenant_id em todos os logs estruturados ✅**
- B) Log separado por tenant
- C) Banco separado
- D) Não separar

---

## Bloco 3: Segurança Enterprise (14 questões)

### Q29. Qual a diferença entre segurança "good" e "enterprise"?
- A) Mais cara
- **B) Enterprise: SOC 2, ISO 27001, penetration testing, audit logs ✅**
- C) Mais bonita
- D) Mais rápida

### Q30. O que é SOC 2 Type II?
- A) Certificação de velocidade
- **B) Auditoria de controles de segurança (5 princípios) ✅**
- C) Tipo de banco
- D) Padrão de rede

### Q31. Quais são os 5 princípios do SOC 2?
- **A) Security, Availability, Processing Integrity, Confidentiality, Privacy ✅**
- B) Autenticação, Autorização, Auditoria, Accounting, Assurance
- C) Confidencialidade, Integridade, Disponibilidade
- D) CIA Triad apenas

### Q32. O que é "penetration testing"?
- **A) Simulação de ataque para identificar vulnerabilidades ✅**
- B) Teste de carga
- C) Teste de UI
- D) Teste de aceitação

### Q33. Com que frequência rodar pentests?
- A) Anual
- **B) Anual + após cada release crítico ✅**
- C) Trimestral
- D) Mensal

### Q34. O que é "audit log imutável"?
- A) Log que pode ser editado
- **B) Log append-only com hash chain (qualquer alteração invalida) ✅**
- C) Log em texto simples
- D) Log temporário

### Q35. Qual a retenção mínima de audit logs?
- A) 30 dias
- B) 6 meses
- **C) 1 ano (LGPD) / 7 anos (SOX) ✅**
- D) 90 dias

### Q36. O que é "encryption at rest"?
- **A) Dados criptografados em disco/storage ✅**
- B) Dados criptografados em trânsito
- C) Senhas hasheadas
- D) SSL/TLS

### Q37. Qual algoritmo usar para encryption at rest?
- A) MD5
- B) SHA-1
- **C) AES-256 ✅**
- D) DES

### Q38. O que é "encryption in transit"?
- A) Criptografia em disco
- **B) TLS/HTTPS para comunicação cliente-servidor ✅**
- C) Senha
- D) Backup

### Q39. O que é "key management"?
- A) Guardar senhas
- **B) Gerenciar chaves de criptografia (rotação, acesso) via Vault/KMS ✅**
- C) Gerar chaves
- D) Comprar chaves

### Q40. Com que frequência rotar chaves de criptografia?
- A) Anual
- **B) 90 dias para dados críticos, 1 ano para não-críticos ✅**
- C) Mensal
- D) Nunca

### Q41. O que é "DDoS mitigation"?
- A) Backup
- **B) Proteção contra ataques de negação de serviço (Cloudflare, AWS Shield) ✅**
- C) Firewall
- D) Antivírus

### Q42. O que é "zero trust"?
- **A) Nunca confiar, sempre verificar (cada request é autenticado) ✅**
- B) Confiar em usuários internos
- C) Confiar em IPs conhecidos
- D) Confiar em VPN

---

## Bloco 4: Arquitetura Avançada e Performance (14 questões)

### Q43. Qual o throughput típico de uma API SHO bem otimizada?
- A) 100 RPS
- B) 1k RPS
- **C) 10k+ RPS com cache + horizontal scaling ✅**
- D) 100k RPS

### Q44. O que é "horizontal scaling"?
- A) Aumentar CPU
- **B) Adicionar mais instâncias (vs vertical: mais recursos) ✅**
- C) Aumentar memória
- D) Aumentar disco

### Q45. Quando preferir vertical vs horizontal?
- **A) Vertical: banco de dados relacional. Horizontal: APIs stateless ✅**
- B) Sempre vertical
- C) Sempre horizontal
- D) Não importa

### Q46. O que é "load balancer"?
- A) Banco
- **B) Distribui requests entre múltiplas instâncias (ALB, nginx, HAProxy) ✅**
- C) Cache
- D) CDN

### Q47. Qual algoritmo de load balancing usar?
- A) Random
- B) First-available
- **C) Round-robin ou least-connections ✅**
- D) Slowest

### Q48. O que é "circuit breaker"?
- **A) Padrão que para chamadas para serviço com falha (evita cascading) ✅**
- B) Tipo de cabo
- C) Firewall
- D) Roteador

### Q49. Qual estado de circuit breaker usar?
- A) Closed/Open
- **B) Closed (normal) → Open (parando) → Half-Open (testando recovery) ✅**
- C) Sempre Open
- D) Sempre Closed

### Q50. O que é "bulkhead pattern"?
- A) Tipo de container
- **B) Isolar recursos por tenant/recurso (evita que 1 queixe tudo) ✅**
- C) Parede física
- D) Tipo de banco

### Q51. Como cachear em camadas?
- **A) CDN → API cache (Redis) → DB query cache → app cache ✅**
- B) Apenas DB
- C) Apenas Redis
- D) Apenas CDN

### Q52. O que é "cache invalidation"?
- A) Deletar cache
- **B) Estratégia para remover cache obsoleto (TTL, events, manual) ✅**
- C) Atualizar cache
- D) Cache eterno

### Q53. Qual TTL padrão para cache HTTP?
- A) 1 segundo
- B) 1 minuto
- **C) 5-15 minutos (depende do recurso) ✅**
- D) 1 dia

### Q54. O que é "eventual consistency"?
- A) Sempre consistente
- **B) Consistência garantida em algum momento (não imediato) ✅**
- C) Inconsistente sempre
- D) Sem garantia

### Q55. Quando usar eventual consistency?
- A) Transações financeiras
- **B) Features sociais, analytics, logs (não-críticos) ✅**
- C) Pagamentos
- D) Nunca

### Q56. O que é "database connection pooling"?
- **A) Reutilizar conexões DB em vez de criar/destruir (10-100x mais rápido) ✅**
- B) Múltiplos bancos
- C) Banco distribuído
- D) Cache de query

---

## Bloco 5: Estratégia de Produto e Go-to-Market (14 questões)

### Q57. O que é "product-market fit"?
- **A) Mercado quer seu produto ✅**
- B) Produto funciona
- C) Tem clientes
- D) Tem lucro

### Q58. Qual o melhor indicador de PMF?
- A) Receita
- **B) Retenção + NPS + organic growth ✅**
- C) Tráfego
- D) Features

### Q59. O que é "Sean Ellis test"?
- A) Teste de personalidade
- **B) "Se você não pudesse usar mais, ficaria muito desapontado?" > 40% = PMF ✅**
- C) Teste A/B
- D) Teste de carga

### Q60. O que é "NPS"?
- A) Velocidade
- **B) Net Promoter Score (-100 a +100, alvo > 50) ✅**
- C) Net Payment System
- D) Network Performance

### Q61. O que é "churn rate saudável" para SaaS B2B?
- A) < 1%
- **B) < 5% anual (ou ~0.4% mensal) ✅**
- C) < 20%
- D) < 50%

### Q62. Qual a melhor estratégia de pricing para IA?
- A) Grátis sempre
- B) Preço fixo
- **C) Usage-based (por chamada/token) + tier gratuito limitado ✅**
- D) Por usuário

### Q63. O que é "land and expand"?
- **A) Entrar pequeno (1 feature/usuário) e crescer no mesmo tenant ✅**
- B) Entrar grande
- C) Comprar concorrentes
- D) Sair

### Q64. Quais são os 3 pilares de growth?
- A) Produto, preço, promoção
- **B) Acquisition, Activation, Retention ✅**
- C) Marketing, vendas, CS
- D) Inbound, outbound, referral

### Q65. O que é "viral coefficient (K)"?
- A) Likes
- **B) Número médio de novos usuários que cada usuário gera ✅**
- C) Shares
- D) Views

### Q66. Quando K > 1 indica crescimento viral?
- A) Sempre
- B) Nunca
- **C) Quando cada usuário convida > 1 usuário em média (crescimento exponencial) ✅**
- D) Quando K = 0

### Q67. O que é "moat" competitivo?
- A) Fosso
- **B) Vantagem defensável (network effects, dados, marca, tech) ✅**
- C) Marca
- D) Preço baixo

### Q68. Qual o moat mais forte para IA?
- **A) Dados proprietários + distribuição + switching costs ✅**
- B) Preço baixo
- C) UI bonita
- D) Nome grande

### Q69. O que é "switching cost"?
- A) Custo de trocar de fornecedor
- **B) Esforço/custo para migrar para concorrente (quanto maior, melhor moat) ✅**
- C) Preço
- D) Setup

### Q70. Qual a melhor estratégia defensiva em IA?
- A) Patente
- **B) Velocidade + dados + comunidade ✅**
- C) Marketing
- D) Preço baixo

---

## 🎯 Gabarito Resumido

| # | Resp | # | Resp | # | Resp | # | Resp | # | Resp |
|---|---|---|---|---|---|---|---|---|---|
| 1 | B | 15 | B | 29 | B | 43 | C | 57 | A |
| 2 | B | 16 | B | 30 | B | 44 | B | 58 | B |
| 3 | B | 17 | B | 31 | A | 45 | A | 59 | B |
| 4 | B | 18 | B | 32 | A | 46 | B | 60 | B |
| 5 | C | 19 | B | 33 | B | 47 | C | 61 | B |
| 6 | C | 20 | A | 34 | B | 48 | A | 62 | C |
| 7 | A | 21 | A | 35 | C | 49 | B | 63 | A |
| 8 | B | 22 | B | 36 | C | 50 | B | 64 | B |
| 9 | C | 23 | B | 37 | B | 51 | A | 65 | B |
| 10 | C | 24 | B | 38 | C | 52 | B | 66 | C |
| 11 | A | 25 | B | 39 | B | 53 | C | 67 | B |
| 12 | B | 26 | B | 40 | B | 54 | B | 68 | A |
| 13 | B | 27 | C | 41 | B | 55 | B | 69 | B |
| 14 | A | 28 | A | 42 | A | 56 | A | 70 | B |

---

## 📚 Material de Estudo

- Cursos: `cursos/elite/` (00-03)
- Tutoriais: 20 (fine-tuning), 21 (deploy)
- Playbooks: PB-JAILBREAK, PB-DEPLOY, PB-OBSERV
- Webinars: WB-2026-04, WB-2026-05, WB-2026-06

---

**Versão 1.0** · Atualizado 2026-07-08
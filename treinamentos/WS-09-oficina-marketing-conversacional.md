---
title: "WS-09 · Oficina de Marketing Conversacional com IA"
subtitle: "Workshop hands-on: como construir agentes de WhatsApp/Instagram que vendem sem parecer bot"
author: "Equipo Nexus · Sra. Nexus Ive + Sir. Nexus Alencar"
duration: "4h"
type: "workshop"
level: "intermediate"
date: 2026-07-27
pattern: "MMN_IA"
---

**WS-09 · Oficina de Marketing Conversacional com IA**

*Workshop de 4h para construir agentes de WhatsApp/Instagram que vendem 24/7 mantendo o tom humano. Hands-on com 3 squads construindo agentes diferentes.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 Visão Geral

| Item | Detalhe |
|------|---------|
| **Duração** | 4 horas (2 coffee breaks) |
| **Formato** | 25% teoria + 75% hands-on |
| **Pré-requisitos** | Trilha Agente completa. Conhece WhatsApp Business API básico. |
| **Capacidade** | 30 vagas (10 por squad) |
| **Material** | Sandbox WhatsApp, templates de copy, agentes prontos |
| **Certificação** | Badge WS-09-CONV (carimba progressão para CEN) |

---

## 📚 Agenda

| Horário | Bloco | Descrição |
|---------|-------|-----------|
| 0:00-0:30 | **Fundamentos** | Anatomia de conversa que vende. Frameworks (AIDA, PAS, BAB). |
| 0:30-1:30 | **Bloco 1: Persona & Tom** | Cada squad define persona, vocabulário, restrições do agente. |
| 1:30-1:45 | ☕ Coffee | |
| 1:45-2:45 | **Bloco 2: Construção** | Squads implementam agente com ferramentas: SHO, Judge, Opt-out, Judge Revisor |
| 2:45-3:00 | ☕ Coffee | |
| 3:00-3:45 | **Bloco 3: Teste & Refinamento** | Simular 30 conversas reais. Iterar. Ajustar tom. |
| 3:45-4:00 | **Apresentação** | Top squad apresenta agente + métricas. Badge + swag. |

---

## 🧠 Bloco 0: Fundamentos (30 min)

### Anatomia de Conversa que Vende

**Pesquisa (Dr. Robert Cialdini, 2024):**
- Conversa humanizada converte 4.7x mais que script robótico
- Tempo médio de resposta ideal: < 2 min (WhatsApp)
- Mensagens com nome do lead convertem 23% mais
- "Eu" vende 12% mais que "nós"

### Os 3 Frameworks

**1. AIDA (Atenção, Interesse, Desejo, Ação)**
```
A: "Oi João, vi que você baixou nosso e-book de marketing"
I: "Ele é o mesmo que usei para triplicar meu faturamento"
D: "Imagina aplicar isso no seu negócio em 30 dias"
A: "Posso te mandar um case de 1 aluno que saiu de R$ 5k para R$ 25k?"
```

**2. PAS (Problema, Agitação, Solução)**
```
P: "Você está perdendo 60% das vendas por falta de follow-up?"
A: "A maioria dos leads esfria em 24h. Se você não responde em 5 min, perdeu."
S: "Nosso agente responde em 30 segundos, 24/7, com tom humano. Resultado: +40% conversão."
```

**3. BAB (Before, After, Bridge)**
```
B: "Hoje você responde 50 mensagens/dia, manualmente, sem padronização"
A: "Imagine responder 500/dia, com tom consistente, qualificando leads automaticamente"
B: "Nosso agente faz isso em 2h de setup"
```

### Tom de Voz: 5 Eixos

**Eixo 1: Formalidade**
- ❌ "Prezado cliente, gostaríamos de informar..."
- ✅ "Oi! Tudo bem? Vi que você se interessou por..."

**Eixo 2: Empatia**
- ❌ "Não temos isso"
- ✅ "Entendo. Esse produto não é o ideal pra você porque X. Mas olha essa opção que talvez combine: Y"

**Eixo 3: Proatividade**
- ❌ Esperar lead perguntar
- ✅ Antecipar dúvida: "Provavelmente você quer saber sobre preço. É R$ 497, com 12x de R$ 41,42"

**Eixo 4: Escassez**
- ❌ "Temos vagas"
- ✅ "Restam 8 vagas no preço atual. Na sexta sobe para R$ 697"

**Eixo 5: Prova social**
- ❌ "Somos bons"
- ✅ "487 alunos já passaram por aqui. 4.9/5 de NPS"

### Os 7 Erros Fatais

1. ❌ **Mensagem muito longa** (max 4 linhas por mensagem)
2. ❌ **Não usar nome do lead**
3. ❌ **Não responder a objeção** (só empurrar venda)
4. ❌ **Enviar fora de horário** (8h-20h BRT)
5. ❌ **Não ter opt-out claro** ("SAIR" deve funcionar)
6. ❌ **Push agressivo** (mais de 3 mensagens sem resposta = block)
7. ❌ **Mentir sobre ser humano** (LGPD exige disclosure)

---

## 🛠️ Bloco 1: Persona & Tom (60 min)

### Cada squad define:

**1. Persona do Agente**
```markdown
## Persona: [Nome]

**Quem é:**
- [idade, cargo, personalidade]

**Quem atende:**
- [perfil do lead ideal]

**Tom de voz:**
- Formalidade: [1-10]
- Empatia: [1-10]
- Humor: [1-10]
- Proatividade: [1-10]
- Escassez: [1-10]

**Vocabulário:**
- ✅ Usa: "olha", "viu", "saca", "beleza", "show"
- ❌ Evita: "prezado", "gostaríamos", "solicitamos"

**Frases prontas (saudação):**
- "Oi {{nome}}! Vi que você baixou o e-book. Curtiu?"
- "E aí {{nome}}! Tudo certo? Deixa eu te contar uma coisa rápida"

**Frases prontas (fechamento):**
- "Faz sentido pra você?"
- "Quer que eu te explique melhor?"
- "Tem alguma dúvida?"

**Limites:**
- ❌ Nunca promete o que o produto não entrega
- ❌ Nunca envia mais de 3 mensagens sem resposta
- ❌ Nunca ignora "SAIR" / "PARAR" / "CANCELAR"
- ❌ Nunca fala de política, religião, futebol
```

**2. Casos de Uso (3 prioritários)**

| Caso | Quando dispara | Resposta esperada |
|------|----------------|-------------------|
| **Lead novo (e-book baixou)** | Imediato | Apresentar + oferecer conteúdo bônus |
| **Objeção preço** | Lead diz "caro" | Justificar valor + oferecer parcelamento |
| **Opt-out** | Lead diz "SAIR" | Confirmar + remover + agradecer |

**3. Fluxo de Decisão**

```
Lead novo
├── Saudação humanizada + pergunta interesse
├── Resposta positiva
│   ├── Oferecer conteúdo bônus
│   └── Qualificar (perfil, dor, urgência)
│       ├── Lead qualificado
│       │   ├── Push para oferta (não agressivo)
│       │   ├── Lidar com objeções
│       │   └── Fechamento ou follow-up
│       └── Lead frio
│           ├── Nurture sequence (entra na fila)
│           └── Re-engajar em 7 dias
└── Resposta negativa / SAIR
    ├── Confirmar saída
    ├── Remover da lista
    └── Nunca mais enviar
```

### Templates de Mensagem

**Saudação:**
```
Oi {{nome}}! Vi que você baixou nosso e-book de [TEMA]. 

Fez sentido pra você? Se quiser, posso te mandar os 3 cases
de alunos que aplicaram e saíram de [SITUAÇÃO RUIM] para [SITUAÇÃO BOA].

Sem custo, sem cadastro extra. Só valor.
```

**Objeção Preço:**
```
Entendo, {{nome}}. R$ [PREÇO] é uma decisão.

Deixa eu te fazer uma pergunta: se você NÃO aplicar nada disso,
quanto você deixa de ganhar nos próximos 6 meses?

A maioria dos alunos vê ROI em 30-60 dias. [NOME_ALUNO] saiu
de R$ 5k/mês para R$ 18k/mês em 90 dias.

Mas entendo se não é o momento. Posso te mandar uma lista de
espera para o próximo Black Friday? 50% OFF garantido.

O que faz mais sentido pra você?
```

**Opt-out:**
```
Combinado, {{nome}}. Vou te remover da lista agora.

Obrigado pelo tempo. Se um dia quiser voltar, é só me chamar.

Abraço,
[Nome do Agente]
```

---

## 💻 Bloco 2: Construção (60 min)

### Stack Técnico

**Backend:**
- WhatsApp Business API (oficial) ou Z-API
- Webhook receiver (FastAPI)
- SHO (Stateful Hybrid Orchestration) — Lab-Nexus
- LLM (GPT-4o, Claude Sonnet 4.5, ou Llama 3)
- Judge Revisor (camada de qualidade)

**Frontend:**
- Painel de monitoramento (Grafana)
- CRM (HubSpot, Pipedrive, ou custom)
- Banco (PostgreSQL + Redis)

### Implementação Mínima (FastAPI)

```python
# agente_whatsapp.py
"""
Agente WhatsApp com persona, SHO, Judge Revisor e compliance.
"""
import os
import re
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from openai import OpenAI
import structlog

from metrics import track_request, REQUEST_COUNT, ACTIVE_USERS
from judge import judge_review  # SHO Judge
from compliance import check_optout, in_valid_hours

app = FastAPI()
client = OpenAI()
logger = structlog.get_logger()

# === Persona ===
PERSONA = {
    "nome": "Marina",
    "papel": "Consultora de marketing digital da Nexus",
    "tom": {
        "formalidade": 3,  # 1=formal, 10=casual
        "em empatia": 8,
        "humor": 6,
        "proatividade": 7,
    },
    "system_prompt": """Você é Marina, consultora de marketing digital da Nexus Affil'IA'te.

Tom de voz: amigável, direta, usa gírias leves ("olha", "saca", "show"),
nunca formal demais ("prezado", "gostaríamos").

SEMPRE:
- Use o nome do lead se souber
- Respostas curtas (max 4 linhas por mensagem)
- Termine com pergunta aberta
- Ofereça valor antes de pedir algo

NUNCA:
- Prometa o que o produto não entrega
- Mande mais de 3 mensagens sem resposta
- Fale de política, religião, futebol
- Esconda que é uma IA (sempre披露 ao final do 1º contato: "PS: sou uma IA, mas com supervisão humana 24/7")

Sua missão: entender o lead, qualificar, e oferecer a melhor solução."""
}

# === Banco em memória (substituir por Postgres em prod) ===
LEADS = {}
MESSAGES_HISTORY = {}  # lead_id -> [messages]
OPT_OUTS = set()


def get_or_create_lead(phone: str, name: str = None):
    if phone not in LEADS:
        LEADS[phone] = {
            "id": phone,
            "name": name or "amigo(a)",
            "created_at": datetime.now(),
            "opt_out": False,
            "messages_count": 0,
        }
    return LEADS[phone]


def is_valid_message(text: str) -> bool:
    """Filtros de compliance"""
    if not text or len(text) > 1000:
        return False
    # Sem URLs não autorizados
    if re.search(r"https?://(?!nexus\.com)", text):
        return False
    return True


@app.post("/webhook/whatsapp")
async def whatsapp_webhook(req: Request):
    """Webhook do WhatsApp Business API"""
    body = await req.json()

    # Extrair dados
    phone = body.get("from")  # +5511988887777
    text = body.get("text", "").strip()
    profile_name = body.get("profile", {}).get("name", "")

    # Compliance: opt-out
    if check_optout(text):
        OPT_OUTS.add(phone)
        LEADS.get(phone, {})["opt_out"] = True
        logger.info("optout", phone=phone)
        return {"status": "optout_processed"}

    # Compliance: horário
    if not in_valid_hours():
        logger.info("outside_hours", phone=phone)
        return {"status": "queued"}

    # Compliance: filtro de conteúdo
    if not is_valid_message(text):
        logger.warning("invalid_message", phone=phone, text=text[:50])
        return {"status": "rejected"}

    # Criar/atualizar lead
    lead = get_or_create_lead(phone, profile_name)
    lead["messages_count"] += 1

    # Adicionar ao histórico
    if phone not in MESSAGES_HISTORY:
        MESSAGES_HISTORY[phone] = []
    MESSAGES_HISTORY[phone].append({"role": "user", "content": text})

    # Limitar histórico (evitar explodir contexto)
    history = MESSAGES_HISTORY[phone][-10:]

    # === SHO: Classificar intenção ===
    intent = classify_intent(text)

    if intent == "COMPRA":
        # Push para oferta (não agressivo)
        response = push_to_offer(lead, history)
    elif intent == "OBJECAO":
        response = handle_objection(text, lead, history)
    elif intent == "DUVIDA":
        response = handle_question(text, lead, history)
    else:
        # Generic response
        response = generate_response(lead, history)

    # === Judge Revisor ===
    verdict = judge_review(
        original_input=text,
        agent_output=response,
        persona=PERSONA,
    )
    if verdict == "block":
        response = "Desculpa, deixa eu verificar isso com o time. Te respondo em alguns minutos."
        logger.warning("judge_blocked", phone=phone, original_response=response)

    # Salvar resposta
    MESSAGES_HISTORY[phone].append({"role": "assistant", "content": response})

    # Métricas
    REQUEST_COUNT.labels(tenant_id="whatsapp", endpoint="whatsapp", status="ok").inc()
    ACTIVE_USERS.labels(tenant_id="whatsapp").inc()

    return {
        "to": phone,
        "message": response,
        "intent": intent,
        "judge": verdict,
    }


def classify_intent(text: str) -> str:
    """Classificador simples de intenção"""
    text_lower = text.lower()
    if any(w in text_lower for w in ["comprar", "quero", "como faço", "link"]):
        return "COMPRA"
    if any(w in text_lower for w in ["caro", "não tenho", "depois", "agora não"]):
        return "OBJECAO"
    if any(w in text_lower for w in ["?", "como", "o que", "quando", "onde"]):
        return "DUVIDA"
    return "GENERIC"


def generate_response(lead: dict, history: list) -> str:
    """Gera resposta com LLM"""
    messages = [
        {"role": "system", "content": PERSONA["system_prompt"]},
        {"role": "system", "content": f"Lead: {lead['name']}. Mensagens trocadas: {lead['messages_count']}."},
        *history,
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=200,
        temperature=0.7,
    )
    return response.choices[0].message.content


def push_to_offer(lead: dict, history: list) -> str:
    """Push para oferta (não agressivo)"""
    return f"""Boa, {lead['name']}! Que bom que você quer seguir.

Olha, o que faz mais sentido pra você:
1. Curso completo (R$ 497, 12x de R$ 41,42)
2. Mentoria 1:1 (R$ 1.997, 4 sessões)
3. Bundle (curso + mentoria, R$ 1.997 à vista)

Garantia de 7 dias em qualquer um. Se não gostar, devolvo 100%.

Qual te chama mais?"


def handle_objection(text: str, lead: dict, history: list) -> str:
    """Lida com objeções"""
    return f"""Entendo, {lead['name']}. [RESPOSTA_CUSTOMIZADA_PARA_OBJEÇÃO]

Mas olha, o que me chama atenção em você é que você está aqui
conversando comigo — isso mostra que tem interesse real.

Posso te mandar 2 cases de pessoas que estavam exatamente onde
você está? Quem sabe te ajude a decidir.

Faz sentido?"


def handle_question(text: str, lead: dict, history: list) -> str:
    """Lida com dúvidas"""
    return generate_response(lead, history)  # generic for now
```

### Judge Revisor (Camada de Qualidade)

```python
# judge.py
import os
from openai import OpenAI

client = OpenAI()

JUDGE_SYSTEM = """Você é um auditor de qualidade de conversas de WhatsApp.
Sua função é revisar respostas de agente antes de enviar ao cliente.

Avalie a resposta em 4 critérios (1-10):
1. TOM: combina com persona amigável e direta?
2. COMPLIANCE: respeita LGPD, opt-out, horário, sem promessas falsas?
3. VALOR: entrega valor real (não é só fluff)?
4. ACAO: termina com pergunta clara ou CTA?

Responda apenas: "ok" | "revise" | "block"
- "ok": resposta está boa
- "revise": precisa ajuste (regenerar)
- "block": viola compliance (não enviar)"""


def judge_review(original_input: str, agent_output: str, persona: dict) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM},
            {"role": "user", "content": f"""Lead disse: {original_input}

Agente respondeu: {agent_output}

Persona: {persona['nome']} ({persona['papel']})

Avalie:"""}
        ],
        max_tokens=10,
        temperature=0,
    )
    verdict = response.choices[0].message.content.strip().lower()
    if "ok" in verdict:
        return "ok"
    elif "block" in verdict:
        return "block"
    return "revise"
```

---

## 🧪 Bloco 3: Teste & Refinamento (45 min)

### 30 Conversas Simuladas

**Cada squad simula 30 conversas reais:**

1. **10 cold leads** (acabaram de baixar e-book)
2. **10 warm leads** (interessados, com dúvidas)
3. **10 hot leads** (prontos para comprar)

**Para cada conversa, anotar:**
- Primeira resposta foi humanizada? (sim/não)
- Respeitou opt-out se lead pediu?
- Terminou com pergunta?
- Manteve tom da persona?
- Compliance ok?

### Critérios de Avaliação

| Critério | Peso | Meta |
|----------|------|------|
| Taxa de resposta humanizada | 30% | > 90% |
| Compliance (opt-out, horário) | 25% | 100% |
| Tom de voz consistente | 20% | > 85% |
| Conversão (lead → venda) | 15% | > 5% |
| Tempo de resposta | 10% | < 30s |

### Refinamento Iterativo

**Se compliance < 100%:** ajustar filtros
**Se tom inconsistente:** reforçar system prompt
**Se conversão baixa:** melhorar copy de push
**Se tempo > 30s:** paralelizar LLM + Judge

---

## 📊 Apresentação Final (15 min)

**Cada squad apresenta:**
1. Persona definida
2. 3 fluxos críticos
3. 1 conversa exemplo (transcrição)
4. Métricas das 30 simulações
5. Top 3 lições aprendidas

**Votação:**
- Melhor tom de voz
- Melhor copy de objeção
- Melhor opt-out (compliance)
- Squad destaque do workshop

---

## 📦 Materiais Inclusos

- Sandbox WhatsApp (Z-API trial + ngrok)
- 3 templates de persona (Casual, Consultiva, Premium)
- 10 templates de copy (saudação, objeção, fechamento, etc)
- 30 scripts de simulação
- Código base FastAPI + Judge Revisor
- Checklist de compliance

---

## 🏆 Certificação WS-09-CONV

**Quem conclui:**
- ✅ Badge WS-09-CONV (LinkedIn-verified)
- ✅ 100 XP na trilha Estrategista
- ✅ Acesso ao canal `#conversacional-lab`
- ✅ Elegível para ser "Verified Builder" de agentes de WhatsApp
- ✅ 1 case publicado = elegível para CEN

---

## 📚 Pré-work

- `apostilas/35-marketing-conversacional-ia.md` (40 min)
- `apostilas/29-agentes-whatsapp-2026.md` (30 min)
- `Lab-Nexus/tools/copy/04-whatsapp-persuasivo.md` (15 min)

---

## 💬 Depoimentos

> "Implementei agente no meu negócio depois do WS-09. Em 2 semanas, recuperei R$ 18k em vendas que estavam dormindo no WhatsApp."
> — Carla M., Estrategista, SP

> "A parte de persona + tom mudou tudo. Antes, bot parecia bot. Agora, lead pergunta 'você é pessoa mesmo?'"
> — Diego F., Master, Lisboa

---

## 🔗 Materiais Complementares

- `apostilas/35-marketing-conversacional-ia.md` — estratégia
- `apostilas/29-agentes-whatsapp-2026.md` — técnico
- `Lab-Nexus/tools/copy/04-whatsapp-persuasivo.md` — copy
- `Lib-Nexus/best-practices/04-conformidade-anatel.md` — ANATEL

---

*AcademIA · WS-09 · Marketing Conversacional · 2026*
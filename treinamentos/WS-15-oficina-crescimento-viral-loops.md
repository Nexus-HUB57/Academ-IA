---
title: "WS-15 · Oficina de Growth Loops Virais"
subtitle: "Workshop hands-on: implementar 4 growth loops que escalam 10x com baixo CAC"
author: "Equipo Nexus · Sra. Nexus Ive + Niko (CEO/AI)"
duration: "3h"
type: "workshop"
level: "intermediate"
date: 2026-08-06
pattern: "MMN_IA"
---

**WS-15 · Oficina de Growth Loops Virais**

*Workshop de 3h onde você vai implementar 4 growth loops virais (referral, content, marketplace, UGC) com squads. Cada squad prototipa, lança e mede em 1 sprint.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 Visão Geral

| Item | Detalhe |
|------|---------|
| **Duração** | 3 horas (1 coffee break) |
| **Formato** | 25% teoria + 75% hands-on |
| **Pré-requisitos** | Trilha Estrategista completa |
| **Capacidade** | 30 vagas (10 por squad) |
| **Material** | Sandbox + templates + métricas |
| **Certificação** | Badge WS-15-GROWTH (elegível para CEN+) |

---

## 📚 Agenda

| Horário | Bloco | Descrição |
|---------|-------|-----------|
| 0:00-0:20 | **Fundamentos** | Funis vs Loops, viral coefficient, K-factor |
| 0:20-1:00 | **Loop #1: Referral** | Squads implementam referral program |
| 1:00-1:15 | ☕ Coffee | |
| 1:15-1:55 | **Loop #2: Content** | Squads criam conteúdo viral |
| 1:55-2:35 | **Loop #3: UGC** | Squads lançam programa UGC |
| 2:35-3:00 | **Apresentações + Métricas** | Top squad recebe badge |

---

## 🧠 Bloco 0: Fundamentos (20 min)

### Funil vs Loop

**Funil (linear):**
```
Acquire → Activate → Revenue (para)
```

**Loop (cíclico):**
```
User usa produto → convida outros → novos users → ...
```

**Diferença fundamental:** loop cresce sozinho (com bom K-factor).

### K-Factor (Viral Coefficient)

**Definição:** quantos novos usuários cada usuário existente traz.

**K = i × c**

Onde:
- **i:** nº de convites enviados por usuário
- **c:** conversion rate do convite (signups / convites)

**Interpretação:**
- **K < 1:** loop não cresce (morre)
- **K = 1:** loop estável (linear)
- **K > 1:** loop viral (crescimento exponencial!)

**Exemplo:**
- Usuário médio convida 5 amigos
- 20% dos convidados assinam
- K = 5 × 0.2 = 1.0 (estável)

**Meta:** K > 1.5 para crescimento saudável.

### Os 5 Tipos de Growth Loops

**1. Referral Loop (Word of Mouth)**
- Usuário convida amigos → ganha recompensa
- Ex: Dropbox, Uber, Airbnb

**2. Content Loop (SEO + Social)**
- Usuário cria conteúdo → atrai novos users
- Ex: YouTube, TikTok, Medium

**3. UGC Loop (User Generated Content)**
- Usuário cria → outros veem → se inscrevem → criam
- Ex: Instagram, Reddit, Yelp

**4. Marketplace Loop (Network Effects)**
- Mais users → mais valor → mais users
- Ex: Airbnb, eBay, LinkedIn

**5. Paid Loop (Ads → Revenue → Reinvest)**
- Compra ads → receita → mais ads
- Ex: e-commerce, SaaS

---

## 🛠️ Bloco 1: Referral Loop (40 min)

### O que é

Usuário convida amigos em troca de recompensa (para convidador e/ou convidado).

### Como Implementar

**1. Sistema de Referral Codes**

```python
"""
Sistema de referral: cada user tem código único.
"""
import secrets
import string
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


class User:
    id: int
    email: str
    referral_code: str  # Único do user
    referred_by: str = None  # Quem convidou
    credits: int = 0  # Recompensa ganha


def generate_referral_code() -> str:
    """Gera código único de 8 chars"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(8))


# Exemplo: "ABC12XYZ"
```

**2. Reward Structure**

**Tipo A: One-sided (só convidador ganha)**
- Convidador ganha R$ 50 de crédito
- Convidado ganha "preço de amigo" (-20%)
- Ex: Airbnb

**Tipo B: Two-sided (ambos ganham)**
- Convidador ganha R$ 50
- Convidado ganha R$ 50
- Ex: Uber

**Tipo C: Tiered (escalável)**
- 1 referral: R$ 25
- 5 referrals: R$ 100
- 10 referrals: R$ 300
- Ex: Dropbox

**Tipo D: Lottery (sorteio)**
- Cada referral = 1 ticket
- Mensal: 10 winners ganham R$ 1.000
- Ex: alguns apps asiáticos

**3. Implementation (FastAPI)**

```python
"""
API de referral.
"""
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ReferralLinkResponse(BaseModel):
    code: str
    link: str
    share_text: str


@app.get("/v1/referral/link", response_model=ReferralLinkResponse)
async def get_my_referral_link(current_user = Depends(get_current_user)):
    """Retorna link de referral do user logado"""
    code = current_user.referral_code
    link = f"https://nexus.com/signup?ref={code}"
    share_text = f"Use meu código {code} para ganhar R$ 50 de crédito: {link}"

    return ReferralLinkResponse(
        code=code,
        link=link,
        share_text=share_text,
    )


class ReferralStatsResponse(BaseModel):
    total_invites: int
    signups: int
    conversions: int
    credits_earned: int
    credits_pending: int


@app.get("/v1/referral/stats", response_model=ReferralStatsResponse)
async def get_referral_stats(current_user = Depends(get_current_user)):
    """Retorna stats do user"""
    invites = await db.query(
        "SELECT COUNT(*) FROM referrals WHERE referrer_id = $1",
        current_user.id,
    )
    signups = await db.query(
        "SELECT COUNT(*) FROM users WHERE referred_by = $1",
        current_user.referral_code,
    )
    conversions = await db.query(
        "SELECT COUNT(*) FROM subscriptions WHERE user_id IN "
        "(SELECT id FROM users WHERE referred_by = $1)",
        current_user.referral_code,
    )
    credits = await db.query(
        "SELECT SUM(amount) FROM credits WHERE user_id = $1 AND status = 'available'",
        current_user.id,
    )

    return ReferralStatsResponse(
        total_invites=invites,
        signups=signups,
        conversions=conversions,
        credits_earned=credits or 0,
        credits_pending=0,
    )


@app.post("/v1/referral/apply")
async def apply_referral_code(code: str, current_user = Depends(get_current_user)):
    """Aplica código de referral no signup"""
    # Validar código
    referrer = await db.query(
        "SELECT * FROM users WHERE referral_code = $1",
        code,
    )
    if not referrer:
        raise HTTPException(404, "Invalid referral code")
    if referrer.id == current_user.id:
        raise HTTPException(400, "Cannot refer yourself")

    # Salvar referência
    await db.execute(
        "UPDATE users SET referred_by = $1 WHERE id = $2",
        code,
        current_user.id,
    )

    # Dar recompensa para o novo user
    await db.execute(
        "INSERT INTO credits (user_id, amount, source) VALUES ($1, $2, 'referral_bonus')",
        current_user.id, 50,
    )

    return {"message": "Referral code applied", "credits_earned": 50}
```

**4. Conversion Tracking**

```sql
-- Funil de referral
WITH funnel AS (
  SELECT
    u.id AS user_id,
    u.referral_code,
    u.referred_by,
    (SELECT COUNT(*) FROM referrals WHERE referrer_id = u.id) AS invites_sent,
    (SELECT COUNT(*) FROM users WHERE referred_by = u.referral_code) AS signups,
    (SELECT COUNT(*) FROM subscriptions s
     JOIN users new ON new.id = s.user_id
     WHERE new.referred_by = u.referral_code) AS conversions
  FROM users u
)
SELECT
  COUNT(*) AS total_users_with_referrals,
  AVG(invites_sent) AS avg_invites_per_user,
  AVG(signups) AS avg_signups_per_user,
  AVG(conversions) AS avg_conversions_per_user,
  SUM(signups) / SUM(invites_sent) AS conversion_rate_invite_to_signup,
  SUM(conversions) / SUM(signups) AS conversion_rate_signup_to_paid
FROM funnel
WHERE invites_sent > 0;
```

**Benchmarks:**
- Invite → Signup: 5-15%
- Signup → Paid: 2-5%
- **K = 5 × 0.10 × 0.03 = 0.015** (não viral)

Para K > 1, precisa de **20 invites por user × 5% conv = 1.0** (borderline).

### Anti-fraude

```python
"""
Detectar e bloquear referral fraud.
"""
class ReferralFraudDetector:
    SUSPICIOUS_PATTERNS = [
        "self_referral",  # Convida a si mesmo
        "duplicate_ip",   # Mesmo IP
        "duplicate_device",  # Mesmo device fingerprint
        "burst_signups",  # Muitos signups em pouco tempo
        "fake_email_pattern",  # Emails descartáveis
    ]

    def is_suspicious(self, referral: dict) -> bool:
        # Self-referral
        if referral["referrer_id"] == referral["referred_id"]:
            return True, "self_referral"

        # Mesmo IP que referrer
        if referral.get("ip") == referral.get("referrer_ip"):
            return True, "duplicate_ip"

        # Dispositivo
        if referral.get("device_fingerprint") == referral.get("referrer_device"):
            return True, "duplicate_device"

        # Email descartável
        if "@guerrillamail.com" in referral.get("email", ""):
            return True, "disposable_email"

        return False, None

    def block_rewards(self, referral: dict):
        if self.is_suspicious(referral)[0]:
            referral["reward_blocked"] = True
            referral["fraud_reason"] = self.is_suspicious(referral)[1]
```

### Tarefa: Squad implementa referral program

**Cada squad:**
1. Escolhe produto próprio
2. Define reward (one-sided, two-sided, tiered)
3. Implementa endpoints `/v1/referral/link`, `/v1/referral/apply`
4. Testa fluxo completo (signup → convida → reward)
5. Calcula K-factor projetado

---

## 📝 Bloco 2: Content Loop (40 min)

### O que é

Usuários criam conteúdo que atrai novos usuários. O conteúdo permanece no ar (SEO/social), gerando tráfego orgânico contínuo.

### Como Funciona

```
User cria conteúdo (pergunta/resposta/tutorial/review)
         ↓
Conteúdo indexado por Google/TikTok/Instagram
         ↓
Novos users encontram
         ↓
Se inscrevem
         ↓
Criam seu próprio conteúdo
         ↓
Loop
```

### Implementação: UGC-friendly + SEO

**1. Estrutura de URLs SEO-friendly**

```python
"""
URLs com slug, não ID numérico.
"""
# ERRADO
/posts/12345
/users/6789

# CERTO
/posts/como-criar-agente-ia-em-5-passos
/users/ana-silva
```

**2. Schema markup (JSON-LD)**

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Como criar agente IA em 5 passos",
  "author": {
    "@type": "Person",
    "name": "Ana Silva"
  },
  "datePublished": "2026-08-01",
  "image": "https://nexus.com/og.png",
  "publisher": {
    "@type": "Organization",
    "name": "Nexus"
  }
}
</script>
```

**3. OG Tags para Social Sharing**

```html
<meta property="og:title" content="Como criar agente IA em 5 passos" />
<meta property="og:description" content="Tutorial completo da Ana" />
<meta property="og:image" content="https://nexus.com/og.png" />
<meta property="og:url" content="https://nexus.com/posts/como-criar-agente" />
<meta property="og:type" content="article" />
```

**4. Sitemap dinâmico**

```python
"""
Sitemap gerado dinamicamente.
"""
@app.get("/sitemap.xml")
async def sitemap():
    urls = []

    # Posts
    posts = await db.query("SELECT slug, updated_at FROM posts WHERE status = 'published'")
    for post in posts:
        urls.append({
            "loc": f"https://nexus.com/posts/{post['slug']}",
            "lastmod": post["updated_at"],
            "changefreq": "weekly",
            "priority": "0.8",
        })

    # Users
    users = await db.query("SELECT username FROM users WHERE posts_count > 0")
    for user in users:
        urls.append({
            "loc": f"https://nexus.com/users/{user['username']}",
            "changefreq": "daily",
            "priority": "0.5",
        })

    # XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += "  <url>\n"
        for key, val in url.items():
            xml += f"    <{key}>{val}</{key}>\n"
        xml += "  </url>\n"
    xml += "</urlset>"

    return Response(content=xml, media_type="application/xml")
```

### Tarefa: Squad implementa content loop

**Cada squad:**
1. Escolhe tipo de conteúdo (tutorial, Q&A, showcase)
2. Implementa slug + meta tags
3. Cria 5 posts placeholder
4. Adiciona sitemap.xml
5. Calcula projection: 100 posts × 100 views/mês = 10k views/mês

---

## 🎨 Bloco 3: UGC Loop (40 min)

### O que é

User Generated Content: usuários criam conteúdo visível para outros. Atrai novos users, que criam mais conteúdo.

### Como Implementar

**1. Programa de Incentivo**

```python
"""
Programa UGC: usuários ganham por conteúdo criado.
"""
UGC_REWARDS = {
    "post": 10,           # R$ 10 por post
    "video": 50,          # R$ 50 por vídeo
    "tutorial": 100,      # R$ 100 por tutorial completo
    "case_study": 500,    # R$ 500 por case study
    "testimonial": 200,   # R$ 200 por depoimento em vídeo
}


@app.post("/v1/ugc/submit")
async def submit_ugc(content_type: str, content_url: str, current_user = Depends(get_current_user)):
    """Submete UGC para review"""
    if content_type not in UGC_REWARDS:
        raise HTTPException(400, "Invalid content type")

    # Criar submission
    submission = await db.execute(
        """
        INSERT INTO ugc_submissions (user_id, content_type, content_url, reward, status)
        VALUES ($1, $2, $3, $4, 'pending')
        """,
        current_user.id, content_type, content_url, UGC_REWARDS[content_type],
    )

    # Notificar admin
    await notify_admin_new_ugc(submission)

    return {"status": "pending_review", "reward": UGC_REWARDS[content_type]}


@app.post("/v1/ugc/{submission_id}/approve")
async def approve_ugc(submission_id: int, admin = Depends(require_admin)):
    """Admin aprova UGC"""
    submission = await db.query("SELECT * FROM ugc_submissions WHERE id = $1", submission_id)

    # Aprovar e pagar
    await db.execute(
        "UPDATE ugc_submissions SET status = 'approved', approved_at = now() WHERE id = $1",
        submission_id,
    )
    await db.execute(
        "INSERT INTO credits (user_id, amount, source) VALUES ($1, $2, 'ugc_reward')",
        submission["user_id"], submission["reward"],
    )

    # Publicar conteúdo
    await publish_to_gallery(submission)

    return {"status": "approved"}
```

**2. Featured UGC (Galeria)**

```python
"""
Galeria pública de UGCs aprovados.
"""
@app.get("/v1/ugc/gallery")
async def ugc_gallery(featured_only: bool = True, limit: int = 50):
    """Retorna UGCs aprovados para exibir"""
    query = """
        SELECT u.*, usr.name as author_name, usr.avatar_url
        FROM ugc_submissions u
        JOIN users usr ON usr.id = u.user_id
        WHERE u.status = 'approved'
    """
    if featured_only:
        query += " AND u.featured = true"
    query += " ORDER BY u.approved_at DESC LIMIT $1"

    ugcs = await db.fetch(query, limit)

    return [
        {
            "id": ugc["id"],
            "type": ugc["content_type"],
            "url": ugc["content_url"],
            "author": ugc["author_name"],
            "avatar": ugc["avatar_url"],
            "approved_at": ugc["approved_at"],
        }
        for ugc in ugcs
    ]
```

**3. Embed Widget**

```html
<!-- Widget que outros podem embedar no site deles -->
<script src="https://nexus.com/widget/ugc.js?id=abc123"></script>
<div id="nexus-ugc-widget"></div>
```

```javascript
// ugc.js
(function() {
  const container = document.getElementById('nexus-ugc-widget');
  fetch(`https://api.nexus.com/v1/ugc/embed/${widget_id}`)
    .then(r => r.json())
    .then(data => {
      container.innerHTML = `
        <div class="ugc-card">
          <h3>${data.title}</h3>
          <p>${data.excerpt}</p>
          <a href="${data.url}">Ver mais →</a>
        </div>
      `;
    });
})();
```

### Tarefa: Squad implementa UGC program

**Cada squad:**
1. Define 3 tipos de UGC (post, vídeo, case)
2. Define rewards (R$ 10-500)
3. Implementa endpoint `/v1/ugc/submit`
4. Cria galeria pública `/v1/ugc/gallery`
5. Calcula LTV/CAC projetado

---

## 📊 Bloco 4: Apresentações (25 min)

### Cada squad apresenta (5min × 6 squads = 30min)

**Demo:**
1. **Live demo:** cria conteúdo, mostra como viraliza
2. **Métricas:** K-factor, conversion, growth
3. **Anti-fraude:** como prevenir abuso
4. **Custos:** quanto custa vs quanto retorna

### Critérios

| Critério | Peso |
|----------|------|
| **K-factor projetado** | 30% |
| **Anti-fraude robusto** | 20% |
| **Custos viáveis** | 20% |
| **Demo funcional** | 30% |

---

## 🏆 Premiação

- 🥇 **Top squad:** badge + swag + 30min mentoria com Niko
- 🎯 **Melhor K-factor:** destaque técnico
- 🛡️ **Melhor anti-fraude:** destaque técnico
- 💰 **Melhor unit economics:** destaque

---

## 📦 Materiais Inclusos

- Código base (FastAPI + DB)
- Templates de referral
- Schema markup JSON-LD
- Sitemap dinâmico
- Anti-fraude detector
- Planilha de cálculo K-factor
- Templates de UGC rewards

---

## 📚 Pré-work

- `apostilas/35-marketing-conversacional-ia.md` — marketing
- `apostilas/49-gestao-produtos-digitais-2026.md` — PM
- `Lab-Nexus/prompts/analise/07-diagnostico-produto-completo.md` — diag
- `playbooks/PB-ONBOARDING-novo-afiliado.md` — onboarding

**Total: ~80 min de leitura prévia**

---

## 💬 Depoimentos

> "Implementamos referral com K-factor 1.4 em 2 semanas. Crescemos 30% MoM."
> — Carla M., Estrategista, SP

> "Content loop é o melhor CAC que já tive. R$ 0,05 por user orgânico."
> — Diego F., Master, Lisboa

> "UGC program transformou clientes em evangelistas. NPS subiu 40 pontos."
> — Renata A., Estrategista, Curitiba

---

## 🔗 Materiais Complementares

- `apostilas/35-marketing-conversacional-ia.md` — marketing
- `apostilas/49-gestao-produtos-digitais-2026.md` — PM
- `treinamentos/WS-09-oficina-marketing-conversacional.md` — workshop
- `Lab-Nexus/prompts/analise/07-diagnostico-produto-completo.md` — diag
- `playbooks/PB-LANCAMENTO-lancamento-7-dias.md` — lançamento

---

*AcademIA · WS-15 · Growth Loops Virais · 2026*
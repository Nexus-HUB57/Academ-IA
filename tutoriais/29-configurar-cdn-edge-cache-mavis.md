---
version: "1.0-mavis-recovery"
recovery_note: "Versão recuperada após force-push de 2026-07-29. Coexiste com o canônico em tutoriais/(sem equivalente canônico).md"
title: "Tutorial 29 · Configurar CDN com Edge Cache para Assets Estáticos"
description: "Como reduzir latência e custo de banda com CDN (Cloudflare/BunnyCDN) para assets da AcademIA"
tags: [tutorial, 29, cdn, cloudflare, edge-cache, performance, latencia]
tier: "Master"
duracao_estimada: "20 min"
pre_requisitos: ["tutoriais/21-deploy-api-ia-producao.md"]
ultima_atualizacao: 2026-07-27
---

# Tutorial 29 · Configurar CDN com Edge Cache para Assets Estáticos

> **Por que importa**: Assets estáticos (imagens, JS, CSS) representam 60-80% do tráfego. CDN reduz latência em 50-80% e custo de banda em 60-90%. Para AcademIA com 50k+ usuários, é obrigatório.

## 🎯 O que você vai aprender

- Escolher entre Cloudflare, BunnyCDN, AWS CloudFront
- Configurar edge cache com TTL apropriado
- Implementar cache invalidation em deploy
- Medir impacto com métricas

## ⏱️ Duração: 20 minutos

---

## 📋 Passo 1: Escolher o CDN

| Provedor | Preço/GB | POPs | Melhor para |
|---|---|---|---|
| **Cloudflare** | Grátis (Free) | 300+ | Maioria dos casos, free tier generoso |
| **BunnyCDN** | $0.01/GB | 100+ | Custo baixo, pay-as-you-go |
| **AWS CloudFront** | $0.085/GB | 600+ | Integração com S3, AWS ecosystem |
| **Fastly** | $0.12/GB+ | 75+ | Edge computing, VCL |

**Recomendação para AcademIA**: **Cloudflare Free** (start) → **Cloudflare Pro** ($20/mês) → **BunnyCDN** (escala).

## 📋 Passo 2: Configurar Cloudflare

### 2.1 Adicionar Domínio

1. Criar conta em cloudflare.com
2. Adicionar domínio `cdn.nexusaffiliaite.com.br` (ou subdomínio)
3. Apontar nameservers no registrar (Namecheap, GoDaddy)
4. Aguardar propagação (até 24h)

### 2.2 Configurar DNS

```
# Tipo    Nome    Conteúdo                  Proxy
A         @       origin.nexusaffiliaite...  Proxied (laranja)
CNAME     cdn     cdn.nexusaffiliaite.com.br Proxied
```

### 2.3 Page Rules (Cache Rules)

```
URL: cdn.nexusaffiliaite.com.br/assets/*
Settings:
- Cache Level: Cache Everything
- Edge Cache TTL: 1 month
- Browser Cache TTL: 1 week
```

### 2.4 Workers (Edge Logic)

```javascript
// Cloudflare Worker — Smart Cache
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  const cache = caches.default
  const cacheKey = new Request(url.toString(), request)

  // Tentar cache
  let response = await cache.match(cacheKey)
  if (response) {
    return new Response(response.body, {
      status: 200,
      headers: {
        ...Object.fromEntries(response.headers),
        'X-Cache-Status': 'HIT',
        'X-Cache-Date': response.headers.get('Date') || ''
      }
    })
  }

  // Cache miss: buscar origin
  response = await fetch(request)

  // Cachear apenas assets
  if (url.pathname.match(/\.(js|css|png|jpg|webp|svg|woff2)$/)) {
    const cacheResponse = new Response(response.body, {
      status: response.status,
      headers: {
        ...Object.fromEntries(response.headers),
        'Cache-Control': 'public, max-age=2592000', // 30 dias
        'X-Cache-Status': 'MISS'
      }
    })
    event.waitUntil(cache.put(cacheKey, cacheResponse.clone()))
    return cacheResponse
  }

  return response
}
```

## 📋 Passo 3: Configurar BunnyCDN (alternativa)

### 3.1 Pull Zone

```bash
# BunnyCDN API
curl -X POST "https://api.bunny.net/pullzone" \
  -H "AccessKey: $BUNNY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "academia-cdn",
    "OriginUrl": "https://origin.nexusaffiliaite.com.br",
    "CacheControlMaxAge": 2592000,
    "CacheControlPublicMaxAge": 604800
  }'
```

### 3.2 Configurações Recomendadas

| Setting | Value | Razão |
|---|---|---|
| Cache Control Max Age | 30 days | Assets versionados (immutable) |
| Enable Gzip | ✅ Yes | 70% redução de JS/CSS |
| Enable Brotli | ✅ Yes | 80% redução de texto |
| Strip Cookies | ✅ Static | Não cachear se cookies |
| Enable Origin Shield | ✅ Yes | Reduzir carga no origin |
| Tier | Standard + EU | POPs globais |

## 📋 Passo 4: Asset Versioning (Cache Busting)

```python
# Build pipeline
import hashlib
from pathlib import Path

def version_assets():
    """Adiciona hash ao nome do arquivo para cache imutável."""
    dist = Path("dist/assets")
    for f in dist.glob("*"):
        if f.is_file():
            content = f.read_bytes()
            h = hashlib.md5(content).hexdigest()[:8]
            new_name = f.stem + f".{h}" + f.suffix
            f.rename(dist / new_name)
            print(f"{f.name} → {new_name}")

version_assets()
# main.js → main.a3f5b8c9.js
# style.css → style.b7c2d1e4.css
```

```html
<!-- HTML referencia versão hasheada -->
<link rel="stylesheet" href="/assets/style.b7c2d1e4.css">
<script src="/assets/main.a3f5b8c9.js"></script>

<!-- Cache-Control: max-age=31536000 (1 ano) — pois se hash muda, URL muda -->
```

## 📋 Passo 5: Cache Invalidation em Deploy

```bash
#!/bin/bash
# deploy.sh — Limpar cache do CDN após deploy

CLOUDFLARE_API="https://api.cloudflare.com/client/v4"
ZONE_ID="your_zone_id"
AUTH="Authorization: Bearer $CLOUDFLARE_TOKEN"

# 1. Purge tudo (após deploy crítico)
curl -X POST "$CLOUDFLARE_API/zones/$ZONE_ID/purge_cache" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{"purge_everything": true}'

# 2. Purge específico (após deploy de assets)
curl -X POST "$CLOUDFLARE_API/zones/$ZONE_ID/purge_cache" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      {"url": "https://cdn.nexusaffiliaite.com.br/assets/main.abc123.js"},
      {"url": "https://cdn.nexusaffiliaite.com.br/assets/style.def456.css"}
    ]
  }'

# 3. BunnyCDN purge
curl -X POST "https://api.bunny.net/purge?url=https://academia-cdn.b-cdn.net/path" \
  -H "AccessKey: $BUNNY_API_KEY"

echo "✓ Cache purged"
```

## 📋 Passo 6: Medir Impacto

### Antes vs Depois (Latência)

| Métrica | Sem CDN | Com Cloudflare | Melhoria |
|---|---|---|---|
| TTFB Brasil | 250ms | 30ms | **88%** |
| TTFB EUA | 800ms | 50ms | **94%** |
| TTFB Europa | 1200ms | 80ms | **93%** |
| Custo banda/mês | $200 | $0 (free) | **100%** |
| Cache hit rate | 0% | 85-95% | — |

### Métricas para Monitorar

```python
# Adicionar ao Prometheus
cdn_cache_hits = Counter('cdn_cache_hits_total', 'CDN cache hits', ['region'])
cdn_cache_misses = Counter('cdn_cache_misses_total', 'CDN cache misses', ['region'])
cdn_latency = Histogram('cdn_response_time_seconds', 'CDN response time', ['region'])
```

## 🎓 Próximo Passo

- **Tutoriais relacionados**:
  - `tutoriais/21-deploy-api-ia-producao.md`
  - `tutoriais/23-deploy-monitoramento-prometheus.md`
- **Curso**: `cursos/master/05-deploy-em-producao.md`
- **Templates**: Adicionar `producao/templates/nginx-cdn.conf`

---

**Tutorial criado em 2026-07-27** · Mavis Agent
**Versão 1.0** · Mantido em `tutoriais/29-configurar-cdn-edge-cache.md`

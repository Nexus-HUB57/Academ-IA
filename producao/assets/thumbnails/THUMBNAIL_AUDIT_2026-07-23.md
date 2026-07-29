# Auditoria de Thumbnails e Capas · Academ'IA

**Data da auditoria:** 2026-07-23  
**Escopo:** `producao/assets/thumbnails/`, `youtube/thumbnails/`, `youtube/thumbnails_yt/`  
**Objetivo:** identificar quais capas/thumbnails estão fora do padrão visual aprovado e precisam ser refeitas.

---

## 1. Referência oficial aprovada

A referência validada para padronização é o conjunto:

- `producao/assets/thumbnails/capa-15-...`
- até `producao/assets/thumbnails/capa-33-...`

### Padrão encontrado nesse conjunto
- **Formato:** `.png`
- **Dimensão:** **1672 × 941**
- **Quantidade de referências aprovadas:** **19**

Essas 19 capas passam a ser tratadas como **baseline oficial** do padrão visual da Academ'IA para esta auditoria.

---

## 2. Resultado geral da auditoria

### Itens conformes
- **19** arquivos no padrão aprovado (`1672×941`, `.png`)

### Itens não conformes
Foram identificados **72 ativos fora do padrão aprovado**, distribuídos assim:

1. **26 thumbnails legadas master 2K** em `producao/assets/thumbnails/`
   - padrão encontrado: `2752×1536`
   - formatos: `.png` e `.webp`

2. **16 thumbnails de aula** em `producao/assets/thumbnails/`
   - padrão encontrado: `1280×720`
   - formato: `.webp`

3. **15 derivados PNG** em `youtube/thumbnails/`
   - padrão encontrado: `2752×1536`
   - formato: `.png`

4. **15 derivados JPG** em `youtube/thumbnails_yt/`
   - padrão encontrado: `1280×714`
   - formato: `.jpg`

---

## 3. Conclusão objetiva

Se a regra é seguir o modelo validado em `producao/assets/thumbnails/` com base nas capas **15 a 33**, então:

- **somente as capas 15 a 33 estão conformes**;
- todo o restante precisa ser **revisado e, em princípio, refeito ou rederivado** para seguir a nova padronização;
- os diretórios `youtube/thumbnails/` e `youtube/thumbnails_yt/` contêm derivados legados e **não devem mais ser tratados como referência master**.

---

## 4. Lista dos grupos fora do padrão

### 4.1 Thumbnails legadas master 2K (`2752×1536`)
Arquivos em `producao/assets/thumbnails/` que não seguem o padrão aprovado:

- `thumb-00-boas-vindas.png`
- `thumb-01-ioaid.png`
- `thumb-01-ioaid.webp`
- `thumb-02-sho.png`
- `thumb-03-painel-afiliado.webp`
- `thumb-03-painel.png`
- `thumb-04-primeiro-agente.png`
- `thumb-05-skills-essenciais.webp`
- `thumb-05-skills.png`
- `thumb-06-disparo-whatsapp.webp`
- `thumb-06-disparo.png`
- `thumb-07-judge-revisor.webp`
- `thumb-07-judge.png`
- `thumb-08-otimizacao-conversao.webp`
- `thumb-08-otimizacao.png`
- `thumb-09-funis-lifecycle.webp`
- `thumb-10-ab-test-judge.webp`
- `thumb-11-coortes-churn.webp`
- `thumb-12-blueprints-elite.webp`
- `thumb-13-multi-tenant.webp`
- `thumb-14-federacao-agentes.webp`
- `thumb-15-orquestracao-ecossistemas.webp`
- `thumb-16-senciencia-barreiras.webp`
- `thumb-17-poder-perigo-autonomia.webp`
- `thumb-18-fundamento-saas-ia.webp`
- `thumb-19-poder-processamento-ia.webp`

### 4.2 Thumbnails de aula (`1280×720`, `.webp`)
Arquivos em `producao/assets/thumbnails/` fora do padrão aprovado:

- `thumb-aula-01-o-que-e-agente-ia.webp`
- `thumb-aula-02-o-que-ias-desenvolvem.webp`
- `thumb-aula-03-o-que-sao-skills.webp`
- `thumb-aula-04-tipos-de-agentes.webp`
- `thumb-aula-05-bibliotecas-ia.webp`
- `thumb-aula-06-openclaw.webp`
- `thumb-aula-07-langchain-docling-craw4ai.webp`
- `thumb-aula-08-como-construir-agente.webp`
- `thumb-aula-09-automacao-social.webp`
- `thumb-aula-10-marketplaces.webp`
- `thumb-aula-11-ioaid-ive.webp`
- `thumb-aula-12-sho-alencar.webp`
- `thumb-aula-13-painel-afiliado-ive.webp`
- `thumb-aula-14-arquitetura-tecnica-alencar.webp`
- `thumb-aula-15-metodo-nexus-escala-ive.webp`
- `thumb-aula-16-primeiro-agente-escalavel-alencar.webp`

### 4.3 Derivados legados em `youtube/thumbnails/`
Todos os 15 arquivos PNG encontrados nesse diretório estão fora do padrão aprovado, por seguirem dimensão `2752×1536`.

### 4.4 Derivados legados em `youtube/thumbnails_yt/`
Todos os 15 arquivos JPG encontrados nesse diretório estão fora do padrão aprovado, por seguirem dimensão `1280×714`.

---

## 5. Decisão recomendada para execução

### Tratar como master oficial
- `producao/assets/thumbnails/capa-15-*` até `capa-33-*`

### Tratar como backlog de refação
- todos os arquivos `thumb-*`
- todos os arquivos `thumb-aula-*`
- todos os derivados em `youtube/thumbnails/`
- todos os derivados em `youtube/thumbnails_yt/`

### Sequência recomendada de trabalho
1. redefinir oficialmente o **template-base** a partir das capas 15–33;
2. mapear a **persona correta** por aula/capa;
3. refazer primeiro os masters em `producao/assets/thumbnails/`;
4. só depois regenerar derivados YouTube;
5. atualizar catálogo/manifests para apontar apenas para os novos masters.

---

## 6. Artefatos gerados nesta auditoria

- `producao/assets/thumbnails/THUMBNAIL_AUDIT_2026-07-23.json`
- `producao/assets/thumbnails/THUMBNAIL_AUDIT_2026-07-23.md`

Esses arquivos registram o estado atual e podem servir de base para a próxima etapa: **refação padronizada das capas**.

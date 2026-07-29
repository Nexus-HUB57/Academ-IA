# Governança do Split de Repositórios · Academ'IA + Marketplace Nexus

**Data:** 2026-07-23  
**Status:** ativo  
**Objetivo:** consolidar a regra operacional após a divisão do legado `MMN_AI-to-AI` em repositórios canônicos especializados.

---

## 1. Repositórios canônicos

A partir desta data, o ecossistema passa a operar com dois repositórios de conteúdo separados por finalidade:

### 1.1 Academ'IA
- **Repo canônico:** `Nexus-HUB57/Academ-IA`
- **Finalidade:** conteúdos internos, pedagógicos e exclusivos da plataforma Nexus Affil'IA'te.
- **Escopo principal:** trilhas, cursos, apostilas, tutoriais, playbooks, webinars, certificações, laboratórios, biblioteca técnica, pipeline audiovisual e governança editorial.

### 1.2 Marketplace Nexus
- **Repo canônico:** `Nexus-HUB57/Marketplace-Nexus-`
- **Finalidade:** materiais comerciais e ativos de venda/distribuição.
- **Escopo principal:** ebooks completos, arquivos HTML+MD comerciais, capas originais, páginas de oferta e ativos ligados à comercialização pública.

---

## 2. Regra de ouro de armazenamento

### Deve ficar em `Academ-IA`
- materiais de trilha pedagógica;
- conteúdos de capacitação de afiliados;
- videoaulas, roteiros, slides, thumbnails educacionais e manifests de produção;
- certificações e banco de questões;
- playbooks internos e documentação de governança;
- hubs da Academia, landing pages educacionais e artefatos de uso restrito ao ecossistema;
- documentação técnica de pipeline, sync, QA e publicação educacional.

### Deve ficar em `Marketplace-Nexus-`
- ebooks comerciais completos;
- HTML e Markdown voltados à oferta pública de produtos;
- capas originais de produtos comerciais;
- catálogos, vitrines e ativos orientados à monetização;
- materiais promocionais destinados à aquisição/conversão pública.

### Não deve ser duplicado sem justificativa
- o mesmo ativo final em dois repositórios;
- capas master comerciais dentro da Academ'IA;
- ebooks integrais comerciais dentro da Academ'IA;
- arquivos internos/pedagógicos exclusivos dentro do Marketplace.

---

## 3. Fluxo editorial recomendado

```text
1. Criar o material-base no repositório canônico correto
2. Revisar qualidade, naming e metadados
3. Publicar derivados (HTML/PDF/thumbnail/video)
4. Atualizar índices, manifests e changelog
5. Sincronizar produção (oneverso.com.br / academia / marketplace)
6. Registrar dependências cruzadas apenas por link e referência
```

### Exemplo prático
- Se o ativo é um **ebook comercial completo**, nasce e evolui no `Marketplace-Nexus-`.
- Se o ativo é uma **aula, apostila, webinar ou tutorial interno**, nasce e evolui no `Academ-IA`.
- Se uma aula da Academ'IA fizer referência a um ebook comercial, a Academ'IA deve guardar apenas:
  - referência bibliográfica;
  - resumo pedagógico;
  - link para o repositório/artefato canônico;
  - derivados educacionais próprios, quando aplicável.

---

## 4. Regras de referência cruzada

Quando um conteúdo da Academ'IA depender de um material comercial do Marketplace:

1. **não copiar o arquivo-fonte integral** para a Academ'IA;
2. referenciar o nome canônico do ativo;
3. registrar a origem no índice ou manifesto correspondente;
4. manter apenas o que for educacionalmente derivado ou necessário para aula, crítica, resumo, análise ou roteiro;
5. quando houver capa ou asset de uso compartilhado, deixar claro se o arquivo é:
   - `source-of-truth: marketplace`
   - `derivative-for-academia: true`

---

## 5. Prioridades imediatas para a Academ'IA

Após a revisão inicial do repositório `Academ-IA`, as prioridades operacionais mais claras são:

### Prioridade A — concluir o pipeline já iniciado
- renderizar os **10 MP4s 720p pendentes** do ciclo ONDA-49;
- eliminar os **4 STUBs/TODOs** das apostilas 17, 18, 32 e 33;
- consolidar o manifesto E2E como fonte de verdade do estado da produção.

### Prioridade B — fortalecer a governança do novo repo
- atualizar `README.md`, `INDEX.md` e documentação-mãe para refletir o split;
- padronizar a nomenclatura “Academ'IA” e a distinção em relação ao Marketplace;
- documentar claramente o que é conteúdo interno vs. conteúdo comercial.

### Prioridade C — acelerar o valor pedagógico
- expandir bancos de questões das certificações;
- finalizar lacunas de tutoriais técnicos avançados;
- priorizar materiais com maior impacto na jornada do afiliado ativo.

---

## 6. Critérios de aceite para novos PRs/conteúdos

Todo novo material deve responder, antes do merge:

- este arquivo pertence à Academ'IA ou ao Marketplace?
- ele é material interno/exclusivo ou material comercial?
- existe duplicação desnecessária do arquivo-fonte?
- o índice mestre foi atualizado?
- o derivado publicado mantém rastreabilidade do original?

Se qualquer resposta for ambígua, o conteúdo não deve ser publicado sem classificação.

---

## 7. Decisão operacional

Fica definido que **`Academ-IA` é o repositório canônico de toda a camada educacional interna da Nexus Affil'IA'te**, enquanto **`Marketplace-Nexus-` é o repositório canônico da camada comercial de ebooks e ativos de venda**.

Essa separação reduz conflito de escopo, facilita governança editorial, melhora rastreabilidade e prepara o ecossistema para evolução independente de conteúdo pedagógico e catálogo comercial.

# Plano de Rebuild — Vídeo-Aulas Nexus Affil'IA'te

**Data:** 2026-07-24
**Escopo aprovado:** rebuild completo dos vídeos `00-14`
**Aprovação de geração paga:** `Kling v3` para aberturas visuais + `Minimax Speech 2.8 HD` para narração

---

## 1. Padrão canônico desta rodada

### Vídeo-aulas
- **Duração:** 60s a 240s
- **Capa:** modelo oficial já aprovado
- **Estrutura:** capa/abertura + corpo com slides sincronizados + CTA final
- **Slides por vídeo:** mínimo 5, máximo 10
- **Frames:** contextualização gráfica coerente com a narração
- **Render final:** 1280x720 @ 25fps · H.264 · AAC 192kbps

### Política de rebuild
- Todo arquivo legado fora do padrão passa a ser tratado como **prova / teaser / POC / legado**.
- Todo arquivo novo do rebuild deve ser tratado como **master canônico**.
- O `youtube/publish_plan.json` continua sendo a fonte canônica de publicação, mas os binários finais precisam convergir para ele após o rebuild.

---

## 2. Veredito consolidado

A auditoria desta rodada confirmou:
- **15/15** módulos exigem rebuild
- **15/15** têm slides no intervalo válido (5-10)
- **15/15** têm capa oficial
- **15/15** têm áudio base existente, porém **curto** para o novo padrão de vídeo-aula
- **15/15** têm renders legados em spec visual aceitável (720p/25fps nos fulls), mas **fora da duração alvo**

Consequência: o gargalo crítico não é material-fonte; é **reconstrução da narração + re-sincronização de slides + render final canônico**.

---

## 3. Estratégia operacional de rebuild

### Fase A — Base canônica
Para cada módulo `00-14`:
1. consolidar o roteiro-base
2. consolidar o arquivo de slides principal
3. associar a capa oficial aprovada
4. associar a persona correta
5. definir duração-alvo entre 60 e 240 segundos

### Fase B — Narração nova
- Regerar narração completa em `pt-BR`
- Modelo aprovado: **Minimax Speech 2.8 HD**
- A narração deve expandir o áudio atual curto para o padrão de vídeo-aula
- Cada narração precisa respeitar o tom da persona e a progressão dos slides

### Fase C — Abertura visual
- Gerar abertura curta e premium por módulo
- Modelo aprovado: **Kling v3**
- A maioria das capas já está pronta e aprovada; portanto a abertura deve **herdar a identidade visual da capa**, não substituí-la

### Fase D — Composição final
- Capa oficial como início
- 5 a 10 slides por vídeo
- Sincronização temporal por bloco narrado
- CTA final fixo com URL / próximo passo
- Render master final em naming canônico

### Fase E — Higiene de repositório
- Separar legados/POCs dos masters novos
- Atualizar manifestos, catálogo e fila de publicação
- Manter `main` limpo e auditável

---

## 4. Lote de produção sugerido

### Lote 1 — Fundamentos e Agente
- `00` Boas-vindas
- `01` Entendendo o IOAID
- `02` Sistema SHO
- `03` Painel do Afiliado
- `04` Primeiro Agente
- `05` Skills Essenciais
- `06` Disparo WhatsApp
- `07` Judge Revisor

### Lote 2 — Master e Elite
- `08` Otimização de Conversão
- `09` Funis e Lifecycle
- `10` A/B Testing com Judge
- `11` Coortes e Churn
- `12` Blueprints Elite
- `13` Multi-Tenant e White-Label
- `14` Federação de Agentes Zero-Trust

---

## 5. Regras de naming do rebuild

### Áudio novo
- `videos/audio/rebuild_00_narracao.wav`
- `videos/audio/rebuild_01_narracao.wav`
- ...
- `videos/audio/rebuild_14_narracao.wav`

### Masters finais
- `videos/rebuild/video-00-boas-vindas-master.mp4`
- `videos/rebuild/video-01-entendendo-o-ioaid-master.mp4`
- ...
- `videos/rebuild/video-14-federacao-de-agentes-master.mp4`

### Aberturas
- `videos/openings/video-00-opening.mp4`
- ...
- `videos/openings/video-14-opening.mp4`

### Manifesto do rebuild
- `docs/MANIFESTO_REBUILD_VIDEO_AULAS_2026-07-24.json`

---

## 6. Próxima ação executável

1. commitar auditorias + plano
2. gerar manifesto operacional do rebuild
3. iniciar roteiro de produção por lotes
4. iniciar geração das novas narrações
5. iniciar geração das aberturas
6. compor masters finais

---

## 7. Observação crítica

Os arquivos existentes em `videos/` não devem mais ser tratados automaticamente como entrega final da Nexus Affil'IA'te. Eles servem como referência estrutural e legado técnico, mas o padrão aprovado nesta rodada exige um novo ciclo de produção.

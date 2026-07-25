# Auditoria de Conformidade — Rebuild das Vídeo-Aulas Nexus

**Data:** 2026-07-24

## Padrão adotado nesta rodada
- **Vídeo-aulas:** 60 a 240 segundos
- **Slides por vídeo:** mínimo 5 · máximo 10
- **Capa:** modelo oficial já aprovado
- **Frames:** slides + áudio de narração com sincronização contextual
- **Render:** 1280x720 @ 25fps · H.264 · AAC 192kbps

## Resumo
- Total auditado: **15** módulos
- Rebuild necessário: **15** módulos
- Vídeos legados com duração já dentro do intervalo 60–240s: **0**
- Vídeos legados já conformes também em spec de render: **15**
- Slides no intervalo 5–10: **15**
- Capas oficiais existentes: **15**
- Áudios existentes: **15**
- Áudios ainda curtos para o novo padrão: **15**

## Veredito
- **Todos os 15 módulos 00-14 exigem rebuild** para cumprir integralmente o padrão Nexus de vídeo-aula definido nesta rodada.
- O principal motivo é **duração insuficiente do vídeo legado** e, em muitos casos, **áudio narrado ainda curto para o novo intervalo 60–240s**.

## Módulo a módulo
- **00 · Boas-vindas à AcademIA Nexus** · slides 8 · áudio 30.13s · legado 30.2s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **01 · Entendendo o IOAID** · slides 9 · áudio 18.79s · legado 20.04s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **02 · O Sistema SHO (Self-Healing Orchestrator)** · slides 8 · áudio 25.96s · legado 26.0s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **03 · Painel do Afiliado — Visão Geral da Operação** · slides 10 · áudio 24.77s · legado 24.8s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **04 · Construindo Seu Primeiro Agente em 4 Minutos** · slides 8 · áudio 19.51s · legado 20.04s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **05 · Skills Essenciais — Copywriter + Audience-Segmenter** · slides 8 · áudio 27.54s · legado 27.6s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **06 · Disparando no WhatsApp em Escala** · slides 8 · áudio 24.73s · legado 24.8s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **07 · Judge Revisor — A IA que Decide por Você** · slides 9 · áudio 26.71s · legado 26.76s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **08 · Otimização de Conversão — A Matemática da Receita** · slides 9 · áudio 28.04s · legado 28.08s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **09 · Funis e Lifecycle — O Sistema Completo** · slides 9 · áudio 18.83s · legado 20.04s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **10 · A/B Testing com Judge — Ciência da Experimentação** · slides 9 · áudio 19.76s · legado 20.04s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **11 · Análise de Coortes e Churn — A Arte de Reter** · slides 9 · áudio 26.86s · legado 26.92s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **12 · Blueprints Elite — O Jogo do Top 10%** · slides 10 · áudio 23.4s · legado 23.44s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **13 · Multi-Tenant e White-Label na Prática** · slides 9 · áudio 19.01s · legado 20.04s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240
- **14 · Federação de Agentes Zero-Trust** · slides 9 · áudio 22.97s · legado 23.0s · rebuild: sim · motivos: audio_curto_abaixo_do_padro_video_aula, duracao_video_fora_do_padrao_60_240

## Diretriz de reconstrução
- Reusar **capa oficial já aprovada** como frame de abertura.
- Reusar arquivos de slides como base de 5–10 quadros sincronizados.
- Gerar **nova narração** para cada módulo com duração-alvo entre 60s e 240s.
- Produzir master final em naming canônico e mover provas/POCs para categoria legada.

# Sync da fila de upload YouTube

## Resumo
- Publicados: **10**
- Prontos para nova tentativa de upload: **5** (09, 10, 11, 12, 13)
- Teasers com nome canônico exato: **1**
- Teasers resolvidos por alias mapeado: **10**
- Teasers ausentes: **4**

## Fila pronta
- **09** · `video-09-funis-e-lifecycle-o-sistema-completo` · vídeo `video-09-funis-e-lifecycle.mp4` · thumb `09-funis-e-lifecycle-o-sistema-completo.png` · teaser `video-09-funis-e-lifecycle.mp4`
- **10** · `video-10-a-b-testing-com-judge-ciencia-da-experimentacao` · vídeo `video-10-a-b-testing-com-judge.mp4` · thumb `10-a-b-testing-com-judge-ciencia-da-experimentacao.png` · teaser `video-10-a-b-testing-com-judge.mp4`
- **11** · `video-11-analise-de-coortes-e-churn-a-arte-de-reter` · vídeo `video-11-coortes-e-churn.mp4` · thumb `11-analise-de-coortes-e-churn-a-arte-de-reter.png` · teaser `video-11-coortes-e-churn.mp4`
- **12** · `video-12-blueprints-elite-o-jogo-do-top-10` · vídeo `video-12-blueprints-elite.mp4` · thumb `12-blueprints-elite-o-jogo-do-top-10.png` · teaser `video-12-blueprints-elite.mp4`
- **13** · `video-13-multi-tenant-e-white-label-na-pratica` · vídeo `video-13-multi-tenant-e-white-label.mp4` · thumb `13-multi-tenant-e-white-label-na-pratica.png` · teaser `video-13-multi-tenant-e-white-label.mp4`

## Observações operacionais
- `youtube/upload_batch_ready.json` foi regenerado com a fila atual, evitando itens já publicados.
- `youtube/publish_plan.csv` foi sincronizado a partir do plano JSON canônico.
- As descrições da fila pronta foram saneadas para nova tentativa de upload, reduzindo risco de `invalidDescription`.

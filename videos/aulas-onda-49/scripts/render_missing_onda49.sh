#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════
# Render ONDA-49 — completa os 10 MP4s 720p faltantes (uma aula por call)
#
# Estratégia (uma única chamada ffmpeg por aula):
#   - carimbo 5 PNGs simultaneamente com -loop 1 -t 32
#   - complex_filter faz scale→pad 1280x720 e concat
#   - anullsrc gera áudio silente (TTS vem depois via ffmpeg -i base -i nar -c copy)
#
# Receita canônica validada contra a aula-17 já no repo (3.7M, 159s).
# ════════════════════════════════════════════════════════════════════
set -euo pipefail

cd "$(dirname "$0")/../../.."   # /home/user/academ_ia

SLIDES_BASE="videos/aulas-onda-49/slides"
RENDERS_BASE="videos/aulas-onda-49/renders"
DUR=32
FPS=30
mkdir -p "$RENDERS_BASE"

AULAS=(
    "aula-15-metricas-roi-ecossistema"
    "aula-16-trilha-fundamental-ia"
    "aula-18-seguranca-ofensiva-pentest"
    "aula-19-monetizacao-avancada-escala"
    "aula-20-trilha-elite-engenharia"
    "aula-21-trilha-master-arquitetura"
    "aula-22-trilha-master-mentoria"
    "aula-23-curso-rag-pratico"
    "aula-24-curso-agents-langgraph"
    "aula-25-curso-prompt-engineering"
)

ok=0
fail=0
for aula in "${AULAS[@]}"; do
    sdir="$SLIDES_BASE/$aula"
    out="$RENDERS_BASE/${aula}-720p.mp4"
    if [ -f "$out" ]; then
        echo "SKIP $aula (já existe)"
        continue
    fi

    # Detecta ordem dos PNGs alfabeticamente (cena-01..cena-05)
    PNG_ARR=()
    while IFS= read -r p; do PNG_ARR+=("$p"); done < <(ls "$sdir"/cena-*.png)
    count=${#PNG_ARR[@]}
    if [ "$count" -lt 5 ]; then
        echo "WARN $aula só tem $count cenas — pulando"
        ((fail+=1))
        continue
    fi

    echo "==> $aula : $count cenas → $out"

    # Constroi complex_filter:
    #   [i:v]scale=…→pad 1280:720[v{i}]
    #   [v0][v1][v2][v3][v4]concat=n=5:v=1:a=0[v]
    FILTER=""
    for i in 0 1 2 3 4; do
        FILTER+="[$i:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black[v$i];"
    done
    FILTER+="[v0][v1][v2][v3][v4]concat=n=5:v=1:a=0[outv]"
    AUD_TOTAL=$((DUR * 5))

    start=$(date +%s)
    ffmpeg -y -hide_banner -loglevel error \
        -loop 1 -t "$DUR" -i "${PNG_ARR[0]}" \
        -loop 1 -t "$DUR" -i "${PNG_ARR[1]}" \
        -loop 1 -t "$DUR" -i "${PNG_ARR[2]}" \
        -loop 1 -t "$DUR" -i "${PNG_ARR[3]}" \
        -loop 1 -t "$DUR" -i "${PNG_ARR[4]}" \
        -f lavfi -t "$AUD_TOTAL" -i "anullsrc=channel_layout=stereo:sample_rate=44100" \
        -filter_complex "$FILTER" \
        -map "[outv]" -map "5:a" \
        -c:v libx264 -preset ultrafast -crf 23 -pix_fmt yuv420p -r "$FPS" \
        -c:a aac -b:a 128k -shortest \
        "$out"
    rc=$?
    elapsed=$(( $(date +%s) - start ))

    if [ "$rc" -eq 0 ] && [ -f "$out" ]; then
        size=$(du -h "$out" | cut -f1)
        echo "    ✓ ok em ${elapsed}s · $size"
        ((ok+=1))
    else
        echo "    ✗ FRACASSO rc=$rc"
        ((fail+=1))
    fi
done

echo ""
echo "═══════════════════════════════════════════════════════"
echo "RESULTADO: ok=$ok · fail=$fail · total arquivos agora: $(ls $RENDERS_BASE/*.mp4 | wc -l)"
echo "═══════════════════════════════════════════════════════"

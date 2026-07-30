#!/bin/bash
# =============================================================================
# RENDERIZAÇÃO — Aula 22: Aula 22
# Trilha: Master | Persona: Dupla | Cenas: 5
# =============================================================================

set -euo pipefail

AULA="22"
SLUG="aula-22"
TRILHA="Master"
PERSONA="Dupla"
TOTAL_CENAS=5

BASE="videos/aulas-onda-49"
WORK="$BASE/render-work/$AULA-$SLUG"
FRAMES="$WORK/frames"
AUDIO="$WORK/audio"
CENAS_OUT="$WORK/cenas"
FINAL="$BASE/renders"
THUMBS="$BASE/thumbnails"

mkdir -p "$FRAMES" "$AUDIO" "$CENAS_OUT" "$FINAL" "$THUMBS"

RES="1920:1080"
FPS=30
CRF=23
PRESET="slow"
AUDIO_BR="192k"
PIX_FMT="yuv420p"

echo "========================================"
echo "🎬 Renderizando Aula $AULA"
echo "========================================"

# Verificar pré-requisitos
MISSING=0
for i in $(seq 1 $TOTAL_CENAS); do
    if [ ! -f "$FRAMES/cena$i.png" ]; then echo "  ❌ Frame: cena$i.png"; MISSING=$((MISSING + 1)); fi
    if [ ! -f "$AUDIO/cena$i.wav" ]; then echo "  ❌ Áudio: cena$i.wav"; MISSING=$((MISSING + 1)); fi
done
if [ $MISSING -gt 0 ]; then echo "❌ Faltam $MISSING arquivos"; exit 1; fi
echo "✅ Pré-requisitos OK"

# Renderizar cenas
DURACOES=(10 15 15 15 10)
for i in $(seq 1 $TOTAL_CENAS); do
    IDX=$((i - 1))
    DURACAO="${DURACOES[$IDX]}"
    FRAME="$FRAMES/cena$i.png"
    AUDIO_FILE="$AUDIO/cena$i.wav"
    OUTPUT="$CENAS_OUT/cena$(printf "%02d" $i).mp4"
    echo "→ Cena $i ($DURACAO s)..."
    FADE_OUT=$(echo "$DURACAO - 0.5" | bc)
    ffmpeg -y -hide_banner -loglevel error -loop 1 -i "$FRAME" -i "$AUDIO_FILE" -t "$DURACAO" -vf "scale=$RES:force_original_aspect_ratio=decrease,pad=$RES:(ow-iw)/2:(oh-ih)/2:#0A1628,fade=t=in:st=0:d=0.5,fade=t=out:st=$FADE_OUT:d=0.5" -c:v libx264 -preset $PRESET -crf $CRF -pix_fmt $PIX_FMT -r $FPS -c:a aac -b:a $AUDIO_BR -shortest -movflags +faststart "$OUTPUT"
    echo "  ✓ Cena $i"
done

# Concatenar
LIST_FILE="$WORK/concat_list.txt"
> "$LIST_FILE"
for i in $(seq 1 $TOTAL_CENAS); do echo "file 'cenas/cena$(printf "%02d" $i).mp4'" >> "$LIST_FILE"; done
FINAL_1080P="$FINAL/aula-$AULA-$SLUG-1080p.mp4"
ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i "$LIST_FILE" -c:v libx264 -preset $PRESET -crf $CRF -pix_fmt $PIX_FMT -r $FPS -c:a aac -b:a $AUDIO_BR -movflags +faststart "$FINAL_1080P"
echo "✅ 1080p: $FINAL_1080P"

# 720p
FINAL_720P="$FINAL/aula-$AULA-$SLUG-720p.mp4"
ffmpeg -y -hide_banner -loglevel error -i "$FINAL_1080P" -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:#0A1628" -c:v libx264 -preset $PRESET -crf $CRF -pix_fmt $PIX_FMT -r $FPS -c:a aac -b:a $AUDIO_BR -movflags +faststart "$FINAL_720P"
echo "✅ 720p: $FINAL_720P"

# Thumbnail
THUMB_FILE="$THUMBS/thumb-$AULA-$SLUG.png"
ffmpeg -y -hide_banner -loglevel error -i "$FINAL_1080P" -ss 00:00:05 -vframes 1 -vf "scale=2560:1440:force_original_aspect_ratio=decrease,pad=2560:1440:(ow-iw)/2:(oh-ih)/2:#0A1628" "$THUMB_FILE"
echo "✅ Thumb: $THUMB_FILE"

echo "========================================"
echo "🎉 AULA $AULA COMPLETA!"
echo "========================================"
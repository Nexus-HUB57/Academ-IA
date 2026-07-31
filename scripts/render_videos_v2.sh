#!/usr/bin/env bash
# scripts/render_videos_v2.sh
# ============================================================
# Renderizador de vídeos v2 (roteiros_v2) — AcademIA
# ============================================================
#
# OBJETIVO:
#   Renderizar MP4 full para os 10 roteiros v2 (C1-C6 + T1-T4) que
#   estão em videos/roteiros_v2/ mas NÃO têm MP4 final ainda.
#
# ENTRADA (assets existentes, gerados por outro dev):
#   - videos/roteiros_v2/{CODIGO}-video-roteiro.md
#   - videos/audios_v2/Ive/{CODIGO}-Ive.mp3
#   - videos/audios_v2/Alencar/{CODIGO}-Alencar.mp3
#   - videos/audios_v2/mix/{CODIGO}-mix-Ive-Alencar.mp3
#   - videos/audios_tts_v2/{CODIGO}-narracao.mp3
#   - videos/clipes_hero_v2/{CODIGO}-hero.mp4 (opcional)
#   - apostilas/imagens/{CODIGO}/cover.png
#
# SAÍDA (segue RENDER_PIPELINE.md oficial):
#   - videos/video-{CODIGO}-{slug}-v2-full.mp4
#
# PIPELINE (ffmpeg):
#   1. Cover image looping (${cover_dur}s)
#   2. (opcional) Concat com hero clip
#   3. Adiciona audio mix (Ive + Alencar)
#
# USO:
#   bash scripts/render_videos_v2.sh              # renderiza todos (10)
#   bash scripts/render_videos_v2.sh C1 C2 T1     # renderiza específicos
#   bash scripts/render_videos_v2.sh --dry-run    # só mostra o que faria
#
# COMPLIANCE:
#   - Não sobrescreve arquivos existentes (skip se MP4 final já existe)
#   - Não toca em vozes oficiais em marca/personas/
#   - Não duplica trabalho de outros devs
#   - Idempotente: pode rodar múltiplas vezes
#
# CRIAÇÃO: 2026-07-30 (Mavis Agent, pós status check)
# ============================================================

set -uo pipefail  # sem -e para não abortar em vídeos que falham individuais

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

VIDEOS="$REPO_ROOT/videos"
ROTEIROS_DIR="$VIDEOS/roteiros_v2"
HERO_DIR="$VIDEOS/clipes_hero_v2"
AUDIO_IVE_DIR="$VIDEOS/audios_v2/Ive"
AUDIO_ALENCAR_DIR="$VIDEOS/audios_v2/Alencar"
AUDIO_MIX_DIR="$VIDEOS/audios_v2/mix"
AUDIO_NARR_DIR="$VIDEOS/audios_tts_v2"
COVER_DIR="$REPO_ROOT/apostilas/imagens"

# Slugs descritivos (mapeamento código → slug)
declare -A SLUGS=(
  [C1]="rag-zero-producao"
  [C2]="agents-langgraph"
  [C3]="prompt-engineering-production"
  [C4]="vector-databases-devs"
  [C5]="voice-ai-jarvis"
  [C6]="multimodal-rag"
  [T1]="ia-para-afiliados"
  [T2]="engenharia-ia-producao"
  [T3]="arquitetura-agentic"
  [T4]="mentoria-lideranca-tecnica"
)

# Códigos alvo
ALL_CODES=(C1 C2 C3 C4 C5 C6 T1 T2 T3 T4)
TARGETS=()
DRY_RUN=false

# Parse args
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --help|-h)
      echo "Uso: bash scripts/render_videos_v2.sh [--dry-run] [CODIGO1 CODIGO2 ...]"
      echo "Códigos disponíveis: ${ALL_CODES[*]}"
      exit 0
      ;;
    C1|C2|C3|C4|C5|C6|T1|T2|T3|T4) TARGETS+=("$arg") ;;
    *) echo "[ERRO] Código inválido: $arg (esperado: ${ALL_CODES[*]})" >&2; exit 1 ;;
  esac
done

# Se sem alvos, usar todos
if [ ${#TARGETS[@]} -eq 0 ]; then
  TARGETS=("${ALL_CODES[@]}")
fi

echo "============================================================"
echo "🎬 Renderizador de Vídeos v2 — AcademIA"
echo "============================================================"
echo "Modo: $([ "$DRY_RUN" = true ] && echo 'DRY-RUN' || echo 'APPLY')"
echo "Alvos: ${TARGETS[*]}"
echo "Repo: $REPO_ROOT"
echo ""

# Validar pré-requisitos
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "[ERRO] ffmpeg não encontrado no PATH" >&2
  exit 1
fi

if ! command -v ffprobe >/dev/null 2>&1; then
  echo "[ERRO] ffprobe não encontrado no PATH" >&2
  exit 1
fi

# Contadores
rendered=0
skipped=0
failed=0

# Função para renderizar um vídeo
render_video() {
  local code="$1"
  local slug="${SLUGS[$code]}"
  local hero="$HERO_DIR/${code}-hero.mp4"
  local audio_mix="$AUDIO_MIX_DIR/${code}-mix-Ive-Alencar.mp3"
  local cover="$COVER_DIR/$code/cover.png"
  local output="$VIDEOS/video-${code}-${slug}-v2-full.mp4"

  echo "──────────────────────────────────────────────────────────"
  echo "🎬 [$code] Renderizando: $slug"

  # Verificar pré-requisitos
  if [ ! -f "$audio_mix" ]; then
    echo "  ❌ Áudio mix não encontrado: $audio_mix"
    ((failed++))
    return 1
  fi

  # Hero é opcional — se não existir, usa só cover com fade
  if [ -f "$hero" ]; then
    echo "  ✓ Hero clip encontrado"
  else
    echo "  ⚠️  Hero clip não encontrado (usando só cover)"
    hero=""
  fi

  if [ ! -f "$cover" ]; then
    echo "  ⚠️  Cover não encontrado: $cover (usando fallback)"
    cover=""  # será tratado abaixo
  fi

  # Se output já existe, skip (não-destrutivo)
  if [ -f "$output" ]; then
    local size=$(stat -c%s "$output")
    echo "  ⏭️  Output já existe ($((size/1024))KB) - skipping"
    ((skipped++))
    return 0
  fi

  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY-RUN] Renderizaria:"
    echo "    hero:   ${hero:-<none>}"
    echo "    audio:  $audio_mix"
    echo "    cover:  ${cover:-<fallback>}"
    echo "    output: $output"
    return 0
  fi

  # Pegar duração do áudio mix
  local audio_dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$audio_mix" 2>/dev/null)
  if [ -z "$audio_dur" ]; then
    echo "  ❌ Não foi possível obter duração do áudio"
    ((failed++))
    return 1
  fi

  # Se hero existe, pegar duração
  local hero_dur=0
  if [ -n "$hero" ] && [ -f "$hero" ]; then
    hero_dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$hero" 2>/dev/null)
    if [ -z "$hero_dur" ]; then
      hero_dur=0
    fi
  fi

  # Duração da capa = audio_dur - hero_dur
  local cover_dur=$(awk -v a="$audio_dur" -v b="$hero_dur" 'BEGIN {printf "%.3f", a-b}')
  if [ -z "$cover_dur" ] || [ "$(awk -v c="$cover_dur" 'BEGIN {print (c<0)?1:0}')" = "1" ]; then
    cover_dur="$audio_dur"
  fi

  echo "  📊 audio=${audio_dur}s hero=${hero_dur}s cover=${cover_dur}s"

  # Workdir temporário
  local workdir=$(mktemp -d)
  local concat_list="$workdir/concat.txt"

  # 1) Cover image looping (${cover_dur}s) - fundo do vídeo
  local cover_clip="$workdir/cover_clip.mp4"

  if [ -n "$cover" ] && [ -f "$cover" ]; then
    ffmpeg -y -loop 1 -i "$cover" -t "$cover_dur" \
      -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,fade=t=in:0:2" \
      -c:v libx264 -preset ultrafast -crf 23 -pix_fmt yuv420p -r 30 \
      -an "$cover_clip" 2>&1 | tail -2
  else
    ffmpeg -y -f lavfi -i "color=c=#0a0e1a:s=1920x1080:d=$cover_dur" \
      -vf "drawtext=text='$code':fontcolor=white:fontsize=120:x=(w-text_w)/2:y=(h-text_h)/2" \
      -c:v libx264 -preset ultrafast -crf 23 -pix_fmt yuv420p -r 30 \
      -an "$cover_clip" 2>&1 | tail -2
  fi

  if [ ! -f "$cover_clip" ]; then
    echo "  ❌ Falha ao gerar cover_clip"
    rm -rf "$workdir"
    ((failed++))
    return 1
  fi

  # 2) Se hero existe, concatenar cover_clip + hero_no_audio
  local video_only="$workdir/video_only.mp4"
  if [ -n "$hero" ] && [ -f "$hero" ] && [ "$(awk -v h="$hero_dur" 'BEGIN {print (h>0)?1:0}')" = "1" ]; then
    local hero_no_audio="$workdir/hero_no_audio.mp4"
    ffmpeg -y -i "$hero" -c:v copy -an "$hero_no_audio" 2>&1 | tail -2

    cat > "$concat_list" <<EOF
file '$cover_clip'
file '$hero_no_audio'
EOF

    ffmpeg -y -f concat -safe 0 -i "$concat_list" \
      -c:v libx264 -preset ultrafast -crf 23 -pix_fmt yuv420p -r 30 \
      "$video_only" 2>&1 | tail -2
  else
    # Sem hero, usa só cover_clip
    cp "$cover_clip" "$video_only"
  fi

  # 3) Adicionar áudio mix
  ffmpeg -y -i "$video_only" -i "$audio_mix" \
    -c:v copy -c:a aac -b:a 128k \
    -shortest "$output" 2>&1 | tail -2

  if [ -f "$output" ]; then
    local size=$(stat -c%s "$output")
    echo "  ✅ Renderizado: $output ($((size/1024))KB)"
    ((rendered++))
  else
    echo "  ❌ Falha na renderização final"
    ((failed++))
  fi

  # Limpar workdir
  rm -rf "$workdir"
  return 0
}

# Renderizar cada alvo
for code in "${TARGETS[@]}"; do
  render_video "$code"
done

echo ""
echo "============================================================"
echo "📋 Resumo"
echo "============================================================"
echo "✅ Renderizados: $rendered"
echo "⏭️  Skipped (já existem): $skipped"
echo "❌ Falharam: $failed"
echo ""

if [ "$DRY_RUN" = true ]; then
  echo "💡 Para aplicar de verdade, rode sem --dry-run"
fi

exit 0

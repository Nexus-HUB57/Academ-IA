#!/bin/bash
# =============================================================================
# SCRIPT TTS — Aula 21: Aula
# Persona: Dupla | Voice: pt-BR-Neural2-C | Speed: 1.0
# =============================================================================

set -e

AULA="21"
PERSONA="Dupla"
VOICE="pt-BR-Neural2-C"
SPEED="1.0"
PITCH="0st"
OUTPUT_DIR="audio"

mkdir -p "$OUTPUT_DIR"

# Configuração da voz
# Style: energetic, clear, engaging
# Ajustes: speed=1.0, pitch=0st


# --- Cena 1: 🎬 CENA 1 — Abertura Cinematográfica (Duração: 10s) ---
echo "🎤 Gerando TTS cena 1..."
gcloud text-to-speech synthesize \
    --text="[Narração da cena 1: 🎬 CENA 1 — Abertura Cinematográfica (Duração: 10s)]" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena1.wav"


# --- Cena 2: 🎬 CENA 2 — Créditos & Ficha Técnica (Duração: 15s) ---
echo "🎤 Gerando TTS cena 2..."
gcloud text-to-speech synthesize \
    --text="[Narração da cena 2: 🎬 CENA 2 — Créditos & Ficha Técnica (Duração: 15s)]" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena2.wav"


# --- Cena 3: 🎬 CENA 3 — Sobre esta apostila (Duração: 15s) ---
echo "🎤 Gerando TTS cena 3..."
gcloud text-to-speech synthesize \
    --text="[Narração da cena 3: 🎬 CENA 3 — Sobre esta apostila (Duração: 15s)]" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena3.wav"


# --- Cena 4: 🎬 CENA 4 — Como usar (Duração: 15s) ---
echo "🎤 Gerando TTS cena 4..."
gcloud text-to-speech synthesize \
    --text="[Narração da cena 4: 🎬 CENA 4 — Como usar (Duração: 15s)]" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena4.wav"


# --- Cena 5: 🎬 CENA 5 — Fechamento & Chamada à Ação (Duração: 8s) ---
echo "🎤 Gerando TTS cena 5..."
gcloud text-to-speech synthesize \
    --text="[Narração da cena 5: 🎬 CENA 5 — Fechamento & Chamada à Ação (Duração: 8s)]" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena5.wav"


echo "✅ TTS completo para Aula $AULA"
ls -la "$OUTPUT_DIR/"

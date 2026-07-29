#!/bin/bash
# =============================================================================
# SCRIPT TTS — Aula 33: Aula
# Persona: Alencar | Voice: pt-BR-Neural2-B | Speed: 0.95
# =============================================================================

set -e

AULA="33"
PERSONA="Alencar"
VOICE="pt-BR-Neural2-B"
SPEED="0.95"
PITCH="-2st"
OUTPUT_DIR="audio"

mkdir -p "$OUTPUT_DIR"

# Configuração da voz
# Style: authoritative, calm, educational
# Ajustes: speed=0.95, pitch=-2st


# --- Cena 1: 🎬 CENA 1 — Abertura Cinematográfica (Duração: 10s) ---
echo "🎤 Gerando TTS cena 1..."
gcloud text-to-speech synthesize \
    --text="[Narração da cena 1: 🎬 CENA 1 — Abertura Cinematográfica (Duração: 10s)]" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena1.wav"


# --- Cena 2: 🎬 CENA 2 — 2. Dados de sessão (Semi-structured) (Duração: 15s) ---
echo "🎤 Gerando TTS cena 2..."
gcloud text-to-speech synthesize \
    --text="[Narração da cena 2: 🎬 CENA 2 — 2. Dados de sessão (Semi-structured) (Duração: 15s)]" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena2.wav"


# --- Cena 3: 🎬 CENA 3 — 3. Dados assíncronos (Queues) (Duração: 15s) ---
echo "🎤 Gerando TTS cena 3..."
gcloud text-to-speech synthesize \
    --text="[Narração da cena 3: 🎬 CENA 3 — 3. Dados assíncronos (Queues) (Duração: 15s)]" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena3.wav"


# --- Cena 4: 🎬 CENA 4 — 4. Dados semânticos (Unstructured + vectors) (Duração: 15s) ---
echo "🎤 Gerando TTS cena 4..."
gcloud text-to-speech synthesize \
    --text="[Narração da cena 4: 🎬 CENA 4 — 4. Dados semânticos (Unstructured + vectors) (Duração: 15s)]" \
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

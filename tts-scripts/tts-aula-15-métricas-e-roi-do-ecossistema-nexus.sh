#!/bin/bash
# =============================================================================
# SCRIPT TTS — Aula 15: Métricas & ROI do Ecossistema Nexus
# Persona: Dupla | Voice: pt-BR-Neural2-C | Speed: 1.0
# =============================================================================

set -e

AULA="15"
PERSONA="Dupla"
VOICE="pt-BR-Neural2-C"
SPEED="1.0"
PITCH="0st"
OUTPUT_DIR="audio"

mkdir -p "$OUTPUT_DIR"

# Configuração da voz
# Style: energetic, clear, engaging
# Ajustes: speed=1.0, pitch=0st


# --- Cena 1: 🎬 Abertura Cinematográfica (10s) ---
echo "🎤 Gerando TTS cena 1..."
gcloud text-to-speech synthesize \
    --text="\"Você não vai aprender ROI. Você vai dominar a única métrica que importa em ecossistemas distribuídos.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena1.wav"


# --- Cena 2: 📚 Cena 2 — Por que ROI de IA é diferente (15s) ---
echo "🎤 Gerando TTS cena 2..."
gcloud text-to-speech synthesize \
    --text="\"ROI tradicional compara receita e custo atribuíveis. Mas IA distribui três problemas novos: benefícios indiretos, custos compartilhados e valor de opção. Por isso o ROI Nexus é mais difícil — e quando bem calculado, é mais persuasivo que o tradicional.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena2.wav"


# --- Cena 3: 📊 Cena 3 — As 4 dimensões do ROI Nexus (15s) ---
echo "🎤 Gerando TTS cena 3..."
gcloud text-to-speech synthesize \
    --text="\"O ROI Nexus tem quatro camadas que se somam. Direto, no curto prazo, é o afiliado medindo. Produtividade, no médio prazo, mede tempo economizado convertido em valor. Estratégico, no longo prazo, é o board olhando opções de futuro. E sistêmico, no muito longo prazo, é o ecossistema inteiro ganhando externalidades positivas.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena3.wav"


# --- Cena 4: 🧮 Cena 4 — As 12 métricas oficiais (15s) ---
echo "🎤 Gerando TTS cena 4..."
gcloud text-to-speech synthesize \
    --text="\"A Nexus reporta publicamente doze métricas oficiais em nexus.io/metrics. As mais críticas: GMV de cinco milhões por mês, treze mil tenants ativos, oitocentas skills publicadas, latência p99 abaixo de duzentos milissegundos, e LTV/CAC acima de quinze. Se você não vê sua métrica aqui, ela provavelmente não é importante para o ecossistema.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena4.wav"


# --- Cena 5: 📈 Cena 5 — Exemplo ROI Direto na prática (8s) ---
echo "🎤 Gerando TTS cena 5..."
gcloud text-to-speech synthesize \
    --text="\"Exemplo concreto: receita atribuível de doze mil reais em junho, custo total de mil reais, ROI Direto de mil e cem por cento. Some a isso produtividade e estratégico, e você tem o caso de negócio que convence qualquer board.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena5.wav"


# --- Cena 6: 🎯 CTA de Fechamento (7s) ---
echo "🎤 Gerando TTS cena 6..."
gcloud text-to-speech synthesize \
    --text="\"Acesse oneverso.com.br/academia, baixe a apostila 15 completa, e meça seu ROI hoje.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena6.wav"


echo "✅ TTS completo para Aula $AULA"
ls -la "$OUTPUT_DIR/"

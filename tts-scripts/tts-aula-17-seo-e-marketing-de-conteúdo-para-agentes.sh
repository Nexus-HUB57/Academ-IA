#!/bin/bash
# =============================================================================
# SCRIPT TTS — Aula 17: SEO & Marketing de Conteúdo para Agentes IA
# Persona: Dupla | Voice: pt-BR-Neural2-C | Speed: 1.0
# =============================================================================

set -e

AULA="17"
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
    --text="\"Você não vai aprender SEO. Você vai dominar a arte de ser citado por uma IA generativa — quando seu concorrente é a própria IA.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena1.wav"


# --- Cena 2: 🔍 Cena 2 — A nova fronteira do Search (15s) ---
echo "🎤 Gerando TTS cena 2..."
gcloud text-to-speech synthesize \
    --text="\"Três números que mudam tudo. O CTR da posição um do Google caiu trinta e dois por cento desde dois mil e vinte e dois. O CTR de fonte citada em respostas de IA cresceu quatrocentos e cinquenta por cento desde dois mil e vinte e três. E o tempo médio de leitura em answer engine caiu para oito segundos. Estamos na era do GEO — Generative Engine Optimization — não mais SEO tradicional.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena2.wav"


# --- Cena 3: 🤖 Cena 3 — Os 4 Algoritmos que Mudaram (15s) ---
echo "🎤 Gerando TTS cena 3..."
gcloud text-to-speech synthesize \
    --text="\"Quatro algoritmos sustentam essa mudança. RAG — Retrieval-Augmented Generation — busca documentos relevantes e cita fontes. RLHF — Reinforcement Learning from Human Feedback — prefere conteúdo autoritativo e bem estruturado. Citation Authority Scoring ranqueia domínios por grafo de links e menções. E Semantic Chunk Matching divide seu conteúdo em blocos de quinhentos tokens e ranqueia por relevância. Implicação prática: estrutura modular, headings claros, respostas diretas vencem textos longos e divagantes.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena3.wav"


# --- Cena 4: 📐 Cena 4 — A Pirâmide de Conteúdo AEO (15s) ---
echo "🎤 Gerando TTS cena 4..."
gcloud text-to-speech synthesize \
    --text="\"Seu conteúdo precisa estar nas camadas cinco, seis ou sete da pirâmide AEO. Camada sete é definition content — definições canônicas que viram referência. Camada seis é original research — dados primários, surveys, benchmarks. Camada cinco é expert commentary — opinião de especialista reconhecido. Conteúdos das camadas um a quatro são ignorados pelas IAs generativas.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena4.wav"


# --- Cena 5: ✅ Cena 5 — Os 7 Padrões que Fazem uma IA Citar Você (8s) ---
echo "🎤 Gerando TTS cena 5..."
gcloud text-to-speech synthesize \
    --text="\"Sete padrões para ser citado. Specificity vence generalidade — números concretos vencem afirmações vagas. Estatísticas com fonte verificada. Citações originais de especialistas reconhecidos. Tabelas comparativas. Listas passo a passo. Seções de perguntas frequentes. E credenciais do autor verificáveis. Aplique os sete e você sai do genérico para o citável.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena5.wav"


# --- Cena 6: 🎯 CTA de Fechamento (7s) ---
echo "🎤 Gerando TTS cena 6..."
gcloud text-to-speech synthesize \
    --text="\"Baixe a apostila 17 em oneverso.com.br/academia e domine o GEO.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena6.wav"


echo "✅ TTS completo para Aula $AULA"
ls -la "$OUTPUT_DIR/"

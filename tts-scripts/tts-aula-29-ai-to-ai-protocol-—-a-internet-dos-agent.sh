#!/bin/bash
# =============================================================================
# SCRIPT TTS — Aula 29: AI-to-AI Protocol — A Internet dos Agentes
# Persona: Dupla | Voice: pt-BR-Neural2-C | Speed: 1.0
# =============================================================================

set -e

AULA="29"
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
    --text="\"Você não vai aprender mais um protocolo. Você vai entender como funciona a Internet dos Agentes — onde seu agente fala com qualquer agente do mundo.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena1.wav"


# --- Cena 2: 🌐 Cena 2 — O que é A2A (15s) ---
echo "🎤 Gerando TTS cena 2..."
gcloud text-to-speech synthesize \
    --text="\"A2A — Agent-to-Agent Protocol — é um padrão aberto criado pelo Google em abril de dois mil e vinte e cinco. Antes dele, se você quisesse que um agente do Google Cloud conversasse com um agente da OpenAI, precisava criar um middleware custom. Com A2A, eles conversam diretamente via JSON-RPC. A analogia é direta: A2A é para agentes de IA o que HTTP foi para websites nos anos noventa. E já é adotado por mais de cinquenta empresas — Google, OpenAI, Microsoft Azure, AWS Bedrock, Salesforce, ServiceNow, Atlassian, SAP, Cisco.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena2.wav"


# --- Cena 3: 💼 Cena 3 — Os 4 cenários que importam para afiliados (15s) ---
echo "🎤 Gerando TTS cena 3..."
gcloud text-to-speech synthesize \
    --text="\"Quatro cenários onde A2A muda seu jogo de afiliados. Primeiro: pesquisa de mercado automatizada — seu agente chama o agente da Hotmart para consultar preço, comissão e estoque em um a dois segundos. Segundo: atendimento conjunto — cliente fala com seu agente, que passa para o suporte da plataforma e volta consolidado. Terceiro: análise cruzada — você combina dados do Google Analytics, Meta Ads e Stripe num único dashboard via agentes. Quarto: orquestração multi-agente — você tem um agente para WhatsApp, um para email, um para Telegram, todos cooperando via A2A sem você programar a integração.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena3.wav"


# --- Cena 4: 📄 Cena 4 — Agent Card (.well-known/agent.json) (15s) ---
echo "🎤 Gerando TTS cena 4..."
gcloud text-to-speech synthesize \
    --text="\"Para outros agentes descobrirem o que seu agente faz, você publica um Agent Card em uma URL bem-conhecida — exatamente como o robots.txt fez para sites em dois mil e cinco. O arquivo fica em seudominio.com/.well-known/agent.json. Lá você declara nome, descrição, versão, capacidades como streaming e push notifications, e a lista de skills disponíveis com seus input schemas. Outros agentes consultam esse arquivo e sabem exatamente o que você oferece. É o mesmo princípio de design do HTTP — descoberta nativa, sem cadastro central.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena4.wav"


# --- Cena 5: 🔧 Cena 5 — Os 4 métodos principais (8s) ---
echo "🎤 Gerando TTS cena 5..."
gcloud text-to-speech synthesize \
    --text="\"A2A define quatro métodos essenciais via JSON-RPC 2.0. tasks/send envia uma tarefa. tasks/get consulta o status. tasks/cancel cancela uma tarefa em andamento. E tasks/subscribe ouve por push notifications. Tudo baseado em JSON-RPC — protocolo leve, request com id, method e params, response com result ou error. Em produção, o agente A envia uma tasks/send ao agente B, recebe task result com artefatos, e segue.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena5.wav"


# --- Cena 6: 🎯 CTA de Fechamento (7s) ---
echo "🎤 Gerando TTS cena 6..."
gcloud text-to-speech synthesize \
    --text="\"Baixe a apostila 29 em oneverso.com.br/academia e descubra como plugar seu agente na Internet dos Agentes.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena6.wav"


echo "✅ TTS completo para Aula $AULA"
ls -la "$OUTPUT_DIR/"

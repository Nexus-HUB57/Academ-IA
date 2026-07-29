#!/bin/bash
# =============================================================================
# SCRIPT TTS — Aula 30: Federação Zero-Trust — Segurança Avançada para Agentes A2A
# Persona: Alencar | Voice: pt-BR-Neural2-B | Speed: 0.95
# =============================================================================

set -e

AULA="30"
PERSONA="Alencar"
VOICE="pt-BR-Neural2-B"
SPEED="0.95"
PITCH="-2st"
OUTPUT_DIR="audio"

mkdir -p "$OUTPUT_DIR"

# Configuração da voz
# Style: authoritative, calm, educational
# Ajustes: speed=0.95, pitch=-2st


# --- Cena 1: 🎬 Abertura Cinematográfica (10s) ---
echo "🎤 Gerando TTS cena 1..."
gcloud text-to-speech synthesize \
    --text="\"Você não vai aprender mais um framework de segurança. Você vai descobrir como agentes de plataformas diferentes se comunicam sem confiar em ninguém.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena1.wav"


# --- Cena 2: 🔒 Cena 2 — Por que Zero-Trust importa para A2A (15s) ---
echo "🎤 Gerando TTS cena 2..."
gcloud text-to-speech synthesize \
    --text="\"Zero-Trust — nunca confiar, sempre verificar — é o padrão corporativo desde dois mil e vinte. Mas a maioria das implementações é para humanos e serviços internos. Em comunicação A2A, três problemas aparecem: você não controla o outro agente, pode ser de qualquer vendor. Não controla a rede, passa por internet pública. E não controla o usuário final. Quatro riscos específicos: agente malicioso fingindo ser legítimo, man-in-the-middle interceptando comunicação, replay attack repetindo request válido, e skill abuse chamando skill com parâmetros maliciosos. A solução é Zero-Trust mais criptografia forte — mTLS, JWS — mais autenticação por skill.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena2.wav"


# --- Cena 3: 🛡️ Cena 3 — Os 6 pilares do Zero-Trust aplicado a A2A (15s) ---
echo "🎤 Gerando TTS cena 3..."
gcloud text-to-speech synthesize \
    --text="\"Seis pilares sustentam Zero-Trust aplicado a A2A. Identidade verificável via mTLS e DIDs — Decentralized Identifiers. Autenticação contínua, não basta logar uma vez, token rotation a cada uma hora. Autorização por recurso, cada skill tem seu scope no JWT. Auditoria distribuída, todo request logado em OpenTelemetry. Criptografia everywhere, TLS 1.3 mínimo, mTLS em federation. E menor privilégio, o agente só vê o que foi declarado no Agent Card. A regra é clara: tratar cada request como se viesse de uma rede pública hostile.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena3.wav"


# --- Cena 4: 🔐 Cena 4 — Identidade verificável (mTLS + DIDs) (15s) ---
echo "🎤 Gerando TTS cena 4..."
gcloud text-to-speech synthesize \
    --text="\"Identidade verificável na prática. mTLS — Mutual TLS — exige que ambos os lados da conexão apresentem certificado, não só o servidor como em HTTPS. Em código, isso vira ssl.create_default_context com Purpose CLIENT_AUTH e load_cert_chain do certificado do agente. E DIDs — Decentralized Identifiers — padrão W3C para identidade auto-soberana. Cada agente ganha um DID único, did:nexus:agent-abc123, com verification method JsonWebKey2020 e service endpoint do tipo A2AService. Benefício: identidade verificável criptograficamente, sem precisar de Certificate Authority central.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena4.wav"


# --- Cena 5: ⚖️ Cena 5 — Autorização por skill (scope-based) + auditoria (8s) ---
echo "🎤 Gerando TTS cena 5..."
gcloud text-to-speech synthesize \
    --text="\"Cada skill tem seu próprio scope no JWT. O agente que chama precisa ter aquele scope específico, com rate limit próprio. consultar-produto até cem por hora. enviar-mensagem até cinquenta por hora. Servidor verifica scope e rate limit antes de executar. E todo request fica logado de forma imutável — trace id, caller DID, callee DID, método, skill, hashes de input e output, duração em milissegundos. Retenção: noventa dias hot, sete anos cold. Está tudo pronto para compliance.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena5.wav"


# --- Cena 6: 🎯 CTA de Fechamento (7s) ---
echo "🎤 Gerando TTS cena 6..."
gcloud text-to-speech synthesize \
    --text="\"Acesse oneverso.com.br/academia e baixe a apostila 30 completa.\"" \
    --voice="$VOICE" \
    --speed="$SPEED" \
    --pitch="$PITCH" \
    --output="$OUTPUT_DIR/cena6.wav"


echo "✅ TTS completo para Aula $AULA"
ls -la "$OUTPUT_DIR/"

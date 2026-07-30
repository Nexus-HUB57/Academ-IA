---
title: "Tutorial 25 · IA Multimodal · Imagem, Áudio e Vídeo"
subtitle: "Como trabalhar com GPT-4V, Claude Vision, Whisper, DALL-E e Sora na prática"
author: "Equipo Nexus · Sir. Nexus Alencar + Ravi (CTO/AI)"
version: "1.0.0"
date: 2026-07-29
pattern: "MMN_IA"
---

**Tutorial 25 · IA Multimodal · Imagem, Áudio e Vídeo**

*Tutorial completo de 1h30 para usar IA multimodal em produção. Cobre visão computacional (GPT-4V, Claude Vision), TTS/STT (Whisper, ElevenLabs), geração de imagem (DALL-E 3, Midjourney, Flux) e vídeo (Sora, Runway).*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 O que Você Vai Conquistar

Em 1h30, você vai:

1. Implementar análise de imagem (OCR, classificação, descrição)
2. Implementar transcrição de áudio (Whisper)
3. Implementar Text-to-Speech natural (ElevenLabs)
4. Gerar imagens (DALL-E 3, Flux)
5. Editar imagens (inpainting, outpainting)
6. Gerar vídeo curto (Sora, Runway)
7. Construir agente multimodal completo

**Pré-requisitos:**
- Python intermediário
- API keys: OpenAI, Anthropic
- Conhecimento básico de LLMs (ver Tutorial 24)

---

## 🖼️ Parte 1: Visão Computacional

### 1.1 — GPT-4V (Vision)

**Capacidades:**
- Descrever imagem em detalhes
- OCR (extrair texto)
- Responder perguntas sobre imagem
- Detectar objetos, pessoas, ações
- Comparar múltiplas imagens
- Analisar gráficos, diagramas, UI

**Limitações:**
- Não lê texto pequeno (use OCR dedicado)
- Pode errar em detalhes finos
- Alucina em imagens de baixa qualidade
- Não conta objetos com precisão

### 1.2 — Implementação Básica

```python
import base64
from openai import OpenAI

client = OpenAI()


def encode_image(image_path: str) -> str:
    """Codifica imagem em base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def analyze_image(image_path: str, prompt: str) -> str:
    """Analisa imagem com GPT-4V"""
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high",  # low | high | auto
                        },
                    },
                ],
            }
        ],
        max_tokens=500,
    )

    return response.choices[0].message.content


# Uso
description = analyze_image(
    "foto_loja.jpg",
    "Descreva esta foto em detalhes. Inclua produtos visíveis, ambiente, e clientes."
)
print(description)
```

### 1.3 — Análise por URL (sem download)

```python
def analyze_image_url(image_url: str, prompt: str) -> str:
    """Analisa imagem via URL"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
    )
    return response.choices[0].message.content


# Uso
url = "https://exemplo.com/produto.jpg"
desc = analyze_image_url(url, "Liste os produtos nesta imagem com preços visíveis.")
```

### 1.4 — OCR Avançado

```python
def extract_text_from_image(image_path: str) -> str:
    """OCR avançado com GPT-4V"""
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Extraia TODO o texto desta imagem.

Para cada bloco de texto, indique:
- Posição (topo/centro/base, esquerda/direita)
- Tipo (título, parágrafo, número, etc)
- Conteúdo exato

Formate como JSON estruturado.""",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high",
                        },
                    },
                ],
            }
        ],
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content


# Uso
text_data = json.loads(extract_text_from_image("nota_fiscal.jpg"))
```

### 1.5 — Claude Vision (Anthropic)

```python
import anthropic
import base64
from PIL import Image
import io

client = anthropic.Anthropic()


def analyze_with_claude(image_path: str, prompt: str) -> str:
    """Análise de imagem com Claude Sonnet 4.5"""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # Detectar tipo MIME
    img = Image.open(image_path)
    mime_type = f"image/{img.format.lower()}"

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    return response.content[0].text


# Uso
analysis = analyze_with_claude(
    "raio_x.jpg",
    "Analise esta imagem médica. Descreva estruturas visíveis e possíveis anomalias. "
    "NOTA: isto é apenas para fins educacionais, não é diagnóstico médico."
)
```

### 1.6 — Casos de Uso

**E-commerce:**
- Extrair título, descrição, preço de fotos
- Detectar defeitos em produtos
- Categorização automática

**Documentos:**
- OCR de notas fiscais
- Extração de dados de contratos
- Processamento de formulários

**Mídia social:**
- Moderar conteúdo (unsafe)
- Gerar alt-text para acessibilidade
- Análise de sentimento por imagem

**Saúde (com disclaimer):**
- Análise de imagens médicas
- Triagem inicial (não diagnóstico)

---

## 🎤 Parte 2: Speech-to-Text (STT)

### 2.1 — Whisper (OpenAI)

**Capacidades:**
- 99 idiomas suportados
- Transcrição de áudios longos (até 25MB)
- Detecção automática de idioma
- Tradução para inglês
- Timestamps palavra-por-palavra

### 2.2 — Whisper API

```python
from openai import OpenAI

client = OpenAI()


def transcribe_audio(audio_path: str, language: str = "pt") -> str:
    """Transcreve áudio com Whisper"""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language,  # ISO 639-1
            response_format="text",  # text | json | srt | vtt
            temperature=0,  # mais determinístico
        )
    return response


# Uso
transcript = transcribe_audio("reuniao.mp3", language="pt")
print(transcript)
```

### 2.3 — Com Timestamps e Segmentos

```python
def transcribe_with_timestamps(audio_path: str) -> dict:
    """Transcrição detalhada com timestamps"""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"],
        )

    return {
        "text": response.text,
        "language": response.language,
        "duration": response.duration,
        "words": [
            {"word": w.word, "start": w.start, "end": w.end}
            for w in (response.words or [])
        ],
        "segments": [
            {"text": s.text, "start": s.start, "end": s.end}
            for s in (response.segments or [])
        ],
    }


# Uso (gerar legendas SRT)
result = transcribe_with_timestamps("video.mp4")
with open("legendas.srt", "w") as f:
    for i, seg in enumerate(result["segments"], 1):
        f.write(f"{i}\n")
        f.write(f"{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}\n")
        f.write(f"{seg['text']}\n\n")


def format_timestamp(seconds: float) -> str:
    """Converte segundos para formato SRT (HH:MM:SS,mmm)"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")
```

### 2.4 — Tradução de Áudio

```python
def translate_audio_to_english(audio_path: str) -> str:
    """Traduz áudio para inglês (independente do idioma original)"""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.translations.create(
            model="whisper-1",
            file=audio_file,
        )
    return response.text
```

### 2.5 — Casos de Uso

- **Reuniões:** transcrever Zoom, gerar atas
- **Vídeos:** legendas automáticas (SRT/VTT)
- **Podcasts:** transformar em blog posts
- **Atendimento:** gravar ligações, transcrever, analisar
- **Acessibilidade:** alt-text para vídeos

---

## 🔊 Parte 3: Text-to-Speech (TTS)

### 3.1 — OpenAI TTS

```python
from openai import OpenAI

client = OpenAI()


def text_to_speech(text: str, voice: str = "alloy", output_path: str = "output.mp3"):
    """Síntese de voz com OpenAI TTS"""
    response = client.audio.speech.create(
        model="tts-1",  # ou "tts-1-hd" para HD
        voice=voice,  # alloy, echo, fable, onyx, nova, shimmer
        input=text,
        speed=1.0,  # 0.25 a 4.0
    )

    response.stream_to_file(output_path)
    return output_path


# Uso
text_to_speech(
    "Olá! Bem-vindo à Nexus Affil'IA'te.",
    voice="nova",
    output_path="boas_vindas.mp3",
)
```

### 3.2 — Vozes Disponíveis

| Voz | Tom | Idioma | Uso |
|-----|-----|--------|-----|
| `alloy` | Neutro | EN/PT | Default, versátil |
| `echo` | Masculino grave | EN/PT | Narrativa, autoridade |
| `fable` | Britânico | EN | Storytelling |
| `onyx` | Masculino | EN/PT | Sério, formal |
| `nova` | Feminino energético | EN/PT | Marketing, vendas |
| `shimmer` | Feminino suave | EN/PT | Empatia, suporte |

### 3.3 — ElevenLabs (Vozes Mais Naturais)

```python
import requests
import os


def elevenlabs_tts(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM",
                   output_path: str = "output.mp3"):
    """
    TTS com ElevenLabs (vozes ultra-naturais).
    voice_id padrão: Rachel (feminino inglês)
    Outras: https://api.elevenlabs.io/v1/voices
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.environ["ELEVENLABS_API_KEY"],
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",  # suporta PT-BR
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


# Uso
elevenlabs_tts(
    "Olá! Eu sou a Marina, sua consultora de marketing.",
    voice_id="21m00Tcm4TlvDq8ikWAM",
    output_path="marina_voice.mp3",
)
```

### 3.4 — Voice Cloning (ElevenLabs)

```python
def clone_voice(name: str, audio_files: list, description: str = "") -> str:
    """
    Clona voz a partir de samples.
    audio_files: lista de paths de arquivos de áudio (WAV/MP3)
    """
    url = "https://api.elevenlabs.io/v1/voices/add"

    headers = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}

    data = {
        "name": name,
        "description": description,
    }

    files = [("files", (open(f, "rb").name, open(f, "rb"), "audio/mpeg"))
             for f in audio_files]

    response = requests.post(url, data=data, files=files, headers=headers)
    response.raise_for_status()

    voice_id = response.json()["voice_id"]
    return voice_id


# Uso
my_voice_id = clone_voice(
    name="Sir Nexus Alencar",
    audio_files=[
        "marca/personas/alencar/audio/official_voice.wav",
        # outros samples para treinar
    ],
    description="Voz oficial do Sir. Nexus Alencar",
)
```

### 3.5 — Streaming de Áudio

```python
def stream_tts(text: str, voice: str = "alloy"):
    """Streaming para latência mínima"""
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        # stream é default
    )

    # Reproduzir chunk por chunk
    for chunk in response.iter_bytes(chunk_size=1024):
        # tocar via PyAudio ou salvar
        yield chunk
```

---

## 🎨 Parte 4: Geração de Imagem

### 4.1 — DALL-E 3 (OpenAI)

```python
from openai import OpenAI
import requests

client = OpenAI()


def generate_image_dalle(prompt: str, size: str = "1024x1024",
                         quality: str = "standard", n: int = 1) -> list:
    """
    Gera imagem com DALL-E 3.
    size: 1024x1024, 1024x1792, 1792x1024
    quality: standard | hd
    """
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality=quality,
        n=n,
        response_format="url",  # ou "b64_json"
    )

    return [img.url for img in response.data]


# Uso
urls = generate_image_dalle(
    "Um gato astronauta flutuando no espaço, estilo digital art, cores vibrantes",
    size="1024x1024",
    quality="hd",
)

# Baixar
for url in urls:
    img_data = requests.get(url).content
    with open("gato_astronauta.png", "wb") as f:
        f.write(img_data)
```

### 4.2 — Flux (Black Forest Labs, open source)

```python
"""
Flux via Replicate API.
Modelos: flux-pro, flux-dev, flux-schnell (grátis)
"""
import replicate


def generate_image_flux(prompt: str, model: str = "flux-schnell") -> str:
    """Gera imagem com Flux"""
    if model == "flux-schnell":
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": prompt,
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "jpg",
                "output_quality": 90,
            },
        )
    elif model == "flux-dev":
        output = replicate.run(
            "black-forest-labs/flux-dev",
            input={
                "prompt": prompt,
                "num_outputs": 1,
                "aspect_ratio": "16:9",
                "output_format": "jpg",
            },
        )

    return output[0]  # URL da imagem


# Uso
url = generate_image_flux(
    "Paisagem cyberpunk de São Paulo 2090, neon, chuva, prédios altos",
    model="flux-schnell",
)
```

### 4.3 — Midjourney (via API terceira)

```python
"""
Midjourney via API GoAPI (ou outra).
Mais barato que Discord, suporta batch.
"""


def generate_image_midjourney(prompt: str) -> str:
    """Gera imagem com Midjourney"""
    import os
    import requests
    import time

    api_key = os.environ["GOAPI_KEY"]

    # Submit task
    response = requests.post(
        "https://api.goapi.ai/mj/v2/imagine",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"prompt": prompt},
    )
    task_id = response.json()["task_id"]

    # Poll
    while True:
        result = requests.get(
            f"https://api.goapi.ai/mj/v2/task/{task_id}",
            headers={"Authorization": f"Bearer {api_key}"},
        ).json()

        if result["status"] == "completed":
            return result["image_url"]
        elif result["status"] == "failed":
            raise Exception(result.get("error", "Unknown error"))

        time.sleep(5)
```

### 4.4 — Edição de Imagem (Inpainting)

```python
"""
Edita parte específica de uma imagem (inpainting).
Use case: trocar rosto, remover objeto, trocar fundo.
"""
from PIL import Image
import replicate


def inpaint_image(image_path: str, mask_path: str, prompt: str) -> str:
    """Substitui área da imagem (definida por mask) por conteúdo gerado"""
    with open(image_path, "rb") as img, open(mask_path, "rb") as mask:
        output = replicate.run(
            "stability-ai/stable-diffusion-inpainting",
            input={
                "image": img,
                "mask": mask,
                "prompt": prompt,
                "num_inference_steps": 50,
                "guidance_scale": 7.5,
            },
        )

    return output[0]
```

### 4.5 — Variações de Imagem

```python
def create_variations(image_path: str, n: int = 4) -> list:
    """Cria variações de uma imagem existente"""
    response = client.images.create_variation(
        image=open(image_path, "rb"),
        n=n,
        size="1024x1024",
    )

    return [img.url for img in response.data]
```

---

## 🎬 Parte 5: Geração de Vídeo

### 5.1 — Sora (OpenAI)

```python
"""
Sora: geração de vídeo a partir de texto.
Disponível via API (preview restrito).
"""


def generate_video_sora(prompt: str, duration: int = 5) -> str:
    """
    Gera vídeo com Sora.
    duration: 5, 10, 15, 20 segundos
    """
    # Em produção: usar SDK oficial
    # Aqui exemplo hipotético baseado em OpenAI API
    response = client.videos.generate(
        model="sora-1.0",
        prompt=prompt,
        duration=duration,
        resolution="1080p",
    )

    return response.video_url
```

### 5.2 — Runway Gen-3

```python
"""
Runway Gen-3: vídeo de alta qualidade, 5-10s.
"""
import requests


def generate_video_runway(prompt: str, image_url: str = None,
                          duration: int = 5) -> str:
    """
    Gera vídeo com Runway.
    Se image_url fornecido: image-to-video
    Senão: text-to-video
    """
    headers = {
        "Authorization": f"Bearer {os.environ['RUNWAY_API_KEY']}",
    }

    if image_url:
        # Image-to-video
        response = requests.post(
            "https://api.runwayml.com/v1/image_to_video",
            headers=headers,
            json={
                "image_url": image_url,
                "prompt": prompt,
                "duration": duration,
                "model": "gen3-alpha",
            },
        )
    else:
        # Text-to-video
        response = requests.post(
            "https://api.runwayml.com/v1/text_to_video",
            headers=headers,
            json={
                "prompt": prompt,
                "duration": duration,
                "model": "gen3-alpha",
            },
        )

    task_id = response.json()["task_id"]

    # Poll
    while True:
        result = requests.get(
            f"https://api.runwayml.com/v1/tasks/{task_id}",
            headers=headers,
        ).json()

        if result["status"] == "completed":
            return result["video_url"]
        elif result["status"] == "failed":
            raise Exception(result.get("error"))

        time.sleep(10)
```

### 5.3 — Síntese de Avatar (HeyGen / D-ID)

```python
"""
Gera vídeo com avatar falando (ideal para treinamentos).
"""


def generate_avatar_video(script: str, avatar_id: str = "default") -> str:
    """Gera vídeo com avatar realista"""
    # HeyGen API
    response = requests.post(
        "https://api.heygen.com/v2/video/generate",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
        json={
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": avatar_id,
                    },
                    "voice": {
                        "type": "text",
                        "input_text": script,
                        "voice_id": "pt-BR-FranciscaNeural",
                    },
                }
            ],
            "dimension": {"width": 1280, "height": 720},
        },
    )

    video_id = response.json()["data"]["video_id"]

    # Poll
    while True:
        status = requests.get(
            f"https://api.heygen.com/v2/video/{video_id}",
            headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
        ).json()

        if status["data"]["status"] == "completed":
            return status["data"]["video_url"]
        time.sleep(10)
```

---

## 🤖 Parte 6: Agente Multimodal Completo

### 6.1 — Caso: Atendente Visual para E-commerce

```python
"""
Agente que recebe foto do produto + pergunta do cliente.
Responde baseado em análise visual + RAG.
"""
from fastapi import FastAPI, UploadFile, File, Form
import tempfile
import os

app = FastAPI()


@app.post("/v1/agent/visual-support")
async def visual_support(
    image: UploadFile = File(...),
    question: str = Form(...),
    user_id: str = Form(...),
):
    """
    Recebe imagem + pergunta, responde com análise multimodal.
    """
    # Salvar imagem temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        content = await image.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # 1. Análise visual com GPT-4V
        visual_analysis = analyze_image(
            tmp_path,
            f"""Analise esta imagem e responda: {question}

            Forneça:
            - Descrição do que vê
            - Resposta à pergunta
            - Se há problemas/defeitos visíveis
            - Sugestões relevantes
            """,
        )

        # 2. RAG: buscar produtos similares ou informações adicionais
        kb_context = retrieve_from_kb(question)

        # 3. Gerar resposta final
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"""Você é um atendente visual da loja Nexus.
                    Use a análise visual + base de conhecimento para responder.
                    KB: {kb_context}""",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encode_image(tmp_path)}",
                            },
                        },
                    ],
                },
                {
                    "role": "assistant",
                    "content": visual_analysis,
                },
            ],
        )

        return {
            "user_id": user_id,
            "response": final_response.choices[0].message.content,
            "visual_analysis": visual_analysis,
        }

    finally:
        os.unlink(tmp_path)
```

### 6.2 — Caso: Videoaula Gerada Completamente por IA

```python
"""
Pipeline: roteiro → narração → vídeo com avatar → legendas
"""


def generate_complete_videoaula(topic: str, duration_min: int = 10) -> str:
    """Gera videoaula completa com IA"""

    # 1. Gerar roteiro
    script = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um professor especialista."},
            {"role": "user", "content": f"Crie roteiro de videoaula de {duration_min}min sobre: {topic}"},
        ],
    ).choices[0].message.content

    # 2. Gerar narração (TTS)
    audio_path = text_to_speech(script, voice="onyx", output_path="narration.mp3")

    # 3. Gerar slides (DALL-E ou Flux)
    slides = []
    for slide_prompt in extract_slide_prompts(script):
        url = generate_image_dalle(slide_prompt)[0]
        slides.append(download_image(url))

    # 4. Gerar avatar falando
    video_path = generate_avatar_video(script)

    # 5. Combinar tudo (FFmpeg)
    final_video = combine_video_audio_slides(
        video_path, audio_path, slides, output="videoaula_final.mp4"
    )

    # 6. Gerar legendas (Whisper)
    subtitles = transcribe_with_timestamps(audio_path)
    save_srt(subtitles["segments"], "videoaula.srt")

    return final_video
```

---

## 📋 Boas Práticas

### 1. Sempre Comunique que é IA

- Disclosure claro em imagens/vídeos gerados
- Watermark em conteúdo gerado (C2PA)
- Não use para deepfakes sem consentimento

### 2. Copyright e LGPD

- Não gere imagem de pessoa real sem consentimento
- Respeite copyright (não copie estilo de artista sem permissão)
- Logs de geração para auditoria

### 3. Custos

| Operação | Custo estimado |
|----------|----------------|
| GPT-4V (1k tokens) | $0.01-0.03 |
| Whisper (1 min áudio) | $0.006 |
| TTS OpenAI (1k chars) | $0.015 |
| TTS ElevenLabs (1k chars) | $0.30 |
| DALL-E 3 HD | $0.12 |
| Sora 5s | $0.50-2.00 |

### 4. Latência

| Operação | Latência |
|----------|----------|
| GPT-4V análise | 1-3s |
| Whisper 1min áudio | 2-5s |
| TTS 1k chars | 1-2s |
| DALL-E 3 | 5-15s |
| Sora 5s | 30-60s |

### 5. Cache e Reuso

- Cache de imagens geradas (hash do prompt)
- Cache de TTS (mesmo texto = mesmo áudio)
- Batch processing para vídeos

---

## 🛠️ Ferramentas

**Visão:**
- GPT-4V (OpenAI)
- Claude Vision (Anthropic)
- Google Cloud Vision (OCR)
- AWS Rekognition

**STT/TTS:**
- Whisper (OpenAI)
- ElevenLabs (vozes premium)
- Google Cloud Speech
- Amazon Polly

**Imagem:**
- DALL-E 3 (OpenAI)
- Midjourney
- Flux (open source)
- Stable Diffusion XL (self-hosted)

**Vídeo:**
- Sora (OpenAI)
- Runway Gen-3
- HeyGen (avatares)
- Pika Labs
- LumaLabs (Dream Machine)

---

## 📚 Materiais Complementares

- `tutoriais/24-redes-neurais-zero-hero.md` — fundamentos NN
- `apostilas/39-ia-generativa-avancada.md` — IA generativa
- `apostilas/45-debugging-otimizacao-agentes-ia.md` — debug
- `treinamentos/WS-09-oficina-marketing-conversacional.md` — agentes
- `marca/personas/VOZES-OFICIAIS.md` — vozes oficiais

---

## 🔗 Links Externos

- OpenAI Vision: https://platform.openai.com/docs/guides/vision
- Whisper: https://platform.openai.com/docs/guides/speech-to-text
- ElevenLabs: https://elevenlabs.io/
- Runway: https://runwayml.com/
- Flux: https://blackforestlabs.ai/

---

*AcademIA · Tutorial 25 · IA Multimodal · 2026*
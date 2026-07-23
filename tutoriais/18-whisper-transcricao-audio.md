---
title: "Transcrição de áudio com Whisper (OpenAI)"
tutorial_code: TUT-AG-01
level: agente
duration: 30min
prerequisites: []
tags: [tutorial, whisper, audio, transcrição, stt, openai, agents]
last_updated: 2026-07-07
---

# 🎙️ Transcrição de Áudio com Whisper (OpenAI)

> **Tempo:** 30 min · **Nível:** Agente · **Pré-requisito:** nenhum

## Problema

Você recebe áudios de clientes (WhatsApp, call center, podcasts) e
precisa transformar em texto para alimentar um agente, gerar resumo,
ou arquivar.

## Por que Whisper

- **Acurácia near-human** em 99+ idiomas (incluindo PT-BR)
- **Custo baixo**: US$ 0.006/minuto de áudio
- **Suporta timestamps** (segmento e palavra)
- **Detecção automática** de idioma
- **Tradução direta** PT → EN em uma chamada

## Setup (2 min)

```bash
pip install openai
echo "OPENAI_API_KEY=sk-proj-..." > .env
```

## Caso 1: Transcrição simples (5 min)

```python
from openai import OpenAI

client = OpenAI()

with open("entrevista.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="pt",         # opcional, detecta se omitido
    )

print(transcript.text)
```

## Caso 2: Com timestamps por segmento (10 min)

```python
with open("aula_90min.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="pt",
        response_format="verbose_json",
        timestamp_granularities=["segment", "word"],
    )

# Iterar segmentos
for seg in transcript.segments:
    print(f"[{seg.start:.1f}s - {seg.end:.1f}s] {seg.text}")

# Acessar palavras individuais (útil para legendas SRT)
for word in transcript.words[:10]:
    print(f"{word.word} @ {word.start:.2f}s")
```

## Caso 3: Tradução para inglês (5 min)

```python
with open("aula_portugues.mp3", "rb") as audio_file:
    translation = client.audio.translations.create(
        model="whisper-1",
        file=audio_file,
    )

print(translation.text)  # saída em inglês
```

## Caso 4: Pipeline completo de reunião (10 min)

```python
# meeting_pipeline.py
from openai import OpenAI
from pathlib import Path
import subprocess

client = OpenAI()

def transcribe_meeting(video_path: str) -> dict:
    # 1. Extrair áudio do vídeo (se for .mp4)
    audio_path = video_path.replace(".mp4", ".mp3")
    if not Path(audio_path).exists():
        subprocess.run([
            "ffmpeg", "-i", video_path, "-vn",
            "-acodec", "libmp3lame", "-q:a", "2", audio_path,
        ], check=True)

    # 2. Transcrever
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language="pt",
            response_format="verbose_json",
        )

    # 3. Resumir com GPT-4o
    summary_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"""Resuma esta transcrição de reunião:

1. Decisões tomadas (lista)
2. Action items (com responsáveis se mencionados)
3. Pontos em aberto
4. Tópicos principais com timestamps

Transcrição:
{transcript.text}"""
        }],
    )

    return {
        "transcript": transcript.text,
        "summary": summary_response.choices[0].message.content,
        "duration_minutes": transcript.duration / 60,
        "segments": len(transcript.segments),
    }

# Uso
result = transcribe_meeting("reuniao_2026_07_07.mp4")
print(result["summary"])
```

## Limites e Truques

### Limite de tamanho: 25 MB

Para áudios maiores, faça chunking:

```python
from pydub import AudioSegment

def chunk_audio(path: str, max_minutes: int = 20) -> list[str]:
    audio = AudioSegment.from_file(path)
    chunk_ms = max_minutes * 60 * 1000
    chunks = []
    for i in range(0, len(audio), chunk_ms):
        chunk = audio[i:i + chunk_ms]
        chunk_path = f"{path}.part_{i // chunk_ms}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)
    return chunks

# Processar
all_text = []
for chunk_path in chunk_audio("entrevista_3h.mp3"):
    with open(chunk_path, "rb") as f:
        t = client.audio.transcriptions.create(model="whisper-1", file=f)
        all_text.append(t.text)
full_transcript = " ".join(all_text)
```

### Prompt hints para vocabulário técnico

Whisper aceita um prompt inicial que melhora acurácia em termos específicos:

```python
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    prompt="Reunião sobre Nexus, MMN_IA, afiliados, SHO, Judge, IOAID, "
           "comissão, Inteligência Artificial, Machine Learning.",
)
```

### Custos estimados

| Cenário | Duração/mês | Custo/mês |
|---|---|---|
| 10 reuniões × 30min | 5 horas | $1.80 |
| 4 podcasts × 60min | 4 horas | $1.44 |
| 1000 chamadas × 2min | 33 horas | $12.00 |
| 10k chamadas × 5min | 833 horas | $300.00 |

## Caso avançado: Speaker Diarization (identificar quem falou)

Whisper não identifica speakers nativamente. Combine com `pyannote.audio`:

```bash
pip install pyannote.audio
```

```python
from pyannote.audio import Pipeline

# Modelo requer HuggingFace token
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="hf_...",
)

diarization = pipeline("reuniao.wav")

# Mapear speakers para transcrição do Whisper
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"[{turn.start:.1f}s - {turn.end:.1f}s] {speaker}:")
```

## Próximos passos

- **Realtime API**: conversa bidirecional com voz em tempo real
- **Text-to-Speech (TTS-1)**: gerar áudio a partir de texto
- **Multilingual RAG**: combinar transcrição + RAG para podcasts

## Recursos

- OpenAI Audio: <https://platform.openai.com/docs/guides/speech-to-text>
- Whisper paper: <https://arxiv.org/abs/2212.04356>
- pyannote.audio: <https://github.com/pyannote/pyannote-audio>
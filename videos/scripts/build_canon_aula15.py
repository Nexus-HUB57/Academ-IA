#!/usr/bin/env python3
"""
build_canon_aula15.py — vídeo CANÔNICO da aula 15 usando assets oficiais do repo.

Não produz capa/slide novos: usa 5 slides oficiais de `videos/aulas-onda-49/slides-oficiais/aula-15/`
+ capa-oficial.png. Áudio vem do TTS gerado com fala real do roteiro.

Mapeamento (verificado contra analytics da understand_images):
  capa-oficial          3.0s  silencio  -> capa abertura
  cena-01-hero          7.2s  Ive  - "Você não vai aprender ROI..."
  cena-01-hero         19.37s Alencar - "ROI tradicional / IA 3 problemas"
  cena-02-stats        16.03s Alencar - "Exemplo 1.100%"
  cena-03-cards        25.32s Alencar - "ROI Nexus 4 camadas"
  cena-04-pyramid      26.21s Alencar - "12 métricas oficiais"
  cena-05-cta           8.74s Ive  - "oneverso / apostila 15"
"""
import asyncio, sys, subprocess, shutil
from pathlib import Path
import edge_tts

ROOT = Path("/home/user/academ_ia")
OFFICIAL = ROOT / "videos" / "aulas-onda-49" / "slides-oficiais" / "aula-15"
PILOTO = ROOT / "videos" / "aulas-onda-49" / "piloto" / "aula-15"
PARSER = PILOTO      # parser outputs estão aqui
CLIPS = PILOTO / "clips_canon"
CLIPS.mkdir(parents=True, exist_ok=True)


def ffmpeg(*args):
    r = subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + list(args),
        capture_output=True, text=True,
    )
    return r.returncode, r.stdout, r.stderr


def dur_s(p):
    return float(subprocess.check_output(
        ["ffprobe","-v","error","-show_entries","format=duration",
         "-of","csv=p=0", str(p)], text=True).strip())


# ── 1) Garantir audios TTS (só 6 cenas geradas pelo parser) ──
VOZES = {
    "Alencar":  ("pt-BR-AntonioNeural",   "-3%", "+0Hz"),
    "Ive":      ("pt-BR-FranciscaNeural", "-3%", "+1Hz"),
    "Narrador": ("pt-BR-FranciscaNeural", "-3%", "+0Hz"),
}

sys.path.insert(0, str(ROOT / "videos" / "scripts"))
from parse_roteiro_piloto import parse_roteiro

ROTEIRO = ROOT / "videos" / "aulas-onda-49" / "roteiros" / "aula-15-metricas-roi-ecossistema.md"
parsed = parse_roteiro(ROTEIRO)
parsed_scenes = sorted(parsed["scenes"], key=lambda s: s["n"])
print(f"⚙ parsed {len(parsed_scenes)} cenas do roteiro")


# Textos exatos referenciados no parser
def get_narration(scene, fallback=""):
    return (scene.get("narration") or fallback).strip()


async def ensure_audios():
    audios = {}
    for s in parsed_scenes:
        persona = s["persona"]
        voice, rate, pitch = VOZES[persona]
        audio = PILOTO / "audios" / f"cena-{s['n']:02d}.mp3"
        text = (s["narration"] or "").strip()
        if not audio.exists() or audio.stat().st_size < 100:
            if text:
                comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
                await comm.save(str(audio))
        audios[s["n"]] = audio
        d = dur_s(audio)
        print(f"  ✓ cena {s['n']:>2} {persona:8s} {d:5.2f}s — {text[:65]!r}")
    return audios


def main_canon(audios):
    cover_silence = PILOTO / "audios" / "00-cover-silence-3s.mp3"
    ffmpeg("-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=22050",
           "-t","3","-q:a","9","-acodec","libmp3lame", str(cover_silence))

    # Definicao da trilha (slide, audio, target_dur_s)
    # 5 slides oficiais + capa (reutilizacao do hero em 2 audio slots)
    track = [
        ("capa-oficial.png", cover_silence, 3.0,   "CAPA OFICIAL"),
        ("cena-01-hero.png", audios[1],   7.20,  "HERO + abertura"),
        ("cena-01-hero.png", audios[2],   19.37, "HERO + ROI tradicional"),
        ("cena-02-stats.png", audios[5],  16.03, "STATS + exemplo 1.100%"),
        ("cena-03-cards.png", audios[3],  25.32, "CARDS + 4 dimensoes"),
        ("cena-04-pyramid.png", audios[4],26.21, "PYRAMID + 12 metricas"),
        ("cena-05-cta.png",   audios[6],  8.74,  "CTA + oneverso"),
    ]

    # Track acumulado para spot-check
    timeline = []

    for idx, (slide_name, audio, target_dur, label) in enumerate(track, 1):
        slide = OFFICIAL / slide_name
        if not slide.exists():
            raise SystemExit(f"❌ slide oficial nao encontrado: {slide}")

        out = CLIPS / f"clip-{idx:02d}.mp4"
        # use -shortest; ffmpeg will keep up to audio length (or target_dur if audio < target)
        # we provide -t to force target as max
        rc, _, err = ffmpeg(
            "-loop","1","-framerate","30",
            "-t", str(target_dur),
            "-i", str(slide),
            "-i", str(audio),
            "-shortest",
            "-vf","scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-c:v","libx264","-preset","ultrafast","-crf","22",
            "-c:a","aac","-b:a","128k",
            str(out),
        )
        if rc != 0:
            raise RuntimeError(f"clip {idx} falhou: {err[:400]}")

        actual_dur = dur_s(out)
        timeline.append((idx, slide_name, audio, label, target_dur, actual_dur))
        print(f"  🎬 clip {idx:>2} {label} target={target_dur}s  actual={actual_dur:.2f}s")

    # Print timeline tabela
    print("\n═══ Spot-check timeline ═══")
    start = 0.0
    for idx, slide_name, audio, label, t, a in timeline:
        print(f"  clip {idx:>2}  in={start:6.2f}s  -> {start+a:6.2f}s  ({label:32s}) {slide_name}")
        start += a
    print(f"  TOTAL = {start:.2f}s")

    # ── 2) Concat demuxer ──
    listf = PILOTO / "list_canon.txt"
    listf.write_text("\n".join(f"file '{p.resolve()}'" for p in sorted(CLIPS.glob("clip-*.mp4"))))
    out = PILOTO / "aula-piloto-15-canon.mp4"
    ffmpeg(
        "-f","concat","-safe","0","-i", str(listf),
        "-c","copy",
        "-movflags","+faststart",
        str(out),
    )

    final = dur_s(out)
    sz = out.stat().st_size
    nstreams = subprocess.check_output(
        ["ffprobe","-v","error","-show_entries","format=nb_streams",
         "-of","csv=p=0", str(out)], text=True).strip()
    print(f"\n🟢 CANON {out.name}: {sz//1024} KB · {final:.2f}s · streams={nstreams}")
    return out, timeline


if __name__ == "__main__":
    audios = asyncio.run(ensure_audios())
    main_canon(audios)

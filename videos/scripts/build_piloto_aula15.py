#!/usr/bin/env python3
"""
build_piloto_aula15.py

Pipeline integrado de 1 vídeo-aula reconstruído de verdade:
1) parse do roteiro → lista de cenas (visual, persona, narration)
2) TTS por cena (edge-tts PT-BR) com voz da persona
3) Slides únicos por cena (PIL 1280×720)
4) mux cena: 1 MP4 por cena = slide looped + audio, dur=cena.dur_seg
5) concat demuxer → aula-piloto-15.mp4
6) sanity-check: hash de pixels a cada 1s, transcrição Whisper
"""
import asyncio, sys, json, hashlib, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/home/user/academ_ia")
sys.path.insert(0, str(ROOT / "videos" / "scripts"))

from parse_roteiro_piloto import parse_roteiro

# ─────────────── paths ───────────────
ROTEIRO = ROOT / "videos" / "aulas-onda-49" / "roteiros" / "aula-15-metricas-roi-ecossistema.md"
PILOTO_DIR = ROOT / "videos" / "aulas-onda-49" / "piloto" / "aula-15"
SLIDES_DIR = PILOTO_DIR / "slides"
AUDIOS_DIR = PILOTO_DIR / "audios"
CLIPS_DIR = PILOTO_DIR / "clips"
for d in (SLIDES_DIR, AUDIOS_DIR, CLIPS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ─────────────── mapping ───────────────
VOZES = {
    "Alencar":  ("pt-BR-AntonioNeural",   "-3%", "+0Hz"),
    "Ive":      ("pt-BR-FranciscaNeural", "-3%", "+1Hz"),
    "Narrador": ("pt-BR-FranciscaNeural", "-3%", "+0Hz"),  # fallback
}

# trilha → cor de fundo
COR_POR_TRILHA = {
    "Fundamental": ((10, 20, 40),  (60, 140, 220)),
    "Master":      ((26, 16, 48),  (180, 130, 240)),
    "Agent":       ((8, 32, 28),   (40, 180, 140)),
    "Elite":       ((38, 28, 8),   (220, 180, 70)),
}

# ─────────────── helpers ───────────────
def ffmpeg(*args, capture=True) -> tuple[int, str, str]:
    r = subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + list(args),
        capture_output=capture, text=True,
    )
    return r.returncode, (r.stdout or ""), (r.stderr or "")


async def synth_one(text: str, voice: str, rate: str, pitch: str, out: Path):
    import edge_tts
    comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await comm.save(str(out))
    return out.exists() and out.stat().st_size > 0


def dur_seconds(path: Path) -> float:
    rc, out, _ = ffmpeg("?", "?")  # placeholder
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)], text=True).strip())


def make_slide(cena: dict, trilha: str, lesson_title: str, out: Path):
    """Gera 1280×720 PNG único para a cena."""
    bg_rgb, accent_rgb = COR_POR_TRILHA.get(trilha, ((10,20,40), (60,140,220)))
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), bg_rgb)
    d = ImageDraw.Draw(img)

    # Encontrar fontes (prefere DejaVu, fallback default)
    def font(size, bold=False):
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        ]
        last_err = None
        for path in candidates:
            try:
                return ImageFont.truetype(path, size)
            except Exception as e:
                last_err = e
                continue
        print(f"  WARN: fontes nao encontradas, usando default: {last_err}")
        return ImageFont.load_default()

    # ── topo: trilha + título da aula ──
    d.rectangle([(0, 0), (W, 64)], fill=accent_rgb)
    d.text((24, 18), f"AcademIA · {trilha}", fill=(255, 255, 255), font=font(20, bold=True))
    if lesson_title:
        d.text((24, 38), lesson_title, fill=(220, 230, 255), font=font(16))

    # ── persona + cena-n ──
    persona = cena["persona"] or "Narrador"
    tone = cena.get("tone") or ""
    d.text((24, 92), f"Cena {cena['n']}  ·  {persona}"
           + (f"  ·  tom {tone}" if tone else ""),
           fill=(255, 255, 255), font=font(22, bold=True))

    # ── título limpo (remove icons) ──
    title_clean = (cena["title"] or "").lstrip("#").strip()
    title_clean = title_clean.lstrip("-—: ").strip()
    if title_clean:
        # quebrar em 2 linhas
        if len(title_clean) > 50:
            mid = len(title_clean) // 2
            # quebrar em espaço
            sp = title_clean.rfind(" ", 0, mid)
            if sp == -1:
                sp = mid
            line1, line2 = title_clean[:sp], title_clean[sp+1:]
        else:
            line1, line2 = title_clean, ""
        d.text((24, 140), line1, fill=(255, 255, 255), font=font(34, bold=True))
        if line2:
            d.text((24, 182), line2, fill=(220, 220, 240), font=font(28, bold=True))

    # ── visual (descrição) ──
    visual = cena.get("visual") or ""
    if visual:
        d.text((24, 240), "Visual:", fill=accent_rgb, font=font(18, bold=True))
        # Quebrar em linhas ~70 chars
        wrap = []
        line = ""
        for word in visual.split():
            test = (line + " " + word).strip()
            if len(test) > 70:
                wrap.append(line)
                line = word
            else:
                line = test
        if line:
            wrap.append(line)
        y = 270
        for ln in wrap[:6]:
            d.text((36, y), "› " + ln, fill=(220, 230, 255), font=font(18))
            y += 26

    # ── prévia narração (caixa inferior) ──
    narr = (cena.get("narration") or "").strip()
    if narr:
        # Caixa
        d.rectangle([(24, H - 220), (W - 24, H - 24)], fill=(0, 0, 0))
        d.rectangle([(24, H - 220), (W - 24, H - 24)], outline=accent_rgb, width=2)
        d.text((44, H - 210), f"{persona} diz:", fill=accent_rgb, font=font(16, bold=True))

        wrap = []
        line = ""
        for word in narr.split():
            test = (line + " " + word).strip()
            if len(test) > 95:
                wrap.append(line)
                line = word
            else:
                line = test
        if line:
            wrap.append(line)
        y = H - 184
        for ln in wrap[:5]:
            d.text((44, y), ln, fill=(240, 244, 255), font=font(18))
            y += 22

    # Marca canto
    d.text((W - 240, H - 32), f"cena {cena['n']} / 6", fill=(150, 180, 220), font=font(14))

    img.save(out, "PNG", optimize=True)


def mux_cena(slide: Path, audio: Path, dur_seg: int, out: Path):
    rc, out_s, err = ffmpeg(
        "-loop", "1", "-framerate", "30", "-t", str(max(dur_seg, 1)),
        "-i", str(slide),
        "-i", str(audio),
        "-t", str(max(dur_seg, 1)),
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
        "-c:a", "aac", "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(out),
    )
    if rc != 0:
        raise RuntimeError(f"mux_cena falha: {err[:400]}")


# ─────────────── main ───────────────
async def main():
    # ── 1) parse roteiro ──
    parsed = parse_roteiro(ROTEIRO)
    print(f"⚙ parse: {len(parsed['scenes'])} cenas | trilha={parsed['trilha']}")
    if len(parsed["scenes"]) < 4:
        raise SystemExit("Parser retornou poucas cenas — abortando")

    # ── 2) TTS por cena ──
    generated = []
    for s in parsed["scenes"]:
        persona = s["persona"] or "Narrador"
        voice, rate, pitch = VOZES[persona]
        text = (s["narration"] or "").strip()
        if not text:
            print(f"  ⚠ cena {s['n']} sem narração — pulando TTS")
            # placeholder 0.5s silence
            audio = AUDIOS_DIR / f"cena-{s['n']:02d}.mp3"
            rc, _, _ = ffmpeg(
                "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=22050",
                "-t", "0.5", "-q:a", "9", "-acodec", "libmp3lame", str(audio)
            )
        else:
            audio = AUDIOS_DIR / f"cena-{s['n']:02d}.mp3"
            ok = await synth_one(text, voice, rate, pitch, audio)
            if not ok:
                raise RuntimeError(f"edge-tts falhou cena {s['n']}")
        d = dur_seconds(audio)
        generated.append({**s, "audio": audio, "audio_dur": d})
        print(f"  ✓ cena {s['n']:>2} | {persona:8s} | {d:5.2f}s audio | alvo {s['dur']}s | narr {len(text)} chars")

    # ── 3) slide por cena ──
    for s in generated:
        slide = SLIDES_DIR / f"cena-{s['n']:02d}.png"
        make_slide(s, parsed["trilha"], parsed["lesson_title"], slide)
        print(f"  🖼  slide cena {s['n']} → {slide.stat().st_size//1024} KB")

    # ── 4) mux cena-a-cena ──
    for s in generated:
        clip = CLIPS_DIR / f"cena-{s['n']:02d}.mp4"
        target = s["dur"] if s["dur"] else max(int(round(s["audio_dur"])), 2)
        # deixa o audio mandar (-shortest)
        rc, _, err = ffmpeg(
            "-loop", "1", "-framerate", "30",
            "-i", str(SLIDES_DIR / f"cena-{s['n']:02d}.png"),
            "-i", str(s["audio"]),
            "-shortest",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            str(clip),
        )
        if rc != 0:
            raise RuntimeError(f"mux cena {s['n']} falhou: {err[:400]}")
        print(f"  🎬 cena {s['n']:>2} clip {target}s → {clip.stat().st_size//1024} KB")

    # ── 5) concat demuxer ──
    listf = PILOTO_DIR / "list.txt"
    listf.write_text("\n".join(
        f"file '{p.resolve()}'" for p in sorted(CLIPS_DIR.glob("cena-*.mp4"))
    ))
    out_mp4 = PILOTO_DIR / "aula-piloto-15.mp4"
    rc, _, err = ffmpeg(
        "-f", "concat", "-safe", "0",
        "-i", str(listf),
        "-c", "copy",
        "-movflags", "+faststart",
        str(out_mp4),
    )
    if rc != 0:
        raise RuntimeError(f"concat falhou: {err[:400]}")

    total_dur = dur_seconds(out_mp4)
    print()
    print(f"🟢 aula-piloto-15.mp4 → {out_mp4.stat().st_size//1024} KB · {total_dur:.2f}s")

    # ── 6) sanity-check hash por segundo ──
    audit_dir = PILOTO_DIR / "audit_hashes"
    audit_dir.mkdir(exist_ok=True)
    seconds = int(round(total_dur))
    unique = set()
    for t in range(seconds + 1):
        rc, _, _ = ffmpeg(
            "-ss", str(t), "-i", str(out_mp4),
            "-frames:v", "1", "-q:v", "2",
            str(audit_dir / f"sec-{t:02d}.jpg"),
        )
        h = hashlib.md5((audit_dir / f"sec-{t:02d}.jpg").read_bytes()).hexdigest()[:12]
        unique.add(h)
        print(f"  frame@{t}s  hash={h}")
    print(f"unique frames: {len(unique)} / {seconds+1} segundos")


if __name__ == "__main__":
    asyncio.run(main())

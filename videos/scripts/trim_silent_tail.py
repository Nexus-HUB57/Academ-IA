#!/usr/bin/env python3
"""
Clipa o final silencioso dos 19 videos *-narrated.mp4 da Onda-49.

Estrategia:
1) Detectar ultimo silencio_start que dura ate o fim do audio (>=1s).
2) Cortar o video em (last_speech_end + tail_silence_tolerance).
3) Re-encoda com mesma qualidade (h264 + aac copy) preservando metadados.
"""
import subprocess
import re
import sys
from pathlib import Path
import json
import shutil

ROOT = Path("/home/user/academ_ia")
RENDER_DIR = ROOT / "videos" / "aulas-onda-49" / "renders"
SRC_MP3_DIR = ROOT / "videos" / "aulas-onda-49" / "audios"
TAIL_TOLERANCE = 1.0  # quanto silencio manter apos a fala (seguro p/ transicao)
THRESHOLD_DB = -35.0
MIN_SIL_DURATION = 0.5

# ──────────────────────────── helpers ────────────────────────────

def dur(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0", str(path)],
        capture_output=True, text=True, timeout=15,
    )
    s = (r.stdout or "0").strip()
    return float(s) if s else 0.0

def detect_last_speech(path: Path) -> tuple[float,int]:
    """Retorna (last_speech_end_seconds, total_silence_segments)."""
    r = subprocess.run([
        "ffmpeg","-hide_banner","-i",str(path),
        "-af",f"silencedetect=noise={THRESHOLD_DB}dB:d={MIN_SIL_DURATION}",
        "-f","null","-"
    ], capture_output=True, text=True, timeout=120)
    starts = []
    ends = []
    pattern = re.compile(r"silence_(start|end):\s*([0-9.]+)")
    for ln in r.stderr.split("\n"):
        for m in pattern.finditer(ln):
            kind, val = m.group(1), float(m.group(2))
            (starts if kind=="start" else ends).append(val)
    if not starts:
        return dur(path), 0

    # Emparalha intervalos (assume alternancia): start_i -> end_i
    # Em filtragens reais com d>0.5, deve haver aproximadamente mesma qtde de end e start.
    # O par LAST silence_start/end eh o candidato ao tail silence.
    # Estrategia: o ULTIMO end que eh >= 0.95 * total == confirma fim do audio.
    total = dur(path)
    tail_speech_end = None

    # Emparelhar
    pairs = []
    i = j = 0
    while i < len(starts) and j < len(ends):
        pairs.append((starts[i], ends[j]))
        i += 1
        j += 1
    # O evento que cobre ate o final
    for s,e in reversed(pairs):
        if e >= total - 0.5:
            tail_speech_end = s
            break
    if tail_speech_end is None:
        return total, len(pairs)
    return tail_speech_end, len(pairs)

def trim_video(src: Path, dst: Path, cut_at: float):
    """Recorta video ate cut_at (em segundos), copiando streams."""
    # sem -c copy pq audio pode ter samplerate mismatch; recomprimir rapido
    cmd = [
        "ffmpeg","-y","-hide_banner","-loglevel","error",
        "-i", str(src),
        "-t", f"{cut_at:.3f}",
        "-c:v","libx264","-preset","ultrafast","-crf","20",
        "-c:a","aac","-b:a","96k",
        "-movflags","+faststart",
        "-metadata","comment=Onda-49 v2 — silent-tail trimmed",
        str(dst),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return r.returncode == 0, r.stderr

# ──────────────────────────── main ────────────────────────────

def main():
    plan = []
    for v in sorted(RENDER_DIR.glob("*-narrated.mp4")):
        stem = v.name.replace("-narrated.mp4","")
        total = dur(v)
        last_speech, nsil = detect_last_speech(v)
        cut = max(last_speech + TAIL_TOLERANCE, 1.0)
        cut = min(cut, total)  # nao posso cortar mais que o total
        plan.append((stem, v, total, last_speech, cut, nsil))

    print("═"*110)
    print(f"{'aula':<48}  {'total':>7}  {'last_sp':>8}  {'cut_v2':>7}  {'#sil':>4}  economia")
    print("─"*110)
    total_cut = 0
    total_orig = 0
    for stem, v, t, ls, c, ns in plan:
        saving = t - c
        total_cut += saving
        total_orig += t
        pct = saving/t*100 if t>0 else 0
        print(f"  {stem:<48}  {t:>7.2f}  {ls:>8.2f}  {c:>7.2f}  {ns:>4}  -{pct:>5.1f}% ({saving:.2f}s)")
    print()
    print(f"Total original: {total_orig/60:.2f} min  →  apos corte: {(total_orig-total_cut)/60:.2f} min")
    print(f"Economia absoluta: {total_cut/60:.2f} min")
    print()

    # executar
    json_plan = {"applied_tail_tolerance": TAIL_TOLERANCE, "threshold_db": THRESHOLD_DB,
                 "min_silence_dur": MIN_SIL_DURATION, "items": []}
    for stem, v, t, ls, c, ns in plan:
        out = RENDER_DIR / f"{stem}-narrated-v2.mp4"
        print(f"⏵ trim {stem}: total={t:.2f}s → cut@{c:.2f}s")
        ok, err = trim_video(v, out, c)
        if not ok:
            print(f"  ❌ FALHA: {err[:400]}")
            continue
        new_dur = dur(out)
        json_plan["items"].append({
            "stem": stem, "src": str(v), "dst": str(out),
            "orig_dur": t, "last_speech": ls, "cut_at": c,
            "actual_v2_dur": new_dur, "saving_s": t - new_dur,
            "silence_segments_detected": ns,
        })
        print(f"  ✅ {new_dur:.2f}s (economia real: {t-new_dur:.2f}s)")

    # grava plano
    plan_path = ROOT / "videos" / "aulas-onda-49" / "trim_plan.json"
    plan_path.write_text(json.dumps(json_plan, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n📋 Plano salvo em: {plan_path}")

    if "--commit" in sys.argv:
        # commit do batch
        msg = "Onda-49: trim silent-tail nos 19 narrated v2 (ffmpeg silencedetect-driven)"
        subprocess.run(["git","add","-A","videos/aulas-onda-49"], cwd=str(ROOT), check=False)
        subprocess.run(["git","commit","-m", msg], cwd=str(ROOT), check=False)
        print("📦 Commit efetuado")

if __name__ == "__main__":
    main()

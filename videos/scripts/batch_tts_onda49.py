#!/usr/bin/env python3
"""
Academ'IA - TTS em lote para ONDA-49 (19 roteiros)
- Lê roteiros videos/aulas-onda-49/roteiros/aula-NN-*.md
- Extrai texto narrável (body, sem frontmatter, sem headings, sem listas, sem code)
- Resolve persona -> voz edge-tts PT-BR
- Salva MP3 original em videos/aulas-onda-49/audios/aula-NN-*.mp3
- Gera também versao "16:9 silent lecture" pronta p/ mux
- Mantém submix Mono p/ 1 pessoa; Stereo interleaved p/ "dupla"
"""
import asyncio
import re
from pathlib import Path
import edge_tts

ROOT = Path(".").resolve()
ROTEIROS = ROOT / "videos" / "aulas-onda-49" / "roteiros"
AUDIOS = ROOT / "videos" / "aulas-onda-49" / "audios"
AUDIOS.mkdir(parents=True, exist_ok=True)

# Mapeamento persona -> voz edge-tts PT-BR
# 'dupla' gera 2 audios (uma por voz) e sao concatenados no mux
VOICE_MAP = {
    "alencar": [("pt-BR-AntonioNeural", "M")],
    "ive":     [("pt-BR-FranciscaNeural", "F")],
    "dupla":   [("pt-BR-AntonioNeural", "M"),
                ("pt-BR-FranciscaNeural", "F")],
}

# Frontmatter nao pode virar audio
def parse_meta(text):
    if text.startswith("---"):
        try:
            _, fm, body = text.split("---", 2)
            import yaml
            return yaml.safe_load(fm) or {}, body.lstrip()
        except Exception:
            return {}, text
    return {}, text

# Limpa MD para virar audio: remove headings, code blocks, listas,
# blockquotes, links, imagens, tabelas, emojis de severo ruido.
def clean_to_spoken(body):
    text = body
    # code fences
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"`[^`]+`", " ", text)
    # imagens e links markdown
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # headings, listas, blockquotes
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)
    # tabelas: remove pipes
    text = re.sub(r"^\s*\|.*\|$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\|", " ", text)
    # emojis leves e bullets unicode
    text = re.sub(r"[\u2700-\u27BF\u2600-\u26FF\u2B00-\u2BFF\u1F300-\u1F6FF\u1F900-\u1F9FF]", "", text)
    # marcações de ênfase
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"_([^_]+)_", r"\1", text)
    # normaliza whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

async def synth_one(voice, text, out_path, rate="+0%", pitch="+0Hz"):
    # 200 chars por chunk evita travas em textos >10K
    chunks = [text[i:i+1500] for i in range(0, len(text), 1500)] if text else []
    if not chunks:
        return False
    # edge-tts suporta concatenar via Communicate.save() com string longa,
    # mas para robustness usamos sequence e concatenamos MP3 após.
    import tempfile, subprocess
    tmpdir = Path(tempfile.mkdtemp(prefix="tts_"))
    part_files = []
    for i, chunk in enumerate(chunks):
        p = tmpdir / f"part_{i:03d}.mp3"
        comm = edge_tts.Communicate(chunk, voice, rate=rate, pitch=pitch)
        await comm.save(str(p))
        part_files.append(p)
    # concat via ffmpeg
    if len(part_files) == 1:
        out_path.write_bytes(part_files[0].read_bytes())
    else:
        listf = tmpdir / "list.txt"
        listf.write_text("\n".join(f"file '{p.name}'" for p in part_files))
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-f", "concat", "-safe", "0",
             "-i", str(listf),
             "-c", "copy", str(out_path)],
            check=True, cwd=str(tmpdir))
    return out_path.exists()


async def main():
    mds = sorted(ROTEIROS.glob("aula-*.md"))
    print(f"Roteiros ONDA-49 encontrados: {len(mds)}")
    print(f"Audios dir: {AUDIOS}")
    print("=" * 72)

    generated = []
    falhas = []
    for md in mds:
        stem = md.stem  # e.g. aula-15-metricas-roi-ecossistema
        text = md.read_text(encoding="utf-8")
        meta, body = parse_meta(text)
        persona = (meta.get("persona") or meta.get("voice") or "dupla").lower()
        personas = VOICE_MAP.get(persona, VOICE_MAP["dupla"])
        spoken = clean_to_spoken(body)
        if not spoken:
            falhas.append((stem, "vazio após clean"))
            continue
        # tag com persona no filename
        out = AUDIOS / f"{stem}-{persona}.mp3"
        try:
            ok = await synth_one(personas[0][0], spoken, out,
                                 rate="-5%", pitch="+0Hz")
            if ok:
                generated.append((stem, persona, out))
                size = out.stat().st_size
                print(f"  OK  {stem:50s} persona={persona:8s} {size:>7d}b")
            else:
                falhas.append((stem, "synth retornou vazio"))
        except Exception as e:
            falhas.append((stem, str(e)[:80]))
            print(f"  ER {stem:50s} {e}")

        # se for dupla, gerar segundo audio (F) para mux stereo L/R
        if persona == "dupla" and len(personas) > 1:
            out2 = AUDIOS / f"{stem}-dupla-F.mp3"
            try:
                ok = await synth_one(personas[1][0], spoken, out2,
                                     rate="-3%", pitch="+1Hz")
                if ok:
                    size = out2.stat().st_size
                    print(f"  OK2 {stem:50s} persona=dupla-F   {size:>7d}b")
            except Exception as e:
                print(f"  ER2 {stem:50s} {e}")

    print()
    print(f"Gerados : {len(generated)}")
    if falhas:
        print(f"Falhas  : {len(falhas)}")
        for s, e in falhas: print(f"  - {s}: {e}")


if __name__ == "__main__":
    asyncio.run(main())

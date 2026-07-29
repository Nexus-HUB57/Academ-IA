#!/usr/bin/env python3
"""
Academ'IA - Parser de roteiro para produção do vídeo-piloto.

Lê `videos/aulas-onda-49/roteiros/aula-NN-*.md` e devolve lista de cenas com:
- n, title, dur_seconds
- visual: descrição visual do slide
- persona: Alencar | Ive | Narrador
- tone: pista de tom de voz (acolhedora, didático, ...)
- narration: TEXTO REAL que deve ser falado (string única, sem markdown)

Onde o markdown tem blockquote `> "..."` para fala, esse texto é o que vai pra TTS.
Suporta os 3 formatos observados no repo: canônico (aulas 01-14), ONDA-49 com
cabeçalho `> Trilha ...` (aulas 16+), e bullet-quirk de aulas 18+.
"""
import re
import json
import sys
import yaml
from pathlib import Path

ROOT = Path("/home/user/academ_ia")

# Regex auxiliares -----------------------------------------------------------------
RE_H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)

RE_DUR = re.compile(
    r"\(\s*(?:Duração:\s*)?(\d+(?:[.,]\d+)?)\s*(s|segundos?|min|minutos?)?\s*\)",
    re.I,
)
RE_CENA_N = re.compile(r"(?:Cena|Slide)\s*(\d+)", re.I)
RE_ICONS = re.compile(r"[🎬📚📊🧮📈🎯💡🔧⚙️🛡️🎓📖🚀⚡🌐👥💰🎨🧠🔍🏗️]")
RE_LEAD = re.compile(r"^(Cena|Slide)\s*\d+\s*[-:—]?\s*", re.I)

RE_VISUAL = re.compile(
    r"^\s*[-*]?\s*\*?\*?(?:Visual|Imagem|Slide|Background|Cena\s+visual)\*?\*?\s*[:\-]?\s*(.+?)\s*$",
    re.I,
)
# Aceita QUALQUER uma:
#   **Narração Ive** (acolhedora):           <- persona dentro de **
#   **Narração** (acolhedora) Ive:
#   **Narração** Ive:
#   - Narração Ive:
#   Narração Ive:
RE_NARR_HEADER = re.compile(
    r"^\s*[-*]?\s*\*+\s*(?:Narração|Narracao|Voz|Fala)\s*(?:\*+\s*)?(?:"
    r"(?P<persona>Alencar|Ive|Narrador|Alencar\s*\+\s*Ive)\s*\*+\s*"
    r"|\s*(?P<persona2>Alencar|Ive|Narrador|Alencar\s*\+\s*Ive)\s*"
    r")?"
    r"(?:\((?P<tone>[^)]*)\))?\s*:?\s*$",
    re.I,
)
_RE_NARR_LINE_FALLBACK = re.compile(
    r"^\s*[-*]?\s*(?:Narração|Narracao|Voz|Fala)\s*(?:da|do)?\s*"
    r"(?P<persona>Alencar|Ive|Narrador|Alencar\s*\+\s*Ive)\s*:?\s*(?:\((?P<tone>[^)]*)\))?\s*$",
    re.I,
)

PERSONA_FALLBACK = {
    "alencar": "Alencar",
    "ive":     "Ive",
    "narrador":"Narrador",
    "dupla":   "Ive",  # default dentro de uma cena "dupla" -> Vamos a cena-a-cena
    None:      "Narrador",
}


def _split_scenes(body: str) -> list[tuple[str, str]]:
    """Divide corpo em blocos por H2. Retorna [(h2, rest_body), ...]."""
    lines = body.split("\n")
    positions = [i for i, ln in enumerate(lines) if ln.startswith("## ")]
    if not positions:
        return []
    positions.append(len(lines))
    out = []
    for k in range(len(positions) - 1):
        out.append((
            lines[positions[k]],
            "\n".join(lines[positions[k] + 1 : positions[k + 1]]),
        ))
    return out


def _parse_scene_block(h2_line: str, body: str, fallback_n: int) -> dict:
    """Extrai cena do par (h2, body)."""
    # Duração
    md = RE_DUR.search(h2_line)
    dur_s = None
    if md:
        v = float(md.group(1).replace(",", "."))
        u = (md.group(2) or "s").lower()
        if u.startswith("min"):
            dur_s = int(round(v * 60))
        else:
            dur_s = int(round(v))

    # Cena number
    mn = RE_CENA_N.search(h2_line)
    scene_n = int(mn.group(1)) if mn else fallback_n

    # Title
    title = RE_ICONS.sub("", h2_line).strip()
    title = RE_DUR.sub("", title).strip()
    title = RE_LEAD.sub("", title).strip()
    title = re.sub(r"^[-:\—–]\s*", "", title).strip()

    # Walk lines for visual / persona / narration blockquote
    visual = None
    persona = None
    tone = None
    quote_lines: list[str] = []
    in_quote = False

    for ln in body.split("\n"):
        stripped = ln.strip()

        # Visual line (sai da area de blockquote mesmo se ativa)
        if not in_quote:
            vmatch = RE_VISUAL.match(ln)
            if vmatch:
                visual = vmatch.group(1).strip()
                continue

        # Narration persona header
        if not in_quote:
            phead = RE_NARR_HEADER.match(ln)
            if phead:
                persona = (phead.group("persona") or "Narrador").strip()
                tone = (phead.group("tone") or "").strip() or None
                in_quote = True
                continue

        if in_quote:
            if stripped.startswith(">"):
                t = re.sub(r"^\s*>\s?", "", stripped).strip()
                if t:
                    quote_lines.append(t)
            elif not stripped:
                # blank line -> fim do blockquote
                in_quote = False
            else:
                # linha solta -> provavelmente fim mas algumas vezes continua
                in_quote = False

    narration = " ".join(quote_lines).strip()
    # Limpa aspas externas duplas/triplas/curvas
    narration = re.sub(r'^[\s"\'“”«»]+', "", narration)
    narration = re.sub(r'[\s"\'“”«»]+$', "", narration)

    return {
        "n": scene_n,
        "title": title,
        "dur": dur_s,
        "persona": persona,
        "tone": tone,
        "visual": visual,
        "narration": narration,
    }


def parse_roteiro(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    meta: dict = {}
    body = raw

    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            _, fm_yaml, body_after = parts
            try:
                meta = yaml.safe_load(fm_yaml) or {}
            except Exception:
                meta = {}
            body = body_after.lstrip()

    # Lesson title: 1) frontmatter.title; 2) H1; 3) "Meta:" line
    lesson_title = meta.get("title")
    if not lesson_title:
        m1 = re.search(r"^#\s+(.+?)$", body, re.M)
        if m1:
            lesson_title = m1.group(1).strip()
        else:
            m2 = re.search(r"Meta\s*:\s*(.+)", body, re.I)
            if m2:
                lesson_title = m2.group(1).strip().split("·")[0].strip()

    # Trilha pode estar em 3 lugares
    trilha = meta.get("trilha")
    if not trilha:
        mt = re.search(r"Trilha\s*\*?\*?:\s*\*?\*?\s*([A-Za-z]+)", body)
        if mt:
            trilha = mt.group(1).strip()

    if not trilha:
        # fallback a partir do lesson code
        lc = (meta.get("lesson") or "").lower()
        if lc.startswith("fund"):
            trilha = "Fundamental"
        elif lc.startswith("agent"):
            trilha = "Agent"
        elif lc.startswith("mstr") or lc.startswith("master"):
            trilha = "Master"
        elif lc.startswith("elite"):
            trilha = "Elite"
        else:
            trilha = "Fundamental"

    blocks = _split_scenes(body)
    scenes: list[dict] = []
    for k, (h2, rest) in enumerate(blocks, start=1):
        s = _parse_scene_block(h2, rest, fallback_n=k)
        # Garantir que só cenas reais sejam mantidas
        if s["title"] or s["narration"] or s["visual"]:
            # Substituir persona herdada do roteiro pela nossa canônica
            pn = s["persona"]
            if pn is None:
                s["persona"] = "Narrador"
            else:
                pn_lower = pn.lower().strip()
                if pn_lower in ("alencar",):
                    s["persona"] = "Alencar"
                elif pn_lower in ("ive",):
                    s["persona"] = "Ive"
                elif pn_lower in ("alencar + ive", "alencar+ive", "dupla"):
                    # Cena-a-cena dentro de "dupla": heurística pelo n
                    s["persona"] = "Ive" if (s["n"] % 2 == 1) else "Alencar"
                else:
                    s["persona"] = "Narrador"
            s["trilha"] = trilha
            scenes.append(s)

    return {
        "meta": meta,
        "lesson_title": lesson_title or path.stem,
        "trilha": trilha,
        "scenes": scenes,
    }


# ─── CLI ─────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else str(
        ROOT / "videos/aulas-onda-49/roteiros/aula-15-metricas-roi-ecossistema.md"
    )
    parsed = parse_roteiro(Path(src))
    print(json.dumps(parsed, ensure_ascii=False, indent=2))

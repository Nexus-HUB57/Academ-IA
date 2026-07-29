#!/usr/bin/env python3
"""
Academ'IA · Conversor MD -> HTML + PDF em lote
"""
from pathlib import Path
import re
import sys

import markdown as md_lib
import yaml
from weasyprint import HTML

ROOT = Path(".").resolve()
APOSTILAS_MD = ROOT / "apostilas"
HTML_DIR = ROOT / "apostilas" / "html"
PDF_DIR = ROOT / "apostilas" / "apostilas_pdf"
COVERS_DIR = ROOT / "docs" / "ebooks"
CSS_FILE = ROOT / "html" / "acad-style.css"


TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__TITLE__ - AcademIA Nexus</title>
  <link rel="stylesheet" href="../html/acad-style.css">
</head>
<body class="dark-theme">
  <article class="ebook">
    <header class="cover">
      <div class="series-tag">AcademIA - Apostila __CODE__</div>
      <h1>__TITLE__</h1>
      <h2>__SUBTITLE__</h2>
      <img class="cover-image" src="__COVER__" alt="Capa - __TITLE__">
      <div class="author"><strong>__AUTHOR__</strong><br>__AUTHOR_ROLE__</div>
      <div class="meta">__META__</div>
    </header>
    <section class="page toc-page">
      <h2>Sumario</h2>
      __TOC__
      <div class="info-box success">
        <strong>Sobre esta apostila:</strong> parte da colecao AcademIA - Nexus HUB57. Conteudo hands-on, baseado em producao real.
      </div>
    </section>
    <section class="page">
      <h2>Conteudo</h2>
      __BODY__
      <hr/>
      <p style="text-align:center;color:var(--fg-muted);margin-top:2rem;">
        <em>Fim da Apostila __CODE__ __DATE_YEAR__ - Licenca CC BY-NC-SA 4.0 - MMN_IA Collective - Nexus HUB57</em>
      </p>
    </section>
  </article>
</body>
</html>
"""


def parse_frontmatter(text):
    if text.startswith("---"):
        try:
            _, fm, body = text.split("---", 2)
            data = yaml.safe_load(fm)
            return data or {}, body.lstrip("\n")
        except Exception as e:
            print(f"  YAML warn: {e}", file=sys.stderr)
            return {}, text
    return {}, text


def derive_code(stem):
    m = re.match(r"^(\d{1,2})(?:-|$)", stem)
    if m:
        return "#" + m.group(1).zfill(2)
    return "#S"


def find_cover(stem):
    candidates = list(COVERS_DIR.glob("ACAD-apostila-" + stem + ".webp"))
    if candidates:
        return str(candidates[0].relative_to(ROOT).as_posix())
    # SVG placeholder inline
    svg = (
        "data:image/svg+xml;utf8,"
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 1200'>"
        "<defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>"
        "<stop offset='0' stop-color='%237c3aed'/>"
        "<stop offset='1' stop-color='%2306b6d4'/></linearGradient></defs>"
        "<rect width='800' height='1200' fill='url(%23g)'/>"
        "<text x='400' y='600' text-anchor='middle' fill='white' "
        "font-family='sans-serif' font-size='52'>AcademIA</text>"
        "</svg>"
    )
    return svg


def md_to_html(md_text):
    return md_lib.markdown(
        md_text,
        extensions=["extra", "fenced_code", "tables", "attr_list", "md_in_html",
                    "sane_lists", "codehilite"],
    )


def extract_first_heading(body_md):
    for line in body_md.splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
    return None


def main():
    if not CSS_FILE.exists():
        print("ERRO: CSS nao encontrada: " + str(CSS_FILE), file=sys.stderr)
        sys.exit(1)
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    mds = sorted([p for p in APOSTILAS_MD.glob("*.md") if p.stem != "README"])
    existing_html = {p.stem for p in HTML_DIR.glob("*.html")}
    existing_pdf = {p.stem for p in PDF_DIR.glob("*.pdf")}

    targets = [m for m in mds if m.stem not in existing_html or m.stem not in existing_pdf]
    print("Total MDs: " + str(len(mds)))
    print("Ja com HTML: " + str(len(existing_html)))
    print("Ja com PDF : " + str(len(existing_pdf)))
    print("A converter : " + str(len(targets)))
    print("=" * 70)

    ok_html, ok_pdf = [], []
    falhas = []

    for md_path in targets:
        stem = md_path.stem
        try:
            text = md_path.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)

            # Title precedence: fm.title -> h1 -> stem
            title = fm.get("title") or extract_first_heading(body) or stem
            subtitle = fm.get("subtitle") or fm.get("description") or "Apostila AcademIA - Nexus HUB57"
            author = fm.get("author") or "MMN_IA Collective"
            author_role = fm.get("author_role") or "PHD nivel Harvard do Universo AI"
            date_year = str(fm.get("date") or fm.get("year") or 2026)[:4]
            code = derive_code(stem)
            cover = find_cover(stem)

            # Strip leading H1 (avoid duplicate with cover)
            body_clean = body
            if fm.get("title"):
                body_clean = re.sub(r"^\s*#\s+.+?\n+", "", body_clean, count=1)

            # Remove capa-markdown se existir no topo
            # ![Capa ...](../../assets/...)
            body_clean = re.sub(r"^\s*!\[[^\]]*\]\([^)]+\)\s*\n+", "", body_clean)
            # Remove bold-titulo-md em algumas apostilas (linha **Nome** logo apos capa)
            # so se a primeira linha apos capa for um bold isolado; manteremos por enquanto

            html_body = md_to_html(body_clean)
            # Remove caption-like alt text redundante
            html_body = re.sub(r"<img[^>]*>", "", html_body, count=1) if html_body.lstrip().startswith("<img") else html_body

            # TOC via extensao toc
            toc_md = md_lib.markdown(body_clean[:8000], extensions=["extra", "toc"])
            toc_m = re.search(r'<div class="toc">.*?</div>', toc_md, re.DOTALL)
            toc = toc_m.group(0) if toc_m else "<ul><li>(conteudo detalhado no corpo)</li></ul>"

            meta = ("Apostila " + code.replace("#", "") + " - Nivel "
                    + str(fm.get("nivel", "Master")) + " - v"
                    + str(fm.get("version", "1.0")) + " - " + date_year)

            rendered = (TEMPLATE
                .replace("__TITLE__", title)
                .replace("__SUBTITLE__", subtitle)
                .replace("__AUTHOR__", author)
                .replace("__AUTHOR_ROLE__", author_role)
                .replace("__CODE__", code)
                .replace("__COVER__", cover)
                .replace("__META__", meta)
                .replace("__TOC__", toc)
                .replace("__BODY__", html_body)
                .replace("__DATE_YEAR__", date_year))

            html_path = HTML_DIR / (stem + ".html")
            html_path.write_text(rendered, encoding="utf-8")
            ok_html.append(stem)

            pdf_path = PDF_DIR / (stem + ".pdf")
            HTML(string=rendered, base_url=str(ROOT)).write_pdf(target=str(pdf_path))
            ok_pdf.append(stem)

        except Exception as e:
            falhas.append((stem, str(e)))

    print()
    print("=" * 70)
    print("HTML OK : " + str(len(ok_html)) + "/" + str(len(targets)))
    print("PDF  OK : " + str(len(ok_pdf)) + "/" + str(len(targets)))
    if falhas:
        print("Falhas  : " + str(len(falhas)))
        for s, e in falhas:
            print("  - " + s + ": " + e[:120])

    print()
    print("=== INVENTARIO ATUAL ===")
    html_n = len(list(HTML_DIR.glob("*.html")))
    pdf_n = len(list(PDF_DIR.glob("*.pdf")))
    print("HTML total: " + str(html_n))
    print("PDF  total: " + str(pdf_n))


if __name__ == "__main__":
    main()

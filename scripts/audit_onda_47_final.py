#!/usr/bin/env python3
"""
Auditoria final da Onda 47 - AcademIA Nexus Affil'IA'te
Valida consistencia entre .md, .html, .pdf e .webp
para apostilas e webinars.
"""

from pathlib import Path
import json
import sys
import re
from collections import defaultdict

ROOT = Path('/workspace/Academ-IA').resolve()
APOSTILAS = ROOT / 'apostilas'
WEBINARS = ROOT / 'webinars'
HTML_APOSTILAS = ROOT / 'html' / 'apostilas'
HTML_WEBINARS = ROOT / 'html' / 'webinars'
PDFS = ROOT / 'pdfs'
CAPAS = ROOT / 'docs' / 'ebooks'

# Convencoes de PDF: alguns usam 'apostila-NN-slug.pdf' (contribuidor)
# outros usam 'NN-slug.pdf' (Mavis)
PDF_PREFIX_VARIANTS = ['apostila-', '']


def audit_collection(md_dir, html_dir, collection_type='apostila'):
    """Audita uma colecao (apostila ou webinar)."""
    pattern = r'^\d+-' if collection_type == 'apostila' else r'^WB-2026-\d+'
    
    items = []
    for md_file in sorted(md_dir.glob('*.md')):
        if '-roteiro' in md_file.stem:
            continue  # roteiros sao separados
        if not re.match(pattern, md_file.name):
            continue
        
        slug = md_file.stem
        # Extrair numero
        m = re.match(r'^(\d+)-' if collection_type == 'apostila' else r'^WB-2026-(\d+)-', md_file.name)
        num = int(m.group(1)) if m else 0
        
        # Conferir HTML
        html_path = html_dir / f"{slug}.html"
        has_html = html_path.exists()
        html_size = html_path.stat().st_size if has_html else 0
        
        # Conferir PDF (qualquer variante)
        pdf_path = None
        # Webinar tem padrao 'webinar-WB-2026-NN-slug.pdf' (sem prefixo)
        for prefix in PDF_PREFIX_VARIANTS:
            candidate = PDFS / f"{prefix}{slug}.pdf"
            if candidate.exists():
                pdf_path = candidate
                break
        # Webinar: tambem 'webinar-{slug}.pdf' (slug ja tem WB-2026-NN)
        if not pdf_path and collection_type == 'webinar':
            candidate = PDFS / f"webinar-{slug}.pdf"
            if candidate.exists():
                pdf_path = candidate
        # Apostila: 'apostila-NN-slug.pdf' (sem prefixo NN)
        if not pdf_path and collection_type == 'apostila':
            # tentar sem o NN
            stem_no_num = re.sub(r'^\d+-', '', slug)
            for prefix in PDF_PREFIX_VARIANTS:
                candidate = PDFS / f"{prefix}{stem_no_num}.pdf"
                if candidate.exists():
                    pdf_path = candidate
                    break
        has_pdf = pdf_path is not None
        pdf_size = pdf_path.stat().st_size if has_pdf else 0
        
        # Conferir capa
        if collection_type == 'apostila':
            cap_name = f"ACAD-apostila-{slug}.webp"
        else:
            cap_name = f"{slug}.webp"
        cap_path = CAPAS / cap_name
        has_cap = cap_path.exists()
        cap_size = cap_path.stat().st_size if has_cap else 0
        
        # Extrair titulo do frontmatter
        title = ''
        subtitle = ''
        author = ''
        try:
            txt = md_file.read_text(encoding='utf-8', errors='ignore')
            in_fm = False
            for line in txt.splitlines()[:30]:
                if line.strip() == '---':
                    if in_fm:
                        break
                    in_fm = True
                    continue
                if in_fm:
                    if line.startswith('title:'):
                        title = line.split(':', 1)[1].strip().strip('"').strip("'")
                    elif line.startswith('subtitle:'):
                        subtitle = line.split(':', 1)[1].strip().strip('"').strip("'")
                    elif line.startswith('author:'):
                        author = line.split(':', 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
        
        items.append({
            'num': num,
            'slug': slug,
            'title': title,
            'subtitle': subtitle[:80] if subtitle else '',
            'author': author,
            'md_size': md_file.stat().st_size,
            'has_html': has_html,
            'html_size': html_size,
            'has_pdf': has_pdf,
            'pdf_size': pdf_size,
            'has_cap': has_cap,
            'cap_size': cap_size,
            'complete': has_html and has_pdf and has_cap,
        })
    
    return items


def print_report(apostilas, webinars):
    print("=" * 80)
    print("AUDITORIA FINAL - ONDA 47 - AcademIA Nexus Affil'IA'te")
    print("=" * 80)
    print()
    
    # Apostilas
    print(f"📚 APOSTILAS: {len(apostilas)}")
    complete_a = sum(1 for a in apostilas if a['complete'])
    print(f"   Completas (MD+HTML+PDF+Capa): {complete_a}/{len(apostilas)}")
    if complete_a < len(apostilas):
        print("   Faltando:")
        for a in apostilas:
            if not a['complete']:
                missing = []
                if not a['has_html']: missing.append('HTML')
                if not a['has_pdf']: missing.append('PDF')
                if not a['has_cap']: missing.append('Capa')
                print(f"     ❌ Apostila {a['num']:02d} ({a['slug']}): falta {', '.join(missing)}")
    print()
    
    # Webinars
    print(f"🎥 WEBINARS: {len(webinars)}")
    complete_w = sum(1 for w in webinars if w['complete'])
    print(f"   Completos (MD+HTML+PDF+Capa): {complete_w}/{len(webinars)}")
    if complete_w < len(webinars):
        print("   Faltando:")
        for w in webinars:
            if not w['complete']:
                missing = []
                if not w['has_html']: missing.append('HTML')
                if not w['has_pdf']: missing.append('PDF')
                if not w['has_cap']: missing.append('Capa')
                print(f"     ❌ WB-{w['num']:02d} ({w['slug']}): falta {', '.join(missing)}")
    print()
    
    # Tamanhos
    total_md_a = sum(a['md_size'] for a in apostilas) / 1024
    total_html_a = sum(a['html_size'] for a in apostilas) / 1024
    total_pdf_a = sum(a['pdf_size'] for a in apostilas) / 1024
    total_cap_a = sum(a['cap_size'] for a in apostilas) / 1024
    
    total_md_w = sum(w['md_size'] for w in webinars) / 1024
    total_html_w = sum(w['html_size'] for w in webinars) / 1024
    total_pdf_w = sum(w['pdf_size'] for w in webinars) / 1024
    total_cap_w = sum(w['cap_size'] for w in webinars) / 1024
    
    print("📊 TAMANHOS TOTAIS")
    print(f"   Apostilas:")
    print(f"     .md:   {total_md_a:>8.1f} KB")
    print(f"     .html: {total_html_a:>8.1f} KB")
    print(f"     .pdf:  {total_pdf_a:>8.1f} KB")
    print(f"     capa:  {total_cap_a:>8.1f} KB ({total_cap_a/1024:.2f} MB)")
    print()
    print(f"   Webinars:")
    print(f"     .md:   {total_md_w:>8.1f} KB")
    print(f"     .html: {total_html_w:>8.1f} KB")
    print(f"     .pdf:  {total_pdf_w:>8.1f} KB")
    print(f"     capa:  {total_cap_w:>8.1f} KB ({total_cap_w/1024:.2f} MB)")
    print()
    
    # Personas (autoria)
    by_author = defaultdict(int)
    for a in apostilas + webinars:
        if a['author']:
            by_author[a['author'][:40]] += 1
        else:
            by_author['(sem autor declarado)'] += 1
    
    print("👥 AUTORIA (declarada no frontmatter):")
    for author, count in sorted(by_author.items(), key=lambda x: -x[1]):
        print(f"   {author:<45} {count}")
    print()
    
    # Resumo final
    total = len(apostilas) + len(webinars)
    complete = complete_a + complete_w
    print("=" * 80)
    print(f"✅ RESUMO: {complete}/{total} materiais 100% completos")
    if complete == total:
        print("🎉 TODOS OS MATERIAIS ESTÃO COMPLETOS (MD + HTML + PDF + Capa)")
    print("=" * 80)


def main():
    apostilas = audit_collection(APOSTILAS, HTML_APOSTILAS, 'apostila')
    webinars = audit_collection(WEBINARS, HTML_WEBINARS, 'webinar')
    print_report(apostilas, webinars)
    
    # Salvar JSON
    out = {
        'apostilas': apostilas,
        'webinars': webinars,
    }
    report_path = ROOT / 'reports' / 'audit_onda_47_final.json'
    report_path.parent.mkdir(exist_ok=True)
    report_path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n💾 Relatorio salvo em: reports/audit_onda_47_final.json")


if __name__ == '__main__':
    main()

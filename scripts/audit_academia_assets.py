from pathlib import Path
import re
import json
from collections import defaultdict

ROOT = Path('/home/user/repo/Academ-IA').resolve()
TEXT_EXTS = {'.md', '.html', '.txt', '.json'}
REF_RE = re.compile(r'([^\s\]\)"\']+\.(?:png|jpg|jpeg|webp|gif|svg|mp3|wav|m4a|mp4|pdf|html))', re.I)


def norm_ref(ref: str) -> str:
    ref = ref.strip()
    ref = ref.strip('`')
    ref = ref.lstrip('./')
    return ref


def candidate_paths(doc: Path, ref: str):
    ref = norm_ref(ref)
    cands = []
    p = Path(ref)
    if p.is_absolute():
        cands.append(ROOT / str(p).lstrip('/'))
    else:
        cands.append((doc.parent / p).resolve())
        cands.append((ROOT / p).resolve())
        name = p.name
        if name:
            for hit in ROOT.rglob(name):
                cands.append(hit.resolve())
    uniq = []
    seen = set()
    for c in cands:
        s = str(c)
        if s not in seen:
            uniq.append(c)
            seen.add(s)
    return uniq


def main():
    docs = [p for p in ROOT.rglob('*') if p.is_file() and p.suffix.lower() in TEXT_EXTS and '.git/' not in str(p)]
    missing = []
    found_counts = defaultdict(int)
    total_refs = 0
    for doc in docs:
        try:
            text = doc.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        refs = sorted(set(m.group(1) for m in REF_RE.finditer(text)))
        for ref in refs:
            total_refs += 1
            cands = candidate_paths(doc, ref)
            hit = None
            for c in cands:
                if c.exists():
                    hit = c
                    found_counts[c.suffix.lower()] += 1
                    break
            if not hit:
                missing.append({
                    'document': str(doc.relative_to(ROOT)),
                    'reference': ref,
                    'candidates_checked': [str(c.relative_to(ROOT)) if str(c).startswith(str(ROOT)) else str(c) for c in cands[:12]]
                })

    # additional canonical inventory checks
    inventory = {
        'thumbnails_masters_png': sorted(p.name for p in (ROOT/'producao/assets/thumbnails').glob('capa-*.png')),
        'youtube_png': sorted(p.name for p in (ROOT/'youtube/thumbnails').glob('*.png')),
        'youtube_jpg': sorted(p.name for p in (ROOT/'youtube/thumbnails_yt').glob('*.jpg')),
        'video_audio_files': sorted(p.name for p in (ROOT/'videos/audio').glob('*')),
        'pdf_files_pdf': sorted(p.name for p in (ROOT/'pdf').glob('*.pdf')) if (ROOT/'pdf').exists() else [],
        'pdf_files_pdfs': sorted(p.name for p in (ROOT/'pdfs').glob('*.pdf')) if (ROOT/'pdfs').exists() else [],
    }

    out = {
        'root': str(ROOT),
        'documents_scanned': len(docs),
        'total_refs_scanned': total_refs,
        'missing_count': len(missing),
        'found_counts_by_ext': dict(found_counts),
        'missing': missing,
        'inventory': inventory,
    }
    out_path = ROOT / 'docs' / 'AUDITORIA_CIRURGICA_ASSETS_2026-07-24.json'
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out_path)
    print(f'missing_count={len(missing)}')


if __name__ == '__main__':
    main()

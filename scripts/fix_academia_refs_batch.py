from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path('/home/user/repo/Academ-IA').resolve()
DOCS_EBOOKS = ROOT / 'docs' / 'ebooks'


def cover_from_source(src: Path, dst: Path, size=(600, 800), fmt='WEBP'):
    img = Image.open(src).convert('RGB')
    fitted = ImageOps.fit(img, size, method=Image.LANCZOS, centering=(0.5, 0.5))
    dst.parent.mkdir(parents=True, exist_ok=True)
    if fmt.upper() == 'WEBP':
        fitted.save(dst, format='WEBP', quality=95, method=6)
    else:
        fitted.save(dst, format=fmt.upper(), optimize=True)
    print('generated', dst.relative_to(ROOT))


def replace_text(path: Path, replacements):
    text = path.read_text(encoding='utf-8')
    orig = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != orig:
        path.write_text(text, encoding='utf-8')
        print('updated', path.relative_to(ROOT))


def main():
    # Create missing ebook covers/assets from approved standardized covers
    cover_from_source(
        ROOT / 'producao/assets/thumbnails/capa-32-pricing-ia-2026-dupla.png',
        DOCS_EBOOKS / 'ACAD-apostila-32-pricing-ia-2026.webp',
        size=(600, 800),
        fmt='WEBP',
    )
    cover_from_source(
        ROOT / 'producao/assets/thumbnails/capa-aula-01-o-que-e-agente-ia-ive.png',
        DOCS_EBOOKS / 'curso-universo-ia--ebook-01-fundamentos-ia-ml.webp',
        size=(600, 800),
        fmt='WEBP',
    )

    # Fix apostilas references: wrong ../../ paths -> correct ../docs/ebooks
    apostilas_dir = ROOT / 'apostilas'
    for p in sorted(apostilas_dir.glob('*.md')):
        replacements = [
            ('../../assets/ebook_covers/', '../docs/ebooks/'),
            ('../../docs/ebooks/', '../docs/ebooks/'),
        ]
        replace_text(p, replacements)

    # Fix course slide references
    replace_text(
        ROOT / 'cursos/fundamental/00-boas-vindas-slides.md',
        [('/home/ubuntu/MMN_AI-to-AI/AcademIA/cursos/fundamental/diagrama_ecossistema_nexus.png', 'diagrama_ecossistema_nexus.png')],
    )
    replace_text(
        ROOT / 'cursos/fundamental/01-entendendo-ioaid-slides.md',
        [('../../assets/ebook_covers/ACAD-apostila-01-apresentacao-infraestrutura.webp', '../../docs/ebooks/ACAD-apostila-01-apresentacao-infraestrutura.webp')],
    )
    replace_text(
        ROOT / 'cursos/fundamental/03-painel-afiliado-slides.md',
        [('../../assets/ebook_covers/ACAD-apostila-05-sete-telas-essenciais.webp', '../../docs/ebooks/ACAD-apostila-05-sete-telas-essenciais.webp')],
    )

    # Fix onda-47 roteiro media paths to explicit sibling dirs/docs
    for p in sorted((ROOT / 'videos/aulas-onda-47/roteiros').glob('aula-*.md')):
        text = p.read_text(encoding='utf-8')
        for i in range(1, 17):
            n = f'{i:02d}'
            text = text.replace(f'`thumb-aula-{n}-', f'`../thumbs/thumb-aula-{n}-')
            text = text.replace(f'`aula-{n}-', f'`../audios/aula-{n}-')
        text = text.replace('`curso-universo-ia--ebook-01-fundamentos-ia-ml.webp`', '`../../../docs/ebooks/curso-universo-ia--ebook-01-fundamentos-ia-ml.webp`')
        p.write_text(text, encoding='utf-8')
        print('updated', p.relative_to(ROOT))

    # Fix selected videos/roteiros checklist refs to explicit thumbnail sibling path
    selected = {
        'videos/roteiros/00-boas-vindas-academia-roteiro.md': [('`thumb-00-boas-vindas.png`', '`../thumbnails/thumb-00-boas-vindas.png`')],
        'videos/roteiros/02-sho-sistema-imune-roteiro.md': [('`thumb-02-sho.png`', '`../thumbnails/thumb-02-sho.png`')],
        'videos/roteiros/04-primeiro-agente-roteiro.md': [('`thumb-04-primeiro-agente.png`', '`../thumbnails/thumb-04-primeiro-agente.png`')],
        'videos/roteiros/15-orquestracao-ecossistemas-roteiro.md': [('`thumb-15-orquestracao-ecossistemas.webp`', '`../thumbnails/thumb-15-orquestracao-ecossistemas.webp`')],
        'videos/roteiros/16-senciencia-barreiras-roteiro.md': [('`thumb-16-senciencia-barreiras.webp`', '`../thumbnails/thumb-16-senciencia-barreiras.webp`')],
        'videos/roteiros/17-poder-perigo-autonomia-roteiro.md': [('`thumb-17-poder-perigo-autonomia.webp`', '`../thumbnails/thumb-17-poder-perigo-autonomia.webp`')],
        'videos/roteiros/18-fundamento-saas-ia-roteiro.md': [('`thumb-18-fundamento-saas-ia.webp`', '`../thumbnails/thumb-18-fundamento-saas-ia.webp`')],
        'videos/roteiros/19-poder-processamento-ia-roteiro.md': [('`thumb-19-poder-processamento-ia.webp`', '`../thumbnails/thumb-19-poder-processamento-ia.webp`')],
    }
    for rel, reps in selected.items():
        replace_text(ROOT / rel, reps)


if __name__ == '__main__':
    main()

#!/bin/bash
# Script de migração de personas para marca/personas
# Estratégia: NÃO sobrescrever arquivos de tamanho igual ou maior
# (preserva qualidade dos arquivos de marca que podem ter sido processados)

set -e

SRC_ROOT="personas"
DST_ROOT="marca/personas"
PRODUCAO="producao/personas"

echo "🔄 Migração de personas → $DST_ROOT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

moved=0
skipped=0
overwritten=0

# Função para mover com proteção
safe_move() {
    local src="$1"
    local dst="$2"

    if [ ! -f "$src" ]; then
        echo "  ⚠️  SOURCE NÃO EXISTE: $src"
        return
    fi

    # Criar diretório de destino se necessário
    mkdir -p "$(dirname "$dst")"

    if [ -f "$dst" ]; then
        local src_size=$(stat -c%s "$src")
        local dst_size=$(stat -c%s "$dst")

        if [ "$src_size" -eq "$dst_size" ]; then
            echo "  ⏭  SKIP (igual): $(basename "$src")"
            skipped=$((skipped+1))
            return
        elif [ "$src_size" -gt "$dst_size" ]; then
            echo "  ⬆️  OVERWRITE (source > dest): $src → $dst"
            cp "$src" "$dst"
            overwritten=$((overwritten+1))
            return
        else
            echo "  ⏭  SKIP (dest > source): $(basename "$src")"
            skipped=$((skipped+1))
            return
        fi
    fi

    echo "  ➕ NOVO: $src → $dst"
    cp "$src" "$dst"
    moved=$((moved+1))
}

# 1. Mover de personas/ → marca/personas/
echo ""
echo "📂 Etapa 1: personas/ → marca/personas/"
echo "---"

for src in $(find "$SRC_ROOT" -type f | sort); do
    rel="${src#$SRC_ROOT/}"
    dst="$DST_ROOT/$rel"
    safe_move "$src" "$dst"
done

# 2. Mover de producao/personas/ → marca/personas/
echo ""
echo "📂 Etapa 2: producao/personas/ → marca/personas/"
echo "---"

if [ -f "$PRODUCAO/sra_nexus_ive.md" ]; then
    safe_move "$PRODUCAO/sra_nexus_ive.md" "$DST_ROOT/ive/sra_nexus_ive.md"
fi

if [ -f "$PRODUCAO/sir_nexus_alencar.md" ]; then
    safe_move "$PRODUCAO/sir_nexus_alencar.md" "$DST_ROOT/alencar/sir_nexus_alencar.md"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Resumo:"
echo "  ➕ Novos:    $moved"
echo "  ⬆️  Overwrite: $overwritten"
echo "  ⏭  Skip:    $skipped"
echo ""
echo "✅ Migração concluída (sem perda de dados)"
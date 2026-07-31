#!/usr/bin/env bash
# scripts/git_maintenance.sh
# ============================================================
# Script de manutenção preventiva do repositório Academ-IA
# ============================================================
#
# OBJETIVO:
#   - Manter o .git enxuto (gc, prune)
#   - Identificar duplicações por hash MD5
#   - Detectar paths legados/duplicados
#   - Reportar tamanho por tipo/extensão
#   - Verificar saúde do packfile
#
# USO:
#   bash scripts/git_maintenance.sh
#   bash scripts/git_maintenance.sh --report-only   # só relatório
#   bash scripts/git_maintenance.sh --apply-gc      # aplica gc (não destrutivo)
#
# COMPLIANCE:
#   - Não modifica working tree
#   - Não sobrescreve arquivos
#   - Apenas leitura + gc (manutenção interna do git)
#   - Idempotente: pode rodar múltiplas vezes
#
# CRIAÇÃO: 2026-07-26 (Mavis Agent, pós BOTTLENECK-AUDIT-2026-07-26)
# ============================================================

set -uo pipefail  # sem -e para não abortar em erros de subshells (xargs, md5sum)

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

REPORT_ONLY=false
APPLY_GC=false
for arg in "$@"; do
  case "$arg" in
    --report-only) REPORT_ONLY=true ;;
    --apply-gc)    APPLY_GC=true ;;
    *) echo "[ERRO] Argumento desconhecido: $arg" >&2; exit 1 ;;
  esac
done

echo "============================================================"
echo "🔧 Git Maintenance · Academ-IA"
echo "============================================================"
echo "Repo: $REPO_ROOT"
echo "Modo: $([ "$REPORT_ONLY" = true ] && echo 'report-only' || echo 'apply')"
echo ""

# --- 1. Saúde do packfile ---
echo "📦 [1/6] Packfile health"
git count-objects -v
echo ""

# --- 2. Tamanho por tipo/extensão ---
echo "📊 [2/6] Tamanho por extensão (working tree)"
printf "  %-12s  %8s  %10s\n" "extensão" "arquivos" "tamanho"
printf "  %-12s  %8s  %10s\n" "----------" "--------" "----------"
total_bin=0
total_count=0
for ext in mp4 wav mp3 pdf png jpg webp; do
  count=$(find . -type f -name "*.$ext" -not -path "./.git/*" 2>/dev/null | wc -l)
  if [ "$count" -gt 0 ]; then
    # find + du é mais rápido que stat em massa
    size=$(find . -type f -name "*.$ext" -not -path "./.git/*" -printf '%s\n' 2>/dev/null | awk '{ sum += $1 } END { print sum+0 }')
    size_mb=$((size / 1024 / 1024))
    total_bin=$((total_bin + size))
    total_count=$((total_count + count))
    printf "  %-10s  %8d  %7d MB\n" ".$ext" "$count" "$size_mb"
  fi
done
total_bin_mb=$((total_bin / 1024 / 1024))
echo "  ---------------------------------------------"
echo "  TOTAL BINÁRIO: ${total_bin_mb} MB em ${total_count} arquivos"
echo ""

# --- 3. Tamanho do .git/ ---
echo "📁 [3/6] Tamanho do .git/"
du -sh .git/ 2>&1 | head -1
echo ""

# --- 4. Duplicações por hash (top 5) ---
echo "🔍 [4/6] Top 5 clusters de duplicação por hash MD5"
if command -v md5sum >/dev/null 2>&1; then
  # Amostra reduzida (top 200 maiores) para evitar travamento
  TMP_HASHES=$(mktemp)
  find . -type f -not -path "./.git/*" -size +500k 2>/dev/null \
    | head -200 \
    | xargs md5sum 2>/dev/null \
    | sort \
    | awk '
        { hashes[$1] = (hashes[$1] ? hashes[$1] "|" $2 : $2) }
        END {
          for (h in hashes) {
            n = split(hashes[h], arr, "|");
            if (n > 1) print n, arr[1]
          }
        }' \
    | sort -rn \
    | head -5 > "$TMP_HASHES"
  if [ -s "$TMP_HASHES" ]; then
    while IFS= read -r line; do
      printf "  %s\n" "$line"
    done < "$TMP_HASHES"
  else
    echo "  Nenhuma duplicação detectada na amostra"
  fi
  rm -f "$TMP_HASHES"
  echo "  (amostra: 200 maiores arquivos >500k)"
else
  echo "  [SKIP] md5sum não disponível"
fi
echo ""

# --- 5. Paths potencialmente debug/suspeitos ---
echo "🗑️  [5/6] Paths suspeitos não-canônicos (referência)"
for pattern in "audit_hashes" "render/intermediate" ".cache" "scratch" "tmp_" ".working"; do
  count=$(find . -type d -name "*$pattern*" -not -path "./.git/*" 2>/dev/null | wc -l)
  if [ "$count" -gt 0 ]; then
    printf "  ⚠️  %d pasta(s) '%s' encontrada(s)\n" "$count" "$pattern"
  fi
done
echo ""

# --- 6. gc (opcional) ---
echo "🧹 [6/6] Git GC"
if [ "$REPORT_ONLY" = true ]; then
  echo "  [SKIP] --report-only (não aplica gc)"
else
  if [ "$APPLY_GC" = true ]; then
    echo "  Aplicando: git gc --aggressive --prune=now"
    git gc --aggressive --prune=now
    echo "  ✅ gc aplicado"
  else
    echo "  [DRY-RUN] Para aplicar: bash scripts/git_maintenance.sh --apply-gc"
  fi
fi
echo ""

# --- Resumo final ---
echo "============================================================"
echo "📋 Resumo"
echo "============================================================"
echo "Working tree: $(git status -s 2>&1 | wc -l) arquivos modificados"
echo "Tamanho do repo: $(du -sh . 2>&1 | cut -f1)"
echo "Tamanho do .git/: $(du -sh .git/ 2>&1 | cut -f1)"
echo ""
echo "✅ Manutenção concluída."
echo ""
echo "Para próximos passos, consulte:"
echo "  - reports/BOTTLENECK-AUDIT-2026-07-26.md"
echo "  - GUIA_MULTI_DEV.md"

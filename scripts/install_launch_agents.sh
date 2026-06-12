#!/bin/bash
# LaunchAgent 설치/동기화 SSOT — config/launch_agents/ → ~/Library/LaunchAgents
#
# 사용법:
#   scripts/install_launch_agents.sh            # 변경된 plist만 백업 후 교체·재로드
#   scripts/install_launch_agents.sh --dry-run  # 적용 없이 차이만 표시
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$PROJECT_ROOT/config/launch_agents"
DST_DIR="$HOME/Library/LaunchAgents"
BACKUP_DIR="$DST_DIR/_backup_$(date '+%Y%m%d')"
UID_NUM="$(id -u)"
DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

changed=0
for src in "$SRC_DIR"/*.plist; do
    base="$(basename "$src")"
    dst="$DST_DIR/$base"
    label="${base%.plist}"

    if [[ -f "$dst" ]] && diff -q "$src" "$dst" >/dev/null 2>&1; then
        continue
    fi

    changed=$((changed + 1))
    if [[ $DRY_RUN -eq 1 ]]; then
        echo "[dry-run] 갱신 필요: $base"
        continue
    fi

    if [[ -f "$dst" ]]; then
        mkdir -p "$BACKUP_DIR"
        cp "$dst" "$BACKUP_DIR/"
    fi

    launchctl bootout "gui/$UID_NUM/$label" 2>/dev/null || true
    cp "$src" "$dst"
    launchctl bootstrap "gui/$UID_NUM" "$dst"
    echo "갱신: $label"
done

if [[ $changed -eq 0 ]]; then
    echo "모든 LaunchAgent 최신 상태."
else
    echo "변경 $changed건 ($([[ $DRY_RUN -eq 1 ]] && echo 'dry-run' || echo '적용 완료'))"
fi

#!/usr/bin/env python3
"""
cleanup_auto_enrich_noise.py — KB 파일에서 auto-enrich 노이즈 섹션 제거

대상: 핵심 공종 파일에서 "auto-enrich via Naver+Tavily+Google+DDG+Ollama" 태그가
      붙은 반복 섹션을 제거한다. Claude Code 수동 편집 섹션은 보존.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import AGENT_KB_DIR  # noqa: E402

KB_DIR = AGENT_KB_DIR

# 핵심 공종 파일 (답변 품질에 직접 영향)
TARGET_FILES = [
    "건축.md",
    "구조.md",
    "공조덕트.md",
    "위생.md",
    "소방기계.md",
    "전기.md",
    "통신.md",
    "공조배관.md",
    "소방전기.md",
    "설비시공조율.md",
    "설비기초.md",
    "설비도면해석.md",
    "설비장비.md",
]

AUTO_ENRICH_MARKER = "auto-enrich via Naver+Tavily+Google+DDG+Ollama"


def remove_auto_enrich_sections(content: str) -> tuple[str, int]:
    """
    auto-enrich 섹션을 제거하고 (정리된 내용, 제거된 섹션 수) 반환.
    섹션은 "## ... (날짜)\n- Source: auto-enrich..." 패턴으로 시작해
    다음 ## 섹션 또는 파일 끝까지를 범위로 본다.
    """
    # 섹션 분리: ## 로 시작하는 헤더 기준
    # 각 섹션을 (header_line + body) 단위로 분리
    sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)

    kept = []
    removed_count = 0

    for section in sections:
        if AUTO_ENRICH_MARKER in section:
            removed_count += 1
        else:
            kept.append(section)

    # 연속된 빈 줄 정리 (3줄 이상 → 2줄)
    result = "".join(kept)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.rstrip() + "\n", removed_count


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("[DRY RUN] 실제 파일 수정 없이 결과만 출력합니다.\n")

    total_removed = 0
    files_changed = 0

    for filename in TARGET_FILES:
        kb_file = KB_DIR / filename
        if not kb_file.exists():
            print(f"  SKIP (파일 없음): {filename}")
            continue

        original = kb_file.read_text(encoding="utf-8")
        cleaned, removed = remove_auto_enrich_sections(original)

        if removed == 0:
            print(f"  OK (변경없음): {filename}")
            continue

        print(f"  제거: {filename} — {removed}개 섹션 삭제")
        total_removed += removed
        files_changed += 1

        if not dry_run:
            # 백업
            backup = kb_file.with_suffix(".md.bak")
            backup.write_text(original, encoding="utf-8")
            # 저장
            kb_file.write_text(cleaned, encoding="utf-8")

    print(f"\n총 {files_changed}개 파일, {total_removed}개 auto-enrich 섹션 {'(dry-run)' if dry_run else '제거 완료'}.")
    if not dry_run:
        print("백업 파일: *.md.bak (확인 후 삭제)")


if __name__ == "__main__":
    main()

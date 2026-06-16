#!/usr/bin/env python3
"""auto-enrich가 누적 append 한 중복 '최신 동향/기준 업데이트' 섹션을 정리한다.

배경: scripts/auto_enrich_knowledge_base.py 가 토픽당 매일 '## {title} (날짜)' 섹션을
append 하면서, 약한 3-gram dedup(마지막 2000자·임계 55%)을 LLM 표현 변주가 통과해
같은 제목 섹션이 에이전트당 10~20개씩 누적됐다(answer 오염·검색 비대). 생성기는
replace-in-place 로 수정됐고(앞으로 누적 차단), 이 스크립트는 이미 쌓인 과거 중복을
일회성 정리한다.

정밀 타깃: 'Source: auto-enrich via' 마커가 있는 섹션만 대상으로 하여, self-healing
웹수집('자동 답변 품질 보강 수집')이나 사람이 작성한 섹션은 절대 건드리지 않는다.
같은 제목(날짜 제외)의 auto-enrich 섹션이 여러 개면 파일 내 마지막(=최신) 1개만 남긴다.

사용:
  python scripts/dedupe_autoenrich_sections.py            # dry-run (변경 미적용)
  python scripts/dedupe_autoenrich_sections.py --apply     # 실제 적용
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = ROOT / "knowledge"

# auto-enrich 섹션 식별 마커(append_section 의 Source 라인)
AUTOENRICH_MARKER = "Source: auto-enrich via"
# '## {title} (YYYY-MM-DD...)' 헤딩에서 title 추출
HEAD_RE = re.compile(r"^## (?P<title>.+?) \(\d{4}-\d{2}-\d{2}")


def _split_sections(content: str) -> list[str]:
    """H2 경계로 분할(프리앰블 + 각 '## ' 섹션). 순서/내용 보존."""
    return re.split(r"(?m)^(?=## )", content)


def dedupe_file(path: Path) -> tuple[int, str]:
    """파일에서 동일 제목 auto-enrich 섹션을 최신 1개만 남긴다.
    반환: (제거한 섹션 수, 새 내용). 변경 없으면 (0, 원본)."""
    original = path.read_text(encoding="utf-8")
    parts = _split_sections(original)

    # 각 part가 auto-enrich 섹션인지 + title 추출
    titles: list[str | None] = []
    for p in parts:
        head = HEAD_RE.match(p)
        if head and AUTOENRICH_MARKER in p:
            titles.append(head.group("title"))
        else:
            titles.append(None)

    # 같은 title 중 마지막 인덱스만 유지
    last_index: dict[str, int] = {}
    for i, t in enumerate(titles):
        if t is not None:
            last_index[t] = i

    removed = 0
    kept_parts: list[str] = []
    for i, (p, t) in enumerate(zip(parts, titles)):
        if t is not None and last_index[t] != i:
            removed += 1
            continue  # 같은 제목의 더 최신 섹션이 뒤에 있으므로 제거
        kept_parts.append(p)

    if removed == 0:
        return 0, original
    new_content = "".join(kept_parts).rstrip() + "\n"
    return removed, new_content


def main() -> None:
    apply = "--apply" in sys.argv
    files = sorted(KNOWLEDGE.rglob("*.md"))
    total_removed = 0
    touched = 0
    for f in files:
        removed, new_content = dedupe_file(f)
        if removed:
            total_removed += removed
            touched += 1
            print(f"  {f.relative_to(ROOT)}: -{removed} 섹션")
            if apply:
                f.write_text(new_content, encoding="utf-8")
    mode = "적용" if apply else "DRY-RUN(미적용)"
    print(f"\n==== {mode}: {touched}파일 / {total_removed}개 중복 auto-enrich 섹션 ====")
    if not apply and total_removed:
        print("실제 적용: python scripts/dedupe_autoenrich_sections.py --apply")


if __name__ == "__main__":
    main()

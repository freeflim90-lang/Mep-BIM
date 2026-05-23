#!/usr/bin/env python3
"""Metadata-only intake scanner for external personal/work archives.

The scanner intentionally does not read file contents. It looks only at path,
file name, extension, size, and modified time, then creates an internal review
report for knowledge curation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
from collections import Counter, defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "docs" / "knowledge_intake" / "external_sources"

KNOWLEDGE_EXTENSIONS = {
    ".md", ".txt", ".log", ".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".csv",
    ".dyn", ".addin", ".json", ".xml", ".cs", ".py", ".html",
}

IGNORE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".heic", ".mp4", ".mov", ".avi", ".exe",
    ".msi", ".dmg", ".pkg", ".zip", ".rar", ".7z", ".iso", ".dll",
}

VALUE_KEYWORDS = {
    "bim": 5,
    "mep": 5,
    "revit": 5,
    "navisworks": 5,
    "dynamo": 5,
    "addin": 5,
    "add-in": 5,
    "family": 4,
    "template": 4,
    "manual": 4,
    "quality": 4,
    "clash": 4,
    "rfi": 3,
    "pjt": 3,
    "standard": 4,
    "report": 3,
    "checklist": 4,
    "산식": 4,
    "품질": 5,
    "간섭": 5,
    "검토": 3,
    "보고서": 4,
    "템플릿": 4,
    "매뉴얼": 4,
    "표준": 5,
    "제안": 3,
    "교육": 3,
    "회의록": 2,
    "패밀리": 4,
    "다이나모": 5,
    "애드인": 5,
    "물량": 4,
    "업무일지": 3,
    "이슈": 4,
    "인수인계": 3,
}

SENSITIVE_KEYWORDS = {
    "npki", "yessign", "certificate", "password", "passwd", "token", "secret",
    "계약", "비용", "연락처", "담당자", "개인정보", "주민", "사업자", "통장",
    "카드", "급여", "인사", "보안", "크랙", "crack", "filecr", "pas123",
}

ARCHIVE_OR_BINARY_KEYWORDS = {
    "설치파일", "installer", "program", "프로그램", "portable", "setup", "backup",
    "백업", "$recycle.bin", "system volume information",
}


def safe_rel(path: Path, roots: list[Path]) -> str:
    for root in roots:
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            continue
    return path.as_posix()


def score_path(path: Path) -> tuple[int, list[str], list[str]]:
    lower = path.as_posix().lower()
    score = 0
    reasons: list[str] = []
    blockers: list[str] = []

    ext = path.suffix.lower()
    if ext in KNOWLEDGE_EXTENSIONS:
        score += 2
        reasons.append(f"knowledge-ext:{ext or 'none'}")
    if ext in IGNORE_EXTENSIONS:
        score -= 5
        blockers.append(f"binary-or-media:{ext}")

    for keyword, weight in VALUE_KEYWORDS.items():
        if keyword.lower() in lower:
            score += weight
            reasons.append(keyword)

    for keyword in SENSITIVE_KEYWORDS:
        if keyword.lower() in lower:
            score -= 8
            blockers.append(f"sensitive:{keyword}")

    for keyword in ARCHIVE_OR_BINARY_KEYWORDS:
        if keyword.lower() in lower:
            score -= 3
            blockers.append(f"archive-or-installer:{keyword}")

    return score, sorted(set(reasons)), sorted(set(blockers))


def classify(score: int, blockers: list[str]) -> str:
    if any(item.startswith("sensitive:") for item in blockers):
        return "blocked_sensitive"
    if any(item.startswith("binary-or-media:") for item in blockers) and score < 4:
        return "skip_binary_media"
    if score >= 10:
        return "high_value_review"
    if score >= 6:
        return "medium_value_review"
    if score >= 3:
        return "low_value_review"
    return "archive_or_skip"


def iter_files(roots: list[Path], max_files: int) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            lowered = Path(dirpath).as_posix().lower()
            if "$recycle.bin" in lowered or "system volume information" in lowered:
                dirnames[:] = []
                continue
            for name in filenames:
                files.append(Path(dirpath) / name)
                if len(files) >= max_files:
                    return files
    return files


def render_report(roots: list[Path], rows: list[dict], max_examples: int) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today = dt.date.today().isoformat()
    by_class = Counter(row["class"] for row in rows)
    by_ext = Counter(row["ext"] or "(none)" for row in rows)
    by_top_folder: Counter[str] = Counter()
    grouped: dict[str, list[dict]] = defaultdict(list)

    for row in rows:
        parts = row["rel"].split("/")
        by_top_folder[parts[0] if parts else "(root)"] += 1
        grouped[row["class"]].append(row)

    lines = [
        "# LUA BIM LAB",
        "# 외장하드 지식 인테이크 후보 리포트",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        f"작성일: {today}",
        "문서상태: 내부 검토용",
        "배포등급: Confidential",
        "스캔 방식: 파일 내용 미열람, 경로/파일명/확장자/크기/수정일 기반",
        "",
        "## 1. 스캔 범위",
        "",
    ]
    for root in roots:
        lines.append(f"- `{root}`")

    lines.extend([
        "",
        "## 2. 요약",
        "",
        f"- 생성 시각: {now}",
        f"- 전체 스캔 파일 수: {len(rows)}",
        "- 주의: 본 리포트는 흡수 후보 선별용이며, 원본 자료를 복사하거나 내용을 추출하지 않았다.",
        "",
        "### 분류별 수량",
        "",
        "| 분류 | 수량 | 의미 |",
        "|---|---:|---|",
    ])
    labels = {
        "high_value_review": "우선 검토 후보",
        "medium_value_review": "검토 후보",
        "low_value_review": "낮은 우선순위 후보",
        "blocked_sensitive": "민감정보 가능성으로 차단",
        "skip_binary_media": "미디어/설치파일 중심 제외",
        "archive_or_skip": "아카이브 또는 제외",
    }
    for key, label in labels.items():
        lines.append(f"| {key} | {by_class.get(key, 0)} | {label} |")

    lines.extend([
        "",
        "### 주요 확장자",
        "",
        "| 확장자 | 수량 |",
        "|---|---:|",
    ])
    for ext, count in by_ext.most_common(20):
        lines.append(f"| `{ext}` | {count} |")

    lines.extend([
        "",
        "### 상위 폴더",
        "",
        "| 폴더 | 파일 수 |",
        "|---|---:|",
    ])
    for folder, count in by_top_folder.most_common(25):
        lines.append(f"| `{folder}` | {count} |")

    for key in ["high_value_review", "medium_value_review", "blocked_sensitive"]:
        lines.extend([
            "",
            f"## {labels[key]}",
            "",
            "| 점수 | 파일 | 사유 | 차단 신호 |",
            "|---:|---|---|---|",
        ])
        for row in sorted(grouped.get(key, []), key=lambda item: item["score"], reverse=True)[:max_examples]:
            reasons = ", ".join(row["reasons"][:8]) or "-"
            blockers = ", ".join(row["blockers"][:8]) or "-"
            lines.append(f"| {row['score']} | `{row['rel']}` | {reasons} | {blockers} |")

    lines.extend([
        "",
        "## 3. 흡수 권장 순서",
        "",
        "1. `high_value_review` 중 BIM 표준, MEP, Dynamo, Add-in, 품질 체크리스트 자료부터 검토한다.",
        "2. 고객명/프로젝트명이 포함된 자료는 원문 흡수 전 익명화 가능성을 먼저 판단한다.",
        "3. `blocked_sensitive`는 자동 흡수하지 않고 보안/법무 검토 후 제외 또는 익명화한다.",
        "4. 설치파일, 압축파일, 이미지 원본은 지식 DB가 아니라 별도 자산 인벤토리로 관리한다.",
        "5. 승인된 자료만 요약본을 `docs/knowledge_intake/curated` 또는 관련 표준문서로 승격한다.",
        "",
        "## 4. 관련 문서",
        "",
        "- `docs/internal_organization_documents/21_KNOWLEDGE_CURATION_INTELLIGENCE_CELL.md`",
        "- `docs/internal_organization_documents/20_PUBLIC_DISCLOSURE_DB_READINESS_CHECKLIST.md`",
        "- `docs/internal_organization_documents/15_KNOWLEDGE_DOCUMENT_REPOSITORY_POLICY.md`",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="+", help="External folders to scan")
    parser.add_argument("--max-files", type=int, default=30000)
    parser.add_argument("--max-examples", type=int, default=80)
    args = parser.parse_args()

    roots = [Path(root).expanduser() for root in args.roots]
    files = iter_files(roots, args.max_files)
    rows = []
    for path in files:
        try:
            stat = path.stat()
        except OSError:
            continue
        score, reasons, blockers = score_path(path)
        rows.append({
            "path": path.as_posix(),
            "rel": safe_rel(path, roots),
            "ext": path.suffix.lower(),
            "size": stat.st_size,
            "mtime": dt.datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
            "score": score,
            "reasons": reasons,
            "blockers": blockers,
            "class": classify(score, blockers),
        })

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / f"{dt.date.today().isoformat()}_EXTERNAL_DRIVE_KNOWLEDGE_INTAKE.md"
    out.write_text(render_report(roots, rows, args.max_examples), encoding="utf-8")
    print(out)
    print(f"files={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

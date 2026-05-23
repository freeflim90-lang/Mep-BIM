#!/usr/bin/env python3
"""Create a daily automated knowledge curation review.

The script classifies recently changed Markdown knowledge into practical review
buckets so the daily update is not only collected, but also triaged for growth.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "docs" / "knowledge_updates" / "curation"
DAILY_REPORT_DIR = PROJECT_ROOT / "docs" / "knowledge_updates" / "daily"

EXCLUDE_PARTS = {
    ".git",
    ".dev-venv",
    "__pycache__",
    "node_modules",
    "dist",
    ".obsidian",
}

SOURCE_ROOTS = [
    PROJECT_ROOT / "data" / "knowledge_base",
    PROJECT_ROOT / "data" / "team_requests",
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "obsidian_vaults" / "lua_bim_lab_global_map" / "NAS_Knowledge",
    PROJECT_ROOT / "obsidian_vaults" / "model_quality_auditor",
]

PURPOSE_RULES = [
    ("MEP BIM 실무 품질", ["mep", "bim", "공조", "덕트", "배관", "소방", "전기", "통신", "위생", "간섭", "품질", "납품", "검수"]),
    ("Model Quality Auditor / Add-in 상품화", ["model quality", "auditor", "addin", "add-in", "revit", "navisworks", "autodesk", "store", "스토어", "상품", "수익", "패키지"]),
    ("교육/온보딩 재사용", ["교육", "커리큘럼", "온보딩", "연차", "팀원", "훈련", "슬라이드", "notebooklm"]),
    ("AI/자동화 생산성", ["ai", "qwen", "자동화", "엑셀", "excel", "개발", "코드", "python", "api", "프롬프트"]),
    ("공식 문서/고객 설명 전환", ["제안", "보고서", "회의록", "rfi", "sow", "견적", "고객", "공식", "외부", "제출"]),
    ("운영/보안/계약 리스크", ["보안", "계약", "개인정보", "토큰", "계정", "권한", "법무", "리스크", "비밀", "승인"]),
]

PROMOTION_RULES = [
    ("표준문서 후보", ["기준", "표준", "절차", "sop", "검수", "체크리스트", "템플릿"]),
    ("교육자료 후보", ["교육", "커리큘럼", "온보딩", "실습", "평가", "팀원"]),
    ("상품자료 후보", ["상품", "가격", "스토어", "패키지", "고객", "판매", "autodesk"]),
    ("QA 체크리스트 후보", ["오류", "검증", "테스트", "품질", "간섭", "재발", "검수"]),
    ("FAQ/고객지원 후보", ["질문", "답변", "문의", "고객지원", "cs", "telegram", "팀원"]),
    ("개발/자동화 백로그 후보", ["개발", "자동화", "qwen", "api", "addin", "excel", "python"]),
]

SECURITY_PATTERNS = [
    ("개인정보 가능성", re.compile(r"(주민|급여|연봉|전화|휴대폰|이메일|메일|개인정보|telegram id|chat id)", re.I)),
    ("계정/토큰 가능성", re.compile(r"(api[_ -]?key|token|secret|password|비밀번호|계정|ssh|\.env)", re.I)),
    ("내부 경로 노출", re.compile(r"(/Users/|C:\\\\|/Volumes/|/private/)", re.I)),
    ("고객/프로젝트 실명 가능성", re.compile(r"(고객명|프로젝트명|발주처|계약금|계약조건)", re.I)),
]


@dataclass
class Finding:
    rel: str
    title: str
    category: str
    purposes: list[str]
    promotions: list[str]
    risks: list[str]
    recommendation: str
    reason: str
    mtime: dt.datetime


def should_skip(path: Path) -> bool:
    if any(part in EXCLUDE_PARTS for part in path.parts):
        return True
    rel = path.relative_to(PROJECT_ROOT).as_posix()
    if rel.startswith("obsidian_vaults/lua_bim_lab_global_map/") and "/NAS_Knowledge/" not in rel:
        return True
    if rel.endswith("_DAILY_KNOWLEDGE_UPDATE.md"):
        return True
    return False


def extract_title(text: str, path: Path) -> str:
    for line in text.splitlines()[:40]:
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def normalize(text: str) -> str:
    return text.lower()


def matched_labels(text: str, rules: list[tuple[str, list[str]]]) -> list[str]:
    lower = normalize(text)
    labels = []
    for label, keywords in rules:
        if any(keyword.lower() in lower for keyword in keywords):
            labels.append(label)
    return labels


def matched_risks(text: str) -> list[str]:
    return [label for label, pattern in SECURITY_PATTERNS if pattern.search(text)]


def category_for(rel: str) -> str:
    if rel.startswith("data/knowledge_base/"):
        return "지식베이스"
    if rel.startswith("data/team_requests/"):
        return "팀 요청 로그"
    if rel.startswith("docs/industry_intelligence/"):
        return "산업동향"
    if rel.startswith("docs/standard_documents/"):
        return "표준문서"
    if rel.startswith("docs/internal_organization_documents/"):
        return "조직운영문서"
    if rel.startswith("docs/revenue_products/"):
        return "상품문서"
    if rel.startswith("docs/training_curriculum/"):
        return "교육자료"
    if rel.startswith("obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/Team_Telegram_QA/"):
        return "팀 Q&A"
    if rel.startswith("obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/"):
        return "Obsidian Q&A"
    if rel.startswith("obsidian_vaults/model_quality_auditor/03_Errors_Fixes/"):
        return "오류 오답노트"
    if rel.startswith("obsidian_vaults/model_quality_auditor/"):
        return "MQA Obsidian"
    return "기타"


def recommendation_for(purposes: list[str], promotions: list[str], risks: list[str], text: str) -> tuple[str, str]:
    if risks:
        return "보안검토", "개인정보/계정/내부경로 등 공개 전 확인이 필요한 신호가 있음"
    if "knowledge-gap-needs-review" in text:
        return "보강필요", "팀원 답변 부족 또는 지식 공백으로 표시됨"
    if len(promotions) >= 2:
        return "승격후보", "표준/교육/상품/QA 등 여러 산출물로 전환 가능"
    if purposes:
        return "유지", "회사 목적성 기준과 연결됨"
    return "보류", "현재 목적성 키워드가 약하므로 중복/아카이브 여부 확인"


def iter_recent_markdown(days: int) -> list[Path]:
    cutoff = dt.datetime.now().timestamp() - days * 86400
    files: list[Path] = []
    for root in SOURCE_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            if path.is_file() and not should_skip(path) and path.stat().st_mtime >= cutoff:
                files.append(path)
    return sorted(set(files))


def analyze(path: Path) -> Finding:
    text = path.read_text(encoding="utf-8", errors="ignore")
    rel = path.relative_to(PROJECT_ROOT).as_posix()
    title = extract_title(text, path)
    scan_text = f"{rel}\n{title}\n{text[:12000]}"
    purposes = matched_labels(scan_text, PURPOSE_RULES)
    promotions = matched_labels(scan_text, PROMOTION_RULES)
    risks = matched_risks(scan_text)
    recommendation, reason = recommendation_for(purposes, promotions, risks, scan_text)
    return Finding(
        rel=rel,
        title=title,
        category=category_for(rel),
        purposes=purposes,
        promotions=promotions,
        risks=risks,
        recommendation=recommendation,
        reason=reason,
        mtime=dt.datetime.fromtimestamp(path.stat().st_mtime),
    )


def table_rows(findings: list[Finding]) -> str:
    if not findings:
        return "| - | - | - | - | - | - |\n"
    rows = []
    for item in findings:
        rows.append(
            "| "
            + " | ".join([
                f"`{item.rel}`",
                item.category,
                item.recommendation,
                ", ".join(item.purposes[:3]) or "-",
                ", ".join(item.promotions[:3]) or "-",
                ", ".join(item.risks) or "-",
            ])
            + " |"
        )
    return "\n".join(rows)


def build_report(findings: list[Finding], today: str, days: int) -> str:
    by_rec: dict[str, list[Finding]] = {}
    for item in findings:
        by_rec.setdefault(item.recommendation, []).append(item)

    ordered = ["보안검토", "보강필요", "승격후보", "유지", "보류"]
    counts = {key: len(by_rec.get(key, [])) for key in ordered}
    top = sorted(
        findings,
        key=lambda item: (
            {"보안검토": 0, "보강필요": 1, "승격후보": 2, "유지": 3, "보류": 4}.get(item.recommendation, 9),
            -len(item.promotions),
            item.rel,
        ),
    )[:40]

    sections = []
    for key in ordered:
        items = by_rec.get(key, [])
        sections.append(f"### {key}\n\n" + table_rows(items[:20]))

    return f"""---
type: daily-knowledge-curation
date: {today}
status: generated
tags:
  - knowledge-curation
  - obsidian
  - daily-review
---

# {today} Daily Knowledge Curation Review

최근 {days}일 내 변경된 Markdown 지식을 자동 분류한 검수 리포트다. 이 리포트는 최종 승인 문서가 아니라 지식 큐레이션 담당자가 빠르게 판단하기 위한 1차 분류표다.

## 요약

| 분류 | 수량 |
|---|---:|
| 보안검토 | {counts["보안검토"]} |
| 보강필요 | {counts["보강필요"]} |
| 승격후보 | {counts["승격후보"]} |
| 유지 | {counts["유지"]} |
| 보류 | {counts["보류"]} |
| 검토 대상 전체 | {len(findings)} |

## 우선 검토 목록

| 문서 | 유형 | 권고 | 목적성 연결 | 승격 후보 | 리스크 |
|---|---|---|---|---|---|
{table_rows(top)}

## 분류별 상세

{chr(10).join(sections)}

## 처리 기준

- `보안검토`: 외부 공개 또는 팀 공유 전 민감정보 제거를 우선한다.
- `보강필요`: 팀원 질문 또는 부족한 답변을 담당 지식베이스에 보강한다.
- `승격후보`: 표준문서, 교육자료, 상품자료, QA 체크리스트, FAQ로 전환할지 판단한다.
- `유지`: 현재 위치에 보관하되 Obsidian 연결성을 유지한다.
- `보류`: 중복, 목적성 낮음, 미검증 가능성을 확인하고 필요 시 아카이브한다.

## 연결

- [[21_KNOWLEDGE_CURATION_INTELLIGENCE_CELL]]
- [[24_TEAM_TELEGRAM_KNOWLEDGE_REQUEST_LOOP]]
- [[Global Knowledge Map]]
"""


def append_daily_report(today: str, curation_path: Path, findings: list[Finding]) -> None:
    daily = DAILY_REPORT_DIR / f"{today}_DAILY_KNOWLEDGE_UPDATE.md"
    if not daily.exists():
        return
    text = daily.read_text(encoding="utf-8")
    marker = "## 자동 큐레이션 검수"
    summary = {
        "보안검토": 0,
        "보강필요": 0,
        "승격후보": 0,
        "유지": 0,
        "보류": 0,
    }
    for item in findings:
        summary[item.recommendation] = summary.get(item.recommendation, 0) + 1
    rel = curation_path.relative_to(PROJECT_ROOT).as_posix()
    block = f"""{marker}

- [x] 최근 변경 지식 자동 분류 실행
- 검수 리포트: `{rel}`
- 보안검토: {summary["보안검토"]}
- 보강필요: {summary["보강필요"]}
- 승격후보: {summary["승격후보"]}
- 유지: {summary["유지"]}
- 보류: {summary["보류"]}
"""
    if marker in text:
        text = text[: text.index(marker)].rstrip() + "\n\n" + block + "\n"
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    daily.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily knowledge curation review")
    parser.add_argument("--days", type=int, default=2, help="최근 변경 문서 조회 기간")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    findings = [analyze(path) for path in iter_recent_markdown(args.days)]
    findings.sort(key=lambda item: (item.recommendation, item.category, item.rel))

    report_path = REPORT_DIR / f"{args.date}_DAILY_KNOWLEDGE_CURATION.md"
    report_path.write_text(build_report(findings, args.date, args.days), encoding="utf-8")
    append_daily_report(args.date, report_path, findings)
    print(f"curation_report={report_path}")
    print(f"curation_items={len(findings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

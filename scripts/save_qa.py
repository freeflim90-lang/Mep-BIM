#!/usr/bin/env python3
"""Q&A 지식 저장 도구 — Obsidian NAS_Knowledge 폴더에 Q&A 노트를 생성하고 MOC를 갱신한다.

사용법:
    # 수동 입력 (팀원/클라이언트/교육 Q&A)
    python save_qa.py --title "Revit 패밀리 공유 방법" --q "패밀리 파일 팀 공유 방법은?" \
        --a "중앙 라이브러리 경로를 Revit.ini에 등록한다." \
        --category 팀원간질문 --domain Revit

    # Claude 세션에서 자동 추출 (대화 종료 후 호출)
    python save_qa.py --from-session <session-jsonl-path>

    # MOC만 갱신
    python save_qa.py --update-moc
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VAULT = PROJECT_ROOT / "obsidian_vaults" / "lua_bim_lab_global_map"
QA_DIR = VAULT / "NAS_Knowledge"
# NAS_Knowledge 내부에 위치 — build_global_obsidian_map.py가 01_MOC/를 덮어쓰므로 분리
MOC_PATH = QA_DIR / "MOC - QA Index.md"

CATEGORIES = ["팀원간질문", "교육온보딩", "클라이언트", "Claude대화"]
DOMAINS = ["BIM실무", "Revit", "Dynamo", "MEP", "Navisworks", "조직운영", "개발기술", "기타"]


# ── 노트 생성 ──────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s가-힣-]", "", text)
    text = re.sub(r"\s+", "_", text.strip())
    return text[:60]


def make_note(title: str, question: str, answer: str, category: str,
              domain: str, date: str, source: str = "") -> str:
    source_line = f"\n> **출처:** {source}" if source else ""
    return f"""---
type: qa-note
category: {category}
domain: {domain}
date: {date}
status: verified
tags:
  - QA
  - {domain}
---

# QA - {title}

## 질문
> **카테고리:** {category} | **날짜:** {date}{source_line}

{question}

## 답변

{answer}

## 관련 자료

- [[MOC - Q&A Knowledge Base]]

## 연결

- [[Global Knowledge Map]]
"""


def save_note(title: str, question: str, answer: str, category: str,
              domain: str, date: str, source: str = "") -> Path:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    slug = slugify(title)
    filename = f"QA - {slug}.md"
    path = QA_DIR / filename

    # 동일 제목 노트가 이미 있으면 누적
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        new_block = f"\n---\n\n## 질문 (추가 {date})\n> **카테고리:** {category} | **날짜:** {date}{chr(10) + '> **출처:** ' + source if source else ''}\n\n{question}\n\n## 답변\n\n{answer}\n"
        path.write_text(existing + new_block, encoding="utf-8")
        print(f"[누적] {path.name}")
    else:
        content = make_note(title, question, answer, category, domain, date, source)
        path.write_text(content, encoding="utf-8")
        print(f"[생성] {path.name}")

    return path


# ── MOC 갱신 ──────────────────────────────────────────────────────────────

def update_moc() -> None:
    if not QA_DIR.exists():
        return

    notes = list(QA_DIR.glob("QA - *.md"))
    by_cat: dict[str, list[str]] = {c: [] for c in CATEGORIES}

    for note in sorted(notes):
        text = note.read_text(encoding="utf-8")
        cat = "기타"
        m = re.search(r"^category:\s*(.+)$", text, re.MULTILINE)
        if m:
            cat = m.group(1).strip()
        title = note.stem  # "QA - 제목"
        entry = f"- [[{title}]]"
        if cat in by_cat:
            by_cat[cat].append(entry)
        else:
            by_cat.setdefault(cat, []).append(entry)

    moc = MOC_PATH.read_text(encoding="utf-8")

    # 카테고리 섹션 교체
    for cat, entries in by_cat.items():
        block = "\n".join(entries) if entries else "*아직 없음*"
        pattern = rf"(<!-- qa-index:{re.escape(cat)} -->)(.*?)(<!-- qa-index:|## 통계|$)"
        replacement = rf"\g<1>\n{block}\n\n\g<3>"
        moc = re.sub(pattern, replacement, moc, flags=re.DOTALL)

    # 통계 갱신
    total = len(notes)
    for cat in CATEGORIES:
        cnt = len(by_cat.get(cat, []))
        moc = re.sub(
            rf"(\| {cat}\s*\|)\s*\d+\s*\|",
            rf"\g<1> {cnt} |",
            moc,
        )
    moc = re.sub(r"(\| 전체 Q&A 노트\s*\|)\s*\d+\s*\|", rf"\g<1> {total} |", moc)

    MOC_PATH.write_text(moc, encoding="utf-8")
    print(f"[MOC 갱신] {total}개 노트 인덱스 완료")


# ── Claude 세션 파싱 ────────────────────────────────────────────────────────

def extract_session_qa(jsonl_path: Path) -> list[dict]:
    """Claude Code 세션 JSONL에서 사용자-어시스턴트 교환을 추출한다."""
    pairs: list[dict] = []
    messages: list[dict] = []

    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            if d.get("type") in ("user", "assistant"):
                role = d["type"]
                content = d.get("message", {}).get("content", [])
                text = ""
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "text":
                        text += c.get("text", "")
                if text.strip():
                    messages.append({"role": role, "text": text.strip(), "ts": d.get("timestamp", "")})

    # user → assistant 쌍으로 묶기
    i = 0
    while i < len(messages) - 1:
        if messages[i]["role"] == "user" and messages[i + 1]["role"] == "assistant":
            q = messages[i]["text"]
            a = messages[i + 1]["text"]
            if _is_quality_pair(q, a):
                pairs.append({"question": q, "answer": a, "ts": messages[i]["ts"]})
        i += 1

    return pairs


# 저품질 Q&A 필터 기준
_NOISE_Q_PATTERNS = [
    "[Request interrupted",
    "Tool loaded",
    "# Update Config Skill",   # 스킬 문서 덩어리
    "# Keybindings",
    "User has answered",
]
_NOISE_A_PREFIXES = [
    "현재 작업 디렉토리와 메모리를",
    "기존 엑셀 자동화 관련 자료를 먼저",
    "프로젝트에 텔레그램 관련 설정이 있는지 먼저",
    "먼저 확인",
    "파악하겠습니다",
    "확인하겠습니다",
]
_MIN_Q_LEN = 8    # 질문 최소 길이
_MIN_A_LEN = 80   # 답변 최소 길이 (단순 "확인하겠습니다" 제거)
_MAX_Q_LEN = 5000 # 질문 최대 길이 (스킬 문서 덩어리 제거)


def _is_quality_pair(q: str, a: str) -> bool:
    if len(q) < _MIN_Q_LEN or len(a) < _MIN_A_LEN:
        return False
    if len(q) > _MAX_Q_LEN:
        return False
    for pat in _NOISE_Q_PATTERNS:
        if pat in q:
            return False
    for prefix in _NOISE_A_PREFIXES:
        if a.strip().startswith(prefix):
            return False
    return True


def save_from_session(jsonl_path: Path, auto: bool = False) -> None:
    pairs = extract_session_qa(jsonl_path)
    if not pairs:
        print("추출된 Q&A 쌍 없음")
        return

    today = dt.date.today().isoformat()
    print(f"\n총 {len(pairs)}개 Q&A 쌍 발견\n")

    for i, pair in enumerate(pairs):
        q_preview = pair["question"][:80].replace("\n", " ")
        print(f"[{i+1}/{len(pairs)}] Q: {q_preview}...")

        if not auto:
            choice = input("  저장? (y/n/q=종료) [n]: ").strip().lower()
            if choice == "q":
                break
            if choice != "y":
                continue

        # 자동/수동 메타데이터 결정
        title = pair["question"].split("\n")[0][:50].strip()
        category = "Claude대화"
        domain = "기타"

        if not auto:
            title_in = input(f"  제목 [{title}]: ").strip()
            if title_in:
                title = title_in
            print(f"  도메인 선택: {', '.join(f'{j+1}={d}' for j, d in enumerate(DOMAINS))}")
            dom_in = input("  번호 [8=기타]: ").strip()
            if dom_in.isdigit() and 1 <= int(dom_in) <= len(DOMAINS):
                domain = DOMAINS[int(dom_in) - 1]

        save_note(title, pair["question"], pair["answer"],
                  category, domain, today, source="Claude Code 세션")

    update_moc()


# ── CLI ────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Q&A → Obsidian NAS_Knowledge")
    sub = parser.add_subparsers(dest="cmd")

    # 수동 저장
    p_add = sub.add_parser("add", help="Q&A 수동 저장")
    p_add.add_argument("--title", required=True, help="노트 제목")
    p_add.add_argument("--q", required=True, help="질문")
    p_add.add_argument("--a", required=True, help="답변")
    p_add.add_argument("--category", choices=CATEGORIES, default="팀원간질문")
    p_add.add_argument("--domain", choices=DOMAINS, default="BIM실무")
    p_add.add_argument("--source", default="", help="출처 (사람 이름, 채널 등)")
    p_add.add_argument("--date", default=dt.date.today().isoformat())

    # 세션 파싱
    p_sess = sub.add_parser("from-session", help="Claude 세션에서 Q&A 추출")
    p_sess.add_argument("jsonl", help="세션 .jsonl 파일 경로")
    p_sess.add_argument("--auto", action="store_true", help="확인 없이 전체 저장")

    # 최신 세션 자동 처리 (Stop 훅에서 호출)
    p_latest = sub.add_parser("latest-session", help="가장 최근 세션에서 자동 저장")
    p_latest.add_argument("--project-dir", default=str(PROJECT_ROOT),
                           help="프로젝트 경로 (Claude가 --cwd로 실행한 경로)")

    # MOC 갱신
    sub.add_parser("update-moc", help="MOC만 갱신")

    # 구버전 호환 플래그 (--from-session, --update-moc)
    parser.add_argument("--from-session", metavar="JSONL")
    parser.add_argument("--update-moc", action="store_true")
    parser.add_argument("--title")
    parser.add_argument("--q")
    parser.add_argument("--a")
    parser.add_argument("--category", choices=CATEGORIES, default="팀원간질문")
    parser.add_argument("--domain", choices=DOMAINS, default="BIM실무")
    parser.add_argument("--source", default="")
    parser.add_argument("--date", default=dt.date.today().isoformat())

    args = parser.parse_args()

    # 서브커맨드 처리
    if args.cmd == "add":
        save_note(args.title, args.q, args.a, args.category,
                  args.domain, args.date, args.source)
        update_moc()

    elif args.cmd == "from-session":
        save_from_session(Path(args.jsonl), auto=args.auto)

    elif args.cmd == "latest-session":
        cwd_slug = args.project_dir.replace("/", "-").replace(" ", "-")
        projects_dir = Path.home() / ".claude" / "projects"
        target = None
        for d in projects_dir.iterdir():
            if d.name in cwd_slug or cwd_slug in d.name:
                target = d
                break
        if not target:
            print("프로젝트 디렉토리를 ~/.claude/projects 에서 찾지 못했습니다.")
            return 1
        jsonl_files = sorted(target.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
        if not jsonl_files:
            print("세션 파일 없음")
            return 1
        latest = jsonl_files[-1]
        print(f"세션 파일: {latest.name}")
        save_from_session(latest, auto=True)

    elif args.cmd == "update-moc":
        update_moc()

    # 구버전 호환 플래그
    elif args.from_session:
        save_from_session(Path(args.from_session))

    elif args.update_moc:
        update_moc()

    elif args.title and args.q and args.a:
        save_note(args.title, args.q, args.a, args.category,
                  args.domain, args.date, args.source)
        update_moc()

    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

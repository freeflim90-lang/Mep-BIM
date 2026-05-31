#!/usr/bin/env python3
"""Generate a daily reasoning-training digest for LUA BIM LABS.

The digest is intentionally reviewable: it turns recent knowledge signals into
self-questions, tentative inferences, and a practical note for the leader to
annotate in Telegram. The leader's reply can then be folded back into the
knowledge base as deeper field knowledge.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "docs" / "reasoning_training"
KB_FILE = PROJECT_ROOT / "data" / "knowledge_base" / "추론훈련루프.md"
STATE_FILE = PROJECT_ROOT / "runtime" / "reasoning_training_digest_seen.txt"

SOURCE_GLOBS = [
    "data/knowledge_base/*.md",
    "data/knowledge_base/qa/*.md",
    "data/team_requests/*.md",
    "docs/internal_growth/**/*.md",
    "docs/knowledge_updates/daily/*.md",
    "docs/industry_intelligence/daily/*.md",
    "obsidian_vaults/model_quality_auditor/03_Errors_Fixes/*.md",
    "obsidian_vaults/model_quality_auditor/04_Decisions/*.md",
    "obsidian_vaults/model_quality_auditor/05_Revit_API_Gates/*.md",
]

SIGNAL_KEYWORDS = {
    "실무문제": ["오류", "문제", "실패", "이슈", "막힘", "원인", "수정", "검증", "재발"],
    "지식공백": ["needs-review", "gap", "공백", "확인 필요", "미검증", "보강", "질문"],
    "자동화": ["자동화", "script", "api", "addin", "add-in", "revit", "navisworks", "dynamo"],
    "품질": ["품질", "검토", "audit", "clash", "간섭", "납품", "체크리스트", "룰"],
    "사업화": ["고객", "상품", "제품", "store", "견적", "제안", "교육", "컨설팅"],
}


@dataclass
class Signal:
    path: Path
    line: str
    categories: list[str]
    score: int

    @property
    def fingerprint(self) -> str:
        raw = f"{self.path.as_posix()}::{self.line}"
        return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def load_local_env() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def recent_paths(days: int) -> list[Path]:
    cutoff = dt.datetime.now() - dt.timedelta(days=days)
    paths: list[Path] = []
    for pattern in SOURCE_GLOBS:
        for path in PROJECT_ROOT.glob(pattern):
            if not path.is_file():
                continue
            if "lua_bim_lab_global_map" in path.parts:
                continue
            try:
                modified = dt.datetime.fromtimestamp(path.stat().st_mtime)
            except OSError:
                continue
            if modified >= cutoff:
                paths.append(path)
    return sorted(set(paths))


def clean_line(raw: str) -> str:
    line = raw.strip()
    if line.count("|") >= 3:
        return ""
    line = re.sub(r"^[-*#>\s]+", "", line)
    line = re.sub(r"\s+", " ", line)
    return line[:260]


def classify(line: str) -> tuple[list[str], int]:
    lowered = line.lower()
    categories: list[str] = []
    score = 0
    for category, keywords in SIGNAL_KEYWORDS.items():
        hits = [keyword for keyword in keywords if keyword.lower() in lowered]
        if hits:
            categories.append(category)
            score += len(hits) * 2
    if "telegram" in lowered or "팀원" in lowered:
        score += 2
    if "source:" in lowered or "tags:" in lowered:
        score -= 2
    return categories, score


def collect_signals(days: int, limit: int) -> list[Signal]:
    signals: list[Signal] = []
    for path in recent_paths(days):
        for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = clean_line(raw)
            if len(line) < 18:
                continue
            categories, score = classify(line)
            if categories and score > 0:
                rel = path.relative_to(PROJECT_ROOT).as_posix()
                path_weight = 3 if any(part in rel for part in ["team_requests", "03_Errors_Fixes", "05_Revit_API_Gates"]) else 0
                signals.append(Signal(path=path, line=line, categories=categories, score=score + path_weight))
    signals.sort(key=lambda item: (item.score, item.path.stat().st_mtime), reverse=True)
    return dedupe_signals(signals, limit)


def dedupe_signals(signals: list[Signal], limit: int) -> list[Signal]:
    seen_lines: set[str] = set()
    chosen: list[Signal] = []
    for signal in signals:
        key = re.sub(r"\W+", "", signal.line.lower())[:120]
        if key in seen_lines:
            continue
        seen_lines.add(key)
        chosen.append(signal)
        if len(chosen) >= limit:
            break
    return chosen


def load_seen() -> set[str]:
    if not STATE_FILE.exists():
        return set()
    return {line.strip() for line in STATE_FILE.read_text(encoding="utf-8").splitlines() if line.strip()}


def save_seen(signals: list[Signal]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = load_seen()
    existing.update(signal.fingerprint for signal in signals)
    STATE_FILE.write_text("\n".join(sorted(existing)) + "\n", encoding="utf-8")


def self_questions(signal: Signal) -> list[str]:
    cats = set(signal.categories)
    questions = [
        "이 신호가 실제 현장 문제라면 가장 먼저 확인해야 할 증거는 무엇인가?",
        "과거 LUA BIM LABS 지식 중 같은 패턴으로 연결할 수 있는 기록은 무엇인가?",
    ]
    if "자동화" in cats:
        questions.append("반복 실행 가능한 스크립트나 Add-in 기능으로 승격할 수 있는가?")
    if "품질" in cats:
        questions.append("납품 전 체크리스트나 Model Quality Auditor 룰로 바꿀 수 있는가?")
    if "지식공백" in cats:
        questions.append("공식 문서, 실제 프로젝트, 담당자 경험 중 무엇으로 검증해야 하는가?")
    if "사업화" in cats:
        questions.append("고객에게 설명 가능한 상품, 교육, 리포트 언어로 바꾸면 무엇이 남는가?")
    return questions[:4]


def inference(signal: Signal) -> str:
    cats = "·".join(signal.categories)
    if "지식공백" in signal.categories:
        return f"{cats} 신호다. 지금 단계에서는 결론보다 검증 질문을 먼저 남겨야 하며, 대표님의 실무 판단을 붙이면 조직 지식의 깊이가 커진다."
    if "자동화" in signal.categories or "품질" in signal.categories:
        return f"{cats} 신호다. 반복되는 판단을 규칙, 체크리스트, 스크립트 후보로 바꾸면 다음 프로젝트의 처리 속도가 올라간다."
    return f"{cats} 신호다. 단일 기록으로 끝내지 말고 현장 사례, 고객 언어, 내부 실행 기준을 함께 붙이면 재사용 가능한 경험 카드가 된다."


def recommended_action(signal: Signal) -> str:
    cats = set(signal.categories)
    if {"자동화", "품질"} & cats:
        return "관련 내부 근거를 1개 더 연결하고, 체크리스트 항목 또는 자동화 백로그 후보로 승격할지 판단한다."
    if "지식공백" in cats:
        return "단정 답변을 보류하고 공식 문서, 프로젝트 사례, 담당자 경험 중 최소 2개 근거로 검증한다."
    if "사업화" in cats:
        return "고객에게 설명 가능한 효율, 품질, 리스크 절감 문장으로 바꾼 뒤 제안서/교육자료 재사용성을 확인한다."
    return "실무 예외 조건을 붙여 경험 카드로 저장하고 다음 유사 문제의 확인 질문으로 재사용한다."


def build_report(signals: list[Signal]) -> tuple[str, str]:
    now = dt.datetime.now()
    if not signals:
        body = "최근 지식 신호에서 새 추론 후보를 찾지 못했다. 오늘은 기존 미검증 항목과 팀원 질문 로그를 재검토한다."
    else:
        sections = []
        for index, signal in enumerate(signals, 1):
            rel = signal.path.relative_to(PROJECT_ROOT).as_posix()
            questions = "\n".join(f"- {question}" for question in self_questions(signal))
            sections.append(
                f"""## {index}. 추론 후보: {', '.join(signal.categories)}

- 내부 근거: `{rel}`
- 관찰 신호: {signal.line}
- 1차 추론: {inference(signal)}
- 해결 방향 초안: {recommended_action(signal)}

### 스스로 던질 질문
{questions}

### 대표 첨언 요청
- 이 내용이 실제 실무에서 맞는 방향인지, 현장 경험이나 예외 조건을 덧붙인다.
"""
            )
        body = "\n\n".join(sections)

    content = f"""---
type: reasoning-training-digest
date: {now.strftime('%Y-%m-%d')}
status: generated
tags:
  - reasoning-training
  - internal-growth
  - telegram
  - obsidian
---

# {now.strftime('%Y-%m-%d %H:%M')} LUA BIM LABS 추론 훈련 다이제스트

이 문서는 최근 내부 지식, 팀원 질문, 오류 기록, 성장 펄스에서 문제 신호를 골라
스스로 질문하고 추론한 뒤 대표의 실무 첨언을 받기 위한 백그라운드 훈련 로그다.

{body}

## 지식화 루프

1. 시스템이 문제 신호를 발견한다.
2. 시스템이 스스로 질문과 1차 추론을 만든다.
3. 대표가 텔레그램에서 실무 첨언을 더한다.
4. 첨언을 Obsidian 지식, QA, 체크리스트, 자동화 후보로 승격한다.
"""

    telegram = format_telegram(now, signals)
    return content, telegram


def format_telegram(now: dt.datetime, signals: list[Signal]) -> str:
    lines = [
        f"[LUA BIM LABS 추론 훈련] {now.strftime('%Y-%m-%d %H:%M')}",
        "",
        "백그라운드가 오늘의 문제 신호를 읽고 스스로 질문을 만들었습니다.",
    ]
    if not signals:
        lines.append("새 후보는 없고, 기존 미검증 지식 재검토가 필요합니다.")
        return "\n".join(lines)

    for index, signal in enumerate(signals[:3], 1):
        rel = signal.path.relative_to(PROJECT_ROOT).as_posix()
        questions = self_questions(signal)
        lines.extend(
            [
                "",
                f"{index}. {', '.join(signal.categories)}",
                f"근거: {rel}",
                f"신호: {signal.line[:180]}",
                f"추론: {inference(signal)}",
                f"해결 방향: {recommended_action(signal)}",
                f"질문: {questions[0]}",
            ]
        )
    lines.extend(
        [
            "",
            "대표 첨언 요청: 실무에서 맞는 점, 빠진 예외, 고객에게 설명할 언어를 답장으로 남겨주세요.",
        ]
    )
    return "\n".join(lines)


def update_kb(report_path: Path, signals: list[Signal]) -> None:
    if not KB_FILE.exists():
        KB_FILE.parent.mkdir(parents=True, exist_ok=True)
        KB_FILE.write_text(
            "# 추론훈련루프 지식 베이스\n\n"
            "LUA BIM LABS가 문제 신호를 스스로 질문하고 추론하며, 대표의 실무 첨언으로 지식을 깊고 넓게 확장하는 루프를 기록한다.\n",
            encoding="utf-8",
        )
    counts: dict[str, int] = {}
    for signal in signals:
        for category in signal.categories:
            counts[category] = counts.get(category, 0) + 1
    summary = ", ".join(f"{key} {value}" for key, value in sorted(counts.items())) or "신규 후보 없음"
    timestamp = dt.datetime.now().isoformat(timespec="seconds")
    with KB_FILE.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n\n## {timestamp} 추론 훈련 다이제스트\n"
            f"- Source: `{report_path.relative_to(PROJECT_ROOT).as_posix()}`\n"
            "- Tags: reasoning-training,internal-growth,telegram,obsidian\n\n"
            f"분류 요약: {summary}\n\n"
            "운영 판단: 시스템의 1차 추론은 대표의 실무 첨언을 받은 뒤 QA, 체크리스트, 자동화 후보, 교육 자료로 승격한다.\n"
        )


def send_telegram(message: str) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("telegram=skipped missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        return False
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": message}).encode("utf-8")
    request = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=payload, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            print(f"telegram=sent status={response.status}")
        return True
    except Exception as exc:  # noqa: BLE001 - daily background jobs should not crash on notification.
        print(f"telegram=failed {type(exc).__name__}: {exc}")
        return False


def run(days: int, limit: int, send: bool, include_seen: bool) -> Path:
    load_local_env()
    signals = collect_signals(days, limit * 3)
    if not include_seen:
        seen = load_seen()
        signals = [signal for signal in signals if signal.fingerprint not in seen]
    signals = signals[:limit]
    content, telegram = build_report(signals)

    now = dt.datetime.now()
    date_dir = REPORT_DIR / now.strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)
    report_path = date_dir / f"{now.strftime('%H%M')}_LUA_REASONING_TRAINING_DIGEST.md"
    report_path.write_text(content, encoding="utf-8")
    update_kb(report_path, signals)
    save_seen(signals)
    if send:
        telegram_with_context = (
            f"{telegram}\n\n"
            f"기록: {report_path.relative_to(PROJECT_ROOT).as_posix()}\n"
            "이 메시지에 답장으로 회신하면 추론 첨언으로 저장됩니다."
        )
        send_telegram(telegram_with_context)
    print(f"reasoning_training_digest={report_path}")
    print(f"signals={len(signals)}")
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate LUA BIM LABS reasoning-training digest.")
    parser.add_argument("--days", type=int, default=3, help="Recent modified-day window to inspect.")
    parser.add_argument("--limit", type=int, default=3, help="Maximum reasoning candidates.")
    parser.add_argument("--no-telegram", action="store_true", help="Generate markdown without sending Telegram.")
    parser.add_argument("--include-seen", action="store_true", help="Allow previously sent signals.")
    args = parser.parse_args()
    run(days=args.days, limit=args.limit, send=not args.no_telegram, include_seen=args.include_seen)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

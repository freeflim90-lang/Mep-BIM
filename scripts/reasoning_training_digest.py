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
import json
import os
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys  # noqa: E402
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import AGENT_KB_DIR, KNOWLEDGE_UPDATES_DIR, QA_KB_DIR, TEAM_REQUESTS_DIR  # noqa: E402
from backend.knowledge_store import knowledge_file_path  # noqa: E402

REPORT_DIR = PROJECT_ROOT / "docs" / "reasoning_training"
KB_FILE = Path(knowledge_file_path("추론훈련루프"))
STATE_FILE = PROJECT_ROOT / "runtime" / "reasoning_training_digest_seen.txt"
QUESTION_HISTORY_FILE = PROJECT_ROOT / "runtime" / "reasoning_training_question_history.json"
DEEPSEEK_BUDGET_FILE = PROJECT_ROOT / "data" / "ai_usage" / "deepseek_monthly_budget.json"
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_ESTIMATED_CALL_COST_USD = 0.35
MIN_DEEPSEEK_QUESTION_NOVELTY = 0.42

_KB_REL = AGENT_KB_DIR.relative_to(PROJECT_ROOT).as_posix()
_QA_REL = QA_KB_DIR.relative_to(PROJECT_ROOT).as_posix()
_TEAM_REQ_REL = TEAM_REQUESTS_DIR.relative_to(PROJECT_ROOT).as_posix()
_UPDATES_REL = KNOWLEDGE_UPDATES_DIR.relative_to(PROJECT_ROOT).as_posix()

SOURCE_GLOBS = [
    f"{_KB_REL}/**/*.md",
    f"{_QA_REL}/*.md",
    f"{_TEAM_REQ_REL}/*.md",
    "docs/internal_growth/**/*.md",
    f"{_UPDATES_REL}/daily/*.md",
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

    @property
    def semantic_fingerprint(self) -> str:
        """Fingerprint the actual signal so daily files cannot repeat it forever."""
        normalized = re.sub(r"\W+", "", self.line.lower())
        return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:16]


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


def collect_signals(days: int, limit: int, seen: set[str] | None = None) -> list[Signal]:
    seen = seen or set()
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
                signal = Signal(path=path, line=line, categories=categories, score=score + path_weight)
                if signal.fingerprint in seen or signal.semantic_fingerprint in seen:
                    continue
                signals.append(signal)
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
    seen: set[str] = set()
    if not STATE_FILE.exists():
        return load_historical_seen()
    seen.update(line.strip() for line in STATE_FILE.read_text(encoding="utf-8").splitlines() if line.strip())
    seen.update(load_historical_seen())
    return seen


def load_historical_seen() -> set[str]:
    """Include old digest observation lines created before semantic seen keys existed."""
    seen: set[str] = set()
    for path in REPORT_DIR.glob("**/*_LUA_REASONING_TRAINING_DIGEST.md"):
        if "/feedback/" in path.as_posix():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in re.finditer(r"^- 관찰 신호:\s*(.+)$", text, flags=re.MULTILINE):
            normalized = re.sub(r"\W+", "", match.group(1).strip().lower())
            if normalized:
                seen.add(hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:16])
    return seen


def save_seen(signals: list[Signal]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = load_seen()
    for signal in signals:
        existing.add(signal.fingerprint)
        existing.add(signal.semantic_fingerprint)
    STATE_FILE.write_text("\n".join(sorted(existing)) + "\n", encoding="utf-8")


def focus_phrase(signal: Signal) -> str:
    line = re.sub(r"`([^`]+)`", r"\1", signal.line)
    line = re.sub(r"[\[\]()*_>#]", "", line)
    line = re.sub(r"\s+", " ", line).strip(" .,-")
    if len(line) <= 70:
        return line
    return line[:67].rstrip() + "..."


def self_questions(signal: Signal) -> list[str]:
    cats = set(signal.categories)
    focus = focus_phrase(signal)
    questions = []
    if "실무문제" in cats:
        questions.append(f"`{focus}`가 실제 현장 문제라면 재현 조건, 영향 범위, 임시 조치 중 무엇을 먼저 확인해야 하는가?")
    else:
        questions.append(f"`{focus}`를 실제 실행 후보로 볼 때 지금 당장 확인할 근거는 무엇인가?")
    if "자동화" in cats:
        questions.append(f"`{focus}`에서 사람이 반복 판단하는 부분만 떼어내면 어떤 스크립트나 Add-in 후보가 되는가?")
    if "품질" in cats:
        questions.append(f"납품 전 품질 기준으로 바꾼다면 `{focus}`는 합격/불합격 조건을 어떻게 가져야 하는가?")
    if "지식공백" in cats:
        questions.append(f"`{focus}`의 미검증 부분은 공식 문서, 프로젝트 사례, 담당자 경험 중 무엇으로 먼저 막아야 하는가?")
    if "사업화" in cats:
        questions.append(f"고객에게 설명할 때 `{focus}`는 시간 절감, 품질 안정, 리스크 감소 중 어디에 가장 가깝나?")
    if len(questions) < 3:
        questions.append(f"`{focus}`와 연결할 기존 노트가 없다면 새 표준문서, QA, 백로그 중 어디에 임시 보관해야 하는가?")
    return questions[:4]


def question_intent(question: str) -> str:
    if "재현 조건" in question or "확인할 근거" in question:
        return "evidence"
    if "스크립트" in question or "Add-in" in question:
        return "automation"
    if "합격/불합격" in question or "품질 기준" in question:
        return "quality_rule"
    if "공식 문서" in question or "미검증" in question:
        return "verification"
    if "고객에게 설명" in question or "시간 절감" in question:
        return "business_language"
    if "임시 보관" in question or "표준문서" in question:
        return "knowledge_placement"
    return "general"


def question_key(question: str) -> str:
    normalized = re.sub(r"\W+", "", question.lower())
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:16]


def question_tokens(question: str) -> set[str]:
    cleaned = re.sub(r"`[^`]+`", " SIGNALFOCUS ", question)
    return {
        token.lower()
        for token in re.findall(r"[A-Za-z0-9가-힣]+", cleaned)
        if len(token) > 1
    }


def jaccard_similarity(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def load_historical_questions() -> list[str]:
    questions: list[str] = []
    if QUESTION_HISTORY_FILE.exists():
        try:
            data = json.loads(QUESTION_HISTORY_FILE.read_text(encoding="utf-8"))
            for item in data.get("questions", []):
                text = str(item.get("question", "")).strip()
                if text:
                    questions.append(text)
        except (OSError, json.JSONDecodeError):
            pass
    for path in REPORT_DIR.glob("**/*_LUA_REASONING_TRAINING_DIGEST.md"):
        if "/feedback/" in path.as_posix():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for block in re.finditer(r"### 스스로 던질 질문\n(?P<body>.*?)(?:\n### |\n## |\Z)", text, flags=re.DOTALL):
            for line in block.group("body").splitlines():
                match = re.match(r"\s*-\s+(.+)", line)
                if match:
                    questions.append(match.group(1).strip())
    seen: set[str] = set()
    unique: list[str] = []
    for question in questions:
        key = question_key(question)
        if key in seen:
            continue
        seen.add(key)
        unique.append(question)
    return unique


def candidate_questions(signals: list[Signal]) -> list[str]:
    questions: list[str] = []
    seen: set[str] = set()
    for signal in signals:
        for question in self_questions(signal):
            key = question_key(question)
            if key in seen:
                continue
            seen.add(key)
            questions.append(question)
    return questions


def question_novelty_score(questions: list[str], historical: list[str]) -> tuple[float, str]:
    if not questions:
        return 0.0, "no_candidate_questions"
    if not historical:
        return 1.0, "no_question_history"
    historical_tokens = [question_tokens(question) for question in historical]
    novelty_scores: list[float] = []
    repeated_intents = 0
    historical_intents = {question_intent(question) for question in historical[-80:]}
    for question in questions:
        tokens = question_tokens(question)
        max_similarity = max((jaccard_similarity(tokens, hist) for hist in historical_tokens), default=0.0)
        novelty_scores.append(1.0 - max_similarity)
        if question_intent(question) in historical_intents:
            repeated_intents += 1
    avg_novelty = sum(novelty_scores) / len(novelty_scores)
    intent_penalty = min(repeated_intents / max(len(questions), 1), 1.0) * 0.12
    score = max(avg_novelty - intent_penalty, 0.0)
    reason = f"question_novelty={score:.2f} avg={avg_novelty:.2f} repeated_intents={repeated_intents}/{len(questions)}"
    return score, reason


def should_spend_deepseek_for_questions(signals: list[Signal]) -> tuple[bool, str]:
    questions = candidate_questions(signals)
    historical = load_historical_questions()
    score, reason = question_novelty_score(questions, historical)
    threshold = float(os.environ.get("REASONING_MIN_DEEPSEEK_QUESTION_NOVELTY", str(MIN_DEEPSEEK_QUESTION_NOVELTY)))
    if score < threshold:
        return False, f"low_question_novelty {reason} threshold={threshold:.2f}"
    unique_intents = {question_intent(question) for question in questions}
    if len(unique_intents) < 2:
        return False, f"low_question_diversity intents={','.join(sorted(unique_intents)) or 'none'}"
    return True, reason


def save_question_history(report_path: Path, signals: list[Signal], novelty_reason: str) -> None:
    existing: list[dict] = []
    if QUESTION_HISTORY_FILE.exists():
        try:
            data = json.loads(QUESTION_HISTORY_FILE.read_text(encoding="utf-8"))
            existing = list(data.get("questions", []))
        except (OSError, json.JSONDecodeError):
            existing = []
    existing_keys = {str(item.get("key", "")) for item in existing}
    now = dt.datetime.now().isoformat(timespec="seconds")
    for signal in signals:
        for question in self_questions(signal):
            key = question_key(question)
            if key in existing_keys:
                continue
            existing_keys.add(key)
            existing.append({
                "key": key,
                "question": question,
                "intent": question_intent(question),
                "signal": signal.semantic_fingerprint,
                "source": signal.path.relative_to(PROJECT_ROOT).as_posix(),
                "report": report_path.relative_to(PROJECT_ROOT).as_posix(),
                "novelty_reason": novelty_reason,
                "created_at": now,
            })
    QUESTION_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUESTION_HISTORY_FILE.write_text(
        json.dumps({"version": 1, "questions": existing[-500:]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


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

### 대표 대리 첨언 처리
- DeepSeek 대표 대리 첨언관이 실무 예외, 고객 설명 언어, 자동 해소 판정을 보강한다.
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
3. DeepSeek 대표 대리 첨언관이 실무 예외와 자동 해소 판정을 보강한다.
4. 필요할 때만 대표가 직접 보정하고, 첨언을 Obsidian 지식, QA, 체크리스트, 자동화 후보로 승격한다.
"""

    telegram = format_telegram(now, signals)
    return content, telegram


def current_budget_month() -> str:
    return dt.datetime.now().strftime("%Y-%m")


def load_deepseek_budget_registry() -> dict:
    if not DEEPSEEK_BUDGET_FILE.exists():
        return {"monthly_budget_usd": float(os.environ.get("DEEPSEEK_MONTHLY_BUDGET_USD", "50")), "months": {}}
    try:
        registry = json.loads(DEEPSEEK_BUDGET_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        registry = {"months": {}}
    registry.setdefault("monthly_budget_usd", float(os.environ.get("DEEPSEEK_MONTHLY_BUDGET_USD", "50")))
    registry.setdefault("months", {})
    return registry


def deepseek_budget_remaining() -> float:
    registry = load_deepseek_budget_registry()
    month_data = registry.get("months", {}).get(current_budget_month(), {})
    used = float(month_data.get("estimated_spend_usd", 0.0))
    budget = float(registry.get("monthly_budget_usd", 50.0))
    return round(max(budget - used, 0.0), 4)


def can_use_deepseek_budget() -> bool:
    estimated = float(os.environ.get("DEEPSEEK_ESTIMATED_CALL_COST_USD", str(DEEPSEEK_ESTIMATED_CALL_COST_USD)))
    return deepseek_budget_remaining() >= estimated


def record_deepseek_budget_use(workflow_id: str, target_agent: str) -> None:
    estimated = round(float(os.environ.get("DEEPSEEK_ESTIMATED_CALL_COST_USD", str(DEEPSEEK_ESTIMATED_CALL_COST_USD))), 4)
    registry = load_deepseek_budget_registry()
    month = current_budget_month()
    month_data = registry.setdefault("months", {}).setdefault(month, {"estimated_spend_usd": 0.0, "calls": []})
    month_data["estimated_spend_usd"] = round(float(month_data.get("estimated_spend_usd", 0.0)) + estimated, 4)
    month_data.setdefault("calls", []).append({
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "workflow_id": workflow_id,
        "target_agent": target_agent,
        "estimated_cost_usd": estimated,
    })
    DEEPSEEK_BUDGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    DEEPSEEK_BUDGET_FILE.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def deepseek_enabled_for_delegate() -> bool:
    if os.environ.get("REASONING_DELEGATE_REVIEW_ENABLED", "true").lower() not in {"1", "true", "yes", "on"}:
        return False
    if os.environ.get("PAID_AI_ENABLED", "false").lower() not in {"1", "true", "yes", "on"}:
        return False
    key = os.environ.get("DEEPSEEK_API_KEY", "")
    return bool(key and key != "sk-fake-key-for-test" and can_use_deepseek_budget())


def deepseek_delegate_model(text: str = "") -> str:
    lowered = text.lower()
    high_enabled = os.environ.get("DEEPSEEK_HIGH_STAKES_REVIEW_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
    if high_enabled and any(keyword in lowered for keyword in ["가격", "투자", "손익분기", "mrr", "arr", "스토어", "로드맵", "상품화"]):
        return os.environ.get("DEEPSEEK_HIGH_STAKES_MODEL", "deepseek-v4-pro")
    return os.environ.get("DEEPSEEK_FINAL_REVIEW_MODEL", "deepseek-v4-flash")


def build_delegate_prompt(report_text: str, signals: list[Signal]) -> str:
    signal_lines = "\n".join(
        f"- {', '.join(signal.categories)} | {signal.path.relative_to(PROJECT_ROOT).as_posix()} | {sanitize_for_markdown(signal.line)}"
        for signal in signals[:3]
    )
    return (
        "당신은 LUA BIM LABS 대표의 추론 첨언 대리자입니다.\n"
        "목표는 대표가 매번 직접 답장하지 않아도 추론 훈련 루프가 현실적인 실무 판단으로 보정되게 하는 것입니다.\n\n"
        "역할 원칙:\n"
        "- 대표의 확정 의사결정을 가장하지 말고, '대표 대리 첨언 초안'으로 작성합니다.\n"
        "- 현장 BIM 실무, 상품화, 교육/온보딩, 자동화 승격 관점에서 빠진 조건을 보강합니다.\n"
        "- 같은 질문을 반복하지 말고, 이번 후보를 archive/merge/promote/send 중 하나로 판정합니다.\n"
        "- 민감정보, 고객명, 프로젝트명, 내부 경로를 추정하거나 복원하지 않습니다.\n\n"
        "출력 형식:\n"
        "## 대표 대리 추론 첨언\n"
        "### 대리 판단\n"
        "- ...\n"
        "### 보강할 현실 조건\n"
        "- ...\n"
        "### 자동 해소 판정\n"
        "- Decision: archive | merge | promote | send\n"
        "- Reason: ...\n"
        "### 다음 지식화 액션\n"
        "- ...\n\n"
        "후보 신호:\n"
        f"{signal_lines}\n\n"
        "다이제스트:\n"
        f"{sanitize_for_markdown(report_text[-7000:])}"
    )


def call_deepseek_delegate(report_text: str, signals: list[Signal]) -> tuple[str, str]:
    if not signals:
        return "", "no_signals"
    should_spend, novelty_reason = should_spend_deepseek_for_questions(signals)
    if not should_spend:
        return "", novelty_reason
    if not deepseek_enabled_for_delegate():
        return "", "disabled_or_budget_or_key"
    prompt = build_delegate_prompt(report_text, signals)
    model = deepseek_delegate_model(prompt)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "당신은 LUA BIM LABS의 대표 대리 추론 첨언관입니다. "
                    "한국어로 간결하게, 실행 가능한 판단과 자동 해소 판정을 작성합니다."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 1600,
        "temperature": 0.2,
    }
    request = urllib.request.Request(
        DEEPSEEK_API_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - daily routine should continue without paid review.
        return "", f"failed:{type(exc).__name__}"
    content = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
    review = sanitize_for_markdown(content.strip())[:4000]
    if review:
        record_deepseek_budget_use("reasoning_training_delegate_annotation", "대표_대리_추론첨언")
    return review, model if review else "empty_response"


def sanitize_for_markdown(text: str) -> str:
    text = re.sub(r"/Users/[^\s`]+", "[LOCAL_PATH_REDACTED]", text)
    text = re.sub(r"api[_ -]?key\s*[:=]\s*\S+", "api_key=[REDACTED]", text, flags=re.IGNORECASE)
    text = re.sub(r"token\s*[:=]\s*\S+", "token=[REDACTED]", text, flags=re.IGNORECASE)
    text = re.sub(r"secret\s*[:=]\s*\S+", "secret=[REDACTED]", text, flags=re.IGNORECASE)
    text = re.sub(r"password\s*[:=]\s*\S+", "password=[REDACTED]", text, flags=re.IGNORECASE)
    return text


def append_delegate_annotation(report_path: Path, delegate_review: str, model_or_reason: str) -> str:
    now = dt.datetime.now()
    if delegate_review:
        block = (
            f"\n\n## 대표 대리 추론 첨언 ({now.strftime('%Y-%m-%d %H:%M:%S')})\n\n"
            f"- Source: DeepSeek API\n"
            f"- Model: {sanitize_for_markdown(model_or_reason)}\n"
            "- Role: 대표 대리 첨언 초안\n\n"
            f"{delegate_review}\n"
        )
        kb_body = delegate_review
    else:
        block = (
            f"\n\n## 대표 대리 추론 첨언 스킵 ({now.strftime('%Y-%m-%d %H:%M:%S')})\n\n"
            f"- Reason: {sanitize_for_markdown(model_or_reason)}\n"
        )
        kb_body = f"스킵: {sanitize_for_markdown(model_or_reason)}"
    with report_path.open("a", encoding="utf-8") as handle:
        handle.write(block)
    KB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not KB_FILE.exists():
        KB_FILE.write_text("# 추론훈련루프 지식 베이스\n\n", encoding="utf-8")
    with KB_FILE.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n\n## {now.isoformat(timespec='seconds')} 대표 대리 추론 첨언\n"
            f"- Source: `{report_path.relative_to(PROJECT_ROOT).as_posix()}`\n"
            f"- Model/Reason: {sanitize_for_markdown(model_or_reason)}\n"
            "- Tags: reasoning-training,delegate-annotation,deepseek\n\n"
            f"{kb_body}\n"
        )
    return block


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
            "대표 대리 첨언: DeepSeek가 실무 예외, 고객 설명 언어, 자동 해소 판정을 보강합니다.",
            "직접 보정이 필요한 경우에만 이 메시지에 답장해주세요.",
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
    seen = set() if include_seen else load_seen()
    signals = collect_signals(days, limit * 25, seen=seen)
    if not include_seen:
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
    delegate_review, delegate_model_or_reason = call_deepseek_delegate(content, signals)
    save_question_history(report_path, signals, delegate_model_or_reason)
    delegate_block = append_delegate_annotation(report_path, delegate_review, delegate_model_or_reason)
    if send and signals:
        telegram_with_context = (
            f"{telegram}\n\n"
            f"기록: {report_path.relative_to(PROJECT_ROOT).as_posix()}\n"
            f"대표 대리 첨언: {'완료' if delegate_review else '스킵'} ({delegate_model_or_reason})\n"
            "필요할 때만 이 메시지에 답장하면 대표 직접 보정으로 추가 저장됩니다."
        )
        send_telegram(telegram_with_context)
    elif send:
        print("telegram=skipped reason=no_new_reasoning_signals")
    print(f"reasoning_training_digest={report_path}")
    print(f"signals={len(signals)}")
    print(f"delegate_annotation={'done' if delegate_review else 'skipped'} reason_or_model={delegate_model_or_reason}")
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

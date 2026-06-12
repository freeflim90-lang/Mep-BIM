from __future__ import annotations

import datetime
import re
from pathlib import Path

from telegram import Update

from backend.core.paths import DATA_DIR, PROJECT_ROOT
from backend.text_utils import sanitize_outbound_text, telegram_user_label


REASONING_KB_FILE = DATA_DIR / "knowledge_base" / "추론훈련루프.md"
REASONING_DIR = PROJECT_ROOT / "docs" / "reasoning_training"
FEEDBACK_DIR = PROJECT_ROOT / "docs" / "reasoning_training" / "feedback"

SENSITIVE_PATTERNS = [
    r"api[_ -]?key",
    r"token",
    r"secret",
    r"password",
    r"\.env",
    r"/Users/[^\\s]+",
    r"010[-\s]?\d{4}[-\s]?\d{4}",
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    r"주민",
    r"계약",
    r"고객명",
    r"프로젝트명",
    r"도면",
]


def _reply_text(update: Update) -> str:
    message = update.message
    if not message or not message.reply_to_message:
        return ""
    return message.reply_to_message.text or message.reply_to_message.caption or ""


def is_reasoning_digest_reply(update: Update) -> bool:
    text = _reply_text(update)
    if not text:
        return False
    return "[LUA BIM LABS 추론 훈련]" in text or "reasoning-training-digest" in text or "추론 훈련 다이제스트" in text


def extract_report_path_from_reply(update: Update) -> Path | None:
    text = _reply_text(update)
    match = re.search(r"기록:\s*`?([^\n`]+)`?", text)
    if not match:
        return None
    raw_path = match.group(1).strip()
    path = PROJECT_ROOT / raw_path
    try:
        path.relative_to(PROJECT_ROOT)
    except ValueError:
        return None
    return path if path.exists() and path.is_file() else None


def latest_reasoning_digest_path() -> Path | None:
    if not REASONING_DIR.exists():
        return None
    candidates = sorted(
        (
            path
            for path in REASONING_DIR.glob("**/*_LUA_REASONING_TRAINING_DIGEST.md")
            if path.is_file()
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def _keyword_hits(text: str, keywords: list[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def build_reasoning_conclusion(feedback: str, report_path: Path | None = None) -> str:
    """Turn field feedback into the next thinking rule for the reasoning loop."""
    safe_feedback = sanitize_outbound_text(feedback.strip())
    themes: list[str] = []
    thinking_rules: list[str] = []
    next_actions: list[str] = []

    if _keyword_hits(safe_feedback, ["상품화", "수익", "스타트업", "자원", "투자", "멀티플", "개발"]):
        themes.append("상품화는 기술 가능성보다 조직의 자원 배분 구조와 기존 수익사업의 안정성에 크게 좌우된다.")
        thinking_rules.append("앞으로 자동화/품질 아이디어를 볼 때 `기술로 만들 수 있는가`보다 먼저 `누가 예산과 시간을 배정할 수 있는가`를 질문한다.")
        next_actions.append("후보마다 개발 난이도, 현업 협업 필요도, 기존 수익사업과의 충돌 여부를 함께 기록한다.")
    if _keyword_hits(safe_feedback, ["교육", "온보딩", "양성", "starter", "전문가", "직원"]):
        themes.append("MEP BIM 전문가는 시장에서 필요하지만, 실제 온보딩 가능한 교육 구조는 부족하다.")
        thinking_rules.append("앞으로 교육 후보를 볼 때 `지식을 설명하는가`가 아니라 `신입/초기 실무자가 다음날 업무에 적용할 수 있는가`를 기준으로 판단한다.")
        next_actions.append("Starter 상품은 실무 갈증, 온보딩 공백, 반복 질문을 연결하는 핵심 상품군으로 별도 추적한다.")
    if _keyword_hits(safe_feedback, ["실무", "현업", "bim engineer", "엔지니어", "협업"]):
        themes.append("실무자는 당장 납품과 모델 품질을 해결해야 하므로, 상품화 관점까지 동시에 가지기 어렵다.")
        thinking_rules.append("앞으로 현업 경험을 받을 때 `실무자의 당장 문제`와 `LUA BIM LABS의 상품화 기회`를 분리해서 본 뒤 다시 연결한다.")
        next_actions.append("실무 첨언에서 반복 업무, 판단 기준, 교육 공백, 자동화 가능 지점을 따로 추출한다.")

    if not themes:
        themes.append("대표의 실무 첨언은 기존 1차 추론의 현실 조건을 보정하는 근거다.")
        thinking_rules.append("앞으로 결론을 확정하기 전에 실무 예외, 시장 조건, 조직 실행 가능성을 한 번 더 질문한다.")
        next_actions.append("첨언을 QA, 체크리스트, 교육자료, 자동화 백로그 중 어디로 승격할지 검토한다.")

    digest_line = ""
    if report_path:
        digest_line = f"\n- 연결 다이제스트: `{report_path.relative_to(PROJECT_ROOT).as_posix()}`"

    return (
        "## 추론 결론\n\n"
        "### 실무 첨언에서 업데이트된 판단\n"
        + "\n".join(f"- {theme}" for theme in themes[:3])
        + "\n\n### 앞으로의 사고 방식\n"
        + "\n".join(f"- {rule}" for rule in thinking_rules[:3])
        + "\n\n### 다음 지식화 액션\n"
        + "\n".join(f"- {action}" for action in next_actions[:3])
        + digest_line
    )


def has_sensitive_external_review_risk(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in SENSITIVE_PATTERNS)


def redact_for_external_review(text: str) -> str:
    safe = sanitize_outbound_text(text)
    safe = re.sub(r"api[_ -]?key\s*[:=]\s*\S+", "api_key=[REDACTED]", safe, flags=re.IGNORECASE)
    safe = re.sub(r"token\s*[:=]\s*\S+", "token=[REDACTED]", safe, flags=re.IGNORECASE)
    safe = re.sub(r"secret\s*[:=]\s*\S+", "secret=[REDACTED]", safe, flags=re.IGNORECASE)
    safe = re.sub(r"password\s*[:=]\s*\S+", "password=[REDACTED]", safe, flags=re.IGNORECASE)
    safe = re.sub(r"/Users/[^\s`]+", "[LOCAL_PATH_REDACTED]", safe)
    safe = re.sub(r"010[-\s]?\d{4}[-\s]?\d{4}", "[PHONE_REDACTED]", safe)
    safe = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[EMAIL_REDACTED]", safe)
    return safe[:12000]


def build_deepseek_final_review_prompt(*, feedback: str, conclusion: str, digest_text: str = "") -> str:
    return (
        "LUA BIM LABS 추론 트레이닝의 최종 검토를 수행하세요.\n\n"
        "역할:\n"
        "- 당신은 답변 생성자가 아니라 최종 검토자입니다.\n"
        "- 내부 결론을 무조건 확정하지 말고, 논리 허점과 실행 리스크를 찾습니다.\n"
        "- 민감정보, 고객명, 프로젝트명, 내부 경로를 추정하거나 복원하지 않습니다.\n\n"
        "검토 기준:\n"
        "1. 대표 실무 첨언이 기존 추론을 어떻게 보정하는가?\n"
        "2. 상품화/교육/자동화 관점에서 빠진 질문은 무엇인가?\n"
        "3. 현업 BIM Engineer가 실제로 실행하기 어려운 지점은 무엇인가?\n"
        "4. LUA BIM LABS가 다음 루프에서 어떤 사고 원칙을 적용해야 하는가?\n\n"
        "출력 형식:\n"
        "## DeepSeek 최종 검토\n"
        "### 보강된 판단\n"
        "- ...\n"
        "### 남은 리스크\n"
        "- ...\n"
        "### 다음 질문\n"
        "- ...\n"
        "### 최종 사고 원칙\n"
        "- ...\n\n"
        "최근 다이제스트 요약:\n"
        f"{redact_for_external_review(digest_text[-6000:])}\n\n"
        "대표 실무 첨언:\n"
        f"{redact_for_external_review(feedback)}\n\n"
        "로컬 추론 결론:\n"
        f"{redact_for_external_review(conclusion)}"
    )


def append_deepseek_final_review(feedback_path: Path, review: str, *, model: str, skipped_reason: str = "") -> str:
    now = datetime.datetime.now()
    safe_review = sanitize_outbound_text(review.strip())
    if skipped_reason:
        block = (
            f"\n\n## DeepSeek 최종 검토 스킵 ({now.strftime('%Y-%m-%d %H:%M:%S')})\n\n"
            f"- Reason: {sanitize_outbound_text(skipped_reason)}\n"
        )
    else:
        block = (
            f"\n\n## DeepSeek 최종 검토 ({now.strftime('%Y-%m-%d %H:%M:%S')})\n\n"
            f"- Model: {sanitize_outbound_text(model)}\n\n"
            f"{safe_review}\n"
        )
    with feedback_path.open("a", encoding="utf-8") as handle:
        handle.write(block)
    with REASONING_KB_FILE.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n\n## {now.isoformat(timespec='seconds')} DeepSeek 최종 검토\n"
            f"- Source: `{feedback_path.relative_to(PROJECT_ROOT).as_posix()}`\n"
            f"- Model: {sanitize_outbound_text(model) if model else 'skipped'}\n\n"
            f"{safe_review if safe_review else '스킵: ' + sanitize_outbound_text(skipped_reason)}\n"
        )
    return safe_review if safe_review else f"DeepSeek 최종 검토 스킵: {skipped_reason}"


def append_reasoning_feedback(update: Update, feedback: str) -> tuple[Path, str]:
    now = datetime.datetime.now()
    safe_feedback = sanitize_outbound_text(feedback.strip())
    requester = sanitize_outbound_text(telegram_user_label(update))
    chat_id = update.effective_chat.id if update.effective_chat else "-"
    report_path = extract_report_path_from_reply(update) or latest_reasoning_digest_path()
    conclusion = build_reasoning_conclusion(safe_feedback, report_path)

    block = (
        f"\n\n## 대표 실무 첨언 ({now.strftime('%Y-%m-%d %H:%M:%S')})\n\n"
        f"- Source: Telegram reply\n"
        f"- Requester: {requester}\n"
        f"- Chat ID: {chat_id}\n\n"
        f"{safe_feedback}\n\n"
        f"{conclusion}\n"
    )

    if report_path:
        with report_path.open("a", encoding="utf-8") as handle:
            handle.write(block)

    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    feedback_path = FEEDBACK_DIR / f"{now.strftime('%Y%m%d-%H%M%S')}_reasoning_feedback.md"
    source_line = report_path.relative_to(PROJECT_ROOT).as_posix() if report_path else "unmatched-reasoning-digest"
    feedback_path.write_text(
        f"""---
type: reasoning-training-feedback
date: {now.strftime('%Y-%m-%d')}
status: captured
tags:
  - reasoning-training
  - telegram-feedback
  - field-knowledge
---

# {now.strftime('%Y-%m-%d %H:%M')} 추론 첨언

- Source digest: `{source_line}`
- Requester: {requester}
- Chat ID: {chat_id}

## 첨언

{safe_feedback}

{conclusion}

## 후속 지식화

- [ ] 원 추론 후보와 연결한다.
- [ ] 실무 예외 조건을 추출한다.
- [ ] QA, 체크리스트, 교육자료, 자동화 백로그 중 승격 대상을 정한다.
""",
        encoding="utf-8",
    )

    REASONING_KB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not REASONING_KB_FILE.exists():
        REASONING_KB_FILE.write_text(
            "# 추론훈련루프 지식 베이스\n\n"
            "LUA BIM LABS가 문제 신호를 스스로 질문하고 추론하며, 대표의 실무 첨언으로 지식을 깊고 넓게 확장하는 루프를 기록한다.\n",
            encoding="utf-8",
        )
    with REASONING_KB_FILE.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n\n## {now.isoformat(timespec='seconds')} 대표 실무 첨언 수집\n"
            f"- Source: `{feedback_path.relative_to(PROJECT_ROOT).as_posix()}`\n"
            f"- Digest: `{source_line}`\n"
            "- Tags: reasoning-training,telegram-feedback,field-knowledge\n\n"
            "운영 판단: 이 첨언은 다음 추론 훈련에서 실무 예외 조건, 고객 설명 언어, 자동화/체크리스트 승격 후보로 재검토한다.\n\n"
            f"{conclusion}\n"
        )
    telegram_conclusion = conclusion.replace("## 추론 결론\n\n", "").replace("### ", "")
    return feedback_path, telegram_conclusion

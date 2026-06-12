"""
C-suite 자율 경영 레이어
  - CEO · COO · CFO 3인이 요청을 심의하고 결정
  - 비용/예산이 수반되는 결정만 소유주 승인 요청 (Telegram)
  - 나머지 결정은 C-suite가 자율 집행하고 결과만 보고
"""
from __future__ import annotations

import asyncio
import datetime
import json
import os
from pathlib import Path

from backend.core.paths import DATA_DIR, PROJECT_ROOT

_CSUITE_LOG_FILE = DATA_DIR / "team_requests" / "csuite_decisions.json"

CSUITE_AGENTS = ["CEO", "COO", "CFO"]

COST_KEYWORDS = [
    "비용", "예산", "구매", "계약", "외주", "채용", "투자", "지출",
    "결제", "월급", "급여", "수수료", "라이선스 구매", "서버 비용",
    "인력 충원", "구독 결제", "예산 집행", "비용 승인", "견적",
    "cost", "budget", "payment", "invoice", "salary", "contract", "purchase",
]

CSUITE_RESPONSIBILITY = {
    "CEO": {
        "role": "제품 방향·브랜드·우선순위 결정. 3개 이상 후보 중 최종 1개를 선택한다.",
        "question": "이 요청이 회사 방향과 일치하는가? 실행 우선순위는?",
    },
    "COO": {
        "role": "운영·일정·팀 자원 배분 결정. 실행 가능성과 병목을 판단한다.",
        "question": "현재 팀 자원으로 실행 가능한가? 병목과 선행 조건은?",
    },
    "CFO": {
        "role": "비용·수익성·손익 판단. 예산 수반 여부를 명시하고 규모를 추정한다.",
        "question": "예산이 필요한가? 규모는? ROI 판단 기준은?",
    },
}


# ---------------------------------------------------------------------------
# 비용 결정 여부 판단
# ---------------------------------------------------------------------------

def is_cost_decision(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in COST_KEYWORDS)


# ---------------------------------------------------------------------------
# 각 C-레벨 의견 생성 (지식 기반, 로컬 처리)
# ---------------------------------------------------------------------------

def _build_agent_opinion(agent: str, user_text: str, knowledge: str) -> str:
    info = CSUITE_RESPONSIBILITY[agent]
    basis = knowledge[-800:] if knowledge else "역할 원칙 기준"
    return (
        f"[{agent}] 심의 의견\n"
        f"- 역할: {info['role']}\n"
        f"- 검토 질문: {info['question']}\n"
        f"- 근거: {basis}\n"
        f"- 판단: 요청 내용 '{user_text[:120]}' 에 대해 역할 범위 내 검토 완료."
    )


# ---------------------------------------------------------------------------
# C-suite 심의 실행
# ---------------------------------------------------------------------------

def csuite_deliberate(user_text: str) -> dict:
    from backend.agent_routing import read_agent_knowledge

    opinions: dict[str, str] = {}
    for agent in CSUITE_AGENTS:
        knowledge = read_agent_knowledge(agent, max_chars=1200)
        opinions[agent] = _build_agent_opinion(agent, user_text, knowledge)

    cost_flag = is_cost_decision(user_text)
    now = datetime.datetime.now().isoformat(timespec="seconds")

    decision = {
        "id": _next_decision_id(now),
        "created_at": now,
        "request": user_text[:300],
        "opinions": opinions,
        "deepseek_synthesis": "",
        "requires_owner_approval": cost_flag,
        "status": "pending_owner_approval" if cost_flag else "approved_by_csuite",
        "approved_by": "" if cost_flag else "C-suite (CEO·COO·CFO)",
        "owner_approved_at": "",
        "owner_rejected_at": "",
        "rejection_reason": "",
    }
    _record_decision(decision)
    return decision


async def csuite_deliberate_with_deepseek(user_text: str) -> dict:
    """C-suite 3인 로컬 심의 후 DeepSeek이 최종 결정문을 합성한다."""
    decision = csuite_deliberate(user_text)

    try:
        from backend.ai_pipeline import can_use_deepseek_budget, record_deepseek_budget_use
        import backend.server_total as st

        if not can_use_deepseek_budget():
            decision["deepseek_synthesis"] = "DeepSeek 예산 소진 — 로컬 심의 결과로 대체"
            return decision

        if not st.DEEPSEEK_API_KEY or st.DEEPSEEK_API_KEY == "sk-fake-key-for-test":
            decision["deepseek_synthesis"] = "DEEPSEEK_API_KEY 미설정 — 로컬 심의 결과로 대체"
            return decision

        opinions_block = "\n\n".join(
            f"[{agent} 의견]\n{op}" for agent, op in decision["opinions"].items()
        )
        synthesis_prompt = (
            "다음은 LUA BIM LABS C-suite (CEO·COO·CFO) 3인의 심의 의견입니다.\n\n"
            f"{opinions_block}\n\n"
            f"요청 원문: {user_text[:400]}\n\n"
            "위 의견을 종합하여 최종 결정문을 작성하세요.\n"
            "형식:\n"
            "1. 결정 요약 (1문장)\n"
            "2. 집행 항목 (불릿, 3개 이하)\n"
            "3. 보류·에스컬레이션 항목 (없으면 '없음')\n"
            "4. 소유주 보고 필요 여부: 비용 수반 시 '예 — 승인 요청 발송', 아니면 '아니오'"
        )

        response = await st.deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "당신은 LUA BIM LABS의 C-suite 결정 합성 AI입니다. "
                        "CEO·COO·CFO 의견을 종합해 간결하고 실행 가능한 결정문을 작성합니다. "
                        "모든 응답은 한국어로 작성하세요."
                    ),
                },
                {"role": "user", "content": synthesis_prompt},
            ],
            stream=False,
        )

        synthesis = response.choices[0].message.content or ""
        decision["deepseek_synthesis"] = synthesis
        record_deepseek_budget_use(workflow_id="csuite_deliberation", target_agent="CEO")

        log = _load_log()
        for item in log.get("decisions", []):
            if item.get("id") == decision["id"]:
                item["deepseek_synthesis"] = synthesis
                break
        _save_log(log)

    except Exception as exc:
        decision["deepseek_synthesis"] = f"DeepSeek 합성 실패: {exc}"

    return decision


# ---------------------------------------------------------------------------
# 결정 로그
# ---------------------------------------------------------------------------

def _load_log() -> dict:
    if not _CSUITE_LOG_FILE.exists():
        return {"decisions": []}
    try:
        return json.loads(_CSUITE_LOG_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"decisions": []}


def _next_decision_id(now: str) -> str:
    date_part = now[:10].replace("-", "")
    log = _load_log()
    prefix = f"CSUITE-{date_part}-"
    numbers = []
    for item in log.get("decisions", []):
        did = item.get("id", "")
        if did.startswith(prefix):
            try:
                numbers.append(int(did.rsplit("-", 1)[-1]))
            except ValueError:
                pass
    return f"{prefix}{max(numbers, default=0) + 1:03d}"


def _record_decision(decision: dict) -> None:
    _CSUITE_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    log = _load_log()
    log.setdefault("decisions", []).append(decision)
    _CSUITE_LOG_FILE.write_text(
        json.dumps(log, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# 소유주 승인 요청 (비용 결정 시)
# ---------------------------------------------------------------------------

def _approval_text(decision: dict) -> str:
    opinions_text = "\n\n".join(
        f"{agent}:\n{opinion}" for agent, opinion in decision["opinions"].items()
    )
    return (
        "💰 [C-suite 비용 결정 — 소유주 승인 필요]\n\n"
        f"결정 ID: {decision['id']}\n"
        f"요청 내용:\n{decision['request']}\n\n"
        f"C-suite 심의 결과:\n{opinions_text}\n\n"
        f"승인: /csuite_approve {decision['id']}\n"
        f"반려: /csuite_reject {decision['id']} 사유"
    )


async def notify_owner_cost_approval(decision: dict) -> None:
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not telegram_chat_id:
        print(f"⚠️ [C-suite] TELEGRAM_CHAT_ID 없음: {decision['id']}")
        return
    try:
        import backend.server_total as st
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        tg_app = getattr(getattr(st.app, "state", None), "tg_app", None)
        if not tg_app:
            print(f"⚠️ [C-suite] tg_app 없음: {decision['id']}")
            return

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ 승인", callback_data=f"csuite_approve:{decision['id']}"),
                InlineKeyboardButton("🚫 반려", callback_data=f"csuite_reason_select:{decision['id']}"),
            ]
        ])
        await tg_app.bot.send_message(
            chat_id=telegram_chat_id,
            text=_approval_text(decision),
            reply_markup=keyboard,
        )
    except Exception as exc:
        print(f"⚠️ [C-suite notify] {exc}")


# ---------------------------------------------------------------------------
# 소유주 승인/반려 처리
# ---------------------------------------------------------------------------

def find_decision(decision_id: str) -> tuple[dict, dict | None]:
    log = _load_log()
    for item in log.get("decisions", []):
        if item.get("id") == decision_id:
            return log, item
    return log, None


def _save_log(log: dict) -> None:
    _CSUITE_LOG_FILE.write_text(
        json.dumps(log, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def owner_approve(decision_id: str) -> str:
    log, item = find_decision(decision_id)
    if not item:
        return f"❌ 결정 ID를 찾을 수 없습니다: {decision_id}"
    if item["status"] != "pending_owner_approval":
        return f"⚠️ 이미 처리된 결정입니다: {item['status']}"
    item["status"] = "owner_approved"
    item["owner_approved_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    _save_log(log)
    return f"✅ [{decision_id}] 소유주 승인 완료. C-suite가 집행합니다."


def owner_reject(decision_id: str, reason: str) -> tuple[str, dict | None]:
    """반려 처리 후 (메시지, 결정 항목)을 반환한다. 재심의에 결정 항목이 필요하다."""
    log, item = find_decision(decision_id)
    if not item:
        return f"❌ 결정 ID를 찾을 수 없습니다: {decision_id}", None
    if item["status"] != "pending_owner_approval":
        return f"⚠️ 이미 처리된 결정입니다: {item['status']}", None
    item["status"] = "owner_rejected"
    item["owner_rejected_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    item["rejection_reason"] = reason
    item.setdefault("revised_direction", "")
    _save_log(log)
    return f"🚫 [{decision_id}] 반려 완료. 사유를 바탕으로 C-suite가 방향을 재검토합니다...", item


# ---------------------------------------------------------------------------
# 반려 사유 반영 재심의 (DeepSeek)
# ---------------------------------------------------------------------------

async def redeliberate_after_rejection(decision: dict) -> dict:
    """소유주 반려 사유를 반영해 C-suite가 수정 방향을 도출한다."""
    original_request = decision.get("request", "")
    rejection_reason = decision.get("rejection_reason", "")
    original_opinions = decision.get("opinions", {})
    original_synthesis = decision.get("deepseek_synthesis", "")

    opinions_block = "\n\n".join(
        f"[{agent} 의견]\n{op}" for agent, op in original_opinions.items()
    )

    revised_direction = ""
    try:
        from backend.ai_pipeline import can_use_deepseek_budget, record_deepseek_budget_use
        import backend.server_total as st

        if not can_use_deepseek_budget():
            revised_direction = "DeepSeek 예산 소진 — 로컬 재검토 필요"
        elif not st.DEEPSEEK_API_KEY or st.DEEPSEEK_API_KEY == "sk-fake-key-for-test":
            revised_direction = "DEEPSEEK_API_KEY 미설정 — 로컬 재검토 필요"
        else:
            prompt = (
                "소유주가 C-suite의 결정을 반려했습니다. 반려 사유를 바탕으로 수정 방향을 제시하세요.\n\n"
                f"[원래 요청]\n{original_request}\n\n"
                f"[C-suite 1차 심의]\n{opinions_block}\n\n"
                f"[1차 결정 요약]\n{original_synthesis}\n\n"
                f"[소유주 반려 사유]\n{rejection_reason}\n\n"
                "위 반려 사유를 완전히 수용하여 수정 방향을 작성하세요.\n"
                "형식:\n"
                "1. 반려 사유 핵심 (1문장)\n"
                "2. 수정 방향 (불릿, 3개 이하)\n"
                "3. 재추진 조건 (소유주가 승인할 수 있는 조건)\n"
                "4. 즉시 실행 가능한 대안 (비용 없이 할 수 있는 것, 없으면 '없음')"
            )
            response = await st.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "당신은 LUA BIM LABS C-suite 재심의 AI입니다. "
                            "소유주의 반려 사유를 최우선으로 존중하고, "
                            "실행 가능한 수정 방향을 간결하게 제시합니다. "
                            "모든 응답은 한국어로 작성하세요."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                stream=False,
            )
            revised_direction = response.choices[0].message.content or ""
            record_deepseek_budget_use(
                workflow_id="csuite_rejection_redeliberation",
                target_agent="CEO",
            )
    except Exception as exc:
        revised_direction = f"재심의 실패: {exc}"

    log, item = find_decision(decision["id"])
    if item:
        item["revised_direction"] = revised_direction
        item["status"] = "revised_pending_action"
        _save_log(log)
        decision["revised_direction"] = revised_direction
        decision["status"] = "revised_pending_action"

    return decision


async def notify_owner_revised_direction(decision: dict) -> None:
    """수정 방향을 소유주에게 Telegram으로 보고한다."""
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not telegram_chat_id:
        return
    try:
        import backend.server_total as st
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        tg_app = getattr(getattr(st.app, "state", None), "tg_app", None)
        if not tg_app:
            return

        revised = decision.get("revised_direction", "재심의 결과 없음")
        cost_flag = is_cost_decision(revised)

        text = (
            f"🔄 [C-suite 재심의 결과 — {decision['id']}]\n\n"
            f"반려 사유: {decision.get('rejection_reason', '')}\n\n"
            f"수정 방향:\n{revised}"
        )

        if cost_flag:
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ 수정안 승인", callback_data=f"csuite_approve:{decision['id']}"),
                    InlineKeyboardButton("🚫 재반려", callback_data=f"csuite_reject_start:{decision['id']}"),
                ]
            ])
            text += "\n\n⚠️ 수정안에도 비용이 포함되어 있습니다. 승인 여부를 결정해주세요."
            await tg_app.bot.send_message(chat_id=telegram_chat_id, text=text, reply_markup=keyboard)
        else:
            text += "\n\n✅ 비용 없는 대안으로 C-suite가 즉시 실행합니다."
            await tg_app.bot.send_message(chat_id=telegram_chat_id, text=text)
    except Exception as exc:
        print(f"⚠️ [C-suite revised notify] {exc}")


# ---------------------------------------------------------------------------
# C-suite 보고 텍스트 (비용 불포함 결정 — FYI 보고)
# ---------------------------------------------------------------------------

def csuite_report_text(decision: dict) -> str:
    opinions_text = "\n".join(
        f"• {agent}: {op.split('- 판단:')[-1].strip()[:120]}"
        for agent, op in decision["opinions"].items()
    )
    return (
        f"📋 [C-suite 자율 결정 — FYI]\n"
        f"결정 ID: {decision['id']}\n"
        f"요청: {decision['request'][:150]}\n\n"
        f"C-suite 심의:\n{opinions_text}\n\n"
        f"집행 주체: {decision['approved_by']}"
    )

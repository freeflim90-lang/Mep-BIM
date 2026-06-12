from __future__ import annotations

import asyncio
import datetime as dt
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import backend.local_coder as local_coder
from backend.core.paths import OBSIDIAN_VAULTS_DIR, PROJECT_ROOT
from backend.email_notifications import send_gmail


QUEUE_FILE = PROJECT_ROOT / os.environ.get("QWEN_PRODUCT_DRAFT_QUEUE", "config/qwen_product_draft_queue.json")
DRAFT_DIR = OBSIDIAN_VAULTS_DIR / "model_quality_auditor" / "06_Qwen_Drafts"
INDEX_FILE = DRAFT_DIR / "Qwen Draft Index.md"


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


def safe_filename(text: str) -> str:
    cleaned = re.sub(r"[^\w가-힣\- ]+", " ", text, flags=re.UNICODE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:90] or "Untitled"


def load_queue() -> dict[str, Any]:
    return json.loads(QUEUE_FILE.read_text(encoding="utf-8"))


def state_file() -> Path:
    return DRAFT_DIR / f"{QUEUE_FILE.stem}_state.json"


def load_state() -> dict[str, Any]:
    path = state_file()
    if not path.exists():
        return {"completed": [], "in_progress": None, "last_report": None, "runs": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any]) -> None:
    path = state_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def external_code_only_mode() -> bool:
    return os.environ.get("CODE_DEV_EXTERNAL_ONLY", "true").lower() not in {"0", "false", "no", "off"}


def next_task(queue: dict[str, Any], state: dict[str, Any]) -> dict[str, Any] | None:
    completed = set(state.get("completed", []))
    for task in queue.get("tasks", []):
        if task["id"] not in completed:
            return task
    return None


def source_context(queue: dict[str, Any], max_chars_per_doc: int = 760) -> str:
    chunks = []
    for rel in queue.get("source_documents", []):
        path = PROJECT_ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        chunks.append(f"## SOURCE: {rel}\n{text[:max_chars_per_doc]}")
    return "\n\n".join(chunks)


def build_prompt(queue: dict[str, Any], task: dict[str, Any]) -> str:
    return f"""조직 선정 아이템: {queue['selected_item']}
제품명: {queue['product']}

이번 Qwen 초안 작업:
- Task ID: {task['id']}
- 제목: {task['title']}
- 산출물: {task['deliverable']}
- 범위: {task['scope']}
- 예상 출력 위치: {task['output_path_hint']}

관련 기준 문서 발췌:
{source_context(queue)}

작성 형식:
1. Plan: 목적, 입력, 출력, 제외 범위
2. Draft: 구현 초안. 코드가 필요하면 핵심 dataclass/함수 시그니처 위주로 간결하게 작성하고, Revit API 의존 코드는 인터페이스 또는 의사코드로만 작성
3. Verification: 로컬 검증 방법과 테스트 케이스
4. API 필요성 판단: 외부 API/Revit API/Navisworks API 필요 여부. 필요한 경우 실제 구현 확정은 Revit API 게이트로 넘길 것
5. Next Draft Task: 다음 큐 작업으로 자연스럽게 이어가기 위해 필요한 입력 또는 선행 조건

제약:
- 실제 Revit Document, Element, Transaction 접근 코드를 확정하지 않는다.
- 고객 모델 데이터 외부 전송을 전제로 하지 않는다.
- 선택된 제품의 v1.0 MVP에 맞게 작고 검증 가능한 초안으로 작성한다.
- 경쟁 제품의 이름, UI, 아이콘, 리본 구성, 도움말 문구, 구현 방식을 복제하지 않는다.
- 기능 범위는 내부 참고로만 쓰고 BIM Command Center 고유 명칭과 데이터 계약으로 재정의한다.
- 전체 응답은 완결된 형태로 작성하고, JSON 예시는 짧게 유지한다.
"""


def fallback_draft(task: dict[str, Any], reason: str) -> str:
    return f"""## Plan
Qwen 로컬 실행이 불가능하여 `{task['id']} {task['title']}` 작업을 대기 상태로 기록한다. 입력은 상품 패키지 문서와 Qwen 개발 경계이며, 출력은 `{task['deliverable']}` 초안이다.

## Draft
실제 초안 생성은 `LOCAL_CODER_ENABLED=true` 상태에서 재실행한다. 예상 출력 위치는 `{task['output_path_hint']}`이며, 현재 범위는 `{task['scope']}`로 제한한다.

## Verification
로컬 Qwen 상태, Ollama 모델 가용성, 초안 파일 생성 여부, Obsidian Qwen Draft Index 연결 여부를 확인한다.

## API 필요성 판단
현재 단계에서는 API 필요 없음. Revit API가 필요한 내용은 실제 Revit 환경에서 `Revit API Test Gate Index`로 넘긴다.

## Next Draft Task
Qwen 실행 환경을 활성화한 뒤 동일 Task ID를 다시 실행한다.

실행 불가 사유: {reason}
"""


async def generate_draft(queue: dict[str, Any], task: dict[str, Any]) -> dict[str, Any]:
    status = await local_coder.status()
    if not status.get("enabled"):
        return {
            "ok": False,
            "reason": "LOCAL_CODER_ENABLED=false",
            "response": fallback_draft(task, "LOCAL_CODER_ENABLED=false"),
            "model": status.get("model"),
            "coder_status": status,
        }
    try:
        result = await local_coder.generate(
            build_prompt(queue, task),
            system=(
                "당신은 LUA BIM LABS의 Qwen_Coder_8B 담당자입니다. "
                "조직이 선정한 상용화 아이템을 기준으로 백엔드 개발 초안을 순차 작성합니다. "
                "Revit API 의존 구현은 확정하지 않고, 순수 로직, 데이터 계약, 테스트 가능한 구조를 우선합니다. "
                "경쟁 제품의 표현이나 구현은 복제하지 않고, 기능 범위만 참고하여 고유 기능으로 내재화합니다. "
                "응답은 간결하고 완결되게 작성합니다."
            ),
            temperature=0.15,
            num_predict=760,
            timeout=120,
        )
    except Exception as exc:  # noqa: BLE001 - keep queue recoverable.
        return {
            "ok": False,
            "reason": f"{type(exc).__name__}: {exc}",
            "response": fallback_draft(task, f"{type(exc).__name__}: {exc}"),
            "model": status.get("model"),
            "coder_status": status,
        }
    result["coder_status"] = status
    return result


def write_draft_note(task: dict[str, Any], result: dict[str, Any], persist_draft_body: bool = False) -> Path:
    today = dt.date.today().isoformat()
    draft_id = f"{task['id']}-{today}"
    path = DRAFT_DIR / f"{draft_id} {safe_filename(task['title'])}.md"
    status = "generated" if result.get("ok") else "blocked"
    if persist_draft_body:
        draft_body = result.get("response", "").strip() or "초안 없음"
    else:
        draft_body = (
            "외부 개발 모드(`CODE_DEV_EXTERNAL_ONLY=true`)에 따라 코드 개발 본문은 Mac mini에 저장하지 않는다.\n\n"
            "초안 본문은 Gmail 발송 대상으로만 처리하며, Gmail 설정이 없으면 본문을 폐기하고 재실행해야 한다."
        )
    content = f"""---
type: qwen-product-draft
project: Model Quality Auditor
task_id: {task['id']}
status: {status}
external_code_only: {str(not persist_draft_body).lower()}
created: {today}
tags:
  - qwen
  - mqa
  - backend-draft
  - product-development
---

# {task['id']} {task['title']}

선정 아이템: {load_queue().get('selected_item', '-')}

## 작업 정보

| 항목 | 내용 |
|---|---|
| 산출물 | {task['deliverable']} |
| 범위 | {task['scope']} |
| 예상 출력 위치 | `{task['output_path_hint']}` |
| Qwen 실행 | {'성공' if result.get('ok') else '대기/실패'} |
| 모델 | {result.get('model') or '-'} |
| 사유 | {result.get('reason') or '-'} |

## Qwen 초안

{draft_body}

## 연결

- [[Qwen Draft Index]]
- [[Qwen Development Boundary]]
- [[Revit API Test Gate Index]]
- [[Build Test Index]]
"""
    DRAFT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    update_index(path)
    return path


def update_index(path: Path) -> None:
    title = path.stem
    rel = path.relative_to(DRAFT_DIR).as_posix()
    link = f"- [[{title}]] — `{rel}`"
    text = INDEX_FILE.read_text(encoding="utf-8") if INDEX_FILE.exists() else "# Qwen Draft Index\n"
    if link not in text:
        if "## 생성된 초안" not in text:
            text = text.rstrip() + "\n\n## 생성된 초안\n"
        text = text.rstrip() + "\n" + link + "\n"
        INDEX_FILE.write_text(text, encoding="utf-8")


def telegram_message(queue: dict[str, Any], task: dict[str, Any], note_path: Path, result: dict[str, Any], next_item: dict[str, Any] | None) -> str:
    next_line = f"{next_item['id']} {next_item['title']}" if next_item else "대기 중인 다음 작업 없음"
    preview = " ".join((result.get("response") or "").split())[:850]
    return (
        "[LUA BIM LABS] Qwen 개발 초안 중간보고\n\n"
        f"■ 선정 아이템: {queue['selected_item']}\n"
        f"■ 완료 작업: {task['id']} {task['title']}\n"
        f"■ 상태: {'완료' if result.get('ok') else '대기/확인 필요'}\n"
        f"■ 기록 위치: {note_path.relative_to(PROJECT_ROOT).as_posix()}\n"
        f"■ 다음 초안 업무: {next_line}\n\n"
        f"■ 초안 요약\n{preview}"
    )[:3900]


def gmail_message(queue: dict[str, Any], task: dict[str, Any], note_path: Path, result: dict[str, Any], next_item: dict[str, Any] | None) -> tuple[str, str]:
    next_line = f"{next_item['id']} {next_item['title']}" if next_item else "대기 중인 다음 작업 없음"
    draft_body = result.get("response") or "초안 없음"
    subject = f"[LUA BIM LABS] 코드 개발 초안 보고 - {task['id']} {task['title']}"
    body = (
        "LUA BIM LABS 코드 개발 초안 보고\n\n"
        f"선정 아이템: {queue['selected_item']}\n"
        f"제품: {queue['product']}\n"
        f"완료 작업: {task['id']} {task['title']}\n"
        f"상태: {'완료' if result.get('ok') else '대기/확인 필요'}\n"
        f"기록 위치: {note_path.relative_to(PROJECT_ROOT).as_posix()}\n"
        f"다음 초안 업무: {next_line}\n"
        f"모델: {result.get('model') or '-'}\n"
        f"사유: {result.get('reason') or '-'}\n\n"
        "초안 본문:\n"
        f"{draft_body}\n\n"
        "운영 기준:\n"
        "- 코드 개발 초안은 Gmail로 발송한다.\n"
        "- Mac mini에는 코드 개발 본문을 저장하지 않는다.\n"
        "- 실제 Revit API write 작업은 검증 게이트 전 확정하지 않는다.\n"
        "- 민감정보와 고객 모델 데이터는 외부 발송 본문에 포함하지 않는다.\n"
    )
    return subject, body


def send_code_development_gmail(queue: dict[str, Any], task: dict[str, Any], note_path: Path, result: dict[str, Any], next_item: dict[str, Any] | None) -> bool:
    subject, body = gmail_message(queue, task, note_path, result, next_item)
    send_result = send_gmail(subject, body, attachments=[] if external_code_only_mode() else [note_path])
    if send_result.get("ok"):
        print("gmail=sent")
        return True
    print(f"gmail=skipped reason={send_result.get('reason')}")
    return False


def send_telegram(text: str) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("telegram=skipped missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        return False
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    request = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=payload, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            print(f"telegram=sent status={response.status}")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"telegram=failed {type(exc).__name__}: {exc}")
        return False


async def run_next(max_tasks: int = 1, send_reports: bool = True, advance_on_blocked: bool = False) -> dict[str, Any]:
    load_local_env()
    queue = load_queue()
    state = load_state()
    completed_runs = []

    for _ in range(max(1, max_tasks)):
        task = next_task(queue, state)
        if not task:
            break
        state["in_progress"] = task["id"]
        save_state(state)

        result = await generate_draft(queue, task)
        if result.get("ok") or advance_on_blocked:
            if task["id"] not in state.setdefault("completed", []):
                state["completed"].append(task["id"])
        state["in_progress"] = None
        next_item = next_task(queue, state)
        persist_body = not external_code_only_mode()
        note_path = write_draft_note(task, result, persist_draft_body=persist_body)
        run_record = {
            "task_id": task["id"],
            "title": task["title"],
            "ok": bool(result.get("ok")),
            "reason": result.get("reason", ""),
            "note": note_path.relative_to(PROJECT_ROOT).as_posix(),
            "next_task": next_item["id"] if next_item else None,
            "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        }
        state.setdefault("runs", []).append(run_record)
        state["last_report"] = run_record
        save_state(state)

        if send_reports:
            send_telegram(telegram_message(queue, task, note_path, result, next_item))
        gmail_sent = send_code_development_gmail(queue, task, note_path, result, next_item)
        run_record["gmail_sent"] = gmail_sent
        run_record["external_code_only"] = external_code_only_mode()
        if external_code_only_mode():
            result["response"] = ""
        completed_runs.append(run_record)

        if not result.get("ok") and not advance_on_blocked:
            break

    return {
        "status": "ok",
        "product": queue["product"],
        "selected_item": queue["selected_item"],
        "runs": completed_runs,
        "remaining": [task["id"] for task in queue.get("tasks", []) if task["id"] not in set(state.get("completed", []))],
    }


def run_next_sync(max_tasks: int = 1, send_reports: bool = True, advance_on_blocked: bool = False) -> dict[str, Any]:
    return asyncio.run(run_next(max_tasks=max_tasks, send_reports=send_reports, advance_on_blocked=advance_on_blocked))

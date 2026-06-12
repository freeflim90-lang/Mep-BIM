from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Callable

from backend.core.paths import DATA_DIR

MANAGEMENT_EXCEL_REQUESTS_FILE = (
    DATA_DIR / "automation_requests" / "management_excel_automation_requests.json"
)
DEFAULT_REGISTRY = {"requests": []}


def _now_text(now: datetime.datetime | None = None) -> str:
    return (now or datetime.datetime.now()).isoformat(timespec="seconds")


def load_management_excel_requests(
    path: Path = MANAGEMENT_EXCEL_REQUESTS_FILE,
) -> dict:
    if not path.exists():
        return {"requests": []}
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"requests": []}
    if not isinstance(registry, dict):
        return {"requests": []}
    registry.setdefault("requests", [])
    if not isinstance(registry["requests"], list):
        registry["requests"] = []
    return registry


def save_management_excel_requests(
    registry: dict,
    path: Path = MANAGEMENT_EXCEL_REQUESTS_FILE,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def next_management_excel_request_id(
    registry: dict | None = None,
    *,
    now: datetime.datetime | None = None,
    path: Path = MANAGEMENT_EXCEL_REQUESTS_FILE,
) -> str:
    today = (now or datetime.datetime.now()).strftime("%Y%m%d")
    source = registry if registry is not None else load_management_excel_requests(path)
    prefix = f"MGMT-EXCEL-{today}-"
    numbers = []
    for item in source.get("requests", []):
        request_id = item.get("id", "")
        if request_id.startswith(prefix):
            try:
                numbers.append(int(request_id.rsplit("-", 1)[-1]))
            except ValueError:
                pass
    return f"{prefix}{max(numbers, default=0) + 1:03d}"


def summarize_management_excel_request(request_text: str) -> dict:
    lower = request_text.lower()
    risk_flags = []
    if any(keyword in lower for keyword in ["개인정보", "주민", "급여", "연봉", "전화", "메일", "이메일"]):
        risk_flags.append("개인정보/민감정보 포함 가능성")
    if any(keyword in lower for keyword in ["외부", "클라우드", "업로드", "공유"]):
        risk_flags.append("외부 전송/공유 검토 필요")
    if any(keyword in lower for keyword in ["매크로", "vba"]):
        risk_flags.append("매크로/VBA 보안 검토 필요")
    return {
        "purpose": "관리팀 반복 Excel 업무 자동화 후보",
        "expected_inputs": "Excel/XLSX/CSV 샘플 파일 또는 열 구조 설명 필요",
        "expected_outputs": "필터 가능한 XLSX/CSV, 검증 로그, 처리 요약",
        "development_need": "샘플 데이터 기반 Python/openpyxl 자동화 초안 필요",
        "approval_required": True,
        "risk_flags": risk_flags or ["특이 리스크 없음. 단, 실제 파일 수령 전 보안 검토 필요"],
    }


def create_management_excel_request_item(
    request_text: str,
    *,
    requester: str,
    requester_chat_id: str = "",
    registry: dict | None = None,
    now: datetime.datetime | None = None,
) -> dict:
    source = registry if registry is not None else {"requests": []}
    request_id = next_management_excel_request_id(source, now=now)
    created_at = _now_text(now)
    return {
        "id": request_id,
        "status": "pending_approval",
        "requester": requester,
        "requester_chat_id": requester_chat_id,
        "request_text": request_text,
        "summary": summarize_management_excel_request(request_text),
        "created_at": created_at,
        "approved_at": "",
        "approved_by": "",
        "rejected_at": "",
        "rejected_by": "",
        "rejection_reason": "",
        "execution_note": "",
    }


def find_management_excel_request(
    request_id: str,
    *,
    path: Path = MANAGEMENT_EXCEL_REQUESTS_FILE,
) -> tuple[dict, dict | None]:
    registry = load_management_excel_requests(path)
    for item in registry.get("requests", []):
        if item.get("id") == request_id:
            return registry, item
    return registry, None


def approve_management_excel_request(
    item: dict,
    *,
    approved_by: str,
    now: datetime.datetime | None = None,
) -> dict:
    item["status"] = "approved_running"
    item["approved_at"] = _now_text(now)
    item["approved_by"] = approved_by
    item["execution_note"] = "승인 후 corporate excel automation pipeline 실행"
    return item


def reject_management_excel_request(
    item: dict,
    *,
    rejected_by: str,
    reason: str,
    sanitizer: Callable[[str], str] | None = None,
    now: datetime.datetime | None = None,
) -> dict:
    clean_reason = sanitizer(reason) if sanitizer else reason
    item["status"] = "rejected"
    item["rejected_at"] = _now_text(now)
    item["rejected_by"] = rejected_by
    item["rejection_reason"] = clean_reason
    return item


def build_management_excel_approval_prompt(item: dict) -> str:
    return (
        "관리팀 Excel 자동화 승인 요청\n"
        f"요청 ID: {item['id']}\n"
        f"요청자: {item['requester']}\n"
        f"요청 내용:\n{item['request_text']}\n\n"
        "처리 기준:\n"
        "1. 실제 파일을 직접 변경하기 전 샘플 데이터와 출력 스키마를 먼저 확정한다.\n"
        "2. Python/openpyxl 기반 자동화를 우선 검토한다.\n"
        "3. 개인정보/급여/계약정보가 포함되면 실행 전 보안 검토로 중단한다.\n"
        "4. 산출물은 XLSX/CSV, 검증 로그, 처리 요약을 포함한다."
    )


def management_excel_report_text(item: dict) -> str:
    summary = item.get("summary", {})
    risk_lines = "\n".join(f"- {risk}" for risk in summary.get("risk_flags", []))
    return (
        "📊 [관리팀 Excel 자동화 승인 요청]\n\n"
        f"요청 ID: {item['id']}\n"
        f"요청자: {item['requester']}\n"
        f"상태: {item['status']}\n\n"
        f"요청 내용:\n{item['request_text']}\n\n"
        "검토 요약:\n"
        f"- 목적: {summary.get('purpose')}\n"
        f"- 입력: {summary.get('expected_inputs')}\n"
        f"- 출력: {summary.get('expected_outputs')}\n"
        f"- 개발 필요: {summary.get('development_need')}\n"
        f"- 리스크:\n{risk_lines}\n\n"
        f"승인: /approve {item['id']}\n"
        f"반려: /reject {item['id']} 사유"
    )

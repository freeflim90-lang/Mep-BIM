from __future__ import annotations

import datetime

from backend.management_excel_approval import (
    approve_management_excel_request,
    build_management_excel_approval_prompt,
    create_management_excel_request_item,
    find_management_excel_request,
    load_management_excel_requests,
    reject_management_excel_request,
    save_management_excel_requests,
)


def test_load_management_excel_requests_missing_file_returns_empty_registry(tmp_path):
    registry = load_management_excel_requests(tmp_path / "missing.json")

    assert registry == {"requests": []}


def test_save_and_find_management_excel_request_round_trip(tmp_path):
    path = tmp_path / "automation_requests.json"
    registry = {
        "requests": [
            {
                "id": "MGMT-EXCEL-20260612-001",
                "requester": "관리팀",
                "request_text": "월간 비용 Excel 집계 자동화",
            }
        ]
    }

    save_management_excel_requests(registry, path)
    loaded, item = find_management_excel_request("MGMT-EXCEL-20260612-001", path=path)

    assert loaded["requests"][0]["requester"] == "관리팀"
    assert item is not None
    assert item["request_text"] == "월간 비용 Excel 집계 자동화"


def test_create_management_excel_request_item_uses_registry_for_next_id():
    now = datetime.datetime(2026, 6, 12, 9, 30, 0)
    registry = {"requests": [{"id": "MGMT-EXCEL-20260612-004"}]}

    item = create_management_excel_request_item(
        "급여 파일은 제외하고 월간 비용 XLSX를 정리",
        requester="홍길동",
        requester_chat_id="123",
        registry=registry,
        now=now,
    )

    assert item["id"] == "MGMT-EXCEL-20260612-005"
    assert item["status"] == "pending_approval"
    assert item["requester_chat_id"] == "123"
    assert "개인정보/민감정보 포함 가능성" in item["summary"]["risk_flags"]


def test_approve_and_reject_management_excel_request_status_transitions():
    now = datetime.datetime(2026, 6, 12, 10, 0, 0)
    item = {"id": "MGMT-EXCEL-20260612-001"}

    approve_management_excel_request(item, approved_by="owner", now=now)

    assert item["status"] == "approved_running"
    assert item["approved_at"] == "2026-06-12T10:00:00"
    assert item["approved_by"] == "owner"
    assert item["execution_note"]

    reject_management_excel_request(
        item,
        rejected_by="owner",
        reason="<script>보안 검토 필요</script>",
        sanitizer=lambda text: text.replace("<", "").replace(">", ""),
        now=now,
    )

    assert item["status"] == "rejected"
    assert item["rejected_at"] == "2026-06-12T10:00:00"
    assert item["rejection_reason"] == "script보안 검토 필요/script"


def test_build_management_excel_approval_prompt_includes_execution_rules():
    prompt = build_management_excel_approval_prompt(
        {
            "id": "MGMT-EXCEL-20260612-001",
            "requester": "관리팀",
            "request_text": "비용 CSV를 XLSX로 변환하고 검증 로그 생성",
        }
    )

    assert "MGMT-EXCEL-20260612-001" in prompt
    assert "관리팀" in prompt
    assert "Python/openpyxl" in prompt
    assert "검증 로그" in prompt

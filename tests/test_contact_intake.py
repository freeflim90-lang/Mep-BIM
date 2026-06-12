import datetime as dt

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.contract_drafts import parse_krw_budget, scope_limit_assessment, validate_project_date
from backend.routers.contact_intake import create_contact_intake_router


def test_contract_budget_parsing_and_scope_risk_assessment():
    assert parse_krw_budget("1억 5000만원") == 150_000_000
    assert parse_krw_budget("2500만원") == 25_000_000

    assessment = scope_limit_assessment(
        budget="2500만원",
        area="35000",
        lod="LOD 350",
        disciplines="기계,전기,소방",
        formats="RVT,IFC",
        start_date="2026-07-01",
        end_date="2026-07-20",
    )

    assert assessment["tier"] == "단일 공종 중심 수행"
    assert any("LOD 350" in item for item in assessment["risks"])
    assert any("연면적 30,000m² 이상" in item for item in assessment["risks"])


def test_validate_project_date_rejects_bad_dates():
    assert validate_project_date("2026-07-01", "start_date") == "2026-07-01"

    app = FastAPI()
    app.include_router(create_contact_intake_router(
        project_root=None,  # type: ignore[arg-type]
        telegram_bot_token="",
        telegram_chat_id=None,
        gmail_settings=lambda: {"sender": "ops@example.com"},
        send_gmail=lambda **kwargs: {"ok": True, "reason": "sent"},
    ))
    client = TestClient(app)
    response = client.post("/api/contact", json={"email": "lead@example.com", "start_date": "2026/07/01"})

    assert response.status_code == 400
    assert response.json()["detail"] == "start_date must use YYYY-MM-DD format"


def test_contact_intake_generates_contract_email_and_log(tmp_path):
    sent = []

    def fake_gmail_settings():
        return {"sender": "ops@example.com"}

    def fake_send_gmail(**kwargs):
        sent.append(kwargs)
        return {"ok": True, "reason": "sent"}

    app = FastAPI()
    app.include_router(create_contact_intake_router(
        project_root=tmp_path,
        telegram_bot_token="",
        telegram_chat_id=None,
        gmail_settings=fake_gmail_settings,
        send_gmail=fake_send_gmail,
        now=lambda: dt.datetime(2026, 6, 12, 9, 30),
    ))
    client = TestClient(app)

    response = client.post(
        "/api/contact",
        json={
            "email": "lead@example.com",
            "company": "ACME BIM",
            "project": "Hospital Tower",
            "building_type": "Medical",
            "area": "35000",
            "budget": "2500만원",
            "disciplines": "기계,전기,소방",
            "lod": "LOD 350",
            "formats": "RVT,IFC",
            "start_date": "2026-07-01",
            "end_date": "2026-07-20",
            "message": "빠른 검토 부탁드립니다.",
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["status"] == "ok"
    assert payload["email_sent"] is True
    assert payload["auto_reply_sent"] is True
    assert payload["tg_sent"] is False
    assert payload["contract_error"] == ""
    contract_path = tmp_path / payload["contract_draft"]
    assert contract_path.exists()
    contract_text = contract_path.read_text(encoding="utf-8")
    assert "BIM 서비스 계약서 초안" in contract_text
    assert "Hospital Tower" in contract_text
    assert "LOD 350" in contract_text
    # 첫 번째 발송: 팀 알림 → 운영 Gmail 주소로
    assert sent[0]["recipient"] == "ops@example.com"
    assert "계약서 초안" in sent[0]["body"]
    # 두 번째 발송: 고객 자동 답장 → 문의 제출자 이메일로
    assert len(sent) == 2
    assert sent[1]["recipient"] == "lead@example.com"
    assert "접수되었습니다" in sent[1]["body"]
    assert "from=lead@example.com" in (tmp_path / "logs" / "contact_submissions.log").read_text(encoding="utf-8")


def test_contact_intake_router_is_registered_in_integrated_app():
    import backend.server_total as server

    paths = {route.path for route in server.app.routes}

    assert "/api/contact" in paths

#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUEUE_FILE = PROJECT_ROOT / "config" / "qwen_product_draft_queue.json"


IDEA_BANK = [
    {
        "platform": "Revit",
        "title": "MEP Access Clearance Auditor MVP 초안",
        "deliverable": "유지관리 공간 진단 룰, 도메인 모델, dry-run 리포트 계약",
        "scope": "Revit API 비의존 로직과 샘플 데이터 우선. 실제 Element 수집은 API 게이트 이후.",
        "output": "backend/product_candidates/access_clearance_auditor.py",
    },
    {
        "platform": "Revit",
        "title": "Sheet Issue Packager MVP 초안",
        "deliverable": "시트, 뷰, 레벨, 공종별 이슈 패키징 데이터 계약",
        "scope": "샘플 JSON 입력에서 검토 패키지를 생성하는 순수 로직 우선.",
        "output": "backend/product_candidates/sheet_issue_packager.py",
    },
    {
        "platform": "Navisworks",
        "title": "Clash Cause Classifier MVP 초안",
        "deliverable": "간섭 원인, 책임 공종, 반복 패턴, 회의 우선순위 분류 스키마",
        "scope": "Clash Detective export CSV/XML을 가정한 파서 계약과 분류 엔진만 작성.",
        "output": "backend/product_candidates/clash_cause_classifier.py",
    },
    {
        "platform": "Navisworks",
        "title": "Search Set QA Reporter MVP 초안",
        "deliverable": "Search Set 명명, 누락, 중복, 커버리지 QA 리포트 계약",
        "scope": "실제 Search Set 생성/수정은 제외하고 export 데이터 검증 로직 작성.",
        "output": "backend/product_candidates/search_set_qa_reporter.py",
    },
    {
        "platform": "Revit + Navisworks",
        "title": "Coordination Handoff Bridge MVP 초안",
        "deliverable": "Revit QA와 Navisworks 간섭 결과 통합 액션 보드 DTO",
        "scope": "JSON/CSV 샘플을 입력받아 통합 액션 목록을 만드는 백엔드 초안 작성.",
        "output": "backend/product_candidates/coordination_handoff_bridge.py",
    },
    {
        "platform": "Revit",
        "title": "Workset Hygiene Auditor MVP 초안",
        "deliverable": "작업세트 명명, 링크 배치, 모델 요소 분포 QA 규칙",
        "scope": "Workset 데이터는 샘플 스냅샷으로 대체하고 점검 로직만 작성.",
        "output": "backend/product_candidates/workset_hygiene_auditor.py",
    },
    {
        "platform": "Revit",
        "title": "Family Connector QA MVP 초안",
        "deliverable": "MEP 패밀리 커넥터 도메인, 방향, 시스템 분류 검증 계약",
        "scope": "Family/Connector API 직접 접근 없이 샘플 커넥터 DTO 기준으로 작성.",
        "output": "backend/product_candidates/family_connector_qa.py",
    },
    {
        "platform": "Navisworks",
        "title": "Weekly Clash Delta Reporter MVP 초안",
        "deliverable": "주간 간섭 증감, 재발, 신규 고위험 이슈 비교 리포트",
        "scope": "두 개의 clash export 파일 비교 로직과 테스트 케이스 작성.",
        "output": "backend/product_candidates/weekly_clash_delta_reporter.py",
    },
    {
        "platform": "Navisworks",
        "title": "Viewpoint Meeting Pack Builder MVP 초안",
        "deliverable": "회의용 viewpoint 묶음, 책임자, 의사결정 상태 데이터 계약",
        "scope": "Viewpoint API 호출은 제외하고 목록 생성/정렬/리포트 로직 우선.",
        "output": "backend/product_candidates/viewpoint_meeting_pack.py",
    },
    {
        "platform": "Revit + Navisworks",
        "title": "Issue Status Sync Contract MVP 초안",
        "deliverable": "Open/In Review/Resolved/Deferred 상태 전이와 충돌 해결 규칙",
        "scope": "양쪽 도구의 실제 동기화는 제외하고 상태 계약과 검증 로직 작성.",
        "output": "backend/product_candidates/issue_status_sync_contract.py",
    },
]


def main() -> int:
    today = dt.date.today()
    date_id = today.strftime("%Y%m%d")
    queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    tasks = queue.setdefault("tasks", [])

    if any(task.get("id", "").startswith(f"ADDIN-IDEA-{date_id}-") for task in tasks):
        print(f"daily_addin_ideas=already_seeded date={date_id}")
        return 0

    start = (today.toordinal() * 5) % len(IDEA_BANK)
    selected = [IDEA_BANK[(start + offset) % len(IDEA_BANK)] for offset in range(5)]
    for index, idea in enumerate(selected, start=1):
        tasks.append({
            "id": f"ADDIN-IDEA-{date_id}-{index:03d}",
            "title": f"{idea['platform']} {idea['title']}",
            "deliverable": idea["deliverable"],
            "scope": idea["scope"],
            "output_path_hint": idea["output"],
        })

    QUEUE_FILE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"daily_addin_ideas=seeded date={date_id} count=5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

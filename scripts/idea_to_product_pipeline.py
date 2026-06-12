#!/usr/bin/env python3
"""Promote internal product ideas into the next Qwen development queue.

This script is intentionally conservative. It does not overwrite the active
Qwen queue unless explicitly requested with --activate, and even then it checks
that the current queue is complete unless --force is supplied.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.collaboration import build_daily_idea_report
from backend.knowledge_store import knowledge_file_path


ACTIVE_QUEUE = PROJECT_ROOT / "config" / "qwen_product_draft_queue.json"
NEXT_QUEUE = PROJECT_ROOT / "config" / "qwen_next_product_draft_queue.json"
IDEATION_DIR = PROJECT_ROOT / "docs" / "product_ideation"
KB_FILE = Path(knowledge_file_path("아이디어발굴"))


def _kb_rel(agent: str) -> str:
    return Path(knowledge_file_path(agent)).relative_to(PROJECT_ROOT).as_posix()


def state_file_for(queue_file: Path) -> Path:
    return (
        PROJECT_ROOT
        / "obsidian_vaults"
        / "model_quality_auditor"
        / "06_Qwen_Drafts"
        / f"{queue_file.stem}_state.json"
    )


def load_json(path: Path, default: dict | None = None) -> dict:
    if not path.exists():
        return default or {}
    return json.loads(path.read_text(encoding="utf-8"))


def queue_status(queue_file: Path = ACTIVE_QUEUE) -> dict:
    queue = load_json(queue_file, {"tasks": []})
    state = load_json(state_file_for(queue_file), {"completed": []})
    task_ids = [task.get("id") for task in queue.get("tasks", []) if task.get("id")]
    completed = set(state.get("completed", []))
    remaining = [task_id for task_id in task_ids if task_id not in completed]
    return {
        "queue_file": str(queue_file.relative_to(PROJECT_ROOT)),
        "state_file": str(state_file_for(queue_file).relative_to(PROJECT_ROOT)),
        "product": queue.get("product", ""),
        "selected_item": queue.get("selected_item", ""),
        "total": len(task_ids),
        "completed": len(task_ids) - len(remaining),
        "remaining": remaining,
        "is_complete": not remaining and bool(task_ids),
    }


def make_task_id(prefix: str, index: int) -> str:
    return f"{prefix}-{index:03d}"


def product_code(title: str) -> str:
    words = [word for word in title.replace("/", " ").replace("-", " ").split() if word]
    ascii_words = [word for word in words if word.isascii()]
    if ascii_words:
        return "".join(word[:3].upper() for word in ascii_words[:3])[:12] or "NEXT"
    return "NEXT-PRODUCT"


def build_next_queue(top_idea: dict) -> dict:
    prefix = product_code(top_idea["title"])
    source_documents = [
        "docs/internal_organization_documents/23_IDEA_TO_PRODUCT_DEVELOPMENT_PIPELINE.md",
        _kb_rel("아이디어발굴"),
        _kb_rel("전략기획"),
        _kb_rel("프로그램개발"),
        _kb_rel("제품패키징"),
    ]
    return {
        "product": top_idea["title"],
        "selected_item": f"{top_idea['title']} MVP 상품화 후보",
        "source_documents": source_documents,
        "tasks": [
            {
                "id": make_task_id(prefix, 1),
                "title": "제품 문제 정의 및 MVP/Pro 범위 초안",
                "deliverable": "대상 사용자, 반복 고통, MVP 포함/제외 범위, Pro 확장 후보, Store 포지션",
                "scope": "아이디어발굴과 전략기획의 선정 근거를 개발 가능한 요구사항으로 전환한다.",
                "output_path_hint": "docs/product_ideation/requirements_brief.md",
            },
            {
                "id": make_task_id(prefix, 2),
                "title": "도메인 모델 및 설정 스키마 초안",
                "deliverable": "입력 데이터, 설정 프로필, 검증 규칙, 결과 DTO, 저장 위치",
                "scope": "Revit API 없이 검증 가능한 순수 백엔드 계약을 먼저 정의한다.",
                "output_path_hint": "backend/product_candidates/domain_contract.py",
            },
            {
                "id": make_task_id(prefix, 3),
                "title": "Dry-run 및 리포트 계약 초안",
                "deliverable": "모델 변경 전 미리보기, skip/warn/error 정책, 고객용 요약 리포트 구조",
                "scope": "실제 모델 변경은 Revit API 게이트 이후로 분리한다.",
                "output_path_hint": "backend/product_candidates/dry_run_report.py",
            },
            {
                "id": make_task_id(prefix, 4),
                "title": "테스트 케이스 및 실패 오답노트 템플릿 초안",
                "deliverable": "정상/경계/오류 케이스, Obsidian 오류 지식 기록 템플릿",
                "scope": "개발 과정의 수정 지식을 재사용 가능한 오답노트로 축적한다.",
                "output_path_hint": "obsidian_vaults/model_quality_auditor/04_Errors_and_Fixes/",
            },
            {
                "id": make_task_id(prefix, 5),
                "title": "Revit API 게이트 및 Store 패키징 계약 초안",
                "deliverable": "API 의존 지점, 실제 Revit 검증 항목, Autodesk Store 제출 문서 체크리스트",
                "scope": "실기 테스트 전 확정 금지 항목과 패키징 선행 문서를 분리한다.",
                "output_path_hint": "docs/revenue_products/store_packaging_contract.md",
            },
        ],
    }


def report_markdown(status: dict, idea_report: dict, promoted: bool, next_queue_path: Path | None) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# LUA BIM LAB",
        "# 아이디어 발굴-상품화 개발 순서 선정 보고",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        f"작성일: {now}",
        "배포등급: Internal Only",
        "주관: 아이디어발굴",
        "협업: 전략기획, 견적심사원, CFO, CEO, 브랜드마케팅, 요구사항분석, 프로그램개발, Qwen_Coder_8B",
        "",
        "## 1. 현재 개발 큐 상태",
        "",
        f"- 제품: {status['product']}",
        f"- 선정 아이템: {status['selected_item']}",
        f"- 완료: {status['completed']} / {status['total']}",
        f"- 완료 여부: {'완료' if status['is_complete'] else '진행 중'}",
        f"- 남은 task: {', '.join(status['remaining']) if status['remaining'] else '없음'}",
        "",
        "## 2. 상품화 후보 TOP 3",
        "",
        "| 순위 | 후보 | 대상 | 점수 | 예상 시간 | 예상 비용 | 예상 월 순매출 | 회수 기간 |",
        "|---:|---|---|---:|---:|---:|---:|---:|",
    ]
    for index, idea in enumerate(idea_report["ideas"], start=1):
        lines.append(
            "| {rank} | {title} | {customer} | {score} | {hours}h | USD {cost} | USD {monthly} | {payback}개월 |".format(
                rank=index,
                title=idea["title"],
                customer=idea["customer"],
                score=idea["monetization_score"],
                hours=idea["estimated_hours"],
                cost=idea["estimated_cost_usd"],
                monthly=idea["expected_monthly_net_usd"],
                payback=idea["payback_months"],
            )
        )
    lines.extend([
        "",
        "## 3. 1순위 후보 개발 전환 판단",
        "",
    ])
    top = idea_report["ideas"][0]
    lines.extend([
        f"- 1순위: {top['title']}",
        f"- 고객 문제: {top['problem']}",
        f"- MVP 해법: {top['solution']}",
        f"- 추천 가격: {top['recommended_price']}",
        f"- API 모드: {top['api_mode']}",
        "",
        "## 4. Handoff",
        "",
        "1. 현재 Qwen 큐가 완료되기 전에는 active queue를 덮어쓰지 않는다.",
        "2. 완료 후 CEO 승인 또는 --activate 실행 시 다음 큐로 전환한다.",
        "3. Qwen_Coder_8B는 요구사항, 도메인 계약, dry-run, 테스트, Revit API 게이트 순서로 초안을 작성한다.",
        "4. 오류와 수정사항은 Obsidian 오답노트로 연결한다.",
        "",
        "## 5. 생성 결과",
        "",
        f"- 다음 큐 후보 생성: {'예' if promoted else '아니오'}",
        f"- 다음 큐 후보 파일: {next_queue_path.relative_to(PROJECT_ROOT) if next_queue_path else '없음'}",
    ])
    return "\n".join(lines) + "\n"


def append_kb_entry(report_path: Path, status: dict, promoted: bool) -> None:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"""

## 기능 내재화 종료 후 아이디어-상품화 개발 큐 전환 기준 ({now})
- Source: LUA BIM LABS internal pipeline automation
- Tags: ideation,productization,qwen,development-queue,obsidian

현재 개발 큐 완료 후 아이디어발굴 조직은 전략기획, 견적심사원, CFO, CEO, 브랜드마케팅, 요구사항분석, 프로그램개발, Qwen_Coder_8B와 협업하여 다음 상품 후보를 선정한다. 활성 Qwen 큐는 완료 전 덮어쓰지 않으며, 다음 후보는 별도 queue 후보 파일로 먼저 생성한다.

- 기준 문서: [[23_IDEA_TO_PRODUCT_DEVELOPMENT_PIPELINE]]
- 최신 선정 보고: `{report_path.relative_to(PROJECT_ROOT)}`
- 현재 큐 완료 상태: {status['completed']} / {status['total']}
- 다음 큐 후보 생성 여부: {'예' if promoted else '아니오'}

@workflow daily_idea_report step: 현재 개발 큐 완료 후 1순위 상품화 후보를 다음 Qwen 개발 큐 후보로 전환한다
@workflow local_qwen_development step: active queue 덮어쓰기는 큐 완료 또는 명시 승인 후에만 수행한다
"""
    KB_FILE.write_text(KB_FILE.read_text(encoding="utf-8") + entry, encoding="utf-8")


def write_report(status: dict, idea_report: dict, promoted: bool, next_queue_path: Path | None) -> Path:
    IDEATION_DIR.mkdir(parents=True, exist_ok=True)
    report_path = IDEATION_DIR / f"{dt.date.today().isoformat()}_IDEA_TO_PRODUCT_PRIORITY_REPORT.md"
    report_path.write_text(report_markdown(status, idea_report, promoted, next_queue_path), encoding="utf-8")
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate product ideas and prepare the next Qwen development queue.")
    parser.add_argument("--force", action="store_true", help="Generate report even when the active Qwen queue is not complete.")
    parser.add_argument("--promote", action="store_true", help="Write the top idea into config/qwen_next_product_draft_queue.json.")
    parser.add_argument("--activate", action="store_true", help="Replace the active Qwen queue with the promoted next queue.")
    parser.add_argument("--limit", type=int, default=3, help="Number of ideas to include in the report.")
    args = parser.parse_args()

    status = queue_status()
    if not status["is_complete"] and not args.force:
        print(json.dumps({
            "ok": False,
            "reason": "active_queue_not_complete",
            "status": status,
            "hint": "Use --force to generate the candidate report without activating the next queue.",
        }, ensure_ascii=False, indent=2))
        return 2

    idea_report = build_daily_idea_report(limit=args.limit)
    next_queue_path = None
    promoted = False

    if args.promote or args.activate:
        next_queue = build_next_queue(idea_report["ideas"][0])
        NEXT_QUEUE.write_text(json.dumps(next_queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        next_queue_path = NEXT_QUEUE
        promoted = True

    if args.activate:
        if not status["is_complete"] and not args.force:
            raise SystemExit("Active queue is not complete. Use --force only with explicit operator approval.")
        ACTIVE_QUEUE.write_text(NEXT_QUEUE.read_text(encoding="utf-8"), encoding="utf-8")

    report_path = write_report(status, idea_report, promoted, next_queue_path)
    append_kb_entry(report_path, status, promoted)

    print(json.dumps({
        "ok": True,
        "active_queue_status": status,
        "report": str(report_path.relative_to(PROJECT_ROOT)),
        "next_queue": str(next_queue_path.relative_to(PROJECT_ROOT)) if next_queue_path else None,
        "activated": bool(args.activate),
        "top_idea": idea_report["ideas"][0]["title"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

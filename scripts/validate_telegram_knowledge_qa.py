"""Validate Telegram knowledge Q&A retrieval quality.

This is a lightweight regression suite for the local knowledge-answer loop.
It catches cases where operational curation reports outrank actual domain
knowledge, or where sensitive values leak into outbound answers.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import backend.server_total as server  # noqa: E402
from backend.knowledge_store import knowledge_file_path  # noqa: E402


def kb_rel(agent: str) -> str:
    return Path(knowledge_file_path(agent)).relative_to(PROJECT_ROOT).as_posix()


@dataclass
class QaCase:
    name: str
    query: str
    expected_top: str
    must_include: tuple[str, ...]
    forbidden: tuple[str, ...] = (
        "| 문서 | 유형 | 권고 |",
        "보안검토",
        "daily_knowledge_curation",
        "knowledge_updates/curation",
        "telegram-auto-search",
        "needs-review",
    )


CASES = [
    QaCase(
        name="공조배관 유체 약어",
        query="공조배관 유체 종류가 cws cwr 말고 또 뭐가 있을까?",
        expected_top=kb_rel("공조배관"),
        must_include=("CHWS/CHWR", "HWS/HWR", "REF", "STM", "Glycol"),
    ),
    QaCase(
        name="덕트 유체 종류",
        query="덕트 유체 종류가 SA RA 말고 또 뭐가 있을까?",
        expected_top=kb_rel("공조덕트"),
        must_include=("OA", "EA", "MA", "PS", "SE"),
    ),
    QaCase(
        name="위생배관 유체 종류",
        query="위생배관 유체 종류가 급수 급탕 말고 또 뭐가 있어?",
        expected_top=kb_rel("위생"),
        must_include=("급탕환수", "오배수", "통기", "우수"),
        forbidden=(
            "| 문서 | 유형 | 권고 |",
            "보안검토",
            "daily_knowledge_curation",
            "knowledge_updates/curation",
            "telegram-auto-search",
            "needs-review",
            "국내 법령 및 고시",
            "KS 규격",
        ),
    ),
    QaCase(
        name="전기 트레이 기본",
        query="전기 케이블 트레이에서 확인해야 하는 기본 기준 알려줘",
        expected_top=kb_rel("전기"),
        must_include=("트레이", "강전", "이격"),
    ),
    QaCase(
        name="Revit Addin 라우팅",
        query="Revit addin에서 설비 질문 답변을 LUA BIM LABS가 하게 하는 구조 알려줘",
        expected_top=kb_rel("Revit_Addin"),
        must_include=("LUA BIM LABS", "Revit", "Obsidian"),
    ),
    QaCase(
        name="공조 약어 모호성",
        query="CWS가 급수야 냉각수야? 도면에서 어떻게 판단해?",
        expected_top=kb_rel("공조배관"),
        must_include=("냉각수", "급수", "범례"),
    ),
    QaCase(
        name="소방기계 헤드",
        query="스프링클러 헤드 주변 BIM에서 뭘 확인해야 해?",
        expected_top=kb_rel("소방기계"),
        must_include=("스프링클러", "헤드", "살수"),
    ),
    QaCase(
        name="자동제어 VAV",
        query="VAV 제어에서 확인해야 하는 포인트 알려줘",
        expected_top=kb_rel("설비자동제어"),
        must_include=("VAV", "최소풍량", "덕트 정압"),
    ),
    QaCase(
        name="설비 도면 해석",
        query="도면에서 공조방식과 부하계산 관련해서 어떤 문서를 같이 봐야 해?",
        expected_top=kb_rel("설비도면해석"),
        must_include=("부하계산서", "장비일람표", "계통도"),
    ),
    QaCase(
        name="Dynamo 카테고리 일괄 선택",
        query="원하는 카테고리의 객체를 일괄 선택하는 다이나모를 구현하고 싶은데 방법을 알려줘",
        expected_top=kb_rel("Dynamo"),
        must_include=("Categories", "All Elements of Category", "FilteredElementCollector", "SetElementIds"),
    ),
    QaCase(
        name="Dynamo 폴더 하위 패밀리 배치",
        query="다이나모로 폴더 하위에 있는 패밀리 배치하는 노드는 어떻게 구성해야되?",
        expected_top=kb_rel("Dynamo"),
        must_include=("Directory.Contents", "doc.LoadFamily", "NewFamilyInstance", ".rfa"),
        forbidden=(
            "| 문서 | 유형 | 권고 |",
            "보안검토",
            "daily_knowledge_curation",
            "knowledge_updates/curation",
            "telegram-auto-search",
            "needs-review",
            "All Elements of Category` 노드에 연결",
        ),
    ),
]


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def validate_case(case: QaCase) -> list[str]:
    errors: list[str] = []
    matches = server.search_local_knowledge(case.query, limit=5)
    answer = server.build_knowledge_answer(case.query, matches)
    if not matches:
        return [f"{case.name}: no matches"]

    top = rel(matches[0]["path"])
    if top != case.expected_top:
        errors.append(f"{case.name}: expected top {case.expected_top}, got {top}")

    for token in case.must_include:
        if token.lower() not in answer.lower():
            errors.append(f"{case.name}: missing expected token {token!r}")

    for token in case.forbidden:
        if token.lower() in answer.lower():
            errors.append(f"{case.name}: forbidden token appeared {token!r}")

    if len(answer) > 3600:
        errors.append(f"{case.name}: answer too long ({len(answer)} chars)")

    return errors


def validate_masking() -> list[str]:
    sample = (
        "담당자 test@example.com, 연락처 010-1234-5678, "
        "식별번호 1234567890, 주민번호 900101-1234567"
    )
    masked = server.sanitize_outbound_text(sample)
    errors: list[str] = []
    for raw in ("test@example.com", "010-1234-5678", "1234567890", "900101-1234567"):
        if raw in masked:
            errors.append(f"masking: raw sensitive value leaked: {raw}")
    for marker in ("[EMAIL_MASKED]", "[PHONE_MASKED]", "[LONG_ID_MASKED]", "[RRN_MASKED]"):
        if marker not in masked:
            errors.append(f"masking: missing marker {marker}")
    return errors


def validate_quality_gate() -> list[str]:
    errors: list[str] = []
    bad_query = "원하는 카테고리의 객체를 일괄 선택하는 다이나모를 구현하고 싶은데 방법을 알려줘"
    matches = server.search_local_knowledge(bad_query, limit=5)
    answer = server.build_knowledge_answer(bad_query, matches)
    assessment = server.assess_knowledge_answer_quality(
        bad_query,
        server.infer_knowledge_agent_from_query(bad_query),
        matches,
        answer,
    )
    if not assessment["ok"]:
        errors.append(f"quality-gate: known Dynamo case should be ok, got {assessment['reasons']}")

    synthetic_bad = [
        {
            "score": 29,
            "path": Path(knowledge_file_path("지식업데이트")),
            "excerpt": "지식 베이스 업데이트 운영 기준",
        }
    ]
    bad_assessment = server.assess_knowledge_answer_quality(
        bad_query,
        "Dynamo",
        synthetic_bad,
        "지식 베이스 업데이트 운영 기준",
    )
    if bad_assessment["ok"]:
        errors.append("quality-gate: operational document should trigger auto supplementation")
    return errors


def main() -> int:
    all_errors: list[str] = []
    print("Telegram knowledge Q&A validation")
    print("=" * 40)
    for case in CASES:
        matches = server.search_local_knowledge(case.query, limit=5)
        top = rel(matches[0]["path"]) if matches else "-"
        print(f"- {case.name}: top={top}")
        all_errors.extend(validate_case(case))
    all_errors.extend(validate_masking())
    all_errors.extend(validate_quality_gate())

    if all_errors:
        print("\nFAILED")
        for error in all_errors:
            print(f"  - {error}")
        return 1

    print("\nPASSED")
    print(f"cases={len(CASES)} masking=ok quality_gate=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

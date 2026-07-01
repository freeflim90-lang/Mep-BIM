from scripts.audit_qa_answer_substance import assess, core_answer


def test_core_answer_excludes_repeated_operational_scaffolding():
    answer = (
        "결론: 모델의 문 개폐 공간을 확인한다. KST03 적용주의로 현장 조건을 검토한다."
        "\n\n실무 보강 (2026-06-20 답변 품질 보강):\n1. 기준 확인: 공통 안내"
    )

    assert core_answer(answer) == "결론: 모델의 문 개폐 공간을 확인한다. KST03 적용주의로 현장 조건을 검토한다."


def test_substance_audit_requires_answer_specific_evidence_and_action():
    result = assess("분전반 앞 작업공간은 어떻게 확인하나요?", "충돌을 확인합니다.")

    assert "문답 단위 근거 또는 KST 상태" in result["missing"]
    assert "답변 고유 설명 120자 이상" in result["missing"]


def test_substance_audit_flags_missing_numbered_structure():
    """재작성이 번호/불릿 구조를 산문으로 풀어써 표준 루브릭 점수가 떨어지던
    회귀(2026-06-26)를 감사에서 잡는지 고정한다."""
    prose = (
        "결론: 각 수치의 시장 정의·지역·기준연도·통화·방법론을 비교해 목적에 맞는 "
        "참고값으로 분리한다. 원문 보고서와 공식 통계, 발행일과 표본을 근거로 출처표를 "
        "만든다. 적용 범위는 제안서와 투자자료다. 담당자는 24시간 안에 확인하고 기록한다."
    )
    structured = (
        "결론: 목적별로 분리한다. 1. 시장 정의·지역·기준연도를 확인한다. "
        "2. 출처 방법론을 비교해 출처표를 만든다. 3. 적용 범위(제안서/투자자료)를 정하고 "
        "담당자가 24시간 내 기록·검토한다."
    )
    q = "BIM 시장 규모 수치가 자료마다 다르면 무엇을 믿나요?"

    prose_missing = assess(q, prose)["missing"]
    structured_missing = assess(q, structured)["missing"]

    assert any("구조" in m for m in prose_missing)
    assert not any("구조" in m for m in structured_missing)

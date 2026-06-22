from scripts.validate_auto_enrich_guardrails import (
    GUARDRAIL_LINE,
    add_guardrails_to_content,
    audit_file,
)


def test_add_guardrails_to_auto_enrich_section():
    content = (
        "# KB\n\n"
        "## 최신 동향 (2026-06-21)\n"
        "- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-21\n"
        "자동 수집 본문\n"
    )

    updated, changed = add_guardrails_to_content(content)

    assert changed == 1
    assert GUARDRAIL_LINE in updated
    assert updated.index(GUARDRAIL_LINE) > updated.index("- Source: auto-enrich via")


def test_add_guardrails_is_idempotent_when_kst04_exists():
    content = (
        "## 최신 동향 (2026-06-21)\n"
        "- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-21\n"
        "- KST04 자동수집: 고객 확정 답변 금지.\n"
    )

    updated, changed = add_guardrails_to_content(content)

    assert changed == 0
    assert updated == content


def test_audit_file_reports_missing_guardrail(tmp_path):
    path = tmp_path / "kb.md"
    path.write_text(
        "## 최신 동향 (2026-06-21)\n"
        "- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-21\n"
        "자동 수집 본문\n",
        encoding="utf-8",
    )

    issues = audit_file(path)

    assert len(issues) == 1
    assert issues[0].title.startswith("최신 동향")


def test_generator_emits_guarded_section(tmp_path):
    """근본수정 고정(cycle255): auto_enrich 생성기 append_section 이 KST04 가드레일을
    포함한 섹션을 써야 한다. 누락 시 매일 실행마다 미가드 섹션이 재유입된다."""
    import scripts.auto_enrich_knowledge_base as ae

    kb = tmp_path / "kb.md"
    kb.write_text("# 테스트 지식 베이스\n", encoding="utf-8")
    ae.append_section(kb, "테스트 토픽 보강", "test,tag", "충분히 긴 본문 콘텐츠입니다. " * 5, "test_stem")

    content = kb.read_text(encoding="utf-8")
    assert "auto-enrich via" in content
    assert ae.GUARDRAIL_LINE.strip() in content
    # 생성된 섹션은 validator 기준 미가드 0 이어야 한다.
    assert len(audit_file(kb)) == 0

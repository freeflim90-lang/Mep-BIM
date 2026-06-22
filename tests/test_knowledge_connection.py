"""에이전트 지식 연결 회귀 테스트.

다각도 점검으로 발견·수정한 두 가지 연결 결함을 고정한다:
  1) 특수문자 에이전트의 stem 정규화 불일치 → 자기 KB 가산점(+50) 누락
  2) 규칙 미스 시 운영 기본값(지식업데이트)으로 떨어져 점수가 임계 밑으로 내려가
     불필요한 웹검색/DeepSeek 재작성 API 가 소모되던 라우팅 갭
"""
from __future__ import annotations

import pytest

import backend.server_total as server
from backend.knowledge_engine import resolve_save_agent
from backend.knowledge_store import safe_agent_stem


# ── 1) stem 정규화: 파일 생성 규칙과 검색측 비교가 같은 결과를 내야 한다 ──
@pytest.mark.parametrize("agent,expected_stem", [
    ("고객지원 CS", "고객지원CS"),
    ("EIR/BEP_심사원", "EIRBEP_심사원"),
    ("최고전략 (CSO)", "최고전략CSO"),
    ("인프라_DevOps (Obsidian)", "인프라_DevOpsObsidian"),
])
def test_safe_agent_stem_strips_special_chars(agent, expected_stem):
    assert safe_agent_stem(agent) == expected_stem


@pytest.mark.parametrize("agent", [
    "고객지원 CS",
    "최고전략 (CSO)",
    "인프라_DevOps (Obsidian)",
])
def test_special_char_agent_finds_own_kb(agent):
    """특수문자가 든 에이전트도 자기 KB 가 검색 top 으로 연결돼야 한다.

    이전엔 path.stem(특수문자 제거) != agent(원본) 이라 +50 가산점이 빠져
    자기 KB 를 못 찾았다."""
    stem = safe_agent_stem(agent)
    query = f"{agent} 운영 기준 핵심"
    matches = server.search_local_knowledge(query, limit=5)
    assert matches, f"no matches for {agent}"
    top_stems = [m["path"].stem for m in matches[:3]]
    assert stem in top_stems, f"{agent}: 자기 KB({stem}) 미연결, top={top_stems}"


# ── 1b) 인프라_DevOps(Obsidian): 주제 적합 질의는 자기 답변이 로컬 즉답이어야 ──
@pytest.mark.parametrize("query", [
    "Obsidian 볼트로 BIM 지식 그래프를 구축하고 자동 동기화하는 방법",
    "Model Quality Auditor Obsidian 연동 운영 절차",
])
def test_infra_obsidian_query_not_falsely_penalized(query):
    """인프라_DevOps(Obsidian)는 정식 지식 에이전트다. 주제 적합 질의에서
    자기 KB 가 top 이면 운영문서 페널티로 불필요한 웹검색을 돌리면 안 된다."""
    matches = server.search_local_knowledge(query, limit=3)
    answer = server.build_knowledge_answer(query, matches)
    agent = server.infer_knowledge_agent_from_query(query)
    readiness = server.assess_team_telegram_answer_readiness(query, agent, matches, answer)
    assert matches[0]["path"].stem == "인프라_DevOpsObsidian"
    assert readiness["should_search"] is False, readiness["reasons"]


# ── 2) 이름-친화도 폴백: 규칙 미스여도 도메인 에이전트로 라우팅 ──
@pytest.mark.parametrize("query,expected_agent", [
    ("요구사항 분석 기능 명세", "요구사항분석"),
])
def test_name_affinity_fallback_routes_to_domain_agent(query, expected_agent):
    assert server.infer_knowledge_agent_from_query(query) == expected_agent


# ── 3) 갭 보강 저장 에이전트: 추론 실패 시 검색 top 으로 역매핑(오염 방지) ──
@pytest.mark.parametrize("query,expected_agent", [
    ("철근 정착길이 이음 기준", "구조"),
    ("EULA 면책조항 작성 기준", "법무조항검토"),
    ("MSI 인스톨러 패키징 서명", "제품패키징"),
    ("해외진출 현지화 우선순위", "글로벌_유통기획관"),
])
def test_resolve_save_agent_uses_search_top_when_routing_fails(query, expected_agent):
    """도메인 질의가 운영 기본값으로 라우팅돼도 웹 보강 내용은 검색 top 의
    올바른 에이전트 KB 에 저장돼야 한다(이전엔 전부 '건축'으로 오염)."""
    assert resolve_save_agent(query) == expected_agent


def test_resolve_save_agent_falls_back_to_default_when_no_match():
    assert resolve_save_agent("완전무관한랜덤xyz단어") == "건축"


# ── 4) 흔한 도메인 용어 라우팅(키워드 보강): 이름 없는 자연 질의도 강하게 연결 ──
@pytest.mark.parametrize("query,expected_agent", [
    ("비상조명 점등 시간 법적 기준", "소방전기"),
    ("유도등 비상전원 용량 산정", "소방전기"),
    ("수전용량 계산해서 변압기 용량 정하기", "전기"),
    ("변압기 용량 산정 기준", "전기"),
    ("피난계단 유효폭이 부족하면 어떻게 조정하나요", "건축"),
    ("직통계단 설치 개수 기준", "건축"),
    ("철근 정착길이 이음 기준", "구조"),
    ("철근 배근 간격 기준", "구조"),
])
def test_common_domain_terms_route_strongly(query, expected_agent):
    assert server.infer_knowledge_agent_from_query(query) == expected_agent
    matches = server.search_local_knowledge(query, limit=3)
    answer = server.build_knowledge_answer(query, matches)
    readiness = server.assess_team_telegram_answer_readiness(
        query, expected_agent, matches, answer
    )
    assert readiness["should_search"] is False, readiness["reasons"]


# ── 5) 내부 신호/트렌드 로그가 도메인 Q&A 를 가로채지 않아야(흔한 토큰 오매칭 방지) ──
def test_internal_signal_log_does_not_hijack_domain_query():
    """'시간' 같은 흔한 토큰으로 AX 신호모니터링 로그가 도메인 답을 이기면 안 된다."""
    matches = server.search_local_knowledge("비상조명 점등 시간 법적 기준", limit=4)
    top_stems = [m["path"].stem for m in matches]
    assert "AX_시간별_신호모니터링" not in top_stems[:2], top_stems


def test_signal_monitoring_query_still_reaches_log():
    """가드: 진짜 신호모니터링 의도 질의는 여전히 해당 로그를 최상위로 찾아야 한다."""
    matches = server.search_local_knowledge("AX 시간별 신호 모니터링 운영 기준", limit=3)
    assert matches and matches[0]["path"].stem == "AX_시간별_신호모니터링"


# ── 6) excerpt 세부주제 정확도: 제목이 질의와 맞는 섹션이 답으로 와야 한다 ──
def test_excerpt_picks_topic_matching_section_not_dense_offtopic():
    """'분전반 전면 작업공간' 질문이 키워드 조밀한 케이블트레이 섹션이 아니라
    분전반/수배전반 관련 섹션을 답으로 뽑아야 한다(세부주제 정확도)."""
    matches = server.search_local_knowledge("분전반 전면 작업공간 확보 거리", limit=1)
    answer = server.build_knowledge_answer("분전반 전면 작업공간 확보 거리", matches)
    head = answer.splitlines()[0] if answer else ""
    assert "케이블 트레이" not in head, head
    assert ("분전반" in head) or ("수배전반" in head), head


def test_excerpt_heading_match_for_sprinkler():
    """제목 일치 부스트로 살수반경 질의는 살수반경 섹션을 답으로 한다."""
    matches = server.search_local_knowledge("스프링클러 헤드 살수반경 기준", limit=1)
    answer = server.build_knowledge_answer("스프링클러 헤드 살수반경 기준", matches)
    assert "살수반경" in answer.splitlines()[0]


def test_structural_spec_buried_sections_surface():
    """구조 시방서 핵심 기준 아래 묻혀있던 거푸집/타설/양생/철골/프리스트레스
    ###를 ##로 승격 → 각 주제 질의가 자기 섹션을 답으로 뽑아야 한다(피복두께
    청크-시작이 아니라). 잘못 묻혔던 철골 콘텐츠 분리 회귀 방지 포함."""
    cases = [
        ("거푸집 존치기간 기준", "거푸집"),
        ("콘크리트 타설 낙하높이", "타설"),
        ("콘크리트 양생 기간", "양생"),
        ("철골 용접 검사 기준", "철골"),
        ("프리스트레스 긴장력", "프리스트레스"),
    ]
    for query, kw in cases:
        assert server.infer_knowledge_agent_from_query(query) == "구조", query
        matches = server.search_local_knowledge(query, limit=1)
        head = server.build_knowledge_answer(query, matches).splitlines()[0]
        assert kw in head, f"{query} -> {head}"
        assert "피복 두께" not in head, f"{query} surfaced 피복두께 chunk-start: {head}"


def test_fireproofing_not_confused_with_rebar_cover():
    """'내화피복(철골 방화 뿜칠)'의 '...피복 두께' substring이 구조 키워드
    '피복 두께'(철근 피복)에 걸려 구조로 새며 철근 피복두께를 confident-오답으로
    답하던 것 회귀 방지. 내화피복은 건축(방화)으로 가고 철골 내화피복 섹션을 답해야."""
    for q in ("내화피복 두께", "철골 내화피복", "내화피복 뿜칠 두께", "내화도료"):
        assert server.infer_knowledge_agent_from_query(q) == "건축", q
    head = server.build_knowledge_answer(
        "내화피복 두께", server.search_local_knowledge("내화피복 두께", limit=1)
    ).splitlines()[0]
    assert "내화피복" in head, head
    assert "철근" not in head and "철근 공사" not in head, head


def test_offtopic_quick_answer_does_not_outrank_topic_section():
    """'보온 두께' 질의가 off-topic 빠른답변(CWS 약어 판단)에 밀리지 않고
    보온 관련 섹션을 답으로 해야 한다('빠른 답변' 플랫 부스트 과대 가중 회귀 방지)."""
    matches = server.search_local_knowledge("냉각수 배관 보온 두께", limit=1)
    head = server.build_knowledge_answer("냉각수 배관 보온 두께", matches).splitlines()[0]
    assert "cws" not in head.lower(), head
    assert "보온" in head, head


def test_ontopic_quick_answer_still_wins():
    """가드: 세부주제가 맞는 빠른답변 섹션은 여전히 선택돼야 한다(과교정 방지)."""
    matches = server.search_local_knowledge("CWS가 급수인지 냉각수인지 판단", limit=1)
    head = server.build_knowledge_answer("CWS가 급수인지 냉각수인지 판단", matches).splitlines()[0]
    assert "cws" in head.lower(), head


# ── 7) 부분문자열 오매칭 방지: '오케스트레이터'가 '트레이'로 전기에 잡히면 안 됨 ──
def test_substring_keyword_does_not_misroute_orchestrator():
    """'파이프라인 오케스트레이터'의 '...트레이터'가 전기 키워드 '트레이'로
    오매칭돼 전기로 가던 버그 회귀 방지."""
    assert server.infer_knowledge_agent_from_query("파이프라인 오케스트레이터") == "파이프라인_오케스트레이터"
    terms = server.query_terms("파이프라인 오케스트레이터")
    assert "강전" not in terms and "충전율" not in terms, terms


@pytest.mark.parametrize("query", [
    "케이블트레이 충전율",
    "케이블 트레이 곡률반경",
    "분전반 케이블 트레이 충전율",
])
def test_cable_tray_still_routes_to_electrical(query):
    """가드: 실제 케이블트레이 질의는 여전히 전기로 라우팅돼야 한다."""
    assert server.infer_knowledge_agent_from_query(query) == "전기"


@pytest.mark.parametrize("query", [
    "BIM Coordinator 6년차 교육",
    "coordinator 교육 로드맵",
    "Coordinator 커리큘럼 단계",
])
def test_ascii_agent_name_word_boundary_no_coordinator_leak(query):
    """@knowledge_agent_name 센티넬의 ASCII 명(COO)이 'coordinator' 속
    부분일치로 발화해 교육 질의가 COO 로 새던 회귀 방지. 교육 의도어가 있으면
    교육컨설팅으로 가야 한다."""
    assert server.infer_knowledge_agent_from_query(query) != "COO"


@pytest.mark.parametrize("query,agent", [
    ("COO 역할이 뭐야", "COO"),
    ("운영총괄 COO 업무", "COO"),
    ("CEO 비전", "CEO"),
    ("CFO 재무 전략", "CFO"),
    ("Revit_Addin 기능", "Revit_Addin"),
])
def test_ascii_agent_name_standalone_still_routes(query, agent):
    """가드: 단어경계 매칭으로 바꿔도 실제 ASCII 에이전트명 단독 질의는
    여전히 해당 에이전트로 라우팅돼야 한다(밑줄 합성명 포함)."""
    assert server.infer_knowledge_agent_from_query(query) == agent


# ── 시설 규모 팩트: 미수록 시설을 confident 로 오답(다른 시설 수치)하지 않게 가드 ──
def test_entity_magnitude_nearby_unit():
    """합성 답변(KB 비의존): 시설명+수치 인접만 '커버'로 인정, 산문 언급은 불인정."""
    from backend.knowledge_engine import _entity_has_magnitude_nearby as near
    ans = "제1터미널 (t1) | 약 496,000㎡ | 2001년 개항 | 표에 없는 프로젝트(예: 성수 project 등)는 원본 확인".lower()
    assert near(ans, "제1터미널") is True          # 수치 인접 → 커버
    assert near(ans, "성수") is False              # 면책 산문 언급뿐 → 미커버


def test_uncovered_facility_magnitude_query_triggers_search():
    """DB 표에 없는 시설의 면적/규모 질의는 (다른 시설 수치를 confident 서빙하지 않도록)
    웹검색을 허용해야 한다 — named-entity-not-covered 가드."""
    for q in ["성수 K-project 면적이 얼마야", "김포 공항 면적이 얼마야", "롯데타워 높이가 얼마야"]:
        m = server.search_local_knowledge(q, limit=2)
        a = server.infer_knowledge_agent_from_query(q)
        r = server.assess_team_telegram_answer_readiness(q, a, m, server.build_knowledge_answer(q, m))
        assert r["should_search"] is True, q


def test_combined_answer_webdown_fallback_honors_entity_coverage():
    """웹 보강 실패(빈 결과) 시 build_combined_answer 폴백도 entity 커버리지를 본다 —
    미수록 시설(성수/김포)은 로컬 발췌(인천공항 등) 재서빙 대신 '찾지 못함', 수록 시설은 반환.
    (웹 백본 다운 중에도 named-entity 가드가 무력화되지 않게 하는 회귀.)"""
    for q in ["성수 K-project 면적이 얼마야", "김포 공항 면적이 얼마야"]:
        ans = server.build_combined_answer(q, "", server.search_local_knowledge(q, limit=2))
        assert "찾지 못" in ans, q
    for q in ["인천공항 제1터미널 면적이 얼마야", "덕트 풍속 기준"]:
        ans = server.build_combined_answer(q, "", server.search_local_knowledge(q, limit=2))
        assert "찾지 못" not in ans, q


@pytest.mark.parametrize("query", [
    "인천공항 제1터미널 면적이 얼마야",
    "인천공항 제2터미널 연면적이 얼마야",
    "청라 스타필드 면적이 얼마야",
])
def test_covered_facility_magnitude_query_stays_confident(query):
    """가드: 실제 DB 표에 수록된 시설(수치 인접)의 규모 질의는 confident 유지 →
    불필요한 웹검색이 돌지 않아야 한다."""
    m = server.search_local_knowledge(query, limit=2)
    a = server.infer_knowledge_agent_from_query(query)
    r = server.assess_team_telegram_answer_readiness(query, a, m, server.build_knowledge_answer(query, m))
    assert "named-entity-not-covered" not in r["reasons"], query


# ── 고아 KB 연결: 심사/검수 관점 질의가 작성/산정 KB 로 새지 않고 심사원 KB 에 도달 ──
@pytest.mark.parametrize("query,expected", [
    ("견적 심사 이상 견적 감지 패턴", "견적심사원"),
    ("견적 적정성 검수", "견적심사원"),
    ("EIR BEP 적정성 심사 납품 검토", "EIR/BEP_심사원"),
    ("ISO 19650 BEP 심사 보고서", "EIR/BEP_심사원"),
])
def test_review_agent_orphan_kb_reachable(query, expected):
    """견적심사원(360행)·EIR/BEP_심사원(223행) 고유 KB 가 '심사' 관점 질의에서
    작성/산정 KB(BIM_프로젝트_견적산정·BEP_수행계획서)에 가려지지 않고 도달."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query", [
    "단열재 종류",
    "비드법 압출법 그라스울 차이",
    "우레탄폼 단열재",
])
def test_insulation_catalog_content_reachable(query):
    """단열재 종류·특징 카탈로그(KS 분류) 저작 — '단열재 종류'가 LOD/마감 발췌에,
    자재명(비드법/그라스울)이 운영 노이즈에 confident/weak-오답이던 것 해소. 건축 라우팅 + 종류 콘텐츠."""
    assert server.infer_knowledge_agent_from_query(query) == "건축"
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert ("비드법" in ans) or ("그라스울" in ans), ans[:120]


def test_eps_room_electrical_not_misrouted_by_insulation_keywords():
    """가드: 단열재 자재명 추가로도 'EPS실 분전반'은 전기 유지(eps/xps 바 키워드 미추가)."""
    assert server.infer_knowledge_agent_from_query("EPS실 분전반 전면 클리어런스") == "전기"


@pytest.mark.parametrize("query", [
    "정화조 용량 산정",
    "오수처리시설 용량",
    "정화조 처리대상인원",
])
def test_septic_treatment_routes_to_plumbing_with_content(query):
    """정화조·오수처리시설 용량(건축 오수정화)은 위생 — 토목 '오수' 키워드가
    처리시설 질의를 가로채지 않아야 한다. 위생 라우팅 + 처리대상인원/방류수 내용."""
    assert server.infer_knowledge_agent_from_query(query) == "위생"
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert ("처리대상인원" in ans) or ("오수처리시설" in ans) or ("방류수" in ans), ans[:120]


@pytest.mark.parametrize("query", ["오수 관로 구배", "우수 관로 기준"])
def test_sewer_pipeline_stays_civil(query):
    """가드: 처리시설이 아닌 오수/우수 관로 질의는 토목 유지(정화조 규칙이 안 가로챔)."""
    assert server.infer_knowledge_agent_from_query(query) == "토목"


@pytest.mark.parametrize("query", [
    "출입통제 시스템",
    "주차관제 설비",
    "출입통제 카드리더 배선",
])
def test_access_parking_control_routes_to_telecom_with_content(query):
    """출입통제·주차관제(약전 보안) 콘텐츠 저작 — 운영 노이즈 weak-오답이던 것 해소.
    통신 라우팅 + fail-safe/LPR 등 내용. 'eps/차단기' 같은 타공종 충돌어는 미추가."""
    assert server.infer_knowledge_agent_from_query(query) == "통신"
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert ("출입통제" in ans) or ("주차관제" in ans) or ("fail-safe" in ans.lower()), ans[:120]


def test_mccb_not_misrouted_to_telecom():
    """가드: '배선용차단기'는 통신으로 가지 않는다(주차 '차단기' 바 키워드 미추가)."""
    assert server.infer_knowledge_agent_from_query("배선용차단기 용량") != "통신"


@pytest.mark.parametrize("query", ["LOD 단계", "LOD 정의", "LOD 100 200 300 400 500"])
def test_general_lod_routes_to_bim_spec(query):
    """일반 LOD(공종어 없는 LOD 정의/단계)는 BIM_시방서(LOD 100~500 기준표)로 — 이전엔
    운영 노이즈 weak였음. @discipline_keywords 뒤 배치로 공종+LOD는 공종 유지."""
    assert server.infer_knowledge_agent_from_query(query) == "BIM_시방서"


@pytest.mark.parametrize("query", ["워크셋 분담", "작업세트 중앙모델 동기화", "모델 분할 기준", "워크셰어링 협업"])
def test_worksharing_modelsplit_routes_to_bim_spec_with_content(query):
    """Revit 워크셰어링·모델 분할(BIM 협업) 콘텐츠 저작 — 운영 노이즈 weak였던 것 해소.
    BIM_시방서 라우팅 + 중앙모델/워크셋/동기화 내용."""
    assert server.infer_knowledge_agent_from_query(query) == "BIM_시방서"
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert ("워크셋" in ans) or ("중앙 모델" in ans) or ("동기화" in ans), ans[:120]


@pytest.mark.parametrize("query", ["공유좌표 설정", "공유좌표 정합", "Acquire Coordinates"])
def test_shared_coordinates_routes_to_bim_spec_with_content(query):
    """공유좌표(Shared Coordinates·기준점) 콘텐츠 저작 — 운영 노이즈 weak였던 것 해소.
    BIM_시방서 라우팅 + Survey Point/PBP/Acquire 내용."""
    assert server.infer_knowledge_agent_from_query(query) == "BIM_시방서"
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert ("공유좌표" in ans) or ("Survey Point" in ans) or ("기준점" in ans), ans[:120]


def test_coordination_link_stays_with_coordination_agent():
    """가드: '좌표계 정합 링크'(NWC 버전 통일 등 조율)는 설비시공조율 유지(공유좌표 규칙이 안 가로챔)."""
    assert server.infer_knowledge_agent_from_query("좌표계 정합 링크") == "설비시공조율"


@pytest.mark.parametrize("query", ["준공 BIM 납품", "as-built 모델", "준공모델 작성"])
def test_asbuilt_routes_to_bim_spec(query):
    """준공/as-built BIM 납품은 BIM_시방서(준공 납품물 체크리스트·LOD 400 보유)로 — weak였던 것 해소."""
    assert server.infer_knowledge_agent_from_query(query) == "BIM_시방서"


def test_construction_completion_inspection_not_over_captured():
    """가드: BIM 무관 '준공 검사 절차'(시공/감리)는 BIM_시방서로 안 감(bare '준공' 미추가)."""
    assert server.infer_knowledge_agent_from_query("준공 검사 절차") != "BIM_시방서"


# ── 90_확장에이전트 도메인 KB 고아 등록 연결: 파일명≠등록ID로 지식업데이트로 새던 것 ──
@pytest.mark.parametrize("query,expected", [
    ("설비 기초 개요", "설비기초"),
    ("설비 장비 BIM 파라미터", "설비장비"),
    ("건물유형별 BIM 적용기준", "건물유형별_BIM적용기준"),
    ("건물유형 공사구분 산정", "BIM_건물유형_공사구분_산정로직"),
    ("국가별 건설법규 비교", "국가별_건설법규_기준비교"),
    ("설계 지침서", "설계_지침서"),
    ("시공 지침서", "시공_지침서"),
    ("설계 시방서", "설계_시방서"),
    ("시공 시방서", "시공_시방서"),
])
def test_registered_extension_orphans_route_to_self(query, expected):
    """90_확장에이전트의 도메인 KB를 inference_only 에이전트로 등록 + 라우팅 → 운영
    기본값(지식업데이트)으로 새던 고아가 자기 KB 로 confident 도달."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query", [
    "철근 정착길이 기준",
    "철근 이음 길이",
    "정착길이 산정",
    "표준갈고리 정착",
])
def test_rebar_development_lap_content_on_topic(query):
    """철근 정착길이·이음(KDS 14 20 52) 콘텐츠 저작 — '철근' 키워드가 구조해석-BIM연동
    발췌에 confident-오답이던 off-topic 케이스 해소. 구조 라우팅 + 정착/이음 내용."""
    assert server.infer_knowledge_agent_from_query(query) == "구조"
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert ("정착길이" in ans) or ("겹침이음" in ans) or ("40d" in ans), ans[:120]


def test_bridge_expansion_joint_not_stolen_by_structure():
    """가드: '교량 신축이음'(토목 가설/별개)은 구조 정착/이음 키워드에 안 잡힌다(bare 이음 미추가)."""
    assert server.infer_knowledge_agent_from_query("교량 신축이음") != "구조"


# ── 답변-내용 정독에서 발견한 confident-오답/라우팅갭 4건(조도·슬럼프·펌프양정·변압기용량) ──
@pytest.mark.parametrize("query,expected", [
    ("조도 기준 lux", "전기"),
    ("콘크리트 슬럼프 기준", "시공_시방서"),
    ("펌프 양정 계산", "위생"),
    ("변압기 용량 산정", "전기"),
])
def test_answer_content_review_fixes_routing(query, expected):
    """답변-내용 정독으로 발견: 조도/슬럼프는 콘텐츠 있으나 라우팅 weak였고, 펌프 양정·
    변압기 용량은 confident-오답(off-topic 발췌)이었다. 라우팅 보강 + 콘텐츠 저작으로 해소."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,expected", [
    ("내화구조 시간", "건축"),
    ("내화등급 기준", "건축"),
    ("내화 성능 시간", "건축"),
    ("방화구조 기준", "건축"),
    ("피난구조 기준", "건축"),
])
def test_fire_resistance_routes_to_architecture_not_structure(query, expected):
    """'내화구조'의 '구조' 부분일치로 구조(structural, PC보 발췌)로 confident-오답이던 것 →
    건축(내화 성능시간 콘텐츠 저작)으로 우선 라우팅. PC보 등 실제 구조 질의는 구조 유지."""
    assert server.infer_knowledge_agent_from_query(query) == expected
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert ("내화시간" in ans) or ("내화구조" in ans) or ("내화등급" in ans), ans[:120]


@pytest.mark.parametrize("query", ["PC보 관통", "전이보 보강", "기둥 단면 설계"])
def test_structural_member_not_stolen_by_fire_resistance_rule(query):
    assert server.infer_knowledge_agent_from_query(query) == "구조"


@pytest.mark.parametrize("query", [
    "콘크리트 타설 온도", "콘크리트 측압", "콘크리트 피복두께", "콘크리트 혼화제", "철골 볼트 조임",
])
def test_concrete_topics_route_to_structure(query):
    """'콘크리트 X'(타설/측압/피복/혼화제)가 '콘크리트' 키워드 부재로 운영기본값으로 새던
    클래스 갭 → 콘크리트/철골/피복/측압/혼화제 구조 키워드 추가(구조.md 콘크리트 시방 보유)."""
    assert server.infer_knowledge_agent_from_query(query) == "구조"


def test_concrete_slump_still_routes_to_construction_spec():
    """가드: '콘크리트 슬럼프'는 시공_시방서 전용 규칙이 구조 '콘크리트' 키워드보다 선점."""
    assert server.infer_knowledge_agent_from_query("콘크리트 슬럼프 기준") == "시공_시방서"


@pytest.mark.parametrize("query,expected,needle", [
    ("앵커볼트 매입깊이", "구조", "앵커볼트"),
    ("용접 비파괴검사", "구조", "탐상"),
    ("초음파탐상 UT", "구조", "UT"),
])
def test_anchor_bolt_and_weld_inspection(query, expected, needle):
    """앵커볼트 매입깊이(저작)·용접 비파괴검사(UT/MT, 콘텐츠 존재 라우팅) → 구조."""
    assert server.infer_knowledge_agent_from_query(query) == expected
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert needle in ans, ans[:100]


@pytest.mark.parametrize("query,expected,needle", [
    ("콘크리트 양생기간", "구조", "양생"),
    ("습윤양생 기간", "구조", "양생"),
    ("교량 신축이음", "토목", "신축이음"),
    ("교량 받침", "토목", "받침"),
])
def test_curing_and_bridge_joint_content(query, expected, needle):
    """콘크리트 양생기간(구조)·교량 신축이음/받침(토목) 콘텐츠 저작 — weak 갭 해소.
    '배관 신축이음'(공조배관)과 'bare 신축이음' 충돌 회피(교량 신축이음 복합어)."""
    assert server.infer_knowledge_agent_from_query(query) == expected
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert needle in ans, ans[:100]


@pytest.mark.parametrize("query,expected", [
    ("취출구 종류", "공조덕트"),
    ("냉각탑 용량", "공조배관"),
    ("신축이음 배관", "공조배관"),
    ("배관 행거", "공조배관"),
    ("연결송수관 설치", "소방기계"),
    ("옥내소화전 방수압", "소방기계"),
])
def test_mep_content_topics_route_to_discipline(query, expected):
    """섹션-주제 일괄 점검에서 발견한 MEP 라우팅 갭(콘텐츠는 있으나 키워드 누락): 취출구·
    냉각탑·배관 신축이음/행거·연결송수관·옥내소화전을 해당 공종 키워드에 추가."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,expected", [
    ("교량 신축이음", "토목"),         # 교량 신축이음은 토목(콘텐츠 저작), 공조배관 '배관 신축이음'과 미충돌
    ("덕트 행거 간격", "공조덕트"),       # 덕트 행거는 공조덕트('배관 행거' 복합어로 미충돌)
])
def test_mep_keyword_additions_avoid_conflicts(query, expected):
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,expected", [
    ("급탕 순환", "위생"),
    ("소제구 간격", "위생"),
    ("간선 굵기", "전기"),
    ("부하 계산", "전기"),
    ("방수 공법", "건축"),
    ("도막방수 두께", "건축"),
    ("지반 개량", "토목"),
    ("경계 측량", "토목"),
])
def test_discipline_content_topics_route_correctly(query, expected):
    """섹션-주제 일괄 점검 — 위생/전기/건축/토목 콘텐츠 주제가 키워드 누락으로 운영기본값으로
    새던 라우팅 갭 보강(콘텐츠 존재 확인)."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query", ["공유좌표 설정", "survey point"])
def test_survey_point_stays_bim_spec_not_civil(query):
    """가드: BIM 공유좌표·Survey Point 는 BIM_시방서 유지(토목엔 'bare 측량' 대신 '경계 측량'만 추가)."""
    assert server.infer_knowledge_agent_from_query(query) == "BIM_시방서"


@pytest.mark.parametrize("query,expected", [
    ("계단실 가압 제연", "공조덕트"),
    ("부속실 급기가압", "공조덕트"),
    ("거실 제연 풍량", "공조덕트"),
    ("계단 단높이 기준", "건축"),     # 일반 계단(제연 아님)은 건축 유지
])
def test_smoke_control_vs_stair_disambiguation(query, expected):
    """가압제연/급기가압(공조덕트 제연 콘텐츠)이 '계단실'(건축 계단 키워드)에 가로채여
    confident-오답이던 것 → 제연/가압제연 우선 규칙. 일반 계단(단높이)은 건축 유지."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,expected", [
    ("수조 용량", "위생"),
    ("저수조 용량 산정", "위생"),
    ("고가수조 용량", "위생"),
    ("물탱크 용량", "위생"),
    ("팽창탱크 용량", "공조배관"),  # 팽창탱크는 공조배관 유지(수조 키워드에 안 걸림)
])
def test_water_tank_capacity_routes_to_plumbing(query, expected):
    """수조/저수조/고가수조/물탱크 용량 → 위생(용량 산정 콘텐츠 저작). 팽창탱크는 공조배관 유지."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,expected", [
    ("주차 경사로 구배", "주차장_모빌리티시설_BIM"),
    ("램프 구배 기준", "주차장_모빌리티시설_BIM"),
    ("지붕 구배 기준", "건축"),
    ("옥상 구배", "건축"),
    ("오배수 구배", "위생"),          # 배수 구배는 위생 유지
    ("배수 구배 기준", "위생"),
    ("도로 종단구배", "토목"),         # 종단구배는 토목 유지
])
def test_slope_keyword_hijack_disambiguation(query, expected):
    """'구배'가 위생(배수) 키워드라 주차 경사로/지붕 구배가 위생 오배수로 confident-오답이던
    것 → 경사로 구배→주차장(17%/14%), 지붕 구배→건축(1/50~1/100) 우선 규칙 + 콘텐츠 저작.
    배수/오배수 구배(위생)·도로 종단구배(토목)는 유지."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,expected", [
    ("회귀 테스트", "QA_테스터"),
    ("통합 테스트", "QA_테스터"),
    ("CI 파이프라인", "인프라_DevOps (Obsidian)"),
])
def test_dev_qa_infra_topics_route_correctly(query, expected):
    """AI/개발 — 회귀/통합 테스트→QA_테스터, CI 파이프라인→인프라_DevOps(ci/cd와 일관) 보강."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,expected", [
    ("공항 수하물처리", "공항_BIM"),
    ("수하물 BHS 시스템", "공항_BIM"),
    ("계류장 탑승교", "공항_BIM"),
    ("공항 연면적", "건축"),     # area 질의는 건축 유지
    ("인천공항 면적", "건축"),
])
def test_airport_facility_vs_area_boundary(query, expected):
    """공항 특화 설비(수하물/BHS/계류장/탑승교)는 공항_BIM, 면적/연면적은 건축 — 건축 '공항'
    키워드(area용)가 공항 특화 질의를 가로채던 facility-vs-discipline 경계 정정."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query", ["거푸집 존치기간", "거푸집 탈형", "동바리 존치"])
def test_formwork_routes_to_structure_with_content(query):
    """거푸집 존치기간(구조.md에 측면2일/슬래브17일/스팬6m 28일 콘텐츠 존재)이 운영
    기본값으로 새던 라우팅 갭 → 거푸집/존치/탈형/동바리 구조 키워드 추가."""
    assert server.infer_knowledge_agent_from_query(query) == "구조"
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert ("존치" in ans) or ("탈형" in ans), ans[:100]


@pytest.mark.parametrize("query,expected", [
    ("방화댐퍼 설치 기준", "공조덕트"),   # spec → 공조덕트(퓨즈온도/설치기준)
    ("방화댐퍼 퓨즈온도", "공조덕트"),
    ("방화댐퍼 이격", "간섭검토"),        # clash → 간섭검토
    ("방화댐퍼 벽체 관통", "간섭검토"),
])
def test_fire_damper_spec_vs_clash_disambiguation(query, expected):
    """방화댐퍼 '설치 기준'(spec)은 공조덕트, '이격/관통'(clash)은 간섭검토 — 기존 간섭검토
    규칙의 bare '설치'가 spec 질의를 confident-오답(Navisworks 발췌)으로 가로채던 것 해소."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,needle", [
    ("펌프 양정 계산", "전양정"),
    ("변압기 용량 산정", "수용률"),
])
def test_answer_content_review_authored_content_on_topic(query, needle):
    """저작한 펌프 양정(전양정=실양정+마찰손실)·변압기 용량(수용률/부등률) 내용이 실제 답변에 담겨야."""
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert needle in ans, ans[:120]


@pytest.mark.parametrize("query,expected", [
    ("요구사항 명세 작성", "요구사항분석"),
    ("요구사항 분석 템플릿", "요구사항분석"),
    ("External Command 구현", "Revit_Addin"),
])
def test_addin_dev_requirements_and_external_command_routing(query, expected):
    """애드인개발 — '요구사항 명세'(요구사항분석 콘텐츠 보유)·'External Command'(띄움 변형,
    Revit_Addin)가 운영기본값/프로그램개발로 새던 것 보강."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query", ["투자유치", "투자유치 IR", "IR 자료", "투자자 미팅"])
def test_investment_relations_routes_to_cfo(query):
    """'투자유치'(붙임)·IR 자료가 CFO 로 — 띄어쓴 '투자 유치'만 있어 흔한 붙임 표기가
    운영 기본값으로 새던 것 보강. CFO 가 투자유치 콘텐츠 보유."""
    assert server.infer_knowledge_agent_from_query(query) == "CFO"


@pytest.mark.parametrize("query,expected", [
    ("BIM 지침서 LOD", "BIM_지침서"),
    ("BIM 시방서 작성", "BIM_시방서"),
    ("시방서 일반 기준", "BIM_시방서"),
])
def test_bim_spec_vs_guide_disambiguation(query, expected):
    """가드: 'BIM 지침서'(BIM_지침서, LOD 상세)와 'BIM 시방서/generic 시방서'(BIM_시방서)가
    문자열로 정확히 분기되어야 한다(broad '시방서' 규칙보다 전용 규칙이 선점)."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,expected", [
    ("전기 LOD 기준", "전기"),
    ("덕트 LOD 단계", "공조덕트"),
    ("LOD 300 350 차이", "건축"),
])
def test_discipline_lod_not_stolen_by_general_lod_rule(query, expected):
    """가드: 공종/특정 LOD 질의는 해당 공종 유지(일반 LOD 규칙이 가로채지 않음)."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query", [
    "피뢰침 보호각",
    "피뢰설비 보호레벨",
    "수뢰부 인하도선",
])
def test_lightning_protection_content_reachable(query):
    """피뢰설비(KS C IEC 62305) 콘텐츠 저작 — 보호각/보호레벨/수뢰부 질의가 운영
    노이즈에 weak-오답이던 것 해소. 전기 라우팅 + 회전구체/LPL 내용."""
    assert server.infer_knowledge_agent_from_query(query) == "전기"
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert ("회전구체" in ans) or ("LPL" in ans) or ("피뢰" in ans), ans[:120]


@pytest.mark.parametrize("query", [
    "주차장 기둥 간격 기준",
    "주차단위구획 치수",
    "주차장 차로 너비",
])
def test_parking_dimension_routes_to_facility_with_content(query):
    """주차 치수(주차단위구획·차로·기둥 bay) 질의가 '기둥'→구조 / 운영기본값으로 새지
    않고 주차장 facility KB(주차장법 치수 콘텐츠)에 도달. 일반 구조 기둥 질의는 구조 유지."""
    assert server.infer_knowledge_agent_from_query(query) == "주차장_모빌리티시설_BIM"
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert ("2.5m" in ans) or ("주차단위구획" in ans), ans[:120]


@pytest.mark.parametrize("query", ["기둥 철근 정착길이", "기둥 관통 보강"])
def test_structural_column_query_not_stolen_by_parking_rule(query):
    assert server.infer_knowledge_agent_from_query(query) == "구조"


@pytest.mark.parametrize("query", [
    "피난계단 설치 기준",
    "특별피난계단 설치 대상",
])
def test_escape_stairs_content_answers_on_topic(query):
    """피난계단 질의가 '설치/기준' 키워드로 엘리베이터 샤프트 배관 발췌에 오답되던
    off-topic-confident 케이스 → 전용 콘텐츠 저작으로 해소. 건축 라우팅 + 직통/특별
    피난계단 내용을 실제로 담아야 한다."""
    assert server.infer_knowledge_agent_from_query(query) == "건축"
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert ("특별피난계단" in ans) or ("직통계단" in ans), ans[:120]


@pytest.mark.parametrize("query,expected", [
    ("설비 자동제어 기준", "설비자동제어"),
    ("자동제어 BACnet DDC 구성", "설비자동제어"),
])
def test_building_automation_orphan_reachable(query, expected):
    """설비자동제어 KB(BACnet/DDC/BMS/VAV)가 plain '자동제어' 질의에서 운영 기본값
    (지식업데이트)으로 떨어지지 않고 도달해야 한다(규칙에 기술 약어만 있고 '자동제어'
    plain 어가 없어 미라우팅되던 고아 수정)."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,expected", [
    ("4D5D BIM 의무화", "4D5D_BIM"),
    ("5D BIM 개요", "4D5D_BIM"),
    ("4D BIM 공정 시뮬레이션", "4D5D_BIM"),
])
def test_4d5d_bim_not_hijacked_by_cost_estimation(query, expected):
    """4D/5D BIM 전용 에이전트가 견적산정의 '5d' 토큰에 가로채이지 않아야 한다
    (5d/5d bim 을 견적산정→4D5D_BIM 으로 이동). 순수 견적 질의는 견적산정 유지."""
    assert server.infer_knowledge_agent_from_query(query) == expected


def test_cost_estimation_still_wins_for_pure_estimate_query():
    assert server.infer_knowledge_agent_from_query("BIM 견적 단가 물량산출 원가") == "BIM_프로젝트_견적산정"


@pytest.mark.parametrize("query,expected", [
    ("견적서 작성 방법", "견적서담당"),
    ("견적서 법적 효력 요건", "견적서담당"),
])
def test_estimate_document_agent_reachable(query, expected):
    """견적서담당(114행) 고유 KB(견적서 작성·법적효력·항목분류)가 '견적서'+작성/효력
    질의에서 산정(견적산정)·심사(견적심사원)에 가려지지 않고 도달."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,expected", [
    ("BIM 견적 산정 표준시장단가", "BIM_프로젝트_견적산정"),
    ("투입공수 물량산출", "BIM_프로젝트_견적산정"),
    ("BEP 수행계획서 작성", "BEP_수행계획서"),
])
def test_creation_agent_still_wins_without_review_intent(query, expected):
    """가드: 심사 의도어가 없는 산정/작성 질의는 여전히 산정/작성 KB 로 라우팅(심사원 규칙이 가로채지 않음)."""
    assert server.infer_knowledge_agent_from_query(query) == expected


# ── 8) C-suite: 재무 질의는 CFO 로 라우팅돼 충분한 KB 로 즉답(콘텐츠는 있는데 라우팅 누락이던 케이스) ──
@pytest.mark.parametrize("query", [
    "상용 제품 가격 정책과 손익분기 재무 분석",
    "회계 세무 처리 기준",
    "Autodesk Store 구독 수익 모델 현금흐름",
])
def test_finance_queries_route_to_cfo_and_answer_locally(query):
    assert server.infer_knowledge_agent_from_query(query) == "CFO"
    matches = server.search_local_knowledge(query, limit=3)
    answer = server.build_knowledge_answer(query, matches)
    readiness = server.assess_team_telegram_answer_readiness(query, "CFO", matches, answer)
    assert readiness["should_search"] is False, readiness["reasons"]


# ── 9) 검색셋 위생: 내부 운영/테스트 산출물이 도메인 검색에서 제외돼야 한다 ──
def test_operational_artifacts_excluded_from_search():
    from backend.knowledge_engine import knowledge_search_files
    parts_blocklist = {"reasoning_training", "internal_growth", "conflict_resolution"}
    leaked = [
        p for p in knowledge_search_files()
        if any(part in parts_blocklist for part in p.parts)
    ]
    assert not leaked, f"운영/테스트 산출물 누출: {[p.name for p in leaked[:5]]}"


@pytest.mark.parametrize("query,expected_agent", [
    ("전략기획 연간 로드맵 수립", "전략기획"),
    ("법무 계약 조항 검토", "법무조항검토"),
    ("토목 배수 구배 기준", "토목"),
])
def test_low_signal_queries_not_hijacked_by_test_artifacts(query, expected_agent):
    """AI 협업 테스트 산출물(TEST_ROUND_*)이 도메인 질의 top 을 가로채면 안 된다."""
    matches = server.search_local_knowledge(query, limit=1)
    assert matches and matches[0]["path"].stem == expected_agent, (
        matches[0]["path"].stem if matches else "no-match"
    )


# ── 10) outbound 마스킹: 고객 전달 직전 시크릿/내부경로 누출 차단(DeepSeek 검수 OFF 대비) ──
@pytest.mark.parametrize("secret", [
    "sk-abc123DEF456ghi789JKL012mno345",
    "GOCSPX-abcdefghij1234567890",
    "ya29.a0AfH6SMxyz_longtoken_here",
    "AKIAIOSFODNN7EXAMPLE",
])
def test_outbound_masks_secrets(secret):
    from backend.text_utils import sanitize_outbound_text
    out = sanitize_outbound_text(f"답변 내용 {secret} 끝")
    assert secret not in out
    assert "[SECRET_MASKED]" in out


def test_outbound_masks_internal_path_but_keeps_relative():
    from backend.text_utils import sanitize_outbound_text
    out = sanitize_outbound_text("경로 /Users/foo/LUA BIM LABS/.env 와 knowledge/10_agents/전기.md")
    assert "/Users/foo" not in out
    assert "[PATH_MASKED]" in out
    assert "knowledge/10_agents/전기.md" in out  # 상대경로는 정상 보존


# ── 11) 답변 잘림: max_chars 캡이 문장/단어 중간을 자르지 않아야 한다 ──
def test_clean_truncate_keeps_short_text():
    from backend.knowledge_engine import _clean_truncate
    assert _clean_truncate("짧은 문장입니다.", 100) == "짧은 문장입니다."


def test_clean_truncate_cuts_at_boundary_not_midword():
    from backend.knowledge_engine import _clean_truncate
    text = "첫 문장입니다.\n둘째 줄 내용이 이어집니다.\n셋째 줄은 관경(이런식으로 길게"
    out = _clean_truncate(text, 25)
    assert not out.rstrip().endswith("관경(")
    assert len(out) <= 26 or out.endswith("…")


def test_excerpts_have_no_midword_truncation():
    """실제 KB excerpt 가 2400자 캡에서 '관경(' 처럼 단어/문장 중간에 끊기면 안 된다."""
    from backend.knowledge_engine import extract_relevant_excerpt, knowledge_search_files
    bad = []
    for p in knowledge_search_files()[:120]:
        t = p.read_text(encoding="utf-8", errors="ignore")
        ex = extract_relevant_excerpt(t, ["기준", "설계", "배관", "전기"], max_chars=2400).rstrip()
        if ex.endswith(("(", "[", "을", "를", "이가")):
            bad.append(p.stem)
    assert not bad, f"단어 중간 잘림: {bad[:5]}"


# ── 12) 자동저장 중복 가드: KB부족 라이브 경로가 같은 내용을 반복 적재하지 않아야 ──
def test_auto_save_skips_duplicate_content(tmp_path, monkeypatch):
    monkeypatch.setenv("KNOWLEDGE_BASE_DIR", str(tmp_path))
    import importlib
    import backend.core.paths as paths
    importlib.reload(paths)
    import backend.knowledge_store as ks
    importlib.reload(ks)
    import backend.web_search as ws
    importlib.reload(ws)

    agent = "건축"
    content = ("• [Naver] 테스트 제목\n  중복 판정용으로 충분히 긴 본문 라인 "
               "http://example.com/x\n  출처: http://example.com/x")
    ws._save_search_result_to_knowledge(agent, "q", content)
    path = ks.knowledge_file_path(agent)
    size1 = __import__("os").path.getsize(path)
    ws._save_search_result_to_knowledge(agent, "q", content)
    size2 = __import__("os").path.getsize(path)
    assert size1 == size2, "중복 내용이 다시 적재됨"

    # 원래 환경 복구
    monkeypatch.delenv("KNOWLEDGE_BASE_DIR", raising=False)
    importlib.reload(paths)
    importlib.reload(ks)
    importlib.reload(ws)


# ── 13) 지연 excerpt 최적화: 반환 매치는 excerpt 보유, 내부 임시필드는 노출 안 됨 ──
def test_returned_matches_have_excerpt_and_no_temp_field():
    """excerpt 를 top-limit 에만 계산하는 최적화 후에도 반환 매치는 정상 excerpt 를
    갖고, 내부 임시 콘텐츠 필드(_content)는 누출되지 않아야 한다."""
    matches = server.search_local_knowledge("분전반 케이블 트레이 충전율", limit=3)
    assert matches
    for m in matches:
        assert m.get("excerpt"), "excerpt 누락"
        assert "_content" not in m, "내부 임시필드 누출"


# ── 14) 덕트 정압: 설계(손실)는 공조덕트, 제어(센서/VAV)는 설비자동제어로 분리 ──
@pytest.mark.parametrize("query,expected_agent", [
    ("급기덕트 정압 손실 계산", "공조덕트"),
    ("덕트 정압 손실 사이징", "공조덕트"),
    ("급기덕트 풍량 밸런싱", "공조덕트"),
    ("VAV 박스 최소풍량 제어", "설비자동제어"),
    ("정압 센서 setpoint 시퀀스", "설비자동제어"),
    ("BMS point list 작성", "설비자동제어"),
])
def test_duct_static_pressure_design_vs_controls_split(query, expected_agent):
    """'덕트 정압' 광범위 키워드가 덕트 설계 질의까지 설비자동제어로 보내던 문제 방지."""
    assert server.infer_knowledge_agent_from_query(query) == expected_agent


# ── 15) 콘텐츠는 충분한데 라우팅 누락이던 관리/상용화 에이전트(법무·패키징·스토어심사) ──
@pytest.mark.parametrize("query,expected_agent", [
    ("EULA 면책조항 작성 기준", "법무조항검토"),
    ("약관 저작권 검토", "법무조항검토"),
    ("MSI 인스톨러 코드 서명", "제품패키징"),
    ("설치 프로그램 패키징 구성", "제품패키징"),
    ("스토어 심사 체크리스트", "스토어심사"),
    ("앱스토어 심사 제출 기준", "스토어심사"),
])
def test_commercialization_agents_route_and_answer_locally(query, expected_agent):
    assert server.infer_knowledge_agent_from_query(query) == expected_agent
    matches = server.search_local_knowledge(query, limit=3)
    answer = server.build_knowledge_answer(query, matches)
    readiness = server.assess_team_telegram_answer_readiness(query, expected_agent, matches, answer)
    assert readiness["should_search"] is False, readiness["reasons"]


def test_commercialization_rules_do_not_steal_other_domains():
    """신규 관리 라우팅 규칙이 공종/타 에이전트 질의를 가로채지 않아야 한다."""
    assert server.infer_knowledge_agent_from_query("스프링클러 살수반경") == "소방기계"
    assert server.infer_knowledge_agent_from_query("철근 정착길이 이음") == "구조"
    assert server.infer_knowledge_agent_from_query("계약 외주 협력사 관리") == "외주관리"


@pytest.mark.parametrize("query,expected_agent", [
    ("월별 경비 영수증 자동분류", "경비정산_AI"),
    ("지출 정산 집계 기준", "경비정산_AI"),
    ("해외진출 현지화 우선순위", "글로벌_유통기획관"),
    ("Obsidian 지식그래프 자동동기화", "인프라_DevOps (Obsidian)"),
    ("devops ci/cd 파이프라인 구성", "인프라_DevOps (Obsidian)"),
])
def test_more_management_agents_route_locally(query, expected_agent):
    assert server.infer_knowledge_agent_from_query(query) == expected_agent
    matches = server.search_local_knowledge(query, limit=3)
    answer = server.build_knowledge_answer(query, matches)
    readiness = server.assess_team_telegram_answer_readiness(query, expected_agent, matches, answer)
    assert readiness["should_search"] is False, readiness["reasons"]


def test_global_distribution_rule_does_not_steal_revenue_agent():
    """'글로벌 유통'(특화어)만 잡고 바로 '글로벌'은 글로벌_매출관리원을 안 뺏어야 한다."""
    assert server.infer_knowledge_agent_from_query("글로벌 매출 성장 관리") == "글로벌_매출관리원"


# ── 16) 한국어 '의' 조사 처리: 'X의'가 'X'로 정규화돼 scoring 손실을 막아야 ──
def test_genitive_particle_stripped_for_scoring():
    from backend.knowledge_engine import query_terms
    assert "분전반" in query_terms("분전반의 작업공간은")
    assert "덕트" in query_terms("덕트의 정압손실")


def test_short_words_with_eui_not_overstripped():
    """2자어(정의·협의·회의)는 '의' 제거 가드로 보호돼야 한다."""
    from backend.knowledge_engine import query_terms
    assert "정의" in query_terms("정의 확인")
    assert "협의" in query_terms("협의 절차")


@pytest.mark.parametrize("with_particle,without", [
    ("분전반의 작업공간은", "분전반 작업공간"),
    ("스프링클러의 헤드 간격은", "스프링클러 헤드 간격"),
    ("위생의 통기관 봉수는", "위생 통기관 봉수"),
])
def test_particle_query_scores_match_plain(with_particle, without):
    """'의' 조사 정규화가 도메인 확장까지 반영돼, 조사 유무 점수가 거의 같아야 한다."""
    sa = server.search_local_knowledge(with_particle, limit=1)[0]["score"]
    sb = server.search_local_knowledge(without, limit=1)[0]["score"]
    assert abs(sa - sb) <= 8, f"{with_particle}={sa} vs {without}={sb}"


# ── 17) 무지식 graceful: 웹 실패 시 off-topic 약매칭을 답으로 내보내면 안 된다 ──
def test_combined_answer_rejects_offtopic_weak_local_on_web_failure():
    """'양자컴퓨터'처럼 도메인 밖 질의는 웹 실패 시 약한 로컬매칭(score<18)을
    답으로 내보내지 말고 '찾지 못함'을 반환해야 한다(엉뚱한 답 방지)."""
    from backend.knowledge_engine import build_combined_answer
    q = "양자컴퓨터 큐비트 오류정정 알고리즘"
    matches = server.search_local_knowledge(q, limit=3)
    answer = build_combined_answer(q, "", matches)
    assert "찾지 못" in answer, answer


def test_combined_answer_keeps_strong_local_on_web_failure():
    """가드: 강한 로컬매칭은 웹 실패 시에도 그대로 답으로 유지돼야 한다."""
    from backend.knowledge_engine import build_combined_answer
    q = "스프링클러 헤드 살수반경"
    matches = server.search_local_knowledge(q, limit=3)
    answer = build_combined_answer(q, "", matches)
    assert "찾지 못" not in answer and len(answer) > 50


def test_combined_answer_rejects_borderline_offtopic():
    """경계 off-topic(운영 노이즈에 score 18~27로 약매칭되는 일상 질의)도 웹 실패 시
    confident 로컬 답변으로 내보내면 안 된다(_WEAK_LOCAL_SCORE=32 가드)."""
    from backend.knowledge_engine import build_combined_answer
    for q in ["양자컴퓨터 큐비트가 뭐야", "오늘 점심 메뉴 추천해줘", "축구 경기 결과 알려줘"]:
        matches = server.search_local_knowledge(q, limit=3)
        answer = build_combined_answer(q, "", matches)
        assert "찾지 못" in answer, (q, answer[:120])


def test_fire_discharge_pressure_not_hijacked_by_waterproofing():
    """'방수압'(放水壓, 소방 방수 압력)이 건축 '방수'(防水, 방수공사) discipline 키워드의
    substring 매칭으로 건축에 가로채이면 안 된다(cycle4 클래스). 소방 방수압/방수량은
    소방기계로, 설비별 법정 수치(연결송수관 0.35·옥내소화전 0.17 MPa)가 답변에 있어야 한다."""
    from backend.knowledge_engine import infer_knowledge_agent_from_query as inf, build_knowledge_answer
    assert inf("연결송수관 방수압") == "소방기계"
    assert inf("옥내소화전 방수압") == "소방기계"
    # 가드: 진짜 방수공사(防水)는 건축 유지.
    assert inf("방수 디테일") == "건축"
    assert inf("도막방수 공법") == "건축"
    # 설비별 방수압 수치가 답변에 정확히 분리돼 있어야(스프링클러 0.1과 혼동 금지).
    a = build_knowledge_answer("연결송수관 방수압", server.search_local_knowledge("연결송수관 방수압", limit=4))
    assert "0.35" in a
    a2 = build_knowledge_answer("옥내소화전 방수압", server.search_local_knowledge("옥내소화전 방수압", limit=4))
    assert "0.17" in a2


def test_english_hydrant_resolves_without_misroute():
    """영문 단일-도메인 소방어(hydrant→소화전)는 로컬 연결. 단 전기 영문어(conduit 등)는
    bare '전기' 확장이 공조배관 '전기트레이'를 hijack 하므로 backlog(웹) — conduit 질의가
    공조배관 냉매배관 답변을 confident 로 내보내면 안 된다(cycle310 회귀 가드)."""
    from backend.knowledge_engine import build_combined_answer
    m = server.search_local_knowledge("fire hydrant pressure", limit=3)
    assert "찾지 못" not in build_combined_answer("fire hydrant pressure", "", m)
    # conduit 은 공조배관 냉매배관 답변으로 새지 않는다(웹 폴백이 정답).
    a = build_combined_answer("conduit fill ratio", "", server.search_local_knowledge("conduit fill ratio", limit=3))
    assert "냉매배관" not in a


def test_conduit_routes_to_electrical():
    """'전선관'(conduit) 질의는 전기로 라우팅돼야 한다(콘텐츠 15회 보유). cycle116 에서
    '전선관리' substring 우려로 보류했으나 '전선관리'는 KB 토픽도 아니고 전기-인접이라
    재검증 후 추가. '전선 관리'(공백)는 전선관과 매칭되지 않는다."""
    from backend.knowledge_engine import infer_knowledge_agent_from_query as inf, build_combined_answer
    for q in ["전선관 충전율 기준", "전선관 굵기"]:
        assert inf(q) == "전기", q
        assert "찾지 못" not in build_combined_answer(q, "", server.search_local_knowledge(q, limit=3)), q


def test_common_typo_variants_route_correctly():
    """흔한 오타/표기 변형(분전판→분전반, 커텐월→커튼월)도 라우팅 정규화로 올바른
    공종에 연결돼야 한다(canonical 이 content-backed 일 때)."""
    from backend.knowledge_engine import infer_knowledge_agent_from_query as inf, build_combined_answer
    assert inf("분전판 결선 기준") == "전기"
    assert inf("커텐월 누수 디테일") == "건축"
    for q in ["분전판 결선 기준", "커텐월 누수 디테일"]:
        matches = server.search_local_knowledge(q, limit=3)
        assert "찾지 못" not in build_combined_answer(q, "", matches), q


@pytest.mark.parametrize("query,expect", [
    ("안녕하세요", "Lua"), ("안녕", "Lua"), ("반갑습니다", "Lua"), ("수고하세요", "Lua"),
    ("고맙습니다", "다행"), ("감사합니다", "다행"), ("고마워요", "다행"), ("땡큐", "다행"),
])
def test_greeting_and_thanks_get_social_reply(query, expect):
    """인사/감사 같은 사회적 발화는 '찾지 못함' 대신 친근한 결정적 응답을 준다(고객 접점 UX)."""
    ans = server.identity_answer(query)
    assert ans is not None and expect in ans


@pytest.mark.parametrize("query", [
    "감사원 감사 절차", "감사 보고서 작성", "안녕 빌딩 BIM 자료", "반가워 프로젝트 연면적",
])
def test_social_reply_not_triggered_by_domain_queries(query):
    """가드: '감사 보고서'·'안녕 빌딩' 처럼 사회어가 도메인 질의에 섞이면 사회응답 미발화."""
    assert server.identity_answer(query) is None


@pytest.mark.parametrize("query", [
    "BIM이 뭐예요", "BIM 왜 써요", "BIM 처음인데 뭐부터 배워야 하나요", "BIM 도입 효과",
])
def test_bim_basics_onboarding_answered(query):
    """신규 고객의 기초/온보딩 질의(BIM이란/왜/처음)는 BIM_지침서 입문 가이드로 연결돼
    'BIM은 정보가 붙은 3D 모델' 수준의 답을 줘야 한다(이전엔 전부 '찾지 못함')."""
    from backend.knowledge_engine import infer_knowledge_agent_from_query as inf, build_combined_answer
    assert inf(query) == "BIM_지침서", query
    a = build_combined_answer(query, "", server.search_local_knowledge(query, limit=4))
    assert "찾지 못" not in a and "BIM" in a


@pytest.mark.parametrize("query,expect_not", [
    ("BIM 물량 산출", "BIM_지침서"),   # 엑셀자동화
    ("스프링클러 BIM 간섭", "BIM_지침서"),  # 간섭검토
])
def test_bim_basics_rule_does_not_hijack_domain(query, expect_not):
    """가드: 기초 라우팅이 도메인 BIM 질의(물량/간섭)를 가로채지 않는다."""
    from backend.knowledge_engine import infer_knowledge_agent_from_query as inf
    assert inf(query) != expect_not


def test_privacy_routes_to_legal_agent():
    """개인정보 처리방침/GDPR 은 법무조항검토에 콘텐츠가 있다(처리방침 15회). 라우팅
    누락으로 default(지식업데이트)로 새던 것 → 법무 라우팅으로 confident 로컬 답변."""
    from backend.knowledge_engine import build_combined_answer, infer_knowledge_agent_from_query as inf
    for q in ["개인정보 처리방침", "개인정보 수집 동의", "GDPR 대응"]:
        assert inf(q) == "법무조항검토", q
        matches = server.search_local_knowledge(q, limit=3)
        assert "찾지 못" not in build_combined_answer(q, "", matches), q
    # 가드: 기존 법무어(계약/저작권)는 그대로 법무.
    assert inf("계약서 검토") == "법무조항검토"


def test_korean_phonetic_abbreviations_resolve():
    """한글 음역 약어(엘오디/아이에프씨)도 영문 약어(LOD/IFC)와 동등하게 로컬 답변에
    연결돼야 한다(한국 고객이 'LOD' 대신 '엘오디'로 흔히 타이핑). 웹검색 낭비 방지."""
    from backend.knowledge_engine import build_combined_answer
    for q in ["엘오디 단계 구분", "아이에프씨 내보내기"]:
        matches = server.search_local_knowledge(q, limit=3)
        answer = build_combined_answer(q, "", matches)
        assert "찾지 못" not in answer, (q, answer[:120])
    # 가드: 공종+LOD 는 공종이 선점, explode 의 'lod' substring 은 미발화.
    from backend.knowledge_engine import infer_knowledge_agent_from_query as inf
    assert inf("전기 엘오디 기준") == "전기"
    assert inf("아이에프씨 좌표계") == "IFC_OpenBIM"
    assert inf("폭발물 explode 처리") != "BIM_시방서"


def test_excerpt_strips_kst04_guardrail_marker():
    """auto-enrich KST04 가드레일 라인은 내부 거버넌스 마커이므로 고객 답변(발췌)에
    노출되면 안 된다. 단 'KST01~KST04 검증' 같은 방법론 본문은 보존돼야 한다."""
    from backend.knowledge_engine import extract_relevant_excerpt
    content = (
        "## 무료 체험 안내\n"
        "- Source: auto-enrich via Naver 2026-06-22\n"
        "- KST04 자동수집: 공식 출처/담당자 검증 전 고객 확정 답변, 납품 기준, 견적 기준으로 사용 금지.\n\n"
        "BIM Command Center 무료 체험 기간은 30일이며 5 seats 까지 사용할 수 있다.\n"
    )
    excerpt = extract_relevant_excerpt(content, ["무료", "체험", "기간"], query="무료 체험 기간")
    assert "KST04 자동수집" not in excerpt
    assert "30일" in excerpt
    # 방법론 본문의 KST01~KST04 표기는 보존(노이즈 마커가 아님).
    methodology = "## 업데이트 루프\n수집, KST01~KST04 검증, QA 승격, 회귀, 폐기 5단계로 운영한다.\n"
    m_excerpt = extract_relevant_excerpt(methodology, ["업데이트", "루프", "검증"], query="업데이트 루프")
    assert "KST01~KST04 검증" in m_excerpt


# ── 18) BIMobject 316KB 카탈로그 magnet: 도메인 질의(특히 영문) 가로채면 안 됨 ──
@pytest.mark.parametrize("query", [
    "fire compartment penetration sealing",
    "duct static pressure loss",
    "cable tray fill rate",
])
def test_bimobject_index_not_magnet_for_domain_queries(query):
    matches = server.search_local_knowledge(query, limit=2)
    top_stems = [m["path"].stem for m in matches[:2]]
    assert "BIMobject_패밀리_인덱스" not in top_stems, top_stems


def test_bimobject_index_still_available_for_family_queries():
    """가드: 패밀리/라이브러리 검색 의도 질의는 패밀리 관련 에이전트로 가야 한다."""
    agent = server.infer_knowledge_agent_from_query("BIMobject 패밀리 라이브러리 찾기")
    matches = server.search_local_knowledge("BIMobject 패밀리 라이브러리 찾기", limit=1)
    # 패밀리 관련 에이전트(BIMobject 인덱스 또는 Revit_Family제작 등)면 정상
    assert matches and ("패밀리" in matches[0]["path"].stem or "Family" in matches[0]["path"].stem)


# ── 19) 자동저장 오염 가드: 웹 결과의 중국어/토큰 오염을 KB 에 들이지 않아야 ──
def test_auto_save_blocks_contaminated_content(tmp_path, monkeypatch):
    monkeypatch.setenv("KNOWLEDGE_BASE_DIR", str(tmp_path))
    import importlib
    import backend.core.paths as paths
    importlib.reload(paths)
    import backend.knowledge_store as ks
    importlib.reload(ks)
    import backend.web_search as ws
    importlib.reload(ws)

    agent = "건축"
    dirty = "这是中文内容测试污染防护机制是否正常工作的测试文本内容"
    ws._save_search_result_to_knowledge(agent, "q", dirty)
    path = ks.knowledge_file_path(agent)
    import os
    saved_dirty = os.path.exists(path) and dirty in open(path, encoding="utf-8").read()
    assert not saved_dirty, "중국어 오염이 KB 에 저장됨"

    clean = "피난계단 유효폭은 1.2m 이상으로 충분히 긴 정상 한국어 본문 http://x.com"
    ws._save_search_result_to_knowledge(agent, "q2", clean)
    assert clean[:20] in open(path, encoding="utf-8").read()

    monkeypatch.delenv("KNOWLEDGE_BASE_DIR", raising=False)
    importlib.reload(paths)
    importlib.reload(ks)
    importlib.reload(ws)


# ── 20) 영문 BIM 용어→한글 확장: 영문 질의가 올바른 한글 KB 도메인으로 연결 ──
@pytest.mark.parametrize("query,expected_top", [
    ("fire compartment penetration sealing", "소방기계"),
    ("rebar development length lap splice", "구조"),
    ("structural beam clash coordination", "간섭검토"),
])
def test_english_query_reaches_correct_korean_domain(query, expected_top):
    """글로벌 제품 영문 질의가 BIMobject 카탈로그가 아니라 올바른 공종 KB 로 가야 한다."""
    matches = server.search_local_knowledge(query, limit=1)
    assert matches and matches[0]["path"].stem == expected_top, (
        matches[0]["path"].stem if matches else "no-match"
    )


def test_english_expansion_does_not_regress_korean():
    assert server.infer_knowledge_agent_from_query("스프링클러 살수반경") == "소방기계"
    assert server.search_local_knowledge("분전반 작업공간", limit=1)[0]["score"] >= 80


@pytest.mark.parametrize("query,leaked_term", [
    ("product roadmap strategy", "덕트"),   # 'duct' in 'product'
    ("event management plan", "통기"),       # 'vent' in 'event'
    ("prevent data loss", "통기"),
])
def test_english_expansion_no_substring_false_match(query, leaked_term):
    """'product'→duct, 'event'→vent 같은 부분문자열 오매칭이 없어야 한다(접두매칭)."""
    from backend.knowledge_engine import query_terms
    assert leaked_term not in query_terms(query)


def test_english_expansion_handles_plural():
    """복수형(ducts)도 접두매칭으로 한글 동의어가 붙어야 한다."""
    from backend.knowledge_engine import query_terms
    assert "덕트" in query_terms("ducts pressure loss")


@pytest.mark.parametrize("query,expected_top", [
    ("telecom MDF IDF separation", "통신"),
    ("hvac duct pressure", "공조덕트"),
])
def test_english_domain_nouns_reach_correct_agent(query, expected_top):
    matches = server.search_local_knowledge(query, limit=1)
    assert matches and matches[0]["path"].stem == expected_top


@pytest.mark.parametrize("query,leaked", [
    ("enable feature toggle", "케이블"),   # 'cable' in 'enable'
    ("betray trust issue", "트레이"),       # 'tray' in 'betray'
    ("portray the design", "트레이"),
])
def test_cable_tray_english_no_substring_false_match(query, leaked):
    from backend.knowledge_engine import query_terms
    assert leaked not in query_terms(query)


# ── 21) read_agent_knowledge tail 절단이 문장 중간에서 시작하지 않아야(깨끗한 컨텍스트) ──
def test_read_agent_knowledge_clean_line_start():
    """큰 KB 의 tail 컨텍스트가 줄 경계에서 시작해야 한다(중간잘림 방지)."""
    from backend.agent_routing import read_agent_knowledge
    for agent in ["소방기계", "공조배관", "전기"]:
        k = read_agent_knowledge(agent)
        assert k, f"{agent} KB 비어있음"
        first = k.splitlines()[0]
        # 줄이 완결적(마크다운 라인 시작 또는 충분히 긴 완성 문장). 깨진 1~2글자 시작 배제.
        assert first.startswith(("- ", "#", "*", "|", "•")) or len(first) > 10, first


def test_read_agent_knowledge_special_char_agents():
    """특수문자 에이전트도 자기 KB 를 로드해야 한다(safe_agent_stem 경유)."""
    from backend.agent_routing import read_agent_knowledge
    for agent in ["고객지원 CS", "인프라_DevOps (Obsidian)"]:
        assert read_agent_knowledge(agent), f"{agent} KB 미로드"


# ── 22) stream_claude 컴포지션: 전체 KB 점수화로 세부주제 섹션을 골라야(recency 편향 제거) ──
@pytest.mark.parametrize("agent,query,want_in_heading", [
    ("소방기계", "스프링클러 헤드 살수반경 기준", "살수반경"),
    ("전기", "분전반 작업공간 확보 거리", "분전반"),
])
def test_compose_knowledge_picks_specific_section(agent, query, want_in_heading):
    """tail 만 보면 오래된 큐레이션 섹션이 잘려 '기본 기준'이 뽑힌다. 전체 KB
    점수화로 구체 세부주제 섹션이 최상위로 와야 한다."""
    import re
    import backend.ai_pipeline as ap
    knowledge = server.read_agent_knowledge(agent)
    resp = ap._compose_knowledge_response(agent, query, knowledge)
    first = re.search(r"▶ (.+)", resp)
    assert first and want_in_heading in first.group(1), resp[:200]


# ── 23) _extract_agent_name: 대괄호는 유효 에이전트만 채택, 아니면 fall-through ──
@pytest.mark.parametrize("role,expected", [
    ("LUA BIM LABS CEO", "CEO"),
    ("총괄 PM 조율차장", "조율차장"),
    ("[소방기계] 검토", "소방기계"),
    ("[urgent] 소방기계 질문", "소방기계"),   # 비에이전트 대괄호 → 평문에서 탐색
    ("[비에이전트랜덤] 텍스트", ""),
])
def test_extract_agent_name_bracket_validation(role, expected):
    import backend.ai_pipeline as ap
    assert ap._extract_agent_name(role) == expected


# ── 24) infer_target_agent: 'test'가 'latest'/'contest'를 빌드검증으로 오배정하면 안 됨 ──
@pytest.mark.parametrize("text", ["latest BIM features", "contest 일정 안내"])
def test_infer_target_agent_test_word_boundary(text):
    import backend.ai_pipeline as ap
    assert ap.infer_target_agent(text) != "빌드검증"


@pytest.mark.parametrize("text", ["test case 작성", "unit test 시나리오", "QA 검증 항목"])
def test_infer_target_agent_real_test_still_routes(text):
    import backend.ai_pipeline as ap
    assert ap.infer_target_agent(text) == "빌드검증"


@pytest.mark.parametrize("text,not_agent", [
    ("special features 추가", "요구사항분석"),   # 'spec' in 'special'
    ("inspection report 검토", "요구사항분석"),
    ("perspective view 설정", "요구사항분석"),
    ("outdoor unit 실외기 배치", "건축"),          # 'door' in 'outdoor'
    ("indoor 공조기 위치", "건축"),
])
def test_infer_target_agent_no_substring_misroute(text, not_agent):
    import backend.ai_pipeline as ap
    assert ap.infer_target_agent(text) != not_agent


@pytest.mark.parametrize("text,agent", [
    ("specification 명세서", "요구사항분석"),
    ("spec sheet 작성", "요구사항분석"),
    ("door 위치 검토", "건축"),
])
def test_infer_target_agent_real_spec_door_still_route(text, agent):
    import backend.ai_pipeline as ap
    assert ap.infer_target_agent(text) == agent


# ── 25) agent_routing substring: cs(docs/metrics), excel(excellent) 오매칭 방지 ──
@pytest.mark.parametrize("text", ["docs 업데이트", "metrics 분석", "physics 검토"])
def test_has_explicit_support_channel_cs_word_boundary(text):
    import backend.agent_routing as r
    assert r.has_explicit_support_channel(text) is False


@pytest.mark.parametrize("text", ["cs 문의 답변", "고객 문의 응대"])
def test_has_explicit_support_channel_real_cs(text):
    import backend.agent_routing as r
    assert r.has_explicit_support_channel(text) is True


def test_excel_automation_not_triggered_by_excellent():
    import backend.agent_routing as r
    assert r.is_management_excel_automation_request("excellent work 정리해줘") is False
    assert r.is_management_excel_automation_request("엑셀 보고서 자동화") is True


def test_infer_target_agent_excel_word_boundary():
    """infer_target_agent 의 'excel' 도 'excellent' 에 오매칭되면 안 된다."""
    import backend.ai_pipeline as ap
    assert ap.infer_target_agent("excellent work 정리") != "엑셀자동화"
    assert ap.infer_target_agent("엑셀 리포트 자동화") == "엑셀자동화"


# ── 26) 분전반 작업공간 질의는 '작업공간' 섹션, 누수 질의는 '배관' 섹션(조건부 확장) ──
def test_panel_workspace_query_picks_access_space_section():
    """'분전반 작업공간'은 작업공간/접근공간 섹션이어야(냉수배관 섹션 아님).
    누수/배관 확장이 작업공간 질의를 배관 섹션으로 끌면 안 된다."""
    q = "분전반 앞 작업공간 얼마나 확보해야 하나요"
    head = server.build_knowledge_answer(q, server.search_local_knowledge(q, limit=1)).splitlines()[0]
    assert "배관" not in head, head
    assert "공간" in head, head


def test_panel_water_query_still_picks_pipe_section():
    """가드: 누수/배관 맥락 질의는 여전히 배관 이격 섹션이어야 한다."""
    q = "분전반 위 냉수 배관 누수 위험"
    head = server.build_knowledge_answer(q, server.search_local_knowledge(q, limit=1)).splitlines()[0]
    assert "배관" in head, head


# ── 27) Revit API 트랜잭션: 한글 질의가 영문 'Transaction 처리' 섹션을 찾아야 ──
@pytest.mark.parametrize("query", [
    "Revit 애드인에서 트랜잭션 처리 어떻게 하나요",
    "Revit 트랜잭션 commit rollback 처리",
])
def test_revit_transaction_query_surfaces_transaction_section(query):
    """한글 '트랜잭션'→영문 매핑 + 길이보너스 + 조건부 assistant 부스트로
    'Transaction 처리' 섹션이 떠야 한다(LUA Assistant 연동 섹션이 가리면 안 됨)."""
    answer = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert "transaction" in answer.lower() or "트랜잭션" in answer, answer.splitlines()[0]


def test_revit_integration_query_still_picks_assistant_section():
    """가드: 실제 연동/설치 질의는 여전히 Revit Assistant 섹션이어야 한다."""
    q = "Revit 어시스턴트 연동 설치 방법"
    head = server.build_knowledge_answer(q, server.search_local_knowledge(q, limit=1)).splitlines()[0]
    assert "assistant" in head.lower() or "연동" in head, head


# ── 28) 패밀리 파라미터 질의는 placement(배치) 확장에 끌리지 않아야 ──
def test_family_parameter_query_not_pulled_by_placement():
    """'패밀리 파라미터 공유'는 배치/로드 확장에 끌리지 말고 파라미터 내용을 답해야."""
    q = "Revit 패밀리 파라미터 공유 어떻게 설정하나요"
    answer = server.build_knowledge_answer(q, server.search_local_knowledge(q, limit=1))
    assert "파라미터" in answer or "parameter" in answer.lower(), answer.splitlines()[0]


def test_family_placement_query_still_works():
    """가드: 실제 배치/로드 질의는 placement 섹션으로 가야 한다."""
    q = "패밀리를 폴더 하위에 배치하는 다이나모"
    answer = server.build_knowledge_answer(q, server.search_local_knowledge(q, limit=1))
    assert "배치" in answer or "로드" in answer or "load" in answer.lower()


# ── 29) 소방 장비(소화펌프/소화전)는 소방기계로 — 위생 '펌프'가 선점하면 안 됨 ──
@pytest.mark.parametrize("query", [
    "소화펌프 양정 토출량",
    "소방 펌프 양정",
    "소방펌프 토출량",
    "옥내소화전 방수압",
    "소화수조 수원 산정",
    "소화전 설치 기준",
])
def test_fire_equipment_routes_to_fire_mechanical(query):
    assert server.infer_knowledge_agent_from_query(query) == "소방기계"


@pytest.mark.parametrize("query", ["급수 펌프 양정", "부스터 펌프 압력"])
def test_plumbing_pump_still_routes_to_plumbing(query):
    """가드: 위생 펌프 질의는 여전히 위생으로 가야 한다."""
    assert server.infer_knowledge_agent_from_query(query) == "위생"


# ── 30) bare '배관' magnet 제거: 공종별 배관이 올바른 공종으로 ──
@pytest.mark.parametrize("query,expected", [
    ("소방 배관 관경", "소방기계"),
    ("공조 배관 보온", "공조배관"),
    ("냉각수 배관 이격", "공조배관"),
    ("위생 배관 계통", "위생"),
    ("오배수 배관 구배", "위생"),
])
def test_pipe_queries_route_by_discipline_not_generic(query, expected):
    """공조배관의 bare '배관' 키워드가 모든 배관 질의를 가로채던 것 회귀 방지."""
    assert server.infer_knowledge_agent_from_query(query) == expected


# ── 31) bare '밸브'/'단열' magnet 제거: 밸브가 공종별로 분기 ──
@pytest.mark.parametrize("query,expected", [
    ("소방 밸브 개폐 점검", "소방기계"),
    ("알람밸브 작동", "소방기계"),
    ("냉각수 밸브 개폐", "공조배관"),
    ("급수 밸브 수격", "위생"),
])
def test_valve_queries_route_by_discipline(query, expected):
    """공조배관 bare '밸브'가 소방/위생 밸브를 가로채던 것 회귀 방지."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,expected", [
    ("외벽 단열 두께", "건축"),
    ("단열재 화재 등급", "건축"),
    ("냉매 단열 두께", "공조배관"),
    ("냉매 배관 단열", "공조배관"),
])
def test_building_vs_pipe_insulation_routing(query, expected):
    """건축 열적 단열(외벽/단열재)과 공조배관 배관단열(냉매)이 정확히 분기돼야."""
    assert server.infer_knowledge_agent_from_query(query) == expected


# ── 32) HR/마케팅 라우팅: 채용·이력서→HR, 마케팅·브랜드→브랜드마케팅 ──
@pytest.mark.parametrize("query,expected", [
    ("신입 BIM 엔지니어 채용 평가 기준", "HR_인재분석관"),
    ("이력서 분석 채용", "HR_인재분석관"),
    ("마케팅 캠페인 기획", "브랜드마케팅"),
    ("브랜드 마케팅 콘텐츠", "브랜드마케팅"),
])
def test_hr_marketing_routing(query, expected):
    assert server.infer_knowledge_agent_from_query(query) == expected


# ── 33) 스토어심사(영문 Store/등록 변형)·외주관리 라우팅 ──
@pytest.mark.parametrize("query,expected", [
    ("Autodesk Store 심사 제출", "스토어심사"),
    ("앱스토어 등록 심사", "스토어심사"),
    ("외주 협력사 계약", "외주관리"),
    ("하도급 발주 관리", "외주관리"),
])
def test_store_and_outsource_routing(query, expected):
    assert server.infer_knowledge_agent_from_query(query) == expected


def test_partner_relations_not_confused_with_outsource():
    """가드: 협력사 안부/관계는 협력사안부, 외주/하도급은 외주관리."""
    assert server.infer_knowledge_agent_from_query("협력사 안부 관계 관리") == "협력사안부"


# ── 36) 테크니컬_라이터(기술문서) vs 배포문서(설치/배포) 분기 ──
@pytest.mark.parametrize("query,expected", [
    ("테크니컬 라이팅 문서화 표준", "테크니컬_라이터"),
    ("기술문서 작성 스타일 가이드", "테크니컬_라이터"),
    ("사용자 가이드 작성 표준", "테크니컬_라이터"),   # 사용자가이드 content=테크니컬_라이터(16), 배포문서(0)
    ("사용자 매뉴얼 작성", "테크니컬_라이터"),
    ("사용자 배포 문서 설치 가이드", "배포문서"),       # 설치 가이드는 배포문서
])
def test_techwriter_vs_deploydoc_routing(query, expected):
    assert server.infer_knowledge_agent_from_query(query) == expected


# ── 37) 유통기획관(⊂통기) 부분문자열 충돌: 위생으로 가면 안 됨 ──
@pytest.mark.parametrize("query,expected", [
    ("글로벌 유통기획관 기준 절차", "글로벌_유통기획관"),
    ("유통 채널 전략", "글로벌_유통기획관"),
    ("통기관 트랩 봉수", "위생"),
    ("급탕환수 순환 온도", "위생"),
])
def test_distribution_planner_not_caught_by_vent_substring(query, expected):
    """'유통기획관'의 '통기' 부분문자열이 위생으로 오라우팅되던 것 회귀 방지."""
    assert server.infer_knowledge_agent_from_query(query) == expected


# ── 38) '헤드' 부분문자열: 헤드헌팅/헤드라인/헤드셋이 소방기계로 가면 안 됨 ──
@pytest.mark.parametrize("query", [
    "헤드헌팅 채용 전략",
    "마케팅 헤드라인 카피",
    "헤드셋 장비 구매",
])
def test_head_substring_not_routed_to_fire(query):
    """스프링클러 '헤드'가 헤드헌팅·헤드라인·헤드셋을 소방기계로 끌던 것 회귀 방지."""
    assert server.infer_knowledge_agent_from_query(query) != "소방기계"


@pytest.mark.parametrize("query", [
    "스프링클러 헤드 살수반경",
    "스프링클러 헤드 간격",
    "살수 헤드 배치",
])
def test_sprinkler_head_still_routes_to_fire(query):
    """가드: 실제 스프링클러 헤드 질의는 여전히 소방기계."""
    assert server.infer_knowledge_agent_from_query(query) == "소방기계"


# ── 39) 사전 회귀 가드: in-domain 비엔지니어링 질의가 공종으로 새지 않아야(부분문자열 클래스) ──
_DISCIPLINES = {"건축", "구조", "토목", "위생", "공조배관", "공조덕트",
                "소방기계", "소방전기", "전기", "통신", "간섭검토"}


@pytest.mark.parametrize("query,excluded", [
    ("스프링클러 말고 다른 소화설비", "스프링클러"),
    ("냉각수 말고 냉수 배관", "냉각수"),
    ("습식 말고 건식 스프링클러", "습식"),
])
def test_negation_excludes_term_from_query(query, excluded):
    """'X 말고/빼고 Y'에서 제외 대상 X 가 검색어에서 빠져야 한다."""
    from backend.knowledge_engine import query_terms
    assert excluded not in query_terms(query), query_terms(query)


def test_negation_does_not_affect_normal_query():
    """가드: '말고/빼고' 없는 일반 질의는 모든 용어 유지."""
    from backend.knowledge_engine import query_terms
    assert "스프링클러" in query_terms("스프링클러 헤드 살수반경")


@pytest.mark.parametrize("query", [
    "FCU 팬코일 결로", "AHU 공조기 외기", "팬코일 유닛 드레인", "공조기 외기 도입",
])
def test_hvac_equipment_acronym_routes_to_hvac(query):
    """FCU/AHU/팬코일/공조기 HVAC 장비 약어가 공조 KB 로 강하게 연결돼야 한다."""
    matches = server.search_local_knowledge(query, limit=1)
    assert matches[0]["path"].stem in {"공조배관", "공조덕트"}
    assert matches[0]["score"] >= 40


def test_hvac_acronym_no_false_match_on_unrelated():
    """가드: '공조기획'(공조 기획) 같은 비HVAC 단어는 공조 확장이 붙지 않아야."""
    from backend.knowledge_engine import query_terms
    t = query_terms("공조기획 회의 일정")
    assert "냉수" not in t and "결로" not in t


@pytest.mark.parametrize("query,expected", [
    ("냉동기 chiller 용량", "공조배관"),
    ("UPS 무정전 전원", "전기"),
    ("MCCB 차단기 용량", "전기"),
    ("ACB 배전반", "전기"),
])
def test_mep_equipment_acronym_routes(query, expected):
    """냉동기/UPS/MCCB/ACB 장비 약어가 콘텐츠 있는 공종 KB 로 강하게 연결돼야 한다."""
    matches = server.search_local_knowledge(query, limit=1)
    assert matches[0]["path"].stem == expected and matches[0]["score"] >= 40


def test_equipment_acronym_no_false_match():
    """가드: 냉동식품·업스케일 등 비장비 단어에 장비 확장이 붙지 않아야."""
    from backend.knowledge_engine import query_terms
    assert "냉동기" not in query_terms("냉동식품 보관 창고")
    assert "차단기" not in query_terms("업스케일 성장 전략")


@pytest.mark.parametrize("query", [
    "물량 산출 자동화", "BOQ 수량 집계", "수량 산출서 작성",
    "QTO quantity takeoff", "자재 물량 내역서",
])
def test_quantity_takeoff_routes_to_excel(query):
    """물량 산출/BOQ/QTO(핵심 BIM 워크플로우)는 콘텐츠 최다인 엑셀자동화로 연결."""
    assert server.infer_knowledge_agent_from_query(query) == "엑셀자동화"
    assert server.search_local_knowledge(query, limit=1)[0]["score"] >= 40


def test_discipline_quantity_stays_in_discipline():
    """가드: 공종별 물량(철근 물량)은 공종(구조)이 선점해야 한다."""
    assert server.infer_knowledge_agent_from_query("철근 물량 산출") == "구조"


@pytest.mark.parametrize("query", [
    "소방법 제연설비", "제연설비 기준", "급기가압 제연", "제연설비 풍량",
])
def test_smoke_control_routes_to_hvac_duct(query):
    """기계제연/급기가압(mechanical smoke control)은 콘텐츠 최다인 공조덕트로 강하게 연결.
    (자연배연 배연창은 건축물 설비기준 면적 규정 → 건축; 아래 test_natural_smoke_vent 참조.)"""
    matches = server.search_local_knowledge(query, limit=1)
    assert matches[0]["path"].stem == "공조덕트" and matches[0]["score"] >= 40


@pytest.mark.parametrize("query", ["배연창 면적", "자연배연 설비", "배연창 설치"])
def test_natural_smoke_vent_routes_to_architecture(query):
    """자연배연(배연창)은 건축물 설비기준(거실 바닥면적 1/100·천장~0.9m) → 건축. 기계제연/
    급기가압(공조덕트)과 구분. 건축에 자연배연 콘텐츠 저작."""
    assert server.infer_knowledge_agent_from_query(query) == "건축"


@pytest.mark.parametrize("query,needle", [
    ("타일 줄눈", "타일"),
    ("도장 도막두께", "도막"),
    ("미장 두께", "미장"),
    ("창호 기밀성능", "기밀"),
    ("창호 수밀 등급", "수밀"),
])
def test_finish_and_window_buried_sections_surface(query, needle):
    """마감(타일/도장/미장)·창호(기밀/수밀/내풍압) ### 를 ## 로 승격 — 묻혀 weak/오발췌이던
    콘텐츠가 건축 해당 시방 섹션으로 surface. (bare '타일'은 '스타일' 충돌로 복합어 사용.)"""
    assert server.infer_knowledge_agent_from_query(query) == "건축"
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert needle in ans, ans[:100]


def test_style_guide_not_misrouted_to_architecture():
    """가드: '스타일 가이드'(기술문서)는 건축으로 안 감(bare '타일' 미사용 — 스타일∋타일 회피)."""
    assert server.infer_knowledge_agent_from_query("기술문서 작성 스타일 가이드") != "건축"


@pytest.mark.parametrize("query", ["토공 다짐도", "되메우기 다짐", "아스팔트 포장 두께", "도로 포장 기준"])
def test_civil_spec_topics_route_to_civil(query):
    """토목 시방서 ### 토픽(토공/다짐/포장/되메우기)이 키워드 누락으로 운영기본값으로
    새던 라우팅 갭 보강(콘텐츠 존재)."""
    assert server.infer_knowledge_agent_from_query(query) == "토목"


@pytest.mark.parametrize("query", ["방수 디테일 처리", "지하 외벽 방수", "옥상 방수 공법"])
def test_waterproofing_detail_surfaces_correct_section(query):
    """방수 공사 시방을 ###→## 승격 — '방수 디테일'이 건축 콘크리트 시방 발췌가 아니라
    방수 시방(도막/시트/외방수/지붕구배) 섹션으로 surface."""
    assert server.infer_knowledge_agent_from_query(query) == "건축"
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert "방수" in ans and ("도막" in ans or "외방수" in ans or "시트" in ans), ans[:100]


@pytest.mark.parametrize("query", ["층간소음 기준", "바닥충격음 기준", "중량충격음", "경량충격음"])
def test_floor_impact_noise_routes_to_architecture(query):
    """층간소음/바닥충격음(주택건설기준 경량58/중량49dB·슬래브210mm) 콘텐츠 저작 — weak였던 것 해소."""
    assert server.infer_knowledge_agent_from_query(query) == "건축"
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=1))
    assert ("충격음" in ans) or ("층간소음" in ans), ans[:100]


def test_smoke_control_no_false_match():
    """가드: '제주도' 등 제연 무관 단어에 제연 확장이 붙지 않아야."""
    from backend.knowledge_engine import query_terms
    assert "제연" not in query_terms("제주도 여행 일정")


@pytest.mark.parametrize("query", ["접지저항 측정", "접지 시스템 등전위본딩", "접지 공사 방식"])
def test_grounding_routes_to_electrical(query):
    """접지(전기 KB 43회)는 전기로 강하게 연결돼야 한다."""
    matches = server.search_local_knowledge(query, limit=1)
    assert matches[0]["path"].stem == "전기" and matches[0]["score"] >= 40


@pytest.mark.parametrize("query", ["직접지원 업무", "간접지원 부서", "직접지원금 신청"])
def test_jikjeop_jiwon_not_caught_by_grounding_substring(query):
    """'직접지원'('직접지'+'원')이 '접지' 부분문자열로 전기에 오매칭되면 안 된다.
    접지는 startswith 확장으로만 처리(substring discipline 키워드 금지)."""
    assert server.infer_knowledge_agent_from_query(query) != "전기"


@pytest.mark.parametrize("query", [
    "애드인 환불 정책 고객 문의", "환불 정책 기준", "구독 청약철회", "반품 처리 절차",
])
def test_refund_routes_to_billing_not_addin(query):
    """환불/청약철회는 결제 정책(라이선스결제 KB 36회)으로 가야 한다.
    '애드인 환불'이 Revit_Addin(API 노이즈)으로 가던 것 회귀 방지."""
    assert server.infer_knowledge_agent_from_query(query) == "라이선스결제"


def test_addin_dev_query_still_routes_to_revit_addin():
    """가드: 환불 없는 일반 애드인 개발 질의는 Revit_Addin 유지."""
    assert server.infer_knowledge_agent_from_query("Revit 애드인 트랜잭션 처리") == "Revit_Addin"


@pytest.mark.parametrize("query", ["애드인 구독 해지 방법", "결제 취소 문의", "라이선스 해지"])
def test_cancellation_routes_to_billing(query):
    """구독 해지/결제 취소도 환불처럼 라이선스결제(결제 정책)로 가야 한다."""
    assert server.infer_knowledge_agent_from_query(query) == "라이선스결제"


@pytest.mark.parametrize("query", ["스프링쿨러 설치 간격", "스프링쿨러 살수반경", "스프링쿨러 헤드"])
def test_sprinkler_typo_routes_to_fire(query):
    """'스프링쿨러'는 '스프링클러'의 흔한 오타 — 소방기계로 라우팅되고 강하게 연결돼야 한다
    (실사용자 오타 견고성). 라우팅 규칙 + query_terms 정규형 추가로 해결."""
    assert server.infer_knowledge_agent_from_query(query) == "소방기계"
    assert server.search_local_knowledge(query, limit=1)[0]["score"] >= 40


@pytest.mark.parametrize("query", ["닥트 사이즈", "디퓨져 위치", "디퓨저 위치"])
def test_hvac_variant_terms_route_to_duct(query):
    """'닥트'(덕트 변형)·'디퓨져'(디퓨저 변형)는 공조덕트로 라우팅·강연결돼야 한다.
    KB 정규형(덕트/디퓨저)으로 query_terms 정규화 + 라우팅 규칙 추가."""
    assert server.infer_knowledge_agent_from_query(query) == "공조덕트"
    assert server.search_local_knowledge(query, limit=1)[0]["score"] >= 40


def test_bare_cancel_not_overcaptured():
    """가드: bare '취소'(회의 취소 등)는 라이선스결제로 과포착되면 안 된다."""
    assert server.infer_knowledge_agent_from_query("회의 취소 공지") != "라이선스결제"


@pytest.mark.parametrize("query", [
    "BIM Command Center 가격 정책", "BIM Command Center 구독 요금",
    "command center 라이선스 비용", "커맨드센터 가격",
])
def test_product_pricing_routes_to_billing(query):
    """자사 제품(BIM Command Center) 가격/구독 질의는 라이선스결제 KB로 가야 한다.
    정답 헤딩 'BIM Command Center 구독 가격 정책'(USD 19/월·190/년). 이전엔
    inferred=generic이라 +50 부스트 미적용 → BIM_제안서(제안 가격전략만, sc36<40)에
    밀려 weak로 웹검색 트리거되던 것 회귀 방지(제품명+가격 any_groups 조합)."""
    assert server.infer_knowledge_agent_from_query(query) == "라이선스결제"


@pytest.mark.parametrize("query", [
    "BIM Command Center 기능 소개",   # 제품명 있으나 가격 토큰 없음
    "우리 회사 가격 정책 전략",         # 가격 토큰 있으나 제품명 없음(전략 주제)
])
def test_product_pricing_guard_not_overcaptured(query):
    """가드: 제품명+가격 둘 다 있어야 라이선스결제. '가격 정책'은 전략 파일
    다수(CEO·시장선도·CSO)에 광범위해 단독으로 라이선스결제 과포착되면 안 된다."""
    assert server.infer_knowledge_agent_from_query(query) != "라이선스결제"


@pytest.mark.parametrize("query", [
    "무료 체험 기간이 며칠인가요", "30일 체험판 어떻게 신청하나요",
    "구독 결제는 어떻게 하나요", "체험 끝나면 자동 결제되나요",
    "Team 5-Pack 라이선스 인원", "카드 결제 변경", "구독 갱신 언제 되나요",
    "BIM Command Center 어디서 구매하나요",
])
def test_billing_faq_routes_to_license(query):
    """결제·구독·체험 FAQ(고객 사전판매/온보딩 빈출)는 라이선스결제 KB로 가야 한다.
    콘텐츠 검증됨(30일 무료체험·구독상태·5 seats·결제보안). 이전엔 generic으로 빠져
    weak→웹검색(웹은 내부 제품 정보 모름) 트리거되던 것 회귀 방지."""
    assert server.infer_knowledge_agent_from_query(query) == "라이선스결제"


@pytest.mark.parametrize("query", [
    "실무 체험단 모집 일정",   # 체험단(교육) — bare '체험' 아님
    "BIM 체험 교육 신청",      # 교육 체험
    "모델 갱신 주기",          # 갱신(모델)
    "자재 구매 발주",          # 구매(조달)
    "장비 구매 비용",          # 구매
    "결제 시스템 보안 설계",    # 결제 시스템(설계)
])
def test_billing_faq_guard_not_overcaptured(query):
    """가드: bare 체험/갱신/구매/결제는 체험단·모델갱신·자재구매·교육체험을
    가로채므로 결제-특정 다단어만 라우팅. 위 비결제 질의는 라이선스결제 아님."""
    assert server.infer_knowledge_agent_from_query(query) != "라이선스결제"


def test_product_manual_routes_to_techwriter():
    """'제품 사용 매뉴얼'은 테크니컬_라이터(사용자 가이드 콘텐츠). '사용 매뉴얼'
    다단어 추가로 커버(bare '매뉴얼'은 '매뉴얼 모드' 등과 충돌해 미사용)."""
    assert server.infer_knowledge_agent_from_query("제품 사용 매뉴얼 어디서 보나요") == "테크니컬_라이터"
    # 가드: '매뉴얼 모드'(수동 모드)는 테크니컬_라이터로 과포착되면 안 된다
    assert server.infer_knowledge_agent_from_query("매뉴얼 모드 전환") != "테크니컬_라이터"


@pytest.mark.parametrize("query", [
    "how much does BIM Command Center cost", "BIM Command Center pricing",
    "how do I subscribe to BIM Command Center", "BIM Command Center subscription plan",
    "is there a free trial", "Team 5-Pack license seats",
])
def test_english_product_faq_routes_to_license(query):
    """글로벌 스토어(Autodesk) 제품이라 영어 제품 FAQ도 라이선스결제로 가야 한다.
    정답 숫자(USD 14·30일·5 seats)는 언어무관 정확 → 웹검색(미출시 제품이라 무용)보다 유용.
    'cost/subscribe/subscription'은 제품명 게이트(any_groups)로 한정."""
    assert server.infer_knowledge_agent_from_query(query) == "라이선스결제"


@pytest.mark.parametrize("query", [
    "subscribe to newsletter",            # 제품명 없는 subscribe → billing 아님
    "subscription business model strategy",  # 제품명 없는 subscription
    "프로젝트 원가 산정 방법",              # 제품명 없는 cost/원가 → 견적산정
    "공사비 cost 견적",                    # cost는 제품명 게이트라 견적 유지
])
def test_english_billing_guard_not_overcaptured(query):
    """가드: cost/subscribe/subscription은 제품명(command center)과 함께일 때만
    라이선스결제. 제품명 없는 newsletter/사업모델/원가산정은 라이선스결제 아님."""
    assert server.infer_knowledge_agent_from_query(query) != "라이선스결제"


@pytest.mark.parametrize("query", ["제품 불만 클레임 처리", "고객 민원 대응", "컴플레인 응대 절차"])
def test_complaint_routes_to_cs_not_log(query):
    """고객 불만/클레임/민원은 운영 로그(추론훈련루프)가 아니라 CS_기술지원관으로."""
    matches = server.search_local_knowledge(query, limit=1)
    assert matches[0]["path"].stem == "CS_기술지원관"
    assert matches[0]["path"].stem != "추론훈련루프"


@pytest.mark.parametrize("query", ["ACC BIM360 협업", "BIM360 공통데이터환경", "construction cloud 모델 공유"])
def test_acc_bim360_routes_to_collab_platform(query):
    """ACC/BIM360 협업 플랫폼(content 풍부)으로 연결. ACC_BIM360을 inference_only 에이전트로
    등록해 라우팅 타깃화. bare 'acc'(access/account)는 충돌 제외."""
    matches = server.search_local_knowledge(query, limit=1)
    assert matches[0]["path"].stem == "ACC_BIM360" and matches[0]["score"] >= 40


@pytest.mark.parametrize("query", ["파일 access 권한", "account 계정 관리"])
def test_acc_substring_no_false_match(query):
    """가드: access/account의 'acc'가 ACC_BIM360으로 오매칭되면 안 된다."""
    assert server.infer_knowledge_agent_from_query(query) != "ACC_BIM360"


@pytest.mark.parametrize("query", ["댐퍼 설치 기준", "방화댐퍼 퓨즈", "풍량댐퍼 조절"])
def test_damper_routes_to_hvac_duct(query):
    """HVAC 댐퍼(방화/풍량)는 공조덕트(콘텐츠 48회)로 강하게 연결."""
    matches = server.search_local_knowledge(query, limit=1)
    assert matches[0]["path"].stem == "공조덕트" and matches[0]["score"] >= 40


def test_seismic_damper_routes_to_structure():
    """가드: 제진/내진 댐퍼(seismic)는 공조가 아니라 구조로."""
    assert server.infer_knowledge_agent_from_query("제진댐퍼 내진 보강") == "구조"


@pytest.mark.parametrize("query,expected_agent", [
    (
        "스프링클러 살수 장애를 단순 간섭이 아니라 생명안전 리스크로 설명하려면 무엇이 빠지면 안 되나요?",
        "소방기계",
    ),
    (
        "소화배관이 전기 케이블 트레이 위에 놓여 있으면 문제가 있나요?",
        "간섭검토",
    ),
    (
        "방화댐퍼 설치 시 점검구 위치 기준이 어떻게 되나요?",
        "공조덕트",
    ),
])
def test_field_simulation_specific_routing_precedes_broad_rules(query, expected_agent):
    """현장형 복합 질문은 넓은 공종 키워드보다 세부 맥락 규칙을 우선한다."""
    assert server.infer_knowledge_agent_from_query(query) == expected_agent


@pytest.mark.parametrize("message,context,expected", [
    ("이거 간격 맞나요?", "선택 요소: 스프링클러 헤드, 간격 3.5m", "소방기계"),
    ("이 이격 괜찮아요?", "선택: 케이블 트레이(강전), 인접 통신 트레이 100mm", "전기"),
])
def test_revit_context_enables_routing_for_vague_query(message, context, expected):
    """Revit 애드인: 모호한 질의도 선택 요소 컨텍스트로 올바른 공종 라우팅(유료 제품 핵심)."""
    from backend.obsidian_notes import build_revit_context_prompt
    # 컨텍스트 없으면 모호 → default, 컨텍스트 있으면 정확 라우팅
    assert server.infer_knowledge_agent_from_query(message) != expected
    combined = build_revit_context_prompt(message, context)
    assert server.infer_knowledge_agent_from_query(combined) == expected


@pytest.mark.parametrize("query,expected", [
    ("개구부 보강 기준", "구조"),
    ("저수조 용량 청소", "위생"),
    ("자동화재탐지설비 경계구역", "소방전기"),
    ("지하매설물 탐사 기준", "토목"),
    ("도로포장 단면 설계", "토목"),
])
def test_distinctive_discipline_terms_route_strongly(query, expected):
    """공종-distinctive 용어(개구부/저수조/자동화재탐지/지하매설물/도로포장)가 약하던 것을 강하게 연결."""
    matches = server.search_local_knowledge(query, limit=1)
    assert matches[0]["path"].stem == expected and matches[0]["score"] >= 40


@pytest.mark.parametrize("query,parts", [
    ("스프링클러 헤드 간격과 살수반경과 벽 이격 기준", ["간격", "살수", "이격"]),
    ("통기관 역할과 트랩 봉수 깊이", ["통기", "봉수"]),
    ("케이블트레이 충전율과 이격 기준", ["충전", "이격"]),
])
def test_multipart_question_coverage(query, parts):
    """다중 항목 질문은 excerpt 2번째 섹션이 미커버 용어를 우선해 가급적 모두 답해야."""
    answer = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=3))
    covered = sum(1 for p in parts if p in answer)
    assert covered >= len(parts) - 1, f"{covered}/{len(parts)}: {answer[:80]}"


@pytest.mark.parametrize("query", [
    "헤드헌팅 채용", "헤드라인 마케팅", "이력서 면접", "브랜드 캠페인",
    "콘텐츠 마케팅", "고객 환불", "구독 결제", "스토어 심사",
    "MSI 인스톨러", "EULA 약관", "외주 하도급", "재무 손익분기",
    "경비 영수증", "교육 커리큘럼", "기술문서 작성",
])
def test_business_queries_not_routed_to_engineering_disciplines(query):
    """HR/마케팅/상용화/지원 질의가 공종 키워드 부분문자열로 오라우팅되면 안 된다.
    새 공종 키워드 추가 시 부분문자열 충돌(헤드/통기/트레이류)을 조기 포착."""
    assert server.infer_knowledge_agent_from_query(query) not in _DISCIPLINES, query


# ── 34) Obsidian 위키링크가 고객 답변에 노출되면 안 됨(qwen 합성 우회 경로 방어) ──
def test_wiki_links_stripped_from_outbound():
    from backend.text_utils import sanitize_outbound_text
    assert sanitize_outbound_text("[[설비자동제어]] 참조") == "설비자동제어 참조"
    assert sanitize_outbound_text("[[설비기초|기초]] 별칭") == "기초 별칭"


@pytest.mark.parametrize("query", ["분전반 작업공간", "방화구획 관통부 처리", "통기관 트랩"])
def test_answers_have_no_wiki_links(query):
    answer = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=3))
    assert "[[" not in answer, answer


# ── 35) 마크다운 서식(##/```/**)이 고객 답변(qwen 미경유 경로)에 노출되면 안 됨 ──
def test_clean_markdown_for_display_strips_formatting():
    from backend.text_utils import clean_markdown_for_display
    raw = "## 제목\n```\ncode\n```\n**굵게** 본문"
    out = clean_markdown_for_display(raw)
    assert "##" not in out and "```" not in out and "**" not in out
    assert "제목" in out and "code" in out and "굵게" in out  # 데이터 보존


@pytest.mark.parametrize("query", ["철근 정착길이 이음", "옥내소화전 방수압", "케이블트레이 충전율"])
def test_answers_have_no_raw_markdown_formatting(query):
    answer = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=3))
    assert "##" not in answer and "```" not in answer and "**" not in answer, answer


def test_clean_markdown_strips_horizontal_rule_keeps_table_and_list():
    """clean_markdown_for_display 는 수평선(---/***/___)을 제거하되 표 구분행(|---|)과
    리스트(- 항목)·본문은 보존해야 한다(답변 끝 '---' 누출 회귀 방지)."""
    from backend.text_utils import clean_markdown_for_display as cm
    assert "---" not in cm("이슈를 동기화한다.\n\n---\n다음 섹션")
    assert "동기화한다" in cm("이슈를 동기화한다.\n\n---")
    assert "|---|" in cm("| A | B |\n|---|---|\n| 1 | 2 |")   # 표 구분행 보존
    assert "- 항목" in cm("- 항목 하나\n- 항목 둘")            # 리스트 보존


def test_more_research_answer_strips_markdown():
    """'더 찾아줘' 연구 응답(build_more_research_answer)도 웹 결과 마크다운을 정리해야 한다
    (모든 답변 빌더 일관 — knowledge/combined/revit/more_research)."""
    web = "## Title\nRevit **bold** 워크셋 내용입니다.\n출처: http://x.com"
    ans = server.build_more_research_answer("워크셋", "BIM_지침서", web, [])
    assert "##" not in ans and "**" not in ans
    assert "워크셋" in ans


def test_combined_answer_strips_markdown_from_web_result():
    """weak→웹보강 경로(build_combined_answer)도 웹 결과의 마크다운(##/**)을 정리해야 한다.
    qwen 합성이 ollama 다운으로 미적용될 때 이 결과가 그대로 고객 답변이 되므로
    (build_knowledge_answer·build_revit_assistant_answer 와 동일 규칙) 회귀 방지."""
    matches = server.search_local_knowledge("Revit 워크셋 분담", limit=3)
    web = "## Worksharing\nRevit worksets allow **multiple users**.\n워크셋은 모델을 논리 단위로 나눈다."
    ans = server.build_combined_answer("Revit 워크셋 분담", web, matches)
    assert "##" not in ans and "**" not in ans
    assert "워크셋" in ans  # 본문 내용은 보존


def test_revit_assistant_answer_has_no_raw_markdown():
    """Revit 애드인 강매칭 경로(qwen 미경유)도 마크다운이 정리돼야 한다."""
    from backend.obsidian_notes import build_revit_assistant_answer
    matches = server.search_local_knowledge("철근 정착길이 이음", limit=3)
    answer = build_revit_assistant_answer("철근 정착길이 이음", matches, "구조")
    assert "##" not in answer and "```" not in answer and "**" not in answer


@pytest.mark.parametrize("query", [
    # 정체성/이름
    "이름이 뭐예요", "너 누구야", "당신은 누구인가요", "누구세요",
    "네 이름이 뭐야", "어시스턴트 이름 알려줘", "자기소개해줘", "Lua가 누구야",
    # 능력(capability)
    "뭐 도와줄 수 있어", "무엇을 할 수 있나요", "너 뭐 할 줄 알아", "너 어떤 기능 있어",
    # 주어 없는 단독 역량/기능 질의(챗봇 문맥 = 봇 능력) — 이전엔 sc20→'찾지 못함' 폴백이던 것
    "무슨 기능이 있나요", "도와줄 수 있어?", "어떤 기능을 제공하나요", "기능이 뭐가 있어",
])
def test_identity_query_answers_lua(query):
    """봇 정체성/이름/능력 질의는 결정적으로 'Lua' 소개를 반환한다(qwen 다운 시에도).
    이전엔 weak→엉뚱한 KB 발췌(IFC 연동 실패 등) 반환하던 것 회귀 방지."""
    ans = server.identity_answer(query)
    assert ans is not None and "Lua" in ans


@pytest.mark.parametrize("query", [
    "이 부재 이름이 뭐야",            # 도메인 요소 이름(봇 정체성 아님)
    "밸브 누구 담당이야",              # 담당 책임 질의
    "스프링클러 헤드 간격",            # 일반 도메인
    "BIM Command Center 가격",        # 제품 질의
    "BIM Command Center 어떤 기능이 있어",  # 제품 기능(봇 능력 아님)
    "Revit 어떤 기능 지원",           # 도메인 기능
])
def test_identity_guard_not_triggered_by_domain_queries(query):
    """가드: self-reference 없는 도메인/제품 질의('X 이름이 뭐야','제품 어떤 기능')는
    봇 정체성·능력으로 오인되면 안 된다."""
    assert server.identity_answer(query) is None


def test_revit_assistant_answer_identity_returns_lua():
    """defense-in-depth: build_revit_assistant_answer 단독 호출 시에도 정체성 질의는
    'Lua' 소개를 반환해야 한다(프로덕션 compose 경로 외 직접 호출/경로 변경 대비)."""
    from backend.obsidian_notes import build_revit_assistant_answer
    matches = server.search_local_knowledge("너 누구야", limit=3)
    answer = build_revit_assistant_answer("너 누구야", matches, "지식업데이트")
    assert "Lua" in answer and "저는 Lua" in answer


@pytest.mark.parametrize("query", [
    "무역센터 kita 프로젝트 개요를 알고 싶어",  # 고유명 주제
    "스프링클러 헤드 간격",                      # 도메인 주제
    "냉동기 어셈블리 밸브 순서가 어떻게 될까",    # 장비 주제
])
def test_extract_topic_terms_has_subject(query):
    """자체 주제(고유명/도메인 명사)가 있는 질의는 topic 비어있지 않음."""
    assert server.extract_topic_terms(query)


@pytest.mark.parametrize("query", [
    "프로젝트 관련 자료를 찾아서 나에게 알려줘 시공사나 연면적 등등",  # 주어 없는 후속질의
    "그 프로젝트 시공사 알려줘",   # 지시어 후속
    "연면적 얼마야",              # 속성+종결어미만
    "시공사 알려줘요",
    "거기 시공사는",             # 조응(장소대명사)
    "그곳 준공일",
    "그거 자료 더 찾아줘",
    "담당자 누구",               # 속성+의문사
    "그거 간격은",               # 속성명사 단독(직전 주제 상속 대상)
    "용량은",
    "순서는 어떻게",
    "그 방법은",
])
def test_extract_topic_terms_subjectless_followup(query):
    """일반 요청·속성·지시어만 있는 후속질의는 topic 비어있음 → 직전 대화 주제 상속 대상.
    문맥기억 부재로 '연면적'만 보고 인천공항으로 오매칭되던 것의 판별 기반."""
    assert server.extract_topic_terms(query) == []


@pytest.mark.parametrize("query", [
    "법무 계약 검토", "계약서 조항 검토", "BIM 용역 계약서 검토", "독소조항 확인",
])
def test_contract_review_routes_to_legal(query):
    """계약서/계약 검토/독소조항은 법무조항검토 KB(BIM 용역 계약서 검토 콘텐츠 보유)로.
    이전 generic·weak(sc28)였던 것 → 콘텐츠-backed 다단어로 confident."""
    assert server.infer_knowledge_agent_from_query(query) == "법무조항검토"


def test_contract_review_guard_outsourcing_first():
    """가드: '외주 계약'은 외주관리가 먼저(순서). 법무 계약 키워드가 가로채면 안 된다."""
    assert server.infer_knowledge_agent_from_query("외주 계약 관리") == "외주관리"


@pytest.mark.parametrize("query", [
    "방화구획 면적 기준", "실 면적 산정", "주차장 면적 기준", "개구부 면적", "마감 면적 계산",
])
def test_area_db_does_not_hijack_generic_area_queries(query):
    """공항·대형시설 '연면적 데이터베이스'가 흔한 토큰 '면적'으로 무관 면적 질의의
    선두(confident) 답변을 가로채면 안 된다(magnet 페널티). 답변 선두가 공항 연면적 DB면 실패."""
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=4))
    head = ans[:200]
    assert not (("인천국제공항" in head or "제2터미널" in head or "스타필드" in head) and "연면적" in head), \
        f"area-DB가 선두 침입: {head[:80]}"


@pytest.mark.parametrize("query", ["인천공항 제2터미널 연면적", "대형시설 규모 연면적"])
def test_area_db_still_served_for_floor_area_queries(query):
    """가드: 연면적/규모/공항 질의는 area-DB가 정상 제공돼야('인천공항 면적 17×' 갭 해소 보존)."""
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=4))
    assert "38만" in ans or "384,000" in ans or "인천국제공항" in ans


@pytest.mark.parametrize("query", ["품질 검수 기준", "BIM 품질 검수", "품질검수 항목"])
def test_quality_inspection_routes_to_delivery_qa(query):
    """'품질 검수'(띄움 변형 포함)는 BIM_납품검수 KB로. content top이나 generic으로 weak였던 것."""
    assert server.infer_knowledge_agent_from_query(query) == "BIM_납품검수"


def test_quality_inspection_guard_bare_quality():
    """가드: bare '품질'(제품 품질 관리 등)은 BIM_납품검수로 과포착되면 안 된다."""
    assert server.infer_knowledge_agent_from_query("제품 품질 관리") != "BIM_납품검수"


@pytest.mark.parametrize("query", ["강의 콘텐츠 제작", "학습 콘텐츠 설계", "강의안 제작"])
def test_learning_content_routes_to_content_designer(query):
    """강의/학습 콘텐츠 '제작·설계'는 러닝콘텐츠디자이너(콘텐츠 풍부). content top이나 weak였던 것."""
    assert server.infer_knowledge_agent_from_query(query) == "러닝콘텐츠디자이너"


@pytest.mark.parametrize("query", ["강의 컨텐츠 제작", "학습 컨텐츠 설계", "컨텐츠 설계 방법"])
def test_content_spelling_variant_normalized(query):
    """'컨텐츠'(콘텐츠 흔한 오기)도 정규화되어 러닝콘텐츠디자이너로 라우팅돼야 한다."""
    assert server.infer_knowledge_agent_from_query(query) == "러닝콘텐츠디자이너"


@pytest.mark.parametrize("query", ["교육 과정 개설", "BIM 교육 신청", "교육 컨설팅 문의"])
def test_education_consulting_not_stolen_by_content_designer(query):
    """가드: 교육 과정/신청/컨설팅은 교육컨설팅 유지(콘텐츠 제작 키워드가 가로채면 안 됨)."""
    assert server.infer_knowledge_agent_from_query(query) == "교육컨설팅"


@pytest.mark.parametrize("query", [
    "냉동기 어셈블리 밸브 순서", "chiller 연결 배관",
    "열교환기 1차측 2차측 밸브", "판형 열교환기 연결 밸브", "셸앤튜브 열교환기",
    "플렉시블 조인트 위치", "후렉시블 조인트 위치",  # 후렉시블=플렉시블 정규화
])
def test_hvac_equipment_routes_to_hvac_piping(query):
    """HVAC 열·수계통 장비(냉동기/열교환기)는 공조배관으로 라우팅(밸브 어셈블리 큐레이션 보유).
    이전 generic/weak였던 것 → +50 부스트로 confident 로컬 답변."""
    assert server.infer_knowledge_agent_from_query(query) == "공조배관"


@pytest.mark.parametrize("query", [
    "TV 신호 분배기",      # 분배기는 공조 키워드 아님(전기/통신)
    "냉동식품 창고 BIM",   # 냉동식품 ⊄ 냉동기 매칭되면 안 됨
])
def test_hvac_equipment_routing_guard(query):
    """가드: 냉동기/열교환기 라우팅이 비(非)HVAC 질의를 가로채면 안 된다."""
    assert server.infer_knowledge_agent_from_query(query) != "공조배관"


@pytest.mark.parametrize("query", [
    "회사 주요 수익원", "수익원", "주요 수익원은 무엇", "LUA BIM LABS 수익원",
])
def test_revenue_source_routes_to_ceo(query):
    """'수익원'(주요 수익원이 무엇인가=사업모델 개요)은 CEO KB로 가야 한다.
    '주요'가 주요_고객사_관계망 magnet이고 '수익원'이 약스코어돼 weak이던 것 회귀 방지."""
    assert server.infer_knowledge_agent_from_query(query) == "CEO"


@pytest.mark.parametrize("query", ["수익 모델 분석", "손익분기점 계산"])
def test_cfo_finance_not_captured_by_revenue_source_rule(query):
    """가드: 수익원→CEO 규칙이 CFO 재무(수익 모델/손익분기)를 가로채면 안 된다."""
    assert server.infer_knowledge_agent_from_query(query) == "CFO"


@pytest.mark.parametrize("query", ["투자 유치 전략", "자금 조달 방법", "자금조달 옵션"])
def test_fundraising_routes_to_cfo(query):
    """투자 유치/자금 조달(CFO 자금조달 콘텐츠: VC/TIPS/CB)은 CFO로 가야 한다. weak이던 것 해소."""
    assert server.infer_knowledge_agent_from_query(query) == "CFO"


@pytest.mark.parametrize("query", ["설비 투자 검토", "투자 수익률 분석"])
def test_bare_investment_not_overcaptured_by_cfo(query):
    """가드: bare '투자'(설비투자/투자수익률)는 CFO 자금조달 규칙으로 과포착되면 안 된다."""
    assert server.infer_knowledge_agent_from_query(query) != "CFO"


@pytest.mark.parametrize("query", ["아파트 BIM", "병원 의료시설 BIM 고려사항"])
def test_banner_heading_excerpt_pulls_content(query):
    """배너 헤딩(## X BIM 마스터급 경험 지식 + Source + ---, 본문은 다음 ## 섹션)이
    heading-match로 뽑혀도 다음 섹션 콘텐츠를 병합해 thin(제목만) 답변이 되지 않아야 한다.
    auto-generated 시설유형 KB의 배너 구조 대응."""
    ans = server.build_knowledge_answer(query, server.search_local_knowledge(query, limit=4))
    assert len(ans) > 300, f"배너-thin 답변({len(ans)}자): {ans[:80]}"


def test_section_body_chars_detects_banner():
    """배너 섹션(메타/--- 뿐) 본문 길이 ~0, 실콘텐츠 섹션은 큰 값."""
    from backend.knowledge_engine import _section_body_chars
    banner = "## X BIM 마스터급 경험 지식 (2026-05-28)\n- Source: claude-code-enhanced\n\n---"
    rich = "## 1. 개요\n병원은 환자 안전이 최우선인 특수 시설이다. 감염 제어와 의료 가스 공급이 핵심이다."
    assert _section_body_chars(banner) < 40
    assert _section_body_chars(rich) > 40


@pytest.mark.parametrize("query", ["BIM 투입 공수 산정", "공수 산정 기준"])
def test_bim_manday_routes_to_workload_table(query):
    """BIM 투입 공수/M-D 산정은 BIM_등급별_투입일_기준표(14k orphan이던 것)로 confident.
    등록 BIM_인력파견_기준(인력파견)과 별개."""
    assert server.infer_knowledge_agent_from_query(query) == "BIM_등급별_투입일_기준표"


def test_staffing_dispatch_not_stolen_by_manday_rule():
    """가드: 투입 공수 규칙이 BIM 인력 파견(별개 에이전트)을 가로채면 안 된다."""
    assert server.infer_knowledge_agent_from_query("BIM 인력 파견 절차") == "BIM_인력파견_기준"


@pytest.mark.parametrize("query,expected", [
    ("데이터센터 BIM 설계", "데이터센터_BIM"),
    ("병원 의료시설 BIM", "병원_의료시설_BIM"),
    ("물류센터 창고 BIM", "물류센터_창고시설_BIM"),
    ("호텔 숙박시설 BIM", "호텔_숙박시설_BIM"),
    ("공항 bim 설계", "공항_BIM"),
    ("주차장 bim", "주차장_모빌리티시설_BIM"),
])
def test_facility_type_kb_routing(query, expected):
    """시설유형 KB(미등록 orphan이던 20개)가 confident 라우팅돼야 한다.
    각 4.7~18k자 콘텐츠 보유했으나 미등록으로 전부 weak→웹검색이던 것 해소."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,forbidden", [
    ("병원 전기 배선", "병원_의료시설_BIM"),   # 공종 특정 → 전기
    ("인천공항 면적 산정", "공항_BIM"),         # 공항 area → 건축('공항 bim' 한정)
    ("주차장 천장고", "주차장_모빌리티시설_BIM"),  # 천장고 → 건축
    ("BIM 교육 커리큘럼", "학교_교육시설_BIM"),  # 교육 → 교육컨설팅
])
def test_facility_routing_does_not_steal_discipline(query, forbidden):
    """가드: 시설유형 라우팅(@discipline_keywords 뒤 배치)이 공종/건축/교육 특정 질의를 가로채면 안 된다."""
    assert server.infer_knowledge_agent_from_query(query) != forbidden


@pytest.mark.parametrize("query", ["도로 종단구배", "종단구배 기준", "흙막이 가시설", "흙막이 공법 검토"])
def test_civil_road_excavation_routes_to_civil(query):
    """토목 도로/가설(종단구배·흙막이)은 토목으로 가야 한다. '도로 종단구배'가 위생 'bare 구배'
    magnet으로 오라우팅되던 것 + 흙막이(토목 콘텐츠 보유)가 weak이던 것 해소."""
    assert server.infer_knowledge_agent_from_query(query) == "토목"


@pytest.mark.parametrize("query", ["배수 구배 기준", "통기관 구배"])
def test_plumbing_slope_still_routes_to_plumbing(query):
    """가드: 토목 종단구배 규칙이 위생 배수/통기 구배를 가로채면 안 된다(위생 'bare 구배' 유지)."""
    assert server.infer_knowledge_agent_from_query(query) == "위생"


@pytest.mark.parametrize("query", [
    "피난 보행거리 기준", "비상구 유효폭", "장애인 화장실 유효 회전반경", "무장애 경사로 기울기",
])
def test_life_safety_code_routes_to_architecture(query):
    """생명안전/법규 질의(피난 보행거리·비상구·BF)는 건축 KB로 가야 한다(건축.md에 수치 보유).
    고위험 질의가 weak→generic이던 것 회귀 방지(content-backed)."""
    assert server.infer_knowledge_agent_from_query(query) == "건축"


@pytest.mark.parametrize("query,forbidden", [
    ("소방 피난기구 설치", "건축"),  # bare 피난 미추가 → 피난기구는 건축 아님
])
def test_life_safety_routing_guard(query, forbidden):
    """가드: 건축 안전어가 소방 피난기구 등을 가로채면 안 된다(bare 피난 미사용)."""
    assert server.infer_knowledge_agent_from_query(query) != forbidden


@pytest.mark.parametrize("query,expected", [
    ("프롬프트 엔지니어링 기법", "프롬프트엔지니어"),
    ("데이터 파이프라인 오케스트레이션", "파이프라인_오케스트레이터"),
    ("품질 테스트 자동화", "QA_테스터"),
    ("제품 출시 체크리스트", "제품패키징"),
])
def test_extended_agents_content_backed_routing(query, expected):
    """콘텐츠 보유했으나 generic 라우팅돼 weak이던 확장에이전트 → 키워드 부여로 confident."""
    assert server.infer_knowledge_agent_from_query(query) == expected


@pytest.mark.parametrize("query,forbidden", [
    ("배관 파이프라인 설계", "파이프라인_오케스트레이터"),  # bare 파이프라인 충돌 방지
    ("빌드 테스트 검증", "QA_테스터"),                    # 빌드 테스트는 빌드검증
])
def test_extended_agents_routing_guard(query, forbidden):
    """가드: 데이터 파이프라인/품질 테스트 키워드가 배관 파이프라인·빌드 테스트를 가로채면 안 된다."""
    assert server.infer_knowledge_agent_from_query(query) != forbidden


def test_carried_retry_safety_gate_rejects_unrelated_followup():
    """문맥 재시도 안전 게이트: 강한 직전 주제(냉동기 밸브)가 무관 질의(김치찌개/양자컴퓨터)를
    confident-오답으로 만들지 않도록, carried 답변이 후속질의 distinctive 용어를 실제 커버할 때만 채택."""
    # 무관 후속 — carried 답변이 '김치찌개'를 안 다룸 → 거부
    냉동기_matches = server.search_local_knowledge("냉동기 어셈블리 밸브 김치찌개 레시피", limit=4)
    assert server._carried_answer_covers_followup("김치찌개 레시피", 냉동기_matches) is False
    assert server._carried_answer_covers_followup("양자컴퓨터 큐비트",
        server.search_local_knowledge("냉동기 어셈블리 밸브 양자컴퓨터 큐비트", limit=4)) is False
    # 정당 후속 — carried 답변이 '이음'을 다룸 → 채택
    이음_matches = server.search_local_knowledge("철근 콘크리트 슬래브 배근 이음 길이는?", limit=4)
    assert server._carried_answer_covers_followup("이음 길이는?", 이음_matches) is True


def test_carried_retry_accepts_pure_attribute_followup():
    """순수 속성 후속질의('간격은?'·'용량은?')는 토픽이 전부 속성어라 extract_topic_terms 가
    빈다. 이때 속성어가 carried 발췌에 실제 있으면 채택해야 한다(이전엔 안전게이트가 무조건
    거부 → '스프링클러 헤드' 후 '간격은?'이 confident carried(sc131) 두고 웹으로 새던 것)."""
    sp = server.search_local_knowledge("스프링클러 헤드 간격은?", limit=4)
    assert server._carried_answer_covers_followup("간격은?", sp) is True
    # garbage(속성어 없음)는 여전히 거부.
    assert server._carried_answer_covers_followup("ㅋㅋ 알려줘",
        server.search_local_knowledge("냉동기 밸브 ㅋㅋ 알려줘", limit=4)) is False


@pytest.mark.parametrize("follow", [
    "더 자세히 알려주세요", "예시 들어줘", "쉽게 설명해줘", "자세하게 알려줘", "사례 보여줘",
])
def test_elaboration_followups_inherit_context(follow):
    """엘라보레이션 요청('더 자세히'·'예시 들어줘'·'쉽게 설명')은 자체 주제가 없으므로
    직전 대화 주제를 상속해야 한다(이전엔 '예시/쉽게/설명해줘'가 토픽으로 오인돼 미상속→웹)."""
    import datetime as _dt
    from types import SimpleNamespace
    upd = SimpleNamespace(effective_chat=SimpleNamespace(id=556), effective_user=SimpleNamespace(id=445))
    server.TELEGRAM_KNOWLEDGE_SESSIONS["556:445"] = {
        "context_subject": "스프링클러 헤드 간격",
        "created_at": _dt.datetime.now().isoformat(timespec="seconds"),
    }
    eff, _ = server._resolve_conversation_context(upd, follow)
    assert eff.startswith("스프링클러 헤드 간격"), (follow, eff)
    # 가드: 실제 토픽이 섞인 질의는 그 토픽을 유지(상속 아님).
    assert server.extract_topic_terms("간섭 사례 알려줘") == ["간섭"]


def test_conversation_context_inherits_subject_for_followup():
    """주어 없는 후속질의는 직전(최근 15분) 대화 주제를 상속한다(문맥기억).
    '무역센터 KITA' 후 '연면적/시공사 찾아줘'가 주어없어 인천공항으로 오매칭되던 것 방지."""
    import datetime as _dt
    from types import SimpleNamespace
    upd = SimpleNamespace(effective_chat=SimpleNamespace(id=777), effective_user=SimpleNamespace(id=888))
    key = "777:888"
    now = _dt.datetime.now()
    server.TELEGRAM_KNOWLEDGE_SESSIONS[key] = {
        "context_subject": "무역센터 kita",
        "created_at": now.isoformat(timespec="seconds"),
    }
    try:
        eq, _ = server._resolve_conversation_context(upd, "연면적 시공사 자료 찾아줘")
        assert eq.startswith("무역센터 kita")  # 후속질의 주제 상속
        # 새 주제는 상속 안 함
        eq2, _ = server._resolve_conversation_context(upd, "스프링클러 헤드 간격")
        assert eq2 == "스프링클러 헤드 간격"
        # 조응 마커(그거/해당)가 있으면 콘텐츠 명사가 있어도 직전 주제 상속('그거 청소공간은?' 등)
        eqa, _ = server._resolve_conversation_context(upd, "그거 청소공간은?")
        assert eqa.startswith("무역센터 kita")
        eqb, _ = server._resolve_conversation_context(upd, "해당 스트레이너 위치는?")
        assert eqb.startswith("무역센터 kita")
        # _recent_context_subject: 최근이면 주제 반환(문맥 재시도 게이트)
        assert server._recent_context_subject(upd) == "무역센터 kita"
        # 15분 초과면 상속 안 함 + _recent_context_subject 빈 문자열
        server.TELEGRAM_KNOWLEDGE_SESSIONS[key]["created_at"] = (
            now - _dt.timedelta(minutes=20)).isoformat(timespec="seconds")
        eq3, _ = server._resolve_conversation_context(upd, "연면적 알려줘")
        assert eq3 == "연면적 알려줘"
        assert server._recent_context_subject(upd) == ""
    finally:
        server.TELEGRAM_KNOWLEDGE_SESSIONS.pop(key, None)


def test_revit_assistant_answer_hides_internal_paths_and_scores():
    """유료 Revit 애드인 답변은 내부 KB 파일 경로/relevance score 를 고객에게
    노출하지 않고 친근한 지식 베이스 이름만 표기해야 한다(내부 조직구조 노출 방지)."""
    from backend.obsidian_notes import build_revit_assistant_answer
    matches = server.search_local_knowledge("BIM Command Center 가격", limit=4)
    answer = build_revit_assistant_answer("BIM Command Center 가격", matches, "라이선스결제")
    assert "knowledge/" not in answer and "10_agents" not in answer  # 내부 경로 미노출
    assert "score " not in answer and ".md" not in answer            # score/파일명 확장자 미노출
    assert "참고한 지식 베이스" in answer                              # 친근한 출처 표기는 유지


# ── 핵심 공종 라우팅은 폴백 도입 후에도 그대로여야 한다(회귀 방지) ──
CORE_DISCIPLINE_CASES = [
    ("방화구획 벽 관통부 처리", "건축"),
    ("철근 콘크리트 슬래브 배근", "구조"),
    ("우수 배수 구배 토공", "토목"),
    ("오배수 통기관 트랩 봉수", "위생"),
    ("냉각수 cws 배관 유체", "공조배관"),
    ("스프링클러 헤드 살수반경", "소방기계"),
    ("화재감지기 수신기 연동", "소방전기"),
    ("분전반 케이블 트레이 충전율", "전기"),
    ("mdf idf 광케이블 통신실", "통신"),
    ("navisworks clash 간섭 공차 bcf", "간섭검토"),
]


@pytest.mark.parametrize("query,expected_agent", CORE_DISCIPLINE_CASES)
def test_core_discipline_routing_unchanged(query, expected_agent):
    assert server.infer_knowledge_agent_from_query(query) == expected_agent


@pytest.mark.parametrize("query,expected_agent", CORE_DISCIPLINE_CASES)
def test_core_discipline_answer_is_local_ready(query, expected_agent):
    """핵심 공종 현실 질의는 로컬 지식만으로 즉답 가능(웹검색/추가 API 불필요)."""
    matches = server.search_local_knowledge(query, limit=3)
    answer = server.build_knowledge_answer(query, matches)
    readiness = server.assess_team_telegram_answer_readiness(
        query, expected_agent, matches, answer
    )
    assert readiness["should_search"] is False, (
        f"{expected_agent}: 로컬 즉답 실패 reasons={readiness['reasons']}"
    )

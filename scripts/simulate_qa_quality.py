#!/usr/bin/env python3
"""
simulate_qa_quality.py — LUA BIM LABS Q&A 품질 시뮬레이션

목적:
  실제 유입될 만한 질문들을 시뮬레이션하고, 지식베이스가 얼마나
  전문적인 수준의 답변을 제공하는지 자동 채점한다.
  주 1회 실행을 전제로 설계. 결과는 logs/qa_simulation/ 에 저장.

실행:
  python3 scripts/simulate_qa_quality.py
  python3 scripts/simulate_qa_quality.py --domain 간섭검토
  python3 scripts/simulate_qa_quality.py --verbose
  python3 scripts/simulate_qa_quality.py --min-score 70
  python3 scripts/simulate_qa_quality.py --min-score 90 --min-pass-rate 100 --no-save
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import backend.server_total as server  # noqa: E402

LOG_DIR = PROJECT_ROOT / "logs" / "qa_simulation"
LOG_DIR.mkdir(parents=True, exist_ok=True)

TODAY = datetime.date.today().isoformat()


# ─────────────────────────────────────────────────────────────────────────────
# 시뮬레이션 질문 데이터셋
# 형식: (질문, 예상_파일_stem, 필수_키워드, 품질_가중치_기준)
# 품질_가중치_기준: "numeric" | "regulation" | "conditional" | "general"
# ─────────────────────────────────────────────────────────────────────────────
class TestCase(NamedTuple):
    question: str
    expected_stem: str
    required_keywords: list[str]
    quality_type: str  # numeric / regulation / conditional / general
    domain: str
    customer_context: str = "일반 고객"
    asker_seniority: int = 0
    expert_panel_role: str = "도메인 QA 패널"
    context_keywords: tuple[str, ...] = ()


def _seniority_panel_cases() -> list[TestCase]:
    """1년차부터 20년차 AI 조직원 전문가가 던지는 깊이별 검증 질문."""
    return [
        TestCase("CHWS와 CHWR의 차이를 초보 고객에게 한 문단으로 설명할 수 있나요?",
                 "공조배관", ["chws", "chwr", "공급"], "general", "공조배관",
                 "입문 학습자", 1, "공조배관 주니어", ("초보", "차이", "공급")),
        TestCase("Revit에서 배관 계통명이 뒤바뀌었을 때 초급 모델러가 확인할 순서는?",
                 "공조배관", ["revit", "계통", "방향"], "general", "공조배관",
                 "초급 모델러", 2, "Revit MEP 주니어", ("순서", "확인", "revit")),
        TestCase("덕트 풍속 기준을 설계 보조자가 도면 검토에 적용하려면 어떤 수치를 봐야 하나요?",
                 "공조덕트", ["풍속", "m/s", "소음"], "numeric", "공조덕트",
                 "설계 보조자", 3, "공조덕트 주니어", ("수치", "기준", "도면")),
        TestCase("DN100 오배수 구배가 맞지 않을 때 현장 BIM 담당자는 어떤 리스크를 먼저 봐야 하나요?",
                 "위생", ["dn100", "구배", "막힘"], "numeric", "위생",
                 "현장 BIM 담당자", 4, "위생 BIM 실무자", ("리스크", "현장", "구배")),
        TestCase("케이블 트레이 충전율 초과를 고객에게 설명할 때 비용보다 먼저 말해야 할 품질 리스크는?",
                 "전기", ["50%", "발열", "증설"], "numeric", "전기",
                 "전기 BIM 고객", 5, "전기 BIM 실무자", ("리스크", "발열", "품질")),
        TestCase("제연 덕트와 일반 덕트가 충돌하면 조율회의에서 어떤 공종을 우선 보호해야 하나요?",
                 "간섭검토", ["제연", "소방", "우선"], "conditional", "간섭검토",
                 "조율회의 참석자", 6, "간섭검토 실무자", ("우선", "회의", "조율")),
        TestCase("Navisworks 클래시가 수천 건일 때 실무 리더는 어떤 규칙으로 노이즈를 줄여야 하나요?",
                 "간섭검토", ["navisworks", "rule", "공차"], "conditional", "Navisworks실무",
                 "BIM 실무 리더", 7, "Navisworks 실무자", ("노이즈", "규칙", "우선순위")),
        TestCase("방화구획 관통 MEP 이슈를 건축, 설비, 소방 관점에서 분리해 설명할 수 있나요?",
                 "건축", ["방화구획", "내화채움", "슬리브"], "conditional", "건축",
                 "복합 공종 고객", 8, "건축 조율 전문가", ("건축", "설비", "소방")),
        TestCase("LOD 300과 LOD 350 차이를 납품 품질 기준으로 판단하면 어떤 증거가 필요하나요?",
                 "건축", ["lod 300", "lod 350", "공종"], "conditional", "BIM프로세스",
                 "납품 품질 관리자", 9, "BIM 품질 관리자", ("납품", "증거", "품질")),
        TestCase("스프링클러 살수 장애를 단순 간섭이 아니라 생명안전 리스크로 설명하려면 무엇이 빠지면 안 되나요?",
                 "소방기계", ["살수", "장애", "헤드"], "numeric", "소방기계",
                 "소방 안전 고객", 10, "소방기계 전문가", ("생명안전", "리스크", "장애")),
        TestCase("MEP 공종 우선순위를 프로젝트 표준으로 만들 때 예외 규칙은 어떻게 둬야 하나요?",
                 "설비시공조율", ["제연", "소방", "오배수"], "conditional", "MEP조율",
                 "프로젝트 BIM 매니저", 11, "시공조율 리더", ("예외", "표준", "프로젝트")),
        TestCase("간섭 보고서가 발주처 의사결정 자료가 되려면 어떤 필드와 등급 체계가 필요하나요?",
                 "간섭검토", ["클래시id", "bcf", "critical"], "conditional", "BIM프로세스",
                 "발주처 보고 고객", 12, "BIM 프로세스 관리자", ("의사결정", "등급", "보고")),
        TestCase("전기실 상부 배관 금지 원칙을 비용, 안전, 유지보수 관점에서 어떻게 설득해야 하나요?",
                 "전기", ["전기실", "누수", "안전"], "conditional", "전기",
                 "PM/공사관리 고객", 13, "전기 조율 책임자", ("비용", "안전", "유지보수")),
        TestCase("Revit 간섭검토와 Navisworks 검토를 조직 표준으로 나누는 기준은 무엇인가요?",
                 "간섭검토", ["revit", "navisworks", "hard clash"], "conditional", "Revit실무",
                 "BIM 조직 운영자", 14, "BIM 표준 관리자", ("조직", "표준", "기준")),
        TestCase("고객 질문이 법규 확인인지 실무 조율인지 구분하려면 답변 전에 어떤 맥락을 확인해야 하나요?",
                 "요구사항분석", ["요구사항", "범위", "확인"], "conditional", "요구사항분석",
                 "상담/영업 고객", 15, "요구사항 분석가", ("맥락", "범위", "확인")),
        TestCase("모델 QA 상품에서 자동 검사와 전문가 검토의 경계를 고객에게 어떻게 설명해야 하나요?",
                 "QA_테스터", ["기능", "재현", "케이스"], "conditional", "QA_테스터",
                 "유료 QA 고객", 16, "QA 리드", ("자동", "전문가", "경계")),
        TestCase("같은 간섭 질문에 대해 초보자, BIM 매니저, 발주처에게 답변 구조를 어떻게 다르게 잡아야 하나요?",
                 "간섭검토", ["제연", "소방", "오배수"], "conditional", "간섭검토",
                 "혼합 이해관계자", 17, "전략 조율 전문가", ("초보자", "매니저", "발주처")),
        TestCase("QA 답변이 법적 확답처럼 오해되지 않게 하면서도 실무적으로 유용하려면 어떤 표현 원칙이 필요한가요?",
                 "고객지원CS", ["범위", "안내", "확인"], "conditional", "고객지원CS",
                 "리스크 민감 고객", 18, "고객지원 책임자", ("오해", "범위", "실무")),
        TestCase("LUA BIM LABS의 지식 답변 품질을 제품화하려면 어떤 평가 축을 KPI로 삼아야 하나요?",
                 "지식큐레이터", ["지식", "검토", "qa"], "conditional", "지식큐레이터",
                 "내부 운영진", 19, "지식 품질 책임자", ("kpi", "평가", "품질")),
        TestCase("20년차 전문가라면 이 답변 체계가 3년 뒤에도 유효하려면 어떤 지식 업데이트 루프가 필요하다고 보나요?",
                 "지식업데이트", ["업데이트", "검토", "지식"], "conditional", "지식업데이트",
                 "장기 전략 고객", 20, "지식 전략 책임자", ("장기", "업데이트", "루프")),
    ]


SIMULATION_CASES: list[TestCase] = _seniority_panel_cases() + [

    # ────────── 간섭검토 ──────────────────────────────────────────────────────
    TestCase("소화배관이 전기 케이블 트레이 위에 놓여 있으면 문제가 있나요?",
             "간섭검토", ["300mm", "이격", "누수"], "numeric", "간섭검토"),
    TestCase("Revit에서 건축과 MEP 간섭 검토할 때 Interference Check랑 Navisworks 중 뭘 써야 해?",
             "간섭검토", ["hard clash", "navisworks", "revit"], "conditional", "간섭검토"),
    TestCase("구조 보에 배관을 관통할 수 있나요? 기준이 어떻게 되나요?",
             "간섭검토", ["기둥", "관통", "1/3"], "numeric", "간섭검토"),
    TestCase("오배수 배관이 공조 덕트와 충돌하면 어느 쪽을 움직여야 하나요?",
             "간섭검토", ["구배", "오배수", "우회"], "conditional", "간섭검토"),
    TestCase("스프링클러 헤드 위에 덕트가 있어도 되나요?",
             "간섭검토", ["살수", "장애", "1.2m"], "numeric", "간섭검토"),
    TestCase("강전 케이블 트레이와 약전 트레이 이격 기준이 얼마예요?",
             "간섭검토", ["300mm", "격벽", "이격"], "numeric", "간섭검토"),
    TestCase("Navisworks 클래시 테스트를 All vs All로 돌렸더니 수천 건이 나왔어요",
             "간섭검토", ["same system", "rule", "공차"], "conditional", "간섭검토"),
    TestCase("공종별 간섭 조율 우선순위를 알려주세요",
             "간섭검토", ["제연", "소방", "오배수"], "conditional", "간섭검토"),
    TestCase("방화댐퍼는 벽체에서 얼마나 이격해서 설치해야 하나요?",
             "간섭검토", ["밀착", "방화구획", "600mm"], "numeric", "간섭검토"),
    TestCase("간섭 보고서 어떤 항목으로 작성해야 하나요?",
             "간섭검토", ["클래시id", "bcf", "rfi"], "general", "간섭검토"),

    # ────────── 구조 ──────────────────────────────────────────────────────────
    TestCase("전이보에 배관을 관통할 수 있나요?",
             "구조", ["전이보", "불가", "절대"], "conditional", "구조"),
    TestCase("RC 보 관통 허용 기준이 뭔가요?",
             "구조", ["1/3", "중앙", "구조기술사"], "numeric", "구조"),
    TestCase("PC 보에 현장에서 배관 구멍 뚫어도 되나요?",
             "구조", ["pc", "슬리브", "공장"], "conditional", "구조"),
    TestCase("슬래브에 개구부 낼 때 보강근이 필요한가요?",
             "구조", ["슬래브", "개구부", "보강"], "conditional", "구조"),

    # ────────── 위생 ──────────────────────────────────────────────────────────
    TestCase("DN100 오배수 배관의 최소 구배는 얼마예요?",
             "위생", ["1/100", "dn100", "구배"], "numeric", "위생"),
    TestCase("통기관 끝단을 지붕에서 얼마나 올려야 하나요?",
             "위생", ["600mm", "지붕", "통기"], "numeric", "위생"),
    TestCase("BIM에서 오배수 배관 구배 어떻게 설정하나요?",
             "위생", ["slope", "revit", "구배"], "general", "위생"),
    TestCase("집수정 배수펌프 흡입 배관 설계 시 주의사항은?",
             "위생", ["공기", "흡입", "역류"], "conditional", "위생"),

    # ────────── 공조 덕트 ──────────────────────────────────────────────────────
    TestCase("제연 덕트와 일반 덕트 이격 기준이 얼마예요?",
             "공조덕트", ["100mm", "제연", "이격"], "numeric", "공조덕트"),
    TestCase("방화댐퍼 설치 시 점검구 위치 기준이 어떻게 되나요?",
             "공조덕트", ["600mm", "댐퍼", "점검구"], "numeric", "공조덕트"),
    TestCase("주방 배기 덕트와 일반 급기 덕트 이격은 얼마나 해야 하나요?",
             "공조덕트", ["500mm", "주방", "유증기"], "numeric", "공조덕트"),
    TestCase("Revit에서 덕트 단열 포함 외경으로 간섭 검토하려면?",
             "공조덕트", ["insulation", "단열", "외경"], "general", "공조덕트"),

    # ────────── 소방 ──────────────────────────────────────────────────────────
    TestCase("폐쇄형 스프링클러 헤드 최대 간격은 얼마예요?",
             "소방기계", ["3.7m", "헤드", "폐쇄"], "numeric", "소방기계"),
    TestCase("소화배관과 전기 케이블 트레이 최소 이격거리가 얼마예요?",
             "소방기계", ["300mm", "트레이", "이격"], "numeric", "소방기계"),
    TestCase("습식 vs 준비작동식 스프링클러 언제 사용하나요?",
             "소방기계", ["습식", "준비작동", "전산실"], "conditional", "소방기계"),
    TestCase("스프링클러 헤드 아래 덕트가 있으면 살수 장애 판정 받나요?",
             "소방기계", ["1.2m", "살수", "장애"], "numeric", "소방기계"),

    # ────────── 전기 ──────────────────────────────────────────────────────────
    TestCase("케이블 트레이 충전율 기준이 어떻게 되나요?",
             "전기", ["50%", "충전율", "트레이"], "numeric", "전기"),
    TestCase("수배전반 근처에 냉수 배관 설치 시 이격 기준은?",
             "전기", ["1m", "큐비클", "누수"], "numeric", "전기"),
    TestCase("강전 트레이 바로 위에 냉수 배관을 설치하면 안 되는 이유는?",
             "전기", ["결로", "낙하", "트레이"], "conditional", "전기"),
    TestCase("분전반 전면 클리어런스가 얼마인가요?",
             "전기", ["1m", "분전반", "작업"], "numeric", "전기"),

    # ────────── 통신 ──────────────────────────────────────────────────────────
    TestCase("MDF와 IDF 같은 실에 강전 분전반 설치해도 되나요?",
             "통신", ["금지", "mdf", "idf"], "conditional", "통신"),
    TestCase("통신 케이블과 전력선 이격 기준이 어떻게 되나요?",
             "통신", ["150mm", "emi", "tia"], "numeric", "통신"),
    TestCase("통신실 온도 기준이 어떻게 되나요?",
             "통신", ["27", "냉방", "서버"], "numeric", "통신"),

    # ────────── 건축 ──────────────────────────────────────────────────────────
    TestCase("방화구획을 MEP 배관이 관통할 때 어떻게 처리하나요?",
             "건축", ["슬리브", "내화채움", "방화댐퍼"], "conditional", "건축"),
    TestCase("BIM LOD 300과 LOD 350 차이는 무엇인가요?",
             "건축", ["lod 300", "lod 350", "공종"], "conditional", "건축"),
    TestCase("엘리베이터 샤프트 내부에 배관 설치해도 되나요?",
             "건축", ["샤프트", "금지", "피트"], "conditional", "건축"),

    # ────────── Revit / Navisworks 실무 ───────────────────────────────────────
    TestCase("Revit에서 구조 보 하단에 배관이 겹치는지 어떻게 확인하나요?",
             "간섭검토", ["interference check", "link", "revit"], "general", "Revit실무"),
    TestCase("Navisworks에서 소방 배관 vs 구조만 테스트하는 방법은?",
             "간섭검토", ["selection", "clash detective", "rule"], "general", "Navisworks실무"),
    TestCase("BCF 파일로 클래시 이슈를 담당자에게 전달하는 방법은?",
             "간섭검토", ["bcf", "rfi", "bim 360"], "general", "BIM협업"),

    # ────────── BIM 프로세스 ───────────────────────────────────────────────────
    TestCase("BIM 간섭 검토 보고서 등급 분류 기준이 어떻게 되나요?",
             "간섭검토", ["critical", "major", "minor"], "conditional", "BIM프로세스"),
    TestCase("LOD 400 모델 납품 전 0 Hard Clash를 달성해야 하나요?",
             "간섭검토", ["lod 400", "hard clash", "서명"], "conditional", "BIM프로세스"),
    TestCase("NWC 파일 내보낼 때 Revit 버전 통일이 왜 중요한가요?",
             "설비시공조율", ["nwc", "버전", "좌표"], "conditional", "BIM프로세스"),

    # ────────── 설비시공조율 ───────────────────────────────────────────────────
    TestCase("MEP 공종 우선순위 전체 순서를 알려주세요",
             "설비시공조율", ["제연", "소방", "오배수"], "conditional", "MEP조율"),
    TestCase("기계실 장비 반입 경로를 BIM에서 어떻게 검토하나요?",
             "설비시공조율", ["반입", "기계실", "장비"], "general", "MEP조율"),
    TestCase("천장 속 설비 배치 순서가 어떻게 되나요?",
             "설비시공조율", ["덕트", "소방", "트레이"], "conditional", "MEP조율"),

    # ────────── 법규 ──────────────────────────────────────────────────────────
    TestCase("NFTC 103 스프링클러 기준 번호가 어떻게 되나요?",
             "소방기계", ["nftc", "103", "스프링클러"], "regulation", "소방법규"),
    TestCase("방화구획 관통 처리 건축법 조항이 어떻게 되나요?",
             "건축", ["건축법", "시행령", "방화구획"], "regulation", "건축법규"),
    TestCase("KEC 전기설비기술기준 케이블 트레이 관련 조항은?",
             "전기", ["kec", "케이블트레이", "이격"], "regulation", "전기법규"),
    TestCase("위생설비 배수 구배 KS 기준 조항은?",
             "위생", ["ks", "구배", "배수"], "regulation", "위생법규"),
]


# ─────────────────────────────────────────────────────────────────────────────
# 지식 검색 엔진
# ─────────────────────────────────────────────────────────────────────────────

def _stem_for_match(match: dict) -> str:
    path = match.get("path")
    if isinstance(path, Path):
        return path.stem.removesuffix("_QA")
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# 품질 채점 기준
# ─────────────────────────────────────────────────────────────────────────────

# 전문적 답변에 포함돼야 할 패턴
_NUMERIC_PATTERN = re.compile(
    r"\b(\d+\.?\d*\s*(mm|cm|m|m²|pa|℃|%|hz|v|kw|kva|lux|db|dn\d+|lod|1/\d+))\b", re.IGNORECASE
)
_REGULATION_PATTERN = re.compile(
    r"\b(nftc|nfpc|kds|kec|kcs|ks[a-z]?\s*\d|건축법|소방법|하수도법|tia-\d+|iso\s*\d+)\b", re.IGNORECASE
)
_CONDITION_WORDS = ["경우", "조건", "반면", "단,", "불가", "가능", "허용", "금지", "단계", "먼저", "우선"]
_SHALLOW_SIGNALS = ["확인이 필요", "담당자에게 문의", "일반적으로 확인", "경우에 따라 다름"]


def score_quality(excerpt: str, quality_type: str, required_keywords: list[str]) -> dict:
    """
    답변 품질을 100점 만점으로 채점한다.
    반환: {total, routing, numeric, regulation, depth, keywords, breakdown}
    """
    excerpt_lower = excerpt.lower()

    # 1. 키워드 존재 여부 (40점)
    kw_hit = sum(1 for kw in required_keywords if kw.lower() in excerpt_lower)
    kw_score = int(kw_hit / max(len(required_keywords), 1) * 40)

    # 2. 수치/기준값 포함 여부 (20점)
    numeric_matches = _NUMERIC_PATTERN.findall(excerpt)
    if quality_type == "numeric":
        numeric_score = min(len(numeric_matches) * 7, 20)
    else:
        numeric_score = min(len(numeric_matches) * 4, 20)

    # 3. 법규 조항 인용 여부 (15점)
    regulation_matches = _REGULATION_PATTERN.findall(excerpt)
    if quality_type == "regulation":
        regulation_score = min(len(regulation_matches) * 8, 15)
    else:
        regulation_score = min(len(regulation_matches) * 5, 15)

    # 4. 조건 분기 (전문성) (15점)
    if quality_type == "conditional":
        cond_hits = sum(1 for w in _CONDITION_WORDS if w in excerpt_lower)
        cond_score = min(cond_hits * 4, 15)
    else:
        cond_hits = sum(1 for w in _CONDITION_WORDS if w in excerpt_lower)
        cond_score = min(cond_hits * 2, 15)

    # 5. 얕은 답변 패널티 (-10점)
    shallow_penalty = sum(5 for s in _SHALLOW_SIGNALS if s in excerpt_lower)
    shallow_penalty = min(shallow_penalty, 10)

    # 6. 응답 밀도 보너스 (10점)
    density_score = min(len(excerpt) // 150, 10)

    total = max(0, kw_score + numeric_score + regulation_score + cond_score
                - shallow_penalty + density_score)
    total = min(total, 100)

    return {
        "total": total,
        "keywords": kw_score,
        "numeric": numeric_score,
        "regulation": regulation_score,
        "conditional": cond_score,
        "shallow_penalty": -shallow_penalty,
        "density": density_score,
        "kw_hit": kw_hit,
        "kw_total": len(required_keywords),
    }


def score_customer_fit(excerpt: str, context_keywords: tuple[str, ...]) -> dict:
    """고객 맥락, 질문 의도, 이해관계자 관점이 답변에 반영됐는지 채점한다."""
    if not context_keywords:
        return {"total": 10, "hit": 0, "total_keywords": 0, "missing": []}

    excerpt_lower = excerpt.lower()
    hits = [kw for kw in context_keywords if kw.lower() in excerpt_lower]
    missing = [kw for kw in context_keywords if kw.lower() not in excerpt_lower]
    score = int(len(hits) / len(context_keywords) * 10)
    return {
        "total": score,
        "hit": len(hits),
        "total_keywords": len(context_keywords),
        "missing": missing,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 시뮬레이션 실행
# ─────────────────────────────────────────────────────────────────────────────

def run_simulation(
    domain_filter: str | None = None,
    verbose: bool = False,
    min_score: int = 60,
) -> dict:
    cases = SIMULATION_CASES
    if domain_filter:
        cases = [c for c in cases if c.domain == domain_filter or c.expected_stem == domain_filter]

    results = []
    domain_stats: dict[str, list[int]] = {}
    customer_stats: dict[str, list[int]] = {}
    seniority_stats: dict[str, list[int]] = {}

    for case in cases:
        matches = server.search_local_knowledge(case.question, limit=5)
        top_stems = [_stem_for_match(match) for match in matches[:3]]
        top_stem = top_stems[0] if top_stems else ""
        routing_ok = case.expected_stem in top_stems

        excerpt = server.build_knowledge_answer(case.question, matches) if matches else ""

        quality = score_quality(excerpt, case.quality_type, case.required_keywords)
        customer_fit = score_customer_fit(excerpt, case.context_keywords)
        score = quality["total"]
        if not routing_ok:
            score = max(0, score - 20)  # 라우팅 실패 패널티
        if case.context_keywords:
            score = max(0, score - (10 - customer_fit["total"]))  # 고객 맥락 누락 패널티

        passed = score >= min_score

        result = {
            "question": case.question,
            "domain": case.domain,
            "customer_context": case.customer_context,
            "asker_seniority": case.asker_seniority,
            "expert_panel_role": case.expert_panel_role,
            "expected": case.expected_stem,
            "top1": top_stem,
            "top3": top_stems,
            "routing_ok": routing_ok,
            "score": score,
            "quality": quality,
            "customer_fit": customer_fit,
            "passed": passed,
            "quality_type": case.quality_type,
        }
        results.append(result)

        if case.domain not in domain_stats:
            domain_stats[case.domain] = []
        domain_stats[case.domain].append(score)

        if case.customer_context not in customer_stats:
            customer_stats[case.customer_context] = []
        customer_stats[case.customer_context].append(score)

        if case.asker_seniority:
            seniority_band = _seniority_band(case.asker_seniority)
            if seniority_band not in seniority_stats:
                seniority_stats[seniority_band] = []
            seniority_stats[seniority_band].append(score)

        if verbose:
            mark = "OK" if passed else "NG"
            seniority = f"{case.asker_seniority}년차 " if case.asker_seniority else ""
            print(f"{mark} [{score:3d}점] [{case.domain:<12}] {seniority}{case.question[:55]}")
            if not passed:
                print(f"     라우팅: {'OK' if routing_ok else f'FAIL (top1={top_stem}, 예상={case.expected_stem})'}")
                print(f"     키워드: {quality['kw_hit']}/{quality['kw_total']} | "
                      f"수치:{quality['numeric']} 법규:{quality['regulation']} 조건:{quality['conditional']}")
                if case.context_keywords:
                    print(f"     고객맥락: {customer_fit['hit']}/{customer_fit['total_keywords']} | "
                          f"누락:{', '.join(customer_fit['missing'])}")

    passed_count = sum(1 for r in results if r["passed"])
    total = len(results)
    rate = int(passed_count / total * 100) if total else 0
    avg_score = int(sum(r["score"] for r in results) / total) if total else 0

    domain_summary = {}
    for domain, scores in domain_stats.items():
        domain_summary[domain] = {
            "avg": int(sum(scores) / len(scores)),
            "min": min(scores),
            "count": len(scores),
            "pass_count": sum(1 for s in scores if s >= min_score),
        }

    customer_summary = _score_summary(customer_stats, min_score)
    seniority_summary = _score_summary(seniority_stats, min_score)

    # 저품질 순으로 정렬 (개선 우선순위)
    low_quality = sorted(
        [r for r in results if not r["passed"]],
        key=lambda r: r["score"]
    )

    return {
        "date": TODAY,
        "total": total,
        "passed": passed_count,
        "rate": rate,
        "avg_score": avg_score,
        "min_score_threshold": min_score,
        "results": results,
        "domain_summary": domain_summary,
        "customer_summary": customer_summary,
        "seniority_summary": seniority_summary,
        "low_quality": low_quality,
    }


def _seniority_band(year: int) -> str:
    if year <= 3:
        return "1-3년차 개념/기초"
    if year <= 7:
        return "4-7년차 실무/예외"
    if year <= 12:
        return "8-12년차 설계/품질"
    if year <= 16:
        return "13-16년차 조직/상품"
    return "17-20년차 전략/미래"


def _score_summary(stats: dict[str, list[int]], min_score: int) -> dict[str, dict]:
    summary = {}
    for key, scores in stats.items():
        summary[key] = {
            "avg": int(sum(scores) / len(scores)),
            "min": min(scores),
            "count": len(scores),
            "pass_count": sum(1 for s in scores if s >= min_score),
        }
    return summary


# ─────────────────────────────────────────────────────────────────────────────
# 리포트 생성
# ─────────────────────────────────────────────────────────────────────────────

def _verdict(rate: int) -> str:
    if rate >= 85:
        return "✅ PASS — 전문가 수준 답변 품질 양호"
    elif rate >= 70:
        return "⚠️  WARN — 일부 도메인 지식 보강 필요"
    else:
        return "❌ FAIL — 현장 전문가 수준 미달, 즉시 보강 필요"


def build_report(sim: dict) -> str:
    lines = [
        f"# LUA BIM LABS Q&A 품질 시뮬레이션 리포트",
        f"",
        f"실행일: {sim['date']}  |  기준점수: {sim['min_score_threshold']}점  |  "
        f"통과: {sim['passed']}/{sim['total']} ({sim['rate']}%)  |  평균: {sim['avg_score']}점",
        f"",
        f"**판정: {_verdict(sim['rate'])}**",
        f"",
        f"---",
        f"",
        f"## 도메인별 결과",
        f"",
        f"| 도메인 | 평균점수 | 최저점수 | 통과/전체 | 진단 |",
        f"|--------|----------|----------|-----------|------|",
    ]

    for domain, stat in sorted(sim["domain_summary"].items(), key=lambda x: x[1]["avg"]):
        avg = stat["avg"]
        verdict = "✅ 양호" if avg >= 75 else ("⚠️ 보강필요" if avg >= 55 else "❌ 갭심각")
        lines.append(
            f"| {domain} | {avg}점 | {stat['min']}점 | "
            f"{stat['pass_count']}/{stat['count']} | {verdict} |"
        )

    if sim.get("seniority_summary"):
        lines += [
            f"",
            f"---",
            f"",
            f"## 연차별 AI 전문가 패널 결과",
            f"",
            f"| 연차 구간 | 평균점수 | 최저점수 | 통과/전체 | 진단 |",
            f"|-----------|----------|----------|-----------|------|",
        ]
        for band, stat in sorted(sim["seniority_summary"].items()):
            avg = stat["avg"]
            verdict = "✅ 양호" if avg >= 75 else ("⚠️ 보강필요" if avg >= 55 else "❌ 갭심각")
            lines.append(
                f"| {band} | {avg}점 | {stat['min']}점 | "
                f"{stat['pass_count']}/{stat['count']} | {verdict} |"
            )

    if sim.get("customer_summary"):
        lines += [
            f"",
            f"---",
            f"",
            f"## 고객 맥락별 결과",
            f"",
            f"| 고객 맥락 | 평균점수 | 최저점수 | 통과/전체 | 진단 |",
            f"|-----------|----------|----------|-----------|------|",
        ]
        for context, stat in sorted(sim["customer_summary"].items(), key=lambda x: x[1]["avg"]):
            avg = stat["avg"]
            verdict = "✅ 양호" if avg >= 75 else ("⚠️ 보강필요" if avg >= 55 else "❌ 갭심각")
            lines.append(
                f"| {context} | {avg}점 | {stat['min']}점 | "
                f"{stat['pass_count']}/{stat['count']} | {verdict} |"
            )

    if sim["low_quality"]:
        lines += [
            f"",
            f"---",
            f"",
            f"## 저품질 답변 — 우선 개선 대상 ({len(sim['low_quality'])}건)",
            f"",
        ]
        for r in sim["low_quality"][:15]:
            score_icon = "🔴" if r["score"] < 40 else "🟡"
            seniority = f" | **질문자**: {r['asker_seniority']}년차 {r['expert_panel_role']}" if r["asker_seniority"] else ""
            lines += [
                f"### {score_icon} [{r['score']}점] {r['question']}",
                f"- **도메인**: {r['domain']} | **고객맥락**: {r['customer_context']}{seniority}",
                f"- **예상파일**: `{r['expected']}` | **실제top1**: `{r['top1']}`",
                f"- **라우팅**: {'✅ 정상' if r['routing_ok'] else '❌ 오류 — 키워드 매핑 확인 필요'}",
                f"- **품질분석**: 키워드 {r['quality']['kw_hit']}/{r['quality']['kw_total']} | "
                f"수치점수 {r['quality']['numeric']} | 법규점수 {r['quality']['regulation']} | "
                f"조건점수 {r['quality']['conditional']} | 고객맥락 {r['customer_fit']['hit']}/{r['customer_fit']['total_keywords']}",
                f"- **개선방향**: " + _improvement_hint(r),
                f"",
            ]

    lines += [
        f"---",
        f"",
        f"## 개선 권장 액션",
        f"",
    ]
    actions = _generate_actions(sim)
    for i, action in enumerate(actions, 1):
        lines.append(f"{i}. {action}")

    return "\n".join(lines)


def _improvement_hint(result: dict) -> str:
    hints = []
    if not result["routing_ok"]:
        hints.append(f"`knowledge_store.py` DISCIPLINE_KEYWORDS에 `{result['expected']}` 관련 키워드 추가")
    q = result["quality"]
    if q["numeric"] < 8:
        hints.append(f"`{result['expected']}.md` 에 구체적 수치(mm, %, °C 등) 추가")
    if q["regulation"] < 5:
        hints.append(f"`{result['expected']}.md` 에 관련 법규 조항(NFTC/KDS/KEC) 명시")
    if q["kw_hit"] < q["kw_total"] // 2:
        hints.append(f"`{result['expected']}.md` 지식 내용 자체 보강 필요")
    customer_fit = result.get("customer_fit", {})
    if customer_fit.get("total_keywords") and customer_fit.get("total", 10) < 7:
        missing = ", ".join(customer_fit.get("missing", [])[:4])
        hints.append(f"고객 맥락 반영 부족 — 누락 관점: {missing}")
    return " / ".join(hints) if hints else "지식 내용 심화 보강 필요"


def _generate_actions(sim: dict) -> list[str]:
    actions = []

    # 라우팅 실패가 많은 도메인
    routing_fails = [r for r in sim["results"] if not r["routing_ok"]]
    if routing_fails:
        stems = list({r["expected"] for r in routing_fails})
        actions.append(f"`knowledge_store.py` DISCIPLINE_KEYWORDS 보강: {', '.join(stems[:5])}")

    # 수치 점수 낮은 파일들
    low_numeric = [r for r in sim["results"] if r["quality"]["numeric"] < 7 and not r["passed"]]
    if low_numeric:
        stems = list({r["expected"] for r in low_numeric})[:4]
        actions.append(f"수치/기준값 부족 파일 보강: {', '.join(stems)} — 실무 이격거리·치수 추가")

    # 법규 점수 낮은 파일들
    low_reg = [r for r in sim["results"] if r["quality"]["regulation"] < 5 and not r["passed"]]
    if low_reg:
        stems = list({r["expected"] for r in low_reg})[:4]
        actions.append(f"법규 조항 미인용 파일 보강: {', '.join(stems)} — NFTC/KDS/KEC 조항 추가")

    # 도메인별 평균 낮은 순
    low_domains = [(d, s["avg"]) for d, s in sim["domain_summary"].items() if s["avg"] < 60]
    low_domains.sort(key=lambda x: x[1])
    for domain, avg in low_domains[:3]:
        actions.append(f"`{domain}` 도메인 전체 지식 재검토 — 현재 평균 {avg}점")

    if not actions:
        actions.append("현재 품질 양호 — auto-enrich 노이즈 정기 제거 및 신규 사례 Q&A 추가 권장")

    return actions


def exit_code_for_rate(pass_rate: int, min_pass_rate: int) -> int:
    return 0 if pass_rate >= min_pass_rate else 1


# ─────────────────────────────────────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="LUA BIM LABS Q&A 품질 시뮬레이션")
    parser.add_argument("--domain", help="특정 도메인만 테스트 (예: 간섭검토, 위생)")
    parser.add_argument("--verbose", "-v", action="store_true", help="질문별 상세 출력")
    parser.add_argument("--min-score", type=int, default=60, help="통과 기준 점수 (기본 60)")
    parser.add_argument("--min-pass-rate", type=int, default=70, help="전체 통과율 하한 % (기본 70)")
    parser.add_argument("--no-save", action="store_true", help="리포트 파일 저장 안 함")
    args = parser.parse_args()

    print("=" * 70)
    print(f"LUA BIM LABS Q&A 품질 시뮬레이션  ({TODAY})")
    print("=" * 70)

    if args.verbose:
        print()

    sim = run_simulation(
        domain_filter=args.domain,
        verbose=args.verbose,
        min_score=args.min_score,
    )

    report = build_report(sim)

    print()
    print(report)

    if not args.no_save:
        report_path = LOG_DIR / f"qa_simulation_{TODAY}.md"
        report_path.write_text(report, encoding="utf-8")

        json_path = LOG_DIR / f"qa_simulation_{TODAY}.json"
        json_path.write_text(
            json.dumps({k: v for k, v in sim.items() if k != "results"},
                       ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"\n📄 리포트 저장: {report_path}")
        print(f"📊 JSON 저장:   {json_path}")

    print(f"\n{'─'*70}")
    print(f"결과: {sim['passed']}/{sim['total']} 통과  ({sim['rate']}%)  |  평균점수: {sim['avg_score']}점")
    print(f"판정: {_verdict(sim['rate'])}")
    if sim["rate"] < args.min_pass_rate:
        print(f"FAIL: 통과율 {sim['rate']}% < 기준 {args.min_pass_rate}%")
    print("=" * 70)

    sys.exit(exit_code_for_rate(sim["rate"], args.min_pass_rate))


if __name__ == "__main__":
    main()

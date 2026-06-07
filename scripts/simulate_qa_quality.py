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
KB_DIR = PROJECT_ROOT / "data" / "knowledge_base"
QA_DIR = KB_DIR / "qa"
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


SIMULATION_CASES: list[TestCase] = [

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
# 지식 검색 엔진 (validate_knowledge_qa.py 와 동일 로직 재사용)
# ─────────────────────────────────────────────────────────────────────────────

_NOISE_LINES = ("- source:", "- tags:", "[tavily]", "[ddg]", "auto-enrich", "auto-quality",
                "needs-review", "자동 수집", "auto-collect", "출처: http")


def _query_terms(query: str) -> list[str]:
    raw = re.findall(r"[A-Za-z0-9_#+.\-가-힣]{2,}", query.lower())
    stopwords = {"으로","에서","대한","관련","정리","알려줘","기준","방법","어떻게","어떤",
                 "있어","인지","뭐야","뭐임","하나요","해요","됩니까","됩니다","입니까","이나요"}
    return [t for t in raw if t not in stopwords][:20]


def _score(text: str, terms: list[str]) -> int:
    lower = text.lower()
    return sum(min(lower.count(t), 6) for t in terms)


def _best_excerpt(content: str, terms: list[str], max_chars: int = 3000) -> str:
    sections = [s.strip() for s in re.split(r"(?=^## )", content, flags=re.MULTILINE) if s.strip()]
    if not sections:
        return content[:max_chars]

    def clean(s: str) -> str:
        return "\n".join(l for l in s.splitlines() if not any(n in l.lower() for n in _NOISE_LINES)).strip()

    scored = sorted(
        [(_score(s, terms), i, clean(s)) for i, s in enumerate(sections)],
        key=lambda x: (x[0], -x[1]), reverse=True
    )
    return scored[0][2][:max_chars] if scored else sections[0][:max_chars]


def _load_kb_files() -> dict[str, str]:
    """KB 파일과 QA 파일을 {stem: content} 로 모두 로드."""
    files: dict[str, str] = {}
    for path in KB_DIR.glob("*.md"):
        files[path.stem] = path.read_text(encoding="utf-8")
    for path in QA_DIR.glob("*_QA.md"):
        stem = path.stem.replace("_QA", "")
        existing = files.get(stem, "")
        files[stem] = existing + "\n\n" + path.read_text(encoding="utf-8")
    return files


def _search(question: str, kb: dict[str, str]) -> list[tuple[int, str]]:
    """질문에 가장 관련 있는 파일 top-5를 (score, stem) 형태로 반환."""
    terms = _query_terms(question)
    scored = []
    for stem, content in kb.items():
        s = _score(content, terms)
        if s > 0:
            scored.append((s, stem))
    scored.sort(reverse=True)
    return scored[:5]


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


# ─────────────────────────────────────────────────────────────────────────────
# 시뮬레이션 실행
# ─────────────────────────────────────────────────────────────────────────────

def run_simulation(
    domain_filter: str | None = None,
    verbose: bool = False,
    min_score: int = 60,
) -> dict:
    kb = _load_kb_files()

    cases = SIMULATION_CASES
    if domain_filter:
        cases = [c for c in cases if c.domain == domain_filter or c.expected_stem == domain_filter]

    results = []
    domain_stats: dict[str, list[int]] = {}

    for case in cases:
        ranked = _search(case.question, kb)
        top_stems = [s for _, s in ranked[:3]]
        top_stem = top_stems[0] if top_stems else ""
        routing_ok = case.expected_stem in top_stems

        # 답변 생성: 정답 파일 또는 실제 top1 파일에서 발췌
        answer_stem = case.expected_stem if case.expected_stem in kb else top_stem
        excerpt = _best_excerpt(kb.get(answer_stem, ""), _query_terms(case.question)) if answer_stem else ""

        quality = score_quality(excerpt, case.quality_type, case.required_keywords)
        score = quality["total"]
        if not routing_ok:
            score = max(0, score - 20)  # 라우팅 실패 패널티

        passed = score >= min_score

        result = {
            "question": case.question,
            "domain": case.domain,
            "expected": case.expected_stem,
            "top1": top_stem,
            "top3": top_stems,
            "routing_ok": routing_ok,
            "score": score,
            "quality": quality,
            "passed": passed,
            "quality_type": case.quality_type,
        }
        results.append(result)

        if case.domain not in domain_stats:
            domain_stats[case.domain] = []
        domain_stats[case.domain].append(score)

        if verbose:
            mark = "✅" if passed else "❌"
            print(f"{mark} [{score:3d}점] [{case.domain:<12}] {case.question[:55]}")
            if not passed:
                print(f"     라우팅: {'OK' if routing_ok else f'FAIL (top1={top_stem}, 예상={case.expected_stem})'}")
                print(f"     키워드: {quality['kw_hit']}/{quality['kw_total']} | "
                      f"수치:{quality['numeric']} 법규:{quality['regulation']} 조건:{quality['conditional']}")

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
        "low_quality": low_quality,
    }


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

    if sim["low_quality"]:
        lines += [
            f"",
            f"---",
            f"",
            f"## 저품질 답변 — 우선 개선 대상 ({len(sim['low_quality'])}건)",
            f"",
        ]
        for r in sim["low_quality"][:15]:
            q = score_icon = ""
            score_icon = "🔴" if r["score"] < 40 else "🟡"
            lines += [
                f"### {score_icon} [{r['score']}점] {r['question']}",
                f"- **도메인**: {r['domain']} | **예상파일**: `{r['expected']}` | **실제top1**: `{r['top1']}`",
                f"- **라우팅**: {'✅ 정상' if r['routing_ok'] else '❌ 오류 — 키워드 매핑 확인 필요'}",
                f"- **품질분석**: 키워드 {r['quality']['kw_hit']}/{r['quality']['kw_total']} | "
                f"수치점수 {r['quality']['numeric']} | 법규점수 {r['quality']['regulation']} | "
                f"조건점수 {r['quality']['conditional']}",
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
        missing = [kw for kw in result["quality_type"] if True]
        hints.append(f"`{result['expected']}.md` 지식 내용 자체 보강 필요")
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


# ─────────────────────────────────────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="LUA BIM LABS Q&A 품질 시뮬레이션")
    parser.add_argument("--domain", help="특정 도메인만 테스트 (예: 간섭검토, 위생)")
    parser.add_argument("--verbose", "-v", action="store_true", help="질문별 상세 출력")
    parser.add_argument("--min-score", type=int, default=60, help="통과 기준 점수 (기본 60)")
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
    print("=" * 70)

    sys.exit(0 if sim["rate"] >= 70 else 1)


if __name__ == "__main__":
    main()

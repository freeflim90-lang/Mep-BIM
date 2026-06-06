#!/usr/bin/env python3
"""
지식 베이스 QA 검증 스크립트
각 AI 담당자 전문 질문에 대해 올바른 파일이 최상위로 검색되고
정답 키워드가 발췌문에 포함되는지 측정한다.

실행:
  python3 scripts/validate_knowledge_qa.py
  python3 scripts/validate_knowledge_qa.py --agent Revit_Addin
  python3 scripts/validate_knowledge_qa.py --verbose
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ──────────────────────────────────────────────
# QA 데이터셋: (질문, 정답파일 stem, 정답 키워드 목록)
# 정답 키워드는 최소 2개 이상 발췌문에 포함돼야 PASS
# ──────────────────────────────────────────────
QA_DATASET: list[tuple[str, str, list[str]]] = [
    # ── Revit Add-in
    ("Revit 2027 .NET 10 마이그레이션 시 주의사항이 뭐야?",
     "Revit_Addin", ["net10", "마이그레이션", ".net 8", "programfiles"]),
    ("Revit API FilteredElementCollector 사용법",
     "Revit_Addin", ["filteredElementCollector", "revit", "요소 수집"]),
    ("Revit 2027 새로운 기능 MCP AI Assistant",
     "Revit_Addin", ["mcp", "ai assistant", "forma"]),

    # ── Dynamo
    ("Dynamo에서 Element.GetParameterValueByName 노드 사용법",
     "Dynamo", ["GetParameterValueByName", "Element", "Dynamo"]),
    ("Dynamo Python 스크립트로 카테고리별 요소 선택",
     "Dynamo", ["FilteredElementCollector", "python", "Categories"]),

    # ── 공조배관
    ("CHWS CHWR 냉수 배관 약어 설명",
     "공조배관", ["chws", "chwr", "냉수", "공급"]),
    ("냉각수 배관 CWS CWR 계통 설명",
     "공조배관", ["cws", "cwr", "냉각수", "냉각탑"]),

    # ── 소방기계
    ("스프링클러 헤드 살수반경 기준",
     "소방기계", ["스프링클러", "살수반경", "헤드"]),

    # ── 전기
    ("CV 케이블과 HFCC 케이블 차이점",
     "전기", ["cv", "hfcc", "할로겐", "독성"]),
    ("케이블트레이 충전율 기준 KEC",
     "전기", ["충전율", "케이블트레이", "kec"]),
    ("EPS실 분전반 전면 클리어런스",
     "전기", ["eps", "분전반", "1,000mm"]),

    # ── 위생
    ("오배수 배관 구배 기준",
     "위생", ["오배수", "구배"]),

    # ── BIM 납품검수
    ("IDS BIM 납품 검수 오류코드 E001",
     "BIM_납품검수", ["e001", "ids", "ifcspace"]),
    ("IfcPropertySet Pset 명명 규칙",
     "BIM_납품검수", ["pset_", "ifcpropertyset", "buildingsmart"]),
    ("BCF 파일 BIM 협업 클래시 해소",
     "BIM_납품검수", ["bcf", "clash", "협업"]),

    # ── IFC / OpenBIM
    ("IFC 5 점진적 출시 전략 buildingSMART",
     "IFC_OpenBIM", ["ifc 5", "incremental", "buildingsmart"]),
    ("IFC4 IfcWall IfcBeam 엔티티 구조",
     "IFC_OpenBIM", ["ifcwall", "ifc4", "entity"]),

    # ── Scan-to-BIM
    ("Leica RTC360 스캐너 정확도 Scan-to-BIM",
     "OpenBIM_프로그램연동", ["leica", "rtc360", "포인트클라우드"]),
    ("Revit 포인트클라우드 rcp e57 연동 방법",
     "OpenBIM_프로그램연동", ["rcp", "e57", "revit"]),

    # ── BIM 납품검수 / 4D BIM
    ("Navisworks TimeLiner 4D 공정 시뮬레이션",
     "Navisworks_Addin", ["timeliner", "4d", "navisworks"]),

    # ── BIM 견적
    ("BIM 용역 표준시장단가 2026 견적 방법",
     "BIM_프로젝트_견적산정", ["표준시장단가", "bim", "단가"]),
    ("Togal AI 물량 산출 자동화 도구",
     "BIM_프로젝트_견적산정", ["togal", "물량산출", "ai"]),

    # ── 건축 (연면적 DB)
    ("인천공항 제2터미널 연면적이 얼마야?",
     "건축", ["384,000", "제2터미널", "2018"]),
    ("스타필드 청라 연면적",
     "건축", ["청라", "350,000", "스타필드"]),

    # ── BIM 인력파견
    ("BIM 운용전문가 자격증 취득 방법",
     "BIM_인력파견_기준", ["bim 운용전문가", "한국bim학회", "민간자격"]),

    # ── FM 자산관리
    ("Autodesk Tandem 디지털트윈 FM BIM",
     "FM_자산관리", ["tandem", "디지털트윈", "globant"]),

    # ── Revit 패밀리
    ("MEP Revit 패밀리 커넥터 설정 방법",
     "Revit_Family제작", ["커넥터", "connector", "패밀리"]),

    # ── 구조 BIM (IFC / 해석 연동)
    ("ETABS Revit 구조 BIM 연동 CSI XRevit 워크플로우",
     "구조", ["etabs", "xrevit", "단면"]),
    ("IFC IfcReinforcingBar 철근 BIM LOD 300 400",
     "구조", ["ifcreinforcingbar", "lod", "철근"]),

    # ── 공조덕트 (풍량 산출 / 방화댐퍼 / IFC)
    ("공조 덕트 풍량 산출 환기횟수 사무실 병원",
     "공조덕트", ["환기횟수", "사무실", "m³"]),
    ("방화댐퍼 퓨즈온도 설치기준 BIM 파라미터",
     "공조덕트", ["firedamper", "퓨즈", "72"]),

    # ── 통신 (MDF/IDF / 케이블 / IFC)
    ("MDF IDF 구내통신설비 차이와 배선반 설계기준",
     "통신", ["mdf", "idf", "배선반"]),
    ("Cat6A 광케이블 케이블트레이 강전 약전 이격 기준",
     "통신", ["cat6a", "이격", "300mm"]),

    # ── 소방전기 (NFTC 203 / 감지기 / 수신기)
    ("연기감지기 차동식 감지면적 부착높이 기준 NFTC 203",
     "소방전기", ["연기식", "감지면적", "nftc"]),
    ("P형 R형 수신기 BIM 차이 소방 설계",
     "소방전기", ["p형", "r형", "수신기"]),

    # ── 토목 (IFC4.3 인프라 / Civil 3D / 토공 물량)
    ("IFC4.3 IfcAlignment 도로 BIM Civil 3D 내보내기",
     "토목", ["ifcalignment", "civil", "내보내기"]),
    ("토공 양단면 평균법 절토 성토 물량 산출",
     "토목", ["양단면", "절토", "성토"]),

    # ── BIM 시방서 (EIR / 발주처 납품기준)
    ("EIR 발주자정보요구사항 BIM 과업지시서 작성 방법",
     "BIM_시방서", ["eir", "발주자", "과업지시서"]),
    ("COBie BIM 유지관리 납품 데이터 표준",
     "BIM_시방서", ["cobie", "유지관리", "fm"]),
]


# ──────────────────────────────────────────────
# 핵심 스코어링 로직 (server_total 의존성 없이)
# ──────────────────────────────────────────────

def _query_terms(query: str) -> list[str]:
    raw = re.findall(r"[A-Za-z0-9_#+.\-가-힣]{2,}", query.lower())
    stopwords = {"으로","에서","대한","관련","정리","알려줘","기준","방법","어떻게","어떤","있어","인지","뭐야","뭐임"}
    return [t for t in raw if t not in stopwords][:20]


def _score(text: str, terms: list[str]) -> int:
    lower = text.lower()
    return sum(min(lower.count(t), 6) for t in terms)


def _extract_excerpt(content: str, terms: list[str], max_chars: int = 2400) -> str:
    line_noise = ("- source:", "- tags:", "[tavily]", "[ddg]", "auto-quality", "needs-review",
                  "자동 수집", "auto-collect", "출처: http")
    sections = [s.strip() for s in re.split(r"(?=^##\s+)", content, flags=re.MULTILINE) if s.strip()]
    if not sections:
        return content[:max_chars]

    def clean(s: str) -> str:
        return "\n".join(l for l in s.splitlines() if not any(n in l.lower() for n in line_noise)).strip()

    scored = sorted(
        [(_score(s, terms), i, clean(s)) for i, s in enumerate(sections)],
        key=lambda x: (x[0], -x[1]), reverse=True
    )
    best = scored[0][2] if scored else sections[0]
    return best[:max_chars]


def run_qa(agent_filter: str | None = None, verbose: bool = False) -> dict:
    kb_dir = PROJECT_ROOT / "data" / "knowledge_base"
    docs_dir = PROJECT_ROOT / "docs"

    all_files = list(kb_dir.rglob("*.md")) + list(docs_dir.rglob("*.md"))
    excluded = {"지식업데이트", "지식큐레이터"}

    total = passed = 0
    failures: list[dict] = []

    for question, expected_stem, answer_keywords in QA_DATASET:
        if agent_filter and agent_filter.lower() not in expected_stem.lower():
            continue
        total += 1
        terms = _query_terms(question)

        # 검색: 파일 전체에서 스코어링
        matches = []
        for path in all_files:
            if path.stem in excluded:
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            score = _score(content, terms)
            # data/knowledge_base/ 파일 보너스
            if "knowledge_base" in str(path):
                score += 8
            # 파일명이 expected_stem이면 보너스 (agent 매칭)
            if path.stem == expected_stem:
                score += 20
            if score <= 0:
                continue
            matches.append((score, path, content))

        matches.sort(key=lambda x: x[0], reverse=True)
        top_match = matches[0] if matches else None

        # 판정 1: 정답 파일이 top 3 안에 있는지
        top3_stems = [m[1].stem for m in matches[:3]]
        file_hit = expected_stem in top3_stems

        # 판정 2: 정답 파일의 발췌문에 정답 키워드 ≥ 2개 포함
        answer_file = next((m for m in matches if m[1].stem == expected_stem), None)
        keyword_hit = False
        keyword_found: list[str] = []
        if answer_file:
            excerpt = _extract_excerpt(answer_file[2], terms)
            excerpt_lower = excerpt.lower()
            keyword_found = [k for k in answer_keywords if k.lower() in excerpt_lower]
            keyword_hit = len(keyword_found) >= 2

        ok = file_hit and keyword_hit
        if ok:
            passed += 1
        else:
            failures.append({
                "q": question,
                "expected": expected_stem,
                "top3": top3_stems,
                "file_hit": file_hit,
                "keyword_hit": keyword_hit,
                "keywords_found": keyword_found,
                "keywords_needed": answer_keywords,
            })

        if verbose:
            mark = "✅" if ok else "❌"
            print(f"{mark} [{top_match[0] if top_match else 0:3d}] {expected_stem:<30} | {question[:55]}")
            if not ok:
                print(f"     top3: {top3_stems}")
                print(f"     키워드 발견: {keyword_found} / 필요: {answer_keywords}")

    rate = int(passed / total * 100) if total else 0
    return {"total": total, "passed": passed, "rate": rate, "failures": failures}


def main() -> None:
    parser = argparse.ArgumentParser(description="LUA BIM LABS 지식 베이스 QA 검증")
    parser.add_argument("--agent", help="특정 agent만 테스트 (예: Revit_Addin)")
    parser.add_argument("--verbose", "-v", action="store_true", help="질문별 상세 출력")
    parser.add_argument("--fail-only", action="store_true", help="실패한 항목만 출력")
    args = parser.parse_args()

    print("=" * 65)
    print("LUA BIM LABS 지식 베이스 QA 검증")
    print("=" * 65)

    result = run_qa(agent_filter=args.agent, verbose=args.verbose or args.fail_only)

    if args.fail_only and result["failures"]:
        print("\n[실패 항목 상세]")
        for f in result["failures"]:
            print(f"\n  ❌ {f['q']}")
            print(f"     예상파일: {f['expected']}  /  top3: {f['top3']}")
            print(f"     키워드 발견: {f['keywords_found']}  /  필요: {f['keywords_needed']}")

    print(f"\n{'─'*65}")
    print(f"결과: {result['passed']}/{result['total']} 통과  ({result['rate']}%)")
    if result["rate"] >= 90:
        print("판정: ✅ PASS — 지식 활용 품질 양호")
    elif result["rate"] >= 70:
        print("판정: ⚠️  WARN — 일부 지식 갭 보강 필요")
    else:
        print("판정: ❌ FAIL — 지식 갭 다수, 즉시 보강 필요")
    print("=" * 65)

    sys.exit(0 if result["rate"] >= 80 else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""AI 조직원 지식연결·답변품질 감사.

전 본부 대표 현실 질의에 대해 로컬 지식만으로 즉답 가능한지(웹검색/추가 API
불필요) 측정한다. weak-rate 가 낮을수록 DeepSeek/웹검색 API 소모가 적다.

  python scripts/knowledge_connection_audit.py             # 콘솔 요약
  python scripts/knowledge_connection_audit.py --json out.json
  python scripts/knowledge_connection_audit.py --verbose   # weak 케이스 상세

CI/정기 점검에서 회귀(로컬 즉답률 하락)를 조기에 잡는 용도.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import backend.server_total as server  # noqa: E402

# 6본부 대표 현실 고객형 질의 (도메인 키워드를 충분히 포함한 자연 질의)
REALISTIC_QUERIES: list[str] = [
    # 엔지니어링(공종)
    "방화구획 관통부 내화충전 시공기준",
    "철근 정착길이 이음 기준",
    "우수관 구배 최소 기준",
    "오배수 통기 트랩 봉수 깊이",
    "냉각수 배관 보온 두께 기준",
    "급기덕트 정압 손실 계산",
    "스프링클러 헤드 살수반경과 간격",
    "화재감지기 경계구역 설정",
    "분전반 전면 작업공간 확보 기준",
    "광케이블 트레이 강전 이격",
    "navisworks 간섭검토 공차 설정",
    # 애드인 개발
    "Revit API 트랜잭션 처리",
    "Dynamo로 카테고리 일괄선택",
    "IFC4 속성셋 매핑",
    "Revit 패밀리 LOD350 모델링",
    "COBie 자산정보 추출",
    # 스토어 상용화
    "Autodesk Store 애드인 제출 심사 기준",
    "구독 결제 라이선스 검증 처리",
    "MSI 인스톨러 패키징 서명",
    "EULA 면책조항 작성 기준",
    "Revit 애드인 QA 회귀테스트 항목",
    "사용자 가이드 작성 표준",
    # 교육/HR/경영지원
    "BIM 교육 커리큘럼 온보딩",
    "이력서 분석 채용 평가 기준",
    "월별 경비 영수증 자동분류",
    # 마케팅 GTM
    "Autodesk Store 마케팅 전략",
    "해외진출 현지화 우선순위",
    "BIM Command Center 가격 정책",
    # 지식/인프라
    "Obsidian 지식그래프 자동동기화",
    "AI 프롬프트 토큰 절감 전략",
]


def audit(queries: list[str]) -> dict:
    rows = []
    for query in queries:
        matches = server.search_local_knowledge(query, limit=3)
        agent = server.infer_knowledge_agent_from_query(query)
        answer = server.build_knowledge_answer(query, matches)
        readiness = server.assess_team_telegram_answer_readiness(query, agent, matches, answer)
        top = matches[0] if matches else None
        rows.append({
            "query": query,
            "routed_agent": agent,
            "top_stem": top["path"].stem if top else "",
            "top_score": int(top["score"]) if top else 0,
            "should_search": bool(readiness["should_search"]),
            "reasons": readiness["reasons"],
        })
    total = len(rows)
    weak = [r for r in rows if r["should_search"]]
    return {
        "total": total,
        "local_ready": total - len(weak),
        "weak": len(weak),
        "local_ready_rate": round((total - len(weak)) / total, 3) if total else 0.0,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="결과 JSON 출력 경로")
    parser.add_argument("--verbose", action="store_true", help="weak 케이스 상세 출력")
    parser.add_argument("--min-rate", type=float, default=0.0,
                        help="로컬 즉답률 하한(미만이면 종료코드 1) — CI 게이트용")
    args = parser.parse_args()

    result = audit(REALISTIC_QUERIES)
    print(f"지식연결 감사: 로컬 즉답 {result['local_ready']}/{result['total']} "
          f"({result['local_ready_rate']*100:.0f}%) | weak {result['weak']}")
    if args.verbose and result["weak"]:
        print("\n약한 답변(웹검색/추가 API 트리거):")
        for r in result["rows"]:
            if r["should_search"]:
                print(f"  sc={r['top_score']:>3} top={r['top_stem']:18} "
                      f"routed={r['routed_agent']:14} reasons={r['reasons']}")
                print(f"      q={r['query']}")

    if args.json:
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"JSON 저장: {args.json}")

    if result["local_ready_rate"] < args.min_rate:
        print(f"FAIL: 로컬 즉답률 {result['local_ready_rate']*100:.0f}% < 기준 {args.min_rate*100:.0f}%")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

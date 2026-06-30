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
    # ── 광역 확장(과적합 방지): 감사셋 30개에만 최적화되지 않도록 다양한 어휘/공종 추가.
    #    좁은 셋은 93%였으나 광역 셋에서 68%→개선 작업으로 노출된 어휘들을 영구 편입.
    "커튼월 멀리언 간격",
    "계단 단높이 단너비 기준",
    "기둥 단면 크기 산정",
    "옹벽 안정 검토",
    "도로 종단 구배 설계",
    "배수 트랩 종류 봉수",
    "냉온수 공급 온도차",
    "펌프 양정 계산",
    "디퓨저 배치 간격",
    "제연 풍량 계산",
    "옥내소화전 방수압",
    "자동화재탐지 감지기 종류",
    "수변전 용량 계산",
    "콘센트 회로 분기",
    "구내방송 스피커 배치",
    "CCTV 카메라 화각",
    "Revit 워크셋 분할",
    "패밀리 파라미터 공유",
    "IFC 내보내기 매핑셋",
    "클래시 그룹핑 규칙",
    "LOD 350 모델 상세",
    # ── 2026-06 후반 답변읽기로 연결한 신규 카테고리(회귀 추적용 영구 편입).
    #    시설유형 KB(미등록 orphan→inference_only 등록), 생명안전 법규(건축), 결제 FAQ,
    #    경영(수익원/투자유치), 확장(프롬프트/투입공수), HVAC 장비, 토목 종단/가설.
    "데이터센터 BIM 설계",
    "병원 의료시설 BIM",
    "물류센터 창고 BIM",
    "호텔 숙박시설 BIM",
    "피난 보행거리 기준",
    "비상구 유효폭",
    "장애인 화장실 회전반경",
    "무료 체험 기간",
    "구독 결제 방법",
    "회사 주요 수익원",
    "투자 유치 전략",
    "프롬프트 엔지니어링 기법",
    "BIM 투입 공수 산정",
    "냉동기 어셈블리 밸브 순서",
    "흙막이 가시설 공법",
    # ── 2026-06-26 대화형 QA 광역 스윕서 해소한 갭(콘텐츠 저작·라우팅 보강) 영구 편입.
    #    처짐/내진(KDS 콘텐츠 저작), 뷰템플릿/기초/전선굵기/납품검수/뷰분류/맨홀(라우팅 갭),
    #    영수증·세금계산서·인보이스 발급(고객 결제증빙 — 내부 경비정산 누출 차단).
    "구조 처짐 한계 기준",
    "보 처짐 허용값",
    "내진 설계 기준",
    "BIM 뷰템플릿 일괄 적용",
    "뷰 필터 색상 규칙",
    "기초 종류",
    "전선 굵기 선정",
    "납품 모델 검수",
    "맨홀 간격",
    "영수증 발급 되나요",
    "세금계산서 발급",
    "인보이스 발급",
    "BIM 객체 분류체계",  # 2026-06-26 저작(OmniClass/UniClass/IFC class) — 백로그서 승격
]

# 알려진 콘텐츠 갭(2026-06-26 광역 스윕). 타깃 에이전트에 콘텐츠가 없거나(0건) 매우
# 얇아(1~2건) 로컬 즉답이 약한 항목 — 도메인 전문가 검증을 거친 콘텐츠 저작 대기.
# 감사 게이트(REALISTIC_QUERIES, 100% 요구)와 분리해 추적만 한다(저작 후 위 목록으로 승격).
# 변동·전문 엔지니어링 수치를 검증 없이 자동 저작하면 confident-오답을 재생산하므로 보류.
CONTENT_GAP_BACKLOG: list[str] = [
    "승강기 기계실 기준",      # 설비장비/건축 — 콘텐츠 0
    "일위대가 산출",          # 견적 — 콘텐츠 0
    "모델 경량화 방법",        # 소프트웨어 워크플로(수치 위험 0) — 저작 우선 후보(홈 에이전트 미정)
    "상수도 인입 기준",        # 위생/토목 — 콘텐츠 얇음(1)
    "가스 배관 이격거리",      # 위생/설비 — 콘텐츠 얇음(2)
    "방화문 설치 기준",        # 건축 — 콘텐츠 얇음(1)
    "말뚝 지지력 산정",        # 구조/토목 — 콘텐츠 얇음(1)
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
        "min_top_score": min((r["top_score"] for r in rows), default=0),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="결과 JSON 출력 경로")
    parser.add_argument("--verbose", action="store_true", help="weak 케이스 상세 출력")
    parser.add_argument("--min-rate", type=float, default=0.0,
                        help="로컬 즉답률 하한(미만이면 종료코드 1) — CI 게이트용")
    parser.add_argument("--min-top-score", type=int, default=0,
                        help="각 감사 질의의 top score 하한(미만이면 종료코드 1)")
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
    if result["min_top_score"] < args.min_top_score:
        print(f"FAIL: 최저 top score {result['min_top_score']} < 기준 {args.min_top_score}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

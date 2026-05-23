#!/usr/bin/env python3
"""Validate local collaboration routing without paid API calls."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import backend.server_total as server  # noqa: E402


CASES = [
    ("일반 CS", "설치가 안돼요 어떻게 해야 하나요?", "support_general", "고객지원 CS", False),
    ("일반 CS", "고객 문의로 답변해줘: Revit 2025에서 실행 버튼이 안 보여요", "support_general", "고객지원 CS", False),
    ("라이선스", "라이선스 인증 실패라고 나오고 구독 상태 확인이 안돼", "license_billing", "라이선스결제", False),
    ("라이선스", "고객지원 문의 환불 라이선스 문제 응답 흐름을 확인해줘", "license_billing", "고객지원 CS", False),
    ("가격", "구독 가격과 MRR 손익분기 검토해줘", "pricing_revenue", "CFO", False),
    ("스토어", "Autodesk Store 출시 전에 심사 리스크와 제출 체크리스트 검토해줘", "store_release", "스토어심사", False),
    ("패키징", "설치파일 MSI 패키징과 .addin manifest 배포 흐름 점검해줘", "packaging_install", "제품패키징", False),
    ("QA", "Revit 2024 2025 빌드 smoke test 검증 계획 세워줘", "build_qa", "빌드검증", False),
    ("요구사항", "MVP 범위와 요구사항 명세를 정리해줘", "requirements_scope", "요구사항분석", False),
    ("Revit", "Revit Add-in 뷰 템플릿 복사 기능 개발 검토해줘", "revit_development", "Revit_Addin", False),
    ("엑셀자동화", "Navisworks 간섭 결과를 Excel로 내보내는 기능 설계해줘", "excel_qwen_automation", "엑셀자동화", False),
    ("경비정산", "텔레그램으로 들어온 영수증을 자동 정리하고 월별 정산표 만들어줘", "expense_receipt_intake", "경비정산_AI", False),
    ("경비정산", "증빙 세금계산서 거래명세서 누락 여부를 확인해줘", "expense_receipt_intake", "경비정산_AI", False),
    ("간섭조율", "MEP통합 간섭 조율 보고서 필드를 정리해줘", "coordination_discipline", "조율차장", False),
    ("보안", "개인정보와 API key가 로그에 남지 않게 보안 검토해줘", "privacy_security", "라이선스_보안관", False),
    ("보안", "telemetry machine id 보안 검토해줘", "privacy_security", "라이선스_보안관", False),
    ("문서", "설치 가이드와 릴리스 노트 작성 기준 정리해줘", "docs_release", "배포문서", False),
    ("교육", "신규 직원 온보딩 교육자료와 연차별 커리큘럼을 구성해줘", "employee_onboarding_training", "교육컨설팅", False),
    ("교육", "BIM 모델러 1년차 3년차 5년차 직무교육 로드맵과 평가 기준 점검", "employee_onboarding_training", "교육컨설팅", False),
    ("교육", "수습 직원 멘토링과 역량 매트릭스 교육 프로세스 테스트해줘", "employee_onboarding_training", "교육컨설팅", False),
    ("이력서분석", "PDF 이력서를 분석해서 경력 대시보드와 인재 평가 보고서를 만들어줘", "resume_analysis_dashboard", "HR_인재분석관", False),
    ("이력서분석", "지원자 서류심사 후보자 경력 분석 대시보드 내재화", "resume_analysis_dashboard", "HR_인재분석관", False),
    ("교육콘텐츠", "NotebookLM으로 교육자료 요약하고 슬라이드와 퀴즈를 만들어줘", "employee_onboarding_training", "러닝콘텐츠디자이너", False),
    ("교육콘텐츠", "노트북LM 연계 강의안과 PPT 제작 흐름을 점검해줘", "employee_onboarding_training", "러닝콘텐츠디자이너", False),
    ("지식업데이트", "지식 업데이트 기준 추가하고 다음 라우팅에 반영해줘", "knowledge_update", "지식업데이트", False),
    ("지식큐레이터", "자동 수집된 지식을 큐레이션하고 승격 보류 보안검토로 분류해줘", "knowledge_update", "지식큐레이터", False),
    ("아이디어", "최고지배자에게 매일 3가지 수익화 아이디어와 토큰수 투입비용을 보고해줘", "daily_idea_report", "아이디어발굴", False),
    ("상품화", "기능 내재화 종료 후 아이디어발굴 조직이 상품화 우선순위와 개발 순서를 정해줘", "idea_to_product_development_queue", "아이디어발굴", False),
    ("로컬개발", "개발 업무지시: FastAPI 상태 API 리팩토링은 qwen coder로 1차 개발해줘", "local_qwen_development", "프로그램개발", False),
    ("로컬개발", "업무지시 프론트엔드 콘솔 로그 표시 테스트 코드를 로컬 1차 개발로 작성해줘", "local_qwen_development", "프로그램개발", False),
    ("엑셀자동화", "엑셀 보고서 자동화는 qwen coder를 주 업무로 배정해서 csv export 검증까지 해줘", "excel_qwen_automation", "엑셀자동화", False),
    ("엑셀자동화", "Navisworks 결과 샘플 CSV를 XLSX 필터 가능한 표로 자동화해줘", "excel_qwen_automation", "엑셀자동화", False),
    ("CS", "환불하고 싶어요", "license_billing", "라이선스결제", False),
    ("CS", "인증 오류가 나요", "license_billing", "라이선스결제", False),
    ("CS", "대시보드가 하얗게 떠요", "support_general", "고객지원 CS", False),
    ("스토어/보안", "앱스토어 제출용 개인정보 처리방침 검토", "privacy_security", "라이선스_보안관", False),
    ("견적", "견적 공수와 일정 버퍼 검토해줘", "requirements_scope", "요구사항분석", False),
    ("조율", "전기 트레이와 덕트 간섭 우선순위 정리", "coordination_discipline", "조율차장", False),
    ("가격", "월 19달러 가격 괜찮아?", "pricing_revenue", "CFO", False),
    ("지식", "프롬프트 기준을 지식에 반영해줘", "knowledge_update", "지식업데이트", False),
    ("애매함", "문 위치 검토해줘", None, None, True),
    ("애매함", "보 검토", None, None, True),
    ("애매함", "모델 문제", None, None, True),
]


def main() -> int:
    failures = []
    for group, text, expected_workflow, expected_target, expected_confirm in CASES:
        preview = server.preview_collaboration_route(text)
        ok = (
            preview.get("workflow_id") == expected_workflow
            and preview.get("target_agent") == expected_target
            and preview.get("requires_confirmation") == expected_confirm
            and preview.get("use_paid_ai") in (False, None)
        )
        status = "PASS" if ok else "FAIL"
        print(
            f"{status} [{group}] {text} -> "
            f"workflow={preview.get('workflow_id')} target={preview.get('target_agent')} "
            f"confirm={preview.get('requires_confirmation')} paid={preview.get('use_paid_ai')}"
        )
        if not ok:
            failures.append((text, preview, expected_workflow, expected_target, expected_confirm))

    print(f"TOTAL={len(CASES)} FAILURES={len(failures)}")
    if failures:
        for failure in failures:
            print("FAIL_DETAIL", failure)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

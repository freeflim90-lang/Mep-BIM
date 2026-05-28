from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Union


BASE_COLLABORATION_WORKFLOWS = [
    {
        "id": "support_general",
        "name": "일반 고객 문의 대응",
        "primary": "고객지원 CS",
        "participants": ["고객지원 CS", "라이선스결제", "배포문서"],
        "keywords": ["고객지원", "고객 문의", "cs", "support", "문의", "사용법", "호환성", "환불"],
        "steps": [
            "문의 유형 분류 및 FAQ 매칭",
            "라이선스/결제/설치 항목만 필요한 경우 담당 지식 연결",
            "고객에게 보낼 1차 답변과 추가 확인 정보 정리",
        ],
        "local_only": True,
    },
    {
        "id": "license_billing",
        "name": "라이선스/결제/구독 검토",
        "primary": "라이선스결제",
        "participants": ["라이선스결제", "고객지원 CS", "CFO", "라이선스_보안관"],
        "keywords": ["라이선스", "라이센스", "결제", "구독", "entitlement", "paypal", "bluesnap", "가격", "환불", "인증"],
        "steps": [
            "구독/체험/만료/오프라인 캐시 상태 분류",
            "고객 응답 문구와 결제 정책 리스크 확인",
            "수익/수수료/세금 또는 보안 영향이 있으면 CFO/보안관 검토",
        ],
        "local_only": True,
    },
    {
        "id": "store_release",
        "name": "Autodesk Store 출시/심사 준비",
        "primary": "스토어심사",
        "participants": ["스토어심사", "제품패키징", "라이선스결제", "배포문서", "고객지원 CS", "라이선스_보안관"],
        "keywords": ["autodesk store", "app store", "스토어", "심사", "출시", "판매", "submit", "submission", "publisher"],
        "steps": [
            "심사 리스크와 제품 설명/스크린샷/지원 연락처 확인",
            "패키징, 라이선스, 개인정보, 지원 문서 준비 상태 점검",
            "제출 전 차단 이슈와 보완 작업을 릴리스 게이트로 정리",
        ],
        "local_only": False,
    },
    {
        "id": "packaging_install",
        "name": "설치/배포 패키징 검토",
        "primary": "제품패키징",
        "participants": ["제품패키징", "배포문서", "빌드검증", "고객지원 CS"],
        "keywords": ["설치", "배포", "installer", "msi", "addin manifest", ".addin", "패키징", "설치파일", "bundle"],
        "steps": [
            "설치/제거/업데이트 경로와 Revit Add-in manifest 확인",
            "빌드 검증과 smoke test 항목 연결",
            "고객용 설치 가이드와 실패 시 CS 응답 흐름 정리",
        ],
        "local_only": True,
    },
    {
        "id": "build_qa",
        "name": "빌드/QA/회귀 검증",
        "primary": "빌드검증",
        "participants": ["빌드검증", "QA_테스터", "프로그램개발", "배포문서"],
        "keywords": ["테스트", "qa", "검증", "빌드", "smoke", "회귀", "버그", "crash", "크래시"],
        "steps": [
            "지원 Revit/Navisworks 버전별 smoke test 범위 설정",
            "P1/P2 차단 이슈와 회귀 테스트 우선순위 분리",
            "릴리스 노트와 알려진 이슈 문서화",
        ],
        "local_only": True,
    },
    {
        "id": "requirements_scope",
        "name": "요구사항/범위 정의",
        "primary": "요구사항분석",
        "participants": ["요구사항분석", "프로젝트분석", "전략기획", "프로그램개발", "견적심사원"],
        "keywords": ["요구사항", "기획", "명세", "spec", "범위", "mvp", "기능 정의", "우선순위", "견적", "공수", "일정 버퍼"],
        "steps": [
            "사용자 문제와 성공 기준을 user story로 정리",
            "MVP/제외 범위/향후 Pro 기능 분리",
            "공수, 일정 버퍼, 개발 리스크를 견적 기준으로 연결",
        ],
        "local_only": True,
    },
    {
        "id": "local_qwen_development",
        "name": "로컬 Qwen Coder 8B 1차 개발",
        "primary": "프로그램개발",
        "participants": ["프로그램개발", "Qwen_Coder_8B", "QA_테스터", "빌드검증", "배포문서"],
        "keywords": [
            "qwen", "qwen coder", "로컬 코더", "로컬 1차", "1차 개발", "업무지시", "개발 업무",
            "일반 코드", "fastapi", "frontend", "백엔드", "프론트엔드", "리팩토링", "테스트 코드",
        ],
        "steps": [
            "조율차장이 Revit/Navisworks API 의존 여부를 먼저 판정",
            "Autodesk API 의존이 없으면 Qwen_Coder_8B가 로컬에서 1차 구현 초안을 작성",
            "프로그램개발이 diff와 영향 범위를 검토하고 위험한 변경을 제거",
            "QA_테스터와 빌드검증이 정적 검증, 단위 테스트, smoke test를 수행",
            "Revit/Navisworks API가 포함되면 최고지배자 실기 테스트 검증 대기로 전환",
        ],
        "local_only": True,
    },
    {
        "id": "excel_qwen_automation",
        "name": "Qwen 기반 엑셀 자동화 주 업무",
        "primary": "엑셀자동화",
        "participants": ["엑셀자동화", "Qwen_Coder_8B", "프로그램개발", "QA_테스터", "빌드검증", "배포문서"],
        "keywords": [
            "엑셀", "excel", "xlsx", "csv", "openxml", "보고서", "표", "필터", "피벗",
            "워크북", "시트", "자동화", "내보내기", "export", "리포트 자동화",
        ],
        "steps": [
            "요청 목적, 입력 데이터, 출력 사용자를 plan으로 먼저 확정",
            "엑셀자동화가 필드명, 단위, 시트 구조, 필터 기준을 설계",
            "Qwen_Coder_8B가 로컬에서 Excel/CSV/OpenXML 자동화 초안을 주 업무로 작성",
            "Qwen_Coder_8B가 샘플 데이터 기반 검증 코드와 엣지 케이스를 먼저 작성",
            "프로그램개발과 QA_테스터가 파일 손상, 인코딩, 수식, 대용량 성능을 검증",
            "Revit/Navisworks 원본 API 접근이 필요하면 API 활용 여부를 내부 검토 후 최고지배자 검증 게이트로 넘김",
        ],
        "local_only": True,
    },
    {
        "id": "expense_receipt_intake",
        "name": "Telegram 영수증/증빙 자동 정리",
        "primary": "경비정산_AI",
        "participants": ["경비정산_AI", "경영지원", "엑셀자동화", "Qwen_Coder_8B", "라이선스_보안관", "CFO"],
        "keywords": [
            "영수증", "증빙", "경비", "비용 정산", "비용정산", "정산", "세금계산서",
            "거래명세서", "카드전표", "receipt", "expense", "텔레그램 영수증", "telegram receipt",
        ],
        "steps": [
            "Telegram으로 접수된 영수증/증빙의 날짜, 금액, 사용처, 결제자, 프로젝트/비용 구분을 추출",
            "경비정산_AI가 중복, 누락, 불명확 항목을 표시하고 질문자에게 추가 확인 항목을 정리",
            "엑셀자동화와 Qwen_Coder_8B가 로컬에서 월별 정산표/CSV/XLSX 구조 초안을 작성",
            "라이선스_보안관이 개인정보, 카드번호, 사업자번호, 고객/프로젝트명이 외부 API로 전송되지 않도록 점검",
            "경영지원이 확정 자료를 회계/세무 전달용 증빙 목록으로 보관하고 CFO는 예산/비용 추이를 검토",
        ],
        "local_only": True,
    },
    {
        "id": "resume_analysis_dashboard",
        "name": "이력서 분석 대시보드/인재 평가",
        "primary": "HR_인재분석관",
        "participants": ["HR_인재분석관", "경영지원", "교육컨설팅", "BIM_템플릿기획관", "라이선스_보안관", "CEO"],
        "keywords": [
            "이력서", "resume", "cv", "지원자", "후보자", "채용", "서류 검토", "서류심사",
            "인재 평가", "인재평가", "경력 분석", "경력 대시보드", "평가 보고서", "pdf 이력서",
        ],
        "steps": [
            "이력서 PDF 또는 구조화 데이터를 로컬 전용으로 접수하고 개인정보/민감정보 포함 여부를 먼저 점검",
            "HR_인재분석관이 경력, 프로젝트, 역할, 기술, 학력, 해외 경험을 표준 JSON 스키마로 추출",
            "대시보드는 추출 결과를 경력 통계, 프로젝트 분포, 기술 역량, 타임라인, 주요 고객/산업 경험으로 시각화",
            "1페이지 인재 평가 보고서는 S/A/B 등급, 핵심 역량 점수, 주요 실적, 강점/보완 영역, 추천 배치안으로 요약",
            "경영지원은 채용 절차와 보관 기준을 확인하고, 교육컨설팅은 입사 후 30/60/90일 육성 계획으로 연결",
            "최종 채용 판단은 대표/담당 리드가 수행하며 AI 점수는 참고 자료로만 사용",
        ],
        "local_only": True,
    },
    {
        "id": "revit_development",
        "name": "Revit Add-in 개발",
        "primary": "Revit_Addin",
        "participants": ["Revit_Addin", "프로그램개발", "Qwen_Coder_8B", "QA_테스터", "빌드검증", "배포문서"],
        "keywords": ["revit", "레빗", "revit api", "iexternalcommand", "패밀리", "뷰 템플릿", "스케줄"],
        "steps": [
            "목적, 사용자 문제, 모델 변경 여부, 성공 기준을 plan으로 먼저 확정",
            "Qwen_Coder_8B는 Add-in 초안 가이드라인과 비 API 의존 순수 로직/테스트 초안만 작성",
            "Revit API 가능성과 트랜잭션 경계 확인",
            "명령 구조, 설정 저장, 예외 처리, 로그 기준 설계",
            "Qwen_Coder_8B가 정적 검증과 테스트 초안을 수행한 뒤 API 필요성을 내부 검토",
            "실제 Revit 실행/모델 변경 검증은 최고지배자 테스트 후 확정",
        ],
        "local_only": False,
    },
    {
        "id": "navisworks_development",
        "name": "Navisworks Add-in 개발",
        "primary": "Navisworks_Addin",
        "participants": ["Navisworks_Addin", "프로그램개발", "엑셀자동화", "Qwen_Coder_8B", "QA_테스터", "배포문서"],
        "keywords": ["navisworks", "navis", "나비스웍스", "나비스", "clash", "간섭", "clash detective"],
        "steps": [
            "목적, 입력 모델, 출력 보고서, 성공 기준을 plan으로 먼저 확정",
            "Qwen_Coder_8B는 Add-in 초안 가이드라인과 Excel/CSV 출력 로직 초안까지만 작성",
            "Navisworks API/ClashResult 접근 범위 확인",
            "간섭 결과 필드와 Excel/CSV 내보내기 구조 설계",
            "Qwen_Coder_8B가 샘플 데이터 기반 검증을 수행한 뒤 API 필요성을 내부 검토",
            "실제 Navisworks 실행/ClashResult 검증은 최고지배자 테스트 후 확정",
        ],
        "local_only": False,
    },
    {
        "id": "coordination_discipline",
        "name": "BIM 공정 조율/간섭 검토",
        "primary": "조율차장",
        "participants": ["조율차장", "건축", "구조", "공조배관", "공조덕트", "소방기계", "전기", "엑셀자동화"],
        "keywords": ["간섭", "clash", "coordination", "조율", "mep통합", "전체공정", "트레이", "덕트"],
        "steps": [
            "공정별 영향 범위와 우선순위 분류",
            "건축/구조/MEP 검토 의견 병합",
            "보고서 필드와 담당자/상태/우선순위 출력 구조 확정",
        ],
        "local_only": True,
    },
    {
        "id": "privacy_security",
        "name": "개인정보/보안/외부통신 검토",
        "primary": "라이선스_보안관",
        "participants": ["라이선스_보안관", "법무조항검토", "고객지원 CS", "배포문서", "스토어심사"],
        "keywords": ["개인정보", "privacy", "보안", "토큰", "api key", "외부 통신", "로그", "데이터 전송", "모델 데이터", "처리방침"],
        "steps": [
            "수집/저장/외부 전송 데이터 항목 식별",
            "로그와 정책 문서의 민감정보 노출 여부 검토",
            "스토어 설명, 개인정보 처리방침, 고객 고지 문구 반영",
        ],
        "local_only": True,
    },
    {
        "id": "pricing_revenue",
        "name": "가격/수익/사업성 검토",
        "primary": "CFO",
        "participants": ["CFO", "CEO", "글로벌_매출관리원", "전략기획", "브랜드마케팅"],
        "keywords": ["가격", "수익", "mrr", "매출", "손익분기", "구독 가격", "사업성", "플랜", "enterprise", "달러"],
        "steps": [
            "가격/플랜/수수료/세금 영향 정리",
            "MRR, 유료 전환, 지원 비용 기준으로 사업성 검토",
            "Store 포지셔닝과 마케팅 메시지로 연결",
        ],
        "local_only": False,
    },
    {
        "id": "docs_release",
        "name": "문서/릴리스 노트/고객 가이드",
        "primary": "배포문서",
        "participants": ["배포문서", "테크니컬_라이터", "브랜드마케팅", "고객지원 CS"],
        "keywords": ["문서", "가이드", "릴리스 노트", "사용자 가이드", "설명", "도움말", "changelog"],
        "steps": [
            "설치/첫 실행/제거/제한사항 문서 항목 정리",
            "스토어 설명과 실제 기능 일치 여부 확인",
            "CS FAQ와 릴리스 노트를 함께 업데이트",
        ],
        "local_only": True,
    },
    {
        "id": "knowledge_update",
        "name": "지식 베이스 업데이트",
        "primary": "지식업데이트",
        "participants": ["지식업데이트", "지식큐레이터", "프롬프트엔지니어", "조율차장"],
        "keywords": ["지식 업데이트", "knowledge", "kb", "학습", "문서 반영", "기준 추가", "지식", "반영", "프롬프트 기준", "큐레이션", "분류", "승격", "보류"],
        "steps": [
            "출처/태그/시간 기준으로 지식 항목 정리",
            "지식큐레이터가 목적성, 승격 후보, 보안검토 여부를 분류",
            "기존 지식과 충돌 여부 확인",
            "다음 라우팅에 반영될 키워드와 담당 에이전트 점검",
        ],
        "local_only": True,
    },
    {
        "id": "employee_onboarding_training",
        "name": "신규 직원 온보딩/연차별 교육 설계",
        "primary": "교육컨설팅",
        "participants": ["교육컨설팅", "러닝콘텐츠디자이너", "경영지원", "BIM_템플릿기획관", "테크니컬_라이터", "QA_테스터", "견적심사원", "고객지원 CS", "조율차장"],
        "keywords": [
            "교육", "온보딩", "신규 직원", "신입", "연차별", "커리큘럼", "l&d", "learning",
            "멘토링", "직무교육", "교육자료", "교육 자료", "수습", "역량 매트릭스",
            "노트북lm", "notebooklm", "슬라이드", "ppt", "강의안", "퀴즈", "교육 콘텐츠", "교육콘텐츠", "학습자료", "강의자료",
        ],
        "steps": [
            "경영지원이 입사/수습/평가 운영 기준과 필수 행정 교육을 확인",
            "교육컨설팅이 연차별 직무 역량, 교육 모듈, 실습 과제, 수료 기준을 설계",
            "BIM_템플릿기획관과 실무 리드가 BIM 모델링/CDE/품질/납품 표준을 교육 항목으로 연결",
            "러닝콘텐츠디자이너가 NotebookLM 기반 요약, 슬라이드 목차, 강의안, 퀴즈, 실습 안내서를 제작",
            "테크니컬_라이터가 교육 자료 문체와 배포 형식을 정리",
            "QA_테스터가 교육 이해도 평가, 실습 검증, 협업 프로세스 테스트 케이스를 점검",
            "외부 고객 교육이나 SLA가 포함되면 견적심사원과 고객지원 CS가 범위/지원 조건을 검토",
        ],
        "local_only": True,
    },
    {
        "id": "daily_idea_report",
        "name": "최고지배자 일일 3대 아이디어 검토",
        "primary": "아이디어발굴",
        "participants": ["아이디어발굴", "전략기획", "견적심사원", "CFO", "CEO", "브랜드마케팅"],
        "keywords": ["아이디어", "매일", "일일 보고", "3가지", "수익화", "토큰수", "투입비용", "투입 시간"],
        "steps": [
            "아이디어발굴이 BIM 반복 고통과 Store 판매 가능성이 있는 후보를 수집",
            "전략기획이 LUA BIM LABS 목적성과 MVP/Pro 범위를 분리",
            "견적심사원이 구현 토큰수, 개발 시간, 운영 비용을 로컬 산식으로 추정",
            "CFO가 가격, MRR, 지원 비용, 손익분기 가능성을 검토",
            "CEO가 실제 구현 후보 3개만 최고지배자 보고 대상으로 승인",
        ],
        "local_only": True,
    },
    {
        "id": "idea_to_product_development_queue",
        "name": "아이디어 발굴-상품화-개발 큐 전환",
        "primary": "아이디어발굴",
        "participants": [
            "아이디어발굴", "전략기획", "견적심사원", "CFO", "CEO", "브랜드마케팅",
            "요구사항분석", "프로그램개발", "Qwen_Coder_8B", "QA_테스터", "빌드검증", "제품패키징",
        ],
        "keywords": [
            "상품화 우선순위", "개발 순서", "개발 큐", "다음 업무", "다음 상품",
            "아이디어발굴 조직", "자체적으로 아이디어", "기능 내재화 종료", "qwen 큐",
            "아이디어 발굴", "상품화 후보", "개발진행", "조직간 협업",
        ],
        "steps": [
            "현재 Qwen 개발 큐 완료 여부를 확인하고 미완료 시 active queue를 유지",
            "아이디어발굴이 내부 지식과 반복 현장 고통을 기준으로 후보를 수집",
            "전략기획과 브랜드마케팅이 Autodesk Store 포지션과 MVP/Pro 범위를 분리",
            "견적심사원과 CFO가 구현 시간, 비용, 가격, 회수 기간을 산정",
            "CEO가 1순위 후보를 승인하면 요구사항분석이 Qwen task로 분해",
            "Qwen_Coder_8B가 초안을 작성하고 QA_테스터, 빌드검증, 제품패키징으로 handoff",
            "오류와 수정 지식은 Obsidian 오답노트와 제품 지식 그래프에 축적",
        ],
        "local_only": False,
    },
]

SUPPORT_PRICING_KEYWORDS = ["가격", "mrr", "매출", "손익분기", "사업성", "구독 가격"]
SUPPORT_LICENSE_KEYWORDS = ["라이선스", "라이센스", "결제", "구독", "entitlement", "환불", "인증"]
EXPLICIT_SUPPORT_CHANNEL_KEYWORDS = ["고객지원", "고객 지원", "고객 문의", "cs", "문의 답변", "일반 문의"]
EDUCATION_TRAINING_KEYWORDS = [
    "교육", "온보딩", "신규 직원", "신입", "연차별", "커리큘럼", "l&d", "learning",
    "멘토링", "직무교육", "교육자료", "교육 자료", "수습", "역량 매트릭스",
    "노트북lm", "notebooklm", "슬라이드", "ppt", "강의안", "퀴즈", "교육 콘텐츠", "교육콘텐츠", "학습자료", "강의자료",
]

ROLE_BOUNDARIES = {
    "CEO": {
        "owns": ["제품 방향", "출시 승인", "사업 리스크"],
        "handoff": {"일정/운영 병목": "COO", "가격/수익성": "CFO", "실무 조율": "조율차장"},
    },
    "COO": {
        "owns": ["운영 KPI", "릴리스 게이트", "지원 준비 상태"],
        "handoff": {"제품 전략": "CEO", "가격/세금": "CFO", "실무 일정 조율": "조율차장"},
    },
    "CFO": {
        "owns": ["가격", "수익", "수수료", "세금", "손익분기"],
        "handoff": {"제품 가치 판단": "CEO", "결제 UX/Entitlement": "라이선스결제", "고객 응답": "고객지원 CS"},
    },
    "조율차장": {
        "owns": ["의도 확인", "협업 프로세스 선택", "팀 간 경계 조율", "최종 병합"],
        "handoff": {"운영 KPI": "COO", "제품 승인": "CEO", "지식 반영": "지식업데이트"},
    },
    "고객지원 CS": {
        "owns": ["1차 고객 응답", "FAQ", "지원 이메일", "문의 분류", "환경 정보 요청"],
        "handoff": {"라이선스/결제": "라이선스결제", "재현/로그 분석": "CS_기술지원관", "개인정보/보안": "라이선스_보안관"},
    },
    "CS_기술지원관": {
        "owns": ["고객 환경 진단", "로그 수집 기준", "재현 절차 정리"],
        "handoff": {"코드 수정": "프로그램개발", "빌드 검증": "빌드검증", "고객 안내": "고객지원 CS"},
    },
    "라이선스결제": {
        "owns": ["구독 상태", "결제 흐름", "Entitlement", "갱신/만료 UX"],
        "handoff": {"가격 정책": "CFO", "비밀값/개인정보": "라이선스_보안관", "고객 답변": "고객지원 CS"},
    },
    "라이선스_보안관": {
        "owns": ["비밀값", "개인정보", "로그 민감정보", "외부 통신", "모델 데이터 전송"],
        "handoff": {"법적 문구": "법무조항검토", "스토어 고지": "스토어심사", "사용자 문서": "배포문서"},
    },
    "법무조항검토": {
        "owns": ["EULA", "개인정보 처리방침 문구", "권리/면책 조항"],
        "handoff": {"보안 구현": "라이선스_보안관", "스토어 제출": "스토어심사"},
    },
    "스토어심사": {
        "owns": ["Autodesk Store 제출물", "심사 리스크", "제품 페이지 필수 항목"],
        "handoff": {"설치 패키지": "제품패키징", "개인정보/외부통신": "라이선스_보안관", "마케팅 문구": "브랜드마케팅"},
    },
    "제품패키징": {
        "owns": ["설치/제거/업데이트", "MSI", ".addin manifest", "배포 패키지"],
        "handoff": {"설치 문서": "배포문서", "빌드 검증": "빌드검증", "고객 실패 문의": "고객지원 CS"},
    },
    "배포문서": {
        "owns": ["설치 가이드", "릴리스 노트", "제한사항", "지원 연락처"],
        "handoff": {"문장 품질": "테크니컬_라이터", "스토어 설명": "브랜드마케팅", "지원 FAQ": "고객지원 CS"},
    },
    "빌드검증": {
        "owns": ["빌드 산출물", "버전별 smoke test", "설치/제거 검증"],
        "handoff": {"회귀/시나리오 테스트": "QA_테스터", "코드 수정": "프로그램개발", "문서화": "배포문서"},
    },
    "QA_테스터": {
        "owns": ["테스트 시나리오", "회귀 검증", "P1/P2/P3 분류"],
        "handoff": {"빌드 산출물": "빌드검증", "코드 수정": "프로그램개발", "릴리스 노트": "배포문서"},
    },
    "요구사항분석": {
        "owns": ["사용자 문제", "범위", "제외 범위", "성공 기준"],
        "handoff": {"사업 우선순위": "전략기획", "기술 가능성": "프로그램개발", "견적": "견적심사원"},
    },
    "프로그램개발": {
        "owns": ["구현 구조", "코드 수정", "예외 처리", "내부 아키텍처"],
        "handoff": {"Revit API": "Revit_Addin", "Navisworks API": "Navisworks_Addin", "QA": "QA_테스터"},
    },
    "Qwen_Coder_8B": {
        "owns": ["엑셀 자동화 구현 초안", "로컬 1차 코드 초안", "테스트 코드 초안", "Add-in 가이드라인 초안"],
        "handoff": {"코드 최종 판단": "프로그램개발", "Autodesk API 검증": "최고지배자", "품질 검증": "QA_테스터"},
    },
    "Revit_Addin": {
        "owns": ["Revit API", "IExternalCommand", "Transaction", "Revit 명령 UX"],
        "handoff": {"공통 코드": "프로그램개발", "빌드": "빌드검증", "문서": "배포문서"},
    },
    "Navisworks_Addin": {
        "owns": ["Navisworks API", "ClashResult", "간섭 보고서 추출"],
        "handoff": {"Excel 출력": "엑셀자동화", "공통 코드": "프로그램개발", "QA": "QA_테스터"},
    },
    "엑셀자동화": {
        "owns": ["보고서 필드", "CSV/Excel 출력", "필터 가능한 표 구조", "엑셀 자동화 주 업무"],
        "handoff": {"간섭 원본": "Navisworks_Addin", "구현 초안": "Qwen_Coder_8B", "고객 문서": "배포문서"},
    },
    "지식업데이트": {
        "owns": ["지식 베이스 반영", "출처/태그/시간 관리", "라우팅 지시문 유지"],
        "handoff": {"지식 분류/승격": "지식큐레이터", "프로세스 지시": "조율차장", "프롬프트 품질": "프롬프트엔지니어"},
    },
    "지식큐레이터": {
        "owns": ["일일 큐레이션 검수", "지식 목적성 분류", "승격/보류 판단", "Obsidian 연결 품질", "공개 전 지식 리스크 식별"],
        "handoff": {"자료 문체화": "테크니컬_라이터", "교육자료 승격": "교육컨설팅", "품질 체크리스트": "QA_테스터", "보안검토": "라이선스_보안관"},
    },
    "교육컨설팅": {
        "owns": ["신규 직원 온보딩", "연차별 교육 로드맵", "직무 역량 매트릭스", "교육 평가/수료 기준"],
        "handoff": {"입사/수습 행정": "경영지원", "BIM 표준 교육": "BIM_템플릿기획관", "슬라이드/강의자료 제작": "러닝콘텐츠디자이너", "교육 문서화": "테크니컬_라이터"},
    },
    "러닝콘텐츠디자이너": {
        "owns": ["NotebookLM 자료 구성", "교육 슬라이드", "강의안", "퀴즈/FAQ", "학습자용 요약본"],
        "handoff": {"교육 목표/평가 기준": "교육컨설팅", "기술 검수": "BIM_템플릿기획관", "문체/배포 형식": "테크니컬_라이터", "실습 검증": "QA_테스터"},
    },
    "프로젝트분석": {
        "owns": ["대상 프로젝트 유형", "반복 업무", "데이터 품질", "이해관계자 분석"],
        "handoff": {"요구사항 정리": "요구사항분석", "사업 우선순위": "전략기획"},
    },
    "전략기획": {
        "owns": ["MVP/Pro 구분", "로드맵", "기능 우선순위", "시장 검증 단계"],
        "handoff": {"제품 승인": "CEO", "수익성": "CFO", "요구사항 세분화": "요구사항분석"},
    },
    "아이디어발굴": {
        "owns": ["신규 제품 후보", "반복 업무 pain point", "Autodesk Store 키워드 적합성", "MVP 후보군"],
        "handoff": {"로드맵 우선순위": "전략기획", "공수/비용": "견적심사원", "수익성": "CFO"},
    },
    "견적심사원": {
        "owns": ["공수", "일정 버퍼", "비용 리스크", "견적 검토"],
        "handoff": {"범위 확정": "요구사항분석", "수익성 판단": "CFO"},
    },
    "글로벌_매출관리원": {
        "owns": ["MRR", "CAC", "전환율", "매출 지표"],
        "handoff": {"가격 정책": "CFO", "마케팅 메시지": "브랜드마케팅"},
    },
    "브랜드마케팅": {
        "owns": ["제품명", "스토어 설명", "스크린샷 메시지", "고객 가치 표현"],
        "handoff": {"심사 필수 항목": "스토어심사", "기술 문서": "테크니컬_라이터"},
    },
    "테크니컬_라이터": {
        "owns": ["사용자 가이드 문장", "릴리스 노트 표현", "제한사항 설명"],
        "handoff": {"설치 절차": "배포문서", "스토어 포지셔닝": "브랜드마케팅"},
    },
    "프롬프트엔지니어": {
        "owns": ["프롬프트 구조", "역할 지시문", "응답 포맷", "토큰 절약 기준"],
        "handoff": {"지식 저장": "지식업데이트", "프로세스 선택": "조율차장"},
    },
    "경영지원": {
        "owns": ["입사/수습 행정", "계정/권한 발급", "계약/청구 문서 보관", "필수 규정 교육"],
        "handoff": {"영수증/정산 자동 취합": "경비정산_AI", "직무 교육 설계": "교육컨설팅", "보안/NDA": "라이선스_보안관", "계약 조항": "법무조항검토"},
    },
    "경비정산_AI": {
        "owns": ["Telegram 영수증 수집", "증빙 항목 추출", "월별 비용 정산표 초안", "누락/중복 증빙 표시"],
        "handoff": {"회계/세무 확정": "경영지원", "정산표 자동화": "엑셀자동화", "민감정보 점검": "라이선스_보안관", "예산 추이": "CFO"},
    },
    "HR_인재분석관": {
        "owns": ["이력서분석_AI 실행 기능", "이력서 PDF 분석", "경력/프로젝트/기술 역량 구조화", "채용 대시보드 데이터", "1페이지 인재 평가 보고서 초안"],
        "handoff": {"채용 절차/보관": "경영지원", "온보딩/육성 계획": "교육컨설팅", "BIM 역량 기준": "BIM_템플릿기획관", "민감정보 점검": "라이선스_보안관", "최종 채용 판단": "CEO"},
    },
    "BIM_템플릿기획관": {
        "owns": ["BIM 템플릿", "공유 파라미터", "LOD/명명 규칙", "뷰/필터 기준"],
        "handoff": {"교육자료 구성": "교육컨설팅", "슬라이드/퀴즈 제작": "러닝콘텐츠디자이너", "공종별 세부 기준": "조율차장", "문서화": "테크니컬_라이터"},
    },
    "건축": {
        "owns": ["건축 공간", "천장고", "방화구획", "문/벽체 영향"],
        "handoff": {"구조 안전": "구조", "MEP 간섭": "조율차장"},
    },
    "구조": {
        "owns": ["보/기둥/슬래브", "관통/타공", "구조 검토 필요성"],
        "handoff": {"건축 요구": "건축", "MEP 조율": "조율차장"},
    },
    "공조배관": {
        "owns": ["냉온수/냉매 배관", "밸브 조작 공간", "단열 포함 외경"],
        "handoff": {"덕트 간섭": "공조덕트", "통합 조율": "조율차장"},
    },
    "공조덕트": {
        "owns": ["덕트 크기", "풍량/정압", "점검구", "제연덕트"],
        "handoff": {"배관 간섭": "공조배관", "통합 조율": "조율차장"},
    },
    "소방기계": {
        "owns": ["스프링클러", "소방배관", "알람밸브/펌프 연계"],
        "handoff": {"방재 신호": "소방전기", "통합 조율": "조율차장"},
    },
    "전기": {
        "owns": ["전력", "케이블 트레이", "분전반", "강전 이격"],
        "handoff": {"통신/약전": "통신", "통합 조율": "조율차장"},
    },
}


def clone_base_workflows() -> list[dict]:
    return copy.deepcopy(BASE_COLLABORATION_WORKFLOWS)


def workflow_by_id(workflows: list[dict], workflow_id: str) -> dict | None:
    for workflow in workflows:
        if workflow["id"] == workflow_id:
            return workflow
    return None


def add_unique(items: list[str], values: list[str]) -> None:
    for value in values:
        clean = value.strip()
        if clean and clean not in items:
            items.append(clean)


def split_directive_values(raw: str) -> list[str]:
    return [part.strip() for part in re.split(r"[,/|]", raw) if part.strip()]


def parse_workflow_directives(knowledge_dir: Union[str, Path]) -> list[dict]:
    """Read @workflow directives curated by the organization-management AI.

    Supported forms:
    @workflow <id> keyword: a, b
    @workflow <id> participant: A, B
    @workflow <id> step: text
    @workflow <id> primary: Agent
    @workflow <id> local_only: true
    """
    base = Path(knowledge_dir)
    directive_files = [
        base / "조율차장.md",
        base / "파이프라인_오케스트레이터.md",
        base / "지식업데이트.md",
        base / "아이디어발굴.md",
        base / "프로그램개발.md",
        base / "엑셀자동화.md",
        base / "경영지원.md",
        base / "HR_인재분석관.md",
        base / "전략기획.md",
        base / "CFO.md",
        base / "CEO.md",
    ]
    directives: list[dict] = []
    pattern = re.compile(r"^\s*@workflow\s+([\w\-]+)\s+([a-zA-Z_]+)\s*:\s*(.+?)\s*$")

    for path in directive_files:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            match = pattern.match(line)
            if not match:
                continue
            workflow_id, field, value = match.groups()
            directives.append({"workflow_id": workflow_id, "field": field.lower(), "value": value.strip(), "source": str(path)})
    return directives


def apply_workflow_directives(workflows: list[dict], directives: list[dict]) -> list[dict]:
    for directive in directives:
        workflow = workflow_by_id(workflows, directive["workflow_id"])
        if workflow is None:
            workflow = {
                "id": directive["workflow_id"],
                "name": directive["workflow_id"],
                "primary": "조율차장",
                "participants": ["조율차장"],
                "keywords": [],
                "steps": [],
                "local_only": True,
            }
            workflows.append(workflow)

        field = directive["field"]
        value = directive["value"]
        if field in {"keyword", "keywords"}:
            add_unique(workflow["keywords"], split_directive_values(value))
        elif field in {"participant", "participants"}:
            add_unique(workflow["participants"], split_directive_values(value))
        elif field == "step":
            add_unique(workflow["steps"], [value])
        elif field == "primary":
            workflow["primary"] = value
        elif field == "name":
            workflow["name"] = value
        elif field == "local_only":
            workflow["local_only"] = value.lower() in {"1", "true", "yes", "on", "로컬"}
    return workflows


def load_collaboration_workflows(knowledge_dir: Union[str, Path]) -> list[dict]:
    workflows = clone_base_workflows()
    return apply_workflow_directives(workflows, parse_workflow_directives(knowledge_dir))


def score_workflow(workflow: dict, lower_text: str) -> int:
    return sum(1 for keyword in workflow["keywords"] if keyword in lower_text)


def select_collaboration_workflow(user_text: str, target_agent: str, request_intent: str, workflows: list[dict]) -> dict:
    lower_text = user_text.lower()
    if request_intent == "support":
        if any(keyword in lower_text for keyword in EDUCATION_TRAINING_KEYWORDS):
            workflow_id = "employee_onboarding_training"
        elif any(keyword in lower_text for keyword in SUPPORT_PRICING_KEYWORDS):
            workflow_id = "pricing_revenue"
        elif any(keyword in lower_text for keyword in SUPPORT_LICENSE_KEYWORDS):
            workflow_id = "license_billing"
        else:
            workflow_id = "support_general"
        return workflow_by_id(workflows, workflow_id) or workflows[0]

    priority_overrides = [
        ("resume_analysis_dashboard", ["이력서", "resume", "cv", "지원자", "후보자", "채용", "서류 검토", "서류심사", "인재 평가", "인재평가", "경력 분석", "경력 대시보드", "평가 보고서", "pdf 이력서"]),
        ("expense_receipt_intake", ["영수증", "증빙", "경비", "비용 정산", "비용정산", "정산", "세금계산서", "거래명세서", "카드전표", "receipt", "expense", "텔레그램 영수증"]),
        ("excel_qwen_automation", ["엑셀", "excel", "xlsx", "csv", "openxml", "워크북", "시트", "리포트 자동화", "보고서 자동화", "내보내기", "export"]),
        ("idea_to_product_development_queue", ["상품화 우선순위", "개발 순서", "개발 큐", "다음 업무", "다음 상품", "아이디어발굴 조직", "자체적으로 아이디어", "기능 내재화 종료", "qwen 큐", "상품화 후보", "개발진행", "조직간 협업"]),
        ("daily_idea_report", ["아이디어", "매일", "일일 보고", "3가지", "수익화", "토큰수", "투입비용", "투입 시간"]),
        ("build_qa", ["smoke", "qa", "검증", "빌드", "회귀", "테스트 체크리스트"]),
        ("employee_onboarding_training", EDUCATION_TRAINING_KEYWORDS),
        ("navisworks_development", ["navisworks", "navis", "나비스웍스", "나비스"]),
        ("revit_development", ["revit", "레빗", "revit api"]),
        ("local_qwen_development", ["qwen", "qwen coder", "로컬 코더", "로컬 1차", "1차 개발", "업무지시", "개발 업무", "일반 코드", "fastapi", "frontend", "백엔드", "프론트엔드", "리팩토링", "테스트 코드"]),
        ("knowledge_update", ["큐레이션", "분류", "승격", "보류", "지식 정리", "지식 업데이트", "knowledge", "kb", "지식", "프롬프트 기준"]),
        ("privacy_security", ["개인정보", "privacy", "보안", "api key", "토큰", "외부 통신", "데이터 전송", "모델 데이터", "처리방침"]),
        ("pricing_revenue", ["가격", "mrr", "매출", "손익분기", "사업성", "구독 가격", "달러", "enterprise"]),
        ("coordination_discipline", ["간섭", "clash", "coordination", "mep통합", "전체공정"]),
        ("requirements_scope", ["견적", "공수", "일정 버퍼"]),
    ]
    for workflow_id, keywords in priority_overrides:
        if any(keyword in lower_text for keyword in keywords):
            matched = workflow_by_id(workflows, workflow_id)
            if matched:
                return matched

    scored = sorted(
        ((score_workflow(workflow, lower_text), workflow) for workflow in workflows),
        key=lambda item: item[0],
        reverse=True,
    )
    if scored and scored[0][0] > 0:
        return scored[0][1]

    for workflow in workflows:
        if workflow["primary"] == target_agent:
            return workflow
    return workflow_by_id(workflows, "requirements_scope") or workflows[0]


def has_explicit_support_channel(user_text: str) -> bool:
    lower_text = user_text.lower()
    return any(keyword in lower_text for keyword in EXPLICIT_SUPPORT_CHANNEL_KEYWORDS)


def determine_primary_agent(user_text: str, target_agent: str, workflow: dict, request_intent: str) -> str:
    lower_text = user_text.lower()
    if request_intent == "support" and has_explicit_support_channel(user_text):
        return "고객지원 CS"
    if workflow.get("id") == "employee_onboarding_training" and target_agent == "러닝콘텐츠디자이너":
        return "러닝콘텐츠디자이너"
    if workflow.get("id") == "knowledge_update" and any(keyword in lower_text for keyword in ["큐레이션", "분류", "승격", "보류", "보안검토", "지식 정리"]):
        return "지식큐레이터"
    return workflow["primary"] or target_agent


def should_run_discipline_review(workflow: dict, target_agent: str, discipline_agents: set[str]) -> bool:
    discipline_workflows = {"revit_development", "navisworks_development", "coordination_discipline"}
    return workflow["id"] in discipline_workflows or target_agent in discipline_agents


AUTODESK_API_KEYWORDS = [
    "revit api", "iexternalcommand", "iexternalapplication", "transaction",
    "filteredelementcollector", ".addin", "add-in manifest", "navisworks api",
    "clashresult", "clash detective", "modelitem", "searchset", "직접 읽", "원본 api",
]


def requires_supreme_validation(user_text: str, workflow: dict | None = None) -> bool:
    lower_text = user_text.lower()
    if workflow and workflow.get("id") in {"revit_development", "navisworks_development"}:
        return True
    return any(keyword in lower_text for keyword in AUTODESK_API_KEYWORDS)


def local_coder_gate(user_text: str, workflow: dict) -> dict:
    requires_validation = requires_supreme_validation(user_text, workflow)
    if requires_validation:
        mode = "supreme_validation_required"
        qwen_role = "addin_guideline_draft"
        verification_owner = "최고지배자"
        instruction = "Revit/Navisworks API 의존 작업이므로 Qwen은 Add-in 초안 가이드라인과 정적 검토까지만 수행하고 최고지배자 실기 테스트 후 확정한다."
    elif workflow.get("id") == "excel_qwen_automation":
        mode = "qwen_excel_primary"
        qwen_role = "excel_automation_primary"
        verification_owner = "Qwen_Coder_8B -> QA_테스터 -> 빌드검증"
        instruction = "엑셀 자동화는 Qwen_Coder_8B를 주 업무 구현 담당으로 두고 샘플 데이터 검증까지 로컬에서 먼저 수행한다."
    elif workflow.get("id") == "local_qwen_development":
        mode = "qwen_first_pass"
        qwen_role = "local_first_pass_developer"
        verification_owner = "Qwen_Coder_8B -> 프로그램개발 -> QA_테스터"
        instruction = "Qwen_Coder_8B가 로컬 1차 구현 초안을 작성하고 목적/검증 plan을 기준으로 프로그램개발/QA/빌드검증이 검토한다."
    else:
        mode = "standard_local_review"
        qwen_role = "not_primary"
        verification_owner = "조율차장"
        instruction = "로컬 지식 기반 협업으로 처리한다."
    return {
        "mode": mode,
        "local_model": "qwen2.5-coder:7b",
        "plan_required": True,
        "qwen_role": qwen_role,
        "verification_owner": verification_owner,
        "requires_supreme_validation": requires_validation,
        "api_escalation_policy": "Qwen 로컬 검증으로 해결되지 않거나 Revit/Navisworks/외부 API 접근이 필요할 때만 API 활용 검토",
        "instruction": instruction,
    }


IDEA_CANDIDATES = [
    {
        "title": "Revit 모델 품질 빠른 진단 리포트",
        "problem": "납품 전 모델에서 경고, 미사용 뷰, 잘못된 네이밍, 과도한 파일 용량을 사람이 반복 점검한다.",
        "solution": "Revit 파일 내부 품질 항목을 원클릭으로 점검하고 Excel/HTML 리포트로 내보낸다.",
        "customer": "BIM 매니저, 설계사무소 납품 담당자",
        "keywords": ["revit", "quality", "report", "bim manager"],
        "complexity": "medium",
        "revenue_score": 8,
        "time_saving_minutes": 45,
        "implementation_risk": 4,
        "store_fit": 9,
    },
    {
        "title": "Navisworks 간섭 결과 책임자 배정 보드",
        "problem": "Clash Detective 결과를 공종별 담당자와 상태로 관리하는 과정이 Excel 수작업에 묶인다.",
        "solution": "간섭 결과를 공종/층/우선순위/담당자 기준으로 정리하고 CSV 리포트를 자동 생성한다.",
        "customer": "BIM 코디네이터, 현장 조율 PM",
        "keywords": ["navisworks", "clash", "coordination", "excel"],
        "complexity": "medium",
        "revenue_score": 9,
        "time_saving_minutes": 60,
        "implementation_risk": 5,
        "store_fit": 8,
    },
    {
        "title": "Revit 패밀리 파라미터 표준화 검사기",
        "problem": "프로젝트마다 패밀리 공유 파라미터와 네이밍 규칙이 달라 집계 오류가 반복된다.",
        "solution": "패밀리/타입 파라미터를 표준 템플릿과 비교하고 누락/오타를 수정 후보로 제시한다.",
        "customer": "BIM 템플릿 관리자, 설계 QA 담당자",
        "keywords": ["revit", "family", "parameter", "template"],
        "complexity": "high",
        "revenue_score": 7,
        "time_saving_minutes": 50,
        "implementation_risk": 6,
        "store_fit": 7,
    },
    {
        "title": "층별 도면 시트 자동 검수기",
        "problem": "층별 평면/천장/전기/소방 시트 누락과 뷰 스케일 불일치를 사람이 출도 직전 확인한다.",
        "solution": "시트 세트와 뷰 템플릿 규칙을 비교해 누락, 스케일, 제목 불일치를 체크리스트로 출력한다.",
        "customer": "설계 PM, BIM 납품 담당자",
        "keywords": ["revit", "sheet", "view template", "qa"],
        "complexity": "low",
        "revenue_score": 7,
        "time_saving_minutes": 35,
        "implementation_risk": 3,
        "store_fit": 8,
    },
    {
        "title": "MEP 점검구 접근성 체크 도우미",
        "problem": "덕트, 밸브, 장비 점검구 접근 공간을 모델에서 반복 확인하지만 기준 누락이 잦다.",
        "solution": "MEP 장비 주변 점검 공간과 간섭 후보를 규칙 기반으로 표시하고 검토 목록을 만든다.",
        "customer": "MEP BIM 엔지니어, 시공 조율 담당자",
        "keywords": ["mep", "clearance", "maintenance", "revit"],
        "complexity": "high",
        "revenue_score": 8,
        "time_saving_minutes": 70,
        "implementation_risk": 7,
        "store_fit": 7,
    },
]

COMPLEXITY_ESTIMATES = {
    "low": {"tokens": 18000, "hours": 10, "cost_usd": 120},
    "medium": {"tokens": 36000, "hours": 24, "cost_usd": 320},
    "high": {"tokens": 64000, "hours": 48, "cost_usd": 760},
}


def estimate_idea_candidate(candidate: dict) -> dict:
    estimate = COMPLEXITY_ESTIMATES[candidate["complexity"]]
    gross_monthly_revenue = candidate["revenue_score"] * 19 * 8
    monthly_support_cost = 40 + candidate["implementation_risk"] * 12
    net_monthly_revenue = round(gross_monthly_revenue * 0.65 - monthly_support_cost, 2)
    payback_months = round(estimate["cost_usd"] / max(net_monthly_revenue, 1), 1)
    monetization_score = (
        candidate["revenue_score"] * 2
        + candidate["store_fit"] * 2
        + min(candidate["time_saving_minutes"] // 10, 8)
        - candidate["implementation_risk"]
    )
    return {
        **candidate,
        "estimated_tokens": estimate["tokens"],
        "estimated_hours": estimate["hours"],
        "estimated_cost_usd": estimate["cost_usd"],
        "expected_monthly_net_usd": net_monthly_revenue,
        "payback_months": payback_months,
        "monetization_score": monetization_score,
        "recommended_price": "USD 19/month or USD 190/year",
        "api_mode": "local_only",
    }


def build_daily_idea_report(limit: int = 3) -> dict:
    ranked = sorted(
        (estimate_idea_candidate(candidate) for candidate in IDEA_CANDIDATES),
        key=lambda item: (item["monetization_score"], -item["payback_months"], -item["implementation_risk"]),
        reverse=True,
    )
    selected = ranked[:limit]
    return {
        "workflow_id": "daily_idea_report",
        "title": "최고지배자 일일 3대 아이디어 검토 보고",
        "mode": "local_only",
        "report_rule": "최고지배자의 별도 요청이 없으면 매일 3개 후보만 선별 보고한다.",
        "participants": ["아이디어발굴", "전략기획", "견적심사원", "CFO", "CEO", "브랜드마케팅"],
        "assumptions": [
            "유료 API 호출 없이 지식 베이스와 고정 산식만 사용",
            "기준 가격은 CFO 지식 베이스의 USD 19/month 또는 USD 190/year",
            "예상 비용은 구현 난이도별 내부 개발 시간, 검증 시간, 문서화 부담을 합산한 보수적 추정",
            "수익화 판단은 반복 업무 절감, Store 키워드 적합성, 구현 리스크, 예상 순매출을 함께 반영",
        ],
        "ideas": selected,
        "rejected_count": max(len(ranked) - len(selected), 0),
    }


def build_workflow_summary(workflow: dict, participants: list[str], use_paid_ai: bool) -> str:
    steps = "\n".join(f"{idx + 1}. {step}" for idx, step in enumerate(workflow["steps"]))
    api_mode = "유료 API 사용 가능" if use_paid_ai and not workflow.get("local_only") else "로컬 지식 기반"
    return (
        f"[협업 프로세스]\n"
        f"- 케이스: {workflow['name']}\n"
        f"- 처리 모드: {api_mode}\n"
        f"- 참여 팀원: {' → '.join(participants)}\n"
        f"- 진행 순서:\n{steps}"
    )


def role_boundary(agent: str) -> dict:
    return ROLE_BOUNDARIES.get(agent, {"owns": [f"{agent} 담당 도메인"], "handoff": {"경계 초과": "조율차장"}})


def role_boundary_line(agent: str) -> str:
    boundary = role_boundary(agent)
    owns = ", ".join(boundary["owns"][:3])
    handoff = ", ".join(f"{key}->{value}" for key, value in list(boundary["handoff"].items())[:2])
    return f"{agent}: 소유={owns}; 경계초과={handoff}"


def build_role_boundary_summary(participants: list[str]) -> str:
    return "[역할 경계]\n" + "\n".join(f"- {role_boundary_line(agent)}" for agent in participants)


def audit_collaboration_workflows(workflows: list[dict]) -> list[dict]:
    issues: list[dict] = []
    known_roles = set(ROLE_BOUNDARIES)
    for workflow in workflows:
        participants = workflow.get("participants", [])
        primary = workflow.get("primary")
        if primary and primary not in participants:
            participants = [primary] + participants
        missing_roles = [agent for agent in participants if agent not in known_roles]
        if missing_roles:
            issues.append({
                "workflow_id": workflow["id"],
                "severity": "warn",
                "issue": "역할 경계 미정의 참여자",
                "agents": missing_roles,
            })
        if not workflow.get("steps"):
            issues.append({
                "workflow_id": workflow["id"],
                "severity": "error",
                "issue": "진행 단계 없음",
            })
        if not workflow.get("keywords"):
            issues.append({
                "workflow_id": workflow["id"],
                "severity": "warn",
                "issue": "라우팅 키워드 없음",
            })
    return issues

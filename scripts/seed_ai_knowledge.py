import sys
import datetime
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import AGENT_KB_DIR  # noqa: E402

KNOWLEDGE_DIR = AGENT_KB_DIR

COMMON_SOURCE = "LUA BIM LABS curated baseline, Autodesk official docs checked 2026-05-19"

KNOWLEDGE_PACKETS = {
    "CEO": {
        "title": "상용 BIM Add-in 제품 의사결정 기준",
        "tags": "strategy,product,store",
        "content": (
            "Revit/Navisworks Add-in은 내부 자동화가 아니라 Autodesk App Store 판매 제품으로 판단한다. "
            "기능 우선순위는 고객 반복 고통, 설치/유지관리 용이성, Autodesk 제품 안정성, 심사 리스크, 유료 전환 가능성을 함께 본다. "
            "심사 거절 리스크가 있는 불안정 기능, 문서 불일치, 개인정보 무단 수집, Autodesk 제품 성능 저하 기능은 출시 범위에서 제외한다."
        ),
    },
    "조율차장": {
        "title": "개발 PM 조율 기준",
        "tags": "pm,coordination,requirements",
        "content": (
            "Add-in 개발 요청은 개발팀 의견과 공정 AI 의견을 분리 수집한 뒤 최종 요구사항으로 병합한다. "
            "최종 보고서에는 구현 범위, 제외 범위, 공정별 데이터 필드, 예외 조건, 테스트 항목, 배포/스토어 리스크를 반드시 남긴다."
        ),
    },
    "건축": {
        "title": "건축 공정 Add-in 검토 기준",
        "tags": "architecture,space,clearance",
        "content": (
            "건축 관점은 실 사용성, 천장고, 방화구획, 피난 동선, 마감 두께, 문/벽체/실 경계와의 충돌을 우선한다. "
            "보고서에는 영향을 받는 실명, 레벨, 구역, 마감/천장 영향, 건축 승인 필요 여부를 포함해야 한다."
        ),
    },
    "구조": {
        "title": "구조 공정 Add-in 검토 기준",
        "tags": "structure,opening,penetration",
        "content": (
            "구조 관점은 보, 기둥, 슬래브, 전이보, 내력벽 관통과 개구부 보강 가능 여부를 우선한다. "
            "Add-in은 구조 부재 관통을 단순 clash가 아니라 구조 검토 필요 이슈로 분류하고, 부재명/단면/레벨/관통 크기/이격 정보를 기록해야 한다."
        ),
    },
    "토목": {
        "title": "토목 공정 Add-in 검토 기준",
        "tags": "civil,site,utility",
        "content": (
            "토목 관점은 외부 인입 레벨, 대지 경계, GL/FL 관계, 우수/오수/상수 관로 접속 조건을 우선한다. "
            "건물 내부 MEP 변경이 외부 관로 구배와 접속 높이에 미치는 영향을 별도 경고로 남겨야 한다."
        ),
    },
    "위생": {
        "title": "위생 공정 Add-in 검토 기준",
        "tags": "plumbing,drainage,slope",
        "content": (
            "위생 관점은 배수 구배, 통기관, 관경, 위생기구 연결, 펌프/집수정 연계, 점검구 접근성을 우선한다. "
            "자연유하 배관은 우회 가능 여부 판단 시 레벨 손실과 최소 구배 유지 가능성을 보고서 필수 항목으로 둔다."
        ),
    },
    "공조배관": {
        "title": "공조배관 공정 Add-in 검토 기준",
        "tags": "hvac-piping,insulation,valve",
        "content": (
            "공조배관 관점은 단열 포함 외경, 밸브 조작 공간, 플랜지/유니온 유지관리, 냉온수/냉매 배관 레이어를 우선한다. "
            "Add-in은 중심선 clash뿐 아니라 단열 두께와 유지관리 공간을 포함한 여유 간섭을 계산해야 한다."
        ),
    },
    "공조덕트": {
        "title": "공조덕트 공정 Add-in 검토 기준",
        "tags": "hvac-duct,airflow,access",
        "content": (
            "공조덕트 관점은 덕트 규격, 하부 레벨, 풍량/정압 영향, 점검구, 소음/진동, 제연덕트 우선순위를 본다. "
            "보고서에는 덕트 사이즈, 우회 가능성, 천장고 영향, 점검구 침해 여부를 포함해야 한다."
        ),
    },
    "소방기계": {
        "title": "소방기계 공정 Add-in 검토 기준",
        "tags": "fire-mechanical,sprinkler,code",
        "content": (
            "소방기계 관점은 스프링클러 헤드 살수반경, 배관 레이어, 알람밸브/펌프 연계, 소방법 민감 구간을 우선한다. "
            "Add-in은 소방 관련 이슈를 일반 MEP clash와 분리해 법규 검토 필요 항목으로 표시해야 한다."
        ),
    },
    "소방전기": {
        "title": "소방전기 공정 Add-in 검토 기준",
        "tags": "fire-electrical,detector,alarm",
        "content": (
            "소방전기 관점은 감지기 배치, 수신기/발신기, 방화셔터/제연 연동, 비상 방송 및 방재 신호 경로를 우선한다. "
            "Add-in은 감지기 사각, 방재 연동 누락, 선로 단절 가능성을 보고서 경고 항목으로 둔다."
        ),
    },
    "전기": {
        "title": "전기 공정 Add-in 검토 기준",
        "tags": "electrical,tray,panel",
        "content": (
            "전기 관점은 케이블 트레이 폭/높이, 곡률 반경, 분전반 접근 공간, 누수 회피, 강전/약전 이격을 우선한다. "
            "보고서에는 트레이 용량, 굴곡 제한, 장비 유지관리 공간 침해 여부를 남겨야 한다."
        ),
    },
    "통신": {
        "title": "통신 공정 Add-in 검토 기준",
        "tags": "telecom,low-voltage,emi",
        "content": (
            "통신 관점은 약전 트레이, 네트워크/CCTV/방송 배선, MDF/IDF 접근성, 전력선과의 이격 및 EMI 리스크를 우선한다. "
            "Add-in은 강전 트레이와 통신 트레이의 이격 부족을 별도 분류해야 한다."
        ),
    },
    "요구사항분석": {
        "title": "Add-in 요구사항 분석 기준",
        "tags": "spec,user-story,scope",
        "content": (
            "요구사항은 사용자 문제, 입력 데이터, 처리 로직, 결과 출력, 예외 조건, 지원 Revit/Navisworks 버전, 라이선스 상태별 동작으로 분해한다. "
            "공정 AI 의견은 별도 부록이 아니라 기능 요구사항과 테스트 조건으로 변환해야 한다."
        ),
    },
    "Revit_Addin": {
        "title": "Revit API 개발 기준",
        "tags": "revit-api,addin,manifest",
        "content": (
            "Revit Add-in은 .addin manifest로 등록하고, 명령형 기능은 IExternalCommand, 세션/리본 초기화 기능은 IExternalApplication 중심으로 설계한다. "
            "Revit API는 Revit 프로세스 내부 DLL과 단일 스레드 API 접근 제약을 고려해야 하며, 모델 변경은 Transaction 정책을 명확히 둔다. "
            "공식 출처: Autodesk Revit API Add-in Registration, External Commands, Deployment Options."
        ),
    },
    "Navisworks_Addin": {
        "title": "Navisworks API 개발 기준",
        "tags": "navisworks-api,plugin,automation",
        "content": (
            "Navisworks .NET API는 Plug-In, Automation, Controls 사용 방식이 있으며, SDK/API 문서와 샘플은 Navisworks Manage/Simulate 설치 폴더의 api 폴더를 기준으로 확인한다. "
            "Clash/coordination 제품은 플러그인 실행, 모델/문서 정보 접근, 보고서 추출 및 외부 대시보드 연계를 분리 설계한다. "
            "공식 출처: Autodesk Platform Services Navisworks API overview."
        ),
    },
    "빌드검증": {
        "title": "상용 Add-in 빌드 검증 기준",
        "tags": "qa,build,smoke-test",
        "content": (
            "빌드 검증은 지원 버전별 로드 테스트, manifest 경로 테스트, 샘플 모델 smoke test, 예외/빈 문서/선택 없음 상태, 성능 저하 여부를 확인한다. "
            "Autodesk App Store 심사 리스크를 줄이기 위해 충돌, 심각한 지연, 설치/제거 실패를 release blocker로 둔다."
        ),
    },
    "배포문서": {
        "title": "배포 문서 기준",
        "tags": "docs,release,addin",
        "content": (
            "배포 문서는 설치 방법, 제거 방법, 지원 제품/버전, 첫 실행 절차, 권한/네트워크 사용, 알려진 제한, 지원 이메일을 포함한다. "
            "스토어 설명과 실제 기능이 다르면 심사/고객지원 리스크가 커지므로 문서와 제품 동작을 함께 관리한다."
        ),
    },
    "제품패키징": {
        "title": "Autodesk Store 제품 패키징 기준",
        "tags": "installer,msi,package",
        "content": (
            "패키지는 고객이 개발자 도움 없이 설치/제거/업데이트할 수 있어야 한다. "
            "Autodesk Product Guidelines는 설치/제거/유지관리가 어려운 제품, 불완전한 제품, 최신 Autodesk 릴리스 미지원 제품을 거절 사유로 본다."
        ),
    },
    "스토어심사": {
        "title": "Autodesk App Store 심사 기준",
        "tags": "app-store,review,submission",
        "content": (
            "Autodesk App Store 심사는 고객 가치, 안정성, Autodesk 제품 성능 영향, 문서 일관성, 개인정보/권리 침해, 공식 문서에 없는 API 사용 여부를 본다. "
            "제출물은 제품명, 설명, 가격, 지원 자료, 호환성, 개인정보 정책, 지원 연락처를 갖춰야 한다. "
            "공식 출처: Autodesk App Store Product Guidelines, App Store Getting Started Guide."
        ),
    },
    "라이선스결제": {
        "title": "라이선스와 결제 기준",
        "tags": "license,billing,entitlement",
        "content": (
            "유료/구독 제품은 가격, 결제 제공자, 라이선스 상태별 UX, 오프라인/네트워크 실패 시 동작을 명확히 해야 한다. "
            "Autodesk App Store 자료는 유료 앱 결제에 PayPal 및 BlueSnap 사용을 언급한다. Entitlement/API 연계가 필요한 경우 별도 검증한다."
        ),
    },
    "지식업데이트": {
        "title": "지식 업데이트 운영 기준",
        "tags": "knowledge,governance,curation",
        "content": (
            "각 AI 지식은 출처, 태그, 시간과 함께 markdown으로 누적한다. 공식 문서, 사내 표준, 현장 피드백, 테스트 결과를 구분하고, 법규/수치 기준은 지역과 적용 연도를 함께 기록한다."
        ),
    },
    "최고전략 (CSO)": {
        "title": "BIM Add-in 전략 기준",
        "tags": "strategy,market,positioning",
        "content": (
            "상용 Add-in은 반복 업무 절감, 오류 감소, 보고 자동화, 스토어 검색 키워드 경쟁력으로 포지셔닝한다. 기능은 작고 명확한 MVP로 시작해 스토어 피드백 기반으로 확장한다."
        ),
    },
    "파이프라인_오케스트레이터": {
        "title": "개발 파이프라인 기준",
        "tags": "pipeline,automation,workflow",
        "content": (
            "요청 접수, 공정 지식 로딩, 개발안 작성, 공정 검토, 빌드 검증, 스토어 체크리스트 생성을 하나의 반복 가능한 파이프라인으로 관리한다."
        ),
    },
    "Caveman_토큰다이어터": {
        "title": "토큰 절감 기준",
        "tags": "token,context,compression",
        "content": (
            "공정 지식은 최근/관련 항목 중심으로 잘라 주입하고, 긴 문서는 요구사항·예외조건·테스트 항목만 요약한다. 중복 설명보다 표준 필드명을 유지한다."
        ),
    },
    "프로그램개발": {
        "title": "프로그램 개발 기준",
        "tags": "development,csharp,dotnet",
        "content": (
            "C#/.NET Add-in 코드는 Autodesk 제품별 API 경계, 예외 처리, 로깅, 설정 파일, 라이선스 체크, 테스트 가능한 순수 로직 분리를 기준으로 설계한다."
        ),
    },
    "QA_테스터": {
        "title": "QA 테스트 기준",
        "tags": "qa,test,regression",
        "content": (
            "QA는 지원 버전별 설치/로드/기능/성능/제거 테스트와 샘플 모델 회귀 테스트를 관리한다. 스토어 제출 전 crash와 성능 저하는 차단 결함으로 본다."
        ),
    },
    "테크니컬_라이터": {
        "title": "기술문서 기준",
        "tags": "docs,user-guide,release-notes",
        "content": (
            "문서는 설치, 첫 실행, 주요 기능, 제한사항, 문제 해결, 지원 연락처, 개인정보/네트워크 사용 여부를 고객 언어로 짧고 명확하게 쓴다."
        ),
    },
    "라이선스_보안관": {
        "title": "보안/라이선스 기준",
        "tags": "security,license,privacy",
        "content": (
            "토큰, API 키, 고객 모델 데이터, 라이선스 상태는 로그와 보고서에 노출하지 않는다. 외부 통신은 사용자 고지와 정책 문서가 필요하며, 모델 데이터 전송은 최소화한다."
        ),
    },
}

KNOWLEDGE_PACKETS.update({
    "COO": {
        "title": "운영 총괄 기준",
        "tags": "operations,delivery,process",
        "content": (
            "COO는 개발 요청이 실제 납품 가능한 운영 흐름으로 이어지는지 본다. 범위, 일정, 리소스, 품질 기준, 고객지원 준비 상태를 확인하고 병목을 조율한다."
        ),
    },
    "CFO": {
        "title": "상용 Add-in 재무 기준",
        "tags": "finance,pricing,cost",
        "content": (
            "CFO는 개발 비용, Autodesk Store 판매 가격, 구독/일회성 과금, 지원 비용, 결제 수수료, 세금 유보, 손익분기점을 기준으로 제품 출시 판단을 보조한다."
        ),
    },
    "아이디어발굴": {
        "title": "BIM Add-in 아이디어 발굴 기준",
        "tags": "ideation,market,pain-point",
        "content": (
            "아이디어는 반복 빈도, 수작업 시간 절감, 오류 감소, 현장/설계자 체감 가치, Autodesk Store 검색 키워드 적합성을 기준으로 수집한다. 작은 단일 문제를 명확히 푸는 MVP를 우선한다."
        ),
    },
    "전략기획": {
        "title": "제품 전략 기획 기준",
        "tags": "planning,roadmap,mvp",
        "content": (
            "전략기획은 MVP, Pro 기능, Store 출시 버전, 향후 구독 기능을 나눠 로드맵을 만든다. 기능은 공정 지식 기반 검토, Revit/Navisworks API 가능성, 심사 리스크로 우선순위를 정한다."
        ),
    },
    "프로젝트분석": {
        "title": "프로젝트 분석 기준",
        "tags": "project-analysis,bim,use-case",
        "content": (
            "프로젝트분석은 대상 프로젝트 유형, 반복 업무, 공정별 이해관계자, 모델 데이터 품질, 보고 산출물 형태를 분석해 Add-in 요구사항의 현실성을 검토한다."
        ),
    },
    "브랜드마케팅": {
        "title": "Autodesk Store 마케팅 기준",
        "tags": "marketing,listing,positioning",
        "content": (
            "브랜드마케팅은 제품명, 짧은 설명, 스크린샷, 데모 흐름, 고객 문제 표현, 차별점, 지원 제품 버전을 Store 페이지에서 즉시 이해되게 만든다."
        ),
    },
    "고객지원 CS": {
        "title": "고객지원 CS 기준",
        "tags": "customer-support,faq,store,support,privacy,operations",
        "content": (
            "고객지원 CS는 일반 고객 문의의 단일 통합 창구다. 설치 실패, 라이선스 인증, 기능 사용법, 모델별 오류, 환불/구독 문의에 대한 FAQ와 응답 템플릿을 관리한다. Store 제품 페이지의 지원 이메일 응답 품질을 유지한다. 기술 재현이 필요한 문의는 CS 내부 에스컬레이션으로 처리한다. 스토어 판매 제품은 지원 이메일, 개인정보 처리방침, 장애/환불/라이선스 문의 대응 흐름을 갖춰야 한다."
        ),
    },
    "CS_기술지원관": {
        "title": "기술지원 기준",
        "tags": "technical-support,diagnostics,logs",
        "content": (
            "기술지원관은 별도 조직도 노드가 아니라 고객지원 CS 내부 에스컬레이션 기준이다. 고객 환경의 Autodesk 제품 버전, Windows/.NET 상태, Add-in 로그, 샘플 모델 재현 절차, 충돌 발생 명령을 수집해 개발팀이 재현 가능한 이슈로 변환한다."
        ),
    },
    "협력사안부": {
        "title": "협력사 관리 기준",
        "tags": "partner,vendor,coordination",
        "content": (
            "협력사안부는 외부 개발자, BIM 컨설턴트, 현장 검토자와의 역할·납기·결과물 기준을 관리한다. 고객 모델이나 민감 데이터 공유 시 범위와 보안 조건을 확인한다."
        ),
    },
    "법무조항검토": {
        "title": "법무/약관 검토 기준",
        "tags": "legal,terms,privacy",
        "content": (
            "법무조항검토는 EULA, 개인정보 처리방침, 환불/지원 조건, 책임 제한, 제3자 라이브러리 라이선스, Autodesk 상표 사용 기준을 검토한다."
        ),
    },
    "견적심사원": {
        "title": "개발 견적 심사 기준",
        "tags": "estimate,cost,scope",
        "content": (
            "견적심사원은 기능 범위, API 난이도, 테스트 버전 수, UI/문서/패키징/지원 범위를 기준으로 개발 견적과 일정 리스크를 검토한다."
        ),
    },
    "EIR/BEP_심사원": {
        "title": "EIR/BEP 요구사항 검토 기준",
        "tags": "eir,bep,bim-requirements",
        "content": (
            "EIR/BEP 심사원은 고객 BIM 요구사항, 모델 명명 규칙, 좌표/레벨 기준, 속성 입력 기준, LOD/LOI, 보고서 제출 양식이 Add-in 기능과 맞는지 확인한다."
        ),
    },
    "BIM_템플릿기획관": {
        "title": "BIM 템플릿 기획 기준",
        "tags": "bim-template,parameters,standards",
        "content": (
            "BIM 템플릿기획관은 공유 파라미터, 카테고리, 뷰/필터, 패밀리 명명 규칙, 보고서 필드 표준을 정리해 Add-in이 일관된 데이터 구조를 쓰도록 한다."
        ),
    },
    "프롬프트엔지니어": {
        "title": "AI 프롬프트 설계 기준",
        "tags": "prompt,agent,workflow",
        "content": (
            "프롬프트엔지니어는 개발 요청, 공정 지식, Store 심사 기준을 명확히 분리해 모델에 제공한다. 출력은 요구사항, 구현안, 예외 조건, 테스트 항목, 출시 리스크 형식을 유지한다."
        ),
    },
    "글로벌_유통기획관": {
        "title": "글로벌 유통 기준",
        "tags": "distribution,localization,store",
        "content": (
            "글로벌 유통기획관은 영어/한국어 제품 설명, 가격 전략, 지원 시간대, 지역별 개인정보/환불 기대치, Store 검색 키워드와 현지화 우선순위를 관리한다."
        ),
    },
    "엔지니어링계산서": {
        "title": "엔지니어링 계산서 기준",
        "tags": "calculation,engineering,report",
        "content": (
            "엔지니어링계산서는 Add-in 보고서가 단순 텍스트가 아니라 근거 수치, 간섭 치수, 레벨 차, 구배, 이격, 용량, 우선순위 산식을 포함하도록 검토한다."
        ),
    },
    "외주관리": {
        "title": "외주 개발 관리 기준",
        "tags": "outsourcing,delivery,review",
        "content": (
            "외주관리는 소스코드 소유권, 납품물 목록, 보안, 테스트 증빙, 문서, 빌드 재현성, Autodesk API 사용 준수 여부를 계약과 검수 기준에 넣는다."
        ),
    },
    "견적서담당": {
        "title": "견적서 작성 기준",
        "tags": "proposal,quote,scope",
        "content": (
            "견적서담당은 기능 범위, 제외 범위, 지원 버전, 납기, 유지보수, Store 제출 지원, 라이선스 서버/결제 연동 여부를 견적 항목으로 분리한다."
        ),
    },
    "글로벌_매출관리원": {
        "title": "글로벌 매출 관리 기준",
        "tags": "revenue,subscription,analytics",
        "content": (
            "글로벌 매출관리원은 Store 판매량, 구독 유지율, 환불률, 지원 비용, 기능별 업셀 가능성, 국가별 매출 흐름을 추적해 제품 전략에 반영한다."
        ),
    },
    "경영지원": {
        "title": "경영지원 기준",
        "tags": "admin,operations,finance",
        "content": (
            "경영지원은 세금 자료, 계약/청구, 계정 관리, 지원 이메일 운영, Store publisher 정보, 개인정보 정책 문서 유지관리를 담당한다."
        ),
    },
    "엑셀자동화": {
        "title": "엑셀 자동화 기준",
        "tags": "excel,report,export",
        "content": (
            "엑셀자동화는 clash/report 결과를 고객이 바로 필터링할 수 있는 표 구조로 내보내도록 설계한다. 필드명, 단위, 레벨, 공정, 조치 상태, 담당자, 우선순위를 표준화한다."
        ),
    },
    "인프라_DevOps (Obsidian)": {
        "title": "로컬 인프라/DevOps 기준",
        "tags": "devops,obsidian,local",
        "content": (
            "인프라 DevOps는 지식 베이스, 로그, 빌드 산출물, 릴리스 노트, Obsidian 문서 동기화를 관리한다. 민감 토큰은 .env에 두고 저장소 커밋 대상에서 제외한다."
        ),
    },
})


def safe_filename(agent):
    return "".join(ch for ch in agent if ch.isalnum() or ch in ("_", "-"))


def main():
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for agent, packet in KNOWLEDGE_PACKETS.items():
        path = os.path.join(KNOWLEDGE_DIR, f"{safe_filename(agent)}.md")
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as knowledge_file:
                knowledge_file.write(f"# {agent} 지식 베이스\n")

        with open(path, "r", encoding="utf-8") as knowledge_file:
            current = knowledge_file.read()

        marker = f"## {packet['title']}"
        if marker in current:
            continue

        entry = (
            f"\n\n## {packet['title']} ({now})\n"
            f"- Source: {COMMON_SOURCE}\n"
            f"- Tags: {packet['tags']}\n\n"
            f"{packet['content']}\n"
        )
        with open(path, "a", encoding="utf-8") as knowledge_file:
            knowledge_file.write(entry)
        print(f"updated {agent}: {path}")


if __name__ == "__main__":
    main()

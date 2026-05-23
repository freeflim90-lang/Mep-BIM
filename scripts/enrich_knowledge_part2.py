"""개발/QA/스토어/비즈니스 에이전트 지식 충전 - Part 2"""
import os, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
KB = PROJECT_ROOT / "data" / "knowledge_base"
KB.mkdir(parents=True, exist_ok=True)
NOW = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
SRC = "LUA BIM LABS domain knowledge baseline 2026-05-19"

PACKETS = {
    "Revit_Addin": [
        ("Revit API 핵심 패턴 및 Transaction 처리", "revit-api,transaction,csharp",
         """모든 모델 변경(요소 생성·수정·삭제)은 Transaction 내에서 실행해야 한다.
Transaction 패턴: using(var tx = new Transaction(doc, "작업명")) { tx.Start(); ... tx.Commit(); }
TransactionGroup: 여러 Transaction을 하나의 Undo 단위로 묶을 때 사용.
SubTransaction: Transaction 내부에서 부분 롤백 가능.
UI 업데이트(ExternalEvent)는 별도 IExternalEventHandler에서 처리하고 Idling 이벤트 남용 금지."""),
        ("Revit API 필터링 및 요소 수집 패턴", "revit-api,filter,collector",
         """FilteredElementCollector로 요소 수집 시 WhereElementIsNotElementType() 필수(타입 제외).
BuiltInCategory 필터: new ElementCategoryFilter(BuiltInCategory.OST_DuctCurves)
빠른 필터(Quick Filter) 먼저 적용 후 느린 필터(Slow Filter) 체이닝해 성능 최적화.
대형 모델(요소 10만↑)에서는 ElementId 배치 처리로 메모리 과부하 방지.
Linked 모델 요소 접근: RevitLinkInstance.GetLinkDocument()로 링크 문서 참조."""),
        ("Revit API 예외 처리 및 로깅 기준", "revit-api,exception,logging",
         """Autodesk.Revit.Exceptions.InvalidOperationException: 잘못된 API 호출 순서(Transaction 외부 변경 시도 등).
Autodesk.Revit.Exceptions.ArgumentNullException: null Document/Element 전달.
try-catch에서 Exception 타입을 구체적으로 잡고 사용자에게 TaskDialog로 안내.
로그 파일은 %AppData%\LUA BIM LABS\logs 에 날짜별 저장, 민감 데이터(모델 경로, 사용자 정보) 제외."""),
        ("Revit 리본 UI 구성 기준", "revit-api,ribbon,ui",
         """RibbonPanel은 IExternalApplication.OnStartup에서 생성, 탭명은 제품명으로 고정.
PushButton: 아이콘 32×32(large), 16×16(small) PNG, 배경 투명.
PulldownButton: 관련 기능 묶음, 최대 8개 이하.
ToolTip에 기능 설명 + 단축키 표기. 비활성 조건(AvailabilityClassName)으로 문서 없을 때 버튼 비활성화."""),
    ],
    "Navisworks_Addin": [
        ("Navisworks .NET API 기본 구조", "navisworks-api,plugin,dotnet",
         """Navisworks 플러그인 3가지 방식: AddInPlugin(메뉴 명령), DockPanePlugin(패널), ImporterPlugin(파일 임포터).
진입점: AddInPluginAttribute로 어셈블리 등록, Execute() 메서드에서 로직 실행.
Document 접근: Autodesk.Navisworks.Api.Application.ActiveDocument
모델 항목 순회: ModelItemCollection → ModelItem → PropertyCategoryCollection."""),
        ("Clash Detective API 활용 기준", "navisworks-api,clash,automation",
         """ClashTest 생성/실행: DocumentClash.TestsData.CreateClash() → ClashTest.Run()
결과 접근: ClashTest.ResultData.ClashResults (ClashResult 컬렉션)
ClashResult 주요 속성: Status(Active/Reviewed/Approved), Distance, Point1/Point2(충돌 좌표).
결과 Excel 내보내기: ClashResult를 순회해 OpenXML 또는 CSV로 직접 작성(Navisworks 내장 보고서보다 커스텀 필드 추가 용이)."""),
        ("Navisworks SearchSet 자동화 기준", "navisworks-api,searchset,selection",
         """SearchSet은 조건 기반 자동 선택 세트. SelectionSource → ConditionSource → Condition 계층 구조.
저장: document.SelectionSets.InsertCopy(savedItem) 후 NWF 저장으로 유지.
공종별 자동 SearchSet: 카테고리(Category)와 속성(Property) 조합으로 MEP 계통 자동 분류.
Add-in 실행 시 기존 SearchSet 중복 방지를 위해 이름 기준 중복 검사 후 덮어쓰기 옵션 제공."""),
    ],
    "요구사항분석": [
        ("BIM Add-in 요구사항 분해 템플릿", "requirements,user-story,scope",
         """요구사항 분해 구조:
1. 사용자 문제 (As a [역할], I want [기능], So that [가치])
2. 입력 데이터 (Revit 요소 타입, 파라미터명, 링크 모델 포함 여부)
3. 처리 로직 (필터 조건, 계산식, 판정 기준)
4. 출력 결과 (Revit 일람표, TaskDialog, Excel, 모델 마커)
5. 예외 조건 (빈 선택, 링크 모델 없음, 파라미터 누락, 지원 버전 외)
6. 지원 환경 (Revit 2023/2024/2025/2026, 언어, 라이선스 상태별 동작)"""),
        ("공정별 데이터 필드 표준", "requirements,data-fields,discipline",
         """충돌 보고서 공통 필드: 충돌ID, 우선순위, 공종1, 공종2, 레벨, 위치(X/Y/Z), 거리(mm), 상태, 담당자, 비고.
건축 추가 필드: 실명, 방화구획ID, 천장고 영향(mm).
구조 추가 필드: 부재명, 단면크기, 보강필요여부, 구조기술사확인.
MEP 공통 추가 필드: 계통명, 관경/덕트크기, 단열포함여부, 유지관리공간침해여부.
소방 추가 필드: 소방법조항, 소방서협의필요여부."""),
        ("스토어 제출용 요구사항 검토 기준", "requirements,store,review-risk",
         """Autodesk App Store 심사 거절 위험 요구사항:
- Revit/Navisworks 비공개 내부 API 사용 → 공식 API로 대체 설계 필수
- 외부 서버 통신 미고지 → 개인정보 정책 및 제품 설명에 명시
- 설치/제거 자동화 미지원 → MSI/번들 인스톨러 필수
- Revit 성능 저하(3초 이상 UI 블로킹) → 비동기(ExternalEvent/Task) 처리
요구사항 단계에서 이 항목들을 체크리스트로 검토 후 개발 범위에 반영한다."""),
    ],
    "빌드검증": [
        ("Revit 버전별 빌드 검증 체크리스트", "build,revit-version,smoke-test",
         """검증 대상 버전: Revit 2023(v23), 2024(v24), 2025(v25), 2026(v26).
각 버전별 확인 항목:
□ .addin 매니페스트 로드 (Revit 시작 시 오류 없음)
□ 리본 탭/패널/버튼 표시 확인
□ 샘플 건축 모델에서 주요 명령 1회 실행
□ Revit 정상 종료 (크래시 없음)
□ 제거 후 잔여 파일/레지스트리 없음
Release blocker: 크래시, 리본 미표시, 제거 실패, Revit 시작 지연 3초 이상."""),
        ("smoke test 자동화 방법론", "build,automation,test",
         """Revit Journal 파일 기반 자동 테스트: Journal 파일로 명령 시퀀스 재생.
단위 테스트: Revit 의존 로직은 인터페이스로 분리 후 Mock 사용(Moq 라이브러리).
통합 테스트: RevitTestFramework(RTF) 사용 — Revit 프로세스 내에서 NUnit 테스트 실행.
CI 파이프라인: MSBuild로 빌드 → RTF로 smoke test → 결과 JUnit XML 출력.
테스트 모델: 빈 프로젝트, 샘플 건축, 샘플 MEP, Workshared 모델 4종 최소 유지."""),
    ],
    "배포문서": [
        ("Revit Add-in 설치 경로 및 매니페스트 기준", "deployment,manifest,install-path",
         """설치 경로(시스템 전체): C:\\ProgramData\\Autodesk\\Revit\\Addins\\[버전]\\
설치 경로(사용자): %AppData%\\Autodesk\\Revit\\Addins\\[버전]\\
.addin 파일과 DLL은 같은 폴더 또는 .addin의 Assembly 태그에 전체 경로 명시.
버전별 폴더 분리 필수(2023, 2024, 2025, 2026). MSI 설치 시 각 버전 폴더에 자동 배포."""),
        ("사용자 배포 문서 필수 항목", "deployment,docs,user-guide",
         """설치 가이드 필수 내용:
1. 지원 제품/버전 목록 (Revit 2023~2026)
2. 설치 전 요구사항 (.NET 버전, WebView2 런타임 등)
3. 단계별 설치 화면 (스크린샷 포함)
4. 첫 실행 절차 (라이선스 활성화, 로그인 등)
5. 네트워크/방화벽 사용 여부 명시
6. 제거 방법 (Windows 앱 제거 + 잔여 폴더 안내)
7. 문제 해결 FAQ (설치 오류 코드별 해결책)
8. 지원 이메일 및 응답 기준 시간"""),
    ],
    "스토어심사": [
        ("Autodesk App Store 제출 체크리스트", "store,submission,checklist",
         """제출 전 필수 확인:
□ 제품명: Autodesk 상표 미포함, 고유하고 명확한 이름
□ 짧은 설명(255자): 핵심 가치와 지원 제품 버전 포함
□ 스크린샷: 실제 Revit/Navisworks 화면 최소 3장
□ 개인정보 처리방침 URL (외부 통신 없어도 필수)
□ 지원 이메일 주소
□ 지원 URL (FAQ/문서 페이지)
□ 버전 호환성: 최신 Autodesk 릴리스 포함 여부
□ 설치/제거 정상 동작 증빙
□ 가격 정책 및 환불 조건 명시"""),
        ("Autodesk App Store 심사 거절 사유 분류", "store,rejection,risk",
         """주요 거절 사유:
1. 제품 불안정 — 크래시, 심각한 지연, Revit 성능 저하
2. 설치/제거 불완전 — 제거 후 잔여 파일, 레지스트리 오염
3. 문서 불일치 — 설명과 실제 기능 차이, 스크린샷 불일치
4. 최신 버전 미지원 — 출시 연도 Revit 버전 미포함
5. 개인정보 미고지 — 외부 통신·데이터 수집 미기재
6. Autodesk 상표 위반 — 제품명·아이콘에 무단 사용
7. 유사 기능 중복 — 기존 Revit 기본 기능과 사실상 동일
심사 기간: 영업일 기준 5~15일. 거절 시 수정 후 재제출 가능."""),
    ],
    "제품패키징": [
        ("MSI 인스톨러 구성 기준", "packaging,msi,installer",
         """Revit Add-in MSI 구조:
- Product GUID: 버전마다 새 GUID 생성
- UpgradeCode: 제품 전체 라이프사이클 동안 고정
- 설치 폴더: Program Files\\[회사명]\\[제품명]
- Revit Addins 폴더 배포: CustomAction 또는 별도 Component로 각 버전 폴더에 복사
WiX Toolset 또는 Advanced Installer 사용 권장.
서명(Code Signing): EV 코드 서명 인증서로 DLL·MSI 서명 시 SmartScreen 경고 감소."""),
        ("패키지 버전 관리 기준", "packaging,versioning,release",
         """버전 체계: Major.Minor.Patch.Build (예: 1.2.3.456)
Major: 호환성 변경, Minor: 기능 추가, Patch: 버그 수정, Build: CI 빌드 번호.
AssemblyVersion과 FileVersion을 일치시키고 InformationalVersion에 브랜치/커밋 정보 포함.
스토어 제출 버전은 MSI 버전과 AssemblyFileVersion이 반드시 일치해야 한다.
업그레이드 시 이전 버전 자동 제거(MajorUpgrade 설정) 또는 병렬 설치 명시적 지원 여부 결정."""),
    ],
    "라이선스결제": [
        ("Autodesk Entitlement API 연동 기준", "license,entitlement,api",
         """Autodesk App Store 유료 앱은 Entitlement API로 구독 상태 검증.
엔드포인트: GET https://apps.autodesk.com/webservices/checkentitlement
파라미터: userid(Autodesk ID), appid(Store App ID)
응답: isValid(true/false), message
Add-in 시작 시 검증 → 실패 시 유료 기능 잠금 + 구매 페이지 링크 표시.
오프라인 시 마지막 검증 결과를 암호화해 로컬 캐시(최대 7일)로 허용."""),
        ("라이선스 상태별 UX 기준", "license,ux,freemium",
         """상태별 동작:
- 유효 구독: 전체 기능 활성화
- 체험판(Trial): 기능 제한 또는 실행 횟수 제한 + 업그레이드 안내
- 만료: 유료 기능 비활성화 + 갱신 링크
- 오프라인 캐시 유효: 전체 기능 허용 (캐시 기간 내)
- 오프라인 캐시 만료: 읽기 전용 모드 + 온라인 연결 안내
구독 갱신 버튼은 AppStore 제품 페이지 URL로 직접 연결한다."""),
    ],
    "고객지원 CS": [
        ("고객 문의 분류 및 대응 SLA", "support,sla,triage",
         """문의 분류:
P1 긴급 — 설치 후 Revit 크래시, 라이선스 전혀 작동 안 함 → 24시간 이내 응답
P2 높음 — 핵심 기능 오류, 결제 문제 → 48시간 이내 응답
P3 일반 — 기능 사용법, 호환성 문의 → 5영업일 이내 응답
P4 개선 — 기능 요청, 피드백 → 월간 배치 검토
응답 템플릿: 문의 수신 확인 → 환경 정보 요청(Revit 버전, OS, 제품 버전) → 재현 시도 → 해결/에스컬레이션."""),
        ("개인정보 처리방침 필수 항목", "support,privacy,gdpr",
         """수집 정보: 이메일(지원 문의 시), 결제 정보(Autodesk App Store 처리, 직접 수집 안 함).
외부 전송: AI 기능 사용 시 외부 API 호출 여부 명시. 고객 모델 데이터 전송 여부 명시.
데이터 보유: 지원 이메일 3년, 결제 기록 Autodesk가 관리.
삭제 요청: 이메일 수신 후 30일 이내 처리.
GDPR/개인정보보호법 준수 문구를 Autodesk App Store 제품 페이지와 지원 사이트에 동시 게재."""),
    ],
    "COO": [
        ("운영 KPI 및 릴리스 게이트 기준", "operations,kpi,release-gate",
         """릴리스 게이트 기준:
□ 빌드 검증: 지원 Revit 버전 전체 smoke test 통과
□ QA: P1/P2 버그 0건, P3 이하 알려진 이슈 문서화
□ 문서: 설치 가이드, 릴리스 노트, 스토어 설명 최신화
□ 법무: EULA, 개인정보 정책 검토 완료
□ 가격/결제: 구독 플랜 및 Entitlement 연동 테스트 완료
운영 KPI: 설치 성공률 95%↑, 지원 문의 응답 SLA 준수율 90%↑, 1개월 이내 환불률 5%↓."""),
        ("개발-출시-지원 사이클 관리", "operations,delivery,lifecycle",
         """Sprint 주기: 2주. 스토어 제출 주기: 분기 1회 이상.
개발 완료 → 내부 QA(1주) → 빌드 검증(2~3일) → 스토어 제출(심사 1~2주) → 출시.
긴급 패치: P1 버그 발생 시 핫픽스 브랜치 → 긴급 빌드 검증 → 스토어 업데이트 제출(심사 단축 요청 가능).
고객 피드백 → 제품 백로그 → 분기 로드맵 업데이트 사이클 운영."""),
    ],
    "CFO": [
        ("Autodesk App Store 수익 구조 및 비용 분석", "finance,revenue,cost",
         """수익: Autodesk App Store 판매 → Autodesk 수수료 공제 후 publisher에게 지급(수수료율 비공개, 30~40% 추정).
비용 항목: 개발비(인건비), 코드 서명 인증서(EV 연간 $300~500), 도메인/호스팅, 지원 운영비.
손익분기점 계산: (월 개발+운영 비용) / (월 구독 수익 × (1-수수료율))
MRR $1,000 목표: Individual $19/월 기준 약 53명 유료 전환 필요.
초기 3개월: 수익보다 설치 수·리뷰 수·지원 비용을 지표로 관리."""),
        ("세금 및 결제 처리 기준", "finance,tax,payment",
         """Autodesk App Store 결제: BlueSnap 또는 PayPal 처리 (publisher 직접 관여 안 함).
VAT/부가세: 구매자 국가 기준 Autodesk가 처리.
Publisher 수익 정산: 월별 정산, 최소 지급액($50) 이상 시 지급.
한국 법인 세금: 해외 플랫폼 수익은 외화 수입 → 환전 시 외화 수입 계좌 별도 관리 권장.
개발비 비용 처리: 소프트웨어 개발비 무형자산 처리 또는 즉시 비용화(회계 정책 결정 필요)."""),
    ],
    "경영지원": [
        ("Autodesk Publisher 계정 운영 기준", "admin,autodesk-publisher,account",
         """Autodesk App Store Publisher 계정: apps.autodesk.com에서 Publisher 등록.
필수 정보: 회사명, 주소, 지원 이메일, 개인정보 정책 URL, 결제 계좌.
제품 관리: 버전 업데이트, 설명 수정, 가격 변경은 Publisher Dashboard에서 직접 처리.
계정 보안: 2FA 필수 활성화, 접근 권한은 최소화(Owner 1명 + Developer 최대 2명).
브랜드 자산: 로고, 스크린샷, 소개 영상을 버전 관리하여 제출 이력 유지."""),
        ("계약·청구·행정 운영 기준", "admin,contract,billing",
         """외주 개발 계약: 소스코드 소유권(work-for-hire), 납품물 목록, 비밀유지(NDA), 하자보수 기간 명시.
청구서: 발행 후 30일 이내 지급 조건, 세금계산서 발행(부가세 별도).
지원 이메일 계정: support@[도메인] 운영, 티켓 시스템(Freshdesk 또는 Gmail 레이블) 연동.
법인 문서 보관: 계약서, 세금계산서, 정산서를 연도별 폴더로 5년 이상 보관."""),
    ],
    "법무조항검토": [
        ("EULA 핵심 조항 기준", "legal,eula,terms",
         """EULA 필수 조항:
1. 라이선스 범위: 구독 기간 내 지정 사용자 1인 사용 허용(비독점, 비양도)
2. 금지 행위: 역공학, 소스코드 추출, 재배포, 서브라이선스 금지
3. 책임 제한: 소프트웨어 결함으로 인한 간접 손해 배상 제외, 최대 배상액 = 구독료 3개월치
4. 지식재산권: 소프트웨어 및 문서의 모든 IP는 판매자 소유
5. 업데이트/지원: 구독 기간 내 업데이트 제공, 지원 응답 SLA 명시
6. 계약 해지: 약관 위반 시 즉시 해지 가능"""),
        ("제3자 라이브러리 라이선스 검토 기준", "legal,third-party,license",
         """라이선스 유형별 상용 판매 가능 여부:
- MIT/BSD/Apache 2.0: 상용 사용 허용, 저작권 고지 필요
- LGPL: DLL 링크 방식으로 사용 시 허용, 수정 배포 시 소스 공개 필요
- GPL: 소스 공개 의무 발생 → 상용 Add-in에 사용 금지
- 독점 라이선스: 계약서 확인 후 사용 범위 준수
Revit/Navisworks API 자체는 Autodesk 이용약관 준수 필수(상용 재배포 허용, 비공개 API 사용 금지)."""),
        ("Autodesk 상표 사용 가이드라인", "legal,trademark,autodesk",
         """허용: "Works with Autodesk Revit®" 문구 사용 (® 필수 표기)
허용: 지원 제품 목록에 Revit, Navisworks 명칭 나열
금지: 제품명에 Autodesk, Revit, Navisworks 포함 (예: "Revit Clash Pro" → 금지)
금지: Autodesk 로고·아이콘 사용
금지: Autodesk 공식 제품으로 오인될 수 있는 마케팅 표현
위반 시 스토어 심사 거절 및 계정 정지 가능."""),
    ],
    "견적심사원": [
        ("BIM Add-in 개발 공수 산정 기준", "estimate,effort,complexity",
         """기능 복잡도 등급:
L1 단순(1~3일): UI 없는 단일 명령, 기존 Revit API 조합
L2 보통(3~10일): 커스텀 UI(WPF/WinForms), 복수 카테고리 필터링, Excel 출력
L3 복잡(10~30일): 실시간 모델 감시(DocumentChanged), 링크 모델 처리, 외부 서버 연동
L4 대형(30일↑): 전체 MEP 협의 워크플로우, Entitlement API 연동, 다국어 지원
추가 공수: 버전별 빌드 테스트 각 0.5일, MSI 패키징 2일, 스토어 문서 2일, QA 전체 기능의 20%."""),
        ("견적 리스크 및 일정 버퍼 기준", "estimate,risk,schedule",
         """일정 버퍼: 순 개발 공수의 30% 추가 (Revit API 환경 변수, 고객 피드백 반영 포함).
리스크 요인:
- 지원 Revit 버전 추가 요청: 버전당 +0.5~1일
- 링크 모델 처리: +20~30%
- 비공개 API 요구 → 공식 API 대체 개발 필요 시 +50% 이상
- 고객 모델 특수 구조(패밀리 명명 비표준): +10~20%
견적서에 '지원 버전'과 '제외 범위'를 명확히 기재해 추가 요청 발생 시 변경 견적으로 처리한다."""),
    ],
    "견적서담당": [
        ("BIM Add-in 견적서 항목 분류", "quote,scope,breakdown",
         """견적 항목 구조:
1. 기본 개발 (기능별 단가 × 수량)
2. 지원 버전 추가 (Revit 버전당 단가)
3. UI/UX 디자인 (WPF 화면 수 × 단가)
4. 테스트 및 QA (전체 개발비의 15~20%)
5. MSI 패키징 및 배포 자동화 (고정 단가)
6. 스토어 제출 지원 (문서 작성 포함, 고정 단가)
7. 라이선스/Entitlement 연동 (선택, 고정 단가)
8. 유지보수 (연간, 개발비의 15~20%)
VAT 별도 표기 필수."""),
        ("견적서 법적 효력 요건", "quote,legal,validity",
         """견적서 유효 기간: 발행 후 30일(명시 필수).
서명/날인: 견적 확정 시 양측 서명 또는 이메일 서면 승인으로 계약 효력 발생.
범위 변경: 서면(이메일 포함) 합의로만 변경 가능 → 변경 견적서 재발행.
지급 조건: 착수금 30~50%, 중간 40%, 납품 완료 10~20% 분할 지급 권장.
환불: 착수 후 취소 시 착수금 반환 불가 조항 명시."""),
    ],
    "글로벌_유통기획관": [
        ("Autodesk App Store 글로벌 출시 기준", "distribution,global,localization",
         """우선 출시 언어: 영어(필수) + 한국어(선택적 병행).
영문 스토어 설명: 제목 60자 이내, 본문 500~1000자, 키워드 5~10개.
가격: USD 기준으로 설정 → Autodesk가 현지 통화 자동 변환.
지역별 결제 제한: 일부 국가는 App Store 결제 지원 안 됨 (사전 확인 필요).
마케팅 채널: LinkedIn(BIM 전문가), YouTube(기능 데모), Autodesk Community 포럼."""),
        ("현지화 우선순위 기준", "distribution,localization,priority",
         """1순위 현지화: 영어(필수) — 스토어 설명, UI 텍스트, 오류 메시지
2순위: 한국어 — 국내 BIM 시장 타겟
3순위: 일본어 — Revit 사용 건설사 비중 높음
4순위: 중국어(간체) — 대형 시장, 별도 규정 검토 필요
UI 현지화: Revit Add-in에서 System.Globalization.CultureInfo로 언어 감지 후 리소스 파일 로드.
스토어 설명 번역: 기계 번역 후 현지 BIM 전문가 검수 필수."""),
    ],
    "글로벌_매출관리원": [
        ("App Store 판매 지표 관리 기준", "revenue,metrics,analytics",
         """주요 지표:
- MRR (Monthly Recurring Revenue): 구독 수 × 월 단가
- 체험판 → 유료 전환율: 목표 15~25%
- 월간 해지율(Churn Rate): 3% 이하 목표
- 고객 획득 비용(CAC): 마케팅비 / 신규 유료 고객 수
- LTV (Life Time Value): 평균 구독 기간 × 월 단가
Autodesk App Store 대시보드에서 다운로드 수, 리뷰 수, 평점 주간 모니터링."""),
        ("매출 성장 전략 기준", "revenue,growth,upsell",
         """업셀 경로: Individual → Team 5-Pack → Enterprise 직접 판매.
Cross-sell: Revit Add-in 구매 고객에게 Navisworks Add-in 번들 할인 제공.
리뷰 전환: 설치 30일 후 in-app 리뷰 요청 (TaskDialog로 구현).
갱신율 향상: 만료 30/7/1일 전 이메일 알림 + 갱신 할인 쿠폰.
국가별 매출 비중이 30% 이상인 국가는 현지화 투자 대상으로 검토."""),
    ],
    "브랜드마케팅": [
        ("Autodesk App Store 리스팅 최적화 기준", "marketing,aso,listing",
         """제목: 핵심 키워드 앞에 배치 (예: "BIM Clash Coordinator for Revit")
키워드: "Revit Add-in", "MEP Coordination", "Clash Detection", "BIM Productivity" 등 포함.
짧은 설명: 첫 2문장에 핵심 문제 해결 가치 명시.
스크린샷 구성: 1-before/after, 2-주요 기능 UI, 3-보고서 출력, 4-설치 화면.
리뷰 평점 4.0↑ 유지: 낮은 평점 리뷰에 24시간 내 공개 응답 필수."""),
        ("BIM 전문가 타겟 마케팅 채널", "marketing,channel,bim",
         """LinkedIn: BIM Manager, MEP Engineer, Revit Specialist 직함 타겟팅.
YouTube: 3분 이내 기능 데모 영상 (영어 자막 필수).
Autodesk Community: forums.autodesk.com Revit API 포럼에 솔루션 제공 후 제품 링크.
BIM 컨퍼런스: AU(Autodesk University), BIMWORLD 참가 또는 스폰서.
무료 체험 → 리뷰 → 구매 퍼널: 체험판 사용자에게 30일 후 만족도 조사 이메일 발송."""),
    ],
    "테크니컬_라이터": [
        ("기술 문서 작성 기준", "docs,technical-writing,style",
         """문서 구조: 개요(무엇을 하는가) → 전제조건 → 단계별 절차 → 결과 확인 → 문제 해결.
문장 원칙: 능동태, 2문장 이내로 단락 나누기, 전문 용어는 최초 사용 시 정의.
스크린샷: 실제 제품 화면, 주요 UI 요소에 번호 레이블, 해상도 1920×1080 기준.
버전 관리: 문서 헤더에 "적용 버전: Revit 2023~2026, 제품 v1.x" 표기.
릴리스 노트 형식: 새 기능 / 개선 / 버그 수정 / 알려진 문제 섹션 분리."""),
        ("사용자 가이드 필수 섹션", "docs,user-guide,structure",
         """1. 빠른 시작 (Quick Start): 설치 → 첫 실행 → 핵심 기능 1가지 사용
2. 기능 레퍼런스: 각 명령별 입력·처리·출력·제한 사항
3. 워크플로우 예시: 실제 프로젝트 시나리오 기반 단계별 가이드
4. 문제 해결(Troubleshooting): 오류 코드별 해결 방법
5. FAQ: 가장 많이 받는 질문 10개
6. 릴리스 노트: 버전별 변경 이력
7. 지원 연락처: 이메일, 응답 시간, 지원 시간대"""),
    ],
    "프로그램개발": [
        ("C# .NET Add-in 아키텍처 기준", "development,csharp,architecture",
         """레이어 구조:
- Presentation: WPF ViewModel + View (MVVM 패턴)
- Application: Command 클래스 (IExternalCommand 구현)
- Domain: 비즈니스 로직 (Revit API 비의존 순수 C# 클래스)
- Infrastructure: Revit API 호출, 파일 I/O, 외부 서버 통신
의존성 방향: Presentation → Application → Domain ← Infrastructure
테스트 가능성: Domain 레이어는 Revit 없이 단위 테스트 가능하도록 설계."""),
        ("성능 최적화 기준", "development,performance,optimization",
         """대형 모델(요소 10만↑) 처리 시 UI 스레드 블로킹 방지:
- ExternalEvent + IExternalEventHandler로 비동기 처리
- FilteredElementCollector 결과를 ElementId 리스트로 먼저 수집 후 배치 처리
- 진행 상황 표시: ProgressBar를 Modeless Dialog로 표시
메모리 관리: Revit API 객체는 사용 후 즉시 참조 해제, List 대신 IEnumerable 활용.
시작 시간 최적화: OnStartup에서 무거운 초기화 금지 → Lazy Loading 패턴 사용."""),
    ],
    "QA_테스터": [
        ("Revit Add-in QA 테스트 케이스 분류", "qa,test-cases,revit",
         """테스트 케이스 분류:
TC-INSTALL: 설치/제거/업그레이드 (각 지원 Revit 버전별)
TC-LOAD: Revit 시작 시 Add-in 로드, 리본 표시
TC-FUNC: 각 기능별 정상 동작 (샘플 모델 기준)
TC-EDGE: 엣지 케이스 (빈 문서, 선택 없음, 링크 모델 없음, 파라미터 누락)
TC-PERF: 대형 모델(요소 5만↑)에서 실행 시간 측정 (3초 이내 기준)
TC-SECURITY: 라이선스 우회 시도, 오프라인 동작 검증"""),
        ("버그 보고서 작성 기준", "qa,bug-report,format",
         """버그 보고서 필수 항목:
1. 제목: [TC-FUNC-001] 공조덕트 충돌 감지 시 NullReferenceException 발생
2. 심각도: Critical/High/Medium/Low
3. 재현 환경: Revit 버전, OS, .NET 버전, Add-in 버전
4. 재현 단계: 번호 있는 단계별 절차 (스크린샷 포함)
5. 예상 결과 vs 실제 결과
6. 로그 파일 첨부 (관련 스택 트레이스)
7. 회귀 여부: 이전 버전에서 정상 동작 여부"""),
    ],
    "테크니컬_라이터": [
        ("릴리스 노트 작성 기준", "docs,release-notes,changelog",
         """릴리스 노트 섹션:
🆕 새 기능: 사용자 관점에서 무엇이 가능해졌는지 서술
🔧 개선: 기존 기능의 성능·UX 향상 내용
🐛 버그 수정: 수정된 문제와 영향 범위
⚠️ 알려진 문제: 해결 예정 이슈와 회피 방법
💥 호환성 변경: 이전 버전과 달라진 동작
버전 번호와 출시 날짜 필수 표기. 내부 이슈 번호(#123)는 외부 문서에 미노출."""),
    ],
    "라이선스_보안관": [
        ("보안 취약점 체크리스트", "security,checklist,addin",
         """코드 보안 점검:
□ DLL에 하드코딩된 API 키·비밀번호 없음 (strings 명령어 또는 dotPeek로 확인)
□ 외부 HTTP 통신 시 HTTPS(TLS 1.2↑) 필수, 인증서 검증 우회 코드 없음
□ 로그 파일에 고객 모델 데이터·개인정보 미포함
□ 임시 파일은 %TEMP% 사용 후 종료 시 삭제
□ 레지스트리에 민감 정보 저장 금지
□ 라이선스 키·활성화 코드는 서버 측 검증 또는 Autodesk Entitlement API 사용"""),
    ],
    "프롬프트엔지니어": [
        ("BIM Add-in 개발 프롬프트 설계 기준", "prompt,agent,workflow",
         """효과적인 프롬프트 구조:
1. 역할 명시: "당신은 [에이전트명] 전문가입니다"
2. 컨텍스트 주입: 관련 지식 베이스 섹션 (최대 2,000자)
3. 작업 명세: 입력 데이터 + 기대 출력 형식
4. 제약 조건: 제외 범위, 금지 표현, 출력 길이
5. 예시 (Few-shot): 유사 케이스 1~2개
토큰 절감: 지식 베이스는 관련도 상위 3섹션만 주입, 중복 제거, 표 형식 활용."""),
    ],
    "Caveman_토큰다이어터": [
        ("컨텍스트 압축 전략", "token,compression,context",
         """압축 우선순위:
1. 핵심 수치·기준만 추출 (서술형 → 표/목록 변환)
2. 반복 용어 약어화 (공조배관=HVAC-P, 스프링클러=SPK)
3. 예시는 1개만 유지, 나머지 패턴 언급으로 대체
4. 출처/날짜 메타 정보는 첫 섹션만 유지
5. 결론 문장을 첫 줄에 배치 (bottom-up → top-down)
지식 베이스 청크 크기: 에이전트당 최대 1,500자로 제한.
프롬프트 길이 목표: 시스템+지식 2,000자 이내, 사용자 요청 500자 이내."""),
    ],
    "BIM_템플릿기획관": [
        ("공유 파라미터 표준 설계 기준", "bim-template,shared-parameter,revit",
         """공유 파라미터 파일 관리: 프로젝트 서버 또는 BIM 360/ACC에 단일 파일 버전 관리.
파라미터 명명: [공종]_[항목명]_[단위] (예: MEP_관경_mm, STR_보강필요여부)
카테고리 배정: 해당 패밀리 카테고리에만 배정 (전체 카테고리 배정 금지)
데이터 타입: 수치는 Length/Area/Volume 타입 사용 (텍스트 수치 금지)
Add-in이 읽는 파라미터는 모두 공유 파라미터로 표준화하여 프로젝트 간 이식성 확보."""),
        ("뷰 템플릿 및 필터 기준", "bim-template,view-template,filter",
         """공종별 협의도 뷰 템플릿: 구조 협의(구조+건축 가시), MEP 협의(MEP+구조 가시).
필터 규칙: 계통별 색상 코드 고정 (공조배관=파랑, 소방=빨강, 전기=노랑, 통신=초록).
Add-in 보고서 뷰: 별도 3D 뷰 자동 생성 → 충돌 마커만 표시.
패밀리 명명: [공종]_[기능]_[규격] (예: MEP_배관_DN100, STR_보_H300×150)."""),
    ],
    "엔지니어링계산서": [
        ("MEP 엔지니어링 계산서 필수 항목", "engineering,calculation,mep",
         """공조 부하 계산: 냉방 부하(W/㎡), 난방 부하(W/㎡), 환기량(m³/h·인).
위생 배수 계산: 배수 부하 단위(DFU), 관경 선정 테이블 적용, 구배별 유속 검증.
전기 부하 계산: 설비 용량 합계, 수용률 적용 후 계약 전력, 변압기 용량 선정.
소방 살수 계산: 헤드 수 × 방수량(80L/min) × 최소 20분 = 저수조 용량.
Add-in 보고서에 계산 근거 수치(공식·입력값·결과값)를 포함해야 설계 검토에 활용 가능."""),
    ],
    "외주관리": [
        ("외주 개발 계약 및 검수 기준", "outsourcing,contract,acceptance",
         """계약서 필수 항목: 작업 범위(SOW), 납품물 목록, 일정, 단가/지급 조건, IP 소유권(work-for-hire), NDA, 하자 보수(3개월 이상).
납품물 검수 기준:
□ 소스코드 저장소 접근 권한 이전
□ 빌드 재현 가능 (README 기준 빌드 성공)
□ 단위 테스트 커버리지 60%↑
□ 지원 Revit 버전 smoke test 통과
□ 문서(설치 가이드, API 명세) 완비
하자 발생 시 원 개발사 우선 수정 의무, 10영업일 내 미이행 시 대금 보류 조항 삽입."""),
    ],
    "협력사안부": [
        ("협력사 관리 및 보안 기준", "partner,vendor,security",
         """협력사 분류: 외주 개발사, BIM 컨설턴트, 현장 검토 파트너, 기술지원 에이전트.
보안 기준: 고객 프로젝트 모델 공유 금지. 테스트 전용 더미 모델만 제공.
협력사 접근 권한: 최소 권한 원칙. 작업 종료 후 즉시 접근 해제.
납기 관리: 주간 진행 보고 + Milestone 기준 지급. 납기 지연 시 페널티 조항 명시.
품질 기준: 납품물은 사내 검수 기준(smoke test + 코드 리뷰) 통과 후 최종 수락."""),
    ],
    "파이프라인_오케스트레이터": [
        ("Add-in 개발 파이프라인 단계 정의", "pipeline,workflow,automation",
         """파이프라인 단계:
1. 요청 접수: 기능 요청 → 우선순위 분류 (CEO/COO 승인)
2. 요구사항 분석: 공종 지식 반영 + 스토어 리스크 체크 (요구사항분석 에이전트)
3. 개발: C#/.NET 구현 + 단위 테스트 (프로그램개발 에이전트)
4. QA: 버전별 smoke test + 버그 수정 (QA_테스터 에이전트)
5. 빌드 검증: MSI 패키징 + 설치/제거 테스트 (빌드검증 에이전트)
6. 스토어 제출: 문서 작성 + 체크리스트 + 제출 (스토어심사 에이전트)
7. 출시 후 지원: 고객 문의 대응 + 지식 베이스 업데이트 (고객지원 CS 에이전트)"""),
    ],
    "지식업데이트": [
        ("지식 베이스 업데이트 운영 기준", "knowledge,governance,curation",
         """업데이트 트리거:
- 현장 피드백 (고객 문의에서 반복되는 패턴)
- Autodesk 공식 문서 변경 (API 업데이트, 스토어 정책 변경)
- 법규 개정 (소방법, 건축법, KEC)
- 내부 프로젝트 완료 후 교훈(Lessons Learned)
업데이트 형식: 섹션 제목에 날짜 + 출처 + 태그 필수. 이전 내용 삭제 금지(추가만).
검증: 수치·법규 기준은 출처 URL 또는 문서명 명시. 추정값은 "(추정)" 표기.
주기: 월 1회 전체 검토, 법규 변경 시 즉시 업데이트."""),
    ],
    "아이디어발굴": [
        ("BIM Add-in 아이디어 발굴 프레임워크", "ideation,bim,pain-point",
         """Pain Point 수집 채널:
1. Autodesk Community 포럼 — 반복 질문 패턴 분석
2. Revit API 개발자 그룹 (LinkedIn/Facebook) — 미해결 기능 요청
3. BIM 프로젝트 현장 인터뷰 — 수작업 반복 업무 목록화
4. 경쟁 제품 리뷰 — 낮은 평점 리뷰의 불만 사항
MVP 선정 기준: 반복 빈도(주 3회↑) × 절감 시간(30분↑/회) × Revit API 구현 가능성(L1~L2)
우선 제외: API 불가 기능, 기존 Revit 기본 기능과 95% 이상 중복."""),
    ],
    "전략기획": [
        ("BIM Add-in 제품 로드맵 기준", "strategy,roadmap,mvp",
         """로드맵 단계:
MVP (0~3개월): 1개 핵심 기능, 스토어 제출, 첫 유료 고객 10명
v1.1 (3~6개월): 피드백 반영 개선 + 기능 1개 추가, 리뷰 20개↑
v2.0 (6~12개월): Pro 기능 추가, 팀 플랜 도입, 2번째 Add-in 출시 준비
기능 우선순위 기준: 고객 요청 빈도 × 개발 공수 역수 × 스토어 경쟁 강도 역수
로드맵은 분기별 검토 → CEO/COO 승인 → 공개 릴리스 노트에 예고."""),
    ],
    "프로젝트분석": [
        ("BIM 프로젝트 Add-in 적용 가능성 분석 기준", "project-analysis,bim,feasibility",
         """분석 항목:
1. 대상 프로젝트 유형: 건축/토목/플랜트/인프라 (Revit 사용 비중)
2. BIM 성숙도: LOD 200~400 여부, 공유 파라미터 표준화 수준
3. 반복 업무 목록: 주간 수작업 시간 합계 > 2시간인 업무
4. 데이터 품질: 패밀리 명명 표준화, 파라미터 입력 완성도
5. 이해관계자: BIM 코디네이터, MEP 엔지니어, 발주처 BIM 요구사항
분석 결과를 요구사항분석 에이전트에 전달하여 Add-in 기능 정의 시작."""),
    ],
    "CS_기술지원관": [
        ("Revit Add-in 기술지원 진단 절차", "technical-support,diagnostics,troubleshoot",
         """1차 진단 (고객 자가 확인):
□ Revit 버전 확인 (About Revit)
□ Add-in 버전 확인 (About 메뉴)
□ Windows 이벤트 뷰어 → 응용 프로그램 오류 확인
□ %AppData%\\LUA BIM LABS\\logs\\ 에서 최신 로그 파일 첨부
2차 진단 (기술지원팀):
□ 샘플 모델로 재현 시도
□ 다른 Revit 모델에서 동일 오류 여부
□ Add-in 재설치 후 재현 여부
□ 다른 Add-in 비활성화 후 충돌 여부 확인"""),
    ],
    "인프라_DevOps (Obsidian)": [
        ("로컬 인프라 운영 기준", "devops,local,obsidian",
         """환경 변수 관리: .env 파일에 저장, .gitignore에 반드시 포함. 절대 저장소 커밋 금지.
지식 베이스 백업: data/knowledge_base/ 폴더를 주 1회 외부 저장소(Git 또는 클라우드) 백업.
로그 관리: logs/ 폴더 90일 이상 로그 자동 삭제 (launchd 또는 cron 설정).
서버 모니터링: uvicorn 프로세스 죽으면 자동 재시작 (launchd plist 설정).
Obsidian Vault 동기화: iCloud 또는 Obsidian Sync로 Mac 간 동기화."""),
    ],
    "EIRBEP_심사원": [
        ("EIR/BEP 핵심 요구사항 검토 기준", "eir,bep,bim-requirements",
         """EIR (Employer's Information Requirements) 검토 항목:
□ LOD(Level of Development) 단계별 요구사항 (설계 LOD200, 시공 LOD350, 준공 LOD400)
□ LOI(Level of Information) — 각 단계별 필수 파라미터 목록
□ 명명 규칙: 파일명, 레이어명, 패밀리명, 파라미터명 형식
□ 좌표계: 프로젝트 기준점, 측량 기준점, 공유 좌표 설정 방식
□ 납품 형식: RVT, IFC, NWD, PDF, Excel 지정 버전

BEP (BIM Execution Plan) 검토 항목:
□ 팀별 역할·책임(RACI) 명확화
□ 소프트웨어 버전 통일 (Revit 연도 버전 고정)
□ 협업 플랫폼: BIM 360/ACC 워크스페이스 설정
Add-in 기능이 EIR 파라미터 명명 규칙과 불일치하면 현장 적용 불가 → 공유 파라미터 매핑 기능 필요."""),
    ],
}

def safe_name(agent):
    return "".join(c for c in agent if c.isalnum() or c in ("_", "-"))

def append_if_missing(agent, title, tags, content):
    path = KB / f"{safe_name(agent)}.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if f"## {title}" in existing:
        return False
    if not existing:
        path.write_text(f"# {agent} 지식 베이스\n", encoding="utf-8")
    entry = f"\n\n## {title} ({NOW})\n- Source: {SRC}\n- Tags: {tags}\n\n{content.strip()}\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)
    return True

added = 0
for agent, sections in PACKETS.items():
    for title, tags, content in sections:
        if append_if_missing(agent, title, tags, content):
            print(f"  ✅ {agent} → {title}")
            added += 1
        else:
            print(f"  ⏭  {agent} → (이미 존재)")

print(f"\nPart 2 완료: {added}개 섹션 추가")

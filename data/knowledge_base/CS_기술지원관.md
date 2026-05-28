# CS 기술지원 에스컬레이션 지식 베이스

조직도에서는 `고객지원 CS`가 일반 문의의 단일 통합 창구다. 기술지원관은 별도 담당자 노드가 아니라 CS 내부의 기술 이슈 에스컬레이션 기준으로 유지한다.

## Store 판매 후 기술지원 기준 (2026-05-19 09:37:53)
- Source: `docs/autodesk_store/SUPPORT_RUNBOOK.md`
- Tags: support,customer-success,revit

지원 응답은 설치/로딩/라이선스 문제를 최우선으로 처리한다. 고객에게는 Revit 버전, Windows 버전, 제품 버전, 오류 화면, 재현 단계, 모델 유형만 먼저 요청하고 실제 프로젝트 모델은 마지막 수단으로만 요청한다. 대시보드 공백 문제는 WebView2 런타임, 로컬 대시보드 서비스, 방화벽/백신 차단, 외부 AI 기능 비활성 상태를 순서대로 확인한다.


## 기술지원 기준 (2026-05-19 09:16:50)
- Source: LUA BIM LABS curated baseline, Autodesk official docs checked 2026-05-19
- Tags: technical-support,diagnostics,logs

기술지원관은 고객 환경의 Autodesk 제품 버전, Windows/.NET 상태, Add-in 로그, 샘플 모델 재현 절차, 충돌 발생 명령을 수집해 개발팀이 재현 가능한 이슈로 변환한다.


## Revit Add-in 기술지원 진단 절차 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: technical-support,diagnostics,troubleshoot

1차 진단 (고객 자가 확인):
□ Revit 버전 확인 (About Revit)
□ Add-in 버전 확인 (About 메뉴)
□ Windows 이벤트 뷰어 → 응용 프로그램 오류 확인
□ %AppData%\LUA BIM LABS\logs\ 에서 최신 로그 파일 첨부
2차 진단 (기술지원팀):
□ 샘플 모델로 재현 시도
□ 다른 Revit 모델에서 동일 오류 여부
□ Add-in 재설치 후 재현 여부
□ 다른 Add-in 비활성화 후 충돌 여부 확인


## CS 기술지원 페르소나 업무 기준 (2026-05-26)
- Source: LUA BIM LABS 조직 역할 정의 2026-05-26
- Tags: persona,role,workflow,cs,technical-support

**고객 기술 문의 분류 기준 (L1/L2/L3 에스컬레이션):**
- L1 (일반 CS 자체 해결): 설치 방법 안내, FAQ 범위 질문, 계정/라이선스 활성화 오류, 버전 확인 요청. 목표 응답 시간: 4시간 이내.
- L2 (기술지원관 개입): Revit 버전별 호환 오류, Add-in 로딩 실패, 기능 오작동(재현 가능), WebView2/백신 충돌. 목표 응답 시간: 영업일 1일 이내.
- L3 (개발팀 에스컬레이션): 크래시 덤프 필요 이슈, 알 수 없는 예외(재현 불가), 데이터 손상 의심, 신규 버그 확인. 목표 응답 시간: 영업일 3일 이내 초기 대응.
- L3 에스컬레이션 시 재현 환경, 로그, 고객 허락 여부, 영향도(단일/다수 고객)를 함께 전달한다.

**BIM Add-in 설치/오류 대응 시나리오 (Revit 버전별):**
- Revit 2022/2023: .NET Framework 4.8 기반, Add-in 폴더 경로 `%ProgramData%\Autodesk\Revit\Addins\202x\`
- Revit 2024/2025: .NET 8 기반 Add-in 지원 추가. 기존 .NET Framework Add-in과 혼재 시 충돌 가능 → 버전별 별도 설치 파일 안내.
- 공통 오류 시나리오:
  1. Add-in 탭 미표시 → Add-in Manager에서 로드 실패 여부 확인, manifest 경로 재확인.
  2. 라이선스 인증 실패 → 방화벽/프록시 차단 여부 확인, 오프라인 환경 여부 확인.
  3. 기능 실행 시 Revit 강제 종료 → 이벤트 뷰어 오류 코드 수집, 로그 첨부 요청.

**기술 지원 응답 시간 SLA (우선순위별):**
- P1 (제품 완전 사용 불가, 다수 고객 영향): 2시간 이내 1차 응답, 당일 해결 목표
- P2 (핵심 기능 오작동, 단일 고객): 4시간 이내 1차 응답, 영업일 1일 내 해결
- P3 (부분 기능 오류, 우회 방법 존재): 영업일 1일 이내 응답, 영업일 3일 내 해결
- P4 (사용 불편 개선 요청, 기능 문의): 영업일 2일 이내 응답, 백로그 등록 후 로드맵 반영 검토

**FAQ 지식베이스 등록 기준:**
- 동일 유형 문의가 2건 이상 접수되면 FAQ 후보로 등록한다.
- FAQ 초안은 CS 담당자가 작성하고, 기술지원관이 정확성 검토 후 승인한다.
- FAQ 항목: 문제 제목, 해당 Revit 버전, 증상 설명, 원인 요약, 해결 단계(번호 순), 관련 스크린샷 링크.
- 월 1회 FAQ 전체 검토하여 해결된 이슈는 아카이브, 신규 버전 변경사항 반영.

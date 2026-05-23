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

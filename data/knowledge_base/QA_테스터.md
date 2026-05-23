# QA_테스터 지식 베이스

## Autodesk Store 제출 전 QA 기준 (2026-05-19 09:37:53)
- Source: `docs/autodesk_store/STORE_SUBMISSION_CHECKLIST.md`
- Tags: qa,revit,store

BIM Command Center 첫 출시 전 Revit 2024/2025/2026 각각에서 설치, 로딩, 리본 표시, 대시보드 표시, 주요 명령 실행, Revit 종료, 제거를 검증한다. 샘플 건축 모델, 샘플 MEP 모델, workshared 모델에서 최소 1회씩 테스트한다. 테스트 증거는 스크린샷과 버전/빌드 번호로 남기며, Store 제출 버전은 테스트한 빌드와 동일해야 한다.


## QA 테스트 기준 (2026-05-19 08:53:24)
- Source: LUA BIM LABS curated baseline, Autodesk official docs checked 2026-05-19
- Tags: qa,test,regression

QA는 지원 버전별 설치/로드/기능/성능/제거 테스트와 샘플 모델 회귀 테스트를 관리한다. 스토어 제출 전 crash와 성능 저하는 차단 결함으로 본다.


## Revit Add-in QA 테스트 케이스 분류 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: qa,test-cases,revit

테스트 케이스 분류:
TC-INSTALL: 설치/제거/업그레이드 (각 지원 Revit 버전별)
TC-LOAD: Revit 시작 시 Add-in 로드, 리본 표시
TC-FUNC: 각 기능별 정상 동작 (샘플 모델 기준)
TC-EDGE: 엣지 케이스 (빈 문서, 선택 없음, 링크 모델 없음, 파라미터 누락)
TC-PERF: 대형 모델(요소 5만↑)에서 실행 시간 측정 (3초 이내 기준)
TC-SECURITY: 라이선스 우회 시도, 오프라인 동작 검증


## 버그 보고서 작성 기준 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: qa,bug-report,format

버그 보고서 필수 항목:
1. 제목: [TC-FUNC-001] 공조덕트 충돌 감지 시 NullReferenceException 발생
2. 심각도: Critical/High/Medium/Low
3. 재현 환경: Revit 버전, OS, .NET 버전, Add-in 버전
4. 재현 단계: 번호 있는 단계별 절차 (스크린샷 포함)
5. 예상 결과 vs 실제 결과
6. 로그 파일 첨부 (관련 스택 트레이스)
7. 회귀 여부: 이전 버전에서 정상 동작 여부

# QA_테스터 지식 베이스

## 2026-06-05 BIM QA 테스터 2026 기준 업데이트
- Source: LUA BIM LABS QA 운영 기준, IFC 품질 검증, Add-in QA 체크리스트
- Tags: qa,bim-quality,ifc,add-in-testing,kst,2026

**BIM QA 테스터 역할 (2026):**
```
BIM 납품 품질 QA:
1. IFC Export 검증: ifcopenshell로 기본 품질 확인
   - IfcProject 1개 존재, GUID 고유성, 계층 완전성
2. 파라미터 입력률: 필수 파라미터 누락 기기 수 보고
3. 간섭 검토: Navisworks Clash Detective 실행 결과 분류
4. KST 태그 분류:
   - QA_PASS: 자동검수 통과 + 수동 검토 전달
   - QA_PASS_WITH_NOTES: 주의 항목 있음 → PM 병행
   - QA_BLOCKED: 정보 부족 → 확인 후 재진행
   - QA_FAIL: 더미값·누락·증빙 미비 → 반려
```

**Add-in 기능 QA 체크리스트 (BIM CC):**
| 테스트 항목 | 기준 | 결과 |
|-----------|------|------|
| Revit 버전별 실행 | 2023/2024/2025/2026 모두 | Pass/Fail |
| 빈 프로젝트에서 실행 | 오류 없이 실행 | Pass/Fail |
| 대용량 모델(1GB+) 처리 | 5초 내 응답 | Pass/Fail |
| 예외 입력 처리 | 오류 메시지 정상 표시 | Pass/Fail |
| 설치·제거 반복 | 레지스트리 오염 없음 | Pass/Fail |

## 2026-06-04 BF/편의시설 QA 룰 분리 기준
- Source: `knowledge/60_public/training_curriculum/team_distribution/samples/2026-06-04_BIM_MODELER_BF_QA_CHECKLIST_SAMPLE.md`
- Tags: qa,BF,accessibility,checklist,KST

QA_테스터는 BF/편의시설 자동검수 룰을 최종 적합 판정으로 보지 않는다. 자동화는 객체 존재, 파라미터 입력, 도면/뷰 링크, 장애물 후보 탐지에 사용하고, 대상시설·의무/권장·인증 단계·지자체 해석은 수동 검토로 분리한다.

QA 룰 후보:
- 접근로, 주차, 출입구, 복도, 승강기, 화장실, 안내설비 객체 존재 여부
- 모델 파라미터 입력 여부
- BF 검토표, RFI, BCF, 인증 문서 링크 누락 여부
- 문/복도/화장실 주변 장애물 후보 탐지

수동 검토 후보:
- 대상시설 여부
- 의무/권장 편의시설 구분
- 예비인증/본인증 단계별 요구 차이
- 특기시방서와 법령 별표 충돌
- 인증기관, 지자체, 설계자 해석

관련: [[건축]] · [[BIM_납품검수]] · [[2026-06-04 BIM 모델러 BF QA 체크리스트 샘플]]

## 2026-06-04 BF 자동검수 룰 후보 샘플 반영
- Source: `knowledge/60_public/training_curriculum/team_distribution/samples/2026-06-04_QA_BF_AUTOCHECK_RULE_CANDIDATE_SAMPLE.md`
- Tags: qa,BF,autocheck,rule-candidate,KST,training

QA_테스터는 BF/편의시설 자동검수 룰을 `존재 확인`, `파라미터 입력`, `증빙 링크`, `장애물 후보 탐지` 중심으로 등록한다. 자동검수 PASS는 BF 적합, 인증 통과, 납품 합격을 의미하지 않는다.

운영 기준:
- `KST04`: 자동 수집 치수, 객체명, 파라미터 후보는 QA 참고 후보로만 사용한다.
- `KST03`: 대상시설, 의무/권장, 예비인증/본인증, 지자체 조건, 특기시방서는 수동 검토 또는 RFI로 넘긴다.
- 인증 통과 보장 문구가 보고서에 포함되면 `QA_FAIL`로 처리한다.
- 대상성 또는 인증 단계가 미확정이면 `QA_BLOCKED` 또는 `QA_PASS_WITH_NOTES`로 남기고 PM 확인을 요청한다.

관련: [[2026-06-04 QA 테스터 BF 자동검수 룰 후보 샘플]] · [[BIM 납품검수 지식 베이스]] · [[프로그램개발 지식 베이스]]

## 2026-06-04 CS BF 응답과 QA 결과 문구 연결
- Source: `knowledge/60_public/training_curriculum/team_distribution/samples/2026-06-04_CS_BF_EVIDENCE_RESPONSE_SAMPLE.md`
- Tags: qa,BF,cs-response,report-wording,KST

QA_테스터는 BF 자동검수 리포트 문구가 CS 응답과 충돌하지 않도록 관리한다. 리포트에는 `자동검수 후보`, `수동 검토 필요`, `PM/RFI 확인 필요` 같은 표현을 사용하고, `BF 불합격`, `인증 통과`, `법규 적합 확정`처럼 최종 판정으로 읽히는 표현을 피한다.

관련: [[고객지원 CS 지식 베이스]] · [[2026-06-04 CS BF 근거기반 고객 응답 샘플]]

## 2026-06-04 BF 자동검수 개발 티켓 QA 연결
- Source: `knowledge/60_public/training_curriculum/team_distribution/samples/2026-06-04_DEV_BF_AUTOCHECK_TICKET_SAMPLE.md`
- Tags: qa,BF,development-ticket,test-case,KST

QA_테스터는 BF 자동검수 개발 티켓의 TC-DEV-BF-001~006을 회귀 테스트 후보로 등록한다. 특히 인증 단계 미입력은 `QA_BLOCKED`, 보고서 금지 문구는 `QA_FAIL`, 증빙 링크 누락은 `QA_PASS_WITH_NOTES`로 분리한다.

관련: [[프로그램개발 지식 베이스]] · [[2026-06-04 개발 R D BF 자동검수 티켓 샘플]]

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


## BIM Add-in QA 테스트 최신 기준 (2026-05-28)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-28
- Tags: qa,testing,revit,update

- Revit 2025 버전에서 회귀 테스트를 진행할 때는 API 업데이트에 대한 단위 테스트를 활용해야 합니다.
- UI 자동화 시스템을 구축하여 사용자 인터페이스의 변화와 버그를 효과적으로 검출합니다. 이때, Revit 2023, 2024, 2025 버전별로 UI 변경 사항을 체크해야 합니다.
- P1/P2 버그 기준에 따라 테스트를 수행합니다: P1은 시스템의 주요 기능이 제대로 작동하지 않을 때, P2는 부수적인 기능에서 발생하는 문제입니다. 각 버전별로 P1/P2 버그를 체크하고 수정해야 합니다.
- Autodesk Model Checker를 활용하여 BIM 모델의 준법성을 자동화 검사합니다. 이 도구는 Revit 2023부터 지원되며, 모델의 제약 조건과 규격을 확인하는 데 효과적입니다.

## QA 테스터 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: QA,testing,automation,Revit-Addin,regression,2025

- Revit Add-in 테스트 전략(2025): Unit Test(RevitTestFramework v3.x, xUnit 2.x) → Integration Test(Journal File 재생) → Smoke Test(빌드 직후 핵심 기능 5개 자동 검증) → UAT(고객 베타 테스터 5~10명) 4계층으로 테스트 피라미드를 구성한다.
- 멀티버전 회귀 테스트 자동화: GitHub Actions `matrix` 전략으로 Revit 2022·2023·2024·2025 환경에서 동일 테스트 스위트를 병렬 실행한다. 각 버전별 `RevitAPI.dll`을 Docker 볼륨 또는 Windows VM 스냅샷으로 분리 관리하며, 신규 빌드 시 자동으로 회귀 테스트가 트리거된다.
- P1/P2 버그 기준 정의: P1(Critical) — 앱 크래시, 데이터 손실, Revit 강제 종료 유발; P2(High) — 주요 기능 오작동, UI 응답 없음, 잘못된 계산 결과; P3(Medium) — 마이너 UI 오류, 성능 저하; P4(Low) — 오탈자, 아이콘 정렬. P1은 4시간 이내, P2는 24시간 이내 수정 착수를 SLA로 정의한다.
- UI 자동화 테스트: Revit의 복잡한 UI 자동화를 위해 `UIAutomation` (.NET) 또는 PyRevit 기반 스크립트로 버튼 클릭, 다이얼로그 응답, 파라미터 입력 시나리오를 자동화한다. 스크린샷 기반 시각 회귀 테스트로 UI 변경 사항을 감지한다.
- 버그 리포트 표준 템플릿: Revit 버전, OS 버전(Windows 11 22H2 등), Add-in 버전, 재현 단계(Step 1~N), 기대 동작, 실제 동작, 로그 파일(`%TEMP%\Autodesk\Revit\Journals\`) 첨부를 필수 항목으로 정의한다. GitHub Issues 템플릿으로 자동 적용한다.
- 관련: [[빌드검증]] · [[Revit_Addin]] · [[CS_기술지원관]]

## QA 테스트 실전 심화 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: qa,testing,revit-addin,unit-test,regression,ci-cd

**Revit Add-in QA 테스트 레벨:**
| 테스트 유형 | 도구 | 범위 | 실행 주기 |
|---|---|---|---|
| 단위 테스트 | xUnit + RevitTestFramework | 비즈니스 로직 함수 | 코드 커밋 시 |
| 통합 테스트 | Revit Journal 재생 | Revit API 호출 흐름 | PR 머지 전 |
| 회귀 테스트 | 자동화 스크립트 | 이전 버그 재발 체크 | 빌드 후 |
| 멀티버전 테스트 | GitHub Actions 매트릭스 | Revit 2023/2024/2025 | 릴리즈 전 |
| 성능 테스트 | StopWatch API | 1만 요소 처리 시간 측정 | 분기 1회 |

**RevitTestFramework 기반 단위 테스트:**
```csharp
[TestFixture]
public class ClashDetectorTests
{
    [Test]
    [TestModel(@"TestModels/SampleMEP.rvt")]
    public void DetectClashes_ShouldReturn_CorrectCount()
    {
        var doc = RevitTestExecutive.CommandData.Application.ActiveUIDocument.Document;
        var result = new ClashDetector(doc).RunDetection();
        Assert.That(result.Count, Is.GreaterThan(0));
        Assert.That(result.All(c => c.Distance < 0), Is.True); // Hard clash only
    }
}
```

**버그 심각도(Severity) 기준:**
- P1 — Critical: Revit 충돌(크래시)·데이터 손실 → 24시간 내 패치 릴리즈
- P2 — Major: 핵심 기능 불동작 → 다음 스프린트 내 수정
- P3 — Minor: UI 오류·성능 저하(50% 이상) → 분기 내 수정
- P4 — Trivial: 오타·비율 불일치 → 여유 시 수정

**QA 완료 기준 (Definition of Done):**
- [ ] 단위 테스트 커버리지 80% 이상
- [ ] P1/P2 버그 0건
- [ ] Revit 2023/2024/2025 모두 실행 확인
- [ ] 설치/제거 테스트 통과 (MSI/MSIX)
- [ ] App Store 심사 기준 체크리스트 통과
- 관련: [[빌드검증]] · [[스토어심사]] · [[Revit_Addin]] · [[제품패키징]]

## R&D 개발지원그룹 QA 게이트 (2026-05-28)
- Source: LUA BIM LABS group knowledge update 2026-05-28
- Tags: R&D개발지원그룹,QA,release-gate,regression,UAT

QA_테스터는 [[R&D_개발지원그룹]]의 품질 판정 지식이다. QA는 개발자가 “완료”라고 말한 기능을 확인하는 단계가 아니라, [[요구사항분석]]의 REQ가 실제 사용자 시나리오와 실패 케이스에서 통과하는지 검증하는 단계다.

QA handoff 기준:
- 각 REQ는 최소 1개 정상 TC와 1개 실패 TC를 가진다.
- Revit/Navisworks 버전별 지원 범위가 테스트 증거와 일치한다.
- UI 테스트는 빈 문서, 선택 없음, 링크 모델 없음, 권한 없음 상태를 포함한다.
- 성능 기준은 요소 수와 실행 시간을 함께 기록한다.
- UAT 피드백은 기능 개선과 결함을 분리해 등록한다.

QA 결과 상태:
| 상태 | 의미 | 다음 단계 |
|---|---|---|
| QA_PASS | 릴리스 가능 | 제품패키징 |
| QA_PASS_WITH_NOTES | 알려진 제한사항 공개 필요 | 제품패키징/CS |
| QA_BLOCKED | 환경·데이터 부족 | 요구사항분석 |
| QA_FAIL | 결함 수정 필요 | 프로그램개발 |

- 관련: [[R&D_개발지원그룹]] · [[요구사항분석]] · [[빌드검증]] · [[제품패키징]]


## BIM Add-in QA 테스트 최신 기준 (2026-05-29)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-29
- Tags: qa,testing,revit,update

- Revit 버전별 회귀 테스트 기준: 각 Revit 버전 업데이트 시점에 맞춰 이전 버전과의 호환성을 확인하는 회귀 테스트를 실시해야 합니다. 최소 3개월 주기로 진행하며, 이 기간 동안 발생한 버그나 변경 사항을 반영하여 테스트 케이스를 업데이트해야 합니다.

- UI 자동화 팁: Revit의 사용자 인터페이스에 대한 자동화 테스트는 Behavior Driven Development (BDD) 기반으로 진행할 것을 권장합니다. 이는 요구 사항을 명확하게 정의하고, 다양한 사용자 상황을 시뮬레이션하여 UI의 일관성과 성능을 검증하는데 유용합니다.

- P1/P2 버그 기준: P1 버그는 즉시 수정해야 하는 심각한 버그로, 사용자가 작업을 수행할 수 없는 경우 등이 해당됩니다. P2 버그는 사용자 경험에 중대한 영향을 미치지만, 작업 자체에는 문제가 없다면 우선 순위가 낮습니다. 테스터들은 이 기준을 준수하며, 버그의 수정 우선순위를 설정해야 합니다.
- 관련: [[빌드검증]] · [[Dynamo]] · [[Revit_Addin]] · [[CS_기술지원관]]


## 2026-06-04 OpenBIM IDS/BCF QA 보강
- Source: `knowledge/40_curation/updates/daily/2026-06-04_LUA_BIM_LABS_OPENBIM_IDS_BCF_UPDATE.md`
- Tags: qa,ids,bcf,openbim,delivery-quality

QA_테스터는 IDS 자동 검증 결과를 최종 납품 합격으로 보지 않는다. IDS는 IFC 모델의 정보 요구사항 검토에 강하지만 geometry, 간섭, 시공성, MEP 연결성 문제를 모두 보장하지 않는다.

QA 보강 기준:
- IDS PASS 후에도 더미 값, 의미 없는 코드, 미연결 MEP 시스템, 미배치 Space를 별도 확인한다.
- BCF 이슈는 검수 실패 항목의 상태, 담당, 재검수일을 추적하는 증빙으로 사용한다.
- IFC 버전은 최신성보다 발주처 EIR/BEP, 수신 소프트웨어, 검증 도구 지원 여부로 선택한다.

다음 액션:
- Model Quality Auditor QA 시나리오에 `IDS PASS but operational FAIL` 케이스를 추가한다.
- BCF 이슈 상태 전환(Open/In Progress/Closed)을 재검수 증빙 항목으로 둔다.
- 다음 확인일: 2026-06-11

관련: [[IFC OpenBIM 지식 베이스]] · [[BIM 납품검수 지식 베이스]] · [[ACC BIM360 CDE 지식 베이스]]


## BIM Add-in QA 테스트 최신 기준 (2026-05-30)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-30
- Tags: qa,testing,revit,update

- Revit 버전별 회귀 테스트는 Revit 2021부터 최신 버전까지 각 버전별로 실행해야 하는 테스트 항목을 정의하고, 이전 버전에서 발생한 버그가 현재 버전에서도 재발하지 않도록 확인한다.
- UI 자동화를 위해 PyRevit와 같은 도구를 활용하여 테스트 스크립트를 작성하고 실행한다. 이를 통해 사용자 인터페이스의 변경사항이나 버그를 효과적으로 검증할 수 있다.
- P1(Priority 1) 버그는 시스템의 안전성과 관련된 심각한 문제로, 즉시 수정해야 한다. P2(Priority 2) 버기는 사용자 경험을 크게 저해하는 중대한 문제로, 우선순위를 높게 설정한다.
- 테스트 기준은 Revit API와 호환성을 유지하면서 BIM 작업 흐름을 최적화하고, 수작업을 최소화하기 위해 설계 및 시공 자동화와 연계된 도구를 활용한다.
- 관련: [[빌드검증]] · [[Dynamo]] · [[Revit_Addin]] · [[CS_기술지원관]]


## BIM Add-in QA 테스트 최신 기준 (2026-05-31)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-31
- Tags: qa,testing,revit,update

- Revit 버전별 회귀 테스트를 진행하여 이전 버전과의 호환성을 확인해야 합니다.
- UI 자동화를 통해 사용자 인터페이스의 변화를 정기적으로 검증합니다.
- P1 버그 기준은 고정되어 있어야 하며, P2 버그는 빠른 수정이 요구됩니다.
- 관련: [[빌드검증]] · [[Dynamo]] · [[Revit_Addin]] · [[CS_기술지원관]]


## BIM Add-in QA 테스트 최신 기준 (2026-06-01)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-01
- Tags: qa,testing,revit,update

- Revit 2025 버전의 Add-in QA 테스트에서는 Revit 2024 버전과 비교하여 회귀 테스트를 진행해야 합니다. 이는 버전 갱신 시 기존 기능이 제대로 작동하는지 확인하기 위함입니다.
- UI 자동화를 위해 PyRevit을 활용해 복잡한 작업을 자동화할 수 있습니다. 예를 들어, 템플릿 설정 및 데이터 입력 등의 반복적인 작업은 PyRevit 스크립트로 처리하여 효율성을 높일 수 있습니다.
- P1/P2 버그 기준에 따르면, P1 버그는 시스템의 핵심 기능이 제대로 작동하지 않을 경우 발생하며 즉시 수정해야 합니다. 반면 P2 버그는 중요한 기능이나 사용자 경험에 영향을 미치지만, 일정 시간 동안 보류할 수 있는 범위입니다.
- 관련: [[빌드검증]] · [[Dynamo]] · [[Revit_Addin]] · [[CS_기술지원관]]


## BIM Add-in QA 테스트 최신 기준 (2026-06-02)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-02
- Tags: qa,testing,revit,update

- Revit 버전별 회귀 테스트를 진행할 때는 최소 3개 이상의 버전을 대상으로 테스트해야 하며, 각 버전에서 발생한 버그를 기록하고 재현해야 합니다.
- UI 자동화를 위해 Selenium과 Testsigma 같은 도구를 활용하여 Revit Add-in QA 테스팅을 자동화할 수 있습니다. 이때, 테스트 케이스는 P1(Priority 1)과 P2(Priority 2) 버그 기준으로 구분되어야 합니다.
- P1 버그는 시스템의 주요 기능에 영향을 미치거나 사용자에게 심각한 문제를 일으키는 버그로, 즉시 수정해야 합니다. P2 버그는 사용자의 작업 흐름에 경미하게 영향을 미치는 버그로, 우선순위가 높은 버그보다는 나중에 수정하는 것이 적절합니다.
- pyRevit와 C# 같은 도구를 활용하여 Revit Add-in의 기능을 테스트할 수 있으며, 이는 특히 복잡한 BIM 모델링 작업에서 유용합니다.
- 관련: [[빌드검증]] · [[Dynamo]] · [[Revit_Addin]] · [[CS_기술지원관]]


## BIM Add-in QA 테스트 최신 기준 (2026-06-03)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-03
- Tags: qa,testing,revit,update

- Revit 2024 버전별 회귀 테스트: BIM Add-in QA 테스터는 각Revit 버전 업데이트마다 실행되는 회귀 테스트를 통해 기존 기능의 정상 작동을 확인해야 합니다. 이는 Revit 2024 버전에서 최소 1회 이상 수행되어야 하며, P1/P2 버그가 발생하지 않도록 점검합니다.

- UI 자동화: 테스터는 사용자 인터페이스(UI)의 변경사항을 모니터링하고, Revit Add-in의 UI 요소들이 각 버전에서 일관되게 동작하는지 확인해야 합니다. 이는 특히 새로운 버전에서 UI가 크게 변화한 경우에 중요합니다.

- P1/P2 버그 기준: 테스터는 버그 우선 순위를 정하는데 있어 P1(Priority 1)과 P2(Priority 2)를 명확히 이해해야 합니다. P1 버그는 시스템의 주요 기능이 작동하지 않는 경우, P2 버그는 사용자 경험에 중대한 영향을 미치는 문제로 분류됩니다. 이 두 우선 순위의 버그는 즉시 수정되어야 하며, 테스트 과정에서 철저히 점검해야 합니다.
- 관련: [[빌드검증]] · [[Dynamo]] · [[Revit_Addin]] · [[CS_기술지원관]]


## BIM Add-in QA 테스트 최신 기준 (2026-06-03)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-03
- Tags: qa,testing,revit,update

- Revit 2023 버전에서 시작하여 2025 버전까지의 회귀 테스트를 수행해야 합니다.
- UI 자동화 시스템을 구축하고, Revit Add-in QA 테스터는 이 시스템을 활용해 사용자 인터페이스의 변화와 문제점을 신속하게 파악할 수 있어야 합니다.
- P1 버그 기준은 고정되지 않았으나, 일반적으로는 버전 출시 후 30일 내에 수정해야 하는 심각한 버그로 간주됩니다. 
- P2 버그 기준은 사용자의 일상 작업 수행에 지장을 주지만, 큰 문제는 아닌 경우를 포함합니다. 이들은 90일 내에 수정되어야 합니다.
- 관련: [[빌드검증]] · [[Dynamo]] · [[Revit_Addin]] · [[CS_기술지원관]]


## BIM Add-in QA 테스트 최신 기준 (2026-06-04)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-04
- Tags: qa,testing,revit,update

- Revit 2024 버전별 회귀 테스트를 진행하여 이전 버전과의 호환성을 확인한다.
- UI 자동화를 위해 Selenium WebDriver와 같이 사용 가능한 프레임워크를 활용하여 BIM Add-in의 사용자 인터페이스를 자동화한다.
- P1(Priority 1) 버그는 즉시 수정해야 하며, P2(Priority 2) 버그는 최대한 빨리 해결해야 한다. 이 기준은 버그의 심각성과 사용자의 경험에 영향을 미치는 정도를 나타낸다.
- Autodesk Model Checker와 같은 도구를 활용하여 API 업데이트 시 모델의 정확성을 확인한다.
- 관련: [[빌드검증]] · [[Dynamo]] · [[Revit_Addin]] · [[CS_기술지원관]]


## BIM Add-in QA 테스트 최신 기준 (2026-06-05)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-05
- Tags: qa,testing,revit,update

- Revit 2023 버전에서 시작하여 2025 버전까지의 회귀 테스트를 수행해야 합니다.
- UI 자동화를 위한 Selenium WebDriver와 TestComplete을 활용해 QA 테스팅을 자동화합니다.
- P1 버그 기준은 사용자 경험에 직접적인 영향을 미치는 심각한 오류이며, P2 버그는 사용자의 작업 진행에 방해가 되는 중등도의 문제입니다.
- 관련: [[빌드검증]] · [[Dynamo]] · [[Revit_Addin]] · [[CS_기술지원관]]


## BIM Add-in QA 테스트 최신 기준 (2026-06-06)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-06
- Tags: qa,testing,revit,update

- Revit 버전별 회귀 테스트 기준: 각 버전 업데이트 시점에서 이전 버전과의 호환성을 확인하는 회귀 테스트를 실시해야 합니다. 최소 3개월마다 한 번 이상의 회귀 테스트를 진행하고, Revit 버전을 변경할 때마다 해당 버전에 대한 회귀 테스트를 수행합니다.

- UI 자동화 팁: UI 자동화 스크립트는 각 버전에서 일관된 방식으로 작동하도록 설계해야 합니다. Revizto와 같은 도구를 활용하여 모델 검토와 실시간 협업을 지원하며, Tavily AI 요약에 언급된 Autodesk Model Checker와 같은 자동화 툴을 사용해 BIM 모델 규격 준수 여부를 확인합니다.

- P1/P2 버그 기준: P1 버그는 즉시 수정해야 하는 심각한 버그로, 사용자 경험과 작업 효율성에 큰 영향을 미칩니다. P2 버그는 중요한 문제이나 P1보다는 덜 심각하며, 해당 버그가 우선 순위를 결정하는 데 있어 Revit 버전 별로 다소 달라질 수 있습니다.
- 관련: [[빌드검증]] · [[Dynamo]] · [[Revit_Addin]] · [[CS_기술지원관]]


## BIM Add-in QA 테스트 최신 기준 (2026-06-09)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-09
- Tags: qa,testing,revit,update

- Revit 2025 버전에서 API 지원을 활용하여 단위 테스트(Unit Testing)를 수행하고, 이는 BIM Add-in QA 테스팅에 중요한 역할을 합니다.
- 회귀 테스트(Regression Testing)는 Revit 24.1과 Revit 25.0 버전 간의 변경 사항을 확인하기 위해 Revit 24.1에서 실행된 테스트를 Revit 25.0에서도 동일한 결과가 나올지 확인합니다.
- UI 자동화(User Interface Automation)는 Tavily AI 요약에 따르면, Revizto와 같은 도구를 사용하여 실시간 협업과 함께 BIM 소프트웨어 테스트 효율성을 높일 수 있습니다. 
- P1 버그 기준은 일반적인 사용자들이 직면할 가능성이 높은 주요한 문제로, 프로젝트의 성공을 위해 반드시 해결해야 하는 오류입니다.
- P2 버그 기준은 P1보다 덜 중요하지만 여전히 중요한 오류로, 이는 사용자가 작업을 수행하는 데 지장이 있는 문제를 포함합니다.
- 관련: [[빌드검증]] · [[간섭검토]] · [[Dynamo]] · [[Revit_Addin]]


## BIM Add-in QA 테스트 최신 기준 (2026-06-12)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-12
- Tags: qa,testing,revit,update

- Revit 버전별 회귀 테스트 기준: 각 Revit 버전 업데이트 시점마다 최소 3개월 동안의 회귀 테스트를 실시해야 하며, 이 기간 동안 발생한 모든 버그가 다시 발생하지 않도록 확인한다.
- UI 자동화 테스트 기준: 사용자 인터페이스 변경 사항에 따라 최소 80% 이상의 UI 자동화 스크립트를 업데이트하고, 새로운 버전에서 기존 스크립트가 정상 작동하는지 확인한다.
- P1/P2 버그 기준: 
  - P1 버그는 즉시 수정해야 하는 중요 버그로, 테스트 중인 Revit 버전이 출시되지 않아야 한다.
  - P2 버그는 빠르게 수정해야 하는 보조 버그로, 최대한 빨리 수정 및 테스트 후 출시 준비를 완료해야 한다.
- 관련: [[빌드검증]] · [[간섭검토]] · [[Dynamo]] · [[Revit_Addin]]


## BIM Add-in QA 테스트 최신 기준 (2026-06-13)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-13
- Tags: qa,testing,revit,update

- Revit 2025 버전별 회귀 테스트를 진행하며, 새로운 기능과 함께 이전 버전의 기능이 정상적으로 작동하는지 확인해야 합니다.
- UI 자동화를 통해 사용자 인터페이스의 변화와 버그를 효과적으로 탐지하고 수정할 수 있습니다. 이를 위해 TestComplete 또는 AutoIt 같은 도구를 활용할 수 있습니다.
- P1(Priority 1) 버그는 즉시 수정되어야 하는 고위험, 중대한 버그로, 사용자의 작업을 방해하거나 안전에 위협을 가하는 문제입니다.
- P2(Priority 2) 버그는 사용자 경험을 크게 저하시키는 중위험의 버그로, 이 또한 신속히 수정되어야 합니다.
- 관련: [[빌드검증]] · [[간섭검토]] · [[Dynamo]] · [[Revit_Addin]]


## BIM Add-in QA 테스트 최신 기준 (2026-06-15)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-15
- Tags: qa,testing,revit,update

- Revit 2023 버전별 회귀 테스트 기준: Revit 2024 업데이트 이전까지의 모든 버전에서의 기능을 확인하며, 특히 BIM Add-in과의 호환성을 철저히 검토해야 합니다.
- UI 자동화 테스트 팁: Selenium WebDriver와 같은 도구를 활용해 Revit UI의 변경 사항을 자동으로 검증합니다. 각 버튼 클릭, 드롭다운 선택 등을 시뮬레이션하여 사용자 경험을 보장합니다.
- P1/P2 버그 기준: P1 버그는 즉시 수정해야 하는 고급 오류로, 사용자의 작업 흐름에 중대한 영향을 미치며, P2 버그는 사용자가 불편함을 느낄 수 있는 중소 규모의 문제입니다. 이 두 가지 유형의 버그는 우선 순위를 높게 설정하여 신속하게 해결해야 합니다.
- 관련: [[빌드검증]] · [[간섭검토]] · [[Dynamo]] · [[Revit_Addin]]


## BIM Add-in QA 테스트 최신 기준 (2026-06-16)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-16
- Tags: qa,testing,revit,update

- Revit 2023 버전별 회귀 테스트 기준: 각 버전 업데이트 시점에서 이전 버전과의 호환성을 확인하고, 새로운 기능이 제대로 작동하는지 검증해야 합니다.
- UI 자동화 테스트 팁: UI 요소들의 위치와 크기를 정적XPath나 CSS 선택자로 추적하여 변동에 따른 문제를 미리 파악할 수 있습니다. 
- P1 버그 기준: 프리미엄 1(P1) 버그는 사용자의 일상적인 작업 수행에 큰 영향을 끼치거나, 안전성과 관련된 문제가 발생하는 경우로 분류합니다.
- P2 버그 기준: 프리미엄 2(P2) 버그는 사용자가 작업을 완료하는데 약간의 불편함이 있는 경우나, 특정 작업에만 영향을 미치는 문제로 정의됩니다.
- 관련: [[빌드검증]] · [[간섭검토]] · [[Dynamo]] · [[Revit_Addin]]

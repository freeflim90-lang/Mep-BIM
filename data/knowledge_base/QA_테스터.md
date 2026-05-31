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

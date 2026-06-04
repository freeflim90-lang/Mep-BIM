# R&D 개발지원그룹 지식 베이스

## 개요
- Source: LUA BIM LABS internal organization knowledge baseline
- Tags: #R&D개발지원그룹 #개발지원 #프로그램개발 #요구사항분석 #RevitAddin #빌드검증 #QA #DevOps #제품개발
- 업데이트: 2026-05-28

R&D 개발지원그룹은 성장전략그룹이 정의한 제품·자동화 후보를 요구사항, 아키텍처, 구현, 테스트, 패키징 가능한 형태로 전환하는 그룹이다. 핵심 질문은 “이것을 안정적으로 만들고 검증하고 배포할 수 있는가”다.

---

## 2026-06-04 BF 자동검수 티켓 개발지원 기준
- Source: `docs/training_curriculum/team_distribution/samples/2026-06-04_DEV_BF_AUTOCHECK_TICKET_SAMPLE.md`
- Tags: R&D,BF,autocheck,RevitAddin,QA,KST

R&D 개발지원그룹은 BF 자동검수 후보를 개발 착수 전 `문제정의`, `입력 데이터`, `출력 결과`, `API 가능성`, `안전성`, `테스트 조건`으로 분해한다. BF 기능은 모델을 자동 수정하거나 인증 판정을 내리는 기능이 아니라, 검토 후보와 증빙 누락을 리포트하는 기능으로 시작한다.

착수 게이트:
- 입력: Revit 요소, 카테고리/패밀리명, 지정 파라미터, 도면/뷰/RFI/BCF 링크
- 출력: 후보 리포트, QA 상태, KST 상태, PM/RFI 확인 요청
- 안전성: dry-run/report-first, 모델 자동 수정 제외
- 테스트: BF 태그 누락, 인증 단계 미입력, 증빙 링크 누락, 금지 문구 차단, 링크 모델 처리
- 실기 검증: 대상 카테고리 매핑, Room/Space/Area 연결, 링크 모델, 대형 모델 성능

관련: [[프로그램개발 지식 베이스]] · [[QA_테스터 지식 베이스]] · [[2026-06-04 개발 R D BF 자동검수 티켓 샘플]]

## 1. 그룹 미션

| 미션 | 설명 |
|---|---|
| 요구사항 구조화 | 전략 후보를 REQ, 사용자 시나리오, 테스트 조건으로 변환 |
| 기술 타당성 검토 | Revit/Navisworks/IFC/API/웹/로컬 자동화 가능성 판정 |
| 개발 실행 지원 | 아키텍처, 코드 기준, Qwen 초안 큐, 구현 검토 |
| 품질·빌드 게이트 | 테스트, 빌드, Store 제출 안정성, 릴리스 차단 결함 관리 |
| 기술 지식 환류 | 개발 중 발견한 패턴을 KB, QA, 표준문서로 되돌림 |

---

## 2. 담당 지식 영역

| 지식 파일 | 역할 |
|---|---|
| [[요구사항분석]] | 제품 후보를 기능 명세와 테스트 가능 조건으로 전환 |
| [[프로그램개발]] | C#/.NET, 백엔드, 자동화 코드 구현 기준 |
| [[Revit_Addin]] | Revit API, Transaction, 리본, Assistant 연동 |
| [[Navisworks_Addin]] | Navisworks API, Clash, SearchSet, 모델 검토 자동화 |
| [[IFC_OpenBIM]] | IFC 매핑, IDS, OpenBIM 납품 검증 |
| [[OpenBIM_프로그램연동]] | 외부 프로그램·데이터 파이프라인 연동 |
| [[빌드검증]] | 멀티버전 빌드, 서명, smoke test, 릴리스 차단 기준 |
| [[QA_테스터]] | 테스트 케이스, 회귀, 결함 등급, UAT |
| [[제품패키징]] | MSI/번들/Store 제출물의 기술 패키징 |
| [[인프라_DevOpsObsidian]] | 개발·지식·배포 자동화 인프라 |
| [[프롬프트엔지니어]] | AI 보조 개발·RAG·프롬프트 품질 기준 |

---

## 3. R&D 개발지원 운영 루프

```
[전략 요청 수신]
  → 성장전략그룹 / 아이디어발굴 / 전략기획

[요구사항 분해]
  → 요구사항분석 / 프로젝트분석 / EIRBEP_심사원

[기술 설계]
  → 프로그램개발 / Revit_Addin / IFC_OpenBIM / Navisworks_Addin

[초안 구현·정적 검토]
  → Qwen_Coder_8B / 로컬 테스트 / 코드 리뷰

[실기 검증]
  → 빌드검증 / QA_테스터 / Revit API Test Gate

[릴리스 handoff]
  → 제품패키징 / 스토어심사 / CS_기술지원관
```

---

## 4. 개발 착수 게이트

R&D 개발지원그룹은 다음 조건이 충족될 때 개발 착수로 전환한다.

| 게이트 | 통과 기준 |
|---|---|
| 문제정의 | 사용자, 반복 빈도, 해결 가치가 명확함 |
| 입력 데이터 | Revit 요소, IFC 속성, Excel, API 등 입력 원천이 정의됨 |
| 출력 결과 | 모델 변경, 리포트, 일람표, UI, API 응답 중 결과 형식 확정 |
| API 가능성 | 공식 API로 가능한지, 실기 검증이 필요한지 분리 |
| 안전성 | dry-run, rollback, report-first 원칙 적용 여부 판단 |
| 테스트 조건 | 최소 smoke test와 실패 케이스가 정의됨 |

---

## 5. 산출물 표준

| 단계 | 산출물 | 저장 위치 |
|---|---|---|
| 요구사항 | REQ 목록, 사용자 시나리오, 제외 범위 | `data/knowledge_base/요구사항분석.md`, 제품별 docs |
| 설계 | 도메인 모델, API 계약, 데이터 스키마 | `docs/`, `obsidian_vaults/model_quality_auditor/06_Qwen_Drafts/` |
| 구현 | 코드, 테스트, migration, 설정 파일 | repo source tree |
| 검증 | smoke test, 빌드 로그, QA 리포트 | `docs/autodesk_store/`, `docs/standard_documents/` |
| 릴리스 | 패키지, 릴리스 노트, Store 제출 체크리스트 | `dist/`, `docs/autodesk_store/` |

---

## 6. R&D 실패 패턴 Top 5

1. 요구사항이 불명확한 상태에서 코드를 먼저 작성해 재작업이 누적됨.
2. Revit API 실기 검증이 필요한 기능을 로컬 정적 검토만으로 완료 처리함.
3. 모델 변경 기능에 dry-run과 rollback 설계가 없어 고객 모델 손상 리스크 발생.
4. 빌드·패키징·Store 심사 조건을 개발 후반에 확인해 릴리스가 지연됨.
5. 개발 중 발견한 지식을 KB로 환류하지 않아 같은 버그와 판단을 반복함.

## 관련 링크
- [[성장전략그룹]]
- [[23_IDEA_TO_PRODUCT_DEVELOPMENT_PIPELINE]]
- [[28_CODE_DEVELOPMENT_GMAIL_REPORTING]]
- [[AX_전략승격리뷰]]


## R&D 개발지원그룹 기술 심화 기준 (2026-05-29)
- Source: claude-code-enhanced 2026-05-29
- Tags: R&D,revit-addin,build,qa,devops,cicd,dotnet,architecture

**Revit Add-in 멀티버전 빌드 아키텍처:**
- Revit 2022/2023: .NET Framework 4.8, API어셈블리 `RevitAPI.dll` / `RevitAPIUI.dll` 각 버전 분리 참조
- Revit 2024/2025: .NET 8, `<TargetFramework>net8-windows</TargetFramework>` + `<PlatformTarget>x64</PlatformTarget>`
- 멀티타겟 전략: `Directory.Build.props`에서 `RevitVersion` 조건부 컴파일 기호 정의 → `#if REVIT2024` 분기
- 빌드 출력: 버전별 `dist/2022/`, `dist/2024/` 폴더 + `.addin` 매니페스트 자동 생성 스크립트
- AssemblyVersion: Revit 버전과 혼동 방지 위해 제품 SemVer(1.2.3) 별도 관리

**QA 게이트 기준 — Revit Addin 출시 전 필수 통과:**
- Smoke Test: Revit 최소 2버전(최신-1, 최신) 모두 패밀리 로드 → 리본 버튼 표시 → 기능 1회 실행 성공
- 트랜잭션 안전성: `using (Transaction t = new Transaction(doc, "LUA_Operation"))` 패턴, `t.Start()`/`t.Commit()` 외부에서 Element 수정 시 `InvalidOperationException` 발생 → 테스트 케이스 포함
- 예외 처리 게이트: `TaskDialog`로 스택트레이스 노출 금지 — 고객사 모델 정보 유출 리스크. 전용 로거(`%AppData%\LUA BIM LABS\logs\`)로만 기록
- ElementId 호환성: Revit 2024+ `ElementId.IntegerValue` 사용 시 `InvalidCastException` → `ElementId.Value` (Int64)로 통일 후 2022 빌드에서는 `#if REVIT2024` 분기
- 메모리 누수: `FilteredElementCollector` 사용 후 `Dispose()` 호출 또는 `using` 블록 적용

**개발 속도 저하 상위 5가지 패턴 및 예방법:**
1. **API 실기 없이 정적 완료 처리**: Revit API는 반드시 Revit 설치 PC에서 실행 검증. `ExternalEvent`·`IExternalEventHandler` 패턴은 Revit 비동기 컨텍스트에서만 동작 — 모킹 불가
2. **ForgeTypeId 미적용**: Revit 2022+ `DisplayUnitType`/`ParameterType` → `ForgeTypeId` 마이그레이션. 구버전 API 잔류 시 빌드 경고 → Revit 2026에서 컴파일 오류
3. **중첩 Transaction**: Transaction 내부에서 Sub-Transaction 없이 ElementId 수정 시 RollBack 불가 — `SubTransaction` 또는 `TransactionGroup` 설계 필수
4. **패키징 후 Store 거절**: `addin` 파일 `Type="Command"` 누락, PackageContents.xml 구조 오류, 서명 인증서 만료 — 릴리스 체크리스트에 Store 심사 사전 확인 포함
5. **로그 없는 현장 결함**: Add-in 오류를 `TaskDialog`만으로 처리하면 현장 재현이 불가. `NLog` 또는 `Serilog` 파일 싱크 + 로그 레벨 제어 설계를 초기 아키텍처에 포함

**Qwen Coder 초안 활용 기준:**
- Revit API 코드 초안은 Qwen으로 생성 후 반드시 인간 검토 — Qwen은 `RevitAPI.dll` 버전 혼용 코드를 생성할 수 있음
- 생성된 초안의 `FilteredElementCollector` 쿼리, LINQ 조합, `Element.LookupParameter()` 반환 null 처리 여부를 코드 리뷰 체크리스트에 포함
- 관련: [[Revit_Addin]] · [[빌드검증]] · [[QA_테스터]] · [[성장전략그룹]]


## R&D 개발지원그룹 마스터급 경험 지식 (2026-05-29)
- Source: claude-code-enhanced 2026-05-29
- Tags: R&D,devops,build-failure,regression,store-submission,field-experience

**Store 제출 거절 사례별 대응 플레이북:**
- 거절 원인 1 — "코드 서명 없음 또는 만료": EV(Extended Validation) 코드 서명 인증서 필수. 인증서 갱신 주기(1~3년)를 릴리스 캘린더에 등록하고 만료 60일 전 자동 알림 설정
- 거절 원인 2 — "설치 경로 외 파일 쓰기": Revit Add-in은 `%AppData%` 또는 `%ProgramData%` 외부에 파일 생성 금지. 임시 파일은 반드시 `Path.GetTempPath()` 사용
- 거절 원인 3 — "Revit 성능 저하": 리본 초기화 시 무거운 I/O(네트워크, DB 연결) 수행 금지. 리본 버튼 클릭 후 비동기 로딩(`ExternalEvent`)으로 이관
- 거절 원인 4 — "패키지 구조 오류": `PackageContents.xml` Components/RuntimeRequirements 항목에서 최소/최대 Revit 버전 선언 정확성 체크

**회귀 방지를 위한 KB 환류 프로세스:**
개발 중 발견한 Revit API 제약·버그·버전별 동작 차이를 즉시 `data/knowledge_base/Revit_Addin.md` 또는 `빌드검증.md`에 기록한다. 기록 포맷: "버전 X에서 발생 → 원인 → 해결 코드 패턴 → 테스트 케이스 추가". 이 환류 없이 다음 릴리스에서 같은 결함이 재발하는 것이 LUA BIM LABS 개발 속도를 저하시키는 구조적 원인이다.

**CI/CD 파이프라인 권장 구성 (GitHub Actions 기준):**
- `build.yml`: 트리거 — PR + main push. 매트릭스 전략으로 Revit 2022/2023/2024/2025 버전별 병렬 빌드
- `smoke_test.yml`: 트리거 — main push 후. Windows Server self-hosted runner에 Revit 설치 후 CLI 자동화로 플러그인 로드 확인
- `release.yml`: 트리거 — 태그 push (`v*`). 서명 → MSI 생성 → `dist/` 폴더 GitHub Release에 첨부 → Store 체크리스트 자동 생성
- 주의: Revit 라이선스가 필요한 smoke test는 self-hosted runner만 가능 — GitHub-hosted runner에서는 실행 불가
- 관련: [[빌드검증]] · [[Revit_Addin]] · [[Navisworks_Addin]] · [[제품패키징]]

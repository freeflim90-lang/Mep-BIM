# CS 기술지원 에스컬레이션 지식 베이스

조직도에서는 `고객지원 CS`가 일반 문의의 단일 통합 창구다. 기술지원관은 별도 담당자 노드가 아니라 CS 내부의 기술 이슈 에스컬레이션 기준으로 유지한다.

## 2026-06-05 CS 기술지원 2026 기준 업데이트
- Source: LUA BIM LABS CS 운영 기준, KST 태그 체계
- Tags: technical-support,escalation,kst,bim,2026

**CS 기술지원 에스컬레이션 판단 기준:**
```
Level 1 — AI 봇 자동 처리:
  → KST01 공식 기준이 있는 질문
  → 설계 수치·법규·납품 형식 등 객관적 답변 가능

Level 2 — CS 담당자 확인 후 답변:
  → KST03 프로젝트별 확인 필요 항목
  → 발주처 BEP·과업지시서 확인 필요한 경우

Level 3 — 전문가 에스컬레이션 (PM/RFI):
  → BF 인증 통과·납품 적합 판정 등 법적 책임 수반
  → 설계 변경·구조기술사 확인 필요
  → CS 단독 확정 불가

Level 4 — 외부 기관 안내:
  → 소방청·국토부·인증기관 등 공식 문의 필요
```

**기술 이슈 유형별 처리 기준:**
| 이슈 유형 | 처리 레벨 | 응답 시간 |
|---------|---------|---------|
| Revit 기능 질문 | Level 1 (봇) | 즉시 |
| BIM LOD 기준 | Level 1 (봇) | 즉시 |
| 발주처별 납품 차이 | Level 2 | 24시간 |
| 소방·BF 인증 판정 | Level 3 (RFI) | 5영업일 |
| 법령 해석 | Level 4 | 안내만 |

## 2026-06-04 근거기반 기술 응답 에스컬레이션 기준
- Source: `knowledge/60_public/training_curriculum/team_distribution/samples/2026-06-04_CS_TECHNICAL_EVIDENCE_RESPONSE_SAMPLE.md`
- Tags: technical-support,evidence-response,KST,escalation

기준, 법규, 납품검수, 제품 오류가 함께 걸린 고객 문의는 CS 1차 응답에서 결론, 근거, 적용 범위, 주의, 다음 액션을 분리한다. CS가 고객에게 안내할 수 있는 범위는 현재 확인된 사실, 요청할 자료, 후속 검토 절차까지이며, 설계 변경·시공 승인·인허가 적합성 판단은 PM/RFI 또는 전문가 확인으로 에스컬레이션한다.

에스컬레이션 신호:
- 고객이 특정 법규 수치나 기준 조항을 납품 합격 기준으로 확정해 달라고 요청한다.
- 자동 수집 지식(`KST04`)에 있는 수치를 근거로 고객이 즉시 수정 여부를 묻는다.
- 발주처 특기시방서, 설계도서, BEP/EIR, 지자체 조건 사이에 충돌 가능성이 있다.
- 제품 기능 오류와 프로젝트 기준 적용 여부가 함께 섞여 있다.

관련: [[고객지원CS]] · [[2026-06-04 CS 기술지원 근거기반 응답 샘플]] · [[BIM_납품검수]] · [[지식업데이트]]

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


## CS 기술지원관 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: cs,technical-support,revit,addin,sla,escalation,troubleshoot

- **L1~L3 에스컬레이션 SLA 강화**: L1 일반 문의는 4시간 이내 응답, L2 Add-in 오작동(Revit 버전 호환·WebView2 충돌 등)은 영업일 1일 이내 해결, L3 크래시 덤프·재현 불가 버그는 영업일 3일 이내 개발팀 초기 대응 완료를 SLA 기준으로 관리한다.
- **Revit 버전별 진단 체계**: Revit 2022/2023은 .NET Framework 4.8 기반으로 Add-in 로딩 실패 시 `%AppData%\Autodesk\Revit\Addins\202x\` manifest 경로와 .NET 버전을 우선 확인한다. Revit 2024/2025는 .NET 8 기반 병렬 로딩 구조이므로 기존 Framework Add-in과 혼재 시 충돌이 발생할 수 있고, 버전별 별도 설치 파일로 안내한다.
- **수집 정보 표준화**: 고객으로부터 Revit 버전(About Revit), Add-in 버전(제품 About 메뉴), Windows 이벤트 뷰어 오류 코드, `%AppData%\LUA BIM LABS\logs\` 최신 로그 파일을 수집한다. 실제 프로젝트 모델은 재현 불가 시 마지막 수단으로만 요청하며, 고객 동의 후 처리한다.
- **FAQ 등록 기준**: 동일 유형 문의 2건 이상 접수 시 FAQ 후보 등록 → CS 초안 작성 → 기술지원관 검토 → 승인 프로세스를 준수한다. 월 1회 전체 FAQ 리뷰하여 해결된 항목은 아카이브하고 신규 Revit 버전 변경사항을 반영한다.
- **Autodesk App Store 특이사항**: Store 구매 고객의 라이선스 인증 실패는 방화벽·프록시 차단 여부와 오프라인 환경을 먼저 점검한다. P1(전체 사용 불가, 다수 고객 영향)은 2시간 이내 1차 응답, 당일 해결 목표를 유지한다.
- 관련: [[고객지원CS]] · [[Revit_Addin]] · [[빌드검증]] · [[QA_테스터]]


## CS 기술지원관 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: cs,technical-support,remote-debug,journal,version-update,store-review,field-experience

고객이 "오류가 있다"고 주장하지만 재현 불가 상황 대처법: 내부 환경에서 재현이 안 될 때 가장 효과적인 방법은 Revit Journal 파일 분석이다. Journal 파일은 `%LocalAppData%\Autodesk\Revit\Autodesk Revit 202x\Journals\` 에 세션별로 저장되며, 오류 발생 당시 명령 시퀀스, API 호출, 예외 스택 트레이스가 텍스트로 기록된다. 고객에게 해당 폴더에서 가장 최근 journal 파일을 첨부하도록 안내한 뒤, 파일 내 `Exception` 또는 `Error` 키워드를 검색해 원인 라인을 식별한다. 재현이 여전히 어려우면 원격 세션(TeamViewer, AnyDesk)으로 고객 환경에서 직접 로그를 채취하고, Add-in Manager에서 다른 Add-in을 비활성화한 뒤 단독 실행으로 충돌 여부를 확인한다.

Revit 버전 업데이트 후 Add-in 무효화 클레임 대응 — 호환성 정책 공지 방법: Autodesk는 매년 Revit 신버전을 출시하며, 기존 Add-in은 신버전에서 재컴파일 없이 작동하지 않는 경우가 많다. 사전 대응으로 ① 제품 페이지와 릴리스 노트에 지원 Revit 버전을 명시 ② Revit 신버전 출시 후 30일 이내 호환 업데이트 공약을 공지 ③ 고객 이메일로 "Revit 202x 호환 업데이트가 준비되었습니다" 개별 통보. 이 대응을 갖추면 App Store 부정 리뷰 전환율을 크게 낮출 수 있다. 이미 클레임이 접수된 경우 업데이트 일정을 48시간 이내에 고객에게 직접 통보하고 조기 접근 링크를 제공하는 것이 클레임을 긍정적 전환으로 바꾸는 가장 빠른 방법이다.

악성 리뷰 대응 전략 — Autodesk App Store 공개 답변 작성법: App Store 리뷰에는 개발자 공개 답변 기능이 있다. 답변 원칙은 ① 감사 인사로 시작(고객의 피드백을 환영한다는 신호) ② 문제 인정과 원인 간략 설명(변명 금지, 사실만 기술) ③ 이미 배포된 수정 버전 안내 또는 예정 날짜 명시 ④ 개인 연락 채널(support@luabimlabs.com) 안내로 마무리. 별점 1점 리뷰에 이 형식의 답변을 달면 Autodesk 심사팀이 평판 관리 의지를 긍정적으로 평가하고, 다른 잠재 고객에게도 신뢰 시그널이 된다. 공격적이거나 감정적인 답변은 절대 금지.

- 관련: [[Revit_Addin]] · [[스토어심사]] · [[빌드검증]]

## CS 기술지원관 BIM 프로그램 심층 이해 (2026-05-29)
- Source: claude-code-enhanced-depth 2026-05-29
- Tags: cs,revit-internals,navisworks,bim-structure,technical-depth,troubleshoot

### Revit 모델 내부 구조 — CS가 알아야 할 핵심

**Document / Element / Parameter 계층 이해:**
Revit 모델(`.rvt`)은 하나의 Document 객체다. Document 안에 모든 Element가 있고, 각 Element는 Category + Family + Type + Instance로 구성된다. CS가 고객 오류를 분류할 때 이 계층을 이해해야 한다:
- "파라미터가 없다" → Instance 파라미터인지 Type 파라미터인지, 공유(Shared) 파라미터인지 먼저 확인
- "값이 안 바뀐다" → Read-only 파라미터(계산식 기반) 또는 Transaction 미시작 오류
- "요소가 선택 안 된다" → 링크 파일(RevitLinkInstance) 안에 있는 요소는 직접 접근 불가

**ElementId 관련 오류 — Revit 2024부터 필수 확인:**
Revit 2024에서 ElementId가 32비트(int) → 64비트(long)으로 변경됐다. 이로 인해 2023 이하 버전용 Add-in을 2024에서 실행하면 `InvalidCastException` 또는 `ArgumentException`이 발생한다. CS는 이 오류를 보면 즉시 Revit 버전 + Add-in 버전 조합을 확인해야 한다.

**ForgeTypeId / UnitTypeId 오류 (Revit 2022+):**
Revit 2022부터 단위 시스템이 `UnitTypeId` → `ForgeTypeId`로 전환됐다. 구버전 코드에 `UnitUtils.ConvertToInternalUnits(value, DisplayUnitType.DUT_MILLIMETERS)` 같은 구문이 있으면 2022 이상에서 컴파일 오류 또는 런타임 예외가 발생한다. 고객이 "길이 계산이 틀리다"고 하면 이 전환 문제를 의심한다.

**Transaction 오류 패턴:**
Add-in이 모델을 수정할 때 반드시 `Transaction`을 열어야 한다. 가장 흔한 오류:
- `Autodesk.Revit.Exceptions.InvalidOperationException: Starting a transaction is not allowed` → 이벤트 핸들러나 동기화 컨텍스트 밖에서 Transaction을 시작한 경우. 로그에서 이 메시지 발견 시 L3 에스컬레이션.
- `TransactionException: The transaction has not been started` → API 순서 오류.
- 고객 증상: "버튼을 눌러도 모델이 안 바뀐다 + 오류창이 뜬다" 패턴으로 나타남.

**DocumentChanged / Application 이벤트 오류:**
실시간 모델 감시 기능(요소 변경 감지)이 있는 Add-in에서 `DocumentChanged` 이벤트 내에서 모델 수정을 시도하면 Revit이 강제 종료된다. 고객이 "특정 요소를 편집하면 Revit이 닫힌다"고 하면 이 패턴이다. 로그에서 `Autodesk.Revit.Exceptions.ForbiddenForDynamicUpdatersException` 키워드를 검색한다.

---

### Revit 링크 파일 관련 오류

링크 파일(`.rvt` 링크)은 별도 Document이고, 링크 안의 요소에 직접 쓰기는 불가능하다. CS 자주 접하는 오류:
- "링크 파일 요소가 선택되는데 기능이 작동 안 한다" → Add-in이 링크 요소는 지원하지 않는 경우. 기능 범위 외 사항임을 안내.
- "링크가 갑자기 Unloaded 됐다" → 파일 경로 변경 또는 중앙 모델 동기화 중 링크 경로 갱신 실패. Manage Links에서 경로 재확인 안내.
- "링크된 모델 요소가 일람표에 안 잡힌다" → Schedule 설정에서 "Include linked files" 옵션 미체크. Revit 기본 기능 범위로 CS L1에서 안내.

---

### Revit IFC 내보내기 오류 (OpenBIM 관련 문의)

- `IFC Export Failed: Cannot export model with invalid parameters` → 필수 파라미터가 비어 있거나 특수문자 포함 시 발생. 내보내기 전 파라미터 검증 실행을 안내.
- `IFC 파일이 열리지 않는다` → IFC 버전(IFC2x3 vs IFC4) 불일치, 또는 IFC 뷰어(Solibri, BIMcollab 등) 버전 확인 필요.
- IFC 내보내기는 Revit 기본 기능 + Add-in 커스텀 설정이 혼재한다. LUA 제품이 개입된 부분과 Revit 기본 기능 부분을 먼저 분리해 원인을 좁힌다.

---

### Navisworks 관련 기술지원

**NWC/NWD 파일 형식:**
- `.nwc`: Navisworks Cache 파일 — Revit, AutoCAD 등에서 직접 내보내는 캐시. 원본 파일이 변경되면 재내보내기 필요.
- `.nwd`: Navisworks Document — 여러 NWC를 합친 통합 파일. 배포용.
- `.nwf`: Navisworks File — 링크 구조 유지 (원본 파일 경로 참조). 경로 변경 시 깨짐.

**Navisworks 자주 접하는 오류:**
- "NWC로 내보냈는데 객체가 없다" → Revit에서 내보내기 전 "현재 뷰" 설정 확인. 3D 뷰에서 내보내야 전체 모델이 포함된다.
- "간섭 검토 결과가 저장 안 된다" → `.nwf` 파일은 결과를 원본 파일에 저장한다. `.nwd`로 저장해야 결과가 포함된다.
- "Clash Detective 실행 시 오류" → Navisworks 버전(2023/2024/2025)과 NWC 내보내기 버전 불일치. 동일 버전 내보내기 안내.
- "TimeLiner 시뮬레이션이 멈춘다" → 대용량 모델(1GB 이상)에서 RAM 부족 현상. 64GB RAM 권장 환경 안내.

**Navisworks Add-in API 제한:**
- Navisworks API는 Revit API보다 접근 범위가 제한적이다. 간섭 결과 내보내기, 뷰포인트 조작, SearchSet 자동화는 가능하지만, 모델 요소의 파라미터를 직접 수정하는 건 불가능하다.
- 고객이 "Navisworks에서 값을 수정하고 싶다"고 하면 Revit 원본 파일을 수정해야 함을 안내.

---

### BIM 워크플로우 오류 — 실무 장면별 분류

**중앙 파일(Central Model) / 작업 집합(Workset) 오류:**
- "동기화가 안 된다" → 다른 사용자가 Revit 강제 종료 후 잠금 해제가 안 된 경우. `SWC` 파일 삭제(중앙 파일 서버에서)가 필요할 수 있다 → L2 에스컬레이션.
- "요소를 편집할 수 없다" → 다른 사용자가 해당 작업 집합을 체크아웃한 상태. 해당 사용자에게 반환 요청 안내.
- "중앙 파일이 손상됐다" → 오류 백업 파일(`Backup` 폴더)에서 이전 버전 복원 안내 → L3 에스컬레이션.

**패밀리(Family) 관련 오류:**
- "패밀리를 로드했는데 기능이 인식 못 한다" → 패밀리 카테고리 또는 공유 파라미터(Shared Parameter) GUID가 Add-in 기대값과 다른 경우. 표준 패밀리 사용 여부 확인.
- "패밀리 파라미터가 없다" → Instance vs Type 파라미터 구분, 또는 패밀리를 재로드 후 Type 파라미터가 초기화된 경우.

**공유 파라미터(Shared Parameter) 오류:**
- Add-in이 특정 공유 파라미터 GUID로 데이터를 읽는 경우, 고객 모델에 해당 파라미터가 없으면 `KeyNotFoundException` 발생.
- 증상: "기능을 실행하면 빈 결과가 나온다 / 오류창이 뜬다"
- 해결: LUA BIM LABS 제공 공유 파라미터 파일(`.txt`)을 모델에 등록하는 절차 안내.

- 관련: [[Revit_Addin]] · [[Navisworks_Addin]] · [[IFC_OpenBIM]] · [[빌드검증]] · [[QA_테스터]]

## 기술지원 CS 운영 기준 업데이트 (2026-06-17)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-17
- Tags: cs,technical-support,revit,update

- Revit/BIM Add-in의 최신 버전 업데이트 시 Revit 버전 호환성 문제 발생 시, 먼저 고객에게 현재 사용 중인 Revit 버전과 Add-in 버전을 확인하도록 요청합니다. 이후 호환성을 확인하고, 불일치시 호환 가능한 최신 버전으로 업데이트를 권장합니다.
- 설치 오류가 발생한 경우, 설치 과정에서 오류 메시지를 고객에게 제공받아 정확하게 파악한 후, 해당 오류 코드에 대한 공식 지원 문서나 온라인 커뮤니티 자료를 참조하여 해결 방안을 제시합니다. 필요하다면 직접적인 원격 지원 요청을 권장할 수 있습니다.
- 고객 응대 시 스크립트 예시: "안녕하세요, [고객 이름]님. Revit/BIM Add-in에 대한 문제로 문의해 주셔서 감사합니다. 현재 사용 중인 Revit 버전과 Add-in 버전을 알려주시면 확인 후 적절한 해결 방안을 안내드리겠습니다."
- 관련: [[간섭검토]] · [[Dynamo]] · [[Revit_Addin]] · [[고객지원CS]]


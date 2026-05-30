# BIM 납품검수 지식 베이스

## BIM 납품검수 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: bim,quality-check,ids,kbims,checker,deliverable,iso19650

BIM 납품검수는 발주처가 요구한 EIR(발주자 정보요구서) 기준으로 제출된 BIM 모델·문서의 적합성을 검증하는 프로세스.
국토부 BIM 업무지침에 따라 설계 단계별(계획/기본/실시) 납품 전 반드시 수행.

**검수 유형:**
- 형식 검수: 파일 포맷(IFC 버전), 파일명 규칙, 폴더 구조
- 내용 검수: 파라미터 입력 완결성, LOD 달성 수준
- 기술 검수: 클래시(간섭) 건수, 좌표 일치, 단위 통일

## BIM 납품검수 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: bim,quality-check,ids,solibri,navisworks,python,kbims-checker

**국토부 BIM 납품 체크리스트 (2023 기준):**
- [ ] 파일명 규칙 준수: `[프로젝트코드]_[공종]_[단계]_[날짜].rvt/ifc`
- [ ] IFC 버전: IFC 2×3 또는 IFC 4 (발주처 요구사항 확인)
- [ ] 공유 파라미터: 룸코드·공종코드·마감코드 입력 완결성 100%
- [ ] 단위 통일: 미터법(mm 기준), 각도(도)
- [ ] 클래시: Hard Clash 0건, Clearance Clash 관리 목록 제출
- [ ] 좌표: Survey Point 국가좌표계(GRS80 or Bessel 1841) 일치
- [ ] 모델 파일 크기: 단일 Revit 파일 300MB 이하 권고

**자동 품질 검수 도구:**
- **Solibri Model Checker**: IDS XML 기반 규칙 검증, BCF 이슈 내보내기
- **KBIMS Checker** (국토부): 국내 BIM 업무지침 자동 검증 (무료 배포)
- **ifctester** (Python): IDS 1.0 검증 라이브러리
  ```python
  import ifctester
  ids = ifctester.ids.open("project_ids.xml")
  ifc = ifcopenshell.open("model.ifc")
  results = ids.validate(ifc)
  for spec in results.specifications:
      print(spec.name, "PASS" if spec.passed else "FAIL")
  ```
- **Revit Warning Export**: `FilledRegion` 경고·교차 경고 목록 → 납품 전 0건 달성

**BCF(BIM Collaboration Format) 이슈 관리:**
- BCF 2.1 표준: buildingSMART International (ISO 21597-1:2020)
- 클래시/품질 이슈 → .bcfzip 파일 → ACC Build 이슈 자동 임포트
- Python bcf-client: BCF API 서버 연동, 이슈 상태(Open/In Progress/Closed) 자동 업데이트

**LUA BIM LABS Add-in 납품검수 모듈 아이디어:**
- Revit 공유 파라미터 입력률(%) 실시간 대시보드 (WPF TaskPane)
- IFC Export → ifctester 자동 실행 → 결과 요약 Excel 생성
- Hard Clash Count → 납품 가능 판정 기준: 0건
- 관련: [[BIM_지침서]] · [[IFC_OpenBIM]] · [[EIRBEP_심사원]] · [[QA_테스터]]

## BIM 납품검수 실전 심화: 검수관 절차와 판정 기준 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: bim,deliverable,inspection,ids,bcf,kbims,grade,acceptance

**단계별 납품 검수 절차 (EIRBEP 심사원 관점):**
1. **형식 검수** (자동): 파일명 규칙, 폴더 구조, 파일 크기 → Python 스크립트 자동 확인
2. **IFC 변환 검수** (자동): ifctester IDS 검증 → 통과/실패 항목 목록 생성
3. **모델 정합성** (반자동): 클래시 건수 확인, 좌표 일치 검증, 단위 통일 확인
4. **파라미터 완결성** (자동): 필수 파라미터 입력률 ≥ 95% 요건
5. **내용 검수** (수동): LOD 달성 수준 샘플링 20개 요소 검토
6. **최종 판정**: 전 항목 통과 시 `Accepted` 스탬프 발행

**납품 판정 기준:**
| 항목 | 합격 기준 | 불합격 조건 |
|---|---|---|
| 파일명 규칙 | 100% 준수 | 1건이라도 위반 |
| IFC Export | Hard Clash 0건 | 1건 이상 |
| 필수 파라미터 | 입력률 95% 이상 | 95% 미만 |
| LOD 달성 | 요구 LOD의 90% 이상 요소 적합 | 90% 미만 |
| 좌표 일치 | 공종 간 오차 ±5mm 이내 | 5mm 초과 |

**불합격 시 RFI 발행 절차:**
1. 검수 결과 → BCF 2.1 이슈 생성 (항목별)
2. ACC Build RFI 자동 등록 (Webhook 연동)
3. 납품자 수정 기간: P1 이슈 3영업일 / P2 이슈 7영업일
4. 재검수: 수정본 재제출 → 해당 항목만 재검증
5. 2회 불합격 시: 프로젝트 매니저 + 발주처 통보

**KBIMS Checker 자동화 연동:**
```bash
# KBIMS Checker CLI 실행 (국토부 무료 배포)
kbims-checker --ifc model.ifc --standard MOLIT2023 --output report.json
# 결과 파싱: 통과/실패 항목 추출
python parse_kbims_report.py report.json
```
- 관련: [[IFC_OpenBIM]] · [[EIRBEP_심사원]] · [[QA_테스터]] · [[ACC_BIM360]]

## BIM 납품검수 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: 납품거절, 검수기준변경, IDS통과실패, 발주처담당교체, 실무부적합

**현장에서 납품 검수 거절 당하는 현실적 이유 5가지와 대응법**:
① 파일명 규칙 단 1건 위반 — BEP에 명시된 파일명 규칙(`[프로젝트코드]_[공종]_[단계]_[날짜]`)에서 언더스코어 대신 공백을 쓰거나 날짜 형식이 다른 경우 전체 납품물 반려. 대응: 납품 전 Python 정규식으로 파일명 일괄 자동 검증 스크립트 실행.
② Hard Clash 1건이라도 미해소 — 검수 기준이 "Hard Clash 0건"인 상태에서 덕트 vs 구조 보 클래시 1건이 남아있는 경우 전체 납품 반려. 대응: Navisworks 클래시 보고서에서 "Approved" 처리 없이 "Active" 상태로 남은 건수를 납품 전날 재확인.
③ 필수 파라미터 입력률 95% 미만 — 자동 검증 도구 없이 "다 입력했다"고 믿는 경우 스케줄로 빈값 필터링 시 탈락. 대응: Revit 일람표에서 필수 파라미터를 열로 추가하고 빈값 필터를 걸어 0건 달성 확인.
④ IFC Export 좌표계 불일치 — 특정 공종이 Internal Origin으로 내보내 다른 공종과 수십 미터 오프셋. 대응: 납품 전 Navisworks에 전 공종 IFC 통합 후 그리드 오버레이 확인.
⑤ LOD 달성 수준 미달 — 발주처가 샘플 20개 요소를 선택해 LOD 300 기준 치수·파라미터 완결성을 직접 확인 시 일부 요소가 LOD 200 수준으로 미달. 대응: LOD 기준표 대비 공종별 자체 샘플링 점검 후 미달 요소 목록 작성 및 사전 보완.

**발주처 담당자 교체 시 검수 기준 변경 리스크 관리**: 기존 담당자와 합의한 검수 기준을 신임 담당자가 번복하거나 추가 요구사항을 제시하는 경우, 기존 합의 근거가 없으면 대응이 어렵다. 예방 원칙: ① 모든 검수 기준 합의는 BEP 서명본으로 문서화하고 ACC에 Published 상태로 보관. ② 담당자 교체 발생 시 신임 담당자에게 BEP 브리핑 회의를 요청하고, 기존 합의 사항 재확인 확인서를 이메일로 수령. ③ 기존 합의 범위 초과 요구는 "변경 계약 대상"임을 명시하고, 이에 동의할 경우에만 이행. ④ 납품 이력(과거 승인된 모델 버전)을 ACC 버전 이력으로 제시하여 "이전에 같은 기준으로 승인된 납품물"임을 입증.

**IDS 검증 통과했지만 실무 부적합 판정 받는 경우**: IDS 기계 검증(ifctester 또는 Solibri)은 통과했으나 발주처 BIM 담당이 "실제 현장에서 쓸 수 없는 모델"이라며 부적합 판정을 내리는 패턴. 주요 원인: ① 파라미터 값이 채워져 있으나 의미 없는 더미 데이터(예: 제조사명 = "TBD", 모델번호 = "00000") — IDS는 존재 여부만 검증하므로 통과되지만 실무 부적합. 대응: IDS 규칙에 정규식 패턴 검증(`<Value type="pattern">[^T][^B][^D].*</Value>`) 추가. ② 형상은 있으나 MEP 커넥터 미연결 — Revit 경고는 없지만 실제 배관 계통이 끊어진 상태. 대응: Revit MEP 시스템 완결성 검사(`Systems` 탭의 "Unconnected" 필터로 미연결 요소 0건 확인). ③ 공간(Space) 미배치 구역 — IFC에 IfcSpace가 존재하지만 일부 구역 공간이 누락된 경우 FM 시스템 데이터 연동 불완전. 대응: 납품 전 "All Rooms/Spaces" 일람표에서 미배치 공간 0건 확인.

- 관련: [[IFC_OpenBIM]] · [[EIRBEP_심사원]] · [[QA_테스터]] · [[ACC_BIM360]]

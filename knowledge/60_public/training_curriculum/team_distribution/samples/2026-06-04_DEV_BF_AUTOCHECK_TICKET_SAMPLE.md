# 2026-06-04 개발 R D BF 자동검수 티켓 샘플

문서상태: 내부 교육 샘플  
작성일: 2026-06-04  
역할: 개발/R&D, QA_테스터, BIM 모델러, PM, BIM 납품검수  
연결 지식: `knowledge/60_public/training_curriculum/team_distribution/samples/2026-06-04_QA_BF_AUTOCHECK_RULE_CANDIDATE_SAMPLE.md`  
사용 KST 코드: `KST01 공식확인`, `KST03 적용주의`, `KST04 자동수집`

---

## 1. 티켓 목적

BF/편의시설 자동검수 룰 후보를 Revit Add-in 또는 Model Quality Auditor 기능 요구사항으로 전환한다. 이 티켓은 BF 적합 판정 엔진을 만드는 것이 아니라, 모델 내 누락·입력·증빙·장애물 후보를 찾아 PM/RFI와 수동 검토로 넘기는 리포트 기능을 정의한다.

핵심 원칙:
- 자동검수는 후보 탐지와 증빙 정리를 담당한다.
- 대상시설, 의무/권장, 예비인증/본인증, 지자체 조건은 자동 확정하지 않는다.
- 보고서에는 BF 불합격, 인증 통과, 법규 적합 확정 표현을 넣지 않는다.
- Revit API 구현은 실기 검증 전까지 확정하지 않는다.

## 2. 개발 티켓 요약

| 항목 | 내용 |
|---|---|
| Ticket ID | DEV-BF-AUTOCHECK-001 |
| 제목 | BF/편의시설 자동검수 후보 리포트 기능 |
| 목표 | 모델 내 BF 검토 후보를 수집하고 QA 상태와 KST 상태를 함께 출력한다. |
| 입력 | Revit 요소, 카테고리/패밀리명, 지정 파라미터, 도면/뷰/RFI/BCF 링크, 인증 단계 필드 |
| 출력 | BF 자동검수 후보 리포트, 누락 목록, 수동 확인 요청 이슈, QA 상태 |
| 제외 | BF 적합 판정, 인증 통과 판정, 법률 자문, 지자체 조건 확정, 자동 설계 변경 |
| 우선순위 | P2 |
| 개발 상태 | 요구사항 정의 / Revit API 실기 검증 전 |

## 3. 기능 요구사항

| REQ ID | 요구사항 | KST | 결과 상태 |
|---|---|---|---|
| REQ-BF-001 | BF 검토 대상 공간/구역 태그 존재 여부를 확인한다 | `KST04` | PASS/FAIL |
| REQ-BF-002 | 접근로, 주차, 출입구, 복도, 승강기, 화장실, 안내설비 객체 존재 후보를 수집한다 | `KST04` | PASS/FAIL |
| REQ-BF-003 | BF 관련 파라미터의 빈값, TBD, 00000, 미정 값을 탐지한다 | `KST04` | FAIL |
| REQ-BF-004 | 도면 번호, 모델 뷰, BCF, RFI, 체크리스트 링크 존재 여부를 확인한다 | `KST04` | PASS_WITH_NOTES/FAIL |
| REQ-BF-005 | 문, 복도, 화장실, 접근로 주변 장애물 후보를 이슈로 생성한다 | `KST04` | PASS_WITH_NOTES |
| REQ-BF-006 | 예비인증/본인증/미대상 필드가 비어 있으면 PM 확인 요청 이슈를 생성한다 | `KST03` | BLOCKED |
| REQ-BF-007 | 보고서에 인증 통과 보장 문구가 들어가지 않도록 템플릿을 제한한다 | `KST03` | FAIL |

## 4. 데이터 스키마 초안

```json
{
  "rule_id": "BF-QA-001",
  "rule_name": "BF 검토 대상 공간 태그 존재",
  "kst_state": "KST04",
  "qa_status": "QA_PASS_WITH_NOTES",
  "element_id": "123456",
  "category": "Rooms",
  "view_name": "A-101 BF Review",
  "evidence_links": {
    "drawing_no": "A-101",
    "rfi_id": "RFI-BF-001",
    "bcf_id": "BCF-004"
  },
  "message": "자동검수 후보입니다. BF 적합 판정 또는 인증 통과 판정이 아닙니다.",
  "next_action": "PM/RFI 확인 필요"
}
```

## 5. QA 상태 매핑

| 내부 상태 | 의미 | UI/보고서 문구 |
|---|---|---|
| QA_PASS | 자동검수 후보 항목 입력 완료 | 수동 검토로 전달 |
| QA_PASS_WITH_NOTES | 후보 탐지는 통과했지만 KST03 주의가 남음 | PM/RFI 확인 병행 |
| QA_BLOCKED | 대상성, 인증 단계, 지자체 조건 정보 부족 | 적용 기준 회신 대기 |
| QA_FAIL | 누락, 더미 값, 증빙 미비, 금지 문구 발견 | 수정 또는 재검토 필요 |

금지 문구:
- BF 불합격
- BF 인증 통과
- 법규 적합 확정
- 자동검수 기준상 수정 지시 필요

허용 문구:
- 자동검수 후보
- 수동 검토 필요
- PM/RFI 확인 필요
- 증빙 링크 누락
- 적용 기준 회신 대기

## 6. Revit API 검토 게이트

| 게이트 | 확인 내용 | 상태 |
|---|---|---|
| API-BF-001 | 대상 카테고리와 패밀리명 매핑이 프로젝트별로 달라질 수 있는가 | 실기 검증 필요 |
| API-BF-002 | Room/Space/Area와 BF 구역 태그 연결 방식이 안정적인가 | 실기 검증 필요 |
| API-BF-003 | 링크 모델의 BF 요소를 읽어야 하는가 | 요구사항 확인 |
| API-BF-004 | 보고서만 생성하고 모델을 수정하지 않는 dry-run 구조인가 | 필수 |
| API-BF-005 | 대형 모델에서 FilteredElementCollector 성능 문제가 없는가 | 성능 테스트 필요 |

## 7. 테스트 케이스

| TC ID | 시나리오 | 기대 결과 |
|---|---|---|
| TC-DEV-BF-001 | BF 태그 없는 공간 모델 | QA_FAIL, 누락 위치와 뷰 출력 |
| TC-DEV-BF-002 | 인증 단계 필드가 비어 있음 | QA_BLOCKED, PM/RFI 확인 요청 |
| TC-DEV-BF-003 | 도면 링크는 있으나 BCF/RFI 없음 | QA_PASS_WITH_NOTES, 증빙 누락 경고 |
| TC-DEV-BF-004 | 보고서 템플릿에 “인증 통과” 문구 포함 | QA_FAIL, 템플릿 차단 |
| TC-DEV-BF-005 | 링크 모델 요소 포함 프로젝트 | 링크 모델 처리 요구사항 확인 이슈 생성 |
| TC-DEV-BF-006 | 대형 모델 5만 요소 이상 | 실행 시간과 메모리 사용량 기록 |

## 8. 보안·데이터 기준

- 고객명, 프로젝트명, 모델 경로, 담당자 연락처는 리포트 외부 공유본에서 익명화한다.
- 요소 ID, 카테고리, 뷰명, 도면 번호는 업무상 필요한 범위로만 남긴다.
- 원본 모델 업로드 기능은 이 티켓 범위에서 제외한다.
- 오류 로그에는 인증 문서 원문, 고객 모델 경로, 사용자 이름을 남기지 않는다.

## 9. 개발 완료 기준

Pass:
- 요구사항과 제외 범위가 분리돼 있다.
- QA 상태와 KST 상태가 함께 출력된다.
- 보고서 문구가 CS/PM 응답 기준과 충돌하지 않는다.
- Revit API 실기 검증 전 항목이 명확히 표시돼 있다.
- dry-run/report-first 구조가 유지된다.

Revise:
- BF 적합 또는 인증 통과를 자동 판정하려 한다.
- KST03 항목을 자동 합격 처리한다.
- 모델을 자동 수정하는 기능이 포함돼 있다.
- 고객 민감정보가 리포트나 로그에 남는다.

## 10. 다음 액션

- 개발/R&D: 도메인 모델과 리포트 JSON 스키마 초안을 작성한다.
- QA_테스터: TC-DEV-BF-001~006을 회귀 테스트 후보로 등록한다.
- PM: 링크 모델 처리와 인증 단계 필드 제공 여부를 RFI로 확인한다.
- BIM 모델러: 실제 샘플 모델에서 BF 구역 태그와 증빙 링크 입력 방식을 확인한다.
- 다음 검토일: 2026-06-11

## 11. 관련 문서

- `knowledge/60_public/training_curriculum/team_distribution/samples/2026-06-04_QA_BF_AUTOCHECK_RULE_CANDIDATE_SAMPLE.md`
- `knowledge/60_public/training_curriculum/team_distribution/samples/2026-06-04_PM_BF_RFI_MEETING_AGENDA_SAMPLE.md`
- `knowledge/60_public/training_curriculum/team_distribution/samples/2026-06-04_CS_BF_EVIDENCE_RESPONSE_SAMPLE.md`
- `knowledge/10_agents/90_확장에이전트/프로그램개발.md`
- `knowledge/10_agents/90_확장에이전트/R&D_개발지원그룹.md`
- `knowledge/10_agents/90_확장에이전트/QA_테스터.md`

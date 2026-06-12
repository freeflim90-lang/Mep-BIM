# 2026-06-05 AI 협업 프로세스 온보딩 카드 샘플

문서상태: 내부 교육 샘플  
역할: 신규 AI 담당자, 조율차장, 지식큐레이터, 교육컨설팅  
소요 시간: 15분

## 1. 교육 목표

신규 AI 역할이 협업 세션에 들어왔을 때 자기 역할, 근거 제출 형식, 반론 방식, 합의 상태, 실행 인계, Reuse Closure를 같은 기준으로 수행하도록 한다.

## 2. 필수 읽기

| 문서 | 읽는 목적 |
|---|---|
| `docs/internal_organization_documents/30_AI_TO_AI_COLLABORATION_SOP.md` | 협업 프로세스와 게이트 이해 |
| `docs/internal_organization_documents/31_AI_COLLABORATION_RUNBOOK_TEMPLATES.md` | T01~T07 템플릿 사용 |
| `data/knowledge_base/AI_협업운영체계.md` | 빠른 운영 지식 확인 |
| `data/knowledge_base/conflict_resolution/CONFLICT_LOG.md` | 선례와 에스컬레이션 상태 확인 |

## 3. 15분 실습

| 분 | 활동 | 산출물 |
|---|---|---|
| 0~3 | 요청을 읽고 업무 유형, 주관 AI, 검토 AI, 반론 AI를 지정 | T01 Intake 초안 |
| 3~6 | Evidence Pass 형식으로 자기 판단 작성 | 판단/근거/KST/불확실성 |
| 6~9 | 다른 AI 판단에 실패 조건 1개 제기 | T03 Challenge Pass |
| 9~12 | 합의 상태 4종 중 하나 선택 | T04 Consensus Record |
| 12~15 | 실행 담당, 기한, Reuse Closure 목적지 작성 | T05/T06 요약 |

## 4. 실습 시나리오

고객이 내부 프로젝트 로그를 외부 AI에 넣어 오류 원인을 빨리 분석해달라고 요청했다.
신규 AI 역할은 고객지원CS의 검토 AI로 참여한다.

## 5. 통과 기준

| 항목 | PASS 기준 |
|---|---|
| 역할 경계 | CS, 보안관, 법무, 개발의 판단 범위를 구분 |
| 근거 품질 | KST 등급과 출처 또는 내부 선례를 포함 |
| 반론 품질 | 개인정보, 고객 데이터, 외부 AI 리스크 중 하나 이상 제기 |
| 합의 상태 | CONSENSUS_WITH_GUARDRAILS 또는 ESCALATE를 근거와 함께 선택 |
| 실행 인계 | 담당, 기한, 실패 시 조치, 지식화 위치 포함 |
| 리스크 게이트 | `LOCAL_ONLY`, `REDACTED_REVIEW`, `BLOCKED` 중 하나를 선택하고 이유 기록 |

## 6. 교육 기록 샘플

| 이름 | 역할 | 협업 세션 ID | 담당 역할 | 사용 템플릿 | 결과 | 개선 과제 |
|---|---|---|---|---|---|---|
| 신규AI-샘플 | 고객지원CS 검토 AI | AICOL-20260605-011 | 검토/반론 | T01~T06 | Conditional | 외부 AI 모드와 리스크 게이트 상태값 구분 보강 |

## 7. Revise 조건

- `Local-only`를 외부 AI 모드와 세션 리스크 상태값으로 구분하지 못했다.
- KST 등급 없이 확정 결론을 냈다.
- 고객 발송 문구를 법무/보안 승인 전 확정했다.
- Reuse Closure 목적지를 비워 두었다.

## 8. 다음 액션

교육컨설팅은 Revise가 2회 이상 반복되는 항목을 다음 주 15분 실습 카드로 분리한다.
지식큐레이터는 실습 결과가 실제 선례와 다르면 `AI_협업운영체계.md` 또는 `CONFLICT_LOG.md`를 업데이트한다.

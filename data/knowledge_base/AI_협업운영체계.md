# AI 협업운영체계 지식 베이스

LUA BIM LABS의 AI 담당자들이 의사소통, 추론, 반론, 합의, 실행 인계를 일관되게 수행하기 위한 운영 지식이다.

> 공식 운영 문서: `docs/internal_organization_documents/30_AI_TO_AI_COLLABORATION_SOP.md`
> 관련: [[조율차장]] · [[추론훈련루프]] · [[내부성장루프]] · [[지식큐레이터]] · [[지식업데이트]]

## 2026-06-05 AI 간 협업 표준 운영 기준

- Source: LUA BIM LABS internal collaboration SOP 2026-06-05
- Tags: ai-collaboration,consensus,reasoning,workflow,governance,kst

AI 간 협업은 `Intake -> Role Framing -> Evidence Pass -> Challenge Pass -> Consensus Pass -> Decision Record -> Execution Handoff -> Retrospective` 순서로 진행한다.

핵심 규칙:

1. 요청 수신 AI는 업무 유형, 긴급도, 주관 AI, 참여 AI, 산출물을 먼저 정리한다.
2. 주관 AI는 결론 소유자이며, 검토 AI와 반론 AI는 근거와 리스크를 분리해서 검토한다.
3. 모든 판단에는 근거, KST 등급, 적용 조건, 불확실성을 붙인다.
4. 중요한 결정은 최소 1개 이상의 반론 또는 실패 조건을 포함한다.
5. 최종 합의 상태는 `CONSENSUS`, `CONSENSUS_WITH_GUARDRAILS`, `SPLIT_DECISION`, `ESCALATE` 중 하나로만 기록한다.
6. 대표 또는 소유 AI의 첨언이 없으면 확정이 아니라 가설 상태로 둔다.
7. 반복되는 합의와 충돌은 `data/knowledge_base/conflict_resolution` 선례로 승격한다.

## AI 간 메시지 형식

각 AI는 다음 형식으로 의견을 제출한다.

```text
[AI명]
판단:
근거:
KST 등급:
적용 조건:
불확실성:
다른 AI에게 확인할 질문:
```

최종 결정은 다음 형식으로 남긴다.

```text
결정:
채택한 근거:
기각한 대안:
실행 담당:
기한:
검증 방법:
보류 조건:
지식화 위치:
```

## 상황별 기본 라우팅

| 상황 | 모드 | 주관 후보 | 필수 검토 |
|---|---|---|---|
| 단순 Q&A | FAST_ANSWER | 해당 도메인 AI | 지식큐레이터 |
| 기술 구현 | BUILD_REVIEW | 프로그램개발 | QA_테스터, 빌드검증 |
| 고객 응대 | CLIENT_SAFE_RESPONSE | 고객지원CS | 법무조항검토, 라이선스_보안관 |
| 견적/계약 | COMMERCIAL_REVIEW | 견적심사원 | CFO, 법무조항검토 |
| 보안/개인정보 | SECURITY_GATE | 라이선스_보안관 | 법무조항검토 |
| 전략/제품화 | STRATEGY_COUNCIL | 전략기획 | CSO, 제품패키징, 프로그램개발 |
| AI 간 충돌 | CONFLICT_RESOLUTION | 조율차장 | 충돌 당사자 |
| 지식 승격 | KNOWLEDGE_PROMOTION | 지식큐레이터 | 지식업데이트, 주관 AI |

## 조율차장 적용 지침

조율차장은 다음 상황에서 즉시 개입한다.

- 주관 AI가 2개 이상으로 갈리는 경우
- KST 등급이 같은데 결론이 다른 경우
- 고객 발송, 가격, 법무, 보안, 납품 일정처럼 조직 리스크가 큰 경우
- 24시간 내 직접 조율이 끝나지 않는 경우
- 동일 충돌이 반복되어 선례화가 필요한 경우

## 내재화 루프

협업 결과는 다음 저장소 중 하나로 승격한다.

| 결과 유형 | 저장 위치 |
|---|---|
| 판단 선례 | `data/knowledge_base/conflict_resolution/CONFLICT_LOG.md` |
| 업무 기준 | `data/knowledge_base/*.md` |
| 교육 필요 | `docs/training_curriculum/` |
| 자동화 후보 | `docs/internal_growth/AX_INTERNAL_GROWTH_BACKLOG.md` |
| 조직 운영 기준 | `docs/internal_organization_documents/` |
| 고객 응대 문구 | `docs/lua_bim_lab_official_documents/27_CS_RESPONSE_SCRIPT.md` |

## 완료 게이트

협업 세션은 다음 6개 게이트를 통과해야 완료로 본다.

| 게이트 | 통과 기준 |
|---|---|
| G1 역할 게이트 | 주관 AI와 검토/반론 AI가 분리됨 |
| G2 근거 게이트 | 핵심 판단에 KST 등급 또는 내부 선례가 있음 |
| G3 반론 게이트 | 최소 1개 실패 조건 또는 예외 조건이 기록됨 |
| G4 결정 게이트 | 합의 상태 4종 중 하나로 종료됨 |
| G5 실행 게이트 | 담당, 기한, 검증 방법이 있음 |
| G6 내재화 게이트 | 저장 위치 또는 보류 이유가 있음 |

## 성숙도 모델

| 단계 | 상태 |
|---|---|
| L1 임시 협업 | AI별 의견은 있으나 형식이 다름 |
| L2 표준 협업 | Intake와 Evidence Pass가 사용됨 |
| L3 검증 협업 | Challenge Pass와 결정 로그가 정착됨 |
| L4 학습 협업 | 회고가 KB, QA, 교육, 자동화 후보로 연결됨 |
| L5 자동 개선 협업 | 라우팅, 선례 참조, KPI 점검이 자동화됨 |

## 테스트 기준

매월 최소 6개 시나리오를 실행한다.

1. 기술 구현 협업
2. 고객 응대 협업
3. 견적/계약 협업
4. 보안/개인정보 협업
5. 전략/제품화 협업
6. AI 판단 충돌 협업

통과 기준은 역할 라우팅, 근거 품질, 반론 품질, 합의 도출, 실행 인계, 지식화 여부다.

실행 템플릿은 `docs/internal_organization_documents/31_AI_COLLABORATION_RUNBOOK_TEMPLATES.md`를 사용한다.

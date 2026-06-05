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
| QA/체크리스트 | `data/knowledge_base/qa/*.md` 또는 `docs/internal_organization_documents/16_INTERNAL_QUALITY_AUDIT_CHECKLIST.md` |
| 교육 필요 | `docs/training_curriculum/` |
| 표준문서 | `docs/standard_documents/` |
| 자동화 후보 | `docs/internal_growth/AX_INTERNAL_GROWTH_BACKLOG.md` |
| 조직 운영 기준 | `docs/internal_organization_documents/` |
| 고객 응대 문구 | `docs/lua_bim_lab_official_documents/27_CS_RESPONSE_SCRIPT.md` |
| 의사결정 로그 | `docs/internal_organization_documents/12_DECISION_LOG_TEMPLATE.md` 또는 프로젝트별 결정 로그 |

## 완료 게이트

협업 세션은 다음 6개 게이트를 통과해야 완료로 본다.

| 게이트 | 통과 기준 |
|---|---|
| G1 역할 게이트 | 주관 AI와 검토/반론 AI가 분리됨 |
| G2 근거 게이트 | 핵심 판단에 KST 등급 또는 내부 선례가 있음 |
| G3 반론 게이트 | 최소 1개 실패 조건 또는 예외 조건이 기록됨 |
| G4 결정 게이트 | 합의 상태 4종 중 하나로 종료됨 |
| G5 실행 게이트 | 담당, 기한, 검증 방법이 있음 |
| G6 내재화 게이트 | Reuse Closure 상태가 Created, Updated, 또는 Explicitly Deferred임 |
| G7 리스크/배포 게이트 | 데이터/외부AI/고객/가격 리스크가 해당 시 기록됨 |

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

## 신규 AI 역할 온보딩

신규 AI 역할은 실제 협업 세션에 들어가기 전에 `docs/training_curriculum/team_distribution/samples/2026-06-05_AI_COLLABORATION_ONBOARDING_CARD_SAMPLE.md`로 15분 실습을 수행한다.

온보딩 통과 기준:
- 자기 역할이 주관, 검토, 반론, 결정권자 중 무엇인지 구분한다.
- Evidence Pass에 판단, 근거, KST 등급, 적용 조건, 불확실성을 포함한다.
- Challenge Pass에 실패 조건 또는 예외 조건을 최소 1개 남긴다.
- 합의 상태를 `CONSENSUS`, `CONSENSUS_WITH_GUARDRAILS`, `SPLIT_DECISION`, `ESCALATE` 중 하나로만 기록한다.
- 실행 담당, 기한, 검증 방법, Reuse Closure 목적지를 비워 두지 않는다.
- 고객/개인정보/가격/외부 AI가 포함되면 리스크 게이트 상태값 6개 중 하나를 선택한다.

실제 내재화는 샘플 카드 작성만으로 보지 않는다. 최소 2개 협업 세션에서 교육 기록, 개선 과제, Reuse Closure 증거가 누적되어야 한다.

2026-06-05 기준 `AITEST_20260605_012`에서 신규 AI 온보딩 카드 샘플 2회 적용은 통과했다.
다만 월간 운영 정착은 실제 운영 세션에서 월 2회 이상 기록이 반복 누적되는지 별도로 본다.

## 2026-06-06 글로벌 멀티에이전트 AI 프레임워크 동향 및 LUA BIM LABS 협업 체계 연계
- Source: LangGraph 2026 Enterprise 리포트, CrewAI vs LangGraph 비교 분석, MCP Linux Foundation 이관 문서
- Tags: multi-agent,LangGraph,CrewAI,MCP,agentic-ai,enterprise,2026

**2026년 멀티에이전트 AI 오케스트레이션 프레임워크 현황:**
| 프레임워크 | 특징 | 주요 강점 | LUA BIM LABS 적합성 |
|----------|------|---------|-----------------|
| **LangGraph** | 그래프 기반 DAG 오케스트레이션 | 엔터프라이즈 감사 추적·체크포인트·롤백 | 복잡한 BIM 검토 파이프라인 |
| **CrewAI** | 역할 기반 Crew DSL | 빠른 프로토타이핑(20줄 시작) | AI 역할 온보딩 실험 |
| **AutoGen** (Microsoft) | 대화형 에이전트 협업 | 코드 생성·실행 통합 | 개발팀 자동화 |
| **OpenAI Agents SDK** | 핸드오프 기반 | GPT-4o 기반 엔터프라이즈 | 레거시 OpenAI 통합 |
| **Google ADK** | Vertex AI 통합 | GCP 네이티브 | 클라우드 BIM 워크플로우 |

**MCP (Model Context Protocol) — 2025~2026 표준화:**
- 2025년: Anthropic이 MCP 규격을 Linux Foundation으로 이관 → 사실상 산업 표준
- VS Code, JetBrains, 주요 AI 프레임워크가 MCP 네이티브 지원
- **LUA BIM LABS 연결점**: Claude Code가 MCP 서버를 통해 Revit/Navisworks에 직접 연결하는 BIM-AI 통합 아키텍처 구현 가능 (Revit 2027 AI Assistant MCP 연동)
- MCP 서버 예시:
  ```
  Claude Code (MCP 클라이언트)
    → mcp-server-revit: Revit API 직접 호출
    → mcp-server-ifc: ifcopenshell 기반 IFC 파싱
    → mcp-server-bim360: ACC BIM 360 데이터 연동
  ```

**엔터프라이즈 AI 채택 현황 (2026 Q2):**
- 대기업의 **2/3가 에이전틱 AI를 프로덕션 운영** 중 (2025년 말 1/3에서 급증)
- 권장 전략: CrewAI(빠른 실험) → LangGraph(프로덕션 스케일) → Agentforce(엔터프라이즈 클라이언트)

**LUA BIM LABS 내부 AI 협업 체계와 글로벌 트렌드 연계:**
- 현재 LUA BIM LABS의 Evidence Pass / Challenge Pass / Risk Gate 체계는 **LangGraph의 Human-in-the-Loop 체크포인트 패턴**과 구조적으로 동일
- CONSENSUS / ESCALATE 상태 관리는 **CrewAI 프로세스 타입(Sequential/Hierarchical)** 개념과 매핑 가능
- 향후 로드맵: 내부 AI 협업 로그(CONFLICT_LOG, AITEST 기록)를 LangSmith 옵저버빌리티 형식으로 자동 수집 → AI 의사결정 감사 추적 고도화

관련: [[프롬프트엔지니어]] · [[Revit_Addin]] · [[ACC_BIM360]] · [[conflict_resolution/README]]

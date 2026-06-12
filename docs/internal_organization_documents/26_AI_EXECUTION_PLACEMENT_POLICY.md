# LUA BIM LAB
# AI 실행 배치 기준

━━━━━━━━━━━━━━━━━━━━

문서번호: LBL-ORG-026  
문서상태: 내부 운영 기준  
작성일: 2026-05-22  
배포등급: Internal Only  
적용범위: DeepSeek API, Qwen Coder, 로컬 지식 검색, Telegram 요청, 지식 큐레이션, 개발/자동화 요청

## 1. 목적

본 문서는 LUA BIM LABS 조직에서 DeepSeek API와 로컬 AI/Qwen/규칙 기반 처리를 어떤 업무에 배치할지 정의한다.

핵심 원칙은 `일상 운영은 로컬, 전략 판단은 월 $50 한도 내 DeepSeek, 민감정보는 항상 로컬`이다.

## 1.1 월 지원 예산 전제

DeepSeek API는 월 `USD 50` 지원분을 기준으로 운영한다. 이 예산은 일상 질문 처리비가 아니라 조직 성장 판단을 보강하는 전략 예산으로 본다.

| 예산 구간 | 권장 배정 | 사용 대상 |
|---|---:|---|
| 상품화/사업성 판단 | 45% / 약 USD 22.50 | 수익형 아이템 우선순위, 가격, MRR, 손익분기 |
| Autodesk Store 전략 | 25% / 약 USD 12.50 | 제품 포지셔닝, 스토어 설명 방향, 출시 리스크 |
| 조직/로드맵 전략 | 20% / 약 USD 10.00 | 개발 순서, 조직 성장 방향, 시장성 판단 |
| 예비 버퍼 | 10% / 약 USD 5.00 | 긴급 전략 검토 또는 월말 보정 |

예산 추정 기록은 `data/ai_usage/deepseek_monthly_budget.json`에 남긴다.

## 2. AI 배치 원칙

| 구분 | 기본 배치 | 이유 |
|---|---|---|
| 팀원 Telegram 지식질문 | 로컬 지식/Obsidian | 내부 질문과 답변이 외부 API로 나가지 않도록 보호 |
| `더 찾아줘` 자동 보강 | 로컬 검색/수집 + needs-review 저장 | 수집 결과는 확정 지식이 아니라 후보 지식 |
| 일일 지식 큐레이션 | 규칙 기반 + 지식큐레이터 | 매일 반복 처리이므로 비용과 보안 리스크를 낮춤 |
| 관리팀 Excel 자동화 | Qwen Coder + 로컬 처리 | 개인정보/업무 데이터 가능성이 높음 |
| Telegram 영수증/증빙 정리 | 경비정산_AI + 로컬 처리 | 결제정보, 개인정보, 고객/프로젝트 정보 가능성이 높음 |
| 이력서 분석/인재 평가 | HR_인재분석관 + 로컬 처리 | 후보자 개인정보, 학력, 경력, 이전 회사/고객 정보가 포함됨 |
| 이력서 DeepSeek 보조 분석 | 기본 금지, 명시 옵션 시 마스킹 텍스트만 제한 허용 | 원본 PDF/개인정보 전송 금지, 로컬 추출 실패 시 사용 불가 |
| 코드 초안/자동화 초안 | Qwen Coder 우선 | 반복 개발 초안은 로컬에서 빠르게 생산 |
| 보안/개인정보/계약 검토 | 로컬 전용 | 외부 전송 금지 |
| 고객지원/라이선스/환불 | 로컬 전용 | 고객 정보와 결제 맥락 보호 |
| 상품화 우선순위/가격/사업성 | DeepSeek 제한 허용 | 민감정보 제거 후 전략 판단 품질 향상 목적 |
| Autodesk Store 전략/포지셔닝 | DeepSeek 제한 허용 | 공개 가능한 수준의 시장/메시지 판단 보강 |
| 조직 로드맵/수익화 판단 | DeepSeek 제한 허용 | 경영 판단 보조 목적 |
| 추론 트레이닝 최종 검토 | 로컬 결론 생성 후 DeepSeek Final Review | DeepSeek은 답변자가 아니라 논리 허점, 사업화 리스크, 다음 질문을 찾는 검토자로만 사용 |

## 2.1 모델 배치표

운영 설정은 `config/ai_model_routing.json`을 기준으로 한다.

| 모델/게이트 | 기본 모델 | 역할 | 사용 기준 |
|---|---|---|---|
| Local Knowledge QA | `qwen2.5:7b` | Telegram Q&A 합성, Obsidian 요약, 반복 지식화 | 내부 질문, 민감 가능성, 반복 처리 |
| Local Coder | `qwen2.5-coder:7b` | 코드/엑셀/자동화 초안 | Revit/Navisworks API 확정 전 초안, 로컬 개발 검토 |
| DeepSeek Final Review | `deepseek-v4-flash` | 추론 트레이닝 최종 검토 | 로컬 결론 + 대표 첨언 이후 민감정보 제거본만 전송 |
| DeepSeek High Stakes Strategy | `deepseek-v4-pro` | 고중요 사업성/가격/투자 검토 | `DEEPSEEK_HIGH_STAKES_REVIEW_ENABLED=true`일 때만 제한 사용 |

기본값은 `local_first_deepseek_final_review`이다. 즉 모든 업무는 로컬에서 먼저 판단하고, DeepSeek은 최종 검토 또는 전략 보강에만 사용한다.

## 3. DeepSeek API 허용 조건

DeepSeek API는 다음 조건을 모두 만족할 때만 사용한다.

1. `PAID_AI_ENABLED`가 활성화되어 있다.
2. 월 DeepSeek 예산 잔액이 남아 있다.
3. 요청이 전략, 사업성, 가격, 로드맵, 상품화, 스토어 포지셔닝과 관련되어 있다.
4. 고객명, 프로젝트명, 도면, 계약정보, 개인정보, 계정/토큰, 내부 경로가 포함되어 있지 않다.
5. 팀원/관리팀 1:1 Telegram 요청이 아니다.
6. 로컬/Qwen으로 충분히 처리 가능한 반복 업무가 아니다.

## 4. DeepSeek API 금지 조건

다음 신호가 있으면 DeepSeek API를 사용하지 않는다.

| 금지 신호 | 예시 |
|---|---|
| 개인정보 | 이름, 전화번호, 이메일, 주민번호, Telegram ID |
| 고객/프로젝트 정보 | 고객명, 프로젝트명, 도면, 계약조건 |
| 계정/보안 정보 | API key, token, secret, password, SSH, `.env` |
| 내부 경로 | `/Users/`, `/Volumes/`, 로컬 파일 경로 |
| 관리팀 데이터 | 급여, 근태, 정산, 구매, 자산, 라이선스 원장 |
| 영수증/증빙 데이터 | 영수증, 세금계산서, 거래명세서, 카드전표, 사업자번호 |
| 채용/이력서 데이터 | 이력서, 지원자명, 생년, 연락처, 학력, 경력, 이전 회사/고객명, 프로젝트명 |
| 팀원 1:1 요청 | 지식질문, 더 찾아줘, 개발, Excel 자동화 |

## 5. 담당별 배치

| 담당 | 기본 AI 배치 |
|---|---|
| 지식업데이트 | 로컬 |
| 지식큐레이터 | 로컬/규칙 기반 |
| 인프라_DevOps (Obsidian) | 로컬 |
| 경영지원/경비정산_AI | 로컬 |
| HR_인재분석관 | 로컬 |
| Qwen_Coder_8B | 로컬 |
| 엑셀자동화 | Qwen + 로컬 |
| QA_테스터/빌드검증 | 로컬 |
| 라이선스_보안관/법무조항검토 | 로컬 |
| 고객지원 CS/라이선스결제 | 로컬 |
| CEO/CFO/COO/전략기획/아이디어발굴 | DeepSeek 제한 허용 |
| 스토어심사/브랜드마케팅/견적심사원 | DeepSeek 제한 허용 |

## 6. 운영 흐름

1. 요청이 들어오면 먼저 담당 조직과 워크플로우를 라우팅한다.
2. 민감정보 신호를 검사한다.
3. 로컬 전용 워크플로우인지 확인한다.
4. 전략/상품화 판단이면 DeepSeek 허용 후보로 둔다.
5. 월 예산 잔액을 확인한다.
6. DeepSeek를 사용한 경우 월별 사용 추정치에 기록한다.
7. 결과 보고서에는 AI 배치 모드와 사유를 기록한다.

## 6.2 AI 협업 세션 배치 기준

AI가 2개 이상 참여하는 협업 세션은 `30_AI_TO_AI_COLLABORATION_SOP.md`를 적용하고, 실행 기록은 `31_AI_COLLABORATION_RUNBOOK_TEMPLATES.md`를 사용한다.

| 협업 단계 | 기본 배치 | DeepSeek 사용 가능 여부 |
|---|---|---|
| Intake | 로컬 | 불가 |
| Role Framing | 로컬 | 불가 |
| Evidence Pass | 로컬 지식/Obsidian 우선 | 공개 가능 전략 판단만 제한 허용 |
| Challenge Pass | 로컬 우선 | 민감정보 제거 후 전략 리스크 검토만 제한 허용 |
| Consensus Record | 로컬 | 불가 |
| Execution Handoff | 로컬 | 불가 |
| Retrospective | 로컬 | 공개 가능 조직 개선 가설만 제한 허용 |

금지:
- 고객명, 프로젝트명, 도면, 계약정보, 개인정보, 내부 경로가 포함된 협업 세션은 외부 API를 사용하지 않는다.
- 보안/개인정보/계약/고객 응대 세션은 DeepSeek가 결론을 확정하지 않는다.
- DeepSeek은 협업 참여자 또는 최종 결정권자가 아니라 제한된 검토자 역할로만 사용한다.

## 6.1 이력서 분석 예외 흐름

1. Telegram PDF 파일은 먼저 로컬 저장소에 내려받는다.
2. `pypdf`, `PyPDF2`, `pdfplumber`, `pdftotext` 중 설치된 로컬 추출기로 텍스트를 추출한다.
3. 로컬 추출이 실패하면 DeepSeek를 호출하지 않는다.
4. 로컬 추출 성공 후 개인정보 마스킹을 수행한다.
5. `RESUME_DEEPSEEK_FALLBACK_ENABLED=true`와 `PAID_AI_ENABLED=true`가 모두 활성이고 예산 잔액이 있을 때만 마스킹 텍스트를 DeepSeek 보조 분석에 사용할 수 있다.
6. 원본 PDF, 연락처, 주민번호, 생년월일, 주소, 고객/프로젝트 실명은 외부 API로 전송하지 않는다.

## 7. 관련 문서

- `21_KNOWLEDGE_CURATION_INTELLIGENCE_CELL.md`
- `30_AI_TO_AI_COLLABORATION_SOP.md`
- `31_AI_COLLABORATION_RUNBOOK_TEMPLATES.md`
- `24_TEAM_TELEGRAM_KNOWLEDGE_REQUEST_LOOP.md`
- `25_MANAGEMENT_EXCEL_AUTOMATION_APPROVAL_GATE.md`
- `knowledge/10_agents/09_지식팀/지식큐레이터.md`
- `knowledge/10_agents/90_확장에이전트/엑셀자동화.md`

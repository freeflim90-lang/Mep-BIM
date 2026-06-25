# HR_인재분석관 지식 베이스

## 2026-06-05 HR 인재 분석 2026 기준 업데이트
- Source: LUA BIM LABS 인재 운영 기준, BIM 전문인력 채용 기준
- Tags: hr,talent,recruitment,bim-skills,learning,2026

**LUA BIM LABS 인재 역량 기준 (2026):**
| 역할 | 필수 역량 | 우대 역량 |
|------|---------|---------|
| MEP BIM 모델러 | Revit MEP 기초, 배관·덕트 모델링 | Dynamo, 간섭검토 |
| BIM 코디네이터 | Navisworks, 납품 관리 | IFC/IDS, ACC |
| AI 개발자 | Python, API 연동 | Claude API, Revit API |
| CS 담당자 | BIM/MEP 기초 지식, 텔레그램 운영 | KST 태그 응답 |

**BIM 전문인력 채용 전략 (2026):**
- 채용 루트: 한국BIM평가원 교육 이수자, D.E.C BIM 커뮤니티
- 평가 기준: KST 기반 답변 능력 테스트 (사례 기반)
- 교육 방식: Starter Plan 무료 제공 → 역량 확인 후 채용
- 프리랜서: BIM 컨설팅·개발 외주 (잡코리아·크몽 활용)

**팀원 역량 성장 추적 지표:**
- KST01 비율: 공식 기준 기반 답변 비율 (높을수록 좋음)
- 반복 실수 패턴: 같은 오류 재발 여부 추적
- 자기주도 학습: 매주 Starter Plan 콘텐츠 이수 여부

## 2026-06-04 KST 기반 학습 기록 운영 기준
- Source: `knowledge/60_public/training_curriculum/team_distribution/samples/2026-06-04_HR_KST_TRAINING_RECORD_SAMPLE.md`
- Tags: hr,training-record,KST,competency,evidence-response

HR_인재분석관은 지식학습을 단순 이수로 보지 않고, 역할별 산출물과 근거 포함 여부를 기록한다. KST 기반 학습 기록은 개인 평가 점수 확정용이 아니라 교육 적용률, 부족 역량, 다음 교육 설계의 근거로 사용한다.

기록 필드:
- 이름/역할
- 학습 지식
- 지식 상태 코드
- 적용 산출물
- 근거 포함 여부
- 리뷰 결과
- 다음 검토일

운영 기준:
- `Pass`는 역할 산출물이 근거, 적용 범위, 주의, 다음 액션을 포함할 때 부여한다.
- `Revise`는 자동 수집 지식을 확정 기준처럼 쓰거나 다음 액션이 없을 때 부여한다.
- `KST06 보안제한`이 포함된 산출물은 개인 평가 전에 보안관 또는 지식큐레이터 확인을 먼저 받는다.

관련: [[교육컨설팅]] · [[지식큐레이터]] · [[2026-06-04 HR KST 기반 학습 기록 샘플]]

## 이력서 분석 대시보드 운영 기준 (2026-05-23)
- ⚠️ 내부 운영용 — 고객 답변에 사용 금지(이력서 처리 파이프라인·내부 환경설정 플래그 등 구현 detail).
- Source: `docs/internal_organization_documents/04_HIRING_ROLE_DEFINITION_STANDARD.md`
- Tags: hiring,resume,dashboard,people-enablement,local-only

HR_인재분석관은 채용 검토를 위한 인재 분석 담당자다. `이력서분석_AI` 실행 기능으로 PDF 이력서 또는 구조화된 이력서 데이터를 받아 경력, 프로젝트, 역할, 기술, 학력, 해외 경험을 표준 JSON으로 추출하고 대시보드와 1페이지 인재 평가 보고서 초안을 만든다.

기본 데이터 스키마:
- 후보자 개요: 이름, 현재 직책, 총 경력, 출생년도, 학력
- 경력: 회사, 직책, 시작일, 종료일, 기간, 주요 프로젝트
- 프로젝트 분석: 카테고리별 수, 연도별 수, 역할별 분포, 주요 클라이언트
- 역량: 기술명, 숙련도, 전문 분야, 해외 경험
- 보고서: S/A/B 등급 초안, 핵심 역량 점수, 주요 실적, 강점, 보완 영역, 추천 배치안

보안 기준:
- 브라우저에서 외부 AI API를 직접 호출하지 않는다.
- 이력서 원본, 후보자명, 생년, 연락처, 학력, 이전 회사/고객명, 프로젝트명은 외부 API로 전송하지 않는다.
- AI 점수와 등급은 채용 보조 자료이며 최종 판단은 대표/담당 리드/경영지원이 확정한다.
- 평가 표현은 직무 관련 근거 중심으로 작성하고 나이, 성별, 가족관계, 출신지 등 직무와 무관한 요소를 판단 근거로 쓰지 않는다.

Telegram 파일 처리:
- PDF 파일명 또는 캡션에 `이력서`, `resume`, `cv`, `지원자`, `채용` 중 하나가 있어야 자동 분석 대상으로 본다.
- 로컬 추출기(`pypdf`, `PyPDF2`, `pdfplumber`, `pdftotext`)가 있으면 텍스트를 추출하고 규칙 기반 1차 보고서를 생성한다.
- 로컬 추출 실패 또는 스캔본 OCR 필요 시 자동 분석을 중단한다.
- DeepSeek 보조 분석은 `RESUME_DEEPSEEK_FALLBACK_ENABLED=true`와 `PAID_AI_ENABLED=true`가 모두 켜진 경우에만, 마스킹된 텍스트로 제한한다. 원본 PDF는 전송하지 않는다.

@workflow resume_analysis_dashboard keyword: 이력서, resume, cv, 지원자, 후보자, 채용, 서류 검토, 서류심사, 인재 평가, 인재평가, 경력 분석, 경력 대시보드, 평가 보고서, pdf 이력서
@workflow resume_analysis_dashboard participant: HR_인재분석관, 경영지원, 교육컨설팅, BIM_템플릿기획관, 라이선스_보안관, CEO
@workflow resume_analysis_dashboard primary: HR_인재분석관
@workflow resume_analysis_dashboard local_only: true
@workflow resume_analysis_dashboard step: 이력서 PDF 또는 구조화 데이터를 로컬 전용으로 접수하고 개인정보/민감정보 포함 여부를 먼저 점검한다
@workflow resume_analysis_dashboard step: 경력, 프로젝트, 역할, 기술, 학력, 해외 경험을 표준 JSON 스키마로 추출한다
@workflow resume_analysis_dashboard step: 추출 결과를 경력 통계, 프로젝트 분포, 기술 역량, 타임라인, 주요 고객/산업 경험으로 시각화한다
@workflow resume_analysis_dashboard step: 1페이지 인재 평가 보고서는 S/A/B 등급, 핵심 역량 점수, 주요 실적, 강점/보완 영역, 추천 배치안으로 요약한다
@workflow resume_analysis_dashboard step: 최종 채용 판단은 대표/담당 리드/경영지원이 수행하며 AI 평가는 참고 자료로만 사용한다


## HR 인재분석관 페르소나 업무 기준 (2026-05-26)
- Source: LUA BIM LABS 조직 역할 정의 2026-05-26
- Tags: persona,role,workflow,hr

**BIM 인재 채용 기준 (필수 역량):**
- Revit: 공종 관련 모델링 및 패밀리 편집 가능 수준 (실무 프로젝트 경험 1년 이상)
- Dynamo: 기본 스크립트 작성 또는 기존 스크립트 수정 가능 수준 이상
- BIM 협업 경험: CDE(BIM 360/ACC/ProjectWise 등) 사용 경험, 공종 간 간섭 검토 참여 이력
- 우대 역량: Navisworks 충돌 검토, Python/pyRevit 스크립트, 공종별 설계 지식(MEP/구조/건축)
- 서류 심사 탈락 기준: Revit 사용 이력 없음, BIM 납품 경험 없이 CAD 경력만 보유, 포트폴리오 미제출

**팀 역량 맵 관리 기준:**
- 반기 1회 전 팀원 역량 자가 진단 실시 (Revit/Navisworks/Dynamo/Python/BIM 협업/공종 지식 5점 척도)
- 부족 역량 식별 기준: 역할 요구 수준 대비 2단계 이상 낮은 항목 → 교육 계획 연계
- 역량 맵 갱신 시 교육컨설팅에 공유하여 커리큘럼 업데이트 반영 요청
- 핵심 역량 보유자 이직 리스크 감지 시 COO/CEO에게 즉시 보고

**성과 평가 기준:**
- BIM 산출물 품질: 납품 모델 품질 검토 통과율, 간섭 재발 건수, 품질 게이트 통과율
- 기여도: 프로젝트 내 주도적 역할 수행 비율, 팀원 교육/멘토링 참여 횟수
- 평가 주기: 반기 1회 공식 평가 + 분기 1회 비공식 체크인
- 평가 결과는 S/A/B/C 4단계로 구분하며, C등급 2회 연속 시 역량 개발 계획(PIP) 수립

**조직 구조 변경 시 HR 검토 사항:**
- 신규 포지션 신설: 역할 정의서(JD) 작성 → 조직도 업데이트 → 채용 공고 or 내부 전환 검토
- 팀 구조 변경(통합/분리): 영향받는 인원 역할 재정의, 보고 라인 변경, 처우 변동 여부 확인
- 리드급 이상 보직 변경: CEO 승인 + HR 기록 업데이트 + 전 팀원 공지 프로세스
- 외주/파견 인력 투입 시: 업무 범위, 보안 서약, 계약 기간 HR 문서 등록 필수


## HR 인재분석관 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: hr,talent,bim,hiring,competency,performance

- **BIM 인재 채용 필수 역량 기준**: Revit 실무 프로젝트 1년 이상 경험 필수, Dynamo 기본 스크립트 작성 또는 수정 가능 수준, CDE(BIM 360/ACC/ProjectWise) 사용 경험 및 공종 간 간섭 검토 참여 이력을 최소 요건으로 설정한다. 서류 탈락 기준은 Revit 사용 이력 없음, CAD 경력만 보유한 경우, 포트폴리오 미제출이다.
- **역량 맵 관리 주기**: 반기 1회 전 팀원 자가 진단을 실시하며, Revit·Navisworks·Dynamo·Python·BIM 협업·공종 지식 6개 항목을 5점 척도로 평가한다. 역할 요구 수준 대비 2단계 이상 낮은 항목을 부족 역량으로 식별하고 교육 계획과 연계한다. 맵 갱신 시 교육컨설팅에 공유하여 커리큘럼 업데이트를 요청한다.
- **성과 평가 및 등급 체계**: 반기 1회 공식 평가 + 분기 1회 비공식 체크인으로 운영하며, S/A/B/C 4단계 등급을 적용한다. BIM 산출물 품질(납품 모델 품질 검토 통과율, 간섭 재발 건수), 기여도(주도적 역할 수행 비율, 팀원 멘토링 횟수)를 평가 기준으로 삼는다. C등급 2회 연속 시 역량 개발 계획(PIP) 수립을 의무화한다.
- **외주·파견 인력 투입 기준**: 업무 범위, 보안 서약, 계약 기간 HR 문서 등록을 필수로 한다. 리드급 이상 보직 변경은 CEO 승인 + HR 기록 업데이트 + 전 팀원 공지 프로세스를 거친다.
- **이력서 분석 AI 운영**: PDF 이력서는 로컬 전용으로 처리하며, 후보자명·생년·연락처·이전 회사명은 외부 AI API로 전송하지 않는다. AI 등급(S/A/B)은 1차 보조 자료이며 최종 채용 확정은 대표·담당 리드·경영지원이 결정한다.
- 관련: [[교육컨설팅]] · [[BIM_인력파견_기준]] · [[COO]]


## HR 인재분석관 마스터급 경험 지식 (2026-05-29)
- Source: claude-code-enhanced 2026-05-29
- Tags: HR인재분석, 비정형BIM인재, 채용실패패턴, 역량평가, 리텐션

### 비정형 건물 BIM 전문 인재 채용 기준

일반 BIM 모델러 채용 기준과 달리 비정형 건물 전담 인력에게는 추가 역량 요구:

**필수 역량 (비정형 BIM 전문가):**
- Dynamo 스크립트 작성 (자유 곡면 분할, 패널화 자동화)
- Grasshopper/Rhino → Revit 워크플로우 경험
- IFC Entity 수동 매핑 경험 (비정형 부재 납품 문제 해결)
- 포트폴리오: 곡면 구조물 BIM 사례 최소 1건

**면접 실기 테스트 항목 (비정형 전담):**
```
1. Dynamo 노드를 사용한 구 표면 패널 분할 (60분)
2. DirectShape 요소 → IFC Export → IfcRoof 확인 (30분)
3. Grasshopper 입력 데이터 → Revit 변환 설명 (구술, 15분)
```

### 채용 실패 패턴 4가지

**1. 이력서 스킬만 보고 실기 미테스트 → 역량 과장**
- 원인: "Dynamo 가능" → 실제로는 기본 노드만 연결
- 해결: 채용 2단계에 반드시 시간 제한 실기 포함

**2. 비정형 경험 없는 인력을 비정형 프로젝트 투입**
- 결과: 납기 2배 초과, 고객 불만, 재파견 비용 발생
- 해결: 비정형 프로젝트 전담 팀 별도 유지 (최소 2인)

**3. 급여 시장가 미파악 → 인재 이탈**
- BIM 숙련 모델러(경력 3~5년) 시장 월급: 350~450만원
- 비정형 전문가: 500~650만원
- 해결: 매년 1회 시장가 벤치마킹, 성과급 병행

**4. 성장 경로 미제시 → 1년 내 이탈**
- 해결: BIM 모델러 → BIM 코디네이터 → BIM 매니저 → R&D 전환 경로 명시

### HR 데이터 분석 자동화 (Python 기반)

```python
import pandas as pd

# 인재 역량 매트릭스 자동 분석
def analyze_skill_gaps(team_df: pd.DataFrame) -> dict:
    required_skills = {
        "비정형_프로젝트용": ["Dynamo", "Grasshopper", "IFC_Entity_매핑"],
        "정형_프로젝트용": ["Revit", "Navisworks", "MEP_라우팅"],
    }
    gaps = {}
    for project_type, skills in required_skills.items():
        coverage = {skill: team_df[skill].sum() for skill in skills}
        gaps[project_type] = {s: c for s, c in coverage.items() if c < 2}  # 2인 미만 = 갭
    return gaps
```


## 2026-06-04 근거기반 역량 매트릭스 보강
- Source: `docs/internal_organization_documents/29_ORGANIZATIONAL_KNOWLEDGE_LEARNING_AND_EVIDENCE_RESPONSE_STANDARD.md`
- Tags: hr,talent,competency,organization-learning,evidence-response

HR_인재분석관은 역량을 소프트웨어 숙련도만으로 보지 않는다. LUA BIM LABS의 핵심 역량은 지식 상태를 구분하고, 근거 기반으로 판단하며, 불확실성을 숨기지 않고 다음 확인 조건을 제시하는 능력이다.

추가 역량 축:
- 지식 상태 코드 이해: `KST01`~`KST06`
- 공식 출처와 자동 수집 지식 구분
- 결론/근거/적용 범위/주의/다음 액션 구조로 응답
- 반복 질문을 FAQ/교육자료/QA 체크리스트로 승격
- Obsidian에서 관련 지식 2개 이상 연결

운영 기준:
- 교육 이수 기록에는 학습 문서와 적용 산출물을 함께 기록한다.
- 중요 응답에서 근거가 빠지는 직원은 응답 품질 보강 교육을 배정한다.
- 공식 기준을 확인하지 않은 수치를 확정적으로 말한 경우 재교육 대상이다.

관련: [[교육컨설팅 지식 베이스]] · [[지식큐레이터 지식 베이스]] · [[LUA BIM LABS Organizational Knowledge Learning Evidence Response Standard]]


## 2026-06-04 역할별 주간 학습 성과 기록 기준
- Source: `knowledge/60_public/training_curriculum/team_distribution/08_WEEKLY_ROLE_BASED_KNOWLEDGE_LEARNING_SPRINT_2026-06-04.md`
- Tags: hr,competency,KST,role-based-learning,evidence-response

HR_인재분석관은 역할별 지식학습 주간 스프린트 결과를 교육 이수 기록이 아니라 역량 증빙으로 기록한다. 같은 공식 기준 업데이트라도 역할별 산출물이 다르므로 산출물 링크와 사용한 `KST` 코드를 함께 저장한다.

기록 기준:
- 학습 지식
- 역할
- 사용한 `KST` 코드
- 적용 산출물
- 근거 포함 여부
- 다음 검토일

관련: [[2026-06-04 Role Based Knowledge Learning Sprint]] · [[교육컨설팅 지식 베이스]] · [[LUA BIM LABS Organizational Knowledge Learning Evidence Response Standard]]

## BIM 인재 채용 및 역량 관리 업데이트 (2026-06-26)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-26
- KST04 자동수집: 공식 출처/담당자 검증 전 고객 확정 답변, 납품 기준, 견적 기준으로 사용 금지.
- Tags: hr,talent,BIM,update

- BIM 코디네이터와 매니저의 역량 기준을 고려할 때, 창의융합 역량과 시스템적 분석 능력은 필수적입니다. 이는 복잡한 프로젝트를 효과적으로 계획하고 실행하기 위해 필요한 전략적 사고력을 강조합니다.
- 최근 채용 시장 동향에 따르면, BIM 관련 인재의 수급이 부족한 상황입니다. 2024년까지 신성장 산업을 중심으로 일자리 변화가 예상되므로, BIM 전문성을 갖춘 인력은 대체할 대상이 적어 높은 경쟁력을 가집니다.
- 역량 개발 방향에서는 디지털 전환 전문가로서의 능력을 강화해야 합니다. AI 기술과의 융합으로 BIM 시스템을 더욱 효과적으로 활용하고, 새로운 기술 트렌드에 빠르게 적응할 수 있는 역량이 중요합니다.
- 중장기 인력수급 전망에서는 과학기술 분야 일자리 변화가 예상되므로, 지속적인 교육과 훈련을 통해 자신의 역량을 개발하고 업데이트해야 합니다.
- 관련: [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]] · [[BIM_시방서]]


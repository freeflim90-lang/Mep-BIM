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
- Source: `docs/training_curriculum/team_distribution/samples/2026-06-04_HR_KST_TRAINING_RECORD_SAMPLE.md`
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


## BIM 인재 채용 및 역량 관리 업데이트 (2026-05-28)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-28
- Tags: hr,talent,BIM,update

- BIM 코디네이터 및 매니저의 역량 기준: 프로젝트 관리, 4D 시뮬레이션, Dynamo와 Revit 같은 고급 소프트웨어 사용 능력이 요구된다.
- 채용 시장 동향: 2025년까지 BIM 관련 직무는 지속적으로 성장할 것으로 예상되며, 특히 반도체 산업 등 고급 기술 분야에서 전문적인 BIM 기술이 필요하게 될 것이다.
- 역량 개발 방향: 모델 관리와 협업 능력 강화를 통해 팀 작업의 효율성을 높이는 것이 중요하다. 또한, 지속적으로 새로운 BIM 소프트웨어 및 기술 트렌드에 대한 교육을 받는 것이 필요하다.


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


## BIM 인재 채용 및 역량 관리 업데이트 (2026-05-29)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-29
- Tags: hr,talent,BIM,update

- BIM 코디네이터와 매니저의 역량 기준: Revit, Navisworks 등 주요 소프트웨어 사용 능력 및 프로젝트 통합과 협업 능력이 필수입니다.
- 채용 시장 동향: 반도체와 R&D 분야에서 BIM 관련 전문 인력의 수요가 높아지고 있습니다. 2025년까지 이러한 산업 부문에서 BIM 기술을 구현할 수 있는 역량이 중요해질 것으로 예상됩니다.
- 역량 개발 방향: 디지털전환과 관련된 지식을 갖추고, 다양한 프로젝트 관리 경험을 쌓는 것이 필요합니다. 또한, 창의융합 역량을 강화하여 문제 해결 능력을 향상시킬 수 있는 교육이나 프로그램에 참여하는 것도 유익할 것입니다.
- 관련: [[건축]] · [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]]


## BIM 인재 채용 및 역량 관리 업데이트 (2026-05-30)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-30
- Tags: hr,talent,BIM,update

- BIM 코디네이터 및 매니저의 역량 기준: 4D 시뮬레이션, 프로젝트 관리 능력, 고급 모델링 등이 필수입니다.
- 채용 시장 동향: 2025년까지 BIM 관련 직무는 스마트 건설, 자동화 및 높은 기술 산업 분야에서 큰 수요를 보일 것으로 예상됩니다. Dynamo, Revit, Navisworks 등 주요 도구에 능숙함이 요구됩니다.
- 역량 개발 방향: 창의융합 역량을 강화하고, 시스템적 관점에서 문제를 분석하는 능력을 키워야 합니다. K-ACE(Korea Art, Culture, and Entertainment) 분야와 같은 글로벌 핵심역량도 중요합니다.
- 인력 수급 전망: 기업은 적절한 채용을 위해 중장기 인력수급 전망을 고려해야 하며, 현장 종사자의 정성적 판단도 함께 반영해야 합니다.
- 관련: [[건축]] · [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]]


## BIM 인재 채용 및 역량 관리 업데이트 (2026-05-31)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-31
- Tags: hr,talent,BIM,update

- BIM 코디네이터와 매니저의 역량 기준: 4D 시뮬레이션, 프로젝트 관리, 자동화 기술 등이 필수입니다.
- 채용 시장 동향: 경험이 풍부한 전문가보다는 신입사원에 대한 선호도가 낮아지지는 않았지만, 실제 역량과 경험을 중시합니다. 2025년까지 BIM 관련 인력 수요가 증가할 것으로 예상되며, 특히 고급기술, MEP 분야에서의 전문성 요구가 높습니다.
- 역량 개발 방향: 혁신적인 기술 도입과 융합 능력을 갖춘 리더십이 중요합니다. 문제 해결 및 시스템적 관점에서의 분석 능력 향상도 필요합니다.
- 관련: [[건축]] · [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]]


## BIM 인재 채용 및 역량 관리 업데이트 (2026-06-01)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-01
- Tags: hr,talent,BIM,update

- BIM 코디네이터와 매니저의 역량 기준: Revit, Navisworks, Solibri 등의 소프트웨어 사용 능력과 함께 자동화, R&D, 고급기술 분야에서의 전문 지식이 요구된다.
- 2025년 채용 시장 동향: BIM 관련 전문가와 모델러는 기술적 지식이 높은 인재를 선호한다. 우주개발, 디지털전환 등 신성장 산업 분야에서의 경험과 역량도 중요하게 고려된다.
- 역량 개발 방향: BIM 관련 기술을 넘어 시스템적 관점에서 문제 해결 능력과 창의융합 역량을 강화해야 한다. 이를 통해 종합적인 프로젝트 관리와 혁신적인 솔루션 제안 능력을 키울 수 있다.
- 관련: [[건축]] · [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]]


## BIM 인재 채용 및 역량 관리 업데이트 (2026-06-02)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-02
- Tags: hr,talent,BIM,update

- BIM 코디네이터와 매니저의 역량 기준: 3D 모델링, 프로젝트 관리, 4D 시뮬레이션 능력이 필수적입니다.
- 채용 시장 동향: 경험이 있는 전문가와 관련 자격증 소지자는 높은 수요를 보이고 있습니다. 특히 고급 기술, MEP 분야 및 자동화 R&D 분야에서의 역량을 갖춘 인재들이 중요합니다.
- 역량 개발 방향: 창의적 문제 해결 능력과 시스템적 관점으로 문제를 분석하는 능력을 강화해야 합니다. 또한 글로벌 핵심역량을 갖춘 전문 경영인력 양성에 중점을 둬야 합니다.
- 2025년까지 BIM 인재 수요는 지속적으로 증가할 것으로 예상되며, 이에 따라 관련 교육과 훈련이 필요합니다.
- 관련: [[건축]] · [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]]


## BIM 인재 채용 및 역량 관리 업데이트 (2026-06-03)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-03
- Tags: hr,talent,BIM,update

- BIM 코디네이터와 매니저의 역량 기준: Revit, Navisworks, Solibri 등의 소프트웨어 사용 능력은 필수이며, 자동화와 인공지능(AI) 분야에서도 전문적인 지식을 갖추어야 한다. 모델 통합과 고급 모델 검증 능력도 중요하다.
- 채용 시장 동향: 2025년까지 BIM 관련 직무는 계속 증가할 것으로 예상되며, 특히 신성장 산업과 R&D 분야에서의 기회가 많을 것이다. 우주개발 및 디지털 전환 전문가 등 새로운 역량이 요구되고 있다.
- 역량 개발 방향: 창의융합 역량을 강화하고, 시스템적 관점에서 문제를 분석하는 능력을 키워야 한다. 또한, 기업은 인력 수급 전망을 고려하여 적절한 채용 및 교육 계획을 세우는 것이 중요하다.
- 관련: [[건축]] · [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]]


## BIM 인재 채용 및 역량 관리 업데이트 (2026-06-03)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-03
- Tags: hr,talent,BIM,update

- BIM 코디네이터와 매니저는 Revit, Navisworks, Solibri 등의 소프트웨어 사용 능력이 필수이며, 자동화 및 인공지능(AI) 기술에 대한 이해도가 높아져야 합니다.
- 2025년까지 BIM 모델 통합과 고급 모델 검증 기술이 중요해질 것으로 예상되므로, 이러한 역량을 강화해야 합니다.
- 채용 시장에서 BIM 관련 직무는 지속적으로 증가할 것으로 보이며, 특히 높은 기술 및 R&D 분야에서의 기회가 많아질 것입니다.
- 새로운 직업 연구에 따르면, 인공지능 기술 전문가와 디지털 전환 전문가 등이 요구되므로, 이러한 역량 개발도 중요합니다.
- 중장기 인력 수급 전망에 따르면, 과학기술 분야의 일자리 변화 양상과 함께 BIM 관련 직무에서도 전문성과 현장 경험을 갖춘 인재가 더 이상한 경향이 있습니다.
- 관련: [[건축]] · [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]]


## BIM 인재 채용 및 역량 관리 업데이트 (2026-06-04)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-04
- Tags: hr,talent,BIM,update

- BIM 코디네이터와 매니저의 역량 기준: Revit, Navisworks, 그리고 자동화를 위한 고급 Python 등 주요 기술을 익혀야 합니다.
- 채용 시장 동향: 2025년까지는 협업과 통합 능력이 높은 역량이 중요해질 것으로 예상됩니다. 특히, IT, MEP, R&D 분야에서 이러한 요구가 증가할 것입니다.
- 역량 개발 방향: 창의융합 역량을 강화하고, 시스템적 관점에서 문제를 해결하는 능력을 키워야 합니다. 또한, 적절한 채용 및 인력 수급 전망을 고려하여 미래 기술 변화에 대비해야 합니다.
- 관련: [[건축]] · [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]]


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
- Source: `docs/training_curriculum/team_distribution/08_WEEKLY_ROLE_BASED_KNOWLEDGE_LEARNING_SPRINT_2026-06-04.md`
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


## BIM 인재 채용 및 역량 관리 업데이트 (2026-06-05)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-05
- Tags: hr,talent,BIM,update

- 2025년 BIM 코디네이터와 매니저의 역량 기준으로는 Revit, Navisworks, 그리고 프로젝트 관리 능력이 필수입니다.
- 반도체와 자동화 같은 하이테크 산업에서 BIM 관련 직무 수요가 증가할 것으로 예상됩니다.
- 4D 시뮬레이션과 프로젝트 관리 기술은 중요한 역량으로 자리잡을 것입니다.
- 채용 시장 동향에서는 리더십과 창의융합 능력이 중요하게 여겨질 것으로 보입니다.
- 역량 개발 방향으로는 K-ACE(Korea Art, Culture, and Entertainment) 분야와 같은 글로벌 핵심역량을 갖춘 전문 경영인력을 양성하는 것이 필요합니다.
- 관련: [[건축]] · [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]]


## BIM 인재 채용 및 역량 관리 업데이트 (2026-06-06)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-06
- Tags: hr,talent,BIM,update

- BIM 코디네이터와 매니저의 역량 기준으로는 Revit, Navisworks, Solibri 등의 소프트웨어 능력이 필수적입니다.
- 2025년까지는 협업과 통합 능력이 중요하게 평가될 것으로 예상됩니다. 이는 BIM 프로젝트의 성공을 위해 팀 간 효과적인 의사소통과 작업 조정이 필요하기 때문입니다.
- 채용 시장 동향에서는 리더십 역량을 갖춘 전문가를 찾는 경향이 강해질 것으로 보입니다. 이는 BIM 프로젝트의 복잡성 증가와 함께 팀 관리 및 프로젝트 관리를 책임지는 능력이 중요하기 때문입니다.
- 역량 개발 방향으로는 지속적인 교육과 학습을 통해 최신 BIM 기술 트렌드를 파악하고, 협업 도구와 소프트웨어의 사용 능력을 향상시키는 것이 필요합니다.
- 관련: [[건축]] · [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]]


## BIM 인재 채용 및 역량 관리 업데이트 (2026-06-07)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-07
- Tags: hr,talent,BIM,update

- BIM 코디네이터와 매니저의 역량 기준: Revit 프로페셔널리즘, 충돌 검출 능력, 협업 능력이 필수적이다. IT 계획과 자동화 관련 지식도 중요하다.
- 채용 시장 동향: 2025년까지 BIM 분야에서 높은 수요가 예상되며, 구조물 인프라, 자동화, R&D 능력이 요구된다. 디지털 전환 전문가와 같은 신직업도 주목해야 한다.
- 역량 개발 방향: 혁신적인 문제 해결 능력을 강화하고, 시스템적 관점에서의 분석 기술을 향상시켜야 한다. 또한, K-ACE(Korea Art, Culture, and Entertainment)와 같은 글로벌 역량을 갖춘 전문 경영인력 양성에도 관심을 가져야 한다.
- 관련: [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]] · [[BIM_시방서]]


## BIM 인재 채용 및 역량 관리 업데이트 (2026-06-09)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-09
- Tags: hr,talent,BIM,update

- BIM 코디네이터와 매니저의 역량 기준: Revit, Dynamo, Python 등의 소프트웨어 사용 능력이 필수입니다.
- 2025년까지 BIM 관련 직무에서 요구되는 주요 기술로 MEP( Mechanical, Electrical, Plumbing) 설계 및 자동화, AI와의 통합 모델링 등이 포함됩니다.
- 채용 시장 동향: 인공지능 기술과 디지털 전환 전문가 등의 신직업 요구 역량이 변화하고 있으며, 이러한 추세를 반영한 BIM 관련 직무에서도 혁신적인 접근 방식이 필요합니다.
- 역량 개발 방향: 시스템적 관점에서 문제 해결 능력과 창의융합 역량을 강화해야 합니다. 이를 통해 복잡한 프로젝트를 효과적으로 관리하고 협업할 수 있는 능력을 키워야 합니다.
- 인력수급 전망: 과학기술 분야에서 일자리 변화가 예상되므로, BIM 관련 직무에서도 이러한 트렌드에 맞춰 역량을 개발해야 합니다.
- 관련: [[설계_지침서]] · [[시공_지침서]] · [[BIM_지침서]] · [[BIM_시방서]]

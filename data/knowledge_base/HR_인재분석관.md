# HR_인재분석관 지식 베이스

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

# LUA BIM LAB
# 외장하드 개인/업무 자료 지식 인테이크 기준

━━━━━━━━━━━━━━━━━━━━

문서번호: LBL-ORG-022  
문서상태: 내부 기준 초안  
작성일: 2026-05-21  
배포등급: Confidential  
적용범위: 외장하드, 개인 백업, 업무용 백업, BIM 자료, Add-in 자료, 프로젝트 기록

## 1. 목적

본 문서는 외장하드에 보관된 개인/업무 자료 중 LUA BIM LAB의 지식 자산으로 흡수 가능한 자료를 선별하기 위한 기준이다.

## 2. 기본 원칙

- 원본 자료는 이동하거나 삭제하지 않는다.
- 최초 스캔은 파일 내용이 아니라 경로, 파일명, 확장자, 크기, 수정일만 사용한다.
- 고객명, 연락처, 계약, 비용, 개인정보, 인증서, 토큰, 설치파일은 자동 흡수하지 않는다.
- 지식화 대상은 원문 복사가 아니라 요약, 익명화, 기준화, 체크리스트화한다.
- 외부 공개 가능 자료로 전환하기 전에는 공개 등급과 보안 검토를 반드시 수행한다.

## 3. 흡수 우선순위

| 우선순위 | 자료 유형 | 승격 대상 |
|---:|---|---|
| 1 | BIM 표준, MEP 매뉴얼, 품질 체크리스트 | 표준문서, 교육자료 |
| 2 | Dynamo, Revit/Navisworks Add-in, 자동화 노드 | 개발 지식, 기능 후보, 오류 오답노트 |
| 3 | 프로젝트 종료 프로세스, 인수인계, 보고서 양식 | 내부 운영 문서, 납품 체크리스트 |
| 4 | 물량 산식, 산출 기준, 템플릿 | Quantity/ROI 기준, 교육 실습 |
| 5 | 제안서, 수행사례, 비교분석 | 상품 패키지, 제안 문구 |

## 4. 자동 차단 대상

| 대상 | 사유 |
|---|---|
| NPKI, 인증서, yessign | 인증/보안 민감정보 |
| 연락처, 담당자, 고객명 원문 | 개인정보 및 고객 기밀 가능성 |
| 계약, 비용, 견적 상세 | 상업/법무 민감정보 |
| 설치파일, 크랙, 패치 파일 | 라이선스 및 보안 리스크 |
| 원본 프로젝트 모델/도면 | 고객 보안 및 용량 관리 리스크 |
| 사진 원본 대량 파일 | 지식 DB보다 자산 저장소 대상 |

## 5. 실행 도구

메타데이터 기반 후보 리포트 생성:

```bash
source .dev-venv/bin/activate && python scripts/external_knowledge_intake.py "/Volumes/One Touch/개인자료" "/Volumes/One Touch/업무용 자료"
```

생성 위치:

`knowledge/30_intake/external_sources/`

## 6. 큐레이션 절차

1. 인테이크 리포트에서 `high_value_review` 후보를 확인한다.
2. 민감정보 가능성이 있는 자료를 제외한다.
3. 자료를 직접 열람해도 되는지 사용자가 승인한다.
4. 승인된 자료만 요약/익명화하여 지식 노트로 만든다.
5. 관련 표준문서, 교육자료, Model Quality Auditor, Add-in 로드맵에 연결한다.
6. 전역 Obsidian 지식맵을 재생성한다.

## 7. 템플릿 내재화 기준

외부 자료에서 유용한 보고서, 등록부, 체크리스트, 카탈로그 형식이 발견되면 원본을 복사하지 않고 다음 방식으로 LUA BIM LAB 공식 템플릿으로 전환한다.

| 전환 대상 | 내재화 방식 | 연결 문서 |
|---|---|---|
| 오류검토/RFI 보고서 | 프로젝트명, 공종, 위치, 심각도, 조치, 근거 중심의 공식 보고 양식으로 재작성 | `24_BIM_ISSUE_REVIEW_REPORT_TEMPLATE.md` |
| 품질 이슈 대장 | 담당, 상태, 기한, 종결 근거, 지식화 여부를 추적하는 운영 등록부로 전환 | `25_PROJECT_QUALITY_ISSUE_REGISTER_TEMPLATE.md` |
| BIM 라이브러리 목록 | Family, Type, LOD, 파라미터, 검수상태, 공개등급을 관리하는 자산 등록부로 전환 | `26_BIM_LIBRARY_FAMILY_REGISTER_TEMPLATE.md` |
| Dynamo/자동화 목록 | 입력, 출력, 위험도, 재사용성, Add-in 전환성을 평가하는 노드 카탈로그로 전환 | `27_DYNAMO_AUTOMATION_NODE_CATALOG_TEMPLATE.md` |
| 인수인계/종료 보고 | 산출물, 미결 이슈, 운영 주의사항, 레슨런을 다음 프로젝트 지식으로 전환 | `28_PROJECT_HANDOVER_KNOWLEDGE_TRANSFER_TEMPLATE.md` |

내재화된 템플릿은 `Client-Shareable`, `Internal`, `Confidential` 등 공개 등급을 부여하고, Obsidian 지식맵에서 원천 후보, 표준문서, 교육자료, 제품문서가 연결되도록 관리한다.

## 8. 관련 문서

- `15_KNOWLEDGE_DOCUMENT_REPOSITORY_POLICY.md`
- `20_PUBLIC_DISCLOSURE_DB_READINESS_CHECKLIST.md`
- `21_KNOWLEDGE_CURATION_INTELLIGENCE_CELL.md`
- `docs/standard_documents/00_DOCUMENT_STANDARD_INDEX.md`
- `knowledge/10_agents/09_지식팀/지식업데이트.md`

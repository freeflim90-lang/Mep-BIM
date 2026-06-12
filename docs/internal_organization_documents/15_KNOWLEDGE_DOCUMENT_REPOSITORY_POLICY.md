# LUA BIM LAB
# 지식관리 및 문서 저장 기준

━━━━━━━━━━━━━━━━━━━━

문서번호: LBL-ORG-015  
문서상태: 내부 기준 초안  
작성일: 2026-05-20

## 1. 목적

본 문서는 프로젝트 경험, 표준문서, 교육자료, 고객 제출 문서, 내부 의사결정을 재사용 가능한 지식으로 관리하기 위한 기준이다.

## 2. 문서 분류

| 분류 | 예시 | 접근 |
|---|---|---|
| 공식 외부 문서 | 제안서, 공문, 납품자료 | PM 승인 |
| 내부 운영 문서 | 본 패키지 문서 | 내부 |
| 교육자료 | 커리큘럼, 실습, 평가 | 내부 |
| 프로젝트 자료 | 모델, 도면, 보고서 | 프로젝트 권한 |
| 민감 자료 | 계약, 비용, 개인정보 | 제한 |

## 3. 저장 원칙

- 문서명에는 날짜, Revision, 문서번호를 포함한다.
- 최종본과 작업본을 구분한다.
- 프로젝트 종료 후 레슨런과 표준 개정 후보를 남긴다.
- 고객 자료는 고객 보안 기준을 우선한다.

## 4. 지식 업데이트 기준

| 출처 | 반영 대상 |
|---|---|
| 반복 오류 | 교육자료, 체크리스트 |
| 고객 반려 | 품질 기준, 납품 기준 |
| 성공 사례 | 제안 문구, 실적 템플릿 |
| 사고/장애 | 보안/권한/복구 절차 |

## 5. Obsidian 지식 시각화 기준

LUA BIM LAB의 `.md` 문서는 원본 폴더 구조를 유지하되, 검색성과 지식 간 연결성을 높이기 위해 전역 Obsidian 인덱스 vault를 별도로 운영한다.

| 항목 | 기준 |
|---|---|
| 전역 vault | `obsidian_vaults/lua_bim_lab_global_map` |
| 시작 문서 | `00_Home/Global Knowledge Map.md` |
| 분류 지도 | `01_MOC/` |
| 문서 색인 | `10_Document_Index/` |
| 시각 자료 | `09_Canvas/Global Knowledge Canvas.canvas`, `Assets/global_knowledge_graph.html` |
| 재생성 스크립트 | `scripts/build_global_obsidian_map.py` |

운영 원칙:

- 원본 문서는 이동하거나 복제하지 않고, Obsidian용 색인 노트를 생성한다.
- 문서 간 연결은 폴더 분류, 제목 키워드, 문서 본문 주요 용어, 명시적 링크를 함께 기준으로 한다.
- 사용자는 Obsidian에서 전역 vault를 열고 Graph View, Canvas, MOC를 통해 필요한 문서를 탐색한다.
- 문서가 대량 추가되거나 분류 체계가 바뀌면 전역 맵을 재생성한다.
- 외부 제출 문서와 내부 운영 문서는 연결되더라도 접근 권한과 배포 범위를 별도로 관리한다.

재생성 명령:

```bash
source .dev-venv/bin/activate && python scripts/build_global_obsidian_map.py
```

## 6. 지식 탐색 흐름

자료를 찾을 때는 다음 순서로 탐색한다.

1. `Global Knowledge Map`에서 전체 카테고리와 핵심 허브를 확인한다.
2. 관련 `MOC`에서 업무 영역별 문서를 좁힌다.
3. 개별 `Document_Index` 노트에서 원본 경로, 요약, 키워드, 관련 문서를 확인한다.
4. Obsidian Graph View 또는 HTML 그래프에서 연결 문서를 추가로 탐색한다.
5. 실제 편집은 원본 `.md` 파일에서 수행하고, 필요 시 전역 맵을 재생성한다.

## 7. 매일 오전 7시 지식 업데이트

조직 공개 전까지 지식 DB를 누적 검증하기 위해 매일 오전 7시에 자동 업데이트를 실행한다.

| 항목 | 기준 |
|---|---|
| 실행 스크립트 | `scripts/daily_knowledge_update.sh` |
| macOS LaunchAgent | `config/launch_agents/com.luabimlab.daily-knowledge-update.plist` |
| 실행 시간 | 매일 07:00 |
| 실행 로그 | `logs/daily_knowledge_update.log` |
| launchd 로그 | `logs/daily_knowledge_update.launchd.out.log`, `logs/daily_knowledge_update.launchd.err.log` |
| 일일 리포트 | `knowledge/40_curation/updates/daily/` |
| 산업 브리핑 | `docs/industry_intelligence/daily/` |

자동 실행 작업:

- 일일 지식 업데이트 리포트를 생성한다.
- 건설, 설계, 시공, BIM 주요 동향을 수집해 Telegram 요약을 전송하고 지식베이스에 누적한다.
- `Model Quality Auditor` Obsidian 그래프를 갱신한다.
- LUA BIM LAB 전역 Obsidian 지식맵을 재생성한다.
- 신규 문서, 오류 오답노트, 의사결정, Revit API 게이트 수량을 기록한다.

수동 실행 명령:

```bash
scripts/daily_knowledge_update.sh
```

운영 변경 기준:

- 기존 월간 지식 업데이트는 일일 업데이트 체계로 전환한다.
- `scripts/monthly_knowledge_update.sh`는 과거 호출 호환용으로만 유지하며, 내부적으로 일일 업데이트를 실행한다.
- 월간 LaunchAgent는 사용하지 않는다.
- 월간 검토가 필요한 KPI, 품질, 교육 항목은 별도 회의체에서 다루되, 지식 수집과 Obsidian 갱신은 매일 수행한다.

## 7.1 건설·설계·시공·BIM 데일리 브리핑

매일 오전 7시 지식 업데이트 안에서 `scripts/daily_industry_briefing.py`를 실행한다. 이 모듈은 RSS/Atom 기반으로 건설, 설계, 시공, BIM 관련 신호를 수집하고 LUA BIM LAB 목적성에 맞게 분류한다.

| 항목 | 기준 |
|---|---|
| 실행 스크립트 | `scripts/daily_industry_briefing.py` |
| 소스 설정 | `config/daily_industry_briefing_sources.json` |
| 일일 보고서 | `docs/industry_intelligence/daily/YYYY-MM-DD_CONSTRUCTION_DESIGN_BIM_DAILY_BRIEFING.md` |
| 누적 지식베이스 | `knowledge/10_agents/90_확장에이전트/산업동향_데일리브리핑.md` |
| Telegram 전송 | `.env` 또는 환경변수의 `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` 사용 |

브리핑은 단순 뉴스 모음이 아니라 다음 항목으로 승격 가능성을 판단한다.

- Model Quality Auditor 진단 룰 후보
- MEP BIM 연차별 교육 사례
- Autodesk Store/Add-in 기능 로드맵 영향
- openBIM, IFC, IDS 기반 납품/품질 기준
- AI/자동화 기반 생산성 개선 아이템

## 8. 외부 공개 전 DB 구축 필수 조건

외부 공개 전에는 문서량보다 신뢰성과 분류 품질을 우선한다.

| 영역 | 필수 조건 |
|---|---|
| 공개 등급 | Public, Client-Shareable, Internal, Confidential로 분류 |
| 원본 경로 | 모든 색인 노트가 원본 문서 경로를 가져야 함 |
| 문서 상태 | draft, review, approved, archived 상태 표시 |
| 검증 상태 | 미검증 기능, Revit API 대기 항목, Qwen 초안 구분 |
| 오류 지식 | 오류는 오답노트 형식으로 원인, 수정, 재발 방지 포함 |
| 보안 | 토큰, 계정, 고객명, 내부 경로, 개인정보 노출 점검 |
| 중복 | 동일 목적 문서의 중복 여부 점검 |
| 연결성 | 고립 문서가 있으면 관련 MOC 또는 허브 문서에 연결 |
| 공개 자료 | 외부 공개 문서는 내부 운영 문서와 분리된 패키지로 관리 |

공개 전 차단 조건:

- 민감 정보가 포함된 문서가 Public 또는 Client-Shareable로 분류된 경우
- 기능 검증 전인데 확정 표현으로 Store, 제안서, 교육자료에 반영된 경우
- 고객 제출 문서에 내부 의사결정, 개발 오류, 비용 구조가 포함된 경우
- 오류 오답노트가 원인/재발 방지 없이 해결 완료로 표시된 경우
- 주요 상품 문서가 전역 Obsidian 맵에서 검색되지 않는 경우

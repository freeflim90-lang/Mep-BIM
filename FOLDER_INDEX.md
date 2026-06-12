# LUA BIM LABS 폴더 인덱스

최종 재구성: 2026-06-13 (파일 체계 전면 재구성)

경로의 단일 출처(SSOT)는 [backend/core/paths.py](backend/core/paths.py)이다.
셸 스크립트는 `source scripts/lib/paths.sh` 로 같은 값을 사용한다.
코드에서 경로를 직접 조립하지 말 것.

## 지식 트리 — knowledge/

AI 조직원(51개 에이전트)이 사용하는 지식의 단일 트리.
`config/product_knowledge_layers.json` 의 4층 승격 모델을 따른다.

| 폴더 | 내용 |
|---|---|
| `knowledge/00_catalog/` | 자동 생성 인덱스 — FILE_MAP.json(검색엔진용), KNOWLEDGE_CATALOG.md(사람용). 매일 07:00 daily-knowledge-update 가 재생성. 수동 편집 금지 |
| `knowledge/10_agents/` | 에이전트별 지식베이스. 팀 폴더: 01_경영진 ~ 09_지식팀, 90_확장에이전트 |
| `knowledge/20_qa/` | 에이전트별 Q&A 누적 지식 (`*_QA.md`) |
| `knowledge/30_intake/` | 미검수 수집물(raw intake) + `team_requests/` 팀 요청 로그 |
| `knowledge/40_curation/` | `quality/` 품질·승인 로그, `updates/` 일일·주간 지식 업데이트 리포트 |
| `knowledge/50_domain/` | 도메인 원천자료 — technical_pdfs, bim_scripts, bimobject, qa_dataset, bim_education |
| `knowledge/60_public/` | 공개·재사용 콘텐츠 — blogger_queue, training_curriculum |

검색 경로: `backend/knowledge_engine.py` 가 10_agents·20_qa·docs·MQA 볼트를 검색하며,
FILE_MAP.json 키워드 역색인으로 후보를 좁힌다 (카탈로그 없으면 풀스캔 폴백).

## 제품 트리 — products/

| 폴더 | 내용 |
|---|---|
| `products/starter_plan/` | Starter Plan 교육 상품 (고객, 커리큘럼, 메시지, 퀴즈) |
| `products/bim_land/` | BIM Land 마켓플레이스 상태 |
| `products/bim_command_center/` | BIM Command Center 운영 데이터 |
| `products/autodesk_market/` | Autodesk 스토어 크롤링 스냅샷 |

## 코드·운영 (위치 고정 — LaunchAgent·import 의존)

| 폴더 | 내용 |
|---|---|
| `backend/` | FastAPI 백엔드 (진입점 server_total.py) |
| `scripts/` | 자동화 스크립트 94+ (LaunchAgent 가 호출) |
| `frontend/`, `website/` | UI·웹사이트 |
| `tests/` | pytest 스위트 (`make verify`) |
| `config/` | 설정 + `launch_agents/` plist 24개 (설치: `scripts/install_launch_agents.sh`) |
| `logs/`, `runtime/` | 로그·런타임 상태 |
| `data/` | 잔여 런타임 상태만 (ai_usage, visitor_count 등). `data/knowledge_base` 는 호환 심링크(제거 예정) |
| `docs/` | 회사 공식 문서 — 계약, 표준문서, 조직운영, 산업동향 |
| `obsidian_vaults/` | Obsidian 볼트 (이동 금지 — 앱이 경로 저장) |

## 레거시·격리

| 폴더 | 내용 |
|---|---|
| `commercial_addins/` | Revit 애드인 상용화 산출물 (00_product ~ 08_feature_backlog) |
| `Mep-BIM/`, `legacy/`, `260519*/` | 과거 소스 스냅샷 — 참조용 |

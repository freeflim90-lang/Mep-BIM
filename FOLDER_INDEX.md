# LUA BIM LABS 폴더 인덱스

최종 재구성: 2026-06-13 (파일 체계 전면 재구성)

경로의 단일 출처(SSOT)는 [backend/core/paths.py](backend/core/paths.py)이다.
셸 스크립트는 `source scripts/lib/paths.sh` 로 같은 값을 사용한다.
코드에서 경로를 직접 조립하지 말 것.

## 루트 운영 원칙

루트에는 저장소 진입점과 실행·검증에 필요한 파일만 둔다.

| 유형 | 위치 |
|---|---|
| 저장소 안내 | `README.md`, `FOLDER_INDEX.md` |
| 실행·검증 설정 | `Makefile`, `Dockerfile`, `docker-compose.yml`, `pytest.ini`, `requirements*.txt` |
| 코드·제품·지식·문서 | 아래 표의 최상위 폴더 |
| 과거 기획서·핸드오프 | `docs/` 또는 `legacy/` 하위 |
| 자동 생성 로그·상태 | `logs/`, `runtime/`, `data/`, `dist/` |

명령어 오타로 생긴 빈 파일, 임시 점검 파일, 분류되지 않은 기획서는 루트에 두지 않는다.
`runtime/`, `dist/`, 제출용 ZIP·업로드 패키지는 원본 지식이 아니라 재생성 가능한 산출물로 취급한다.

## 지식 트리 — knowledge/

AI 조직원(51개 에이전트)이 사용하는 지식의 단일 트리.
`config/product_knowledge_layers.json` 의 4층 승격 모델을 따른다.

| 폴더 | 내용 |
|---|---|
| `knowledge/00_catalog/` | 자동 생성 인덱스 — FILE_MAP.json(검색엔진용), KNOWLEDGE_CATALOG.md(사람용). 매일 07:00 daily-knowledge-update 가 재생성. 수동 편집 금지 |
| `knowledge/10_agents/` | 에이전트별 지식베이스. 팀 폴더: 01_경영진 ~ 09_지식팀, 90_확장에이전트. 공용 도메인 자료는 원칙적으로 `50_domain/`에 둔다 |
| `knowledge/20_qa/` | 에이전트별 Q&A 누적 지식 (`*_QA.md`) |
| `knowledge/30_intake/` | 미검수 수집물(raw intake) + `team_requests/` 팀 요청 로그 |
| `knowledge/40_curation/` | `quality/` 품질·승인 로그, `updates/` 일일·주간 지식 업데이트 리포트 |
| `knowledge/50_domain/` | 도메인 원천자료 — technical_pdfs, bim_scripts, bimobject, qa_dataset, bim_education |
| `knowledge/60_public/` | 공개·재사용 콘텐츠 — blogger_queue, training_curriculum |

검색 경로: `backend/knowledge_engine.py` 가 10_agents·20_qa·docs·MQA 볼트를 검색하며,
FILE_MAP.json 키워드 역색인으로 후보를 좁힌다 (카탈로그 없으면 풀스캔 폴백).

현재 `knowledge/10_agents/conflict_resolution/`, `knowledge/10_agents/시설유형/`은 기존 지식 호환을 위한 예외 폴더이다.
신규 자료는 팀 책임자가 명확하면 해당 팀 폴더로, 도메인 원천자료이면 `knowledge/50_domain/`으로 배치한다.

## 제품 트리 — products/

수익 제품 단일 인덱스(SSOT)는 [config/products.json](config/products.json) 이다.
교육 플랜·서비스·애드인을 한 곳에서 참조로 통합한다(과거 products/·docs/·product_knowledge_layers.json 3곳 파편화 해소).

| 폴더 | 내용 |
|---|---|
| `products/starter_plan/` | Starter Plan 교육 상품 (고객, 커리큘럼, 메시지, 퀴즈) |
| `products/model_quality_audit/` | 모델 품질 감리(B2B 서비스) 운영 상태. 문서 원본은 `docs/revenue_products/model_quality_audit/` |
| `products/bim_command_center/` | BIM Command Center 운영 데이터 (빌드 완료·발송 대기) |
| `products/bim_land/` | BIM Land 마켓플레이스 상태 |
| `products/autodesk_market/` | Autodesk 스토어 크롤링 스냅샷 |

## 코드·운영 (위치 고정 — LaunchAgent·import 의존)

| 폴더 | 내용 |
|---|---|
| `backend/` | FastAPI 백엔드 (진입점 server_total.py) |
| `scripts/` | 자동화 스크립트 94+ (LaunchAgent 가 호출) |
| `frontend/`, `website/` | UI·웹사이트 |
| `tests/` | pytest 스위트 (`make verify`) |
| `config/` | 설정 + `launch_agents/` plist 24개 (설치: `scripts/install_launch_agents.sh`) |
| `logs/`, `runtime/` | 로그·런타임 상태. `runtime/README.md` 외의 상태 파일은 Git에 보관하지 않음 |
| `data/` | 잔여 런타임 상태만 (ai_usage, visitor_count 등). `data/knowledge_base` 는 호환 심링크(제거 예정) |
| `docs/` | 회사 문서 (아래 두 폴더는 중복이 아니라 역할이 다름) |
| `obsidian_vaults/` | Obsidian 볼트 (이동 금지 — 앱이 경로 저장) |

`docs/` 의 두 핵심 문서 세트는 명확히 구분된다(병합 금지):
- `docs/internal_organization_documents/` — **내부 거버넌스**: 운영헌장·RACI·결재권한·인사/온보딩·KPI·리스크·AI협업 SOP. 조직이 내부적으로 돌아가는 방식.
- `docs/lua_bim_lab_official_documents/` — **외부/고객용 공식 문서**: 회사소개·서비스 카탈로그·제안·계약·RFI·딜리버리·인보이스·CS 스크립트. 고객·대외 발행용.

## 레거시·격리

| 폴더 | 내용 |
|---|---|
| `commercial_addins/` | Revit 애드인 상용화 산출물 (00_product ~ 08_feature_backlog) |
| `legacy/`, `260519*/` | 과거 소스 스냅샷 — 참조용 |

Store 제출 문서의 원본은 `docs/autodesk_store/`이다.
`commercial_addins/**/03_store_submission/autodesk_store_upload*`와 `dist/`의 패키지는 스크립트가 만드는 복사본이므로 Git에 보관하지 않는다.

# 인프라_DevOps (Obsidian) 지식 베이스


## 로컬 인프라/DevOps 기준 (2026-05-19 09:16:50)
- Source: LUA BIM LABS curated baseline, Autodesk official docs checked 2026-05-19
- Tags: devops,obsidian,local

인프라 DevOps는 지식 베이스, 로그, 빌드 산출물, 릴리스 노트, Obsidian 문서 동기화를 관리한다. 민감 토큰은 .env에 두고 저장소 커밋 대상에서 제외한다.


## 로컬 인프라 운영 기준 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: devops,local,obsidian

환경 변수 관리: .env 파일에 저장, .gitignore에 반드시 포함. 절대 저장소 커밋 금지.
지식 베이스 백업: data/knowledge_base/ 폴더를 주 1회 외부 저장소(Git 또는 클라우드) 백업.
로그 관리: logs/ 폴더 90일 이상 로그 자동 삭제 (launchd 또는 cron 설정).
서버 모니터링: uvicorn 프로세스 죽으면 자동 재시작 (launchd plist 설정).
Obsidian Vault 동기화: iCloud 또는 Obsidian Sync로 Mac 간 동기화.

## Model Quality Auditor Obsidian Vault 기준 (2026-05-20)
- Source: `obsidian_vaults/model_quality_auditor`, `docs/revenue_products/model_quality_audit/14_OBSIDIAN_KNOWLEDGE_SYSTEM.md`
- Tags: obsidian,mqa,knowledge-graph,devlog,error-fix

`Model Quality Auditor`는 별도 프로젝트로 개발하고 실제 Revit API 사용 가능 환경에서 빌드/테스트 후 Addin Dashboard에 합친다. 개발 중 발생하는 오류, 수정, 의사결정, Revit API 테스트 게이트는 `obsidian_vaults/model_quality_auditor` vault에 기록한다.

운영 기준:
1. 오류/수정은 `03_Errors_Fixes`에 남기고 증상, 원인, 수정, 검증, 재발 방지를 포함한다.
2. 기술/제품 결정은 `04_Decisions`에 남기고 Addin Dashboard 병합 영향 여부를 기록한다.
3. Revit API가 필요한 항목은 `05_Revit_API_Gates`에 대기시키고 실제 Revit 환경 테스트 후 확정한다.
4. Qwen이 작성한 초안은 `06_Qwen_Drafts`에 보관하고 검증 상태를 표시한다.
5. Obsidian Graph View, Canvas, `Assets/mqa_knowledge_graph.html`로 지식 연결을 시각적으로 확인한다.


## GitHub API 연동 운영 기준 (2026-05-20)
- Source: LUA BIM LABS local integration policy
- Tags: github,devops,security,token

GitHub PAT는 코드와 지식 베이스에 저장하지 않고 `GITHUB_TOKEN` 또는 `GITHUB_PAT` 환경변수에서만 읽는다. 상태 확인과 저장소 조회는 읽기 전용으로 먼저 운영하며, issue 생성, push, release 생성처럼 저장소를 변경하는 작업은 최고지배자 또는 DevOps의 명시 지시가 있을 때 별도 승인 흐름으로 추가한다.

권장 토큰 권한은 Fine-grained token 기준 `Metadata: Read-only`, `Contents: Read-only`이며 private repo 조회가 필요할 때만 대상 저장소를 제한해 부여한다. 토큰이 화면, 대화, 로그에 노출되면 즉시 revoke 후 새 토큰으로 교체한다.

## LUA BIM LAB 전역 Obsidian 지식 맵 기준 (2026-05-20)
- Source: `obsidian_vaults/lua_bim_lab_global_map`, `scripts/build_global_obsidian_map.py`
- Tags: obsidian,knowledge-graph,document-index,moc,canvas

LUA BIM LAB의 모든 주요 `.md` 문서는 원본 위치를 유지하고, 별도 전역 vault에서 검색/그래프/카테고리 탐색용 색인으로 시각화한다. 이 구조는 표준문서, 내부조직문서, 교육 커리큘럼, 수익형 상품 문서, AI 직원 지식 베이스, 개발 프로젝트 기록을 하나의 지식망으로 연결하기 위한 운영 기준이다.

운영 경로:
- 전역 vault: `obsidian_vaults/lua_bim_lab_global_map`
- 시작 문서: `00_Home/Global Knowledge Map.md`
- 카테고리 MOC: `01_MOC/`
- 문서 색인: `10_Document_Index/`
- Canvas: `09_Canvas/Global Knowledge Canvas.canvas`
- HTML 그래프: `Assets/global_knowledge_graph.html`

운영 원칙:
1. 원본 `.md` 문서는 이동하지 않는다.
2. 색인 노트는 원본 경로, 요약, 키워드, 관련 문서를 포함한다.
3. 문서 검색은 `Global Knowledge Map -> MOC -> Document Index -> 원본 문서` 순서로 수행한다.
4. 개발 오류, 수정 기록, 의사결정은 프로젝트별 vault에 남기고, 전역 vault는 이를 다시 찾아갈 수 있는 허브 역할을 한다.
5. 신규 문서가 추가되거나 폴더 구조가 바뀌면 아래 명령으로 전역 맵을 재생성한다.

```bash
source .dev-venv/bin/activate && python scripts/build_global_obsidian_map.py
```

## 매일 07:00 지식 업데이트 자동화 기준 (2026-05-21)
- Source: `scripts/daily_knowledge_update.sh`, `config/launch_agents/com.luabimlab.daily-knowledge-update.plist`
- Tags: launchd,daily-update,obsidian,knowledge-db,public-readiness

지식 수집 및 Obsidian 업데이트는 매일 오전 7시에 macOS LaunchAgent로 실행한다. 실행 목적은 신규 문서, 오류 오답노트, 의사결정, Revit API 검증 게이트를 누락 없이 전역 지식 DB에 반영하는 것이다.

실행 항목:
1. `docs/knowledge_updates/daily`에 일일 지식 업데이트 리포트를 생성한다.
2. 건설, 설계, 시공, BIM 데일리 브리핑을 생성하고 Telegram 요약을 전송한다.
3. 브리핑 결과를 `data/knowledge_base/산업동향_데일리브리핑.md`에 누적한다.
4. `Model Quality Auditor` 프로젝트 vault의 HTML 그래프를 재생성한다.
5. LUA BIM LAB 전역 Obsidian vault를 재생성한다.
6. 실행 로그를 `logs/daily_knowledge_update.log`에 남긴다.

등록된 LaunchAgent:
- Label: `com.luabimlab.daily-knowledge-update`
- 등록 위치: `~/Library/LaunchAgents/com.luabimlab.daily-knowledge-update.plist`
- 기준 파일: `config/launch_agents/com.luabimlab.daily-knowledge-update.plist`
- 실행 시간: 매일 07:00

운영 변경:
- 기존 `com.luabimlabs.monthly-knowledge-update` LaunchAgent는 사용하지 않는다.
- 기존 `scripts/monthly_knowledge_update.sh`는 과거 호출 호환용으로만 유지하고, 내부적으로 `scripts/daily_knowledge_update.sh`를 실행한다.
- 지식 수집, Obsidian 갱신, 일일 리포트 생성은 모두 일일 업데이트를 기준으로 한다.

수동 실행:

```bash
scripts/daily_knowledge_update.sh
```

건설·설계·시공·BIM 브리핑만 수동 실행:

```bash
source .dev-venv/bin/activate && python scripts/daily_industry_briefing.py
```

Telegram 없이 보고서와 지식베이스만 생성:

```bash
source .dev-venv/bin/activate && python scripts/daily_industry_briefing.py --no-telegram
```

상태 확인:

```bash
launchctl print gui/$(id -u)/com.luabimlab.daily-knowledge-update
```

외부 공개 전 추가로 필요한 DB 품질 조건:
- 문서별 공개 등급 분리: Public, Client-Shareable, Internal, Confidential
- 문서별 상태 관리: draft, review, approved, archived
- Qwen 초안과 검증 완료 문서 분리
- Revit API 가능 환경에서만 확정할 항목 별도 게이트 관리
- 토큰, 계정, 고객명, 내부 경로, 개인정보 자동/수동 점검
- 오류 오답노트의 원인, 수정, 검증, 재발 방지 필수화
- 고립 문서 탐지 및 MOC 연결
- 외부 공개용 vault 또는 패키지 별도 분리

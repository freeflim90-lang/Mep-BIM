# 인프라_DevOps (Obsidian) 지식 베이스

## 2026-06-05 LUA BIM LABS 인프라·DevOps 현황 업데이트
- Source: LUA BIM LABS 서버 운영 로그, LaunchAgent 설정, GitHub 동기화 현황
- Tags: devops,obsidian,local,server,launchagent,cloudflare,2026

**LUA BIM LABS 인프라 구성 (2026-06-05 기준):**
| 컴포넌트 | 기술 | 역할 |
|---------|------|------|
| 백엔드 서버 | FastAPI + Uvicorn (port 8000) | API·텔레그램 봇 |
| 원격 접속 | Cloudflare Tunnel + Tailscale | 외부 접근 |
| 지식베이스 | knowledge/10_agents/ (140개 파일) | AI 답변 소스 |
| Obsidian | lua_bim_lab_global_map 볼트 | 지식 시각화 |
| 자동화 | LaunchAgent (15개 에이전트) | 스케줄 실행 |
| 동기화 | sync_knowledge.sh → GitHub | 코드 백업 |
| 모니터링 | logs/ 디렉토리 | 실행 이력 |

**2026년 인프라 개선 완료 사항:**
- 텔레그램 봇 Conflict 해결: `delete_webhook()` 선행 호출 추가
- 좀비 마커 파일 자동 감지: `.daily_knowledge_update_running` 정리
- MQA·Knowledge 정적 파일 서빙: `/mqa`, `/knowledge` 경로 추가
- 모델 라우팅 상태 모니터링: `/api/model-routing-status` 엔드포인트

**Obsidian 볼트 구조 (2026-06-05):**
- `NAS_Knowledge/`: 800+ 지식 노트 (일간 뉴스 자동 추가)
- `01_MOC/`: MOC 인덱스 파일 (AI Knowledge Base 134+ 파일)
- `Assets/`: global_knowledge_graph.html (웹 임베드)
- 총 source_count: 1,925개

## 로컬 인프라/DevOps 기준 (2026-05-19 09:16:50)
- Source: LUA BIM LABS curated baseline, Autodesk official docs checked 2026-05-19
- Tags: devops,obsidian,local

인프라 DevOps는 지식 베이스, 로그, 빌드 산출물, 릴리스 노트, Obsidian 문서 동기화를 관리한다. 민감 토큰은 .env에 두고 저장소 커밋 대상에서 제외한다.


## 로컬 인프라 운영 기준 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: devops,local,obsidian

환경 변수 관리: .env 파일에 저장, .gitignore에 반드시 포함. 절대 저장소 커밋 금지.
지식 베이스 백업: knowledge/10_agents/ 폴더를 주 1회 외부 저장소(Git 또는 클라우드) 백업.
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
1. `knowledge/40_curation/updates/daily`에 일일 지식 업데이트 리포트를 생성한다.
2. 건설, 설계, 시공, BIM 데일리 브리핑을 생성하고 Telegram 요약을 전송한다.
3. 브리핑 결과를 `knowledge/10_agents/90_확장에이전트/산업동향_데일리브리핑.md`에 누적한다.
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


## 인프라 DevOps Obsidian Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: DevOps,Obsidian,CI-CD,automation,knowledge-management,2025

- Obsidian + Git 동기화 자동화(2025): Obsidian Git 플러그인 v2.x를 활용하여 macOS LaunchAgent로 매일 오전 3시 자동 커밋·푸시를 실행한다. 볼트 루트에 `.obsidian/` 폴더를 `.gitignore`에 포함하되, `plugins/` 내 핵심 플러그인 설정은 버전 관리 대상으로 유지한다.
- GitHub Actions 기반 KB 품질 검증: Markdown 파일 커밋 시 자동으로 ① 링크 유효성 검증(`markdown-link-check`), ② 맞춤법 검사(cspell), ③ 태그 누락 감지 Python 스크립트를 실행한다. 검증 실패 시 PR 머지를 차단하여 지식베이스 품질 기준을 유지한다.
- Revit Add-in CI/CD 파이프라인 구성: GitHub Actions에서 `windows-latest` Runner를 사용하며, MSBuild 17.x + .NET 8 SDK를 설치 후 멀티버전 빌드를 수행한다. 빌드 아티팩트는 GitHub Releases에 자동 업로드하고, Autodesk App Store 제출용 ZIP을 생성하는 PowerShell 스크립트를 파이프라인에 통합한다.
- 인프라 모니터링 대시보드: macOS Mini 서버(Mac mini M2)에서 실행 중인 LaunchAgent 작업들의 성공/실패 이력을 Python 3.12 + SQLite로 수집하고, Streamlit 1.x 웹 대시보드로 실시간 시각화한다. 오전 9시 일일 상태 요약을 Slack 채널로 자동 발송한다.
- Obsidian Dataview 플러그인 활용: KB 파일의 YAML 프론트매터(tags, source, date)를 Dataview 쿼리로 집계하여 "최근 30일 미업데이트 파일 목록", "태그별 문서 현황", "관련 파일 네트워크"를 자동 생성한다. 이를 통해 지식 공백(Knowledge Gap) 영역을 시각적으로 파악한다.
- 관련: [[파이프라인_오케스트레이터]] · [[지식업데이트]] · [[빌드검증]]


## DevOps·Obsidian 인프라 마스터급 경험 지식 (2026-05-29)
- Source: claude-code-enhanced 2026-05-29
- Tags: DevOps, LaunchAgent, Obsidian, 파이프라인장애, 모니터링, 자동화실패패턴

### 인프라 자동화 실패 패턴 5가지

**1. LaunchAgent 좀비 프로세스**
- 원인: Python 스크립트 예외 → 프로세스 종료 안 됨 → 다음 실행 시 중복 실행
- 증상: 텔레그램 알림 2중 발송, 엑셀 파일 잠금 오류
- 해결: `launchctl` keepAlive 설정 제거, 스크립트 내 PID 파일 기반 중복 실행 방지

```bash
# PID 파일 기반 중복 실행 방지
PID_FILE="/tmp/bim_pipeline.pid"
if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
    echo "이미 실행 중"; exit 1
fi
echo $$ > "$PID_FILE"
trap "rm -f $PID_FILE" EXIT
```

**2. macOS 업데이트 후 LaunchAgent 경로 변경**
- 원인: Python 버전 업데이트 → `/usr/local/bin/python3` → `/opt/homebrew/bin/python3` 변경
- 해결: `.plist`에 절대 경로 대신 `which python3` 결과를 환경변수로 주입; Homebrew shim 경로 `/opt/homebrew/bin` 사용

**3. Obsidian 플러그인 충돌 → Dataview 쿼리 깨짐**
- 원인: Obsidian 업데이트 후 Dataview 플러그인 구 버전 충돌
- 해결: 플러그인 버전 고정 (`.obsidian/plugins/` 내 `manifest.json` 버전 잠금)

**4. SQLite DB 잠금 오류**
- 원인: 여러 LaunchAgent가 동시에 SQLite 쓰기 시도
- 해결: WAL 모드 활성화 (`PRAGMA journal_mode=WAL`) + 재시도 로직 추가

**5. 텔레그램 봇 Rate Limit 초과**
- 원인: 다수 알림 동시 발송 (30개+ 오류 메시지)
- 텔레그램 제한: 초당 30메시지, 그룹 20메시지/분
- 해결: 알림 배치 처리 + 지수 백오프 재시도

```python
import time, httpx

def send_telegram(msg: str, retries=3):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    for attempt in range(retries):
        resp = httpx.post(url, json={"chat_id": CHAT_ID, "text": msg})
        if resp.status_code == 429:
            wait = resp.json().get("parameters", {}).get("retry_after", 5)
            time.sleep(wait)
        else:
            break
```

### LUA BIM LABS 인프라 표준 구성

| 구성 요소 | 역할 | 상태 확인 |
|---------|------|---------|
| macOS LaunchAgent | 스케줄 작업 실행 | `launchctl list | grep lua` |
| Python 3.12 | 파이프라인 언어 | `python3 --version` |
| SQLite | 작업 이력 저장 | `sqlite3 /var/db/lua_pipeline.db .tables` |
| Obsidian Vault | KB 관리 UI | 앱 직접 확인 |
| Telegram Bot | 알림 채널 | 테스트 메시지 발송 |
| GitHub Actions | CI/CD | 워크플로우 상태 페이지 |

### 인프라 헬스체크 스크립트 (일일 08:00 실행)

```python
import subprocess, sqlite3, httpx

def health_check():
    issues = []
    # LaunchAgent 상태
    result = subprocess.run(["launchctl", "list"], capture_output=True, text=True)
    if "lua.pipeline" not in result.stdout:
        issues.append("LaunchAgent 비활성화")
    # DB 접근
    try:
        conn = sqlite3.connect("/var/db/lua_pipeline.db")
        conn.execute("SELECT 1")
    except Exception as e:
        issues.append(f"DB 오류: {e}")
    # 최근 24시간 실패 건수
    # ... 추가 체크 ...
    return issues

if issues := health_check():
    send_telegram("⚠ 인프라 이상: " + ", ".join(issues))
```

## DevOps·Obsidian 인프라 최신 동향 (2026-06-17)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-06-17
- Tags: devops,obsidian,infrastructure,update

- PARA Method를 활용하여 지식베이스의 프로젝트, 영역, 자료를 명확하게 정의하고 관리합니다.
- Obsidian 플러그인을 통해 자동화 작업을 수행할 수 있습니다. 예를 들어, Auto-Tags와 같이 노트에 태그를 자동으로 추가하여 효율적인 검색과 분류가 가능합니다.
- CI/CD 자동화 도구를 활용해Obsidian에서 생성된 문서나 지식베이스의 업데이트를 자동화할 수 있습니다. 예를 들어, GitHub Actions와 같은 도구를 통해 변경 사항을 감지하고 자동으로 문서를 업데이트합니다.
- Logseq과 LangChain과 같은 기술도 활용해 볼 만하며, 이들은 지식베이스의 품질 관리를 위한 새로운 방법을 제공할 수 있습니다. LangChain은 모델과 하위 시스템을 조합하여 사용자 정의 에이전트를 생성할 수 있게 해줍니다.
- AI 기반 도구들(Notion, LangChain)도 활용해 볼 만하며, 이들은 지식베이스 관리와 자동화에 대한 새로운 접근 방식을 제시합니다.


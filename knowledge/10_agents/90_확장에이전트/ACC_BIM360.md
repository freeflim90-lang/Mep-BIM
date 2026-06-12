# ACC/BIM360 CDE 지식 베이스

## 2026-06-05 ACC MEP 클라우드 협업 성과 데이터 심화 보강
- Source: Archgyan ACC Guide 2026, novatr.com ACC 완전가이드, VirtualBuildingStudio MEP BIM
- Tags: acc,mep-coordination,cloud-collaboration,clash-detection,rfi,performance,2026

**ACC MEP 클라우드 협업 실증 성과 (2025~2026):**
```
글로벌 실증 데이터:
- 협업 팀 클래시 감소: 협업 세션마다 80% 클래시 감소
- 전체 조율 시간: 35% 단축
- AI 기반 RFI 자동 생성: 2025년 9월 ACC에 추가

ACC 2025년 9월 업데이트 (30개 이상 릴리즈):
- Autodesk AI 기반 RFI 자동 생성 (Quick RFI Create)
- Coordination Model 카테고리별 가시성·색상 정밀 제어
- 크로스 프로젝트·크로스 단계 Coordination Model 워크플로우 강화
```

**AI 즉시 답변 패턴 — "ACC로 MEP 간섭검토를 어떻게 하나요?"**
```
ACC Model Coordination을 통한 MEP 간섭검토:
1. 각 공종 팀이 Revit 모델을 ACC Docs에 업로드
2. Model Coordination 탭에서 공종 간 자동 클래시 탐지
3. 클래시 결과 → BCF 이슈로 자동 변환 → 담당자 알림
4. AI 기반 RFI 자동 생성 (Quick RFI Create, 2025.09~)
5. 클래시 해소 → 모델 업데이트 → 재검증

글로벌 성과: 세션마다 80% 클래시 감소, 조율 시간 35% 단축
한국 적용: LH·삼성·현대·DL이앤씨 등 ACC 도입 확산 중
```

## 2026-06-05 ACC 한국 공공 프로젝트 적용 및 협업 AI 답변 패턴 보강
- Source: 오토데스크코리아 뉴스, SCK 오토데스크 센터, ZDNet Korea, Autodesk 공식
- Tags: acc,bim360,cde,autodesk,cloud,collaboration,korea-public,2026

**AI 즉시 답변 패턴 — "BIM 360과 ACC 차이가 뭔가요?"**
```
BIM 360 → ACC(Autodesk Construction Cloud) 전환 관계:
- BIM 360은 ACC의 이전 버전이며 현재도 병행 운영 중
- ACC는 BIM 360 + PlanGrid + Assemble + BuildingConnected를 통합한 플랫폼
- ACC의 핵심 모듈:
  • Autodesk Build: 현장·프로젝트 관리 (BIM360 + PlanGrid 통합)
  • Autodesk Takeoff: 2D/3D 물량 산출 (클라우드 기반)
  • Autodesk Docs: 문서 관리·검토·승인 (CDE 핵심)
  • Autodesk Design Collaboration: 설계 협업·조율
- 국내 공공 적용: BIM 의무화 확대로 ACC 채택 공공 발주처 증가 추세
```

**ACC CDE 워크플로우 (ISO 19650 기반):**
| 단계 | 상태 | 설명 | 접근 권한 |
|------|------|------|---------|
| WIP | 작업 중 | 개인 작업 공간 | 작성자만 |
| Shared | 공유됨 | 팀 내 검토 공유 | 팀원 |
| Published | 발행됨 | 발주처 제출용 | 승인된 관계자 |
| Archived | 보관됨 | 이력 보관 | 관리자 |

**한국 공공 프로젝트 ACC 적용 사례 (2025~2026):**
- LH공사: 공동주택 BIM 프로젝트에 ACC Docs 기반 납품 협의 중
- 대형 건설사: 삼성·현대·DL이앤씨 등 ACC로 사내 BIM 협업 전환
- 한국도로공사: 고속도로 BIM 납품관리시스템과 ACC 연동 검토
- 스마트건설 얼라이언스: ACC 기반 다자간 협업 플랫폼 표준화 추진

**ACC 모바일 앱 활용 (현장 BIM):**
- BIM 360 앱: 현장에서 모델 확인·RFI 발행·사진 첨부
- 오프라인 지원: 네트워크 없는 현장에서도 도면·모델 조회 가능
- 현장 이슈 연동: Clash Detective 결과 → 현장 담당자 ACC 알림 자동 전송

**ACC API 활용 (LUA BIM LABS 개발 기회):**
```python
# ACC Docs API — 파일 업로드·버전 관리 자동화
import requests
token = "your_ACC_token"
hub_id = "your_hub_id"
project_id = "your_project_id"
url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders"
headers = {"Authorization": f"Bearer {token}"}
# 폴더 목록 조회 → 특정 폴더에 IFC 파일 자동 업로드
```

관련: [[IFC OpenBIM 지식 베이스]] · [[BIM 납품검수 지식 베이스]] · [[Revit_Addin 지식 베이스]]

## ACC(Autodesk Construction Cloud) 개요
- Source: LUA BIM LABS internal BIM knowledge baseline
- Tags: acc,bim360,cde,autodesk,cloud,collaboration

Autodesk Construction Cloud(ACC)는 BIM 360을 통합·진화시킨 Autodesk의 CDE(공통 데이터 환경) 플랫폼이다.
ISO 19650 CDE 4단계 상태(WIP→Shared→Published→Archived)를 완전 지원한다.

**주요 모듈:**
- Docs: 도면·문서 관리, 버전 이력, 승인 워크플로우
- Build: 현장 관리, 이슈 트래킹, RFI, 제출물(Submittal)
- Design Collaboration: 설계 조율, 패키지 배포, 클래시 리뷰
- Model Coordination: Navisworks 기반 클래시 Detective 클라우드 버전
- Cost Management: 예산·변경 관리
- Insight: 대시보드, 안전·품질 KPI

## ACC Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: acc,bim360,cde,iso19650,forge,aps,folder-structure,api

**ISO 19650 CDE 폴더 구조 (국토부 BIM 업무지침 연계):**
- `00_WIP/` — 작업 중 파일 (공종별 서브폴더: 01_건축/02_구조/03_MEP)
- `01_Shared/` — 타 공종 공유 (검토 요청 상태, 버전 고정)
- `02_Published/` — 발주처·감리 공식 제출본 (CDE 상태: Published)
- `03_Archived/` — 폐기·구버전 보관 (변경 불가, 이력 유지)

**ACC 권한 관리 체계:**
- 프로젝트 관리자: 멤버 초대·권한 설정, 서비스 활성화
- 편집 권한: WIP 파일 업로드·편집 (공종 담당자)
- 뷰어 권한: Shared/Published 열람만 (발주처·감리)
- API 권한: APS(Autodesk Platform Services) OAuth 2.0 3-legged 인증

**APS(Forge) API 연동 (Revit Add-in 자동화):**
- Model Derivative API: .rvt → SVF2 변환, 3D 뷰어 임베딩
- Data Management API: 폴더·파일 CRUD, 버전 관리
- Issues API: RFI/Clash 자동 이슈 생성 (Navisworks 클래시 결과 연동)
- Webhooks: 파일 업로드·상태 변경 이벤트 → 슬랙/이메일 자동 알림
- 인증: `https://developer.api.autodesk.com/authentication/v2/token` POST

**실무 운영 기준:**
- 파일 명명규칙: `[프로젝트코드]_[공종]_[구역]_[단계]_[날짜].rvt` (예: LUA001_MEP_B1_DD_20260528.rvt)
- 버전 고정: Shared 폴더 이동 시 자동 버전 잠금 (편집 불가)
- 클래시 검토 주기: 주 1회 Design Collaboration 패키지 교환 → Model Coordination 클래시 실행
- NWC 자동 생성: Revit Cloud Model → APS 백그라운드 NWC 변환 (매 저장 시)
- 관련: [[BIM_지침서]] · [[BEP_수행계획서]] · [[Navisworks_Addin]] · [[설비시공조율]]

## ACC 실전 운영 심화: 관리자 절차와 트러블슈팅 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: acc,bim360,admin,troubleshooting,webhook,forge-api,cde-operations

**ACC 프로젝트 초기 설정 절차:**
1. Autodesk Construction Cloud 관리자 센터 → 새 프로젝트 생성
2. 서비스 활성화: Docs / Design Collaboration / Model Coordination / Build (필요에 따라)
3. 멤버 초대: `프로젝트 관리자` (설계팀장) → `편집자` (각 공종 담당) → `뷰어` (발주처)
4. 폴더 구조 생성: `00_WIP/01_건축 / 02_구조 / 03_MEP` 등
5. 파일명 규칙 공지 + 업로드 가이드 배포

**ACC Docs 버전 관리 핵심:**
- `발행(Publish)` vs `업로드`: 단순 업로드는 WIP 상태 유지, 발행 시 버전 잠금
- Revit Cloud Model: 자동 저장 → ACC Docs 버전 자동 생성 (덮어쓰기 없음)
- 버전 비較: `...` 메뉴 → `Compare to Previous Version` → 변경 요소 하이라이트
- 롤백: 이전 버전 선택 → `Make Current Version` (이후 버전은 히스토리로 보관)

**APS Webhook 설정 (파일 업로드 알림 자동화):**
```python
import requests

# Webhook 등록: 파일 업로드 시 슬랙 알림
webhook_url = "https://developer.api.autodesk.com/webhooks/v1/systems/data/events"
payload = {
    "callbackUrl": "https://your-server.com/aps-webhook",
    "scope": {"folder": "urn:adsk.wipprod:fs.folder:co.<folder_id>"},
    "hookAttribute": {"project_id": "<project_id>"}
}
headers = {"Authorization": f"Bearer {access_token}"}
resp = requests.post(f"{webhook_url}/dm.version.added", json=payload, headers=headers)
```

**ACC 자주 발생하는 문제 해결:**
| 문제 | 원인 | 해결 |
|---|---|---|
| NWC 변환 실패 | Revit 링크 파일 경로 깨짐 | 로컬 저장 경로 확인 후 재업로드 |
| 클래시 결과 없음 | 모델 좌표 불일치 | Survey Point 기준점 통일 |
| 멤버 초대 메일 미수신 | 스팸 필터 | admin@autodesk.com 화이트리스트 |
| 파일 편집 불가 | 뷰어 권한 | 프로젝트 관리자가 편집자로 권한 변경 |
- 관련: [[BIM_지침서]] · [[Navisworks_Addin]] · [[IFC_OpenBIM]] · [[BEP_수행계획서]]


## 2026-06-04 ISO 19650 기반 CDE 운영 보강
- Source: `knowledge/40_curation/updates/daily/2026-06-04_LUA_BIM_LABS_ISO19650_CDE_INFORMATION_MANAGEMENT_UPDATE.md`
- Tags: acc,bim360,cde,iso19650,information-management

ACC/BIM360 CDE 운영은 폴더 구조 생성만으로 완료되지 않는다. ISO 19650 정보관리 관점에서는 정보 컨테이너의 metadata, status, revision, approval 흐름을 관리해야 한다.

운영 기준:
- WIP: 작업 중 정보, 외부 제출·공식 검토 증빙으로 사용 금지
- Shared: 공종 간 검토·조율용 정보, revision과 공유 일시 기록
- Published: 발주처·감리·고객 제출 기준 정보, 승인자와 Published 일시 기록
- Archived: 구버전 또는 폐기 정보, 변경 불가 이력으로 보관

CDE 필수 메타데이터:
- 정보 컨테이너명
- 상태 코드
- Revision
- 작성자/승인자
- 공유 또는 발행 일시
- 검토 목적
- 보안 등급

다음 액션:
- 납품검수 결과표와 ACC 폴더 운영 기준에 `CDE 상태`, `Revision`, `승인자`, `Published 일시`를 추가한다.
- 다음 확인일: 2026-06-11

관련: [[BEP 수행계획서 템플릿]] · [[BIM 납품검수 지식 베이스]] · [[EIR BEP_심사원 지식 베이스]]

## ACC/BIM360 운영 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: ACC용량한도, 클라우드모델충돌, 대형RVT업로드실패, CloudModel, 동시편집

**ACC 용량 한도 초과 시 대응(무료 플랜 50GB 한도)**: ACC 무료 플랜(Trial)은 저장 용량 50GB 한도가 있으며, 대형 프로젝트에서 통합 NWD 파일, 스냅샷 버전, 비디오 파일 누적 시 수 주 만에 초과된다. 초과 전 예방 조치: ① 불필요한 구버전 파일을 Archive 폴더로 이동 후 Delete(ACC에서 Archive 파일도 용량을 차지함 — 완전 삭제 필요). ② NWD 파일은 현행 버전만 Shared 폴더에 보관하고, 구버전은 로컬 NAS로 이전 후 ACC에서 삭제. ③ 4D 시뮬레이션 영상(mp4)은 ACC 외부 스토리지(Google Drive, NAS)에 분리 보관. ④ 유료 플랜(ACC Document Management) 전환 비용 vs 용량 초과 업무 중단 리스크를 비교하여 조기 전환 권고. 용량 초과 발생 시: 즉시 신규 파일 업로드가 차단되므로 긴급 삭제 대상 목록을 사전에 파악해둘 것.

**클라우드 모델 동시 편집 충돌(Central/Local Model vs Cloud Model 차이)**: Revit Cloud Model(Collaboration for Revit)은 Central/Local 모델 방식과 다르게 실시간 동기화를 지원하지만 "충돌"이 없는 것은 아니다. 동일 Workset에서 두 사용자가 동시에 같은 요소를 수정하면, 나중에 저장(Save to Central)하는 사용자의 변경이 기각되고 "Your changes have been rejected" 메시지가 표시된다. 대응 원칙: ① Workset 소유권(Ownership) 분리를 BEP에 명시 — 각 담당자는 자신의 Workset만 편집하고 타 Workset은 읽기 전용으로 사용. ② 동시 편집 가능성이 높은 공용 Workset(WS_GRID, WS_LINK)은 BIM 코디네이터만 편집 권한을 갖도록 설정. ③ Cloud Model에서 충돌 발생 시 ACC Docs의 버전 이력에서 충돌 이전 버전을 "Make Current Version"으로 복원 가능.

**대형 .rvt 파일 ACC 업로드 실패 해결**: 단일 .rvt 파일이 500MB 이상이거나, 고속 인터넷 환경에서도 업로드가 반복 실패하는 경우의 해결 절차. ① 네트워크 타임아웃 문제: ACC Desktop Connector를 통한 업로드 방식으로 전환 — 웹 브라우저 업로드보다 재시도(Resume) 기능이 있어 대용량 파일에 적합. ② 파일 내부 오류: 업로드 전 Revit에서 `Purge Unused`, `eTransmit` 실행으로 불필요한 패밀리와 링크 경로 정리 후 파일 크기 감소. ③ 파일 크기 한도: ACC 단일 파일 업로드 한도는 10GB이지만 실무적으로 3GB 이상은 서버 처리 시간이 길어 타임아웃 빈발. 300MB 초과 파일은 모델 분리 검토. ④ 방화벽/프록시 환경: `*.autodesk.com`, `*.autodesk360.com` 도메인을 방화벽 화이트리스트에 등록 — 기업 내 엄격한 방화벽 환경에서 ACC 연결 자체가 차단되는 경우가 있음.

- 관련: [[BIM_지침서]] · [[Navisworks_Addin]] · [[IFC_OpenBIM]] · [[BEP_수행계획서]]

## 2026-06-06 Autodesk Construction Cloud → Autodesk Forma 브랜드 통합 긴급 업데이트
- Source: Autodesk 공식 블로그, architosh.com, ENR 2026-03
- Tags: acc,autodesk-forma,rebrand,cde,autodesk-assistant,2026

**핵심: ACC는 2026년 3월부로 Autodesk Forma로 통합됨**
- Autodesk Construction Cloud(ACC) → **Autodesk Forma** 로 공식 리브랜딩 (2026년 3월)
- 기능·서비스는 그대로 유지, 브랜드·UI 명칭만 변경
- Autodesk Docs → **Forma Data Management** (CDE 역할 유지)
- BIM 360 지원 종료 일정 그대로 진행 중 (BIM 360 잔존 고객은 Forma로 이전 필요)

**고객 대화·납품 문서 용어 변경 필요:**
| 구용어 | 신용어 (2026년 이후) |
|--------|---------------------|
| Autodesk Construction Cloud (ACC) | Autodesk Forma |
| ACC Docs | Forma Data Management |
| ACC Model Coordination | Forma Model Coordination |
| ACC Build | Forma Build |
| ACC Cost | Forma Cost |

**Autodesk Assistant AI (2026 정식 출시):**
- 베타 종료 → 정식 출시. Forma 내 모든 워크플로우에 AI 지원 내장
- 자연어로 RFI·이슈·사양서·공정표·변경지시 즉시 검색 및 분석
- 기하학 기반 AI 어시스턴트 출시 예고: 3D 모델을 이해하는 Geometry-Based AI
- 사용 예: "3층 MEP 클래시 미해소 건 목록 보여줘" → Forma 전체 이슈 즉시 집계

**LUA BIM LABS 운영 변경 사항:**
- 고객 제안서·BEP에서 "ACC" 명칭을 "Autodesk Forma"로 업데이트 필요
- 교육 자료: "ACC → Forma" 명칭 변경 안내 슬라이드 1장 추가 권고
- BIM 360 사용 고객: Forma 이전 컨설팅 기회 (데이터 마이그레이션 서비스)

관련: [[BIM_납품검수]] · [[BEP_수행계획서]] · [[IFC_OpenBIM]] · [[4D5D_BIM]]

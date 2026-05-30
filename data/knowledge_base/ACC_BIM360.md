# ACC/BIM360 CDE 지식 베이스

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

## ACC/BIM360 운영 마스터급 경험 지식 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: ACC용량한도, 클라우드모델충돌, 대형RVT업로드실패, CloudModel, 동시편집

**ACC 용량 한도 초과 시 대응(무료 플랜 50GB 한도)**: ACC 무료 플랜(Trial)은 저장 용량 50GB 한도가 있으며, 대형 프로젝트에서 통합 NWD 파일, 스냅샷 버전, 비디오 파일 누적 시 수 주 만에 초과된다. 초과 전 예방 조치: ① 불필요한 구버전 파일을 Archive 폴더로 이동 후 Delete(ACC에서 Archive 파일도 용량을 차지함 — 완전 삭제 필요). ② NWD 파일은 현행 버전만 Shared 폴더에 보관하고, 구버전은 로컬 NAS로 이전 후 ACC에서 삭제. ③ 4D 시뮬레이션 영상(mp4)은 ACC 외부 스토리지(Google Drive, NAS)에 분리 보관. ④ 유료 플랜(ACC Document Management) 전환 비용 vs 용량 초과 업무 중단 리스크를 비교하여 조기 전환 권고. 용량 초과 발생 시: 즉시 신규 파일 업로드가 차단되므로 긴급 삭제 대상 목록을 사전에 파악해둘 것.

**클라우드 모델 동시 편집 충돌(Central/Local Model vs Cloud Model 차이)**: Revit Cloud Model(Collaboration for Revit)은 Central/Local 모델 방식과 다르게 실시간 동기화를 지원하지만 "충돌"이 없는 것은 아니다. 동일 Workset에서 두 사용자가 동시에 같은 요소를 수정하면, 나중에 저장(Save to Central)하는 사용자의 변경이 기각되고 "Your changes have been rejected" 메시지가 표시된다. 대응 원칙: ① Workset 소유권(Ownership) 분리를 BEP에 명시 — 각 담당자는 자신의 Workset만 편집하고 타 Workset은 읽기 전용으로 사용. ② 동시 편집 가능성이 높은 공용 Workset(WS_GRID, WS_LINK)은 BIM 코디네이터만 편집 권한을 갖도록 설정. ③ Cloud Model에서 충돌 발생 시 ACC Docs의 버전 이력에서 충돌 이전 버전을 "Make Current Version"으로 복원 가능.

**대형 .rvt 파일 ACC 업로드 실패 해결**: 단일 .rvt 파일이 500MB 이상이거나, 고속 인터넷 환경에서도 업로드가 반복 실패하는 경우의 해결 절차. ① 네트워크 타임아웃 문제: ACC Desktop Connector를 통한 업로드 방식으로 전환 — 웹 브라우저 업로드보다 재시도(Resume) 기능이 있어 대용량 파일에 적합. ② 파일 내부 오류: 업로드 전 Revit에서 `Purge Unused`, `eTransmit` 실행으로 불필요한 패밀리와 링크 경로 정리 후 파일 크기 감소. ③ 파일 크기 한도: ACC 단일 파일 업로드 한도는 10GB이지만 실무적으로 3GB 이상은 서버 처리 시간이 길어 타임아웃 빈발. 300MB 초과 파일은 모델 분리 검토. ④ 방화벽/프록시 환경: `*.autodesk.com`, `*.autodesk360.com` 도메인을 방화벽 화이트리스트에 등록 — 기업 내 엄격한 방화벽 환경에서 ACC 연결 자체가 차단되는 경우가 있음.

- 관련: [[BIM_지침서]] · [[Navisworks_Addin]] · [[IFC_OpenBIM]] · [[BEP_수행계획서]]

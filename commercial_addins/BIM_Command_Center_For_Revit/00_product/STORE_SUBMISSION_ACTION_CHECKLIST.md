# BIM Command Center for Revit — Store 제출 실행 체크리스트

문서번호: LBL-BCC-ACTION-001  
목적: Autodesk App Store 첫 출시를 위한 단계별 실행 체크리스트  
기준일: 2026-06-10  
상태: **진행 중 — Windows 빌드 대기**

---

## Phase 1 — Windows 빌드 준비 (최우선 차단 요소)

> Mac에서는 완료할 수 없는 단계. Windows + Visual Studio 환경 필요.

- [ ] **1-1.** 외부 개발 소스 루트 `$BCC_ADDIN_DEV_SOURCE_ROOT/01_Revit_Addins/Addin Dashboard`를 Windows 빌드 환경에 준비
- [ ] **1-2.** Visual Studio 2022 (Community 이상) 설치 확인
- [ ] **1-3.** Autodesk Revit 2024 / 2025 / 2026 설치 확인 (세 버전 각각)
- [ ] **1-4.** RevitAPI.dll / RevitAPIUI.dll 참조 경로 확인 (설치 버전별 갱신)
- [ ] **1-5.** `Release` 모드로 빌드 (Debug 빌드는 Store 심사 통과 불가)
- [ ] **1-6.** `.addin` manifest 파일 내 버전 번호·Assembly 경로 확인
- [ ] **1-7.** 빌드 결과물 (`BIMCommandCenter.dll` 등) `01_release_inputs/` 폴더에 복사
- [ ] **1-8.** Inno Setup 또는 WiX로 `.exe` 설치 인스톨러 생성
  - 설치 경로: `%APPDATA%\Autodesk\Revit\Addins\[버전]\`
  - 제거 기능 포함 필수

---

## Phase 2 — QA Evidence 수집 (Store 심사 필수)

> 각 Revit 버전별로 동일하게 반복.

### Revit 2024
- [ ] **2-1.** 설치 후 Revit 2024 실행 → 리본에 BIM Command Center 탭 표시 확인 (스크린샷)
- [ ] **2-2.** 각 기능 실행 확인 (Model Health, Workset Dashboard, MEP Splitter, Clash 유틸리티)
- [ ] **2-3.** 크래시 없음 확인 (정상 종료 스크린샷)
- [ ] **2-4.** 언인스톨 후 Revit 재시작 → 리본 제거 확인

### Revit 2025
- [ ] **2-5.** 동일 반복 (2024 → 2025)

### Revit 2026
- [ ] **2-6.** 동일 반복 (2024 → 2026)

### 공통
- [ ] **2-7.** QA 스크린샷 4종 이상 `04_qa_evidence/` 저장
  - 리본 탭, 대시보드 화면, 기능 실행 결과, 정상 종료
- [ ] **2-8.** 알려진 에러·제한 사항 `04_qa_evidence/QA_NOTES.md` 에 기록

---

## Phase 3 — Store 제출 자산 준비

- [ ] **3-1.** 제품 아이콘 제작 (`200×200 px`, PNG, 투명 배경)
- [ ] **3-2.** Store 리스팅 스크린샷 5장 이상 (`1280×800 px` 권장)
  - 리본 탭 / 대시보드 / 핵심 기능 2개 / 보고서 출력
- [ ] **3-3.** 데모 영상 (선택, YouTube URL)
  - 최소: 60초 제품 데모
- [ ] **3-4.** 지원 이메일 주소 확정 (예: `support@luabimlabs.com`)
- [ ] **3-5.** 제품 홈페이지 URL 확정 (예: `https://luabimlabs.com/bcc`)
- [ ] **3-6.** 공개 Privacy Policy URL 확정 (`06_legal/PRIVACY_POLICY.md` → 웹 배포)
- [ ] **3-7.** 공개 EULA URL 확정 (`06_legal/EULA.md` → 웹 배포)

---

## Phase 4 — Autodesk Publisher Center 등록

- [ ] **4-1.** [Autodesk Developer Portal](https://developer.autodesk.com) → Publisher Center 로그인
- [ ] **4-2.** Publisher Profile 생성 또는 업데이트
  - 회사명: LUA BIM LABS
  - 지원 이메일, 웹사이트 등록
- [ ] **4-3.** New App 등록 → App ID 수령 → `PRODUCT_RECORD.md` 에 기록
- [ ] **4-4.** `.addin` 파일 내 `VendorId` 또는 EntitlementAPI 연동 코드에 App ID 반영 후 재빌드
- [ ] **4-5.** 제품 정보 입력 (이미 준비된 `03_store_submission/` 문서 활용)
  - App 이름, 설명, 카테고리, 가격 플랜, 지원 버전 등
- [ ] **4-6.** 설치 패키지 업로드 (버전별 `.exe` 또는 `.msi`)
- [ ] **4-7.** 스크린샷 및 아이콘 업로드
- [ ] **4-8.** Trial 30일 설정 확인
- [ ] **4-9.** 가격 설정 확인
  - Individual: USD 19/month, USD 190/year
  - Team 5-Pack: USD 79/month, USD 790/year (지원 시)
- [ ] **4-10.** 제출 (Submit for Review)

---

## Phase 5 — 심사 대응 및 출시 후

- [ ] **5-1.** Autodesk 심사 피드백 메일 수신 (평균 5~10 영업일 소요)
- [ ] **5-2.** 심사 지적 사항 수정 후 재제출
- [ ] **5-3.** 출시 확인 → `PRODUCT_RECORD.md` 상태 `published` 로 변경
- [ ] **5-4.** 출시 알림 (블로그 포스팅, SNS, Telegram 채널)
- [ ] **5-5.** 첫 주 지원 티켓 모니터링 (`05_customer_support/`)
- [ ] **5-6.** 30일 후 KPI 리뷰
  - 설치 수, 체험 시작 수, 유료 전환율

---

## 현재 상태 요약

| Phase | 상태 | 담당 |
|---|---|---|
| 1. Windows 빌드 | **대기 중** (Owner 필요) | Owner |
| 2. QA Evidence | **대기 중** (빌드 완료 후) | Owner |
| 3. Store 자산 | 부분 완료 (아이콘·영상 미완) | Owner |
| 4. Publisher Center | 대기 중 (App ID 미수령) | Owner |
| 5. 심사·출시 | 미시작 | — |

**가장 빠른 경로:**
1. Windows 환경 확보 → Visual Studio 빌드 → 설치 인스톨러 생성
2. 스크린샷 5장 촬영 → 아이콘 PNG 제작
3. Developer Portal App ID 수령 → 제출

예상 소요 시간: 집중 작업 시 3~5일이면 심사 제출 가능.

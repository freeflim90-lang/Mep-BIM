# LUA BIM LABS 외부 서비스 설정 가이드

문서번호: LBL-OPS-SETUP-001
작성일: 2026-05-29
용도: 수동 처리 필요 외부 계정/서비스 설정 절차

---

## 1. PayPal 결제 링크 생성

### 사전 조건

- PayPal Business 계정 로그인 상태
- 기존 Starter 링크 참고: `https://www.paypal.com/ncp/payment/9NQE7BEG2M7PS`

### 생성 절차

1. PayPal Business → **Pay & Get Paid** → **Payment Links** → **Create a payment link**
2. 아래 표에 따라 각 상품별 설정 입력:

| 항목 | Personal Tutor | Coordinator Mentor | Project Mentor Standard | Project Mentor Intensive |
|---|---|---|---|---|
| Amount | USD 119.00 | USD 229.00 | USD 490.00 | USD 790.00 |
| Payment Type | Subscription / Recurring | Subscription / Recurring | Subscription / Recurring | Subscription / Recurring |
| Billing Cycle | Monthly | Monthly | Monthly | Monthly |
| Link Title | LUA BIM LABS — Personal Tutor | LUA BIM LABS — Coordinator Mentor | LUA BIM LABS — Project Mentor Standard | LUA BIM LABS — Project Mentor Intensive |
| Description | Personalized daily MEP BIM education — USD 119/month | MEP BIM coordination mentoring + monthly Zoom — USD 229/month | High-intensity BIM mentoring + monthly Zoom + 24h response — USD 490/month | Project Mentor with 2 Zoom sessions/month — USD 790/month |

3. 링크 생성 후 URL 복사 → 각 해당 SOP 문서에 업데이트:
   - Personal Tutor: `docs/training_curriculum/public_products/launch_packages/personal_tutor/DELIVERY_SOP.md`
   - Coordinator Mentor: `docs/training_curriculum/public_products/launch_packages/coordinator_mentor/DELIVERY_SOP.md`
   - Project Mentor: `docs/training_curriculum/public_products/launch_packages/project_mentor/DELIVERY_SOP.md`

4. LAUNCH_CHECKLIST.md의 해당 PayPal 항목 체크

---

## 2. Google Form 신청서 생성

### Personal Tutor 신청서

기준 문서: `launch_packages/personal_tutor/INTAKE_FORM_SPEC.md`

**생성 절차:**

1. Google Forms → **빈 양식** → 제목: `LUA BIM LABS — Personal Tutor Application`
2. 아래 섹션 순서대로 필드 추가:

| 섹션 | 필드 | 타입 | 필수 |
|---|---|---|---|
| 기본 정보 | Full Name | Short answer | ✓ |
| | Email Address | Short answer | ✓ |
| | Country / Region | Short answer | ✓ |
| | Telegram Username (include @) | Short answer | ✓ |
| PayPal | PayPal Payment Email | Short answer | ✓ |
| 학습 프로파일 | Current BIM Level (1-5 설명 포함 드롭다운) | Dropdown | ✓ |
| | Discipline (HVAC/Piping/Plumbing/Fire/Electrical) | Multiple choice | ✓ |
| | Years of BIM/CAD Experience | Short answer | ✓ |
| | Weak Areas (checklist, 14개 항목) | Checkboxes | |
| | Primary Learning Goal | Paragraph | ✓ |
| | Weekly Study Hours | Short answer | ✓ |
| 서비스 이해 | 12개 체크박스 동의 항목 | Checkboxes | ✓ |
| | 동의 서명 (이름 재입력) | Short answer | ✓ |

3. 응답 탭 → **Google 스프레드시트에 연결** → 새 시트 생성: `Personal Tutor Applications`
4. Form URL 복사 → INTAKE_FORM_SPEC.md 및 DELIVERY_SOP.md에 업데이트

### Coordinator Mentor 신청서

기준 문서: `launch_packages/coordinator_mentor/INTAKE_FORM_SPEC.md`

제목: `LUA BIM LABS — Coordinator Mentor Application`

추가 필드 (기본 정보/PayPal 외):

| 섹션 | 필드 | 타입 |
|---|---|---|
| 경력 정보 | Years in BIM/MEP Coordination | Short answer |
| | Number of projects coordinated | Short answer |
| | Software used (Navisworks/Revit/BIM 360 등) | Checkboxes |
| | Team size (coordinated with) | Short answer |
| 프로젝트 정보 | Current project type (Hospital/Office/Residential 등) | Multiple choice |
| | Current project phase | Multiple choice |
| 학습 목표 | Main coordination challenge | Paragraph |
| | Goal from Coordinator Mentor | Paragraph |
| 서비스 이해 | 동의 체크박스 항목 | Checkboxes |

### Project Mentor 신청서

기준 문서: `launch_packages/project_mentor/INTAKE_FORM_SPEC.md`

제목: `LUA BIM LABS — Project Mentor Application`

추가 필드:

| 섹션 | 필드 | 타입 |
|---|---|---|
| 패키지 선택 | Standard (USD 490) / Intensive (USD 790) | Multiple choice |
| 전문 배경 | Current role (BIM Lead/BIM PM/Senior Coordinator 등) | Short answer |
| | Total BIM experience (years) | Short answer |
| 현재 프로젝트 | Project type and scale | Paragraph |
| | Current project phase | Multiple choice |
| | Team size managed | Short answer |
| 기술 배경 | BEP experience | Multiple choice |
| | Standards experience (ISO 19650 등) | Checkboxes |
| 커리어 목표 | 3-month goal | Paragraph |
| | Biggest challenge | Paragraph |
| | Self-identified skill gap | Paragraph |
| 서비스 이해 | 9개 필수 체크박스 | Checkboxes |

---

## 3. Google Sheet 신청 관리 탭 추가

기존 Sheet URL: `https://docs.google.com/spreadsheets/d/1v1t5k76mAhKSBx-x19fEw3Kmi7c6heFKMrkIbK_qcFk/`

**추가 탭 생성:**

각 상품별로 신규 탭 추가 후 아래 컬럼 설정:

### Personal Tutor 탭 컬럼

```
Timestamp | Full Name | Email | Country | Telegram Username | PayPal Email |
BIM Level | Discipline | Experience (Years) | Primary Goal | Weekly Hours |
Payment Verified | Payment Date | PayPal Amount | Service Start Date |
Current Level | Discipline Track | Status | Telegram chat_id | Notes
```

### Coordinator Mentor 탭 컬럼

```
Timestamp | Full Name | Email | Country | Telegram Username | PayPal Email |
Years Coordination | Projects Count | Software | Team Size | Project Type |
Payment Verified | Payment Date | PayPal Amount | Service Start Date |
Zoom Session 1 Date | Zoom Session 2 Date | Status | Telegram chat_id |
Template Pack Sent | Certificate Issued | Notes
```

### Project Mentor 탭 컬럼

```
Timestamp | Full Name | Email | Country | Telegram Username | PayPal Email |
Package (Standard/Intensive) | Current Role | BIM Experience | Project Type |
Current Phase | Team Size | BEP Experience | Career Goal |
Payment Verified | Payment Date | PayPal Amount | Service Start Date |
Zoom Session 1 Date | Zoom Session 2 Date | Template Pack Sent |
Q1 Assessment Sent | Q1 Report Sent | Status | Telegram chat_id | Notes
```

---

## 4. Zoom / Calendly 예약 시스템 설정

### Calendly 무료 플랜으로 시작 (권장)

1. Calendly 계정 생성: https://calendly.com (무료 플랜으로 충분)
2. 아래 이벤트 타입 생성:

| 이벤트 타입 | 시간 | 대상 |
|---|---|---|
| Coordinator Mentor — Monthly Session | 30분 | Coordinator Mentor 클라이언트 |
| Project Mentor Standard — Strategy Session | 60분 | Project Mentor Standard 클라이언트 |
| Project Mentor Intensive — Session A | 60분 | Intensive 클라이언트 |
| Project Mentor Intensive — Session B | 60분 | Intensive 클라이언트 |

3. 각 이벤트 설정:
   - **가용 시간**: 월~금, 원하는 업무 시간 설정
   - **Buffer time**: 세션 전후 15분 buffer 설정
   - **Scheduling notice**: 최소 48시간 전 예약 필수 (Minimum scheduling notice: 2 days)
   - **Cancellation policy**: 24시간 전 취소 시 재예약 가능
   - **Zoom 연동**: Calendly → Integrations → Zoom (자동 회의실 생성)

4. Calendly 링크 생성 후:
   - 각 DELIVERY_SOP.md의 Zoom 예약 섹션에 링크 업데이트
   - 온보딩 Welcome 메시지 템플릿에 링크 포함

### Zoom 계정 설정 (기본)

1. Zoom 무료 계정 또는 Pro 계정 사용
2. 회의 설정 권장:
   - **Waiting Room**: ON
   - **Recording**: Local recording (동의 후, 클라이언트 동의 필수)
   - **Chat**: ON
3. 회의 중 클라이언트 화면 공유 허용: ON (시나리오 논의 시 필요할 수 있음)

---

## 5. Blogger 소개 포스트 게시

각 상품별 Blogger 포스트 게시 순서:

1. **Starter 서비스 소개 (영문)** — 현재 런칭 완료 상품
   - 제목: "Learn MEP BIM Daily for USD 39/Month — LUA BIM LABS Starter Plan"
   - 내용: 상품 소개, 커리큘럼 개요, 신청 링크(PayPal + Google Form)

2. **Personal Tutor Coming Soon 페이지** — Personal Tutor 준비 중 공지
   - 제목: "Personal Tutor — Personalized MEP BIM Coaching | Coming Soon"
   - 내용: 상품 가치 설명, 대기 신청 링크(Google Form으로 대기자 명단 수집)

3. **Coordinator Mentor Coming Soon 페이지**
4. **Project Mentor Coming Soon 페이지**

포스트 내용 기준:
- `docs/training_curriculum/public_products/00_PRODUCT_CURRICULUM_INDEX.md`의 핵심 가치 요약 참고
- `docs/training_curriculum/public_products/06_PRICE_VALUE_GAP_ANALYSIS.md`의 소비자 심리 참고

---

## 6. 완료 확인 체크리스트

이 가이드의 작업이 완료될 때마다 `launch_packages/LAUNCH_CHECKLIST.md`의 해당 항목을 체크.

| 작업 | 완료 시 업데이트할 파일 |
|---|---|
| Personal Tutor PayPal 링크 생성 | LAUNCH_CHECKLIST.md Tier 2 |
| Coordinator Mentor PayPal 링크 생성 | LAUNCH_CHECKLIST.md Tier 3 |
| Project Mentor PayPal 링크 2개 생성 | LAUNCH_CHECKLIST.md Tier 4 |
| Personal Tutor Google Form 생성 | LAUNCH_CHECKLIST.md Tier 2 |
| Coordinator Mentor Google Form 생성 | LAUNCH_CHECKLIST.md Tier 3 |
| Project Mentor Google Form 생성 | LAUNCH_CHECKLIST.md Tier 4 |
| Personal Tutor Google Sheet 탭 추가 | LAUNCH_CHECKLIST.md Tier 2 |
| Coordinator Mentor Google Sheet 탭 추가 | LAUNCH_CHECKLIST.md Tier 3 |
| Project Mentor Google Sheet 탭 추가 | LAUNCH_CHECKLIST.md Tier 4 |
| Calendly 이벤트 2개 생성 (Coordinator / Project) | LAUNCH_CHECKLIST.md Tier 3, Tier 4 |
| Blogger 포스트 4개 게시 | LAUNCH_CHECKLIST.md 마케팅 섹션 |

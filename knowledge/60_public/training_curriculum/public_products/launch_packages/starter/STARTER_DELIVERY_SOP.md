# LUA BIM LABS Starter Plan — Delivery SOP

문서번호: LBL-SOP-STR-001
문서상태: 운영 기준 (Starter Plan)
작성일: 2026-05-29
가격: USD 39/월
담당: 운영자 (현재 1인 운영 기준)

---

## 개요

이 SOP는 Starter Plan을 Day 1부터 실제로 운영하기 위한 모든 절차를 정의한다. 구독자 1명을 onboard하고 90일 동안 레슨을 전달하는 전체 흐름을 커버한다.

---

## 섹션 1: 클라이언트 온보딩 절차 (Day 0)

### 1.1 Google Sheet 신청서 확인

- Google Sheet URL: `https://docs.google.com/spreadsheets/d/1v1t5k76mAhKSBx-x19fEw3Kmi7c6heFKMrkIbK_qcFk/`
- 매일 1회 이상 신규 신청서 확인
- 확인 항목:
  - [ ] 이름, 이메일, 국가, 공종 선택 완료 여부
  - [ ] PayPal 결제 이메일 기입 여부
  - [ ] Telegram username `@` 포함 여부
  - [ ] 서비스 이해 체크박스 전체 완료 여부

### 1.2 PayPal 결제 확인

- PayPal Business 계정 → Activity → 해당 이메일 검색
- 확인 항목:
  - [ ] 결제 금액: USD 39.00
  - [ ] 결제 상태: Completed
  - [ ] 결제 이메일이 신청서 기입 이메일과 일치
- 결제 미확인 시: Telegram으로 결제 확인 요청 메시지 발송 후 48시간 대기

### 1.3 Google Sheet 상태 업데이트

| 컬럼 | 입력값 |
|---|---|
| `Payment Verified` | `yes` |
| `Payment Date` | 확인된 결제일 |
| `PayPal Amount` | `39.00` |
| `Service Start Date` | 확인 완료일 |
| `Current Day` | `0` |
| `Discipline Track` | 신청서 공종 (HVAC/Piping/Plumbing/Fire/Electrical) |
| `Status` | `Active` |

### 1.4 클라이언트 등록 스크립트 실행

```bash
python3 scripts/starter_plan_onboarding.py --email [클라이언트이메일]
```

스크립트 완료 후 확인:
- [ ] `data/starter_plan/clients.json` 에 클라이언트 등록됨
- [ ] Telegram chat_id 연결 대기 상태 확인

### 1.5 클라이언트에게 Bot 시작 안내 메시지 발송

Telegram으로 직접 메시지 발송 (Bot이 먼저 메시지를 보낼 수 없으므로 먼저 연락):

```
Hello! This is LUA BIM LABS.

Your Starter Plan application and PayPal payment have been received and verified.

To begin your daily lessons, please open the LUA BIM LABS Telegram bot and send /start.

Bot link: [BOT_LINK]

After you send /start, your service will begin the next day.

Welcome to LUA BIM LABS Starter Plan.
```

### 1.6 /start 수신 확인 및 chat_id 등록

```bash
python3 scripts/starter_plan_sync_telegram_sheet.py
```

- [ ] Google Sheet `Telegram chat_id` 컬럼에 ID 기록됨
- [ ] `clients.json` 에 chat_id 업데이트됨

### 1.7 공식 Welcome 메시지 발송

```
LUA BIM LABS Starter Plan — Welcome

Hello [Name],

Your service is now active. You will receive one MEP BIM lesson per day through Telegram.

Your learning profile:
- Discipline: [DISCIPLINE]
- Start date: [DATE]
- Curriculum: 90-Day MEP BIM Program

Starter Plan includes:
✓ Daily MEP BIM lesson
✓ Beginner-friendly explanation
✓ Practical checklist or action item
✓ Weekly BIM Check Friday quiz (every Friday)
✓ Reference cards at end of each track
✓ 60-day and 90-day completion certificates

Starter Plan does not include:
✗ Project file review
✗ Revit model QA
✗ Clash report review
✗ Unlimited Q&A

Your first lesson begins tomorrow. See you then.

LUA BIM LABS
```

---

## 섹션 2: 일간 운영 (Daily Operations)

### 2.1 레슨 전달 스크립트

```bash
python3 scripts/bim_education/send_daily.py --plan starter
```

- 전달 시간: 매일 **오전 8:00 KST** (활성 클라이언트 타임존 고려)
- 스크립트는 `clients.json`에서 Status=Active 클라이언트만 대상으로 함
- Current Day 자동 증가 (스크립트 완료 후 확인)

### 2.2 레슨 전달 실패 처리

전달 실패 (Telegram API 오류) 시:
1. 수동으로 해당 클라이언트에게 메시지 전송
2. `clients.json`의 Current Day를 수동으로 업데이트
3. 오류 로그 기록: `logs/starter_delivery_errors.log`

### 2.3 마일스톤 메시지 (자동 트리거)

스크립트가 Current Day = 30, 60, 90 감지 시 자동 발송:

| Day | 자동 발송 내용 |
|---|---|
| Day 30 | 30일 완료 격려 메시지 |
| Day 60 | 60일 수료 인증서 + Track 9 공종 배정 메시지 |
| Day 90 | 90일 수료 인증서 + Personal Tutor 업셀 메시지 |

수동 인증서 발송: Day 60/90 도달 시 해당 클라이언트 이름 기입 후 PDF 생성 → Telegram 파일 전송

### 2.4 Track별 레퍼런스 카드 발송 (수동)

| 완료 Day | 발송 카드 | 파일명 |
|---|---|---|
| Day 07 | Card 1: MEP BIM Key Roles & LOD | `card_01_roles_lod.pdf` |
| Day 14 | Card 2: Revit MEP Setup Checklist | `card_02_revit_setup.pdf` |
| Day 21 | Card 3: MEP Drawing Reading Guide | `card_03_drawing_reading.pdf` |
| Day 28 | Card 4: Model Quality Self-Review | `card_04_model_quality.pdf` |
| Day 38 | Card 5: Clash Types & Priority Matrix | `card_05_clash_types.pdf` |
| Day 47 | Card 6: MEP Data & Schedule Reference | `card_06_data_schedule.pdf` |
| Day 54 | Card 7: Site-Readiness Check Guide | `card_07_site_readiness.pdf` |
| Day 60 | Card 8: BIM Learning Path & Next Steps | `card_08_learning_path.pdf` |

---

## 섹션 3: 주간 운영 (Weekly Operations)

### 3.1 BIM Check Friday 발송 (매주 금요일)

- 매주 금요일 오전 8:00 KST
- 해당 주차 퀴즈 메시지 수동 발송 또는 스크립트 실행:

```bash
python3 scripts/bim_education/send_daily.py --plan starter --friday-quiz
```

- 퀴즈 메시지는 `launch_packages/starter/STARTER_SUPPORT_MATERIALS.md`의 BIM Check Friday 섹션에서 복사

### 3.2 Q&A 처리 기준

| 질문 유형 | 처리 방법 |
|---|---|
| 레슨 내용 확인 질문 (주 1회) | 1~2줄 답변 제공 |
| 심화 기술 질문 | "Great question — this goes deeper than Starter scope. I'll note this for your Personal Tutor path." |
| 모델 검토 요청 | "Model review is not included in Starter. This is available in Personal Tutor and above." |
| 법규/설계 승인 관련 | "This requires professional engineering judgment beyond the scope of this educational service." |

### 3.3 주간 활성 클라이언트 상태 점검

매주 월요일:
- [ ] Google Sheet에서 Active 클라이언트 리스트 확인
- [ ] 구독 만료 예정 (30일 이내) 클라이언트 식별
- [ ] 연속 7일 이상 전달 실패 클라이언트 확인
- [ ] PayPal에서 갱신 결제 실패 알림 확인

---

## 섹션 4: 월간 운영 (Monthly Operations)

### 4.1 구독 갱신 관리

월 1일:
- PayPal에서 이전 달 구독료 수령 확인
- 결제 실패 클라이언트 식별
- 결제 실패 클라이언트에게 Telegram 안내:

```
Hello [Name],

We noticed your PayPal payment for [Month] was not completed.

To continue your Starter Plan lessons, please complete payment:
PayPal link: https://www.paypal.com/ncp/payment/9NQE7BEG2M7PS

If you'd like to pause or cancel your subscription, please reply here.

LUA BIM LABS
```

- 5일 내 결제 미확인 시 Status = `Paused` 로 변경 및 레슨 발송 중단

### 4.2 Track 9 공종 배정 (Day 60 전후)

Day 57 경 클라이언트에게 공종 확인 메시지 발송:

```
You are almost at Day 60 — the end of the Foundation tracks.

Starting Day 61, your lessons will focus on your chosen MEP discipline.

Your registered discipline: [DISCIPLINE]

If you would like to change your discipline before Day 61, reply here with your choice:
- HVAC
- Piping / Mechanical
- Plumbing / Sanitary
- Fire Protection
- Electrical

Otherwise, your [DISCIPLINE] deep-dive lessons begin automatically on Day 61.
```

### 4.3 90일 완료 업셀 메시지

Day 90 인증서와 함께 발송:

```
LUA BIM LABS Starter — 90 Days Complete

Congratulations on completing the 90-Day MEP BIM Starter Program.

You have built a foundation in:
✓ MEP BIM orientation and workflows
✓ Revit MEP basics and model quality
✓ Clash coordination fundamentals
✓ Data and schedule management
✓ Site-readiness thinking
✓ [DISCIPLINE] discipline deep-dive

Your next step:

Personal Tutor — USD 119/month
- Personalized level diagnosis
- Custom daily lessons
- Monthly written progress report
- Level check and advancement tracking
- Discipline-specific scenario lessons
- Coming Soon

Reply here if you're interested in Personal Tutor, or have questions about your next BIM learning path.

Thank you for learning with LUA BIM LABS.
```

---

## 섹션 5: 클라이언트 이탈 및 환불 처리

### 5.1 취소 요청 처리

클라이언트가 취소 요청 시:
1. 다음 결제일 전 취소로 처리 (즉시 환불 아님)
2. Google Sheet Status = `Cancelled`
3. 마지막 결제 기간 끝까지 레슨 계속 제공
4. PayPal 구독 취소 (해당 시)

### 5.2 환불 정책 (Terms 기준)

| 상황 | 처리 |
|---|---|
| 레슨 수신 전 환불 요청 | 전액 환불 |
| 1~7일 레슨 수신 후 | 무환불 원칙 (단, 기술적 오류 등 LUA BIM LABS 귀책 시 처리) |
| 8일+ 레슨 수신 후 | 환불 불가 (조기 결제 종료 취소만 가능) |

---

## 섹션 6: 운영 도구 및 파일 경로

| 도구/파일 | 경로/URL |
|---|---|
| 신청서 Google Sheet | `https://docs.google.com/spreadsheets/d/1v1t5k76mAhKSBx-x19fEw3Kmi7c6heFKMrkIbK_qcFk/` |
| 클라이언트 JSON | `data/starter_plan/clients.json` |
| 레슨 전달 스크립트 | `scripts/bim_education/send_daily.py` |
| 온보딩 스크립트 | `scripts/starter_plan_onboarding.py` |
| Telegram 동기화 | `scripts/starter_plan_sync_telegram_sheet.py` |
| 레퍼런스 카드 PDF | `docs/training_curriculum/public_products/launch_packages/starter/reference_cards/` |
| 인증서 PDF | `docs/training_curriculum/public_products/launch_packages/starter/certificates/` |
| BIM Check Friday | `docs/training_curriculum/public_products/launch_packages/starter/STARTER_SUPPORT_MATERIALS.md` |
| 배달 오류 로그 | `logs/starter_delivery_errors.log` |

---

## 섹션 7: 서비스 범위 경계 스크립트

서비스 범위 외 요청이 왔을 때 사용하는 표준 응답:

**모델 검토 요청 시:**
```
Thank you for sharing this. Model review is not included in the Starter Plan.

For model QA and coordination feedback, I recommend:
→ Personal Tutor plan (coming soon) — personalized daily lessons with Q&A
→ Project Mentor plan (coming soon) — real project issue review

Starter continues your daily lessons on [tomorrow's topic].
```

**설계/법규 질문 시:**
```
This is a great question, but it goes into engineering design and code compliance territory — which is beyond what I can provide as educational content.

For professional engineering guidance, please consult a licensed engineer on your project team.

Tomorrow's lesson covers [topic], which will help with [related practical skill].
```

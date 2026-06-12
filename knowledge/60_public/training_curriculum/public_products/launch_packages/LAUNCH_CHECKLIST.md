# LUA BIM LABS 상품별 런칭 체크리스트

문서번호: LBL-LAUNCH-000
문서상태: 운영 마스터 체크리스트
작성일: 2026-05-29

---

## 런칭 완료 기준

모든 항목 ✅ 완료 시 해당 상품 런칭 가능 판정.

---

## Tier 1: Starter (USD 39/월) — 현재 런칭 완료

### 결제 및 접수

- [x] PayPal Payment Link 생성 완료 (https://www.paypal.com/ncp/payment/9NQE7BEG2M7PS)
- [x] Google Form 신청서 완성
- [x] Google Sheet 신청 관리 시트 운영 중
- [x] Terms and Disclaimers 문서 완성

### 온보딩 및 전달 인프라

- [x] Telegram Bot 설정 완료
- [x] `starter_plan_onboarding.py` 스크립트 운영 중
- [x] `starter_plan_sync_telegram_sheet.py` 운영 중
- [x] `bim_education/send_daily.py` 운영 중
- [x] Delivery SOP 완성 → `launch_packages/starter/STARTER_DELIVERY_SOP.md`

### 커리큘럼 콘텐츠

- [x] Track 1 (Day 01–07): MEP BIM Orientation ✅ 완성
- [x] Track 2 (Day 08–14): Revit MEP Basics ✅ 완성
- [x] Track 3 (Day 15–21): Drawing and System Reading ✅ 완성
- [x] Track 4 (Day 22–28): Model Quality Basics ✅ 완성
- [x] Track 5 (Day 29–38): Clash Coordination Basics ✅ 완성 (`lessons/TRACK_5_TO_8_COMPLETE.md`)
- [x] Track 6 (Day 39–47): Data and Schedule Basics ✅ 완성
- [x] Track 7 (Day 48–54): Site-Readiness Thinking ✅ 완성
- [x] Track 8 (Day 55–60): BIM Career Habit Building ✅ 완성
- [x] Track 9A (Day 61–90): HVAC Deep-Dive ✅ Day 61-67 완성 (`STARTER_SUPPORT_MATERIALS.md`)
- [x] Track 9B (Day 61–90): Piping Deep-Dive ✅ Day 61-67 완성
- [x] Track 9C (Day 61–90): Plumbing Deep-Dive ✅ Day 61-67 완성
- [x] Track 9D (Day 61–90): Fire Protection Deep-Dive ✅ Day 61-67 완성
- [x] Track 9E (Day 61–90): Electrical Deep-Dive ✅ Day 61-67 완성
- [ ] Track 9A-E Day 68-90: 공종별 나머지 23일 레슨 (차기 작업)

### 지원 자료

- [x] Quick Reference Cards (8장) ✅ 완성 (`STARTER_SUPPORT_MATERIALS.md`)
- [x] 60일 수료 인증서 템플릿 ✅ 완성
- [x] 90일 수료 인증서 템플릿 ✅ 완성
- [x] BIM Check Friday 13주 전체 ✅ 완성 (`lessons/TRACK_5_TO_8_COMPLETE.md`)

### 마케팅

- [ ] Blogger 서비스 소개 포스트 (영문)
- [ ] Telegram CTA 메시지 (채널/SNS용)
- [ ] 가격 페이지 텍스트 확정

---

## Tier 2: Personal Tutor (USD 119/월) — Coming Soon → 런칭 준비 중

### 결제 및 접수

- [ ] PayPal Payment Link 생성 (USD 119/월)
- [ ] 전용 Google Form 신청서 완성 (Starter와 다른 상세 학습 프로파일 필요)
- [ ] Google Sheet 신청 관리 시트 생성
- [x] Personal Tutor Terms 문서 완성 ✅ (`docs/personal_tutor_terms_and_disclaimers.md`)

### 온보딩 및 전달 인프라

- [ ] 레벨 진단 발송 스크립트 또는 수동 프로세스 확정 (차기 작업)
- [ ] 월간 보고서 생성 루틴 (Obsidian → PDF) (차기 작업)
- [ ] 약점 보정 레슨 발송 시스템 (조건부 레슨 발송 로직) (차기 작업)
- [x] Delivery SOP 완성 ✅ (이미 완성됨)
- [x] Delivery SOP 완성 ✅ (`launch_packages/personal_tutor/DELIVERY_SOP.md`)

### 커리큘럼 및 서비스 콘텐츠

- [x] 레벨 진단 테스트 5개 (Level 1-5) ✅ (`assessments/LEVEL_ASSESSMENTS.md` — 50문항)
- [x] 월간 학습 진도 보고서 템플릿 ✅ (`MONTHLY_REPORT_TEMPLATE.md`)
- [x] 공종별 시나리오 레슨 (5공종 × 3개 = 15개) ✅ (`scenario_lessons/DISCIPLINE_SCENARIOS.md`)
- [x] 약점 보정 레슨 라이브러리 (W01-W10) ✅ (`corrective_lessons/CORRECTIVE_LESSONS_W01_W10.md`)
- [x] 신청서 (Intake Form) ✅ (`INTAKE_FORM_SPEC.md`)
- [x] Level 1-5 커리큘럼 경로 완성 ✅ (02_PERSONAL_TUTOR_CURRICULUM.md)
- [ ] W11-W30 약점 보정 레슨 (운영 중 데이터 기반 추가)
- [ ] PayPal 결제 링크 생성 (USD 119/월) — 절차: `docs/external_service_setup_guide.md` 섹션 1

### 마케팅

- [ ] "Personal Tutor vs Starter" 비교 페이지
- [ ] Coming Soon 신청 대기 폼 (Blogger/랜딩페이지)

---

## Tier 3: Coordinator Mentor (USD 229/월) — Coming Soon → 런칭 준비 중

### 결제 및 접수

- [ ] PayPal Payment Link 생성 (USD 229/월)
- [ ] 전용 Google Form 신청서 완성
- [ ] Google Sheet 신청 관리 시트 생성
- [x] Coordinator Mentor Terms 문서 완성 ✅ (`docs/coordinator_mentor_terms_and_disclaimers.md`)

### 온보딩 및 전달 인프라

- [ ] Zoom 세션 예약 시스템 (Calendly 또는 수동) — 절차: `docs/external_service_setup_guide.md` 섹션 4
- [ ] 세션 리마인더 발송 루틴 (차기 작업)
- [x] Delivery SOP 완성 ✅ (`launch_packages/coordinator_mentor/DELIVERY_SOP.md`)

### 커리큘럼 및 서비스 콘텐츠

- [x] 45일 커리큘럼 완성 ✅ (03_COORDINATOR_MENTOR_CURRICULUM.md)
- [x] 신청서 (Intake Form) ✅ (`INTAKE_FORM_SPEC.md`)
- [x] 조율 템플릿 팩 (5개 파일 내용) ✅ (`templates/TEMPLATE_PACK_CONTENT.md`)
- [x] 케이스 스터디 2개 ✅ (`case_studies/CASE_STUDY_01_02.md`)
- [x] 조율 시나리오 챌린지 1개 ✅ (`scenarios/SCENARIO_01.md`)
- [x] 월간 세션 안건 템플릿 ✅ (`SESSION_AGENDA_TEMPLATE.md`)
- [ ] 45일 수료 인증서 PDF 실제 제작 (차기 작업)
- [ ] 케이스 스터디 3번째 (운영 2개월 후 추가)
- [ ] PayPal 결제 링크 생성 (USD 229/월) — 절차: `docs/external_service_setup_guide.md` 섹션 1

### 마케팅

- [ ] "Coordinator Mentor vs Personal Tutor" 포지셔닝 페이지
- [ ] Coming Soon 신청 대기 폼

---

## Tier 4: Project Mentor (USD 490/월) — Coming Soon → 런칭 준비 중

### 결제 및 접수

- [ ] PayPal Payment Link 생성 (USD 490 Standard / USD 790 Intensive)
- [ ] 전용 신청 + 스코프 확인 프로세스 (Project Mentor는 계약 전 스코프 논의 필요)
- [ ] Google Sheet 신청 관리 시트 생성
- [x] Project Mentor Terms 문서 완성 ✅ (`docs/project_mentor_terms_and_disclaimers.md`)

### 온보딩 및 전달 인프라

- [ ] Zoom 세션 예약 시스템 (Calendly 또는 수동) — 절차: `docs/external_service_setup_guide.md` 섹션 4
- [ ] 24시간 우선 응답 Telegram 알림 시스템 (차기 작업)
- [x] Delivery SOP 완성 ✅ (`launch_packages/project_mentor/DELIVERY_SOP.md`)

### 커리큘럼 및 서비스 콘텐츠

- [x] 마일스톤 기반 멘토링 구조 완성 ✅ (04_PROJECT_MENTOR_CURRICULUM.md)
- [x] 신청서 (Intake Form) ✅ (`INTAKE_FORM_SPEC.md`)
- [x] BEP 템플릿 (8개 섹션, ISO 19650 기반) ✅ (`BEP_TEMPLATE.md`)
- [x] QA/QC 체크리스트 (HVAC 35항목 + 전기 33항목) ✅ (`qa_checklists/QA_CHECKLISTS.md`)
- [x] 분기 커리어 성장 Assessment 폼 ✅ (`CAREER_ASSESSMENT_FORM.md`)
- [x] 납품 시뮬레이션 시나리오 1개 ✅ (`delivery_simulations/SIMULATION_01.md`)
- [x] 월간 세션 안건 템플릿 ✅ (`SESSION_AGENDA_TEMPLATE.md`)
- [ ] 배관 QA/QC 체크리스트 (차기 작업)
- [ ] 납품 시뮬레이션 시나리오 2-3번 (운영 중 추가)
- [ ] PayPal 결제 링크 생성 (USD 490 / USD 790) — 절차: `docs/external_service_setup_guide.md` 섹션 1

### 마케팅

- [ ] "Project Mentor는 왜 다른가" 포지셔닝 페이지
- [ ] 문의 기반 신청 흐름 설계

---

## 공통 체크리스트 (전 상품 공통)

### 법무 및 컴플라이언스

- [x] Starter Terms and Disclaimers 완성
- [x] Personal Tutor Terms 완성 ✅ (`docs/personal_tutor_terms_and_disclaimers.md`)
- [x] Coordinator Mentor Terms 완성 ✅ (`docs/coordinator_mentor_terms_and_disclaimers.md`)
- [x] Project Mentor Terms 완성 ✅ (`docs/project_mentor_terms_and_disclaimers.md`)
- [ ] 개인정보 처리 방침 (Privacy Notice) 초안
- [ ] 환불 정책 공개 문구 확정

### 마케팅 채널

- [ ] Blogger 상품별 소개 포스트 작성
- [ ] Telegram 채널 상품 공지 메시지 작성
- [ ] SNS (LinkedIn 등) 소개 콘텐츠 작성
- [ ] 이메일 시퀀스 (결제 완료 → 온보딩 → 30/60/90일 체크인)

### 운영 모니터링

- [ ] 구독자 수 추적 (Google Sheet)
- [ ] 레슨 전달 성공률 로깅
- [ ] 이탈률 (churn rate) 월간 추적
- [ ] NPS/만족도 설문 (90일 완료 후 발송)

---

## 런칭 순서 권고

| 순서 | 상품 | 조건 | 목표 시기 |
|---|---|---|---|
| 1 | Starter | 이미 런칭 — 콘텐츠 완성 우선 | 2026년 6월 중 Track 5-9 완성 |
| 2 | Personal Tutor | Starter 구독자 10명 확보 후 | 2026년 8월 |
| 3 | Coordinator Mentor | Personal Tutor 구독자 5명 확보 후 | 2026년 10월 |
| 4 | Project Mentor | Coordinator Mentor 검증 후 | 2027년 Q1 |

---

## 남은 실행 작업 (수동 처리 필요)

### 즉시 처리 (Starter 품질 완성)

1. [ ] Reference Card PDF 실제 제작 (Canva 또는 Google Slides → PDF 8장) — 완료 후 `data/starter_plan/reference_cards/` 에 배치
2. [ ] Certificate PDF 실제 제작 (60일/90일 템플릿 기반, 클라이언트별 이름 변수화)
3. [x] `bim_education/send_daily.py` 90일 커리큘럼 기반으로 업데이트 완료 ✅
   - [x] Track 9 공종 배정 로직 (Day 61+ discipline별 분기) ✅
   - [x] BIM Check Friday 자동 발송 로직 (매주 금요일 자동 감지) ✅
   - [x] BIM Check Friday 퀴즈 파일 13주분 생성 ✅ (`data/starter_plan/friday_quiz/week_01~13.txt`)
   - [x] 마일스톤 메시지 자동 발송 (Day 30/60/90) ✅
   - [x] 레퍼런스 카드 파일 전송 자동화 (PDF 파일 배치 후 자동 발송) ✅
   - [ ] Track 5-8 레슨 파일 (`day_031.txt` ~ `day_060.txt`) 생성 — `TRACK_5_TO_8_COMPLETE.md` 기반 수동 변환 필요
   - [ ] Track 9 레슨 파일 (`data/starter_plan/messages/{discipline}/day_061~090.txt`) 생성 — `STARTER_SUPPORT_MATERIALS.md` 기반 수동 변환 필요

### 런칭 준비 (Personal Tutor)

4. [ ] PayPal 결제 링크 생성 (USD 119/월 구독) — `docs/external_service_setup_guide.md` 섹션 1
5. [ ] Google Form 생성 (Personal Tutor 신청서, `INTAKE_FORM_SPEC.md` + `external_service_setup_guide.md` 섹션 2 기준)
6. [ ] Google Sheet 신청 관리 탭 추가 — `external_service_setup_guide.md` 섹션 3 기준
7. [x] Personal Tutor Terms 문서 작성 완료 ✅ (`docs/personal_tutor_terms_and_disclaimers.md`)
8. [ ] "Coming Soon" → "Available Now" 으로 Blogger 포스트 업데이트

### 런칭 준비 (Coordinator Mentor)

9. [ ] PayPal 결제 링크 생성 (USD 229/월 구독) — `external_service_setup_guide.md` 섹션 1
10. [ ] Google Form 생성 (Coordinator Mentor 신청서) — `external_service_setup_guide.md` 섹션 2
11. [ ] Zoom 예약 링크 설정 (Calendly 무료 플랜으로 시작 가능) — `external_service_setup_guide.md` 섹션 4
12. [ ] 템플릿 팩 5개를 실제 Excel/Word 파일로 변환 후 클라이언트 전달용 패키지 생성
13. [x] Coordinator Mentor Terms 작성 완료 ✅ (`docs/coordinator_mentor_terms_and_disclaimers.md`)

### 런칭 준비 (Project Mentor)

14. [ ] PayPal 결제 링크 2개 생성 (Standard USD 490 / Intensive USD 790) — `external_service_setup_guide.md` 섹션 1
15. [ ] Google Form 생성 (Project Mentor 신청서, 스코프 확인 포함) — `external_service_setup_guide.md` 섹션 2
16. [ ] BEP Template → Word 파일 변환 (`.docx`, 클라이언트 전달용)
17. [ ] QA/QC Checklists → Excel 변환 (`.xlsx`, 체크박스 포함)
18. [ ] Career Assessment → Google Forms 변환 (분기별 자동 발송)
19. [x] Project Mentor Terms 작성 완료 ✅ (`docs/project_mentor_terms_and_disclaimers.md`)

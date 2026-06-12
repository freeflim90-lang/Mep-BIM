# Personal Tutor — Intake Form Specification

**Service:** LUA BIM LABS Personal Tutor  
**Form Platform:** Google Forms (link sent after PayPal payment confirmation)  
**Form Title:** "LUA BIM LABS Personal Tutor — 학습 프로필 등록 양식"  
**Version:** 1.0  
**Document Owner:** COO

---

## Purpose

This intake form is completed by every new Personal Tutor subscriber before their first lesson is delivered. It collects the information needed to: (1) verify payment, (2) establish communication, (3) diagnose the client's correct learning level, and (4) create a personalized curriculum. This form is more detailed than the Starter plan intake form because the Personal Tutor service is fully customized to each client.

The completed form response is saved to the client's Google Drive folder and referenced throughout their subscription.

---

## Section 1: Basic Information

**Section Title (displayed in form):** "기본 정보"

| Field # | Field Label | Type | Required | Validation |
|---------|-------------|------|----------|------------|
| 1.1 | 성함 (Full Name) | Short text | Yes | Min 2 characters |
| 1.2 | 이메일 주소 (Email Address) | Email | Yes | Valid email format |
| 1.3 | 국가 및 거주 도시 (Country and City) | Short text | Yes | — |
| 1.4 | 시간대 (Time Zone) | Dropdown | Yes | See dropdown list below |
| 1.5 | 연락 가능한 시간대 (Preferred contact hours) | Checkboxes | Yes | See options below |

**Dropdown 1.4 — Time Zone options:**
- UTC+9 (Seoul, Tokyo)
- UTC+8 (Beijing, Singapore, Hong Kong)
- UTC+7 (Bangkok, Jakarta)
- UTC+5:30 (Mumbai)
- UTC+3 (Riyadh, Dubai)
- UTC+1 (London BST)
- UTC+0 (London GMT)
- UTC-5 (New York EST)
- UTC-8 (Los Angeles PST)
- Other (please specify in Notes field)

**Checkboxes 1.5 — Preferred contact hours (select all that apply):**
- 오전 6시–9시 (Early morning)
- 오전 9시–12시 (Morning)
- 오후 12시–3시 (Early afternoon)
- 오후 3시–6시 (Afternoon)
- 오후 6시–9시 (Evening)
- 오후 9시–자정 (Late evening)

---

## Section 2: Payment Confirmation

**Section Title (displayed in form):** "결제 확인"

**Section Description (displayed):**
> Personal Tutor 서비스는 USD 119/월 PayPal 결제 확인 후 시작됩니다. 아래에 결제 정보를 입력해 주세요.

| Field # | Field Label | Type | Required | Validation / Notes |
|---------|-------------|------|----------|--------------------|
| 2.1 | PayPal 결제 이메일 주소 (PayPal payment email) | Email | Yes | Must match PayPal transaction sender |
| 2.2 | PayPal 거래 ID (Transaction ID) | Short text | Yes | Format hint: begins with letters + 17 digits |
| 2.3 | 결제 완료일 (Payment date) | Date | Yes | Cannot be future date |
| 2.4 | 결제 금액 확인 (Amount paid) | Multiple choice | Yes | Options: "USD 119", "다른 금액 (아래 메모에 기입)" |
| 2.5 | 메모 (Notes on payment, if any) | Long text | No | — |

**Internal note for LUA BIM LABS staff:** Cross-check 2.1 and 2.2 against PayPal dashboard before proceeding with onboarding. Do not proceed if transaction cannot be verified.

---

## Section 3: Telegram Setup

**Section Title (displayed in form):** "텔레그램 연결"

**Section Description (displayed):**
> Personal Tutor 레슨과 Q&A는 모두 텔레그램 1:1 채팅으로 진행됩니다. 아래 정보를 입력해 주세요.

| Field # | Field Label | Type | Required | Validation / Notes |
|---------|-------------|------|----------|--------------------|
| 3.1 | 텔레그램 사용자 이름 (Telegram username — @로 시작) | Short text | Yes | Must start with @; no spaces |
| 3.2 | 텔레그램 표시 이름 (Display name in Telegram) | Short text | Yes | — |
| 3.3 | 텔레그램 수신 가능 여부 확인 | Multiple choice | Yes | "네, 텔레그램이 설치되어 있고 알림을 받을 수 있습니다" / "아직 텔레그램이 없습니다 (설치 후 다시 제출해 주세요)" |

**Internal note:** If client selects "아직 텔레그램이 없습니다", send an email reply with setup instructions and ask them to resubmit the form after installation.

---

## Section 4: Detailed Learning Profile

**Section Title (displayed in form):** "학습 프로필"

**Section Description (displayed):**
> 이 섹션은 맞춤형 커리큘럼을 설계하기 위한 핵심 정보입니다. 최대한 자세하게 작성해 주실수록 첫 레슨부터 정확하게 맞춤화됩니다.

### 4A: Current Level Self-Assessment

| Field # | Field Label | Type | Required | Options / Notes |
|---------|-------------|------|----------|-----------------|
| 4.1 | 현재 BIM 수준 자기 평가 (Self-assessed current level) | Multiple choice | Yes | See level descriptions below |
| 4.2 | 수준 선택 이유 (Reason for selecting this level) | Long text | Yes | Min 50 characters |

**Multiple choice options for 4.1:**
- **Level 1 — 입문자 (Beginner):** BIM이 생소하거나 Revit을 거의 사용해본 적 없음
- **Level 2 — 모델러 (Modeler):** Revit으로 기본 MEP 요소를 배치할 수 있으나 시스템 연결이나 표준이 불확실함
- **Level 3 — 코디네이터 (Coordinator):** 클래시 감지와 기본 코디네이션 워크플로를 수행할 수 있음
- **Level 4 — 리드 (Lead):** BEP 작성, QA/QC, 팀 납품 관리 경험 있음
- **Level 5 — 자동화 (Automation):** Dynamo 또는 Revit API 기반 자동화에 입문하거나 심화하려 함
- **잘 모르겠음 (Unsure):** 진단 테스트 결과에 전적으로 맡기겠음

### 4B: Discipline

| Field # | Field Label | Type | Required | Options |
|---------|-------------|------|----------|---------|
| 4.3 | 주요 MEP 분야 (Primary MEP discipline) | Multiple choice | Yes | 기계-HVAC / 기계-배관 (Piping) / 위생-배관 (Plumbing) / 소방 (Fire Protection) / 전기 (Electrical) / 복합 (Multiple disciplines) |
| 4.4 | 복합 분야인 경우, 어떤 분야들인지 기입 (If multiple, list disciplines) | Short text | No | Required if 4.3 = 복합 |

### 4C: Professional Experience

| Field # | Field Label | Type | Required | Options / Notes |
|---------|-------------|------|----------|-----------------|
| 4.5 | BIM 관련 업무 경력 (BIM work experience) | Multiple choice | Yes | 없음 / 1년 미만 / 1–3년 / 3–5년 / 5년 이상 |
| 4.6 | 현재 직책 또는 역할 (Current role or title) | Short text | Yes | — |
| 4.7 | 주로 사용하는 BIM 소프트웨어 (Software currently used) | Checkboxes | Yes | Revit / Navisworks / AutoCAD MEP / Dynamo / BIM 360 / ACC / MagiCAD / Trimble / 기타 |
| 4.8 | 기타 소프트웨어 명시 (Other software — specify) | Short text | No | — |
| 4.9 | 최근 수행한 가장 큰 프로젝트 규모 (Largest project size recently) | Multiple choice | No | 소규모 건물 (5층 이하) / 중규모 건물 (6–20층) / 대규모 건물 (21층 이상) / 산업 플랜트 / 인프라 / 경험 없음 |

### 4D: Learning Goals

| Field # | Field Label | Type | Required | Notes |
|---------|-------------|------|----------|-------|
| 4.10 | 학습 목표 (Learning goal — why are you joining Personal Tutor?) | Long text | Yes | Min 80 characters; prompt: "Personal Tutor를 통해 달성하고 싶은 구체적인 목표를 적어 주세요." |
| 4.11 | 목표 달성 기한 (Target timeline for achieving your goal) | Multiple choice | Yes | 3개월 이내 / 6개월 이내 / 1년 이내 / 기한 없이 꾸준히 |
| 4.12 | 이 목표가 중요한 이유 (Why this goal matters to you) | Long text | Yes | Min 50 characters |

### 4E: Known Weak Points

| Field # | Field Label | Type | Required | Notes |
|---------|-------------|------|----------|-------|
| 4.13 | 스스로 느끼는 약점 분야 (Self-identified weak areas) | Checkboxes | Yes | See checklist below |
| 4.14 | 약점에 대한 추가 설명 (Additional detail about weak areas) | Long text | No | — |

**Checkboxes for 4.13 (select all that apply):**
- Revit 인터페이스와 기본 조작
- MEP 패밀리 배치 및 편집
- MEP 시스템 연결 (커넥터 연결, 시스템 할당)
- 표준 명명 규칙 (Naming conventions)
- LOD 이해 및 적용
- 클래시 감지 및 해결 워크플로
- Navisworks 사용
- BEP (BIM Execution Plan) 작성
- QA/QC 체크 수행
- Dynamo 기초
- Revit API 기초
- 도면 생성 및 어노테이션
- 모델 링크 및 워크셋 관리
- 없음 / 잘 모르겠음

### 4F: Available Study Time

| Field # | Field Label | Type | Required | Options |
|---------|-------------|------|----------|---------|
| 4.15 | 하루 학습 가능 시간 (Daily available study time) | Multiple choice | Yes | 15분 이하 / 15–30분 / 30분–1시간 / 1–2시간 / 2시간 이상 |
| 4.16 | 주당 학습 가능 일수 (Days per week available to study) | Multiple choice | Yes | 주 2일 / 주 3–4일 / 주 5일 / 주 7일 |
| 4.17 | 현재 Revit 실무 접근 환경 (Access to Revit for practice) | Multiple choice | Yes | 회사 라이선스로 사용 가능 / 개인 라이선스 보유 / 학생 버전 사용 / 현재 접근 불가 |

---

## Section 5: Service Understanding and Scope Agreement

**Section Title (displayed in form):** "서비스 이해 및 범위 동의"

**Section Description (displayed):**
> Personal Tutor 서비스를 올바르게 이용하시려면 아래 내용을 모두 읽고 각 항목에 동의해 주세요. 동의하지 않는 항목이 있으면 서비스 시작이 불가합니다.

### 5A: What Personal Tutor Includes (확인 체크박스)

Each item below is a separate required checkbox. Label: "위 내용을 이해하고 동의합니다"

| # | Statement |
|---|-----------|
| 5.1 | 레슨은 텔레그램 1:1 채팅으로 매일 전송됩니다. 화상통화나 화면 공유는 포함되지 않습니다. |
| 5.2 | Q&A는 주 3회까지 가능하며, 답변은 다음 영업일 오후 6시까지 제공됩니다. |
| 5.3 | 매주 금요일 BIM Check 챌린지가 정규 레슨 대신 발송됩니다. |
| 5.4 | 10일마다 제 MEP 분야 (4.3에서 선택한 분야) 기반의 시나리오 레슨이 추가 제공됩니다. |
| 5.5 | 매월 수준 진단(5문항)과 2페이지 서면 진도 보고서가 제공됩니다. |
| 5.6 | 반복되는 약점이 감지되면 보정 레슨(W01–W30)이 추가로 발송됩니다. |
| 5.7 | 구독료는 월 USD 119이며 환불 정책은 LUA BIM LABS 이용약관을 따릅니다. |

### 5B: What Personal Tutor Does NOT Include (확인 체크박스)

| # | Statement |
|---|-----------|
| 5.8 | 실제 프로젝트 납품물(도면, BEP, 클래시 리포트 등) 검토 및 서명 서비스는 포함되지 않습니다. |
| 5.9 | Dynamo 스크립트나 Revit 애드인을 제 프로젝트용으로 제작해 주는 서비스는 포함되지 않습니다. |
| 5.10 | MEP 엔지니어링 설계 계산(부하 계산, 덕트/배관 사이징 등)은 서비스 범위에 포함되지 않습니다. |
| 5.11 | Revit 소프트웨어 라이선스, 설치, 기술 지원은 포함되지 않습니다. |
| 5.12 | 주 3회 한도를 초과하는 Q&A는 해당 주에 처리되지 않습니다. |

---

## Section 6: Consent for Learning Records

**Section Title (displayed in form):** "학습 기록 동의"

| Field # | Statement | Type | Required |
|---------|-----------|------|----------|
| 6.1 | LUA BIM LABS는 서비스 제공 목적으로 제 학습 데이터(레슨 기록, Q&A 내용, 수준 진단 결과)를 저장하고 분석하는 것에 동의합니다. | Checkbox | Yes |
| 6.2 | 저의 개인 식별 정보(이름, 이메일, 텔레그램)가 포함되지 않는 익명화된 학습 패턴 데이터는 LUA BIM LABS 교육과정 개선에 활용될 수 있음에 동의합니다. | Checkbox | Yes |
| 6.3 | 학습 기록은 구독 종료 후 12개월간 보관된 후 삭제됩니다. | Checkbox (acknowledgment) | Yes |

---

## Section 7: Open Notes

**Section Title (displayed in form):** "추가 메모"

| Field # | Field Label | Type | Required |
|---------|-------------|------|----------|
| 7.1 | LUA BIM LABS에 전달하고 싶은 추가 사항이 있으면 자유롭게 작성해 주세요. | Long text | No |

---

## Form Submission Confirmation Message

Displayed after the client submits the form:

> 제출해 주셔서 감사합니다! 결제 확인 후 영업일 기준 1–2일 이내에 텔레그램으로 연락드리겠습니다. 그 전에 수준 진단 테스트가 텔레그램으로 발송될 예정입니다. 잠시만 기다려 주세요!

---

## Internal Processing Checklist (for LUA BIM LABS staff)

After form is submitted:
- [ ] Verify PayPal transaction (Section 2)
- [ ] Confirm Telegram username is valid (test send a message)
- [ ] Review level self-assessment and weak areas (Section 4)
- [ ] Proceed with DELIVERY_SOP.md Step 3 — Level Assessment Administration

---

*End of Personal Tutor Intake Form Specification v1.0*

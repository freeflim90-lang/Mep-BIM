# Personal Tutor — Delivery SOP (Service Operations Manual)

**Service:** LUA BIM LABS Personal Tutor  
**Price:** USD 119/month  
**Delivery Channel:** Telegram (1:1 private chat)  
**Document Owner:** COO  
**Version:** 1.0  
**Effective Date:** 2026-06-01

---

## 1. Purpose and Scope

This SOP governs every operational step required to deliver the Personal Tutor service from first client contact through offboarding. Any staff member assigned to a Personal Tutor client must follow this document exactly. Deviations require written approval from the COO.

---

## 2. Client Onboarding Checklist (Day 0)

### Step 1: Payment Verification
- [ ] Confirm PayPal payment of USD 119 received in LUA BIM LABS PayPal account
- [ ] Record client name, PayPal transaction ID, and payment date in the Client Register (Google Sheet: `PT_CLIENT_REGISTER`)
- [ ] Set subscription renewal reminder 25 days from payment date

### Step 2: Intake Form Receipt and Review
- [ ] Client submits INTAKE_FORM_SPEC Google Form link
- [ ] Download form responses and save to: `Google Drive / PT Clients / [Client_Telegram_Handle] / Intake/`
- [ ] Review form for completeness — if any required field is missing, send Telegram message requesting completion within 24 hours
- [ ] Flag any scope confusion (e.g., client expects live video calls) and clarify before proceeding

### Step 3: Level Assessment Administration
- [ ] Based on client's self-reported level, send the corresponding Level Assessment from `LEVEL_ASSESSMENTS.md`
- [ ] Send via Telegram with the message: *"안녕하세요! 시작하기 전에 먼저 수준 진단 테스트를 진행합니다. 아래 10문항에 답해 주세요. 시간 제한은 없습니다."*
- [ ] Set a 48-hour deadline for the client to complete the assessment
- [ ] If no response after 48 hours, send one reminder. If no response after 72 hours, escalate to COO.

### Step 4: Level Assessment Scoring
- [ ] Score the assessment using the answer key in `LEVEL_ASSESSMENTS.md`
- [ ] Scoring rubric:
  - 9–10 correct → Confirmed at stated level, start current level curriculum
  - 7–8 correct → Confirmed at stated level, flag 2 weak areas in client profile
  - 5–6 correct → Place one level below stated level, inform client with explanation
  - 4 or below → Place two levels below stated level, inform client with explanation
- [ ] Record diagnosed level in `PT_CLIENT_REGISTER`
- [ ] Log any weak areas identified into client's `WEAKNESS_LOG.md`

### Step 5: Client Profile Setup
- [ ] Create client folder: `Google Drive / PT Clients / [Client_Telegram_Handle] /`
- [ ] Create the following files inside the folder:
  - `CLIENT_PROFILE.md` (copy template, fill all fields from intake form and assessment)
  - `LESSON_LOG.md` (empty log, columns: Date, Lesson_ID, Topic, Delivered, Client_Response)
  - `WEAKNESS_LOG.md` (empty log, columns: Date, Pattern_Code, Description, Corrective_Lesson_Sent, Resolved_Date)
  - `QA_LOG.md` (empty log, columns: Date, Question, Answer_Sent, Within_Deadline)
  - `PROGRESS_REPORTS/` folder (empty)

### Step 6: Curriculum Planning
- [ ] Open `CLIENT_PROFILE.md` and confirm: diagnosed level, discipline, weak areas, daily available time
- [ ] Select the appropriate Level curriculum track from the master curriculum
- [ ] Mark the discipline-specific scenario lesson schedule (every 10 days from Day 1)
- [ ] Pre-select corrective lessons from `CORRECTIVE_LESSONS_W01_W10.md` for any pre-identified weak patterns
- [ ] Record the planned Day 1 lesson topic in `LESSON_LOG.md`

### Step 7: Welcome Message
- [ ] Send the following welcome message via Telegram within 4 hours of completing profile setup:

```
안녕하세요, [이름]님! LUA BIM LABS Personal Tutor에 오신 것을 환영합니다.

진단 결과, [이름]님의 현재 수준은 Level [N] ([Level Name])으로 확인되었습니다.
[선택된 이유 1-2문장]

앞으로의 학습 계획:
- 매일 맞춤형 MEP BIM 레슨을 이 채널로 보내드립니다
- 주 3회까지 Q&A 가능하며, 다음 날 오후 6시까지 답변드립니다
- 10일마다 [Discipline] 현장 시나리오 레슨이 포함됩니다
- 매월 레벨 체크 및 2페이지 서면 진도 보고서를 제공합니다

첫 번째 레슨은 내일 오전 9시에 발송됩니다. 궁금한 점이 있으면 언제든지 질문해 주세요!
```

### Step 8: First Lesson Preparation
- [ ] Prepare Day 1 lesson content the evening before (must be ready by 8:00 AM next day)
- [ ] Format lesson using the standard daily lesson template (see Section 3.2)
- [ ] Schedule Telegram message send for 9:00 AM client's local time zone
- [ ] Mark `LESSON_LOG.md` row as `Scheduled`

### Onboarding Completion Criteria
All 8 steps must be completed before the first lesson is sent. Typical onboarding window: 2–3 business days from payment.

---

## 3. Daily Operations

### 3.1 Daily Schedule (Per Client)

| Time | Action |
|------|--------|
| 08:00 AM | Check Telegram for overnight client messages |
| 08:15 AM | Log any incoming Q&A in `QA_LOG.md` |
| 08:30 AM | Finalize and send today's lesson |
| 12:00 PM | Mid-day Telegram check for responses or follow-up questions |
| 05:00 PM | Final Telegram check; send any pending Q&A answers due today |
| 05:30 PM | Prepare tomorrow's lesson based on today's client response |
| 05:45 PM | Update `LESSON_LOG.md` with today's delivery status |

### 3.2 Daily Lesson Format

Every lesson must follow this exact format when sent via Telegram:

```
📘 [Level N] Day [DD] — [Lesson Title]

🎯 오늘의 목표:
[1-2 sentences: what the learner will understand after this lesson]

📖 핵심 개념:
[Main concept explanation — 3-5 paragraphs, plain language, no jargon without definition]

🔧 실전 적용:
[Specific steps in Revit or Navisworks that the learner should try today]

✅ 오늘의 체크:
- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]

❓ 생각해보기:
[One reflection question to confirm understanding — the learner should reply with their answer]

---
Q&A 가능 횟수 이번 주: [N]/3회 사용됨
다음 레슨: 내일 오전 9시
```

### 3.3 Monitoring Client Responses

- Read every client response within the day it is received
- If the client answers the "생각해보기" question correctly, send a brief confirmation: *"정확합니다! [1-sentence reinforcement]"*
- If the answer is partially correct, send: *"좋은 접근입니다. 한 가지 보충하면 — [correction]"*
- If the answer is wrong, send a corrective follow-up (not a full lesson — 2-3 sentences maximum)
- Log response quality in `LESSON_LOG.md` under `Client_Response` column: `Correct / Partial / No Response / Incorrect`

### 3.4 Tracking No-Response Days

- If the client does not respond to a lesson for 3 consecutive days, send a check-in message:
  *"[이름]님, 잘 지내고 계신가요? 진도를 계속 이어가고 싶을 때 알려 주세요. 레슨은 계속 준비되어 있습니다."*
- If no response for 7 consecutive days, notify COO for possible subscription flag
- Continue delivering lessons regardless of client response status (the service obligation continues)

### 3.5 Adaptive Lesson Adjustment

- After every 5 lessons, review `LESSON_LOG.md` response quality
- If 3 or more `Incorrect` or `No Response` entries → reduce lesson complexity by one step next 5 days
- If 5 consecutive `Correct` entries → advance lesson pace, consider level-up evaluation trigger

---

## 4. Weekly Operations

### 4.1 Monday: Week Planning

- [ ] Review the past week's `LESSON_LOG.md` entries
- [ ] Confirm Q&A count for the new week resets to 0 (Q&A limit is 3/week)
- [ ] Send a brief Monday message to each client:
  *"새로운 한 주 시작합니다! 이번 주 레슨 주제: [Topic 1], [Topic 2], [Topic 3]. 질문 3회 사용 가능합니다."*

### 4.2 Q&A Tracking and Response (Any Day)

**Q&A Eligibility Rules:**
- Maximum 3 Q&A questions per calendar week (Monday–Sunday)
- Q&A must be directly related to MEP BIM learning (see Section 8 for scope boundary)
- Each question = one Q&A credit, regardless of question length

**Q&A Process:**
1. Client sends a question via Telegram
2. Log in `QA_LOG.md`: Date, Question summary, Q&A count this week
3. If client has used fewer than 3 Q&A this week → accept and respond by 6:00 PM the next business day
4. If client has used 3 Q&A this week → send: *"이번 주 Q&A 3회를 모두 사용하셨습니다. 다음 월요일부터 다시 3회 이용 가능합니다. 질문은 메모해 두시면 그때 바로 답변드리겠습니다!"*
5. Record answer delivery in `QA_LOG.md` under `Within_Deadline` column (Yes/No)

**Q&A Answer Format:**
```
❓ 질문: [Restate the question]

💡 답변:
[Detailed answer — use numbered steps if procedural, use examples where helpful]

📌 관련 레슨: Day [N] — [Lesson Title] 참고
추가 궁금한 점이 있으면 질문해 주세요.
```

### 4.3 Friday: BIM Check

Every Friday, send a BIM Check challenge instead of a regular lesson:

```
🔍 BIM Check Friday — Week [N]

이번 주 배운 내용을 실제 모델에서 확인해봅시다.

📋 이번 주 체크리스트:
- [ ] [Check item 1 — tied to this week's lessons]
- [ ] [Check item 2]
- [ ] [Check item 3]
- [ ] [Check item 4]
- [ ] [Check item 5]

📸 선택 과제: 체크 완료 후 Revit 화면 스크린샷을 보내주시면 피드백 드립니다.

다음 주 첫 레슨: 월요일 오전 9시
```

### 4.4 Weekly Weakness Pattern Review (Every Sunday)

- [ ] Review all 7 days of `LESSON_LOG.md` and `QA_LOG.md`
- [ ] Identify any recurring error patterns (e.g., client consistently wrong about slope, naming, connections)
- [ ] If a pattern appears 2+ times in one week → log in `WEAKNESS_LOG.md` with the pattern code
- [ ] Select the matching corrective lesson from `CORRECTIVE_LESSONS_W01_W10.md`
- [ ] Schedule the corrective lesson as an insert into the following week's lesson plan (send in addition to regular daily lesson — send it as a separate message labeled "보충 레슨")

---

## 5. Monthly Operations

### 5.1 Monthly Level Check (Day 28–30 of each month)

**Process:**
1. On Day 28 of the subscription month, send the level assessment for the client's current level
2. Use the same `LEVEL_ASSESSMENTS.md` test used at intake (questions may be reordered; do not change)
3. Scoring:
   - 9–10 correct → Level-up evaluation triggered (see Section 6)
   - 7–8 correct → Continuing at current level, note improvement
   - 5–6 correct → Continuing, increase corrective lesson frequency next month
   - 4 or below → Flag for COO review; offer optional escalation call with Coordinator Mentor
4. Record score in `PT_CLIENT_REGISTER` under `Monthly_Check_[Month]` column
5. Inform client of result within 24 hours of receiving their answers

### 5.2 Monthly Progress Report Generation (Day 29–30)

**Source data required before drafting:**
- [ ] `LESSON_LOG.md` — lesson count, response quality data
- [ ] `QA_LOG.md` — Q&A count and topics
- [ ] `WEAKNESS_LOG.md` — identified patterns and resolved items
- [ ] Monthly level check score

**Drafting process:**
1. Open `MONTHLY_REPORT_TEMPLATE.md`
2. Fill all [FIELD_NAME] placeholders with real client data
3. Export/format as 2-page PDF (use Google Docs → Export as PDF)
4. Name file: `PT_[Client_Handle]_Report_[YYYY-MM].pdf`
5. Save to: `Google Drive / PT Clients / [Client_Telegram_Handle] / PROGRESS_REPORTS/`
6. Send PDF to client via Telegram with the message:
   *"[이름]님, [Month] 진도 보고서를 보내드립니다. 궁금한 점이 있으면 언제든지 알려 주세요!"*

**Deadline:** Report must be delivered by the last calendar day of the subscription month.

### 5.3 Monthly Curriculum Adjustment

After reviewing the monthly level check and progress report:
- [ ] Update `CLIENT_PROFILE.md` with current level, top 3 weak areas, and next month's focus topics
- [ ] Revise the next month's lesson plan in `LESSON_LOG.md` (add planned topics for Days 1–30)
- [ ] If corrective lessons were sent this month, remove resolved weak areas from `WEAKNESS_LOG.md` (mark Resolved_Date)
- [ ] Confirm discipline scenario schedule continues on 10-day cycle

### 5.4 Subscription Renewal

- On Day 25 of each month, send renewal reminder:
  *"안녕하세요 [이름]님! 이번 달 구독이 [Date]에 갱신됩니다. PayPal 자동결제가 설정되어 있으시면 별도 조치가 필요 없습니다. 변경 사항이 있으시면 알려 주세요."*
- On renewal date, confirm payment received in PayPal and update `PT_CLIENT_REGISTER`
- If payment not received within 3 days of renewal date, pause lesson delivery and send payment reminder
- If payment not received within 7 days, initiate offboarding process (see Section 9)

---

## 6. Level-Up Criteria and Process

### 6.1 Level-Up Trigger Conditions

All three conditions must be met before offering a level upgrade:

| Condition | Requirement |
|-----------|-------------|
| Monthly Level Check Score | 9 or 10 correct out of 10 |
| Consecutive Lesson Response Quality | `Correct` for 10 of last 14 lessons |
| Weak Areas Resolved | All logged weak patterns in `WEAKNESS_LOG.md` marked Resolved |

### 6.2 Level-Up Notification

Send the following message when all conditions are met:

```
🎉 축하드립니다, [이름]님!

이번 달 레벨 체크와 전반적인 학습 진도를 검토한 결과, Level [N+1] ([Level Name])으로 승급하실 준비가 되셨다고 판단됩니다.

다음 달부터 Level [N+1] 커리큘럼을 시작하겠습니다. 더 심화된 내용으로 함께 성장해 봅시다!
```

### 6.3 Level-Up Administrative Steps

- [ ] Update `CLIENT_PROFILE.md`: Current_Level → Level [N+1]
- [ ] Record level-up date in `PT_CLIENT_REGISTER`
- [ ] Switch to Level [N+1] curriculum starting next month's Day 1
- [ ] Send Level [N+1] assessment on first day of new level (intake re-check)
- [ ] Update BIM Check Friday questions to Level [N+1] content
- [ ] Update discipline scenario lessons to Level [N+1] scenarios

### 6.4 Skip-Level Policy

No client may advance more than one level per month. If a client scores 10/10 on the Level [N] check, they advance to Level [N+1] only, not Level [N+2].

---

## 7. Escalation to Coordinator Mentor

### 7.1 Escalation Triggers

Escalate to the Coordinator Mentor (Project Mentor or Coordinator Mentor plan holder, or senior staff) when:

- Client asks a question that exceeds Level 5 (Automation) scope
- Client reports a real production BIM coordination crisis (not a learning question)
- Client's monthly check score is 4 or below for two consecutive months
- Client expresses serious dissatisfaction and requests a senior review
- Any technical question about live project deliverables (clash report sign-off, BEP approval, etc.)

### 7.2 Escalation Process

1. Inform the client: *"이 질문은 제가 추가로 확인하여 더 정확한 답변을 드리겠습니다. 내일까지 답변 드리겠습니다."* (This preserves the next-day SLA)
2. Forward the client's question and relevant profile data to Coordinator Mentor staff via internal Slack: `#pt-escalation`
3. Coordinator Mentor must respond within 4 hours during business hours
4. Compile the escalated answer and deliver to client within the next-day deadline
5. Log escalation in `QA_LOG.md` under a separate `Escalated` column (Yes/No)

---

## 8. Response Time Standards

### 8.1 Next-Day Q&A Guarantee

- All Q&A questions received before 5:00 PM local time must be answered by 6:00 PM the following business day
- Questions received after 5:00 PM are treated as received the next morning (response due within 2 business days)
- Weekend questions: answered by 6:00 PM Monday

### 8.2 Unable to Respond on Time

If a deadline cannot be met for any reason (illness, technical issue, etc.):

1. Send a message to the client within the deadline window: *"답변 준비에 조금 더 시간이 필요합니다. [Tomorrow's date] 오전까지 보내드리겠습니다. 불편을 드려 죄송합니다."*
2. Log the delay in `QA_LOG.md` under `Within_Deadline` = `No (Delay notified)`
3. Report the delay to COO via Slack `#pt-ops` within the same business day
4. The extended deadline becomes a firm commitment — no further delays permitted for that question

### 8.3 Response Time Standards Table

| Message Type | Response SLA |
|--------------|-------------|
| Q&A Question (within 3/week) | Next business day by 6:00 PM |
| General Telegram message (not Q&A) | Same day by 6:00 PM |
| Lesson delivery | 9:00 AM daily |
| Monthly report delivery | Last day of subscription month |
| Level-up notification | Within 24 hours of level check scoring |
| Onboarding welcome message | Within 4 hours of profile setup completion |

---

## 9. Scope Boundary Enforcement

### 9.1 What Is In Scope

- MEP BIM concept explanations (Revit, Navisworks, Dynamo, coordination)
- Procedural questions about modeling tasks in Revit
- Questions about BIM standards (LOD, BEP, naming conventions)
- Clarifications of lesson content
- Review of a screenshot or exported view the client shares for learning purposes

### 9.2 What Is Out of Scope

- Live project production support (reviewing client's actual deliverables for approval)
- Custom Dynamo script writing for client's project
- Revit troubleshooting for non-learning purposes (e.g., "my file is corrupt")
- MEP engineering design decisions (sizing, calculations, code compliance)
- Revit license or IT support issues
- Video calls or screen sharing
- Lessons about software other than Revit, Navisworks, Dynamo (unless directly related to BIM coordination)

### 9.3 Redirect Script

When a client sends an out-of-scope request, respond with:

*"감사합니다 [이름]님. 이 내용은 Personal Tutor 서비스 범위에 포함되지 않아 직접 지원이 어렵습니다. [Brief explanation of why]. 만약 [alternative need — e.g., 실제 프로젝트 BIM 코디네이션 지원]이 필요하시다면 LUA BIM LABS의 [relevant service]를 확인해 보시길 권해드립니다. 학습 관련 질문은 언제든지 환영합니다!"*

**Never refuse without redirecting.** Always offer a path forward — either back to in-scope learning or to the appropriate LUA BIM LABS service.

---

## 10. Client Offboarding

### 10.1 Voluntary Cancellation

When a client requests cancellation:
1. Acknowledge the cancellation within 4 hours: *"[이름]님, 구독 취소 요청을 확인했습니다. [Last service date]까지 모든 서비스를 정상 제공하며, 이후 채널을 마무리하겠습니다."*
2. Continue delivering all services until the last paid day
3. On the final day, send:
   ```
   [이름]님, 함께한 [N]개월 동안 정말 수고하셨습니다.
   
   최종 학습 요약:
   - 시작 레벨: Level [N]
   - 마무리 레벨: Level [N]
   - 완료 레슨 수: [N]개
   - 주요 성장 포인트: [2-3 sentences]
   
   언제든지 다시 시작하고 싶으실 때 연락 주세요. 좋은 BIM 엔지니어로 성장하시길 응원합니다!
   ```
4. Archive client folder to: `Google Drive / PT Clients / ARCHIVED / [Client_Handle]_[End_Date] /`
5. Mark `PT_CLIENT_REGISTER` row as `Offboarded` with date

### 10.2 Non-Payment Offboarding

If payment is not received within 7 days of renewal date:
1. Send final payment notice: *"[이름]님, [N]일 전 갱신 예정이었으나 결제가 확인되지 않습니다. 결제가 완료되면 바로 서비스를 재개합니다. 24시간 내 결제가 어려우시면 알려 주세요."*
2. If no payment or response within 24 hours of final notice → pause all lesson delivery
3. Archive client data
4. Mark `PT_CLIENT_REGISTER` as `Suspended - Non-Payment`
5. If client pays within 30 days of suspension, reinstate service (no re-onboarding needed, resume from last lesson)
6. After 30 days of non-payment, mark as `Terminated`

### 10.3 Post-Offboarding Data Retention

- Client data retained for 12 months after offboarding in archived folder
- After 12 months, delete client data in compliance with privacy policy
- Aggregate anonymized learning data (no PII) may be retained for curriculum improvement

---

## 11. Record Keeping Summary

| Document | Location | Update Frequency |
|----------|----------|-----------------|
| PT_CLIENT_REGISTER | Google Sheet | Per event (payment, level change, offboarding) |
| CLIENT_PROFILE.md | Client Drive folder | Monthly (after progress report) |
| LESSON_LOG.md | Client Drive folder | Daily |
| WEAKNESS_LOG.md | Client Drive folder | As detected / As resolved |
| QA_LOG.md | Client Drive folder | Per Q&A event |
| PROGRESS_REPORTS/ | Client Drive folder | Monthly |

---

*End of Personal Tutor Delivery SOP v1.0*

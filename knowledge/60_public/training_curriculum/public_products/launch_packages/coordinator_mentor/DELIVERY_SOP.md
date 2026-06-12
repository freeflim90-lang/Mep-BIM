# Coordinator Mentor — Delivery SOP
## Standard Operating Procedure | LUA BIM LABS
**Service:** Coordinator Mentor | USD 229/month
**Version:** 1.0 | Effective: 2026-06-01

---

## 1. PURPOSE AND SCOPE

This SOP governs all operational activities for the Coordinator Mentor service. It is the single authoritative reference for LUA BIM LABS staff delivering this program. All staff must read and follow this document. Deviations require written approval from the COO.

This SOP covers the full lifecycle: client onboarding, daily and weekly delivery, monthly Zoom sessions, template pack management, certificate issuance, and escalation to Project Mentor.

---

## 2. CLIENT ONBOARDING

### 2.1 Intake and Payment Confirmation

**Trigger:** Client submits Intake Form and PayPal payment of USD 229 is confirmed.

**Step 1 — Payment Verification (within 2 business hours of submission)**
- Log in to PayPal dashboard and confirm payment received from the client email address on the intake form.
- Cross-check payment amount: USD 229.00 exactly.
- If payment is pending or incorrect, send the Payment Issue message from the Message Library (see Appendix A) and pause onboarding.
- If payment is confirmed, proceed immediately to Step 2.

**Step 2 — CRM Entry (within 2 business hours of payment confirmation)**
Create a new client record in the CRM with the following fields:
- Full name
- Email address
- Telegram username (record exactly as submitted, including the @ symbol)
- PayPal email
- Country/time zone
- Start date
- Subscription renewal date (Start Date + 30 days)
- Intake form answers (copy all fields verbatim)
- Coordinator experience level (Junior / Mid / Senior — assessed from intake answers)
- Assigned mentor (staff member responsible)

**Step 3 — Telegram Onboarding (within 4 business hours of payment confirmation)**
- Locate the client's Telegram account by the username from their intake form.
- Send the Welcome Message (Template CM-W01 from Appendix B).
- Send the Onboarding Packet via Telegram (5 files, see Section 7).
- Request confirmation that files were received.
- Add the client to the active monitoring list.

**Step 4 — Day 1 Setup Confirmation (within 24 hours of first contact)**
- After the client confirms receipt of the template pack, send the Day 1 Start Message (Template CM-W02).
- This message includes: the lesson delivery schedule, how to submit Issue Review reports, response time policy, and the monthly Zoom session scheduling link.
- Log confirmation in CRM: Onboarding Complete = TRUE, Date = [date confirmed].

### 2.2 Onboarding Completion Checklist

Before marking a client as "Active," verify all items below are checked:

- [ ] Payment confirmed in PayPal
- [ ] CRM record created with all fields
- [ ] Telegram contact established
- [ ] Welcome message sent
- [ ] Template pack (5 files) sent and receipt confirmed
- [ ] Day 1 Start Message sent
- [ ] Client added to Telegram monitoring list
- [ ] Monthly Zoom scheduling link sent
- [ ] Start date and renewal date logged in CRM

---

## 3. DAILY OPERATIONS

### 3.1 Lesson Delivery

The Coordinator Mentor curriculum is delivered as structured lessons sent via Telegram. Lessons are pre-written and approved. Staff are responsible for delivery, not creation, of lesson content (unless a custom session is authorized by the COO).

**Delivery Schedule:**
- Lessons are sent Monday–Friday at a consistent time in the client's local morning (between 08:00–09:00 local time where possible, or the time noted in the client's profile).
- Each lesson is a single Telegram message or a short set of linked messages.
- Lessons are numbered sequentially. CRM tracks the last lesson sent per client.

**Lesson Delivery Steps (each weekday):**
1. Open CRM and review the "Due for Lesson Today" list (automated dashboard).
2. For each client on the list, verify the lesson number to be sent from the CRM.
3. Copy the lesson content from the Lesson Library (internal Google Drive, access required).
4. Send the lesson via Telegram at the scheduled time.
5. Update CRM: Last Lesson Sent = [Lesson Number], Date Sent = [today].
6. If the client responds with a question about the lesson, log it in the Q&A Tracker (see Section 3.3) and reply within the response time policy (see Section 8).

**Lesson Pause Requests:**
If a client requests a pause (travel, workload, etc.), escalate to the COO. Pauses are not automatic and require written approval. The CRM pause flag must be set with a resume date.

### 3.2 Daily Monitoring Schedule

Staff must check Telegram daily (Monday–Friday) on the following schedule:

| Time Slot | Action |
|-----------|--------|
| 09:00 local | Send due lessons; check for overnight messages from clients in other time zones |
| 12:00 local | Mid-day check — respond to any unresolved messages flagged from morning |
| 17:00 local | End-of-day check — clear all pending responses; flag anything requiring next-day follow-up |

On weekends: Check Telegram once each day (Saturday and Sunday) for urgent messages only. "Urgent" is defined as a client message flagged with the words "urgent," "crisis," "emergency," or similar. Non-urgent weekend messages receive a response by 09:00 Monday.

### 3.3 Q&A Tracking

All questions received via Telegram are logged in the Q&A Tracker (shared Google Sheet). Required fields:

| Field | Description |
|-------|-------------|
| Date Received | Date the question was sent by the client |
| Client Name | From CRM |
| Lesson Reference | Which lesson the question relates to, if applicable |
| Question Summary | 1–2 sentence summary of the question |
| Response Sent | Date the response was sent |
| Response By | Staff member who responded |
| Escalated? | Yes / No |
| Notes | Any follow-up required |

Q&A entries are reviewed weekly during the internal team review (see Section 4.1) to identify patterns and improve lesson content.

---

## 4. WEEKLY OPERATIONS

### 4.1 Internal Team Review (Every Monday, 30 minutes)

Held internally — clients do not attend. Agenda:
1. CRM dashboard review: active clients, overdue lessons, renewal dates in the next 14 days
2. Q&A Tracker review: identify recurring questions; flag for lesson content improvement
3. Issue Review submissions received last week: were all reviewed and responded to?
4. Any escalation flags from the previous week
5. Any client at risk of cancellation or non-renewal (based on engagement indicators)

**Engagement Indicators to Monitor:**
- Client has not responded to a lesson in 5+ days
- Client has submitted zero Issue Review reports in 2 consecutive weeks
- Client has not responded to the monthly Zoom scheduling message within 7 days

If any indicator is triggered, send the Re-engagement Message (Template CM-RE01) and flag in CRM.

### 4.2 Issue Review Submission and Response

**What is an Issue Review:**
Each week, clients are invited to submit one real coordination issue they are facing at work. This is the core of the service — applying learning to real problems. The submission can be a message, screenshot, or brief written description sent to the LUA BIM LABS Telegram account.

**Submission Window:** Clients may submit at any time. The recommended prompt is sent by staff every Monday morning:

> "Good morning [Name]. This is your Week [N] prompt: Share one coordination challenge you encountered this week — a clash, a team communication issue, or a workflow problem. A few sentences and a screenshot (if you have one) is perfect. I'll send you a detailed response this week."

**Response Requirement:**
- Staff must send a written response to each Issue Review submission within 48 hours (business hours).
- Responses must: acknowledge the issue, provide a structured analysis or recommendation, reference relevant lesson content where applicable, and end with a follow-up question or action item for the client.
- Minimum response length: 150 words. Maximum recommended: 400 words.
- Log response in Q&A Tracker.

### 4.3 Weekly Case Study

One case study is delivered per month (see Section 5.3). There is no separate weekly case study — the weekly touchpoint is the Issue Review prompt and lesson delivery.

---

## 5. MONTHLY OPERATIONS

### 5.1 Monthly Zoom Session (30 Minutes)

One 30-minute Zoom session is included per calendar month.

**Scheduling Process:**
- On Day 1 of each month (or upon onboarding), send the client the Calendly scheduling link.
- The session must be completed within that calendar month. Unused sessions do not roll over.
- Sessions may be rescheduled once, with at least 48 hours notice. A no-show (client does not attend without 48-hour notice) counts as the session used.
- Session conducted by the assigned mentor.

**Session Protocol:**
1. Prepare by reviewing the client's CRM record, Q&A log, and Issue Review submissions from the past month.
2. Follow the Monthly Session Agenda Template (separate document: SESSION_AGENDA_TEMPLATE.md).
3. Take notes during the session in the Session Notes field in CRM.
4. Within 24 hours of the session: send the Post-Session Summary via Telegram (Template CM-PS01).

**Post-Session Summary Required Fields:**
- Date and duration of session
- Key discussion points (3–5 bullet points)
- Action items for the client (numbered list)
- Action items for LUA BIM LABS (if any)
- Next session scheduling note

### 5.2 Monthly Case Study Distribution

One case study is sent to the client each month. Case studies are anonymized real-world coordination scenarios with analysis.

**Timing:** Send during Week 3 of the subscription month (i.e., approximately Day 15–18).
**Format:** Text-based, sent as a Telegram message or linked PDF.
**Action:** After sending, post the prompt: "After reading this case study, what would you have done differently in the first 48 hours? Send me your thoughts — there's no wrong answer."
**Logging:** Log in CRM: Case Study [N] Sent = TRUE, Date = [date].

### 5.3 Monthly Scenario Challenge

One coordination scenario challenge is sent per month.

**Timing:** Send during Week 2 of the subscription month (i.e., approximately Day 8–12).
**Process:**
1. Send the scenario challenge message with full description and instructions.
2. Give the client 5 business days to submit their response.
3. Evaluate the response against the scoring criteria (see individual scenario files).
4. Send written feedback via Telegram within 48 hours of submission.
**Logging:** Log in CRM: Scenario [N] Sent, Submission Received, Feedback Sent.

---

## 6. TEMPLATE PACK DELIVERY

### 6.1 Template Pack Contents

The following 5 templates are sent to all Coordinator Mentor clients at onboarding:

| # | File Name | Description |
|---|-----------|-------------|
| 1 | CM-T01_Clash_Priority_Matrix.xlsx | Clash prioritization scoring sheet |
| 2 | CM-T02_Coordination_Meeting_Agenda.docx | Ready-to-use meeting agenda |
| 3 | CM-T03_Issue_Log_Master.xlsx | Comprehensive issue tracking table |
| 4 | CM-T04_Clash_Group_Naming_Convention_Guide.pdf | Naming convention guide |
| 5 | CM-T05_Weekly_Clash_Status_Report.docx | Weekly report template |

### 6.2 Delivery Protocol

Templates are sent via Telegram as direct file attachments (not links to Google Drive, to avoid access issues).

Send with the following message (Template CM-T-DELIVERY):

> "Here is your Coordinator Mentor Template Pack — 5 files you can use immediately on your projects. [File 1] [File 2] [File 3] [File 4] [File 5] — These are yours to keep and use on any project. If you have questions about how to use any of them, just ask. I'll explain each one in more detail in your first few lessons."

**Confirm receipt:** Ask the client to reply with a thumbs-up or "received" before closing the onboarding task.

### 6.3 Template Updates

If a template is updated after a client's onboarding date, the updated version is sent proactively via Telegram with a note explaining what changed. Clients always have the latest version.

---

## 7. 45-DAY COMPLETION CERTIFICATE

### 7.1 Eligibility

A client is eligible for the 45-Day Completion Certificate if they meet ALL of the following criteria by Day 45 of their subscription:

- [ ] Completed a minimum of 30 lessons (out of the scheduled 45 weekday lessons)
- [ ] Submitted a minimum of 3 Issue Review reports
- [ ] Attended the monthly Zoom session (or rescheduled and attended)
- [ ] Submitted at least 1 scenario challenge response

### 7.2 Issuance Process

1. On Day 44 of each active client's subscription, run the Eligibility Check from the CRM dashboard.
2. If eligible: Generate the certificate using the Certificate Template (internal Canva template, "CM Certificate v1.0"). Fields to fill: Client full name, completion date, certificate number (CM-[YEAR]-[SEQUENCE]).
3. Export as PDF.
4. Send via Telegram with the message (Template CM-CERT01).
5. Log in CRM: Certificate Issued = TRUE, Certificate Number, Date Issued.

**If not eligible:** Send the Gap Message (Template CM-CERT-GAP) explaining which criteria were not met and offering a 2-week extension review period.

### 7.3 Certificate Numbering

Format: `CM-2026-001` (year + 3-digit sequence). Sequence resets each calendar year. The running sequence number is tracked in the CRM.

---

## 8. ESCALATION TO PROJECT MENTOR

### 8.1 When to Escalate

Escalation means recommending that the client upgrade to Project Mentor (USD 490/month). Triggers for an escalation conversation:

- Client is consistently asking questions about BEP writing, QA/QC systems, or team management (beyond coordination scope)
- Client has been promoted or is targeting a BIM Lead role
- Client expresses frustration that the service doesn't address their strategic needs
- Client's questions consistently exceed coordination-level complexity
- Client has completed 3+ months and demonstrates advanced capability

### 8.2 Escalation Process

1. Do NOT upsell without a genuine reason. Only initiate escalation when there is a real need.
2. Send the Escalation Conversation Message (Template CM-ESC01) — this is a genuine, non-pushy message describing what Project Mentor covers and why it might be relevant.
3. If the client expresses interest, connect them to the Project Mentor intake form and waive the current month's remaining lessons (pro-rate the upgrade if mid-month).
4. Log in CRM: Escalation Initiated, Date, Outcome (Upgraded / Declined / Considering).

---

## 9. RESPONSE TIME POLICY

This is a firm commitment. All staff must adhere to these times.

| Message Type | Response Time |
|--------------|--------------|
| General Telegram message (Monday–Friday) | Within 24 hours |
| Issue Review submission | Within 48 hours (business days) |
| Scenario challenge submission | Within 48 hours of submission |
| Post-Zoom session summary | Within 24 hours of session |
| Payment or billing questions | Within 4 business hours |
| Urgent flag (client uses "urgent/crisis/emergency") | Within 4 hours (including evenings) |
| Weekend messages (non-urgent) | By 09:00 Monday |

**If response time is at risk of being missed** (staff illness, technical issue, etc.): Send the Delay Notification message within the response window: "Hi [Name], I received your message. I'm looking into this and will send you a full response by [specific time]. Thank you for your patience."

Log all delay notifications in CRM.

---

## 10. OUT-OF-SCOPE REQUEST HANDLING

### 10.1 What Is Out of Scope

The following are NOT included in Coordinator Mentor:

- Authoring or reviewing BEP documents
- Reviewing the client's actual project models
- Attending the client's company meetings or calls
- Providing legal, contractual, or HR advice
- Creating custom lesson content on demand
- Career coaching (strategic role progression) — this is Project Mentor territory
- Providing content in languages other than English

### 10.2 How to Handle Out-of-Scope Requests

**Step 1:** Acknowledge the request warmly. Never make the client feel bad for asking.
**Step 2:** Explain clearly what IS possible and what is not.
**Step 3:** If the out-of-scope request is something Project Mentor covers, mention it briefly (once, not repeatedly).

**Example Response:**

> "That's a great question, [Name]. Reviewing your actual project BEP sits outside the Coordinator Mentor scope — it requires a deeper engagement with your project documents than I'm able to do in this format. What I can do is walk you through the key sections of a BEP and how to approach writing each one, which is something we'll cover in an upcoming lesson. If you want hands-on BEP review and guidance, Project Mentor is set up for exactly that — just let me know if you'd like more details."

Do not repeat the upsell mention more than once per interaction.

---

## APPENDIX A — PAYMENT ISSUE MESSAGE TEMPLATES

**CM-PAY-01: Payment Amount Mismatch**
> "Hi [Name], thank you for signing up for Coordinator Mentor. We've received your form, but the payment we received doesn't match the subscription amount. Could you please check the PayPal payment for [Amount] to [PayPal address]? Once confirmed, we'll get your account activated right away. Apologies for any inconvenience."

**CM-PAY-02: Payment Pending**
> "Hi [Name], thank you for signing up. Your intake form is received. PayPal is showing your payment as pending — this usually clears within 24 hours. We'll activate your account as soon as the payment clears. We'll message you here when you're ready to go."

---

## APPENDIX B — MESSAGE TEMPLATES

**CM-W01: Welcome Message**
> "Welcome to Coordinator Mentor, [Name]! I'm [Staff Name] from LUA BIM LABS — I'll be your mentor throughout this program. Your account is active and we're ready to start.
>
> I'm sending you the Template Pack right now (5 files). Once you confirm you've received them, I'll send your Day 1 information. Really glad to have you here — looking forward to working through some real coordination challenges together."

**CM-W02: Day 1 Start Message**
> "Great — you're all set, [Name]. Here's what your Coordinator Mentor program looks like:
>
> LESSONS: You'll receive a lesson Monday–Friday, each designed around a real coordination skill. Lessons are short and practical.
>
> WEEKLY ISSUE REVIEW: Every Monday I'll send you a prompt to share a real coordination challenge you're facing. I'll reply with a detailed written response — this is the most valuable part of the program.
>
> MONTHLY ZOOM: Once a month we have a 30-minute Zoom call. I'll send you the scheduling link at the start of each month.
>
> RESPONSE TIME: Monday–Friday, I respond to all messages within 24 hours.
>
> If you have any questions, message me here anytime. Your first lesson arrives tomorrow morning. Let's get started."

**CM-RE01: Re-engagement Message**
> "Hi [Name], I wanted to check in — I noticed we haven't had much back-and-forth recently and I want to make sure the program is working for you. Is there anything you'd like to cover that we haven't yet? Or any area where you'd like me to focus more? This is your program — let's make sure it's useful."

**CM-T-DELIVERY: Template Pack Delivery Message**
(See Section 6.2)

**CM-CERT01: Certificate Delivery Message**
> "Congratulations, [Name]! You've completed 45 days of Coordinator Mentor. Here is your Certificate of Completion — Certificate Number [CM-XXXX-XXX]. This reflects your commitment to developing your coordination skills and applying them to real project challenges. Well done."

**CM-CERT-GAP: Certificate Eligibility Gap Message**
> "Hi [Name], we're at Day 45 of your program. You've made good progress, and I want to be straightforward with you: the completion certificate requires [list unmet criteria]. You're close. I'd like to offer a 2-week review period — if we can complete those items together, I'll issue the certificate. Let me know if you'd like to do that."

**CM-ESC01: Escalation to Project Mentor Message**
> "Hi [Name], something I've noticed over the past few weeks — your questions are consistently going deeper than coordination; you're thinking about BEP structure, team quality systems, and how to lead a BIM project rather than just coordinate one. That tells me you're ready for the next level. Project Mentor is designed for exactly where you are now. It includes 60-minute monthly Zoom sessions, BEP review, QA/QC system guidance, and career growth planning. If you'd like to know more, I'm happy to walk you through it — no pressure."

---

*Document Owner: COO, LUA BIM LABS*
*Review Cycle: Quarterly*
*Last Reviewed: 2026-05-01*

# Project Mentor — Delivery SOP
## Standard Operating Procedure | LUA BIM LABS
**Service:** Project Mentor | USD 490/month (Standard) | USD 790/month (Intensive)
**Version:** 1.0 | Effective: 2026-06-01

---

## 1. PURPOSE AND SCOPE

This SOP governs all operational activities for the Project Mentor service. It is the single authoritative reference for LUA BIM LABS staff delivering this program. All staff must read and follow this document before delivering any Project Mentor session or client interaction.

Project Mentor is a higher-engagement service than Coordinator Mentor. Clients are BIM Leads, Senior BIM Coordinators, or experienced professionals preparing to move into BIM project leadership roles. The service includes monthly 60-minute Zoom sessions, BEP guidance, QA/QC development support, delivery simulation scenarios, and a quarterly Career Growth Assessment.

Deviations from this SOP require written approval from the COO.

---

## 2. CLIENT ONBOARDING

### 2.1 Payment Verification and Package Confirmation

**Trigger:** Client submits Intake Form and PayPal payment is confirmed.

**Payment amounts:**
- Standard: USD 490/month
- Intensive: USD 790/month

**Step 1 — Payment Verification (within 2 business hours of submission)**
- Confirm PayPal payment amount matches the package selected on the intake form.
- If the client selected "Standard" but paid "Intensive" amount (or vice versa), contact them immediately to confirm package before proceeding.
- Payments that are pending: send the Payment Pending message (Template PM-PAY-01) and pause onboarding.

**Step 2 — CRM Entry (within 2 business hours of payment confirmation)**

Create a new client record with the following fields:
- Full name and email
- Telegram username (with @ symbol)
- PayPal email
- Package type: Standard or Intensive
- Country and time zone
- Start date and renewal date
- Intake form answers (verbatim copy)
- Career stage assessment (Junior Lead / Mid Lead / Senior Lead — assessed from intake)
- BEP experience flag: Yes / Partial / No (from intake form)
- QA/QC system flag: Yes / Partial / No (from intake form)
- Career goal: Stay in BIM Lead / Move to PM / Independent Consulting / Other
- Assigned mentor (staff member responsible for this client)
- Quarterly assessment due date (Start Date + 90 days; then every 90 days)

**Step 3 — Welcome Message and First Zoom Scheduling (within 4 business hours)**
- Send Welcome Message (Template PM-W01) via Telegram.
- Include the Calendly link for the first Zoom session. The first session should happen within 10 days of onboarding — this is a priority.
- Do not wait for the client to ask — proactively schedule.

**Step 4 — Template Pack Delivery (within 24 hours of first Telegram contact)**
- Send the Project Mentor Template Pack (see Section 6).
- Request confirmation of receipt before closing the onboarding task.
- Send the Template Pack Context Message (Template PM-T-DELIVERY) with a brief explanation of each document.

**Step 5 — Day 1 Setup Message (after template receipt confirmed)**
- Send the Day 1 Start Message (Template PM-W02) explaining the full service structure: Zoom cadence, Telegram availability, weekly check-ins, quarterly assessment, and delivery simulations.
- Log all steps complete in CRM: Onboarding Complete = TRUE.

### 2.2 Onboarding Completion Checklist

- [ ] Payment confirmed (correct amount + correct package)
- [ ] CRM record created with all fields
- [ ] Welcome message sent via Telegram
- [ ] First Zoom session scheduled within 10 days
- [ ] Template pack sent and receipt confirmed
- [ ] Day 1 Start Message sent
- [ ] Client added to monitoring list
- [ ] Quarterly assessment due date logged in CRM

---

## 3. DAILY OPERATIONS

### 3.1 Telegram Monitoring

Project Mentor includes a commitment to higher-priority Telegram monitoring than Coordinator Mentor. Standard package clients receive responses within 24 hours on business days. Intensive package clients receive responses within 12 hours on business days.

**Monitoring Schedule (business days):**

| Time | Action |
|------|--------|
| 08:30 local | Morning check — review all overnight messages from all PM clients |
| 12:00 local | Midday check — clear pending responses from morning; prioritize Intensive clients |
| 17:00 local | End-of-day check — resolve all open items; log anything carried to next day |

**Weekend monitoring:**
- Standard clients: check once per day. Respond by 09:00 Monday for non-urgent messages.
- Intensive clients: check twice per day (morning and evening). Respond to non-urgent within 6 hours.
- Urgent messages (see Section 8): respond within 4 hours regardless of day or package.

### 3.2 Response Quality Standard

Project Mentor responses are expected to be more technically substantive than Coordinator Mentor responses. When a client asks a technical question (BEP structure, model health, team management, delivery strategy), the response must:
- Acknowledge the question specifically (not generically)
- Provide a direct, expert-level answer
- Reference applicable standards (ISO 19650, BEP best practices, QA/QC frameworks) where relevant
- End with a next step or follow-up question for the client

Minimum response length for technical questions: 200 words. Maximum recommended: 600 words. For complex questions requiring more, break the response into a structured message with clear headers.

---

## 4. WEEKLY OPERATIONS

### 4.1 Internal Team Review (Every Monday, 30 minutes)

Agenda (same format as Coordinator Mentor, but PM-specific items added):
1. CRM dashboard: active PM clients, upcoming Zoom sessions, quarterly assessment due dates
2. Telegram review: any technical questions from the past week that required escalation?
3. Delivery simulation submissions: any outstanding evaluations?
4. Career assessment reports: any due this week?
5. Clients at risk: engagement indicators reviewed (see Section 4.3)

### 4.2 Weekly Check-In Message

Every Monday morning, send a brief personalized check-in to each Project Mentor client. This is not a form message — it must reference something specific to the client's situation (current project, recent conversation, upcoming deadline they mentioned).

**Format:**
> "Good morning [Name]. Week [N] — how's the [specific project or challenge they mentioned] going? [One specific prompt question based on their current situation.] Send me an update when you have a moment."

This message takes 2–3 minutes per client to personalize. It is not optional. It signals ongoing engagement and prevents the client from feeling that the service is passive.

**Log:** Mark in CRM: Weekly Check-In Sent = TRUE, Week [N], Date.

### 4.3 Engagement Indicators

Monitor for the following engagement warning signals:

| Indicator | Threshold | Action |
|-----------|-----------|--------|
| Client has not responded to any message | 5+ business days | Send the Re-engagement Message (PM-RE01) |
| Client has not scheduled their Zoom session | 14 days into the month | Send a direct scheduling message with 3 specific time options |
| Client has not submitted a delivery simulation in 2 months | — | Proactively offer a new scenario |
| Client expresses that they are "too busy" repeatedly | 2+ consecutive weeks | Raise a scope/expectations conversation |
| Client asks questions consistently outside PM scope | 3+ times | Raise the boundary clearly (see Section 9) |

---

## 5. MONTHLY OPERATIONS

### 5.1 Monthly Zoom Session (60 Minutes)

One 60-minute Zoom session per calendar month is included. This is the anchor of the service.

**Scheduling:**
- Send the Calendly link on the first day of each month (or at onboarding for Month 1).
- Session must be completed within the calendar month. Sessions do not roll over.
- One reschedule allowed with 48+ hours notice.
- No-show = session used. (See rescheduling policy in SESSION_AGENDA_TEMPLATE.md)

**Pre-Session Preparation (mentor, 30 minutes before the session):**
- Review the client's CRM record: career goal, current project, BEP/QA status, notes from previous sessions.
- Review Telegram exchanges from the past 30 days — what themes emerged?
- Review the previous session's post-session summary and action item completion.
- Note any delivery simulation or scenario submitted since the last session.
- Prepare 2 discussion prompts in case the client runs out of agenda items.

**Session Protocol:**
- Follow the Monthly Session Agenda Template (SESSION_AGENDA_TEMPLATE.md).
- Take notes during the call.
- Within 24 hours: send the Post-Session Summary (Template PM-PS01).

### 5.2 Delivery Simulation

One delivery simulation scenario is issued per month (or as agreed with the client — some months may have the scenario mid-month, others near end of month based on client workload).

**Process:**
1. Issue the scenario via Telegram. Client has 7 business days to submit their delivery package plan.
2. Evaluate the submission against the scenario's scoring criteria (see individual scenario files).
3. Send detailed written feedback within 48 hours of submission.
4. Discuss the scenario and feedback in the monthly Zoom session if timing aligns — this is highly recommended.

**Logging:** CRM: Simulation [N] Issued, Submitted, Feedback Sent, Discussed in Zoom (Y/N).

### 5.3 Post-Session Follow-Up Summary

Send within 24 hours of the Zoom session. Use the format specified in SESSION_AGENDA_TEMPLATE.md.

---

## 6. QUARTERLY OPERATIONS

### 6.1 Career Growth Assessment

A Career Growth Assessment is conducted every 90 days for all Project Mentor clients.

**Process:**
1. On the day the quarterly assessment is due (tracked in CRM), send the Career Assessment Form to the client via Telegram.
2. Give the client 7 days to complete and return the form.
3. LUA BIM LABS reviews the responses and generates the Career Growth Report (see CAREER_ASSESSMENT_FORM.md for the scoring interpretation guide).
4. Send the Career Growth Report within 5 business days of receiving the completed form.
5. Schedule a Zoom session to discuss the report (this may be the regular monthly session if timing aligns, or an additional 30-minute call).

**Career Growth Report Format:**
- Competency radar chart (or table equivalent) showing self-assessment scores
- LUA BIM LABS commentary on each competency area (based on Telegram exchanges and session observations)
- Gap analysis: current state vs. career goal
- 3 priority development areas for the next quarter
- Recommended resources or actions for each priority area

**Logging:** CRM: Quarterly Assessment [N] Sent, Received, Report Issued, Discussion Completed.

### 6.2 Quarterly Service Review

In addition to the client-facing Career Growth Assessment, LUA BIM LABS conducts an internal quarterly service review for each PM client:

- Is the client progressing toward their stated career goal?
- Is the service delivering value commensurate with the USD 490/month fee?
- Is there any scope creep or boundary issue that needs to be addressed?
- Is the client a good candidate for an upgrade pathway or additional services?

Document the review findings in CRM: Quarterly Review Notes.

---

## 7. TEMPLATE PACK DELIVERY

### 7.1 Template Pack Contents

The following templates are sent to all Project Mentor clients at onboarding:

| # | Document | Description |
|---|----------|-------------|
| 1 | PM-T01_BEP_Template.docx | 8-section BIM Execution Plan template (ISO 19650 aligned) |
| 2 | PM-T02_HVAC_QA_Checklist.xlsx | HVAC BIM model QA/QC checklist |
| 3 | PM-T03_Electrical_QA_Checklist.xlsx | Electrical BIM model QA/QC checklist |
| 4 | PM-T04_Career_Assessment_Form.pdf | Quarterly self-assessment form |
| 5 | PM-T05_Delivery_Checklist.xlsx | Pre-delivery verification checklist for model submissions |

### 7.2 Delivery Protocol

Send all files as direct Telegram file attachments. Do not use Google Drive links.

**Template Pack Context Message (Template PM-T-DELIVERY):**
> "Here is your Project Mentor Template Pack — 5 documents that form the core working toolkit for a BIM Lead. [File 1] — your BEP template, ready to be adapted for your next project. [File 2] [File 3] — the QA/QC checklists you'll use before approving any model for coordination or delivery. [File 4] — your quarterly career assessment form, which we'll use every 90 days to track your growth. [File 5] — the delivery checklist. These are yours to use on real projects immediately. We'll go through each one in our first Zoom session."

---

## 8. PRIORITY RESPONSE ENFORCEMENT

### 8.1 Response Time Commitments

| Message Type | Standard Package | Intensive Package |
|-------------|-----------------|------------------|
| General Telegram message (Mon–Fri) | Within 24 hours | Within 12 hours |
| Technical question (Mon–Fri) | Within 24 hours | Within 8 hours |
| Delivery simulation submission | Within 48 hours | Within 24 hours |
| Post-Zoom session summary | Within 24 hours | Within 12 hours |
| Career Growth Report | Within 5 business days of receiving form | Within 3 business days |
| Billing questions | Within 4 business hours | Within 2 business hours |
| Urgent flag | Within 4 hours (any day) | Within 2 hours (any day) |

### 8.2 Priority Enforcement Protocol

**If a response time is at risk of being missed:**
1. Send a Delay Notification within the standard response window: "Hi [Name], I have your message. I'm looking into this in detail and will send you a full response by [specific time]."
2. Log the delay in CRM: Delayed Response, Reason, Resolution Date.
3. If a delay occurs more than twice in a 30-day period, flag for COO review.

**Urgent classification:** Any message from a client containing the words "urgent," "client deadline," "submission tomorrow," "crisis," "emergency," or "approval needed by."

---

## 9. OUT-OF-SCOPE BOUNDARY ENFORCEMENT

### 9.1 What Is Out of Scope for Project Mentor

- Authoring BEP documents on behalf of the client (guidance only — the client writes)
- Attending the client's company meetings or calls as a representative of LUA BIM LABS
- Reviewing and approving the client's actual project models
- Providing legal, HR, or contractual advice
- Creating or reviewing project-specific standard files (custom scripts, custom families, etc.)
- Serving as a reference or guarantor for the client's employment applications
- Providing content in languages other than English

### 9.2 How to Handle Out-of-Scope Requests

**Step 1:** Acknowledge the request warmly. The client is not wrong to ask.
**Step 2:** Explain clearly what is and is not possible within the service.
**Step 3:** Offer the closest in-scope alternative.

**Example response:**
> "I'd love to help you review your actual BEP document in detail, [Name] — but doing a full document review and markup sits outside what Project Mentor is set up to do. What I can do is walk you through each section together on our next Zoom call, and you can screen-share the document so I can give you real-time guidance on structure and content. That tends to be more useful than a written markup anyway. Would that work for you?"

### 9.3 Repeated Out-of-Scope Requests

If a client repeatedly requests out-of-scope work (3 or more times):
1. Have a direct conversation about expectations on the next Zoom session.
2. Revisit the intake form's service understanding acknowledgements.
3. If the client genuinely needs services beyond the scope (e.g., a full BEP authoring engagement), discuss a custom project engagement at an additional fee — escalate to COO to scope and price.

---

## APPENDIX — MESSAGE TEMPLATES

**PM-W01: Welcome Message**
> "Welcome to Project Mentor, [Name]. I'm [Mentor Name] from LUA BIM LABS — I'll be your dedicated mentor throughout the program. Your account is active. I'm sending you the scheduling link for your first Zoom session — let's get that booked within the next 10 days. I'll also send your template pack shortly. Really glad you're here. This is going to be a productive few months."

**PM-W02: Day 1 Start Message**
> "You're all set, [Name]. Here's how Project Mentor works:
>
> MONTHLY ZOOM: 60 minutes, once a month. We'll cover your real project challenges, BEP and QA/QC development, and career strategy. Scheduling link sent separately.
>
> WEEKLY CHECK-IN: I'll message you every Monday. This keeps us connected and ensures I can help you in real time, not just once a month.
>
> DELIVERY SIMULATIONS: Once a month, I'll send you a delivery scenario to work through. Your submitted response gets detailed written feedback from me.
>
> QUARTERLY CAREER ASSESSMENT: Every 90 days, you complete a self-assessment and I generate a Career Growth Report showing your progress.
>
> RESPONSE TIME: Monday–Friday, I respond within 24 hours (Standard) or 12 hours (Intensive).
>
> If anything urgent comes up — a tricky project situation, a client deadline, a team conflict — message me. That's what I'm here for."

**PM-RE01: Re-engagement Message**
> "Hi [Name], I haven't heard much from you recently and I want to check in properly. Is the program still working for you, or has something shifted in your workload or goals? I'd rather have an honest conversation and adjust than have you feel like you're not getting value. Message me when you can — I'm here."

---

*Document Owner: COO, LUA BIM LABS*
*Review Cycle: Quarterly*
*Last Reviewed: 2026-05-01*

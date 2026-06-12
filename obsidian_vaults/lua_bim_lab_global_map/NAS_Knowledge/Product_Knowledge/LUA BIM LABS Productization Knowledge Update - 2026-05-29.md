---
type: product-knowledge-update
brand: LUA BIM LABS
date: 2026-05-29
status: active
tags:
  - lua-bim-labs
  - productization
  - starter-plan
  - telegram-education
  - paypal
  - obsidian
---

# LUA BIM LABS Productization Knowledge Update - 2026-05-29

## Summary

LUA BIM LABS has moved from general MEP BIM knowledge sharing into the first productized education service:

- Product: LUA BIM LABS Starter Plan
- Price: USD 39 / month
- Delivery: Telegram daily lessons
- Payment: PayPal
- Intake: Google Form and Google Sheet
- Knowledge system: Obsidian NAS Knowledge

## Product Knowledge Added

### Starter Plan

- [[Starter/README|Starter Product Knowledge]]
- [[Starter/Starter Plan - 30 Day Launch Curriculum|Starter Plan - 30 Day Launch Curriculum]]

Starter is now structured as a 30-day paid launch curriculum rather than a loose internal year-based training sequence.

Each lesson should include:

- one focused MEP BIM topic
- one practical project lens
- three BIM checks
- one common mistake
- one daily action
- one scope reminder

### Product Ladder

- [[Personal_Tutor/README|Personal Tutor]]
- [[Coordinator_Mentor/README|Coordinator Mentor]]
- [[Project_Mentor/README|Project Mentor]]

The current product ladder is:

```text
Starter -> Personal Tutor -> Coordinator Mentor -> Project Mentor
```

Starter validates demand and beginner pain points. Later services should deepen diagnosis, coordination mentoring, and project-specific support with stricter boundaries.

## Operations Knowledge Added

### Application and Telegram

Source documents:

- `docs/starter_plan_application_form_spec.md`
- `docs/starter_plan_application_management.md`
- `docs/starter_plan_telegram_onboarding_pipeline.md`

Operational flow:

```text
Google Form -> PayPal payment -> Telegram /start -> chat_id sync -> manual payment review -> active client -> daily lesson delivery
```

Key principle:

Telegram `chat_id` prevents uncontrolled delivery, but payment verification should remain a human review step during launch.

### Revenue and PayPal

Source document:

- `docs/paypal_revenue_tax_operations.md`

Current status:

- Non-registered individual launch stage
- Focus on evidence collection and annual income tax preparation
- Business registration should be reviewed when revenue becomes regular and repeated

Important evidence:

- PayPal monthly statement
- PayPal transaction detail
- PayPal withdrawal confirmation
- Korean bank deposit record
- Google Form response
- Telegram activation/service proof
- Starter curriculum/service description at time of payment

## Knowledge Collection Rules

### Public-Safe Knowledge

May be reused for:

- blog posts
- Telegram Starter lessons
- beginner FAQs
- public onboarding

Examples:

- general MEP BIM concepts
- anonymized beginner mistakes
- checklist patterns
- productized learning structure

### Client-Private Knowledge

Keep separate in client records:

- name
- email
- PayPal email
- Telegram username
- Telegram chat ID
- payment status
- learning profile

### Project-Sensitive Knowledge

Requires review before reuse:

- project-derived examples
- model files
- drawings
- clash reports
- approval, code, design, or construction decision issues

## Current Obsidian Structure

```text
NAS_Knowledge
├─ Blog_MEP_BIM
├─ Starter_Plan_Clients
├─ Product_Knowledge
│  ├─ Starter
│  ├─ Personal_Tutor
│  ├─ Coordinator_Mentor
│  └─ Project_Mentor
├─ Revit_Assistant_QA
└─ Team_Telegram_QA
```

## Next Knowledge Actions

- Review the first real Starter customer questions.
- Promote repeated beginner issues into Starter FAQ.
- Use Starter completion patterns to design Personal Tutor diagnosis.
- Keep PayPal/customer information out of public product knowledge.
- Continue blog knowledge capture under `Blog_MEP_BIM`.
- Rebuild the global Obsidian map after each major product knowledge update.

## Related

- [[Product Knowledge]]
- [[Starter/README|Starter Product Knowledge]]
- [[Starter/Starter Plan - 30 Day Launch Curriculum|Starter Plan - 30 Day Launch Curriculum]]
- [[Global Knowledge Map]]


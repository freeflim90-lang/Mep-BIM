# Starter Plan Application Form Specification

## Purpose

The Starter application form collects the minimum information needed to:

- identify the client
- confirm PayPal payment
- connect the client to Telegram delivery
- understand the client's MEP BIM learning level and discipline focus
- assign the correct Day 61–90 discipline track
- record consent for receiving educational content
- create a client profile and Obsidian learning note

## Recommended Form Title

LUA BIM LABS Starter Plan Application

## Form Description

Thank you for joining the LUA BIM LABS Starter Plan.

This is a 90-Day MEP BIM Starter Program delivered through Telegram.

Program structure:
- Day 1–60: MEP BIM Foundation (MEP orientation, Revit MEP basics, drawing reading, model quality, clash coordination, data and schedules, site-readiness thinking, BIM career habits)
- Day 61–90: Discipline Deep-Dive (your chosen MEP discipline — HVAC, Piping, Plumbing, Fire Protection, or Electrical)
- Every Friday: BIM Check Friday quiz (self-assessment, no grades)
- Track completion: Quick Reference Card delivered at the end of each foundation track
- Day 60: Foundation completion message
- Day 90: Program completion message

After submitting this form and completing PayPal payment, LUA BIM LABS will verify your payment and connect you to the Telegram lesson delivery channel.

Before submitting this application, please complete the Starter Plan payment.

PayPal Payment Link:
https://www.paypal.com/ncp/payment/9NQE7BEG2M7PS

After payment, submit this form with the email used for PayPal payment.

## Section 1: Client Information

Required:

- Full name
- Email address
- Country
- Preferred language

Optional:

- Time zone
- Company or school
- Job title

## Section 2: PayPal Payment Information

Required:

- Email used for PayPal payment

Optional:

- PayPal transaction ID or receipt ID
- Payment date

Fixed expected amount:

- USD 39

Instruction text:

Please complete payment before submitting this form. If you have not paid yet, use the PayPal link above.

## Section 3: Telegram Connection

Required:

- Telegram username, including `@`

Optional:

- Telegram display name
- Telegram user ID if known

Instruction text:

Telegram username is required so LUA BIM LABS can match your application with your Telegram account.

After payment and form submission, please open the LUA BIM LABS Telegram bot and send `/start`. Your service can begin only after PayPal payment is verified and Telegram connection is confirmed.

If you do not know your Telegram user ID, leave it blank.

## Section 4: Learning Profile

Required:

- Current BIM level
- MEP discipline track (Days 61–90)

Optional:

- Revit MEP experience
- Navisworks experience
- Learning goal
- Biggest current difficulty

Suggested options:

Current BIM level:

- Beginner
- Junior Revit MEP Modeler
- MEP Engineer learning BIM
- BIM Coordinator beginner
- Other

MEP discipline track (Days 61–90):

This selection determines your Day 61–90 specialist curriculum. Days 1–60 are the same Foundation program for all learners.

- HVAC (Air Conditioning & Ventilation)
- Piping / Mechanical
- Plumbing / Sanitary
- Fire Protection
- Electrical

Learning goal:

- Learn MEP BIM basics
- Improve Revit MEP modeling
- Understand clash coordination
- Prepare for BIM project work
- Build daily BIM learning habit

## Section 5: Service Understanding

Required checkboxes:

- I understand the Starter Plan is a 90-Day MEP BIM program: Day 1–60 Foundation, Day 61–90 Discipline Deep-Dive.
- I understand my chosen MEP discipline determines my Day 61–90 curriculum track.
- I understand I will receive a BIM Check Friday quiz every Friday (self-assessment only, no grades or feedback).
- I understand Quick Reference Cards will be sent at the end of each foundation track (up to 8 cards over 90 days).
- I understand the Starter Plan provides daily MEP BIM lessons through Telegram.
- I understand the Starter Plan does not include project file review.
- I understand the Starter Plan does not include Revit model QA.
- I understand the Starter Plan does not include clash report review.
- I understand the Starter Plan is educational content only and does not provide engineering design verification, code compliance confirmation, construction approval, legal advice, or professional certification.
- I understand LUA BIM LABS does not guarantee employment, certification, project approval, construction acceptance, or business results.
- I understand Personal Tutor, Coordinator Mentor, and Project Mentor are Coming Soon.
- I agree to receive educational messages through Telegram.
- I have read and agree to the Starter Plan terms, disclaimers, refund policy, and cancellation policy.

## Section 6: Privacy and Content Use

Required checkboxes:

- I will not upload confidential project files, private drawings, contracts, or personal data through Telegram.
- I understand that general questions may be anonymized and reused as educational knowledge by LUA BIM LABS.
- I agree that LUA BIM LABS may store my learning profile and service notes for education delivery and support.

## Section 7: Questions

Optional:

- What would you like to learn first?
- Any question before onboarding?

## After Submission

Manual operations:

1. Check PayPal payment.
2. Register the client with `scripts/starter_plan_onboarding.py`.
3. Ask the client to open the Telegram bot and send `/start`.
4. Confirm Telegram `chat_id`.
5. Create Obsidian client note.
6. Send Telegram welcome message.
7. Add client to daily Starter lesson delivery.

## Telegram Welcome Message Template

Hello, this is LUA BIM LABS.

Your Starter Plan application and PayPal payment have been received.

You are now enrolled in the 90-Day MEP BIM Starter Program.

Program structure:
- Day 1–60: MEP BIM Foundation
- Day 61–90: {discipline} Deep-Dive track
- Every Friday: BIM Check Friday quiz
- Track completion: Quick Reference Cards (up to 8 over 90 days)

Starter Plan includes:
- Daily MEP BIM lesson through Telegram
- Beginner-friendly explanation with practical checklist or action item
- Weekly BIM Check Friday self-assessment quiz
- Quick Reference Cards at track completion points
- Day 60 Foundation completion message
- Day 90 program completion message

Starter Plan does not include:
- Project file review
- Revit model QA
- Clash report review
- Unlimited 1:1 Q&A

Personal Tutor, Coordinator Mentor, and Project Mentor are planned as Coming Soon services.

Welcome to LUA BIM LABS Starter Plan.

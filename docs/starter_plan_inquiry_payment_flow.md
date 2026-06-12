# Starter Plan Inquiry and PayPal Payment Flow

## Public Flow

1. Blog CTA
2. Starter application form with PayPal link inside
3. PayPal payment
4. Payment confirmation
5. Telegram onboarding
6. Daily MEP BIM lesson delivery
7. Obsidian client learning record

## Required Links

Add these to `config/personal_mep_bim_tutor_plans.json`.

```json
"service_links": {
  "application_form": "https://forms.gle/...",
  "application_sheet": "https://docs.google.com/spreadsheets/d/...",
  "telegram_contact": "https://t.me/...",
  "contact_email": "contact@example.com",
  "terms_url": ""
}
```

Current application management sheet:

https://docs.google.com/spreadsheets/d/1v1t5k76mAhKSBx-x19fEw3Kmi7c6heFKMrkIbK_qcFk/edit?usp=sharing

Add the PayPal Starter link here:

```json
{
  "id": "starter",
  "paypal_payment_link": "https://www.paypal.com/ncp/payment/...",
  "paypal_subscription_link": ""
}
```

## Starter Form Fields

Semi-integrated form rule:

The Google Form should show the PayPal link before the payment information section.

```text
Before submitting this application, please complete the Starter Plan payment.

PayPal Payment Link:
https://www.paypal.com/ncp/payment/9NQE7BEG2M7PS

After payment, submit this form with the email used for PayPal payment.
```

Detailed form specification:

- `docs/starter_plan_application_form_spec.md`
- `config/starter_plan_application_form_schema.json`
- `docs/starter_plan_terms_and_disclaimers.md`

- name
- email
- country
- Telegram username
- current BIM level
- MEP discipline
- Revit MEP experience
- learning goal
- question
- PayPal payment email
- PayPal transaction ID, optional

## Manual Verification

For the first launch, verify PayPal payment manually before starting lessons.

After verification:

1. Create client profile from `config/personal_mep_bim_tutor_client_schema.json`.
2. Create an Obsidian client note.
3. Add the client to Telegram delivery.
4. Mark payment status as `paid`.

## Recommended Admin Columns

Add these manual management columns to the Google Sheet after the form response columns:

```text
Payment Verified
Telegram Verified
Client Status
Start Date
End Date
Obsidian Note
Admin Notes
```

Recommended status values:

```text
pending_payment
paid_waiting_telegram
active
expired
cancelled
refund_requested
refunded
```

# LUA BIM LABS PayPal Revenue and Tax Operations

## Purpose

This document defines the first-launch revenue management process for LUA BIM LABS Starter Plan payments received through PayPal.

This is an operational checklist, not tax or legal advice. Final VAT, income tax, corporate tax, and zero-rated export treatment should be reviewed with a Korean tax professional.

## Current Product

- Product: LUA BIM LABS Starter Plan
- Price: USD 39 / month
- Payment provider: PayPal
- Application system: Google Form and Google Sheet
- Delivery: Telegram
- Current launch status: non-registered individual launch stage

## Current Operator Status

LUA BIM LABS is currently launching as a non-registered individual / pre-business-registration test.

Operational position:

- Focus on market validation, customer onboarding, and evidence collection.
- Do not overcomplicate VAT zero-rate filing before business registration.
- Keep clean records so income can be explained and reported later.
- Review business registration when revenue becomes regular and repeated.
- Confirm final tax handling with a Korean tax professional before annual filing.

## Source of Truth

- PayPal: payment and withdrawal source of truth
- Google Sheet: customer, payment, service status, and revenue management
- Obsidian: internal service notes and product knowledge
- Bank statement: KRW receipt confirmation after withdrawal
- Dedicated bank account: recommended account for PayPal withdrawals only

## Payment Review Flow

1. Customer submits Google Form.
2. Customer completes PayPal payment.
3. Revenue manager checks the PayPal transaction.
4. Revenue manager matches PayPal payer email with the Google Form row.
5. Revenue manager marks `Payment Verified = yes`.
6. Revenue manager records transaction details in the Revenue Ledger sheet.
7. Telegram `/start` sync records `Telegram Chat ID`.
8. Customer is activated only after payment and Telegram connection are confirmed.

## PayPal Withdrawal to Korean Bank

PayPal Korea official guidance says funds can be withdrawn to a local Korean bank account in KRW. PayPal also states that withdrawals of less than KRW 150,000 have a fee, while no withdrawal fee applies when the KRW withdrawal amount is KRW 150,000 or more. Currency conversion may still affect the received amount.

Operational recommendation:

- Use one dedicated Korean bank account for PayPal withdrawals.
- Do not mix PayPal education revenue with personal living transactions where possible.
- Do not withdraw every USD 39 payment one by one unless cashflow requires it.
- Batch withdrawals after the PayPal KRW amount exceeds KRW 150,000 where practical.
- Save the PayPal withdrawal confirmation and Korean bank deposit record.
- Record the withdrawal date, KRW received amount, and exchange/conversion reference in the Revenue Ledger.

Official PayPal references:

- https://www.paypal.com/kr/cshelp/article/how-do-i-withdraw-funds-from-my-paypal-account-help394
- https://www.paypal.com/kr/digital-wallet/paypal-consumer-fees

## Evidence to Save Monthly

Save these files every month:

- PayPal monthly statement, CSV or PDF
- PayPal transaction detail for each payment
- PayPal withdrawal confirmation
- Korean bank deposit record after withdrawal
- Google Form response row
- Service delivery proof, such as Telegram activation date or client status
- Telegram bot/channel/service notice screenshots
- Starter curriculum/service description at the time of payment
- Refund/cancellation record if applicable

Recommended folder naming:

```text
Finance/PayPal/2026-05/
Finance/PayPal/2026-06/
```

## Revenue Ledger Columns

Maintain a separate Google Sheet tab named `Revenue Ledger`.

Recommended columns:

```text
Month
Payment Date
PayPal Transaction ID
PayPal Payer Email
Customer Email
Customer Country
Product
Currency
Gross Amount
PayPal Fee
Net Amount
Payment Status
Service Status
Operator Registration Status
VAT Review Type
Zero-rate Review
FX Date
FX Source
KRW Revenue Amount
Withdrawal Date
KRW Received
PayPal Statement Saved
Order/Application Evidence Saved
Telegram Activation Evidence Saved
Tax Review Status
Evidence Folder
Business Registration Review
Notes
```

## Non-Registered Launch Stage Tax Handling

Because the current launch status is non-registered individual / pre-business-registration, the practical first goal is clean evidence collection and annual income tax preparation.

Recommended handling:

- Record every PayPal payment in USD.
- Record the official or chosen FX basis consistently.
- Record actual KRW deposit when PayPal funds are withdrawn.
- Save evidence that the money came from Telegram-based MEP BIM education service.
- Prepare to report the income in the next annual individual income tax filing period.
- Ask a tax professional whether the income should be treated as business income or other income based on actual operation.

Important:

- PayPal screenshots alone are weaker than full PayPal statements and bank records.
- Repeated, continuous revenue may indicate business activity even before formal business registration.
- If the service becomes regular and meaningful in size, review business registration.

## VAT and Future Business Registration Review

Important future operating rule:

Do not assume every PayPal payment is automatically zero-rated export revenue.

Review at least:

- Whether the customer is overseas or domestic
- Whether the service qualifies as an export or foreign-currency-earning service
- Whether the customer has a domestic place of business
- Whether supporting documents are sufficient
- Whether the service is educational content, digital content, consulting, or another category

Suggested internal status values:

```text
needs_review
likely_zero_rate
domestic_vat_review
not_zero_rate
tax_advisor_confirmed
```

At the current non-registered launch stage, use `needs_review` by default for VAT-related columns unless a tax professional confirms otherwise.

## Income Tax or Corporate Tax

PayPal revenue should be reviewed for annual individual income tax reporting while operating as a non-registered individual.

For KRW bookkeeping, record the basis used consistently:

- payment date amount and exchange rate; or
- withdrawal/conversion date amount and bank deposit record

The final method should be confirmed with the accountant/tax advisor and then used consistently.

## Monthly Revenue Manager Checklist

1. Download PayPal monthly statement.
2. Match every PayPal payment to a Google Form row.
3. Check missing application rows for paid customers.
4. Check submitted applications without payment.
5. Update `Payment Verified`.
6. Update `Revenue Ledger`.
7. Save withdrawal and bank records.
8. Mark evidence saved columns.
9. Review refund or cancellation cases.
10. Save Telegram service evidence.
11. Review whether business registration is becoming necessary.
12. Send unresolved items to tax/accounting review.

## Business Registration Review Triggers

Review business registration when one or more are true:

- Payments become regular and repeated.
- Monthly revenue becomes meaningful and stable.
- You want cleaner expense handling for software, equipment, tools, and content production.
- You need formal invoices, business identity, or stronger customer trust.
- You want to formally review VAT zero-rate treatment for overseas education/service revenue.

## Risk Controls

- Do not activate service without payment verification.
- Do not treat PayPal balance as final KRW revenue without recording exchange/conversion handling.
- Do not rely only on screenshots when CSV/PDF statements are available.
- Do not mix customer private information into public Obsidian product knowledge.
- Keep domestic customer cases separately reviewable.

# Autodesk Store Actual Submission Workflow

- Date checked: 2026-05-19
- Product: BIM Command Center for Revit
- Recommended first-release licensing path: Autodesk App Store Subscription + Entitlement API

## 1. Publisher Setup

1. Go to Autodesk Marketplace Publisher Center.
2. Enter Publisher Corner.
3. Complete publisher information.
4. Set publisher email for automated download/review notifications.
5. Set support contact for end users.
6. Configure publisher profile page and company logo.

Notes:

- Publisher settings apply across apps, not only one product.
- Support contact must be ready before publishing.
- Autodesk review communication may use the publisher email.

## 2. Payment Setup

Autodesk Store paid apps can use payment processors such as PayPal and BlueSnap.

### PayPal path

- Use a PayPal Business or Premier account.
- Configure the PayPal account email in Publisher Corner.
- Use the master PayPal email address as the PayPal account in Autodesk Store.
- IPN listener is optional if using Entitlement API only.

### BlueSnap path

If using BlueSnap:

- Configure payment methods in BlueSnap.
- Create/copy the BlueSnap Data Protection Key.
- Enable subscription reminder emails if desired.
- Create BlueSnap API credentials.
- Add Autodesk-required IP ranges in BlueSnap API settings.
- Enter BlueSnap data protection key and API credentials in Autodesk Publisher Corner.

Important:

- BlueSnap Data Protection Key and API credentials are production secrets.
- Do not commit these values to source code or documentation.

## 3. Create New Product

1. Click `Publish a New Product`.
2. Accept the publisher agreement.
3. Select app type: Desktop based app.
4. Select operating system.
5. Select language.
6. Save as draft if the build or assets are not complete.

For BIM Command Center first release:

- App type: Desktop based app
- OS: Windows
- Language: English first, Korean later if desired

## 4. Fill App Submission Form

Use the prepared values from `STORE_FORM_FIELD_VALUES.md`.

Required material:

- Product name
- App description
- Install/uninstall text
- Support information
- App file or cloud file link
- App icon
- Screenshots
- Optional YouTube demo video
- Compatibility products and versions
- Categories
- Price type and price

Autodesk documentation notes:

- App description can be long and may include formatting, bullets and links.
- App file can be an installer, zipped app files or PDF files.
- Icon recommendation is 120x120 pixels.
- Up to 10 screenshots can be uploaded.
- Screenshot recommendation: up to 2000 x 2000 px, 72/96 DPI, max 20 MB.
- Price value should be numeric only.
- Prices are in USD.

## 5. Subscription Setup

For monthly or yearly subscription:

1. Select `Subscription` as the price type.
2. Enter numeric price only.
3. Decide monthly or yearly subscription offering in the Store flow.
4. Enable 30-day free trial if desired.
5. Make sure Entitlement API is integrated before enabling trial/subscription unlock.

Important:

- Autodesk documentation says payment type cannot be changed once `Subscription` is selected.
- A 30-day free trial for Paid or Subscription apps requires Autodesk App Store Entitlement API integration.

Recommended BIM Command Center price:

- Individual: USD 19/month or USD 190/year
- Team 5-Pack: USD 79/month or USD 790/year if the Store/payment workflow supports a separate product or contract
- Enterprise: direct custom sales outside the simple Store listing flow

## 6. Subscription Handling Choice

Autodesk describes two mechanisms for desktop app subscription handling:

1. Entitlement API
2. Custom web service consuming PayPal IPN notifications relayed by Autodesk Store

### Recommended for first release

Use Entitlement API only.

Why:

- Simplest option.
- No custom payment backend required.
- No custom user database required.
- Lower privacy and security risk.
- Fits current BIM Command Center implementation.

### Do not use yet

Do not build a custom IPN/payment backend for v1.0.

Custom IPN backend is useful only if we later need:

- Internal CRM/accounting automation
- Custom account portal
- Machine locking
- Advanced usage analytics
- Multi-seat enterprise management beyond Store entitlement

## 7. Compatibility Selection

Only select Autodesk products and versions actually tested.

For first release target:

- Autodesk Revit 2024
- Autodesk Revit 2025
- Autodesk Revit 2026

Autodesk documentation says compatibility means:

- The publisher tested the app with that product.
- The publisher can support customers using the app with that product.

Do not select Revit 2027 until QA evidence exists.

## 8. Preview And Submit

1. Review summary screen.
2. Click Preview.
3. Check how the app page looks in the Store.
4. Go back and fix text, screenshots, compatibility or price if needed.
5. Submit.

Autodesk documentation says reviewers usually contact publishers after submission. Use `appsubmissions@autodesk.com` if there is no response after the expected review window.

## 8.1 Automation Boundary

No public Autodesk App Store submission API or upload CLI was found in the checked documentation. For v1.0, automate local package preparation only and keep Publisher Center upload/preview/submit manual.

Use:

`scripts/prepare_autodesk_store_upload_package.py`

## 9. After Submission

After app is submitted/reviewed:

- Store App ID becomes important for Entitlement API.
- Insert the App ID into `license-settings.json`.
- Rebuild release DLLs and installer.
- Test entitlement with a Store/test account.
- Verify download/test purchase flow before public launch.

## 10. Test Purchase

Autodesk documentation describes a test purchase flow from the unpublished app preview page for paid apps. It may involve a small test charge, so verify payment setup before using it.

Use test purchase to validate:

- Store payment flow
- Download availability
- Entitlement response
- Installer package
- User support instructions

## 11. Operational Policy For BIM Command Center

For v1.0:

- Store handles purchase and subscription billing.
- PayPal/BlueSnap handle payment method details.
- BIM Command Center checks entitlement only.
- LUA BIM LABS support handles installation, loading and entitlement error troubleshooting.
- Billing, card, cancellation and payment processor issues should be directed to Autodesk Store/PayPal/BlueSnap support flows.

## Sources

- Autodesk Marketplace Publisher Center: https://aps.autodesk.com/app-store/publisher-center
- Autodesk desktop app submission guide: https://www.autodesk.com/content/dam/autodesk/www/adn/pdf/desktop-app-submission-process-overview.pdf
- Autodesk desktop subscription guide: https://damassets.autodesk.net/content/dam/autodesk/www/adn/pdf/selling-desktop-app-on-monthly-subscription.pdf
- Autodesk BlueSnap settings guide: https://apps.autodesk.com/en/Public/BlueSnapDetailSettings
- Autodesk App Store FAQ: https://apps.autodesk.com/EN/Public/FAQ

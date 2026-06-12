# Subscription Account And Payment Risk

- Date: 2026-05-19
- Product: BIM Command Center for Revit

## Summary

Using Autodesk App Store subscription reduces direct payment risk because payment collection is handled through Autodesk App Store payment flows and supported processors such as PayPal or BlueSnap. BIM Command Center should not collect or store credit card numbers, bank details or payment credentials.

The add-in should only verify subscription entitlement through Autodesk App Store Entitlement API.

## What We Should Store

Keep this minimal:

- Autodesk App Store App ID
- Autodesk login user identifier returned by Revit for entitlement check
- Entitlement check timestamp
- Entitlement result: valid or invalid
- Non-sensitive support ticket information if the user contacts support

## What We Should Not Store

Do not store:

- Credit card number
- CVV
- Bank account details
- PayPal password or BlueSnap credentials
- Full payment method details
- Customer project model files unless explicitly needed for support
- Machine ID, MAC address, CPU ID, phone number or personal email for license activation

## Payment And Account Ownership

Autodesk App Store supports paid app purchase through PayPal and BlueSnap. Customers may be redirected to PayPal or BlueSnap for purchase/payment. Subscription cancellation is handled through PayPal or BlueSnap shopper/subscription account flows.

LUA BIM LABS should direct billing, card, cancellation and failed payment issues to the appropriate payment platform or Autodesk App Store support when the issue is outside the add-in.

## Publisher-Side Sensitive Data

If using BlueSnap or PayPal publisher settings, publisher credentials, API keys, data protection keys and IPN listener secrets must be treated as production secrets.

Rules:

- Do not commit payment credentials to source code.
- Do not put payment credentials in screenshots or support tickets.
- Store credentials only in the relevant payment processor / Autodesk Publisher Corner configuration.
- If an IPN listener is added later, verify messages and log only minimal non-sensitive fields.

## IPN / Payment Notification Data

Autodesk subscription documentation indicates IPN-style notifications can include subscription and payment identifiers such as app name, subscription ID, payment ID and payment date. If we later build an IPN listener, treat those as business records and personal data adjacent.

Minimum controls:

- HTTPS-only endpoint
- Signature or source validation where available
- No card data logging
- Access-restricted logs
- Retention policy
- Support process for deletion/account questions

## Privacy Policy Implications

The privacy policy should say:

- Core Revit commands run locally.
- Subscription entitlement requires internet access.
- Entitlement check uses Autodesk login user identifier and Store App ID.
- Payment method details are handled by Autodesk App Store payment processors, not by the add-in.
- Support requests may include contact details supplied by the user.

## Support Implications

Support can help with:

- Add-in installation
- Revit loading
- Entitlement check error screenshots
- App version and compatibility

Support should not ask for:

- Card number
- CVV
- PayPal password
- BlueSnap password
- Autodesk account password

## Practical Recommendation

For first release:

- Use Autodesk App Store subscription + Entitlement API.
- Do not build a custom payment backend.
- Do not build an IPN listener unless needed for internal CRM/accounting automation.
- Keep support and privacy language clear that billing is handled through the Store/payment processor flow.
- Decide PayPal or BlueSnap in Publisher Corner before launch.
- Treat payment processor keys and API credentials as production secrets.

## Official References

- Autodesk App Store FAQ: https://apps.autodesk.com/EN/Public/FAQ
- Autodesk Publisher Center: https://aps.autodesk.com/app-store/publisher-center
- Autodesk desktop app subscription guide: https://damassets.autodesk.net/content/dam/autodesk/www/adn/pdf/selling-desktop-app-on-monthly-subscription.pdf
- Autodesk App Store Terms of Use: https://apps.autodesk.com/Content/pdf/TOU.pdf
- Autodesk BlueSnap settings: https://apps.autodesk.com/en/Public/BlueSnapDetailSettings
- BlueSnap subscription capabilities: https://support.bluesnap.com/docs/subscription-options

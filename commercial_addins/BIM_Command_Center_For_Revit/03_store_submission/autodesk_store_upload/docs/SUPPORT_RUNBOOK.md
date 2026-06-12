# Support Runbook

## Product

BIM Command Center for Revit

## Support Promise

Recommended public promise:

- Response within 2 business days
- Support by email
- Critical install/licensing issues prioritized first

## Required Customer Information

Ask the customer for:

- Revit version
- Windows version
- Product version
- Installation path if known
- Screenshot of error message
- Whether the model is local, central or cloud workshared
- Steps to reproduce the issue

Do not ask for the customer model unless absolutely necessary. If a model is needed, request a stripped sample model first.

## Common Issue Categories

### Add-in does not load

- Check `.addin` file location.
- Check assembly path.
- Check missing DLL dependencies.
- Check blocked files downloaded from internet.
- Check Revit version compatibility.

### License activation problem

- Confirm user email or license ID.
- Confirm whether machine was replaced.
- Reset activation if policy allows.
- Never ask the customer to send private machine identifiers in public channels.

### Subscription or payment problem

- Confirm whether the problem is add-in entitlement, Store download, payment failure, cancellation or refund.
- For entitlement checks, ask for Revit version, Autodesk login status and a screenshot of the add-in message.
- For card, PayPal, BlueSnap, cancellation or billing issues, direct the customer to the relevant Autodesk App Store, PayPal or BlueSnap support flow.
- Never ask for card number, CVV, PayPal password, BlueSnap password or Autodesk account password.

### Dashboard panel is blank

- Confirm WebView2 runtime is installed.
- Confirm local dashboard service is running if required.
- Confirm firewall or antivirus is not blocking local communication.
- Confirm the product can run without external AI services if those are disabled.

### Command fails on a model

- Ask for Revit journal excerpt if possible.
- Ask whether the model is workshared.
- Ask for element/category/view context.
- Reproduce on sample model before requesting customer files.

## Release Hotfix Rules

- Patch install/load/license failures first.
- Avoid adding new features in hotfix builds.
- Keep release notes short and factual.
- Re-test all supported Revit versions before publishing the hotfix.

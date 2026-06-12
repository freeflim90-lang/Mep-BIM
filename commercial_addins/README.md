# Commercial Addins

This directory is the commercial release workspace.

Development source stays outside this operational repository. Store packaging, release inputs, QA evidence, legal drafts and customer support materials are managed here so commercial releases do not get mixed with personal development folders.

## Products

- `BIM_Command_Center_For_Revit`

## Rules

- Do not edit development source from this folder.
- Point source-writing automation at the external add-in development root with `BCC_ADDIN_DEV_SOURCE_ROOT`.
- Keep final installers, icons, screenshots and QA evidence here.
- Archive every submitted Store package.
- Do not store payment processor credentials, Autodesk passwords or customer payment information.
- Store App ID can be documented, but payment secrets must stay in Autodesk/PayPal/BlueSnap admin systems.

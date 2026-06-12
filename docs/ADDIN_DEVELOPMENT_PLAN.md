# LUA BIM LABS Add-in Development Mission

## Mission

Use the AI dashboard as an execution console for Revit and Navisworks add-in development. The dashboard should receive tasks, route them to the right virtual agent, stream progress, and produce implementation-ready output.

## Target Products

- Revit add-ins: C#/.NET commands and applications using the Autodesk Revit API.
- Navisworks add-ins: C#/.NET plugins using the Navisworks product SDK/API installed with Navisworks Manage or Simulate.
- Dashboard integration: development requests can arrive from Telegram or the browser dashboard.

## Current Routing

- `요구사항분석`: feature scope, user story, risk, API feasibility.
- `Revit_Addin`: Revit API command/application design, manifest structure, model element access.
- `Navisworks_Addin`: Navisworks plugin design, clash/review workflow, model coordination support.
- `빌드검증`: build, smoke test, manual verification checklist.
- `배포문서`: installer, `.addin` manifest, user guide, release notes.
- `제품패키징`: installer/MSI, versioned package, uninstall/update behavior.
- `스토어심사`: Autodesk App Store submission readiness and rejection risk checks.
- `라이선스결제`: paid/subscription model, entitlement, payment-provider readiness.
- `고객지원 CS`: support email, privacy policy, refund/support workflow, issue triage.

## Discipline Knowledge Review

Every commercial add-in request should include a discipline scope. The dashboard routes the implementation task to the add-in team and then asks the relevant BIM discipline agents to review the feature requirements.

- `건축`: room/space, ceiling height, fire compartment, finish, opening and layout constraints.
- `구조`: beam, column, slab, opening, sleeve, reinforcement and penetrations.
- `토목`: external utilities, site boundary, GL/FL relationship and civil tie-ins.
- `위생`: supply/drainage slope, fixture, pump and sanitary pipe rules.
- `공조배관`: chilled/hot water, refrigerant, valve, insulation and maintenance clearance.
- `공조덕트`: duct size, airflow, static pressure, smoke exhaust and routing constraints.
- `소방기계`: sprinkler coverage, fire pipe, head spacing and code-sensitive routing.
- `소방전기`: detectors, fire alarm wiring, panel and emergency signal coordination.
- `전기`: tray, feeder, panel, clearance, leakage avoidance and strong-power separation.
- `통신`: low-voltage tray, network, CCTV, broadcasting and EMI separation.
- `MEP통합`: routes all MEP discipline opinions.
- `전체공정`: routes architectural, structural, civil and MEP opinions.

The final PM report must preserve these discipline opinions as product requirements, not as loose comments.

## Knowledge Update Loop

Each discipline agent has a local markdown knowledge base under `knowledge/10_agents/`.

The intended loop is:

- Update a discipline knowledge base from the dashboard before or during product planning.
- Store the update with title, source, tags and timestamp.
- When an Add-in development task runs, infer the relevant discipline agents.
- Load each relevant discipline knowledge base into the review prompt.
- Preserve the resulting discipline opinions in the final PM report.

This makes discipline advice cumulative instead of relying only on the model's general prior knowledge.

## Initial AI Knowledge Seeding

The `scripts/seed_ai_knowledge.py` script seeds role-specific knowledge for:

- management agents
- discipline agents
- Revit/Navisworks development agents
- QA, documentation, packaging and App Store commercialization agents
- token, security and pipeline support agents

Run it again when a new baseline packet is added. Existing packet titles are not duplicated.

## Revit Add-in Baseline

- Revit add-ins need registration through an `.addin` manifest.
- Command-style tools should be modeled around `IExternalCommand`.
- Application lifecycle tools should be modeled around `IExternalApplication`.
- The add-in must handle cases where there is no active document if the command can appear in that state.

## Navisworks Add-in Baseline

- Navisworks API documentation and samples are installed with Navisworks Manage/Simulate under the product API folder.
- Coordination workflows should assume Navisworks 2020 or later when relying on modern coordination issue add-in behavior.
- Navisworks 2026 includes API surface updates such as `NwdExportOptions`, so version-specific capability checks matter.

## Immediate Next Build Step

Create a first scaffold generator that emits:

- `src/RevitAddin/`
- `src/NavisworksAddin/`
- manifest templates
- build notes
- smoke-test checklist

The dashboard should eventually trigger this generator and stream file creation results back through `/ws/office`.

## Autodesk App Store Commercialization Baseline

Official Autodesk guidance makes commercialization part of the product, not a final afterthought:

- Review Autodesk App Store Product Guidelines before submitting.
- Prepare publisher account details and app listing assets.
- For paid products, prepare a PayPal account and price.
- Provide a publisher privacy policy.
- Provide a customer support email address for the product page.
- Check whether APS Client ID or cloud product URL is needed for BIM 360, Forma, or APS-connected workflows.
- Ensure the add-in does not crash or significantly slow down Autodesk products.
- Package installation so a customer can install, uninstall, and understand compatibility without developer assistance.
- Show product compatibility clearly by Autodesk product and version.

## Store Submission Checklist

- Product name, short description, long description.
- Screenshots and optional video.
- Supported Autodesk product versions.
- Installer package or plugin package.
- Privacy policy URL.
- Support email address.
- Paid/free/subscription pricing decision.
- License or entitlement flow.
- Trial behavior if offered.
- User documentation and first-run instructions.
- Smoke-test evidence for each supported Revit/Navisworks version.
- Crash/performance risk notes.
- Known limitations.

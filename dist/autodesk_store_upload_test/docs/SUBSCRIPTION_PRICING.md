# Subscription Pricing Strategy

- Date: 2026-05-19
- Product: BIM Command Center for Revit
- Currency for Autodesk App Store: USD
- Working KRW assumption: about 1 USD = 1,500 KRW, for internal Korean planning only.

## Recommendation

Launch with three subscription products:

| Plan | Monthly | Annual | Target |
|---|---:|---:|---|
| Individual | USD 19/month | USD 190/year | Freelance BIM users and small teams |
| Team 5-Pack | USD 79/month | USD 790/year | Small BIM/MEP teams |
| Enterprise | Custom | Custom | Firms needing deployment, training and multi-seat support |

## First Release Price

Recommended first Autodesk Store price:

**USD 19/month or USD 190/year per user**

This is high enough to position the product as a professional BIM productivity tool, but low enough for early adoption while the brand, support process and review history are still being built.

Approximate Korean planning value:

- USD 19/month: about KRW 28,500/month
- USD 190/year: about KRW 285,000/year
- USD 79/month team pack: about KRW 118,500/month
- USD 790/year team pack: about KRW 1,185,000/year

Actual billing should remain USD in Autodesk App Store materials.

## Why This Price

Observed Revit add-in pricing varies widely:

- Simple single-purpose tools often appear around USD 5-10/month.
- Many useful Revit productivity or MEP tools appear around USD 10-15/month.
- More specialized workflow/integration tools can reach about USD 29/month or higher.
- Deep vertical products can be far above this, but they need mature support, documentation and proven ROI.

BIM Command Center is a multi-tool dashboard, so it can be priced above a single small command. However, the first public release still needs user trust, support evidence and review history. USD 19/month is the best opening point.

## Launch Promotion

Recommended:

- 30-day free trial through Autodesk Entitlement API.
- First 3 months at USD 12/month for early adopters if the Store payment flow allows coupons or manual promotion.
- Keep annual plan at USD 190/year to reward commitment.

If coupon/promotion mechanics are difficult, use the 30-day trial only and keep the regular price.

## Upgrade Path

### Version 1.0

USD 19/month, USD 190/year

Includes local productivity modules:

- Dashboard launcher
- Model Health Dashboard
- Workset Dashboard
- Auto Save / Auto Sync
- MEP Splitter
- Clash point and view utilities
- Unit conversion, after validation

### Version 1.5

Keep price or raise to USD 24/month after:

- Stable installer and support process
- 10+ paying users or several positive reviews
- Revit 2027 compatibility
- Better documentation and demo videos

### Version 2.0

Keep the same three-product structure unless customer demand proves a separate premium tier is necessary. AI/cloud/reporting features should be added only after privacy, support and operating cost controls are complete.

## Revenue Targets

| Paid users | Individual monthly MRR | Annualized |
|---:|---:|---:|
| 10 | USD 190 | USD 2,280 |
| 25 | USD 475 | USD 5,700 |
| 50 | USD 950 | USD 11,400 |
| 100 | USD 1,900 | USD 22,800 |

Team plans can raise average revenue per account faster than individual plans, but they require clearer support and license management.

## Commercial Package Exclusion

The first commercial package excludes `RevitAddin.MepBim`. It should not appear in the dashboard command list, installer payload, Store listing feature list or entitlement rules.

## Store Implementation Notes

- Autodesk submission accepts a Subscription payment type for apps.
- Price should be entered as a numeric USD value.
- Once Subscription is selected, payment type may not be changeable for that app record.
- Paid or Subscription apps can offer a free 30-day trial, but the add-in needs Autodesk App Store Entitlement API integration.
- The app should check subscription entitlement before unlocking paid commands.
- Autodesk describes Entitlement API as the simplest first-release subscription handling option when the app should not require a custom backend.

## Final Price To Use In Store Draft

Use this for the first submission:

- Payment type: Subscription
- Trial: 30 days
- Monthly price: 19
- Annual price: 190

If annual pricing cannot be configured separately in the selected Store workflow, submit monthly first at USD 19/month and provide annual/team options through direct enterprise sales later.

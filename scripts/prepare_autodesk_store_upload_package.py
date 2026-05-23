#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "autodesk_store"
DEFAULT_OUT = ROOT / "commercial_addins" / "BIM_Command_Center_For_Revit" / "03_store_submission" / "autodesk_store_upload"
COMMERCIAL_PRODUCT = ROOT / "commercial_addins" / "BIM_Command_Center_For_Revit"

REQUIRED_DOCS = [
    "STORE_FORM_FIELD_VALUES.md",
    "BIM_COMMAND_CENTER_STORE_LISTING_DRAFT.md",
    "SUBSCRIPTION_PRICING.md",
    "PRIVACY_POLICY_DRAFT.md",
    "EULA_DRAFT.md",
    "USER_GUIDE_DRAFT.md",
    "SUPPORT_RUNBOOK.md",
    "SUPPORT_EMAIL_TEMPLATES.md",
    "RELEASE_NOTES_V1_0.md",
    "QA_SMOKE_TEST_PLAN.md",
    "SCREENSHOT_VIDEO_SHOTLIST.md",
    "ENTITLEMENT_API_IMPLEMENTATION.md",
    "SUBSCRIPTION_ACCOUNT_PAYMENT_RISK.md",
    "AUTODESK_STORE_ACTUAL_WORKFLOW.md",
    "UPLOAD_AUTOMATION_POLICY.md",
]

COMMERCIAL_HANDOFF_DOCS = [
    "04_qa_evidence/PHASE1_DRY_RUN_TEST_CHECKLIST.md",
    "08_feature_backlog/BIMLIZE_RIBBON_FEATURE_MATRIX.md",
    "08_feature_backlog/PHASE1_SIMPLE_FEATURES.md",
    "08_feature_backlog/BIMIZE_FEATURE_INTERNALIZATION.md",
]


def copy_file(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def make_zip(source_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in source_dir.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(source_dir.parent))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare a local Autodesk Store upload handoff package."
    )
    parser.add_argument("--installer", help="Path to final Windows installer/package.")
    parser.add_argument("--icon", help="Path to 120x120 product icon.")
    parser.add_argument("--screenshots", help="Directory containing Store screenshots.")
    parser.add_argument("--video", help="Path to demo video file or text file containing video URL.")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output directory.")
    args = parser.parse_args()

    out = Path(args.out).resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    manifest = {
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "product": "BIM Command Center for Revit",
        "upload_mode": "manual_autodesk_publisher_center",
        "docs": {},
        "assets": {},
        "missing": [],
        "manual_steps": [
            "Log in to Autodesk Publisher Center.",
            "Create or open the BIM Command Center product draft.",
            "Select Desktop based app, Windows, English.",
            "Select Subscription only after confirming price.",
            "Upload installer/package manually.",
            "Upload icon, screenshots and video URL manually.",
            "Preview Store page.",
            "Submit manually.",
        ],
    }

    docs_out = out / "docs"
    for name in REQUIRED_DOCS:
        ok = copy_file(DOCS / name, docs_out / name)
        manifest["docs"][name] = "included" if ok else "missing"
        if not ok:
            manifest["missing"].append(f"doc:{name}")

    handoff_out = out / "commercial_handoff"
    for name in COMMERCIAL_HANDOFF_DOCS:
        ok = copy_file(COMMERCIAL_PRODUCT / name, handoff_out / name)
        manifest["docs"][f"commercial:{name}"] = "included" if ok else "missing"
        if not ok:
            manifest["missing"].append(f"commercial_doc:{name}")

    assets_out = out / "assets"

    if args.installer:
        src = Path(args.installer).expanduser().resolve()
        ok = copy_file(src, assets_out / "installer" / src.name)
        manifest["assets"]["installer"] = str(src) if ok else "missing"
        if not ok:
            manifest["missing"].append(f"installer:{src}")
    else:
        manifest["missing"].append("installer")

    if args.icon:
        src = Path(args.icon).expanduser().resolve()
        ok = copy_file(src, assets_out / "icon" / src.name)
        manifest["assets"]["icon"] = str(src) if ok else "missing"
        if not ok:
            manifest["missing"].append(f"icon:{src}")
    else:
        manifest["missing"].append("icon")

    if args.screenshots:
        screenshots_dir = Path(args.screenshots).expanduser().resolve()
        if screenshots_dir.exists():
            count = 0
            for src in screenshots_dir.iterdir():
                if src.is_file() and src.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                    copy_file(src, assets_out / "screenshots" / src.name)
                    count += 1
            manifest["assets"]["screenshots"] = count
            if count == 0:
                manifest["missing"].append("screenshots:no image files")
        else:
            manifest["missing"].append(f"screenshots:{screenshots_dir}")
    else:
        manifest["missing"].append("screenshots")

    if args.video:
        src = Path(args.video).expanduser().resolve()
        ok = copy_file(src, assets_out / "video" / src.name)
        manifest["assets"]["video"] = str(src) if ok else args.video
    else:
        manifest["missing"].append("video")

    manifest_path = out / "UPLOAD_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    zip_path = out.with_suffix(".zip")
    make_zip(out, zip_path)

    print(f"Prepared: {out}")
    print(f"ZIP: {zip_path}")
    if manifest["missing"]:
        print("Missing:")
        for item in manifest["missing"]:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

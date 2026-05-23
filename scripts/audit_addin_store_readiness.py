import csv
import datetime
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "260519 소스 폴더"
REPORT_DIR = PROJECT_ROOT / "docs" / "autodesk_store"


def text_or_empty(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def first_xml_value(path: Path, tag: str) -> str:
    text = text_or_empty(path)
    match = re.search(rf"<{tag}>(.*?)</{tag}>", text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


def read_csproj_metadata(path: Path) -> dict:
    text = text_or_empty(path)
    frameworks = re.findall(r"<TargetFrameworks?>(.*?)</TargetFrameworks?>", text, re.IGNORECASE)
    revit_versions = sorted(set(re.findall(r"Revit\s*(20\d{2})", text, re.IGNORECASE)))
    navis_versions = sorted(set(re.findall(r"Navisworks(?:\s+Manage)?\s*(20\d{2})", text, re.IGNORECASE)))
    package_refs = re.findall(r'<PackageReference\s+Include="([^"]+)"\s+Version="([^"]+)"', text)
    project_refs = re.findall(r'<ProjectReference\s+Include="([^"]+)"', text)
    hint_paths = re.findall(r"<HintPath>(.*?)</HintPath>", text, re.IGNORECASE | re.DOTALL)
    return {
        "frameworks": "; ".join(frameworks),
        "assembly": first_xml_value(path, "AssemblyName"),
        "revit_versions": ", ".join(revit_versions),
        "navis_versions": ", ".join(navis_versions),
        "package_refs": "; ".join(f"{name} {version}" for name, version in package_refs),
        "project_refs": "; ".join(project_refs),
        "hint_paths": "; ".join(h.strip() for h in hint_paths[:8]),
        "has_revit_api": "RevitAPI" in text,
        "has_navisworks_api": "Navisworks" in text,
        "has_postbuild_deploy": any(token in text for token in ["PostBuild", "$(APPDATA)", "Autodesk\\Revit\\Addins"]),
    }


def read_addin_metadata(path: Path) -> dict:
    text = text_or_empty(path)
    return {
        "addin_type": first_xml_value(path, "AddInId") and first_xml_value(path, "FullClassName"),
        "assembly_path": first_xml_value(path, "Assembly"),
        "addin_id": first_xml_value(path, "AddInId"),
        "full_class": first_xml_value(path, "FullClassName"),
        "vendor_id": first_xml_value(path, "VendorId"),
        "vendor_description": first_xml_value(path, "VendorDescription"),
        "text": text,
    }


def score_product(product: dict) -> tuple[int, list[str], list[str]]:
    score = 0
    blockers = []
    actions = []

    if product["csproj_count"]:
        score += 15
    else:
        blockers.append("No csproj found")

    if product["addin_count"]:
        score += 15
    else:
        actions.append("Create or locate .addin/plugin manifest")

    if product["installer_count"]:
        score += 15
    else:
        actions.append("Create customer-friendly installer/uninstaller")

    if product["readme_count"]:
        score += 10
    else:
        actions.append("Write README/user guide")

    if product["has_license_code"]:
        score += 10
    else:
        actions.append("Define licensing/trial behavior")

    if product["has_tests"]:
        score += 10
    else:
        actions.append("Add smoke/regression test checklist")

    if product["hardcoded_user_paths"]:
        blockers.append("Hardcoded local/user paths in manifests or projects")
    else:
        score += 10

    if product["broken_project_refs"]:
        blockers.append("Suspicious ProjectReference path")
    else:
        score += 5

    if product["platform"] in ("Revit", "Navisworks"):
        score += 5

    if product["latest_version_hint"]:
        score += 5
    else:
        actions.append("Verify latest supported Autodesk version")

    return min(score, 100), blockers, actions


def product_dirs() -> list[tuple[str, Path]]:
    roots = [
        ("Revit", SOURCE_ROOT / "01_Revit_Addins"),
        ("Navisworks", SOURCE_ROOT / "02_Navisworks_Tools"),
    ]
    products = []
    for platform, root in roots:
        if not root.exists():
            continue
        for child in sorted(root.iterdir()):
            if child.is_dir() and not child.name.startswith("."):
                products.append((platform, child))
    return products


def audit_product(platform: str, path: Path) -> dict:
    ignored_dirs = {"bin", "obj", ".vs", ".git"}
    files = [
        p for p in path.rglob("*")
        if p.is_file() and not any(part in ignored_dirs for part in p.parts)
    ]
    csprojs = [p for p in files if p.suffix.lower() == ".csproj"]
    addins = [p for p in files if p.suffix.lower() == ".addin"]
    slns = [p for p in files if p.suffix.lower() == ".sln"]
    readmes = [p for p in files if p.name.lower() == "readme.md"]
    installers = [
        p for p in files
        if p.suffix.lower() in (".iss", ".msi", ".exe")
        or "installer" in p.name.lower()
        or "setup" in p.name.lower()
        or p.name.lower().startswith(("install", "uninstall", "build_installer"))
    ]
    source_text = "\n".join(text_or_empty(p) for p in files if p.suffix.lower() in (".cs", ".csproj", ".addin", ".iss", ".ps1", ".bat", ".md"))
    cs_meta = [read_csproj_metadata(p) for p in csprojs]
    addin_meta = [read_addin_metadata(p) for p in addins]
    versions = sorted(set(
        v
        for meta in cs_meta
        for v in (meta["revit_versions"] + ", " + meta["navis_versions"]).split(", ")
        if v
    ))
    hardcoded_user_paths = any(
        token in source_text
        for token in ["C:\\Users\\", "Desktop\\", "\\개발 소스\\", "/Users/"]
    )
    broken_project_refs = any("......" in meta["project_refs"] or "..CommonJY" in meta["project_refs"] for meta in cs_meta)
    product = {
        "platform": platform,
        "name": path.name,
        "path": str(path.relative_to(PROJECT_ROOT)),
        "sln_count": len(slns),
        "csproj_count": len(csprojs),
        "addin_count": len(addins),
        "installer_count": len(installers),
        "readme_count": len(readmes),
        "frameworks": "; ".join(sorted(set(m["frameworks"] for m in cs_meta if m["frameworks"]))),
        "versions": ", ".join(versions),
        "vendor_ids": ", ".join(sorted(set(m["vendor_id"] for m in addin_meta if m["vendor_id"]))),
        "assemblies": "; ".join(sorted(set(m["assembly_path"] for m in addin_meta if m["assembly_path"]))[:5]),
        "has_license_code": "License" in source_text or "Entitlement" in source_text,
        "has_tests": any("test" in str(p).lower() for p in files),
        "has_external_api_or_network": any(token in source_text for token in ["HttpClient", "WebRequest", "api.openai", "localhost", "http://", "https://"]),
        "hardcoded_user_paths": hardcoded_user_paths,
        "broken_project_refs": broken_project_refs,
        "latest_version_hint": any(v in versions for v in ["2026", "2025"]),
        "packages": "; ".join(sorted(set(pkg for m in cs_meta for pkg in m["package_refs"].split("; ") if pkg)))[:600],
        "notes": "",
    }
    score, blockers, actions = score_product(product)
    product["readiness_score"] = score
    product["blockers"] = "; ".join(blockers)
    product["next_actions"] = "; ".join(actions)
    if product["has_external_api_or_network"]:
        product["next_actions"] = (product["next_actions"] + "; " if product["next_actions"] else "") + "Prepare privacy policy/network disclosure"
    return product


def write_reports(products: list[dict]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = REPORT_DIR / "addin_inventory.csv"
    fieldnames = [
        "platform", "name", "path", "readiness_score", "blockers", "next_actions",
        "sln_count", "csproj_count", "addin_count", "installer_count", "readme_count",
        "frameworks", "versions", "vendor_ids", "assemblies", "has_license_code",
        "has_tests", "has_external_api_or_network", "hardcoded_user_paths",
        "broken_project_refs", "latest_version_hint", "packages"
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            writer.writerow({key: product.get(key, "") for key in fieldnames})

    ranked = sorted(products, key=lambda p: p["readiness_score"], reverse=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Autodesk Store Readiness Audit",
        "",
        f"- Generated: {now}",
        f"- Source: `{SOURCE_ROOT.name}`",
        f"- Products scanned: {len(products)}",
        "",
        "## Recommended Launch Order",
        "",
    ]
    for idx, product in enumerate(ranked[:10], 1):
        lines.append(
            f"{idx}. **{product['name']}** ({product['platform']}) - score {product['readiness_score']}/100"
        )
        if product["blockers"]:
            lines.append(f"   - Blockers: {product['blockers']}")
        if product["next_actions"]:
            lines.append(f"   - Next: {product['next_actions']}")
    lines.extend([
        "",
        "## Product Inventory",
        "",
        "| Platform | Product | Score | Versions | Installer | README | License | Blockers |",
        "|---|---:|---:|---|---:|---:|---:|---|",
    ])
    for product in ranked:
        lines.append(
            f"| {product['platform']} | {product['name']} | {product['readiness_score']} | "
            f"{product['versions'] or '-'} | {product['installer_count']} | {product['readme_count']} | "
            f"{'Y' if product['has_license_code'] else 'N'} | {product['blockers'] or '-'} |"
        )
    lines.extend([
        "",
        "## Store Submission Gate",
        "",
        "A product is not ready to submit until all of these are complete:",
        "",
        "- One clear product name and value proposition.",
        "- Installer and uninstaller tested on a clean Windows machine.",
        "- Revit/Navisworks latest supported version verified.",
        "- No hardcoded developer/local paths in manifests or project files.",
        "- No undocumented Autodesk API usage.",
        "- Privacy policy prepared if network, cloud, telemetry or customer model data is used.",
        "- Support email and user guide prepared.",
        "- Smoke-test evidence captured for each supported Autodesk version.",
        "- Listing screenshots and short demo video prepared.",
    ])
    (REPORT_DIR / "STORE_READINESS_AUDIT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    products = [audit_product(platform, path) for platform, path in product_dirs()]
    write_reports(products)
    print(f"audited {len(products)} products")
    print(REPORT_DIR / "STORE_READINESS_AUDIT.md")
    print(REPORT_DIR / "addin_inventory.csv")


if __name__ == "__main__":
    main()

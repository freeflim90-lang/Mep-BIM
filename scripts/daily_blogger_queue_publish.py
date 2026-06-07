#!/usr/bin/env python3
"""Publish one queued Blogger topic and delete it after successful upload."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import time
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from typing import Any

import urllib.request

from blogger_publish import load_credentials, resolve_blog_id


DEFAULT_BLOG_URL = "https://engineer250212.blogspot.com/"
DEFAULT_LABELS = ["MEP BIM", "LUA BIM LABS", "Revit MEP", "BIM Training"]
DEFAULT_LOCK_FILE = "runtime/blogger_queue_publish.lock"
DEFAULT_STATE_FILE = "runtime/blogger_daily_generation_state.json"
DEFAULT_DAILY_AGENT_PLIST = "/Users/choejeong-yeon/Library/LaunchAgents/com.luabimlab.daily-blogger-post.plist"
DEFAULT_DUPLICATE_WARN_DAYS = 30
DEFAULT_SERVICE_CONFIG = "config/personal_mep_bim_tutor_plans.json"


SEED_TOPICS: list[dict[str, Any]] = [
    {
        "slug": "001-mep-bim-coordination-language",
        "title": "MEP BIM as a Coordination Language, Not Just a 3D Model",
        "focus": "why MEP BIM connects design, construction, commissioning, and facility management teams",
        "case_example": "A duct route may look correct in isolation, but it can fail when ceiling height, lighting, sprinkler, cable tray, and access panel requirements are reviewed together.",
        "checklist": ["Confirm system intent before modeling", "Review ceiling space by zone", "Track owner discipline for each issue"],
    },
    {
        "slug": "002-insulation-thickness-clash-checks",
        "title": "Why Insulation Thickness Matters in MEP Clash Coordination",
        "focus": "how pipe and duct insulation changes the real coordination envelope",
        "case_example": "A chilled water pipe without modeled insulation may pass a visual check, but the installed outside diameter can conflict with nearby trays or ceiling frames.",
        "checklist": ["Check pipe outside diameter with insulation", "Separate hard clashes from clearance issues", "Record insulation assumptions in the model QA note"],
    },
    {
        "slug": "003-chilled-water-supply-return",
        "title": "How to Check Chilled Water Supply and Return Logic in Revit MEP",
        "focus": "basic CHWS and CHWR system logic for practical model review",
        "case_example": "If supply and return connections are mixed at AHU coils, schedules and flow data become unreliable even if the geometry looks clean.",
        "checklist": ["Verify CHWS and CHWR system names", "Check coil connector direction", "Compare schedule data with equipment tags"],
    },
    {
        "slug": "004-valve-maintenance-space",
        "title": "Valve Maintenance Space: A Small BIM Detail With Big Site Impact",
        "focus": "why operation and replacement space should be reviewed before construction",
        "case_example": "A valve can be modeled without clashes, but if the handle cannot be operated after ceiling installation, the BIM model has missed a real maintenance issue.",
        "checklist": ["Review handle swing and access direction", "Check nearby ceilings and walls", "Mark maintenance clearance issues separately"],
    },
    {
        "slug": "005-navisworks-clash-grouping",
        "title": "How to Group Navisworks Clashes for a Useful Coordination Meeting",
        "focus": "turning raw clash results into practical meeting actions",
        "case_example": "Two hundred individual clashes may represent one repeated routing issue. Grouping by zone, system, and cause makes the meeting faster.",
        "checklist": ["Group by location first", "Separate repeated issues from unique issues", "Assign one responsible owner per group"],
    },
    {
        "slug": "006-revit-mep-family-connectors",
        "title": "Common Revit MEP Family Connector Mistakes",
        "focus": "connector settings that affect system data, flow, and coordination quality",
        "case_example": "A pump family may look correct in 3D, but wrong connector classification can break system flow and schedule reliability.",
        "checklist": ["Check connector domain", "Check flow direction", "Test the family inside a sample system"],
    },
    {
        "slug": "007-mep-model-qa-checklist",
        "title": "A Practical MEP Model QA Checklist Before Coordination",
        "focus": "simple quality checks before sharing an MEP model with other disciplines",
        "case_example": "Many coordination meetings are delayed not by major design problems, but by inconsistent links, views, levels, and system naming.",
        "checklist": ["Check linked model positions", "Review warnings and disconnected elements", "Confirm view templates and worksets"],
    },
    {
        "slug": "008-electrical-tray-clearance",
        "title": "Electrical Tray Clearance in MEP BIM Coordination",
        "focus": "why cable tray routing must consider access, separation, and installation sequence",
        "case_example": "A cable tray may pass through a congested corridor but still block valve operation or reduce space for duct insulation.",
        "checklist": ["Review tray width and bend space", "Check access below and beside trays", "Coordinate with mechanical services early"],
    },
    {
        "slug": "009-dynamo-for-repetitive-mep-tasks",
        "title": "When Dynamo Can Save Time in Repetitive MEP BIM Tasks",
        "focus": "where automation helps and where manual engineering judgment is still required",
        "case_example": "Renaming hundreds of parameters can be automated, but deciding whether a system is correctly designed still needs human review.",
        "checklist": ["Automate repetitive data edits", "Keep a backup before batch changes", "Validate results with a sample schedule"],
    },
    {
        "slug": "010-mep-bim-learning-habit",
        "title": "How to Build a Daily MEP BIM Learning Habit",
        "focus": "small daily lessons that improve long-term BIM judgment",
        "case_example": "A junior modeler who studies one practical issue each day can build stronger coordination sense than someone who only memorizes commands.",
        "checklist": ["Study one real issue daily", "Write one lesson learned", "Apply the lesson to a current model"],
    },
]


TOPIC_AREAS = [
    {
        "area": "MEP BIM coordination",
        "subjects": ["ceiling coordination", "plantroom layout", "shaft planning", "corridor congestion", "riser coordination", "equipment access", "coordination meeting preparation"],
        "checks": ["Review all linked disciplines together", "Separate design issues from modeling issues", "Assign a clear owner for each action"],
    },
    {
        "area": "HVAC duct BIM",
        "subjects": ["duct sizing review", "air terminal placement", "VAV box access", "fire damper coordination", "duct insulation clearance", "AHU connection logic", "diffuser coordination"],
        "checks": ["Check duct height and insulation", "Confirm access panels before approval", "Compare model routes with mechanical intent"],
    },
    {
        "area": "HVAC piping BIM",
        "subjects": ["chilled water loops", "hot water loops", "condenser water routing", "pump room coordination", "valve operation space", "pipe slope review", "strainer and air vent placement"],
        "checks": ["Confirm supply and return separation", "Review valve and flange access", "Check pipe data against equipment schedules"],
    },
    {
        "area": "plumbing and sanitary BIM",
        "subjects": ["drainage slope", "cleanout access", "water supply zoning", "pump discharge routing", "fixture connection review", "pipe sleeve coordination", "inspection space planning"],
        "checks": ["Check slope and invert levels", "Review access to cleanouts", "Coordinate sleeves before structural freezing"],
    },
    {
        "area": "fire protection BIM",
        "subjects": ["sprinkler head layout", "main pipe routing", "branch pipe clearance", "fire pump room layout", "valve station access", "alarm valve coordination", "ceiling device conflicts"],
        "checks": ["Review sprinkler coverage intent", "Check ceiling device conflicts", "Confirm valve station access"],
    },
    {
        "area": "electrical BIM",
        "subjects": ["cable tray routing", "panel room clearance", "conduit congestion", "lighting coordination", "busduct planning", "low-voltage tray separation", "equipment maintenance zones"],
        "checks": ["Review tray width and bend radius", "Confirm panel working clearance", "Coordinate early with HVAC routes"],
    },
    {
        "area": "Revit MEP workflow",
        "subjects": ["system classification", "shared parameters", "view templates", "worksets", "family connectors", "schedules", "model warnings"],
        "checks": ["Check naming rules", "Test data in schedules", "Keep view standards consistent"],
    },
    {
        "area": "Navisworks workflow",
        "subjects": ["clash grouping", "search sets", "clash status tracking", "viewpoints", "issue reports", "coordination zones", "weekly model comparison"],
        "checks": ["Group issues by cause", "Use saved viewpoints consistently", "Track status between meetings"],
    },
    {
        "area": "BIM data and QA",
        "subjects": ["model health checks", "parameter completeness", "naming standards", "LOD review", "handover data", "quantity takeoff readiness", "model audit reports"],
        "checks": ["Check required parameters", "Validate sample quantities", "Document assumptions clearly"],
    },
    {
        "area": "BIM automation",
        "subjects": ["Dynamo batch checks", "Excel data exchange", "Python scripts", "Revit API ideas", "schedule automation", "parameter cleanup", "report generation"],
        "checks": ["Automate repetitive work only", "Keep a rollback copy", "Validate results before sharing"],
    },
    {
        "area": "project case studies",
        "subjects": ["hospital MEP BIM", "data center coordination", "airport BIM workflow", "factory utility routing", "commercial complex ceilings", "hotel shaft planning", "office tower plantrooms"],
        "checks": ["Start from project risk", "Connect BIM checks to site decisions", "Record lessons learned"],
    },
    {
        "area": "daily BIM career training",
        "subjects": ["junior modeler habits", "coordinator communication", "BIM review notes", "meeting minutes", "RFI preparation", "portfolio building", "Telegram lesson design"],
        "checks": ["Learn one practical topic daily", "Write one short review note", "Apply the lesson to a real model"],
    },
]


LESSON_ANGLES = [
    "Practical Rules for",
    "Common Mistakes in",
    "A Simple Checklist for",
    "How to Review",
    "Why BIM Coordinators Should Understand",
    "Real Project Lessons From",
    "Model QA Tips for",
    "Coordination Meeting Notes on",
    "Data Quality Basics for",
    "Daily Training Guide to",
    "Before Construction: Check",
    "How LUA BIM LABS Teaches",
    "From Revit Model to Site Decision:",
    # Added to extend unique post cycle and cover broader BIM perspectives
    "Step-by-Step Guide to",
    "What Site Engineers Need to Know About",
    "Comparing Approaches to",
    "Handover Checklist for",
    "Junior BIM Modeler's Guide to",
    "How Contractors Interpret",
    "Five Key Questions About",
    "Owner and FM Requirements for",
    "Troubleshooting",
    "Field vs. Model: Understanding",
    "Cost and Schedule Implications of",
    "ISO 19650 and",
]


def _load_env() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _topic_cycle_length() -> int:
    return len(TOPIC_AREAS) * max(len(a["subjects"]) for a in TOPIC_AREAS) * len(LESSON_ANGLES)


def _send_telegram(message: str) -> None:
    _load_env()
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        print("Telegram credentials missing, skipping notification.")
        return
    payload = json.dumps({"chat_id": chat_id, "text": message}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as exc:
        print(f"Telegram notification failed: {exc}")


def _check_duplicate_warning(next_index: int, warn_days: int) -> None:
    cycle = _topic_cycle_length()
    position = (next_index - 1) % cycle
    remaining = cycle - position
    if remaining <= warn_days:
        message = (
            f"⚠️ [LUA BIM LABS 블로그 알림]\n"
            f"블로그 주제 소진 임박: {remaining}일 후 주제가 반복됩니다.\n"
            f"현재 인덱스: {next_index} / 사이클: {cycle}\n\n"
            f"TOPIC_AREAS 또는 LESSON_ANGLES에 새 주제를 추가해주세요.\n"
            f"파일: scripts/daily_blogger_queue_publish.py"
        )
        print(message)
        _send_telegram(message)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:80]


def normalize_acronyms(text: str) -> str:
    replacements = {
        "Bim": "BIM",
        "Mep": "MEP",
        "Hvac": "HVAC",
        "Qa": "QA",
        "Api": "API",
        "Rfi": "RFI",
        "Vav": "VAV",
        "Ahu": "AHU",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def generated_topic(index: int) -> dict[str, Any]:
    area = TOPIC_AREAS[(index - 1) % len(TOPIC_AREAS)]
    subject = area["subjects"][((index - 1) // len(TOPIC_AREAS)) % len(area["subjects"])]
    angle = LESSON_ANGLES[(index - 1) % len(LESSON_ANGLES)]
    title = normalize_acronyms(f"{angle} {subject.title()} in {area['area'].title()}")
    focus = f"practical {subject} decisions in {area['area']}"
    case_example = (
        f"In a real project, {subject} can look acceptable in a model view, "
        f"but still create coordination risk when installation sequence, access, "
        f"clearance, and model data are reviewed together."
    )
    return {
        "slug": f"{index:03d}-{slugify(title)}",
        "title": title,
        "focus": focus,
        "case_example": case_example,
        "checklist": area["checks"],
    }


def annual_topics(total: int = 365) -> list[dict[str, Any]]:
    topics = list(SEED_TOPICS)
    for index in range(len(SEED_TOPICS) + 1, total + 1):
        topics.append(generated_topic(index))
    return topics


def load_service_links(config_path: Path) -> dict[str, str]:
    if not config_path.exists():
        return {}
    data = json.loads(config_path.read_text(encoding="utf-8"))
    links = data.get("service_links", {})
    starter = next((plan for plan in data.get("plans", []) if plan.get("id") == "starter"), {})
    return {
        "application_form": links.get("application_form", ""),
        "contact_email": links.get("contact_email", ""),
        "telegram_contact": links.get("telegram_contact", ""),
        "paypal_payment_link": starter.get("paypal_payment_link", ""),
        "paypal_subscription_link": starter.get("paypal_subscription_link", ""),
    }


def render_service_cta(args: argparse.Namespace) -> str:
    links = load_service_links(Path(args.service_config))
    application_form = html.escape(links.get("application_form", ""))
    paypal_link = html.escape(links.get("paypal_payment_link", ""))
    subscription_link = html.escape(links.get("paypal_subscription_link", ""))
    telegram_contact = html.escape(links.get("telegram_contact", ""))
    contact_email = html.escape(links.get("contact_email", ""))

    lines = [
        "<h2>Personalized MEP BIM Tutor</h2>",
        "<p>LUA BIM LABS is launching the Starter plan for Personal MEP BIM Tutor through Telegram. The first public offer is simple: one practical MEP BIM lesson every day, written for beginners and early-stage BIM learners who want a steady learning habit.</p>",
        "<p><strong>Starter Plan:</strong> USD 39/month. Personal Tutor, Coordinator Mentor, and Project Mentor are planned as Coming Soon services.</p>",
        "<p>The application form includes the PayPal payment link and onboarding questions. Please complete payment and submit the form with the email used for PayPal payment.</p>",
    ]

    if application_form or paypal_link or subscription_link:
        lines.append("<ul>")
        if application_form:
            lines.append(f'  <li><a href="{application_form}">Apply for the Starter Plan</a></li>')
        if paypal_link:
            lines.append(f'  <li><a href="{paypal_link}">Pay with PayPal</a></li>')
        if subscription_link:
            lines.append(f'  <li><a href="{subscription_link}">Subscribe with PayPal</a></li>')
        if telegram_contact:
            lines.append(f'  <li><a href="{telegram_contact}">Contact LUA BIM LABS on Telegram</a></li>')
        lines.append("</ul>")
    else:
        lines.append("<p>The Starter application and PayPal payment link will be announced soon. Follow this blog for the opening notice.</p>")

    if contact_email:
        lines.append(f"<p>Contact: {contact_email}</p>")

    return "\n".join(lines)


def render_post(topic: dict[str, Any], args: argparse.Namespace | None = None) -> str:
    title = html.escape(topic["title"])
    focus = html.escape(topic["focus"])
    case_example = html.escape(topic["case_example"])
    checklist = topic.get("checklist", [])
    checklist_html = "\n".join(f"  <li>{html.escape(item)}</li>" for item in checklist)
    service_cta = render_service_cta(args) if args else ""

    return f"""<p><strong>{title}</strong></p>

<p>Today's LUA BIM LABS lesson focuses on {focus}. In real construction projects, MEP BIM quality is measured not only by clean geometry, but also by whether the model supports coordination, installation, maintenance, and reliable project decisions.</p>

<h2>Why This Topic Matters</h2>

<p>MEP systems compete for limited building space. Ducts, pipes, cable trays, equipment, valves, access panels, insulation, slopes, and maintenance zones must work together. A model can look visually acceptable and still create problems if the underlying MEP logic is weak.</p>

<h2>Practical Case Example</h2>

<p>{case_example}</p>

<h2>Practical Workflow</h2>

<p>Start by checking the engineering intent, then review the Revit model data, and finally confirm the coordination condition in context with architectural, structural, and other MEP disciplines. Good MEP BIM coordination is not a one-click clash test. It is a repeatable review process.</p>

<h2>Quick Checklist</h2>

<ul>
{checklist_html}
</ul>

<h2>LUA BIM LABS Tip</h2>

<p>Do not treat MEP BIM as simple 3D drafting. Treat it as a practical decision system. The best BIM modelers understand both software behavior and engineering consequences.</p>

{service_cta}
"""


def seed_topics(queue_dir: Path) -> None:
    queue_dir.mkdir(parents=True, exist_ok=True)
    for index, topic in enumerate(annual_topics(), start=1):
        path = queue_dir / f"{index:03d}-{topic['slug']}.json"
        if path.exists():
            continue
        payload = {
            "blogUrl": DEFAULT_BLOG_URL,
            "labels": DEFAULT_LABELS,
            "draft": False,
            **topic,
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def next_generated_index(state_file: Path, log_file: Path | None) -> int:
    if state_file.exists():
        data = json.loads(state_file.read_text(encoding="utf-8"))
        return int(data.get("next_index", 366))

    published_count = 0
    if log_file and log_file.exists():
        published_count = sum(1 for line in log_file.read_text(encoding="utf-8").splitlines() if line.strip())
    return max(366, published_count + 1)


def queue_generated_daily_topic(
    queue_dir: Path,
    state_file: Path,
    log_file: Path | None,
    warn_days: int = DEFAULT_DUPLICATE_WARN_DAYS,
) -> Path:
    queue_dir.mkdir(parents=True, exist_ok=True)
    index = next_generated_index(state_file, log_file)
    _check_duplicate_warning(index, warn_days)
    topic = generated_topic(index)
    path = queue_dir / f"{index:03d}-{topic['slug']}.json"
    payload = {
        "blogUrl": DEFAULT_BLOG_URL,
        "labels": DEFAULT_LABELS,
        "draft": False,
        **topic,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps({"next_index": index + 1}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def next_topic_file(queue_dir: Path) -> Path | None:
    files = sorted(queue_dir.glob("*.json"))
    return files[0] if files else None


def markdown_escape(text: str) -> str:
    return text.replace("|", "\\|").strip()


def write_obsidian_note(topic: dict[str, Any], url: str, obsidian_dir: Path) -> Path:
    obsidian_dir.mkdir(parents=True, exist_ok=True)
    title = topic["title"]
    slug = slugify(title)
    note_path = obsidian_dir / f"{date.today().isoformat()} - {slug}.md"
    checklist = "\n".join(f"- {item}" for item in topic.get("checklist", []))
    labels = topic.get("labels", DEFAULT_LABELS)
    tags = "\n".join(f"  - {slugify(label)}" for label in labels)
    content = f"""---
type: blog-knowledge
source: blogger
brand: LUA BIM LABS
published: {date.today().isoformat()}
url: {url}
tags:
{tags}
---

# {title}

## Blog Link

{url}

## Knowledge Insight

{topic.get("focus", "")}

MEP BIM knowledge should be retained when it improves project judgment, model quality, coordination decisions, or repeatable education. This topic is useful for LUA BIM LABS because it connects software workflow with engineering and construction consequences.

## Educational Insight

This topic can be reused as a short daily lesson for engineers, BIM modelers, and coordinators. It supports the LUA BIM LABS Telegram training model by turning one focused issue into a practical checklist and discussion point.

## Practical Case

{topic.get("case_example", "")}

## Checklist

{checklist}

## Reuse Ideas

- Convert into a Telegram daily MEP BIM lesson.
- Expand into a Revit/Navisworks hands-on exercise.
- Use as a short onboarding discussion for junior BIM staff.
- Link to future case studies, QA checklists, or automation scripts.
"""
    note_path.write_text(content, encoding="utf-8")
    return note_path


def publish_topic(args: argparse.Namespace, topic_file: Path) -> str:
    from googleapiclient.discovery import build

    topic = json.loads(topic_file.read_text(encoding="utf-8"))
    content = render_post(topic, args)
    body = {
        "kind": "blogger#post",
        "title": topic["title"],
        "content": content,
        "labels": topic.get("labels", DEFAULT_LABELS),
    }

    if args.dry_run:
        print(json.dumps({"source": str(topic_file), **body}, ensure_ascii=False, indent=2))
        return "dry-run"

    creds = load_credentials(
        Path(args.client_secrets),
        Path(args.token),
        args.client_id_env,
        args.client_secret_env,
        args.oauth_port,
    )
    service = build("blogger", "v3", credentials=creds)
    blog_id = resolve_blog_id(service, args.blog_id, topic.get("blogUrl", args.blog_url))
    post = service.posts().insert(
        blogId=blog_id,
        body=body,
        isDraft=bool(topic.get("draft", args.draft)),
    ).execute()
    url = post.get("url", "")

    if args.obsidian_dir:
        write_obsidian_note(topic, url, Path(args.obsidian_dir))

    if args.delete_after_publish:
        topic_file.unlink()

    if args.log_file:
        log_path = Path(args.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as log:
            log.write(json.dumps({"date": date.today().isoformat(), "title": topic["title"], "url": url}, ensure_ascii=False) + "\n")

    return url


def publish_all(args: argparse.Namespace, queue_dir: Path) -> None:
    from googleapiclient.errors import HttpError

    count = 0
    rate_limit_retries = 0
    while True:
        topic_file = next_topic_file(queue_dir)
        if not topic_file:
            print(f"Queue empty. Published {count} posts.")
            if args.enable_daily_agent_on_empty:
                enable_daily_agent(Path(args.daily_agent_plist))
            return
        try:
            url = publish_topic(args, topic_file)
        except HttpError as exc:
            status = getattr(exc.resp, "status", None)
            if status == 429 and rate_limit_retries < args.max_rate_limit_retries:
                rate_limit_retries += 1
                print(
                    f"Rate limit hit. Sleeping {args.rate_limit_sleep_seconds} seconds "
                    f"before retry {rate_limit_retries}/{args.max_rate_limit_retries}.",
                    flush=True,
                )
                time.sleep(args.rate_limit_sleep_seconds)
                continue
            raise
        rate_limit_retries = 0
        count += 1
        print(f"[{count}] Published: {url}", flush=True)
        if args.sleep_seconds:
            time.sleep(args.sleep_seconds)


def enable_daily_agent(plist_path: Path) -> None:
    uid = str(os.getuid())
    subprocess.run(["launchctl", "bootout", f"gui/{uid}", str(plist_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["launchctl", "bootstrap", f"gui/{uid}", str(plist_path)], check=True)
    print(f"Enabled daily Blogger agent: {plist_path}", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish one queued LUA BIM LABS Blogger post.")
    parser.add_argument("--queue-dir", default="content/blogger_queue")
    parser.add_argument("--seed-topics", action="store_true")
    parser.add_argument("--client-secrets", default="config/blogger/client_secret.json")
    parser.add_argument("--client-id-env", default="BLOGGER_CLIENT_ID")
    parser.add_argument("--client-secret-env", default="BLOGGER_CLIENT_SECRET")
    parser.add_argument("--token", default="config/blogger/token.json")
    parser.add_argument("--oauth-port", type=int, default=8080)
    parser.add_argument("--blog-id")
    parser.add_argument("--blog-url", default=DEFAULT_BLOG_URL)
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--delete-after-publish", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--log-file", default="logs/blogger_daily_publish.jsonl")
    parser.add_argument("--obsidian-dir", default="obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/Blog_MEP_BIM")
    parser.add_argument("--publish-all", action="store_true")
    parser.add_argument("--sleep-seconds", type=float, default=1.0)
    parser.add_argument("--rate-limit-sleep-seconds", type=float, default=600.0)
    parser.add_argument("--max-rate-limit-retries", type=int, default=200)
    parser.add_argument("--lock-file", default=DEFAULT_LOCK_FILE)
    parser.add_argument("--generate-when-empty", action="store_true")
    parser.add_argument("--state-file", default=DEFAULT_STATE_FILE)
    parser.add_argument("--enable-daily-agent-on-empty", action="store_true")
    parser.add_argument("--daily-agent-plist", default=DEFAULT_DAILY_AGENT_PLIST)
    parser.add_argument("--service-config", default=DEFAULT_SERVICE_CONFIG)
    parser.add_argument("--duplicate-warn-days", type=int, default=DEFAULT_DUPLICATE_WARN_DAYS)
    return parser.parse_args()


@contextmanager
def single_instance(lock_file: Path):
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(lock_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.write(fd, str(os.getpid()).encode("utf-8"))
        yield
    finally:
        os.close(fd)
        try:
            lock_file.unlink()
        except FileNotFoundError:
            pass


def main() -> None:
    args = parse_args()
    queue_dir = Path(args.queue_dir)
    if args.seed_topics:
        seed_topics(queue_dir)
        print(f"Seeded topics in {queue_dir}")
        return

    try:
        with single_instance(Path(args.lock_file)):
            if args.publish_all:
                publish_all(args, queue_dir)
                return

            topic_file = next_topic_file(queue_dir)
            if not topic_file and args.generate_when_empty:
                topic_file = queue_generated_daily_topic(
                    queue_dir,
                    Path(args.state_file),
                    Path(args.log_file) if args.log_file else None,
                    warn_days=args.duplicate_warn_days,
                )
            if not topic_file:
                print(f"No queued topics in {queue_dir}")
                return

            url = publish_topic(args, topic_file)
            print(f"Published: {url}")
    except FileExistsError:
        print(f"Another Blogger queue publisher is already running: {args.lock_file}")


if __name__ == "__main__":
    main()

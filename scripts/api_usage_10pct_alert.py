#!/usr/bin/env python3
"""Send Telegram alerts when free API usage crosses 10% milestones."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "api_usage_alerts.json"
DEFAULT_STATE = PROJECT_ROOT / "runtime" / "api_usage_alert_state.json"
DEFAULT_LOG = PROJECT_ROOT / "logs" / "api_usage_alerts.log"


def load_dotenv() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_log(message: str) -> None:
    DEFAULT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with DEFAULT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(message.rstrip() + "\n")


def send_telegram(text: str, dry_run: bool = False) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if dry_run:
        print(text)
        return True
    if not token or not chat_id:
        append_log("telegram=skipped reason=missing_config")
        return False
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            ok = resp.status == 200
    except Exception as exc:  # noqa: BLE001
        append_log(f"telegram=failed {type(exc).__name__}: {exc}")
        return False
    append_log(f"telegram={'sent' if ok else 'failed'}")
    return ok


def period_key(period: str) -> str:
    now = datetime.now()
    if period == "daily":
        return now.strftime("%Y-%m-%d")
    if period == "yearly":
        return now.strftime("%Y")
    return now.strftime("%Y-%m")


def resolve_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    return path if path.is_absolute() else PROJECT_ROOT / path


def read_usage_from_json(source: dict[str, Any]) -> float:
    path = resolve_path(source["path"])
    data = read_json(path, {})
    key = source.get("used_key", "used")
    current: Any = data
    for part in key.split("."):
        current = current[part]
    return float(current)


def read_usage_from_sqlite(source: dict[str, Any]) -> float:
    path = resolve_path(source["path"])
    if not path.exists():
        return 0.0
    query = source["query"]
    params = source.get("params", [])
    with sqlite3.connect(path) as conn:
        row = conn.execute(query, params).fetchone()
    if not row or row[0] is None:
        return 0.0
    return float(row[0])


def read_usage_from_command(source: dict[str, Any]) -> float:
    result = subprocess.run(
        source["command"],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        timeout=int(source.get("timeout_seconds", 20)),
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "command failed").strip())
    return float((result.stdout or "").strip().splitlines()[-1])


def read_used(source: dict[str, Any]) -> float:
    source_type = source.get("type", "json")
    if source_type == "json":
        return read_usage_from_json(source)
    if source_type == "sqlite_sum":
        return read_usage_from_sqlite(source)
    if source_type == "command":
        return read_usage_from_command(source)
    if source_type == "static":
        return float(source.get("used", 0))
    raise ValueError(f"Unsupported source type: {source_type}")


def reached_thresholds(percent: float, step: int) -> list[int]:
    capped = max(0, min(100, int(percent)))
    return [value for value in range(step, 101, step) if capped >= value]


def format_alert(monitor: dict[str, Any], used: float, limit: float, percent: float, threshold: int) -> str:
    unit = monitor.get("unit", "units")
    reset_hint = monitor.get("reset_hint", "")
    remaining = max(0.0, limit - used)
    reset_line = f"\nReset: {reset_hint}" if reset_hint else ""
    return (
        "[API 사용량 알림]\n"
        f"{monitor.get('name', monitor['id'])}: {threshold}% 도달\n"
        f"현재 사용량: {used:,.0f} / {limit:,.0f} {unit} ({percent:.1f}%)\n"
        f"남은 사용량: {remaining:,.0f} {unit}"
        f"{reset_line}"
    )


def check_monitors(config_path: Path, state_path: Path, dry_run: bool = False, notify_all: bool = False) -> int:
    load_dotenv()
    config = read_json(config_path, {"monitors": []})
    state = read_json(state_path, {"monitors": {}})
    step = int(config.get("threshold_step_percent", 10))
    sent_count = 0

    for monitor in config.get("monitors", []):
        if not monitor.get("enabled", True):
            continue
        monitor_id = monitor["id"]
        limit = float(monitor["limit"])
        if limit <= 0:
            append_log(f"{monitor_id}=skipped reason=invalid_limit")
            continue
        current_period = period_key(monitor.get("period", "monthly"))
        monitor_state = state.setdefault("monitors", {}).setdefault(monitor_id, {})
        if monitor_state.get("period_key") != current_period:
            monitor_state.clear()
            monitor_state["period_key"] = current_period
            monitor_state["sent_thresholds"] = []

        try:
            used = read_used(monitor["source"])
        except Exception as exc:  # noqa: BLE001
            append_log(f"{monitor_id}=failed {type(exc).__name__}: {exc}")
            continue

        percent = (used / limit) * 100
        sent_thresholds = set(int(value) for value in monitor_state.get("sent_thresholds", []))
        due = [value for value in reached_thresholds(percent, step) if value not in sent_thresholds]
        if notify_all and not due:
            due = [max(0, min(100, int(percent)))]
        for threshold in due:
            if send_telegram(format_alert(monitor, used, limit, percent, threshold), dry_run=dry_run):
                sent_thresholds.add(threshold)
                sent_count += 1

        monitor_state.update(
            {
                "period_key": current_period,
                "last_checked_at": datetime.now().isoformat(timespec="seconds"),
                "last_used": used,
                "last_percent": round(percent, 2),
                "sent_thresholds": sorted(sent_thresholds),
            }
        )
        append_log(f"{monitor_id}=checked used={used:.0f} limit={limit:.0f} percent={percent:.2f}")

    if not dry_run:
        write_json(state_path, state)
    return sent_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Alert every 10% of free API usage.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--state", default=str(DEFAULT_STATE))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--notify-all", action="store_true", help="Send a status alert even when no new threshold is crossed.")
    args = parser.parse_args()
    sent = check_monitors(resolve_path(args.config), resolve_path(args.state), args.dry_run, args.notify_all)
    print(f"alerts_sent={sent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

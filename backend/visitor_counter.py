from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any


class VisitorCounter:
    def __init__(self, path: Path):
        self.path = Path(path)

    @staticmethod
    def session_key(ip_address: str, day: dt.date) -> str:
        raw_ip = (ip_address or "unknown").strip() or "unknown"
        return hashlib.sha256(f"{raw_ip}:{day.isoformat()}".encode()).hexdigest()[:16]

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        return data if isinstance(data, dict) else {}

    def save(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def total(self) -> int:
        data = self.load()
        try:
            return int(data.get("total", 0))
        except (TypeError, ValueError):
            return 0

    def record(self, ip_address: str, *, day: dt.date | None = None) -> int:
        today = day or dt.date.today()
        key = self.session_key(ip_address, today)
        data = self.load()

        try:
            total = int(data.get("total", 0))
        except (TypeError, ValueError):
            total = 0
        seen = data.get("seen", {})
        if not isinstance(seen, dict):
            seen = {}

        if key not in seen:
            total += 1
            seen[key] = today.isoformat()
            cutoff = (today - dt.timedelta(days=7)).isoformat()
            seen = {item_key: item_day for item_key, item_day in seen.items() if str(item_day) >= cutoff}
            self.save({"total": total, "seen": seen})

        return total


def client_ip_from_headers(headers: dict[str, str] | Any, fallback: str = "unknown") -> str:
    forwarded = headers.get("x-forwarded-for", "") if headers else ""
    first_forwarded = str(forwarded).split(",")[0].strip()
    return first_forwarded or fallback or "unknown"

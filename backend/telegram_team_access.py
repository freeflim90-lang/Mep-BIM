from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def parse_allowed_chat_ids(raw: str | None) -> set[str]:
    return {item.strip() for item in (raw or "").split(",") if item.strip()}


def load_enabled_team_chat_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"⚠️ [Telegram team registry] {exc}")
        return set()
    ids: set[str] = set()
    for user in registry.get("users", []) if isinstance(registry, dict) else []:
        if not isinstance(user, dict):
            continue
        chat_id = str(user.get("telegram_chat_id", "")).strip()
        if chat_id and user.get("status") != "disabled":
            ids.add(chat_id)
    return ids


def allowed_team_chat_ids(*, env_raw: str | None, registry_path: Path) -> set[str]:
    return parse_allowed_chat_ids(env_raw) | load_enabled_team_chat_ids(registry_path)


def update_chat_id(update: Any) -> str:
    return str(update.effective_chat.id) if getattr(update, "effective_chat", None) else ""


def telegram_chat_allowed(*, update: Any, env_raw: str | None, registry_path: Path) -> bool:
    allowed = allowed_team_chat_ids(env_raw=env_raw, registry_path=registry_path)
    if not allowed:
        return True
    return update_chat_id(update) in allowed

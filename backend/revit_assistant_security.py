from __future__ import annotations

import os
import secrets
from pathlib import Path
from typing import Mapping, Optional

from fastapi import HTTPException


def extract_bearer_token(authorization: Optional[str]) -> Optional[str]:
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        return None
    return token.strip()


def configured_revit_assistant_api_keys(env: Mapping[str, str] = os.environ) -> set[str]:
    raw_tokens = f"{env.get('LUA_CHAT_TOKEN', '')},{env.get('REVIT_ASSISTANT_API_KEYS', '')}"
    return {item.strip() for item in raw_tokens.split(",") if item.strip()}


def require_revit_assistant_api_key(
    api_key: Optional[str],
    env: Mapping[str, str] = os.environ,
) -> None:
    configured = configured_revit_assistant_api_keys(env)
    if not configured:
        return

    candidate = api_key.strip() if api_key else ""
    if not candidate or not any(secrets.compare_digest(candidate, allowed) for allowed in configured):
        raise HTTPException(status_code=401, detail="invalid revit assistant api key")


def resolve_revit_feedback_note_path(
    note_path: str,
    *,
    project_root: Path,
    allowed_root: Path,
) -> Path | None:
    if not note_path.strip():
        return None
    requested = Path(note_path)
    if requested.is_absolute():
        return None

    resolved = (project_root / requested).resolve()
    try:
        resolved.relative_to(allowed_root.resolve())
    except ValueError:
        return None
    return resolved

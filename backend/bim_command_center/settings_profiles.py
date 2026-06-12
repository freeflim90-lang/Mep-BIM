from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


CURRENT_PROFILE_VERSION = "1.0"


class ProfileScope(str, Enum):
    OFFICE = "office"
    PROJECT = "project"


class SettingsProfileError(ValueError):
    pass


@dataclass(frozen=True)
class SettingsProfile:
    name: str
    scope: ProfileScope
    version: str = CURRENT_PROFILE_VERSION
    settings: dict[str, Any] = field(default_factory=dict)
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "scope": self.scope.value,
            "version": self.version,
            "description": self.description,
            "settings": self.settings,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SettingsProfile":
        if not isinstance(payload, dict):
            raise SettingsProfileError("Profile payload must be an object.")
        name = payload.get("name")
        if not isinstance(name, str) or not name.strip():
            raise SettingsProfileError("Profile name is required.")
        version = payload.get("version")
        if version != CURRENT_PROFILE_VERSION:
            raise SettingsProfileError(f"Unsupported profile version: {version!r}.")
        try:
            scope = ProfileScope(payload.get("scope"))
        except ValueError as exc:
            raise SettingsProfileError(f"Unsupported profile scope: {payload.get('scope')!r}.") from exc
        settings = payload.get("settings", {})
        if not isinstance(settings, dict):
            raise SettingsProfileError("Profile settings must be an object.")
        description = payload.get("description", "")
        if not isinstance(description, str):
            raise SettingsProfileError("Profile description must be a string.")
        return cls(
            name=name.strip(),
            scope=scope,
            version=version,
            description=description,
            settings=settings,
        )


class SettingsProfileStore:
    def __init__(self, root: Path):
        self.root = Path(root)

    def scope_dir(self, scope: ProfileScope) -> Path:
        return self.root / scope.value

    def profile_path(self, scope: ProfileScope, name: str) -> Path:
        safe_name = name.strip().replace("/", "_").replace("\\", "_")
        if not safe_name:
            raise SettingsProfileError("Profile name is required.")
        return self.scope_dir(scope) / f"{safe_name}.json"

    def save(self, profile: SettingsProfile) -> Path:
        profile = SettingsProfile.from_dict(profile.to_dict())
        path = self.profile_path(profile.scope, profile.name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def load(self, scope: ProfileScope, name: str) -> SettingsProfile:
        path = self.profile_path(scope, name)
        if not path.exists():
            raise SettingsProfileError(f"Profile not found: {scope.value}/{name}")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SettingsProfileError(f"Broken profile JSON: {path}") from exc
        profile = SettingsProfile.from_dict(payload)
        if profile.scope != scope:
            raise SettingsProfileError(f"Profile scope mismatch: expected {scope.value}, got {profile.scope.value}")
        return profile

    def list_profiles(self, scope: ProfileScope | None = None) -> list[dict[str, Any]]:
        scopes = [scope] if scope else [ProfileScope.OFFICE, ProfileScope.PROJECT]
        rows: list[dict[str, Any]] = []
        for item_scope in scopes:
            folder = self.scope_dir(item_scope)
            if not folder.exists():
                continue
            for path in sorted(folder.glob("*.json")):
                try:
                    profile = self.load(item_scope, path.stem)
                    rows.append({
                        "name": profile.name,
                        "scope": profile.scope.value,
                        "version": profile.version,
                        "description": profile.description,
                        "path": path.as_posix(),
                    })
                except SettingsProfileError as exc:
                    rows.append({
                        "name": path.stem,
                        "scope": item_scope.value,
                        "version": None,
                        "description": "",
                        "path": path.as_posix(),
                        "error": str(exc),
                    })
        return rows


def default_profile_store(root: str | Path | None = None) -> SettingsProfileStore:
    if root is None:
        from backend.core.paths import BIM_COMMAND_CENTER_DIR
        root = BIM_COMMAND_CENTER_DIR / "settings_profiles"
    return SettingsProfileStore(Path(root))


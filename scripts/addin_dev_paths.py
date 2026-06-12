from __future__ import annotations

import os
from pathlib import Path


ENV_NAME = "BCC_ADDIN_DEV_SOURCE_ROOT"


def addin_dev_source_root(env: dict[str, str] | None = None) -> Path | None:
    raw = (env or os.environ).get(ENV_NAME, "").strip()
    return Path(raw).expanduser() if raw else None


def require_addin_dev_source_root(env: dict[str, str] | None = None) -> Path:
    root = addin_dev_source_root(env)
    if root is None:
        raise SystemExit(
            f"{ENV_NAME} is required. Point it at the external add-in development source root."
        )
    if not root.exists():
        raise SystemExit(f"{ENV_NAME} does not exist: {root}")
    return root

